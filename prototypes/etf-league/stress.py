"""Extreme-condition and fairness tests for the ETF League prototype.

Run: python3 stress.py
Every scenario also passes the conservation assert inside settle().
"""
import random
import statistics as st
from league import Params, Team, settle, STAKE, USD

P = Params()
fails = []


def usd(x):
    return f"${x / USD:,.2f}" if x is not None else "—"


def check(name, cond, detail=""):
    print(("  PASS " if cond else "  FAIL ") + name + (f"  ({detail})" if detail else ""))
    if not cond:
        fails.append(name)


def invariants(teams, r, label):
    # Nobody loses more than their stake; winners never get less than their stake back.
    for t in teams:
        tp = r.team_payout[t.name]
        assert tp >= 0, label
        if not r.void and t.name in r.winners:
            assert tp >= t.stake, f"{label}: winner {t.name} got back less than stake"
            assert r.creator_payout[t.name] >= STAKE, label
            if t.backers:
                assert r.backer_payout_each[t.name] >= STAKE - 1, label


def show(teams, r):
    if r.void:
        print(f"    VOID: {r.reason}")
        return
    for t in teams:
        mark = "WIN " if t.name in r.winners else "lose"
        roi = (r.team_payout[t.name] - t.stake) / t.stake * 100
        b = usd(r.backer_payout_each[t.name]) if t.backers else "—"
        print(f"    {mark} {t.name:<10} ret {t.ret_bps/100:+6.2f}%  members {t.members:>2}  "
              f"team ROI {roi:+8.1f}%  creator {usd(r.creator_payout[t.name])}  backer each {b}")
    print(f"    platform {usd(r.platform)}  season+ {usd(r.season_in)}  season- {usd(r.season_out)}  "
          f"refunded {usd(r.refunded)}")


def scenario(title, teams, p=P, season_pot=0):
    print(f"\n## {title}")
    r = settle(teams, p, season_pot)
    invariants(teams, r, title)
    show(teams, r)
    return r


print("=" * 70)
print("PART 1: extreme scenarios (alpha=1, stake-weighted)")
print("=" * 70)

scenario("Basic 4 ETFs", [Team("A", 800, 5), Team("B", 300, 2), Team("C", -100, 0), Team("D", -500, 3)])

r = scenario("Too few ETFs (3) → void", [Team("A", 500), Team("B", 100), Team("C", -200)])
check("3 ETFs voids and refunds", r.void and all(v == t for v, t in zip(r.team_payout.values(), [STAKE] * 3)))

r = scenario("All returns equal → void", [Team(x, 200, 3) for x in "ABCD"])
check("equal returns void", r.void)

r = scenario("Top coalition: 3 of 5 tie for best", [Team("A", 400, 1), Team("B", 400, 1), Team("C", 400, 1), Team("D", 100, 9), Team("E", -50, 4)])
check("tied best group all win", not r.void and set(r.winners) == {"A", "B", "C"})

teams = [Team("Crowd", 900, 20)] + [Team(f"Solo{i}", 100 - i * 50, 0) for i in range(5)]
r = scenario("Crowd of 21 wins, losers are 3 solo creators (thin pot)", teams)
roi = (r.team_payout["Crowd"] - teams[0].stake) / teams[0].stake
check("thin pot: crowd still gets stake back", r.team_payout["Crowd"] >= teams[0].stake, f"ROI {roi*100:.1f}%")

teams = [Team("CrowdA", 900, 20), Team("CrowdB", 700, 20), Team("SoloC", -100, 0), Team("SoloD", -300, 0)]
r0 = settle(teams, P)
check("4 ETFs → exactly 2 winners (top half)", len(r0.winners) == 2, str(r0.winners))
r = scenario("Really thin pot: two full teams win, two solos lose", teams)
r = scenario("Same, with season pot $50 available (top-up)", teams, season_pot=50 * USD)
check("top-up used from season pot", r.season_out > 0, usd(r.season_out))

