# 001 — KOL Impression Streams

**Status:** Captured · **Captured:** 2026-10-04 · **Origin:** Neco
**Working name:** TBD

---

## 1. One-liner
Projects fund a campaign. KOLs post on X and get paid **in real time, per verified impression**, with money streaming into their wallet as the post is seen.

## 2. Problem
- **Projects** usually pay KOLs upfront, or in fixed chunks, for posts whose reach they can't verify until later. They overpay for flops and have no recourse.
- **KOLs** chase invoices, wait for payment, or deal through agencies and middlemen who take a cut and add delay. Smaller KOLs, especially outside the US/EU, get the worst terms.
- **Both sides** argue about results after the fact, because nothing ties the payment to performance automatically.

## 3. How it works
**Project side**
1. Create a campaign:
   - Budget in a stablecoin (USDC or AUSD), escrowed on-chain.
   - Rate per 1,000 impressions.
   - Eligible KOLs (an open list or invited handles).
   - Rules: must tag the project, minimum post lifetime, per-post cap, holdback %.
2. Watch a live dashboard showing spend, impressions and effective cost per 1,000 impressions for each KOL.

**KOL side**
1. Sign in **with X** (Privy's X login proves handle ownership and creates an embedded wallet).
2. Join a campaign and post. The app detects the post, or the KOL pastes its link.
3. Watch the balance **tick up** as impressions grow, and withdraw at any time.

**Mechanism**
- An **impression oracle** reads `impression_count` for each campaign post from the X API (v2 public metrics) every N minutes and writes the *change since the last reading* on-chain.
- The escrow contract releases `delta × rate`, split into:
  - **Paid now:** for example 80%, claimable straight away.
  - **Holdback:** for example 20%, released after the minimum post lifetime (for example 7 days) if the post is still up and no flag was raised.
- **Real-time feel:** between readings, the UI interpolates the stream. On-chain, each reading settles almost instantly.
- **Post deleted early:** the stream stops and the holdback goes back to the project.
- **Per-post cap:** the stream stops when the cap or budget is reached.

**Anti-fraud** (this is the hard part, and judges will ask):
- Quality multiplier: engagement-to-impression ratio bands. Very high impressions with almost no engagement suggests bought views, so the rate drops.
- Account quality gate: account age, follower/following ratio, history. Delphi already has influence scoring.
- Holdback plus a dispute window for the project.
- Per-KOL and per-post caps.

**Trust in the oracle:**
- Run the X API reads as a **Chainlink CRE workflow**. Several nodes fetch and agree on the number before it's written on-chain, so no single server of ours decides the payout. The X API key sits in CRE secrets.
- MVP fallback: our own keeper with signed readings, with the upgrade path to CRE.

## 4. Why on-chain, and why Monad
- Paying per impression means thousands of tiny settlements. On-chain that's only practical with **sub-cent fees** and **fast blocks**. Monad has 300 ms blocks, 600 ms finality and sub-cent fees.
- Escrow removes the trust problem: projects can't skip payment, and KOLs can't be paid for impressions that never happened.
- It settles instantly across borders. A Lagos KOL paid by a Singapore project gets stablecoins in seconds.

## 5. Competitors and difference
- KOL marketplaces and agencies: manual deals, flat fees, slow payouts.
- "Post-to-earn" and engagement-farming platforms: reward volume, not verified reach, and attract bots.
- Streaming-payment protocols (Sablier, Superfluid-style): stream by **time**, not by **performance**.
- **The difference:** payment tied to *verified performance* and settled *as it happens*.

## 6. Hackathon fit — Monad Metropolis (deadline 13 Oct 2026)

| Where | Fit | Why |
|---|---|---|
| **Track 03 Social, Attention & Culture** | **Primary** | The track is about attention and "programmable incentives… how communities create and capture value". Paying for attention as it accrues is the core of that |
| Track 02 Consumer & Payments | Secondary | Close to their example of "subscriptions that charge by the second". This one charges by the impression |
| **Chainlink: Best workflow with CRE ($3k)** | Strong | The impression oracle as a CRE workflow is a clean, real use |
| **Privy ($5k)** | Strong | X sign-in to prove handle ownership, plus embedded wallets for KOLs who've never used crypto |
| Agora: Cross-Border Payments ($10k) | Possible | Global projects paying KOLs in other countries in AUSD is a real cross-border payment flow. Check the bounty wording |
| Envio ($1k) | Easy add | Index campaign and stream events for the dashboards |
| Nansen ($5k) | Stretch | Score KOL audience quality with on-chain labels. Only works if engagers' wallets can be linked |

**Judging angle:**
- The live demo is the money ticking up while impressions climb.
- It's a clear "only on Monad" story.
- It's an honest anti-fraud design.

**Track 03 weak spot:** they want teams that have grown a community. Mitigation: line up 3–5 real KOLs and one real project for a live pilot campaign during the build, then show the numbers.

## 7. Reuse from existing repos (as disclosed dependencies)
- **Delphi:** crypto-Twitter ingestion (twitterapi.io) and creator influence scoring → the KOL quality gate.
- **Kickoff:** Privy auth, server transaction queue, cron and keeper patterns, signed webhooks from kickoff-data.
- **Cuerate:** micropayment settlement plumbing and leaderboard logic.

## 8. MVP scope (9 days)
**In:**
- One campaign contract: escrow, rate, caps, holdback, claim, refund.
- Keeper or CRE oracle that reads X metrics and posts deltas.
- KOL app: X sign-in, join, live balance, withdraw.
- Project dashboard: create campaign, live spend and impressions.
- Basic quality multiplier.

**Out:**
- Nansen scoring.
- Multi-platform support (TikTok, YouTube).
- Dispute UI (use admin-only flags for the MVP).

**Cost check:** X API pay-per-use is $0.005 per post read. Polling one post every 10 minutes is about 144 reads, or about $0.72 per day. Cheap for a demo, but it has to be priced into a real product.

## 9. Risks and open questions
- **X API terms and accuracy.** Is `impression_count` reliable and current enough to pay against? How quickly does it update? Check X's developer policy on using metrics for payments.
- **Bot impressions** can't be fully solved, only priced in. Be explicit about this.
- **Which stablecoin:** USDC (native Circle support on Monad) or AUSD (largest on Monad, Agora bounty).
- **Does CRE support Monad as a write target?** Not confirmed. Check the docs; fall back to a keeper.
- **Pilot:** which real project and KOLs could run a live campaign during the build?

---

## Sponsor integrations (Monad Metropolis)
See the sponsor-by-sponsor fit table in [`hackathons/2026-10-monad-metropolis/SPONSORS.md` §14](../hackathons/2026-10-monad-metropolis/SPONSORS.md#14-fit-with-our-ideas).
