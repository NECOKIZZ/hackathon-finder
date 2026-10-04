# Monad Metropolis — Sponsor Bounties

**Researched:** 2026-10-04. Bounty → sponsor mapping comes from the logos on the official page. Each bounty's full requirements are behind the portal login; everything below comes from public docs.

**"What they want"** is our read of each sponsor's goals on Monad. It's **inferred**, not quoted. Check it against the bounty text in the portal.

---

## 0. All bounties at a glance

| Bounty | Sponsor | Prize | What the sponsor is | Integration effort |
|---|---|---|---|---|
| Best Mobile Trading App on Monad | **Agora** | $10,000 | AUSD stablecoin issuer, the largest stablecoin on Monad | Low (use AUSD) |
| Best Cross-Border Payments App on Monad | **Agora** | $10,000 | ″ | Low |
| Build the Next Consumer Trading App on Kuru | **Kuru** | $5,000 | Monad-native order-book DEX + swap aggregator | Low (Flow API) |
| Bring New Assets and Markets to Kuru | **Kuru** | $5,000 | ″ | Medium |
| Best Use of Dynamic | **Dynamic** | $5,000 | Embedded wallets, acquired by Fireblocks | Low |
| Privy! | **Privy** | $5,000 | Embedded wallets + social login | Low |
| Best use of Nansen | **Nansen AI** | $5,000 | On-chain analytics, wallet labels, smart money | Low–Med |
| Best use of Perpl's API | **Perpl** | $5,000 | Fully on-chain perps order book on Monad | Med (Rust SDK) |
| Best Analytics / Risk Tool | **Perpl** | $3,000 | ″ | Med |
| Best workflow with CRE | **Chainlink** | $3,000 | Oracle network; CRE = workflow runtime | Medium |
| Best Community Team Project | **Monad Foundation** | $5,000 | — | n/a (solo) |
| Bring Any-Chain Liquidity to Monad | **Aurora Intents** | $5,000 | Cross-chain intent execution (NEAR Intents) | Low (widget/API) |
| Best Mera-Powered UX on Monad | **Monad Foundation** (Mera) | $2,500 | Passkey account library | Low |
| Mera: One Passkey, Many Keys | **Monad Foundation** (Mera) | $2,500 | ″ | Low–Med |
| Best Agent Wallet Plugin | **MetaMask** | $2,500 | Smart Accounts Kit, delegation, ERC-7715 | Medium |
| Best Integration of CVI/CVA | **Cleanverse** | $2,000 | Compliance layer: verified identity + verified assets | Medium |
| Best Use of Envio | **Envio** | $1,000 | Indexer (HyperIndex/HyperSync) | Low |
| Best Projects using Alchemy | Alchemy | credits | RPC/infra | — |
| Build with Hunyuan | Kepler Plan by Tencent | $2k credits | Tencent AI models | — |
| Best Builds Powered by KIMI | Kimi (Moonshot) | $3k credits | LLM API | — |
| Best Builds with Qwen 3.8 Max | Alibaba Cloud | $5k credits | LLM API | — |

Other sponsors on the page with no listed bounty: Mercuryo (fiat on/off-ramp), Zerion, Quicknode, Tenderly, Dwellir, Spectrum, BlockVision, Chainstack, Crouton Digital, ack3. The page says more bounties are "listed in full on the platform".

**Cash bounties total about $81k,** roughly the same as 2.7 track prizes, and spread across many more winners. This is the opportunity: **one project built to integrate 4–6 sponsors properly can compete for several bounties at once.**

---

## 1. Agora — $10k Mobile Trading · $10k Cross-Border Payments

**Who:**
- Issuer of **AUSD**, a fully reserved dollar stablecoin (cash, T-bills and overnight repo, managed by VanEck).
- **The largest stablecoin on Monad**: supply roughly doubled to about $73M in one week, with Pendle AUSD yield pools.
- Became a "full-stack infrastructure provider" with a Stablecoin API (beta announced 8 Jul 2026) aimed at "developers, AI agents, and teams building money-movement infrastructure".