teams = [Team("Gem", 900, 0)] + [Team(f"Crowd{i}", 50 - i * 10, 20) for i in range(4)]
r = scenario("Solo gem wins, 3 full teams (63 people) lose (cap 100x)", teams)
check("gem gain within 100x cap", r.team_payout["Gem"] - STAKE <= 100 * STAKE)
r = scenario("Same with cap 10x → excess flows to the other winner first", teams, Params(cap_multiple=10))
check("gem gain capped at 10x", r.team_payout["Gem"] - STAKE <= 10 * STAKE)
teams = [Team("Gem", 900, 0), Team("Small", 500, 0), Team("CrowdX", -100, 20), Team("CrowdY", -300, 20)]
r = scenario("Two solo winners vs two full losing teams, cap 10x → refund", teams, Params(cap_multiple=10))
check("all winners capped → losers refunded unmatched stake", r.refunded > 0, usd(r.refunded))

teams = [Team("Max", 1000, 20), Team("Big", 500, 20), Team("Big2", -100, 20), Team("Max2", -900, 20)]
r = scenario("Four maxed teams (84 people)", teams)

teams = [Team(f"E{i}", random.Random(i).randint(-800, 800), random.Random(i * 7).randint(0, 20)) for i in range(200)]
r = settle(teams, P)
invariants(teams, r, "200 ETFs")
check("200 ETFs settles with conservation", not r.void, f"{len(r.winners)} winners")

print("\n" + "=" * 70)
print("PART 2: exploits")
print("=" * 70)


def clone_test(alpha):
    p = Params(alpha=alpha)
    base = [Team(f"X{i}", r_, 0) for i, r_ in enumerate([-300, -200, -100, 0, 50, 80])]
    # Option 1: 21 people form ONE team on a strong ETF (+6%).
    t1 = base + [Team("Team", 600, 20)]
    r1 = settle(t1, p)
    one_team = r1.team_payout["Team"] - 21 * STAKE
    # Option 2: the same 21 people each create an identical clone ETF.
    t2 = base + [Team(f"Clone{i}", 600, 0) for i in range(21)]
    r2 = settle(t2, p)
    clones = sum(r2.team_payout[f"Clone{i}"] for i in range(21)) - 21 * STAKE
    return one_team, clones

print("\n## Team vs clones: 21 people back one ETF, or each copies it as their own ETF")
for a in (0.0, 0.5, 1.0):
    one, cl = clone_test(a)
    print(f"    alpha={a}: one team gains {usd(one)}  |  21 clones gain {usd(cl)}")
one0, cl0 = clone_test(0.0)
one1, cl1 = clone_test(1.0)
check("alpha=0 (one team, one share) rewards cloning over backing", cl0 > one0 * 1.5, "flaw confirmed")
print("    note: clones also add 21 ETFs that shift the median; compare per-stake gains below")

print("\n## Same capital, team vs clones, holding the field's median fixed")
field = [Team(f"F{i}", -500 + i * 25, 0) for i in range(41)]   # 41 neutral ETFs
for a in (0.0, 1.0):
    p = Params(alpha=a)
    r1 = settle(field + [Team("Team", 700, 4)], p)
    team_gain = r1.team_payout["Team"] - 5 * STAKE
    r2 = settle(field + [Team(f"C{i}", 700, 0) for i in range(5)], p)
    clone_gain = sum(r2.team_payout[f"C{i}"] for i in range(5)) - 5 * STAKE
    print(f"    alpha={a}: 5 people as one team gain {usd(team_gain)}  |  as 5 clones gain {usd(clone_gain)}")

print("\n## Same, with clone-merging (identical baskets join the first ETF's team)")
from league import merge_clones
p = Params(alpha=1.0)
r1 = settle(field + [Team("Team", 700, 4, "AI")], p)
team_gain = r1.team_payout["Team"] - 5 * STAKE
merged, _ = merge_clones(field + [Team(f"C{i}", 700, 0, "AI") for i in range(5)])
r2 = settle(merged, p)
clone_gain = r2.team_payout["C0"] - 5 * STAKE
print(f"    one team gains {usd(team_gain)}  |  5 clones (merged) gain {usd(clone_gain)}")
check("clone-merging removes the copy advantage", abs(team_gain - clone_gain) <= 5)

