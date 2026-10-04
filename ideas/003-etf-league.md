# 003 — ETF League ("Stake $5 on your ETF")

**Status:** Captured · refined 2026-10-05 · **Origin:** Neco
**Working name:** TBD

---

## 1. One-liner
Hold an on-chain ETF and you already earn trading fees. Lock a **fixed $5 stake** to enter the weekly league. Best-growing ETFs (and their backers) win the stakes of the worst. Peer-to-peer, like Kickoff: the platform never puts money in.

## 2. Core rules (decided 2026-10-05)
- **Stake: fixed $5, separate from the portfolio.** It isn't a % of the ETF and doesn't sit inside the basket. Same ticket for everyone, so small players aren't priced out and whales aren't over-exposed. This is Kickoff's live "fixed stake" mode (its listing agent opens every market at a fixed ticket).
- **Minimum ETF size:** small, e.g. $10 (or EARN's own minimum). Only there to keep dust and dummy ETFs out.
- **Score = % growth of the ETF's stocks** over the round (Monday US open → next Monday open), priced with trusted reference prices and time-weighted around the snapshots. The stake token, WETH and stablecoins are excluded. Never dollars added: % rewards skill, not size.
- **ETF composition:** at least 3 eligible stock tokens, no single stock above 50%, locked for the round.
- **Result:** the middle ETF draws the line (one ETF, one vote).
  - **Top half win, bottom half lose their stake.**
  - Winners are paid stake × accuracy (Kickoff's weighted payout, 100× cap with water-fill).
  - Ties across the whole field → void, refund.
- **Round needs at least 4 ETFs,** otherwise void and refund.

## 3. Backers (supporting a creator)
- **Backing = joining the creator's team.** A backer buys $5 tickets behind an ETF. **The team wins or loses together** with that ETF's result. Backers never compete against each other.
- **The pot = every stake on the bottom-half teams** (creators + their backers). The top-half teams split it, weighted by stake × accuracy.
- **Natural odds:** a crowded favourite that wins pays each backer less; a hidden gem that wins pays a lot. Backers become scouts.
- **Creator rewards from backers:** the creator takes **10% of their backers' winnings** (only when the team wins).
- **Skin in the game:**
  - Total backing per ETF is capped (e.g. 20 tickets per creator ticket).
  - Backing closes when the round starts.
  - The ETF mix is locked for the round.

## 4. Leaderboards and extras
- **Creators:** wins, streaks, total backing attracted.
- **Scouts (backers):** season win rate and return.
- **Extras (later):**
  - Streak bonuses and survivor seasons, paid from the season pot.
  - Duels (one-on-one, $5).
  - Beat-the-SPY bonus.
- **Why bring big liquidity** (outside the game):
  - trading fees on the ETF;
  - room for more backers (more creator income);
  - a season "depth bonus" for liquidity kept in all season.

## 5. How we make money
- **10% of the losers' stakes:** 5% to us, 5% to the season pot.
- **Stake-token demand** if stakes are paid in our token or EARN. Sponsorship from the ETF platform, since we send it holders.
- **Example:** 200 ETFs × $5 = $1,000. Bottom half $500 → 10% = $50 (us $25, season pot $25). Top half split $450, weighted by rank. Backers multiply the volume.

## 6. Where it runs
- **On top of EARN (Robinhood Chain):** EARN already has the ETFs and the fee-earning (see §7). We only build the stake escrow, scoring and league. EARN as the stake token aligns us with them, so pitch them to sponsor.
- **Our own version elsewhere** (e.g. BNB Chain with Ondo / xStocks / bStocks): only if we also build the ETF layer. Note the BNB Hack rules require trades to go through PancakeSwap.

## 7. Prior art: EARN on Robinhood Chain (earnonhood.com/etfs), checked 2026-10-05
- **What it is:** a self-deployed **Balancer V3** on Robinhood Chain (chain 4663; vault `0x2808…69EB`, not Balancer's official vault).
  - Each "ETF" is a weighted pool. Shares = liquidity position, earning 0.3% swap fees.
  - A launcher lets anyone create a basket.
  - Their footer: "'ETF' is product branding, not a regulated exchange-traded fund."
- **The EARN token sits in almost every basket:** EARN ETF = SPY / QQQ / WETH / EARN; EARN AI = NVDA / TSM / MU / WETH / EARN; EARN AEROSPACE = SPCX / BA / PLTR / WETH / EARN.
- **Caveats:**
  - Fixed-weight pools auto-rebalance (sell winners, buy losers).
  - Pools are small (EARN ETF ≈ 1 SPY + 1 QQQ). DefiLlama ≈ $375k TVL across all EARN products.
- **No public repo found.** Balancer V3 is open source (GPL-3.0).

## 8. Hackathon fit
| Hackathon | Fit | Notes |
|---|---|---|
| Colosseum, Robinhood Chain track (12 Oct) | 🟢 | Build on EARN. Competes with Kickoff for the one submission, unless shipped as a Kickoff feature ("Kickoff ETF League") |
| BNB Hack: Tokenized Stocks (11 Oct) | 🟡 | Needs our own ETF layer + PancakeSwap execution |
| BLI Legal Tech (~1 Nov) | 🟡 | RWA theme |

## 9. Risks
- **A house cut of a prize pot is gambling-like.** Skill contests are treated differently in some places. Get legal advice before a real launch.
- **Dependence on EARN's contracts** (audit status unknown) and thin pools.
- **One settlement a week:** for demos, run a one-day round.
