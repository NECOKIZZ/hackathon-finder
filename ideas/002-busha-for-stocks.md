# 002 — Busha for Stocks

**Status:** Captured · **Captured:** 2026-10-04 · **Origin:** Neco
**Working name:** TBD

---

## 1. One-liner
**Buy US stocks with naira in seconds, 24/7.** Busha's simplicity, applied to equities. Under the hood: naira → stablecoin → tokenized stock, held in the user's own passkey wallet.

## 2. Problem
- Nigerians want US stock exposure, both as a naira hedge and for growth.
- Today they use broker apps (Bamboo, Risevest and others). Those come with:
  - Dollar funding friction and FX spreads.
  - Market-hours-only trading and settlement delays.
  - Custody you can't see: you trust the app's broker chain.
  - No way to move or send your shares.
- Busha shows that a simple, locally trusted app can win at "naira in, asset out". It's SEC-licensed as a VASP and rebranded in January 2026 as a broader digital-money app. But it does crypto, not stocks.

## 3. How it works
**User flow (the first five minutes)**
1. Sign in with Face ID. A Mera passkey creates the wallet: no seed phrase, no "wallet" wording.
2. Fund with naira through a local on-ramp. This is mocked or uses a partner in the demo.
3. Search "Apple" and buy ₦5,000 worth. You own 0.0x AAPL, shown in naira and in dollars.
4. Portfolio view: value in naira, gain or loss, dividends.
5. Extras that broker apps can't easily offer: **send a stock to a friend by name**, **buy at 2 am on a Sunday**, **round-up investing**.

**Under the hood**
- Naira → stablecoin (AUSD or USDC) through an on-ramp partner.
- Stablecoin → stock token through a swap on Monad (for example a **Kuru** order-book market) or through the issuer's mint and redeem.
- Prices from oracle feeds, with off-hours handling (see risks).

## 4. Why on-chain, and why Monad
- 24/7 trading, instant settlement, fractional units, transferable shares and a verifiable 1:1 backing. These are what make stock tokens better than a broker app.
- Monad gives an exchange-like feel: 300 ms blocks, an on-chain order book (Kuru), sub-cent fees on small ₦ trades.

## 5. Competitors and difference
- **Bamboo, Risevest:** broker-backed, market hours, custodial, no transfers.
- **Busha:** crypto only (for now). Also a possible partner or acquirer for this.
- **Global stock-token issuers** (Ondo Global Markets, xStocks, Dinari dShares): supply the assets but not the Nigerian consumer front end or naira rails.
- **The difference:** a Nigerian-first consumer app (naira in, Face ID, send stocks by name) on top of on-chain stocks.

## 6. Hackathon fit — Monad Metropolis (deadline 13 Oct 2026)

| Where | Fit | Why |
|---|---|---|
| **Agora: Best Mobile Trading App on Monad ($10k)** | **Primary** | This is a mobile trading app. Use AUSD as the base currency |
| **Kuru: Build the Next Consumer Trading App ($5k)** | Strong | Consumer trading front end on Kuru's order book |
| **Kuru: Bring New Assets and Markets ($5k)** | Strong | Listing stock-token markets on Kuru brings a new asset class to Monad |
| Bring Any-Chain Liquidity to Monad ($5k) | Strong if we bridge | Stock tokens live elsewhere (see the blocker), so bridging them in is exactly this bounty |
| Track 02 Consumer Products & Payments | Track pick | "A user's first five minutes", and an app that never mentions a blockchain |
| Track 01 Finance & Trading | Alternative | "Teams who have shipped a trading product". Weaker narrative fit than 02 |
| Mera ×2 ($5k) / Privy / Dynamic | Add-on | Passkey onboarding. Pick one wallet stack; Mera is Monad's own |

**Judging angle:**
- Demo a real Nigerian user flow from ₦ to AAPL in under 60 seconds, on a phone.
- Stack the Agora + Kuru + liquidity bounties, which together are worth more than a track prize.

## 7. Reuse from existing repos (as disclosed dependencies)
- **Synesis:** the no-crypto-wording UX rules, name-based sends, PIN confirmation, agent "buy ₦5k of Apple every Friday" (recurring buys).
- **Kickoff:** research on Robinhood stock tokens (thin liquidity, weekend pricing, swap-on-delay / TWAP fix), plus a compliance flag that already exists in `docs/future-upgrades/kickoff-robinhood-chain-alignment.md`.
- **Delphi:** trading UI and the Jupiter-style swap widget pattern.

## 8. MVP scope (9 days)
**In:**
- Mobile-first web app: passkey sign-in, ₦ funding (mocked on-ramp with a clear label), search, buy, sell, portfolio.
- 3–5 stock tokens.
- Trading through Kuru markets (or a simple AMM fallback).
- Send a stock by name.

**Out:**
- Real naira rails.
- KYC.
- Dividends.
- Production-grade issuer integration.

## 9. Risks and open questions
- **Blocker: no confirmed tokenized-stock issuer is live on Monad.**
  - Ondo is on Ethereum, BNB Chain and Solana.
  - Dinari dShares are on Ethereum, Arbitrum, Base and Avalanche.
  - I couldn't confirm any on Monad as of 2026-10-04.
  - Options:
    - (a) Bridge an existing stock token in. This fits the "Any-Chain Liquidity" bounty but needs a working bridge route.
    - (b) Demo with **clearly labeled** test stock tokens priced by an oracle. Fine for a hackathon, but say so.
    - (c) Ask Monad, Kuru or Agora in Discord whether an issuer is coming. They may know of one, and asking also gets you noticed.
- **Regulation.** Selling tokenized securities to Nigerians is a regulated activity:
  - Nigeria's SEC licenses VASPs (Busha holds one).
  - It has authorized tokenized securities on the NASD digital platform.
  - Issuers restrict who can hold their tokens.
  - Fine for a hackathon; a real product needs a licensed partner. Busha itself would be the obvious one.
- **Off-hours pricing.** Stock tokens trade thin and wide when US markets are closed. Show the "buy at 2 am Sunday" price honestly, or use limit orders.
- **Naira on-ramp partner** for a real launch: Busha, Yellow Card or others.

---

## Sponsor integrations (Monad Metropolis)
See the sponsor-by-sponsor fit table in [`hackathons/2026-10-monad-metropolis/SPONSORS.md` §14](../hackathons/2026-10-monad-metropolis/SPONSORS.md#14-fit-with-our-ideas).