**Developer surface:**
- **Stablecoin API** (docs.agora.finance/api):
  - Mint AUSD on demand to a reusable deposit address.
  - Self-service redeem, with "no fees on AUSD to and from USD".
  - Non-custodial cross-chain transfers.
  - Register wallets and bank accounts.
  - Reusable mint and redeem "routes".
  - Rewards for building with AUSD.
  - Access is through a demo booking.
- **On-chain:** AUSD is a plain ERC-20 on Monad. Any app can hold it, send it or swap into it without the API.

**What people use it for:** treasury, cross-border B2B payments, trading pairs (AUSD markets on Monad DEXs), yield.

**What they want on Monad (our read):** **Usage and distribution for AUSD.** Both bounties are consumer-facing (mobile trading, cross-border payments), so they want apps that put AUSD in front of real users as the main dollar.

**How to win:**
- Make AUSD the app's *default* dollar, not one option among several.
- Show a real corridor, e.g. Nigeria ↔ abroad.
- Mint or redeem through their API if access arrives in time.

---

## 2. Kuru — $5k Consumer Trading App · $5k New Assets and Markets

**Who:**
- A **fully on-chain order-book DEX** (central limit order book) plus AMM vaults, native to Monad.
- Raised a $2M seed (Electric Capital) and an $11.6M Series A (Paradigm).

**Developer surface:**
- **Kuru Flow** (swap aggregator across every market on Monad):
  - Base URL `https://ws.kuru.io`.
  - `POST /api/generate-token` returns a JWT.
  - `POST /api/quote` takes user, tokens, amount and slippage, and returns the **best route + transaction calldata**.
  - **Optional referrer address + fee in bps**, so the integrator earns on every swap. This is a built-in business model.
- TypeScript SDK, Python CLOB SDK (market making), audited Solidity contracts.
- First-party **agent skill** (live order book, best bid/ask/mid), plus a community MCP server.

**What people use it for:** spot trading on Monad, market making, routing swaps from wallets and apps.

**What they want (our read):**
- **Order flow and listings.** One bounty pays for a consumer front end that brings users to Kuru liquidity.
- The other pays for **new assets/markets**, i.e. more pairs and more volume.

**How to win:**
- Route every trade through Flow, with a referrer fee so it's a real business.
- Bring a market Kuru doesn't have yet.

---

## 3. Perpl — $5k Best use of the API · $3k Best Analytics / Risk Tool

**Who:**
- A **fully on-chain perps exchange**: both the order book and the matching/risk engine are on-chain.
- Built for Monad's parallel execution (several orders processed in the same block).
- Raised $9.25M (Dragonfly-led). The team is in London.

**Developer surface:**
- **Rust SDK** (`perpl-sdk`): in-memory mirror of on-chain state (contracts, L3 order books, accounts, positions), synced from a snapshot plus the event stream. Includes order-request builders.
- **`perpl-cli`**: read-only CLI.
- RPC-based. **No REST or websocket API**; you read events through Monad RPC.

**What people use it for:** leveraged perps trading, market making (Hummingbot connector docs exist).

**What they want (our read):** Tooling around their exchange: bots, dashboards, **risk analytics** (liquidation heatmaps, funding, open interest, trader PnL).

**Fit for us:** Low for both ideas. contract-info or a Delphi-style scoring dashboard would suit the $3k analytics bounty as a separate small entry.

---

## 4. Chainlink — $3k Best workflow with CRE

**Who:** The oracle network. **CRE (Chainlink Runtime Environment)** runs *workflows*:
- a trigger (cron, HTTP or on-chain event);
- capabilities (HTTP fetch, EVM read/write, consensus), executed by a network of independent nodes;
- written in Go or TypeScript.

**Monad status:** ✅ **Monad mainnet supports simulation and production on-chain writes** since CLI v1.29.0 (7 Aug 2026). The forwarder is `0x76c9cf548b4179F8901cda1f8623568b58215E62`. Testnet supports simulation since v1.30.0.

**What people use it for:**
- Bringing off-chain data or API results on-chain with node consensus.
- Automation.
- Cross-chain actions.
- It replaced Chainlink Functions.