print("\n## Sybil median attack: attacker adds k junk ETFs to push their ETF above the median")
field = [Team(f"F{i}", -200 + i * 20, 0) for i in range(20)]
for k in (0, 5, 10, 20):
    attacker = [Team("Mine", 0, 0)] + [Team(f"Junk{i}", -900, 0) for i in range(k)]
    r = settle(field + attacker, P)
    net = sum(r.team_payout[t.name] for t in attacker) - sum(t.stake for t in attacker)
    print(f"    {k:>2} junk ETFs: attacker net {usd(net)}  (Mine wins: {'Mine' in r.winners})")

print("\n## Creator sybil-backs own ETF (fee loop)")
field = [Team(f"F{i}", -300 + i * 40, 3) for i in range(15)]
for sybils in (0, 10, 20):
    r = settle(field + [Team("Own", 500, sybils)], P)
    t = Team("Own", 500, sybils)
    net = r.team_payout["Own"] - t.stake
    print(f"    {sybils:>2} self-backers: creator+sybils net {usd(net)}  per stake {net / t.members / USD:+.2f}")

print("\n" + "=" * 70)
print("PART 3: Monte Carlo fairness, 20,000 rounds (alpha=1)")
print("=" * 70)
rng = random.Random(42)
roi = {"creator": [], "backer": [], "solo_team": [], "crowded_team": [], "skilled": [], "unskilled": []}
platform = season = refunded = voids = topups = 0
stake_total = 0
season_pot = 0
for _ in range(20_000):
    n = rng.randint(4, 60)
    teams = []
    skills = []
    for i in range(n):
        skill = rng.gauss(0, 1)
        ret = int(skill * 150 + rng.gauss(0, 300))          # skill moves return, luck dominates
        # backers crowd toward skilled ETFs (they can see past records), noisy
        backers = max(0, min(20, int(rng.expovariate(1 / (2 + 4 * max(skill, -0.4) + 2)))))
        teams.append(Team(f"E{i}", ret, backers))
        skills.append(skill)
    r = settle(teams, P, season_pot)
    stake_total += sum(t.stake for t in teams)
    if r.void:
        voids += 1
        continue
    season_pot += r.season_in - r.season_out
    platform += r.platform
    season += r.season_in
    refunded += r.refunded
    topups += r.season_out > 0
    for t, s in zip(teams, skills):
        c = (r.creator_payout[t.name] - STAKE) / STAKE
        roi["creator"].append((c, 1))
        team_roi = (r.team_payout[t.name] - t.stake) / t.stake
        (roi["skilled"] if s > 1 else roi["unskilled"] if s < -1 else []).append((team_roi, t.members))
        if t.backers:
            b = (r.backer_payout_each[t.name] - STAKE) / STAKE
            roi["backer"].append((b, t.backers))          # weight by number of backers
        (roi["crowded_team"] if t.backers >= 10 else roi["solo_team"] if t.backers == 0 else []).append((team_roi, t.members))

def wmean(v):
    return sum(x * w for x, w in v) / sum(w for _, w in v)
def wwin(v):
    return sum(w for x, w in v if x > 0) / sum(w for _, w in v)
print("    (per-stake averages: every $5 counts once)")
for k, v in roi.items():
    print(f"    {k:<13} mean ROI {wmean(v)*100:+6.2f}%  win rate {wwin(v)*100:5.1f}%  stakes={sum(w for _, w in v)}")
all_stakes = roi["creator"] + roi["backer"]
print(f"    ALL STAKES    mean ROI {wmean(all_stakes)*100:+6.2f}%  (should equal minus the platform+season take)")
print(f"    platform take {platform/stake_total*100:.2f}% of all stakes; season pot net +{usd(season_pot)}; "
      f"void rounds {voids}; top-ups {topups}; refunded {usd(refunded)}")
check("skilled ETFs earn more than unskilled", wmean(roi["skilled"]) > wmean(roi["unskilled"]))
check("platform take ≤ 5% of stakes", platform / stake_total <= 0.05)
check("creators earn more than backers on average (fee)", wmean(roi["creator"]) > wmean(roi["backer"]))
gap = wmean(roi["creator"]) - wmean(roi["backer"])
print(f"    creator vs backer gap: {gap*100:.2f} points (the 10% creator fee)")

print("\n" + "=" * 70)
print("RESULT:", "ALL CHECKS PASSED" if not fails else f"{len(fails)} FAILED: {fails}")
