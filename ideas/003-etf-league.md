# 003 — ETF League (build your own ETF, win everyone's tickets)

**Status:** Captured · **Captured:** 2026-10-04 · **Origin:** Neco (refined in discussion)
**Working name:** TBD

---

## 1. One-liner
Build your own ETF from tokenized stocks, add a ticket, and compete weekly on growth. Your stocks stay 100% yours. The best investors win everyone's tickets.

## 2. Problem
- Tokenized stocks are now widely available (709 on BNB Chain alone, often in three brands: Ondo, xStocks, bStocks). Holding them is passive and lonely: nothing rewards you for picking well.
- Prediction games reward skill but force you into bets, not ownership.
- Curated baskets and ETFs already exist (e.g. an S&P 500 token), but you can't make your own and show you're good at it.

## 3. How it works
**Investors**
1. Build an ETF: pick stocks and weights, fund it. A vault buys the real stock tokens and issues you one ETF token. You can redeem for the underlying stocks at any time.
2. Add a **ticket** to enter the weekly league. The ticket is a separate stake; your stocks are never at risk.
3. At week's end, ETFs are ranked by **growth of the stock part only**. The ticket is excluded from the score so its price can't distort the rankings.
4. **The top half / top 10 split all tickets, with the best getting the biggest share** (Kickoff's median-gate and accuracy-weighted payout). Not winner-takes-all, which would reward all-in gambles.

**Players** (people who don't want to hold stocks)
- Make predictions instead (e.g. "where will Tesla open Monday?", "pick this week's 5 winners"). Pay the same ticket, win tickets.
- One shared leaderboard ranks everyone by how good their calls are, whichever way they play.

**The ticket asset (swappable by design)**
- **Hackathon:** a stock token itself, e.g. an S&P 500 token. Losers' S&P tokens go to winners: stocks stay central and winners earn more stock.
- **Later:** our own token. Every ETF needs it (steady demand), and owning its trading pool earns us trading fees.
- USDC also works as a fallback.

## 4. Why on-chain
- Real stock tokens are owned and redeemable in the user's own wallet. A vault anyone can verify holds the basket.
- Trading is 24/7 and payouts settle instantly.
- Weekend pricing is honest: show ETF value as a range while markets are closed.

## 5. Hackathon fit
| Hackathon | Fit | Notes |
|---|---|---|
| **BNB Hack: Tokenized Stocks** (11 Oct) | 🟢 | Stock tokens central (ETF components + S&P ticket). Spot only via PancakeSwap. $2k Agentic Wallet special: an AI helper builds and tops up your ETF from a prompt. DX report material from mixing three token brands |
| Colosseum, Robinhood Chain track (12 Oct) | 🟡 | Robinhood stock tokens. Overlaps with Kickoff's slot (one submission per team) |

## 6. Reuse
- **Kickoff:** payout engine (median gate, accuracy weights, cap and water-fill), leaderboards, agent personas.
- **Synesis:** interpret → confirm agent pattern for the AI ETF helper.

## 7. Open questions and risks
- **Liquidity:** only allow stock tokens with real on-chain trading volume.
- **Demo timing:** a week is too long to show, so run a one-day league for the demo.
- **Our own token:** may look like a cash grab to hackathon judges, and a token whose value comes from a prize game can be treated as a security. Use an S&P ticket for the hackathon and get legal advice before launching a token.
- **It's still a game with money on it.** The ticket is small and separate from holdings, but a real launch needs legal advice.
- Check Ondo's existing ETF tokens so we don't rebuild something it already sells.

## 8. Prior art: EARN on Robinhood Chain (earnonhood.com/etfs), checked 2026-10-05
- **What it is:** a self-deployed **Balancer V3** (vault `0x2808…69EB`, not Balancer's official vault) on Robinhood Chain (chain 4663).
  - Each "ETF" is a **weighted pool**: your share = your liquidity position, earning 0.3% swap fees.
  - A **launcher** lets anyone create a basket (e.g. user-made "Leaders": GOOGL / SPCX / META / NVDA).
  - Their own footer: "'ETF' is product branding, not a regulated exchange-traded fund."
- **Their token-in-every-basket trick:** the **EARN token sits in almost every basket** (EARN ETF = SPY / QQQ / WETH / EARN; EARN AI = NVDA / TSM / MU / WETH / EARN; …). That's our "you must buy our token" idea, proven live.
- **Caveats:**
  - Fixed-weight pools **auto-rebalance** (sell winners, buy losers), so they behave differently from holding the stocks.
  - Pools are small (EARN ETF ≈ 1 SPY + 1 QQQ). DefiLlama shows ≈ $375k TVL across all EARN products.
- **No public repo found.** Balancer V3 itself is open source (GPL-3.0).

## 9. Plan B: build the league on top of EARN (no exchange to build)
**The clock, not listings, drives the game.** It runs every week. Any EARN basket can enter: EARN's own, community-made, or one the player creates with EARN's launcher. New listings simply join the next round.

**Weekly round**
1. **Start:** Monday at US market open (13:30 UTC). Starting at market open means stock prices have a real reference, so nobody can game the weekend gap.
2. **Enter:**
   - **Investor mode:** lock your EARN basket shares into the league contract for the week. They keep earning swap fees inside the pool, and you get them back at the end.
   - **Player mode:** just pick a basket without holding it.
   - Either way, buy a **ticket** (USDG, or the EARN token if we partner with them).
3. **Score:** % change in the basket's **value per share** from start to end. This includes the swap fees it earned, so busy baskets get a bonus.
4. **End:** next Monday at market open. The top half split the ticket pot (Kickoff's weighted payout: the best get the most). Investors also get their shares back.
5. **Leaderboards:** best investors, and best basket creators (whose baskets did best, and how many people played them).

**Keeping it fair**
- **Value baskets with trusted prices**, not the pool's own prices. Otherwise someone could pump a thin coin in their basket.
- **Only allow league-eligible baskets:** stock tokens + WETH + USDG + EARN, above a minimum liquidity. No memecoin baskets.
- **Snapshot with averages** around start and end (time-weighted), not a single block.
- **Investor mode requires locked shares,** so nobody can borrow shares for the snapshot.

**Why EARN would like it:** the league sends players and trading volume (fees) to their pools. Pitch them to sponsor the prize pot or use EARN as the ticket.

**Fit:** Colosseum Robinhood Chain track (12 Oct). Competes with Kickoff for the one submission, unless it ships as a Kickoff feature ("Kickoff ETF League").
