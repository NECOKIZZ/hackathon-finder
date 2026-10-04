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
  - The pot is split **per team** (see §3, "Splitting the pot").
  - Ties across the whole field → void, refund.
- **Round needs at least 4 ETFs,** otherwise void and refund.

## 3. Backers (supporting a creator)
**Backers buy into the ETF they support.** They hold real shares of the creator's ETF.

**They win or lose in two ways:**
1. **As holders (automatic):** their ETF shares rise or fall with the stocks, and earn trading fees. No game needed.
2. **In the league (optional):** a backer locks the same **fixed $5 stake** and **joins the creator's team**.
   - The team wins or loses on the ETF's % growth, the same result as the creator.
   - **Top-half teams** (creator + backers) get their $5 back plus a share of the bottom-half teams' stakes.
   - **Bottom-half teams** lose their $5s.
   - Payout = stake × accuracy, as in Kickoff. Every member of a team earns the same % return.

**Rules**
- **Must hold to back:** lock at least the minimum holding (e.g. $10) of that ETF's shares in the league escrow for the round. The shares keep earning fees and come back after. No ticket-only backing.
- Joining closes when the round starts. The ETF mix is locked for the round.
- One team per wallet per round (keeps it clean, no hedging across teams).

**Why creators want backers**
- Backers' buy-ins grow the ETF, which means more trading and more fees for everyone in it, including the creator.
- **The creator takes 10% of their backers' league winnings** (only when the team wins).

## Splitting the pot (two steps)
1. **Between winning teams:** each winning team gets a slice by **how well its ETF did** (how far above the middle line). **One team, one share.** Team size doesn't buy a bigger slice.
2. **Inside a team:** members split their team's slice **equally per $5 stake**. Then **10% of each backer's winnings goes to the creator.**

**Effect:** a crowded winning team splits its slice among many people (less each); a small winning team splits among few (more each). That gives a reason to spread across ETFs instead of piling onto one.

**When few people are on the losing side**
- It's peer-to-peer, so a thin losing side simply means smaller winnings that week.
- **Live odds before the round locks:** show each team's estimated payout per $5 if it wins. Crowded teams show low payouts, so people spread out and the losing side naturally fills up.
- **Team size cap** (e.g. 20 backers per creator) stops one ETF absorbing the whole league.
- **Thin-pot top-up:** if the losing pot is under ~5% of winning stakes, the season pot (funded by the rake) tops it up to a minimum. Still player-funded overall.

**Example**
- A: creator + 20 backers (21 × $5); B: 3 members. Both win.
- C: 1 member; D: 2 members. Both lose → pot $15, minus 10% = $13.50.
- A did better than B, so A gets 60% ($8.10) and B gets 40% ($5.40).
- Per $5 stake: A members get about $0.39 each (+7.7%); B members get $1.80 each (+36%).
- A's creator also takes 10% of their 20 backers' winnings.
- Lesson: crowded teams earn little even when they win.

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
