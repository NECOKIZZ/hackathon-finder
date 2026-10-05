"""ETF League settlement prototype.

All money is integer micro-dollars (1 USD = 1_000_000) so conservation can be
checked exactly. Weights use floats; integer allocation uses largest remainder.

Model (see ideas/003-etf-league.md):
- Each ETF is a team: one creator plus backers. Every member stakes a fixed $5.
- Score: ETF % return over the round (basis points), stocks only.
- Distance D_i = best return - return_i. Median gate over ETFs (one ETF, one vote).
- Winners: D_i < median D (or the best-coalition rule). Losers forfeit their stakes.
- Rake on the transferred amount, split platform / season pot.
- Winning teams share the pot by weight = team_stake**alpha * accuracy.
- Gains per team are capped at cap_multiple * team_stake; amounts the winners
  cannot absorb are refunded to the losers (unmatched stake).
- Inside a team: equal per stake, then creator takes creator_fee of backers' gains.
- Thin-pot top-up from the season pot when the pot is tiny vs winning stakes.
"""
from dataclasses import dataclass, field

USD = 1_000_000
STAKE = 5 * USD


@dataclass
class Params:
    alpha: float = 1.0           # 1 = stake-weighted (Kickoff), 0 = one team one share
    gamma: int = 6               # accuracy sharpness (Kickoff/Trepa)
    cap_multiple: int = 100      # max gain per team = cap * team stake
    rake_bps: int = 1000         # 10% of transferred losing stakes
    platform_share_bps: int = 5000  # half of rake to platform, half to season pot
    creator_fee_bps: int = 1000  # creator takes 10% of backers' gains
    topup_bps: int = 500         # top up pot to 5% of winning stakes if thin
    min_etfs: int = 4
    max_backers: int = 20


@dataclass
class Team:
    name: str
    ret_bps: int                 # ETF % return over the round, in basis points
    backers: int = 0             # number of backers (each stakes STAKE)
    basket: str = ""             # composition key (tokens + weights, rounded)

    @property
    def members(self):
        return 1 + self.backers

    @property
    def stake(self):
        return self.members * STAKE


@dataclass
class Result:
    void: bool
    reason: str = ""
    winners: list = field(default_factory=list)
    team_payout: dict = field(default_factory=dict)   # total returned to team (stake + gain)
    creator_payout: dict = field(default_factory=dict)
    backer_payout_each: dict = field(default_factory=dict)
    platform: int = 0
    season_in: int = 0
    season_out: int = 0
    refunded: int = 0


def _alloc(total, weights):
    """Split integer `total` by float weights, exact sum (largest remainder)."""
    s = sum(weights)
    if total == 0 or s == 0:
        return [0] * len(weights)
    raw = [total * w / s for w in weights]
    base = [int(x) for x in raw]
    rem = total - sum(base)
    order = sorted(range(len(raw)), key=lambda i: raw[i] - base[i], reverse=True)
    for i in order[:rem]:
        base[i] += 1
    return base


def merge_clones(teams, max_backers=None):
    """ETFs with the same basket are one team: later copies join the first one.

    The first-created ETF keeps the creator role; copies' members become its
    backers. Without this, copying an ETF beats backing it (each copy would
    count as its own ETF in the median gate). Returns (merged_teams, mapping).
    """
    first, merged, mapping = {}, [], {}
    for t in teams:
        key = t.basket or t.name
        if key in first:
            host = first[key]
            host.backers += t.members
            mapping[t.name] = host.name
        else:
            nt = Team(t.name, t.ret_bps, t.backers, t.basket)
            first[key] = nt
            merged.append(nt)
            mapping[t.name] = t.name
    return merged, mapping