**What they want (our read):** A **real off-chain → on-chain workflow** where CRE's consensus matters, i.e. trusted data deciding where money goes.

**How to win:** CRE should be the thing that *decides payouts*, not decoration.

---

## 5. MetaMask — $2.5k Best Agent Wallet Plugin

**Who:** MetaMask's **Smart Accounts Kit** ("gator"), supported on **Monad** (v2.0.0).

**Developer surface:**
- **Smart accounts:** Hybrid (EOA + WebAuthn), Multisig, Stateless7702.
- **Delegations:**
  - `createDelegation`, `redeemDelegations`.
  - **Caveat enforcers** restrict them, e.g. `erc20TransferAmount`, `limitedCalls`, period transfers, function-call scopes.
  - **Redelegation chains** narrow authority (Alice → Bob → Carol).
- **ERC-7715 Advanced Permissions** (`requestExecutionPermissions`), so a user grants a dapp or agent fine-grained spending rights:
  - `erc20-token-allowance`
  - `erc20-token-periodic` (e.g. 10 USDC a day)
  - **`erc20-token-stream`** (linear, e.g. **0.1 USDC per second**)
  - native-token equivalents
  - approval revocation
- **Agent tooling:** `npx skills add MetaMask/smart-accounts-kit`, and an **x402 payments** skill.
- Scaffold: `npx @metamask/create-gator-app`.

**What they want (our read):** Agents that act for users **within limits the user grants**: no seed phrases for the agent, no unlimited approvals.

**How to win:** An agent that holds no funds and spends only through a user-granted ERC-7715 permission, with the caveats visible in the UI.

---

## 6. Privy — $5k

**Who:** Embedded wallets with **social login (email, SMS, passkey, Google, X/Twitter…)**, server wallets, delegated server actions. Owned by Stripe. Monad has official Privy templates (React Native + Expo; Next.js PWA).

**What people use it for:** onboarding non-crypto users; X login for crypto-social and gaming apps.

**What they want (our read):** Apps where Privy is *the* onboarding layer and is clearly visible in the first-run UX.

**Note:** **Kickoff already uses Privy**, so we know the SDK.

---

## 7. Dynamic — $5k

**Who:** Embedded and connected wallet SDK. **Acquired by Fireblocks (Oct 2025)**; still sold under the Dynamic brand.

**2026 features:**
- Gasless transactions on any EVM chain.
- MoonPay onramp.
- Unified deposit addresses.
- **Agent wallets**: a server-side agent operates a Dynamic wallet as a real user.
- **Agent Payments via x402.**

**Conflict:** Privy, Dynamic and Mera all cover onboarding. **Pick one primary.** Combining them weakens each bounty case.

---

## 8. Monad Foundation — Mera bounties ($2.5k + $2.5k) · Community ($5k)

