# 003 — ETF League ("Stake $5 on your ETF")

**Status:** Captured · refined 2026-10-05 · **Origin:** Neco
**Working name:** TBD

---

## 1. One-liner
Hold an on-chain ETF and you already earn trading fees. **Lock a fixed $5 of the stake token next to it**, and if your ETF beats the bottom half this week, you win their $5s.

## 2. Core mechanic (Neco's design)
- **An ETF** = a basket of tokens (e.g. 4 stocks + the platform token). Holders earn trading fees just by holding (as on EARN).
- **The stake:** to enter the weekly round, lock a **fixed $5** worth of the stake token (EARN, or our own token later) in a **separate escrow**, alongside your ETF.
- **The round:**
  - ETFs are ranked by the growth of the **picked stocks only** (stake token, WETH and stablecoins excluded from the score).
  - **Top half:** get their $5 back plus a share of the bottom half's stakes. Better rank = bigger share (Kickoff's weighted payout, not winner-takes-all).
  - **Bottom half:** lose their $5 stake. Their ETF holdings and fees are never touched.
- **Why a fixed $5:** everyone risks the same, so whales can't buy wins. Scoring by % growth means a $50 holder can beat a $50,000 holder.

## 3. Upgrades that make it more interesting
1. **Back an ETF.**
   - Anyone can lock $5 behind someone else's ETF without holding it.
   - Backers win or lose with that ETF.
   - **Creators earn 10% of their backers' winnings.**
   - "Back my ETF" links are made for sharing on X, which makes this the viral loop.
2. **Streaks.** Every consecutive top-half week adds a small bonus (paid from the season pot). ETFs with long streaks become famous, and backers pile in.
3. **Duels.** Challenge another ETF one-on-one for $5: "My AI basket vs your Aerospace basket this week." Easy to share, easy to understand.
4. **Survivor season.** Over a season (e.g. 8 weeks), the bottom half are knocked out of the survivor table each week (they can keep playing normal rounds). The last ETFs standing win the **season pot**.
5. **Beat-the-market bonus.** ETFs that beat SPY that week get an extra slice. Picking well has to mean beating the index, not just beating other players.

## 4. Fairness rules
- **Lock window:** stakes are locked from Monday's US market open to next Monday's open (real price anchors, no weekend-gap games).
- **Snapshot prices with time-weighted averages** around start and end, using trusted stock prices, not the pool's own prices.
- **Eligibility:**
  - minimum ETF size and liquidity;
  - stock tokens + majors only (no memecoin baskets);
  - the holder must have held the ETF for the whole week.
- **Spamming many ETFs doesn't pay:** spreading $5s across 10 random ETFs averages out to losing the platform fee. Leaderboards use season-long records, so luck doesn't look like skill.

## 5. How we make money
- **10% of the bottom half's stakes** (e.g. 5% to us, 5% to the season pot).
- **Stake-token demand:** every entry, backing and duel needs the token. With our own token, we earn its trading fees.
- **Sponsorship:** the platform (e.g. EARN) funds pots, because the league sends holders to its pools.

**Example:** 200 ETFs enter × $5 = $1,000. The bottom 100 lose $500. 10% = $50 (us $25, season pot $25). The top 100 split $450, weighted by rank. Backers and duels multiply the volume.

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