def settle(teams, p=Params(), season_pot=0):
    for t in teams:
        if t.backers < 0:
            raise ValueError(f"{t.name}: backers out of range")
    n = len(teams)
    total_stake = sum(t.stake for t in teams)
    refund_all = lambda reason: Result(True, reason, team_payout={t.name: t.stake for t in teams},
                                       creator_payout={t.name: STAKE for t in teams},
                                       backer_payout_each={t.name: STAKE for t in teams})
    if n < p.min_etfs:
        return refund_all("too few ETFs")
    best = max(t.ret_bps for t in teams)
    D = [best - t.ret_bps for t in teams]
    if len(set(D)) == 1:
        return refund_all("all returns equal")

    count_at_best = D.count(0)
    sd = sorted(D)
    # "Top half" gate: m is the (n//2 + 1)-th smallest distance, so with no ties
    # exactly floor(n/2) ETFs win. Ties at the boundary lose (losers always exist).
    k = n // 2 + 1
    m = sd[k - 1]
    if count_at_best * 2 >= n:          # best coalition (Trepa): top group wins together
        win = [d == 0 for d in D]
    else:
        win = [d < m for d in D]
    if not any(win) or all(win):
        return refund_all("degenerate gate")

    acc = []
    for i, t in enumerate(teams):
        if not win[i]:
            acc.append(0.0)
        elif m == 0:
            acc.append(1.0)
        else:
            acc.append((1.0 / (1.0 + D[i] / m)) ** p.gamma)

    W = sum(t.stake for i, t in enumerate(teams) if win[i])
    L = sum(t.stake for i, t in enumerate(teams) if not win[i])

    # Capacity of winners to absorb gains; unmatched losing stake is refunded.
    capacity = sum(p.cap_multiple * t.stake for i, t in enumerate(teams) if win[i])
    keep = 10_000 - p.rake_bps
    transferable = min(L, capacity * 10_000 // keep)
    refunded = L - transferable
    rake = transferable * p.rake_bps // 10_000
    platform = rake * p.platform_share_bps // 10_000
    season_in = rake - platform
    pot = transferable - rake

    season_out = 0
    floor = W * p.topup_bps // 10_000
    if pot < floor and season_pot > 0:
        season_out = min(floor - pot, season_pot)
        pot += season_out

    # Water-fill gains across winning teams with per-team caps.
    idx = [i for i in range(n) if win[i]]
    gains = {i: 0 for i in idx}
    caps = {i: p.cap_multiple * teams[i].stake for i in idx}
    remaining, active = pot, set(idx)
    while remaining > 0 and active:
        order = sorted(active)
        wts = [(teams[i].stake ** p.alpha) * acc[i] for i in order]
        if sum(wts) == 0:
            wts = [1.0] * len(order)
        share = _alloc(remaining, wts)
        remaining = 0
        for i, s in zip(order, share):
            room = caps[i] - gains[i]
            take = min(room, s)
            gains[i] += take
            remaining += s - take
            if gains[i] >= caps[i]:
                active.discard(i)
    # Anything still unplaced (all capped) goes back to losers too.
    refunded += remaining

    # Refunds to losers pro-rata to stake (per team, then equal per member).
    loser_idx = [i for i in range(n) if not win[i]]
    loser_ref = dict(zip(loser_idx, _alloc(refunded, [teams[i].stake for i in loser_idx])))

    res = Result(False, winners=[teams[i].name for i in idx], platform=platform,
                 season_in=season_in, season_out=season_out, refunded=refunded)
    for i, t in enumerate(teams):
        if win[i]:
            g = gains[i]
            per_member = _alloc(g, [1.0] * t.members)       # equal per stake
            creator_gain = per_member[0]
            backer_gains = per_member[1:]
            fee = sum(bg * p.creator_fee_bps // 10_000 for bg in backer_gains)
            creator_total = STAKE + creator_gain + fee
            backer_each = (STAKE + (sum(backer_gains) - fee) / t.backers) if t.backers else None
            res.team_payout[t.name] = t.stake + g
            res.creator_payout[t.name] = creator_total
            res.backer_payout_each[t.name] = backer_each
        else:
            r = loser_ref[i]
            res.team_payout[t.name] = r
            res.creator_payout[t.name] = r / t.members
            res.backer_payout_each[t.name] = (r / t.members) if t.backers else None

    paid = sum(res.team_payout.values())
    assert paid + platform + season_in == total_stake + season_out, "conservation broken"
    return res