**Mera (built by Category Labs, Monad's core development company):**
- A free client-side TypeScript library. A **WebAuthn passkey ceremony produces 32 bytes**, which **seed a normal EOA** on any chain.
- No recovery phrase, no smart-contract account, no bundler, no MPC, no third party.
- The same passkey gives the same account on web, iOS and Android.
- **"One Passkey, Many Keys"** refers to **deriving several accounts from one passkey via HD paths** (e.g. a personal wallet, an agent wallet, and per-app or per-campaign accounts).

**What they want (our read):** Mera is Monad's own onboarding tool, so they want it showcased in a real product. The second bounty specifically rewards using **multiple derived keys** in a meaningful way.

**Community bounty:** For teams that built with or for a community. Weak fit for a solo builder.

---

## 9. Nansen — $5k Best use of Nansen

**Who:**
- On-chain analytics: **wallet labels, smart money, token flows, PnL**.
- API + CLI (Monad supported) + **MCP**.
- **x402 pay-per-call**, with no API key, paid in **USDC on Base, Solana or Monad**: $0.01–$7.50 per call.
- Nansen supplies **83 endpoints to Monad's API Hub**.

**What people use it for:** tracking smart money, due diligence on wallets and tokens, alpha.

**What they want (our read):** Apps where Nansen data **changes a decision** (who to trust, what to buy, when to stop), ideally paid for with **x402 on Monad**.

---

## 10. Aurora Intents — $5k Bring Any-Chain Liquidity to Monad

**Who:**
- Aurora Labs' cross-chain execution layer on **NEAR Intents** (about $2.5B monthly volume across wallets and trading platforms).
- **Monad is supported as both source and destination.** 30+ chains, including Ethereum, Base, Arbitrum, Solana and TON.

**Developer surface:**
- **Swap Widget** (drop-in).
- **Swap API** (REST): `originAsset`, `destinationAsset`, `amount`, `swapType`, `slippageTolerance`.
- **Intents Deposits** (deposit into a protocol from any chain).
- **Intents Connect SDK** (`@aurora-is-near/intents-connect`): `createExecution`, `submitSignature`, `listExecutions`.
- **Integrator fees:** 60% integrator / 40% Aurora, minimum 2 bps on stables.
- API keys from Intents Studio. Rate limit: 100 requests per 10 s.

**What they want (our read):** Funding into Monad apps from *any* chain in one step, with no manual bridging.

**How to win:** Make "fund from any chain" part of the core flow, e.g. pay with USDC on Base and arrive as AUSD in a Monad app.

---

## 11. Cleanverse — $2k Best Integration of CVI/CVA

**Who:** A compliance layer for on-chain finance. Live on **Monad**, Base, Ethereum, Arbitrum, BNB, Polygon, Solana and others.
- **CVI (Verified Identity):** a wallet bound to a bank-verified identity through **A-Pass**, a reusable, non-transferable credential. Personal data stays local, and the credential can be revoked.
- **CVA (Verified Asset):** an "A-Token" stablecoin with clean origination, programmable rules and full traceability.
- **Programmed governance:** eligibility checks run *before* value moves, with Travel Rule compliance and sanctions checks.

**Signals:**
- Ran its own "Cleanverse Build" hackathon, supported by the Monad Foundation.
- That hackathon was judged on **"CVI-CVA Integration Depth (30 pts)"**, so they reward *enforced* verification, not a badge.
- Past Monad builds: TrustFlow (identity-gated undercollateralised lending), SpendClear (payment governor for agents).

**What they want (our read):** Real flows where **only verified identities can receive or hold verified assets**: payouts, payments, regulated assets.

---

## 12. Envio — $1k Best Use of Envio

**Who:** An indexer.
- **HyperIndex:** event handlers produce a GraphQL API.
- **HyperSync:** up to 2000× faster than RPC for history.
- **HyperRPC:** a drop-in RPC.
- **Monad mainnet and testnet** are supported, including **traces from block 0**.

**How to win:** Dashboards and leaderboards that run on an Envio index. This is an easy add-on to any project.

---

## 13. AI credit bounties (Hunyuan / KIMI / Qwen / Alchemy)
Prizes are credits, not cash. Only worth it if the project already uses an LLM and swapping models costs nothing.

---

## 14. Fit with our ideas

✅ = natural, core to the product · ◐ = possible add-on · — = no fit

| Sponsor bounty | 001 KOL Impression Streams | 002 Busha for Stocks |
|---|---|---|
| Agora Cross-Border $10k | ✅ Global projects pay KOLs in any country in AUSD | ◐ ₦ → AUSD leg |
| Agora Mobile Trading $10k | — | ✅ It *is* a mobile trading app |
| Kuru Consumer Trading $5k | — | ✅ All trades route through Kuru Flow (+ referrer fee) |
| Kuru New Assets/Markets $5k | ◐ Campaign tokens get Kuru markets | ✅ Stock-token markets on Kuru |
| Chainlink CRE $3k | ✅ **The impression oracle**: nodes read X metrics and agree before payout | ◐ Stock price feeds / off-hours guard |
| MetaMask Agent Wallet $2.5k | ✅ **The project grants an `erc20-token-stream` permission** so budget streams per impression with no escrow lock-up | ✅ "Buy ₦5k of Apple every Friday" via `erc20-token-periodic` |
| Privy $5k | ✅ **X login proves the KOL owns the handle** + embedded wallet | ◐ Onboarding (if not Mera) |
| Dynamic $5k | ◐ Agent wallet for the campaign bot | ◐ Onboarding |
| Mera ×2 $5k | ◐ Passkey for projects; "many keys" = one account per campaign | ✅ Face ID onboarding; "many keys" = separate spending, investing and gift accounts |
| Nansen $5k | ✅ **Shill-and-dump guard**: if the KOL's wallet sells the token they're promoting, the stream stops. Plus KOL wallet credibility scores. Paid with x402 on Monad | ◐ Smart-money signals on stock-token flows |
| Aurora Intents $5k | ✅ Projects fund campaigns from any chain | ✅ **Bring stock tokens and liquidity from Solana/Ethereum** (where Ondo and xStocks live). Directly addresses the "no stocks on Monad" blocker |
| Cleanverse CVI/CVA $2k | ✅ Verified-identity KOLs + Travel-Rule-compliant payouts | ✅ **Only verified users can hold stock tokens.** Compliance is a real need here |
| Envio $1k | ✅ Live campaign and stream dashboards | ✅ Portfolio and trade history |
| Perpl $5k / $3k | — | ◐ Stock perps (if Perpl lists equity markets) |

**Cash bounties each idea could realistically enter** (assuming the portal allows one project to enter several bounties; still to confirm):
- **001:** Agora Cross-Border 10k + CRE 3k + MetaMask 2.5k + Privy 5k + Nansen 5k + Aurora 5k + Cleanverse 2k + Envio 1k = **$33.5k**, plus the Track 03 prize ($10k).
- **002:** Agora Mobile 10k + Kuru 5k + 5k + MetaMask 2.5k + Mera 5k + Aurora 5k + Cleanverse 2k + Envio 1k = **$35.5k**, plus the Track 02 prize ($10k).

**Don't try to win them all.** Each bounty needs a real, visible integration in the demo. Pick **4–5** that are central to the product, and treat the rest as add-ons only if time allows.

---

## 15. Sources
- [Metropolis page](https://monad.xyz/developers/hackathons/metropolis)
- [Agora Stablecoin API](https://www.agora.finance/product/stablecoin-api)
- [AUSD growth on Monad](https://cryptobriefing.com/agora-ausd-stablecoin-monad-growth/)
- [Kuru Flow guide](https://docs.monad.xyz/guides/kuru-flow)
- [Kuru SDK](https://pypi.org/project/kuru-sdk)
- [perpl-sdk](https://docs.rs/crate/perpl-sdk/0.2.4)
- [Perpl raise](https://blockworks.com/news/perpl-perpetuals-raise-funding-dragonfly-testnet)
- [CRE supported networks](https://docs.chain.link/cre/supported-networks-ts)
- [CRE release notes](https://docs.chain.link/cre/release-notes)
- [MetaMask Smart Accounts Kit](https://docs.metamask.io/llms-smart-accounts-kit-full.txt)
- [Advanced Permissions](https://docs.metamask.io/smart-accounts-kit/concepts/advanced-permissions/)
- [Monad smart accounts](https://docs.monad.xyz/tooling-and-infra/wallet-infra/smart-accounts.md)
- [Monad embedded wallets](https://docs.monad.xyz/tooling-and-infra/wallet-infra/embedded-wallets)
- [Dynamic changelog](https://dynamic.xyz/changelog)
- [Mera docs](https://docs.monad.xyz/guides/mera)
- [Introducing Mera](https://monad.xyz/blog/introducing-mera)
- [Nansen x402](https://docs.nansen.ai/getting-started/x402-payments)
- [Monad API Hub](https://cryptobriefing.com/monad-api-hub-usdc-pay-per-request/)
- [Aurora Intents docs](https://docs.intents.aurora.dev/llms-full.txt)
- [Cleanverse](https://cleanverse.com/)
- [Cleanverse Build](https://cleanverse.com/hackathon)
- [TrustFlow example](https://github.com/pranay123-stack/trustflow)
- [Envio Monad](https://docs.envio.dev/docs/HyperIndex/monad-testnet)
- [Monad onramps](https://docs.monad.xyz/tooling-and-infra/onramps)
