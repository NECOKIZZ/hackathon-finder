# 003 — Feedback on the tokenized-stocks ideas

**Date:** 2026-10-04. These are reactions to three ideas from [`003-tokenized-stocks-bank.md`](003-tokenized-stocks-bank.md) plus Neco's yield-and-hedge idea. Not build specs.

---

## A. Kickoff for stocks: Monday Open Markets
Guess where a stock opens on Monday. Markets open at Friday's close and settle at the 9:30 ET open. The closest guesses win.

**What's strong**
- **The engine already exists.** Kickoff's settlement (median gate, accuracy weighting, cap and water-fill) works on any distance. Swap the scoreline distance for `|guess − open| / Friday close` and the rest carries over unchanged. This is the cheapest new product in the bank.
- **Weekly rhythm.** Friday close → weekend → Monday open, every week. That builds a habit and gives people something to post about ("Monday mood"). The weekend gap is a real, current, under-served problem.
- **The tokenized-stock weekend price works as live odds.** It's the only price that moves on weekends, so it's the natural reference point, and the "token vs reality" scoreboard after each open is good content.
- **Settlement can be defined, not guessed.** Kickoff solved the same problem by declaring official FPL points the truth. Here, the truth is "the first reference price at or after 9:30 ET from oracle X". Write it into the market rules.

**What's weak**
- **It's a derivative on a security.** That's harder to defend than football with regulators. Fine for a hackathon; it's the first question for a real product.
- **Only one settlement per week.** A hackathon demo can't wait for Monday, so it needs a replay mode: run last weekend's gaps through the engine (the "Time Machine").
- **It barely fits BNB.** BNB requires tokenized stocks to be *central* and the product to be **spot only, no perps**. If the token is only a price signal, it isn't central. The fix is to stake and pay out in the stock token itself (stake TSLAx on TSLA's open, winners paid in TSLAx). Even then, judges may see it as a derivative.

**Best home:** **Colosseum World's Fair, Robinhood Chain track** (12 Oct). Kickoff already runs on Robinhood Chain, and Robinhood Chain *is* the stock-token chain. Adding Monday Open as a new market type in Kickoff is real, new in-window work, built on code that's mostly from the same window. Much stronger than just polishing Kickoff.

**Verdict:** 🟢 Strong idea. Wrong hackathon for BNB, right one for Colosseum.

---

## B. Weekend CEX arbitrage bot (when there's no anchor)

**Honest framing first:** with no anchor, it isn't arbitrage. Arbitrage means you can lock in a price difference and close it for certain. On weekends:
- **Same token, two venues** (e.g. TSLAx on a CEX vs on PancakeSwap). This *is* real arbitrage, but only if you hold inventory on both sides and can move tokens between venues fast. CEX withdrawal delays and limits often kill it.
- **Different issuers** (bStocks vs Ondo vs xStocks for the same stock). They're *not* the same asset: different backing, different redemption terms. The gap is basis risk, not free money.
- **Token vs "real" price.** There is no real price until Monday. This is a directional bet on the open.

**Reality on the money side:** professional market makers and MEV bots close same-chain DEX-to-DEX gaps within a block. A hackathon bot won't earn real money, and judges know that.

**Where it *is* strong:**
- **As a scanner with honest profit and loss** (the bank's idea #2): spread after gas, fees, slippage and MEV, and when it's *not* worth trading. BNB's Trading API (cross-DEX quotes, MEV protection) and Transaction API (dry-run) are built for this.
- **As a data engine.** The weekend spreads are exactly the signal that A (live odds) and Gap Guard need.
- **As material for the Developer Experience Report,** which is 25% of the BNB score. A bot touches every API and every edge case (liquidity depth, weekend behaviour, how the three token types differ).

**BNB rules:** execution has to be on BSC mainnet. A CEX leg can be *read* for signals, but anything the bot executes should happen on-chain.

**Verdict:** 🟡 Weak as a business, strong as a BNB submission if framed as an "honest weekend spread engine" rather than a "money bot". It also feeds A.

---

## C. "Ethena for stocks": earn yield while hedging stock prices
*(Interpretation: the original note said "SPE xxx". Confirm what was meant.)*

**Two different things this could mean. Pick one:**
1. **Fully hedged (Ethena-style).** Hold the stock token and short the same stock as a perp. Price moves cancel out, and you collect funding, which is usually positive because traders pay to be long stocks with leverage. The result is a *stock-backed synthetic dollar that earns yield*. You have no stock exposure; the yield is the product.
2. **Protected stock holding.** Keep the stock but cap the downside while earning something. That's a collar or covered-call vault (options), not perps.

**Why version 1 is interesting right now**
- Equity perps on Hyperliquid's HIP-3 markets run about **$3B a day**, with open interest up to about **$2.7B**. Funding is paid **every hour**. Funding for equity perps has **no natural anchor on weekends** and is capped at 4% an hour, so weekend funding can be rich, and also risky.
- That gives the bank's weekend theme a *yield* angle: "earn the weekend premium that leveraged longs pay."

**Risks (the things judges will ask about)**
- Funding can turn negative, so the yield turns into a cost.
- **A Monday gap up can liquidate the short side** before you rebalance. You need a weekend risk mode: lower leverage, bigger margin buffer.
- The long leg (spot token) and short leg (perp) are on different venues or chains, so you're exposed to the gap between them and to moving collateral.
- Issuer and redemption risk on the spot token.

**Fit**
- **BNB Hack: ❌ not allowed.** It's spot only, no perps, and the short leg is a perp.
- **Colosseum World's Fair, Hyperliquid track ($100k across 10 teams): 🟢 natural home.** But it's one submission per team, so it competes with A for that slot.
- Otherwise a candidate for the next perps-focused or Hyperliquid hackathon.

**Verdict:** 🟢 The most original of the three as a *product*. Hardest to build safely in a week.

---

## D. The rest of the bank: which ones inspire

- **Weekend Oracle Wars:** forecasters stake money on Monday's open, and their accuracy becomes their reputation. That's A with AI agents as the players, using Kickoff's agent personas and ERC-8004 reputation. A strong upgrade path for A.
- **Token vs reality scoreboard + Time Machine:** not standalone products, but **A's demo depends on them**, since replay gets around the "one settlement a week" problem.
- **Monday Gap Insurance:** clever, but it's an underwriting business. Pricing tail risk with no history is hard. Later.
- **Gap Guard (#1):** good, but it's the hackathon's own suggested idea, so expect many similar entries. Only build it if your version clearly stands out, e.g. as B's data engine.

---

## E. Suggested routing
| Idea | Hackathon | Deadline |
|---|---|---|
| **A** Monday Open Markets (as a new Kickoff market type) | Colosseum, Robinhood Chain track | 12 Oct |
| **B** Honest weekend spread engine (+ Gap Guard view) | BNB Hack: Tokenized Stocks | 11 Oct |
| **C** Ethena for stocks | Later, at a Hyperliquid or perps hackathon (Colosseum slot taken by A) | — |

## Sources
- [BNB Hack: Tokenized Stocks rules](https://bnbchain.org/en/hackathons/tokenized-stocks)
- [Colosseum Official Rules](https://colosseum.com/legal/Crypto%20World's%20Fair%20Hackathon%20Rules.pdf)
- [Hyperliquid perps and outcome markets (Coin Metrics)](https://coinmetrics.substack.com/p/state-of-the-network-issue-368)
- [HIP-3 stocks API](https://docs.bitquery.io/docs/perpetuals/hyperliquid/hip3-stocks-api/)
