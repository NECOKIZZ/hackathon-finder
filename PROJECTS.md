# Project Inventory — NECOKIZZ

Scanned 2026-10-03 across all 16 repos on the account. This is the input for hackathon matching: what each project is, what it's built on, how finished it is, what parts can be reused, and which sponsor tracks it could fit.

**How to read the readiness score (1–5):**
1. Idea or stub only.
2. Partial build, not deployable.
3. Works end to end on testnet or locally, rough edges.
4. Deployed and demoable, with docs.
5. Live, polished, has a demo video.

---

## 1. At a glance

| Project | Repo | What it is | Chain / sponsor stack | Readiness | Tier |
|---|---|---|---|---|---|
| **Kickoff** | `kickoff` (private) | Proximity prediction markets for EPL scorelines and FPL player points, plus AI agent accounts | Robinhood Chain (EVM), Privy, Claude, MCP | 4 | Main |
| **Synesis** | `Synesis` | AI agent USDC wallet: plain-English and voice commands, `.arc` names, scheduled and conditional payments | Arc, Circle (user- and dev-controlled wallets, App Kit, CCTP), Solana devnet, MemWal / Walrus | 4 | Main |
| **Cuerate** | `Cuerate` | AI prompt marketplace: paid likes, fork lineage, decaying fork royalties, x402 agent API | Arc, Circle dev-controlled wallets, Circle SCP, x402 | 5 (live + demo video) | Main |
| **WalTube** | `WalTV` (+ `Waltube-docs`) | The Sui port of Cuerate for AI video, with Seal-encrypted premium workflows | Sui (Move), Walrus, Seal, Enoki zkLogin | 4 | Main (fork of Cuerate) |
| **Lock-In / Player Perps** | `Lock-In-` | Solana version of the proximity-market engine (Anchor), with an on-chain proof of the score | Solana (Anchor/Rust), TxLine oracle | 3–4 (devnet proven) | Main (sibling of Kickoff) |
| **Delphi** | `Delphi` | AI memecoin intelligence terminal: CT feed, then narrative matching, Scratch Score, then swap or launch | Solana, Bags, Jupiter, DexScreener, Helius, Claude | 4 (beta) | Main |
| **ARC Name Service (.arc)** | `.arc` | `.arc` name registry: contracts, SDK, REST API, React package, web app | Arc, USDC fees | 3–4 | Main (infrastructure) |
| **Cuerate RE Agent** | `Cuerate-reverse-Engineer` | Pay-per-call agent that turns an AI image back into a structured prompt with confidence scores | OKX.AI / X Layer, x402-style 402 flow, OpenRouter | 4 | Side (feeds Cuerate) |
| **Archer** | `Archer` | Real-time multiplayer spin-the-wheel pot game | Arc testnet, Socket.io, Supabase | 3 | Side |
| **contract-info** | `contract-info` | Contract inspector for any EVM chain (CLI + web UI, 2,600+ chains) | Any EVM | 3 | Side (tool) |
| **HashPay × ARC** | `hashpay-pitch` | Single-page prototype: HashPay payment links addressed to `.arc` names | Arc, HashPay | 2 | Side (pitch) |
| **motion-storyboard** | `motion-design` | Claude skill that writes motion-video prompts for HyperFrames | Claude Code, HyperFrames | 4 | Tool (demo-video engine) |
| cryptobob | `cryptobob` | Personal portfolio site (Figma Make export) | — | 3 | Not submittable |
| ModelBrief | `ModelBrief` | ML model-report Python library. A **fork of ChidiebereNjoku/ModelBrief** | Python | — | Not yours to submit |
| ZerionCLI-fork | `ZerionCLI-fork` (private) | **Empty repository** | — | 0 | Ignore |
| Waltube-docs | `Waltube-docs` | Static pitch and docs site for WalTube | — | — | Asset for WalTube |

---

## 2. Project families

The 16 repos come down to **four product lines**. This matters for reuse: one engine can be submitted in a new skin on another chain.

```
A. Creator economy / prompt royalties
   Cuerate (Arc) ──fork──► WalTube (Sui)  ──docs──► Waltube-docs
        └── feeds ◄── Cuerate RE Agent (OKX.AI)

B. Proximity prediction markets (shared fixed-point engine)
   Lock-In / Player Perps (Solana, Rust) ──port──► Kickoff (Robinhood Chain, TS + Solidity)

C. Arc / USDC-native identity + payments
   .arc Name Service ──used by──► Synesis wallet
                     ──used by──► HashPay × ARC pitch
   Archer, Cuerate also live on Arc testnet

D. Solana trading intelligence
   Delphi (Bags + Jupiter + Claude)
```

Lines A, B and C each have **one engine on two or more chains already**. A chain-specific hackathon (Base, Monad, Aptos, Stellar, NEAR, etc.) can usually be met by porting the escrow or contract layer while keeping the engine.

---

## 3. Main projects — detailed specs

### 3.1 Kickoff — proximity markets for EPL (Robinhood Chain)

**One-liner:** Predict the exact scoreline or a player's FPL points. Payouts depend on how *close* you were, not on whether you were exactly right.

**Problem:** Binary football bets reward luck and favour the house. Kickoff pays the most accurate half of the field out of the other half's stakes, so skill compounds and there's no bookmaker.

**How the market works** (`packages/engine/src/engine.ts`, BigInt fixed point, SCALE = 1e6):
- **Market A (scoreline):** the distance `D` combines a wrong-outcome penalty `P=4`, a goal-difference error (weight 1, capped at 3), a total-goals error (weight 0.5, capped at 4) and clean-sheet calls (weight 0.25).
- **Market B:** player-points distance.
- **Settlement:** void checks, then a best-coalition check, then an **unweighted median gate** (one trader, one vote, so whales can't drag the median), then accuracy weight `a = (1/(1+D/m))^6`, then a pool split by `stake × a`, then a 100× cap with water-fill.
- **Take:** 10% of the losers' pool. Half goes to a platform reserve, half to the **Season Accumulator Pool**.

**Features shipped:**
- **Listing agent:** a daily Vercel cron auto-lists every EPL fixture in the next 8 days and voids postponed ones.
- **Managed AI agents** with "souls" (Analyst, Contrarian, Fortress). Personas are in `docs/agents/souls/`. Users can let an agent stake for them. On-chain this is `AgentVault` with EIP-712 linking.
- **Agent-native surface:** an MCP server (`/api/mcp`), an installable `/skill.md`, `/llms.txt`, and OAuth.
- Live PnL chart, leaderboard, positions, waitlist and invite gating, faucet, admin.
- **kickoff-data service:** a standalone data-truth service. FPL is the settlement authority, with API-Football, football-data.org and Flashscore via Apify used for cross-checks and the live feed. It has a quorum design and signed webhooks. It's hosted on Render with Supabase.
- **4 motion videos** (`videos/`): launch v1 and v2, an 89s walkthrough and a 45s Floodlight piece. There are also repo-local video skills.

**Stack:**
- Next.js 16, React 19, Tailwind 4, Drizzle + Postgres (Neon), Privy auth, viem.
- Anthropic SDK, MCP SDK, Vitest (10 test files), pnpm workspace (`engine`, `schema`).

**Contracts (Foundry, Robinhood testnet, deployed 2026-09-25):**
- `KickoffEscrow`: stake and claim per market.
- `AgentVault`: per-user agent accounts with deposit, stake, claim and pause.
- `AccumulatorVault`: season pool, finalized by the relayer, claimed by winners.
- `MockUSDC`.

**Status:** Deployed on Robinhood Chain testnet. A human-to-human market settled on-chain. Agent create and claim had not been exercised yet, per `docs/agents/ROLLOUT.md`. The most active repo on the account.

**Gaps before submitting:**
- **No README.**
- Testnet only.
- Agent claim path not yet exercised end to end.

**Reusable pieces:** the proximity settlement engine, AgentVault (delegated agent wallets), the multi-source data-quorum service, MCP/skill.md agent onboarding, the video pipeline.

**Fits:** Robinhood Chain / Arbitrum Orbit ecosystem, prediction markets, sports / SportFi, AI agents + DeFi, MCP / agent-tooling tracks, any EVM chain (port the escrow).

---

### 3.2 Synesis — the agentic USDC wallet (Arc)

**One-liner:** A USDC wallet where your identity is `name.arc` and an AI agent turns plain English or voice into safe, PIN-confirmed on-chain actions.

**Problem:** Wallets expose `0x` addresses, seed phrases and gas. Normal people can't automate money ("pay Sara every Friday").

**Design rule:** *Never show crypto complexity unless asked.* Names instead of addresses, OTP or Google instead of seed phrases, USDC as gas, a PIN instead of private keys.

**Architecture:**
- **Two wallets:**
  - *Main Wallet:* Circle user-controlled wallet, PIN-protected.
  - *Smart Agent:* Circle developer-controlled wallet that holds a separate budget.
- **Two-phase agent:**
  - `POST /api/agent/interpret`: the LLM produces structured `Task[]` and never executes.
  - `POST /api/agent/confirm-policy`: PIN, then idempotency claim, then a per-user lock, then a live balance check, then execution.
  - **The LLM can never move money directly.**
- **Task model:**
  - Multiple tasks from one message.
  - Triggers: `now | time | price | balance_above | and-composite`.
  - Modes: `once | repeat`.
  - Compound steps use `$prev.*` references.
- **Skill system:** a semantic skill router (pgvector embeddings, top-K = 6, cosine fallback at 0.4) with a skill-sync check that runs at build time.
- **Memory:** contact memory, a user profile card, and episodic memory through **MemWal on Walrus** (flag-gated).
- **Cross-chain:** Circle App Kit swaps, CCTP bridge, Arbitrum yield, and a **Solana devnet** integration through Circle's Signing API.
- **Policy orchestration:** cron jobs for recurring and conditional tasks. Circle webhooks keep a balance cache. A resilience layer handles Circle outages.
- **Voice:** Web Speech API for speech-to-text and text-to-speech.

**Stack:**
- Next.js 15, React 19, Supabase (auth, Postgres, RLS, pgvector), Circle SDKs.
- Claude via OpenRouter, `@hashpaylink/sdk`, three.js.

**Docs:** unusually strong. `ARCHITECTURE`, `MEMORY_ARCHITECTURE`, `CROSS_CHAIN`, `AGENT_ROADMAP`, `KNOWN_ISSUES`, `STRESS_TEST`, a builder guide and a pitch deck.

**Status:** V3.5 shipped. 26k lines, the biggest codebase after Kickoff. Last commit 2026-07-24.

**Gaps:** Solana is devnet-only and flag-gated. The V4 agent is design-only. There's a mainnet-hardening checklist still open in `KNOWN_ISSUES.md`.

**Reusable pieces:** the interpret-then-confirm agent safety pattern, the skill router, Circle wallet plumbing, the memory architecture.

**Fits:** Circle / Arc / USDC tracks, "AI agents that hold money", consumer payments, account abstraction and wallet UX, Walrus (MemWal), Solana payments, voice-AI tracks.

---

### 3.3 Cuerate — paid prompts with fork royalties (Arc)

**One-liner:** AI creators post the prompt behind an image or video. Viewers pay them through micropayment likes. Forks keep on-chain credit and royalties.

**Live:** https://cuerate.dotarc.my · **Demo video:** https://youtu.be/LqkwzZhjd7M

**Hackathon history:** Built for the **Lepton hackathon** (Arc). Applying to the **Arc Open Source Showcase**.

**Features:**
- Prompt and workflow posts tagged by model.
- **Paid likes:** 0.001 USDC base tier.
- **Forks with on-chain lineage.**
- **Decaying fork royalties:** 50% to the liked post, 25% to its parent, 12.5% to the grandparent, and so on. An original post pays 95/5.
- Tipping, leaderboards, notifications, search.
- **x402 `inspire` API:** agents pay per query from a Circle agent wallet, and the fee flows through the fork split.

**Stack:**
- React + Vite, Tailwind, Radix, MUI.
- Firebase Auth, Firestore and Cloud Functions v2.
- Supabase Storage.
- Circle dev-controlled wallets.
- `CuerateRoyalty.sol` (Foundry, deployed through Circle's Smart Contract Platform).

**Backend functions:** wallet lifecycle, `recordPaidLike`, batch `settlePendingPayments`, `sendTip`, `onPromptCreated` (which calls `registerPost` on-chain), `inspire` (x402), the leaderboard cron, `circleWebhook`.

**Reusable pieces:**
- `CuerateRoyalty.sol`, a general derivative-lineage royalty splitter.
- An x402-on-Arc reference implementation.
- Circle wallet and settlement plumbing.

**Gaps:** Testnet only. The `package.json` name is still the Figma template default.

**Fits:** creator economy, micropayments / nanopayments, x402 / agent payments, Arc / Circle, open-source showcase tracks, AI + crypto.

---

### 3.4 WalTube — Cuerate on Sui, for AI video

**One-liner:** A decentralized social layer for AI video creators. Prompts are stored permanently, remixes are credited and premium workflows are cryptographically paywalled.

**What's different from Cuerate:**
- Video-first.
- **Seal-encrypted premium workflows:** the paywall is threshold IBE, not a UI gate.
- **Enoki zkLogin** with sponsored (gasless) transactions.
- Media stored on Walrus.
- Payments in SUI.

**Move packages (`/move`):**
- `cuerate_attribution`: shared `AttributionRecord` per prompt or fork, with depth and root.
- `waltube_royalties`: `RoyaltyConfig` with basis-point splits and atomic `receive_payment`.
- `waltube_premium`: a `WorkflowAccessPolicy` whose object ID *is* the Seal identity, so it can't be forged. Includes `pay_and_unlock` and `seal_approve`.

**Stack:**
- React 18 + Vite 6, Tailwind 4, TanStack Query.
- Firestore for social data.
- `@mysten/sui`, `dapp-kit`, `enoki`, `seal`.
- Vercel functions for Enoki.

**Status:** Premium workflows work end to end (2026-06-20). There's a pitch deck plus a separate docs site (`Waltube-docs`).

**Fits:** Sui, Walrus, Seal and Mysten tracks (e.g. Sui Overflow, Walrus hackathons), creator economy, content paywalls, zkLogin / onboarding UX.

---

### 3.5 Lock-In / Player Perps — proximity markets on Solana

**One-liner:** Market A (scoreline proximity) as an Anchor program, with the final score checked against **TxLine's on-chain Merkle proof**.

**Architecture:**
- **`engine/`:** a pure-Rust, fixed-point crate (`distance.rs`, `settle.rs`). A worked-example test reproduces the spec exactly.
- **`programs/player_perps/`:**
  - Lifecycle: `initialize`, `stake`, `lock`, `validate_score`, `claim`.
  - **Two settlement paths:**
    - *Fast path* (`submit_settlement`): the keeper computes the result and the program verifies `D`, the median and conservation.
    - *Full path:* a batched, resumable on-chain pipeline for when compute and account limits bind.
- **`keeper/`:** a byte-identical TypeScript mirror of the engine, plus an e2e test. A GitHub Actions keeper commits registry updates several times a day, so it's live.
- **`ui/`:** static HTML app (fixtures, match page, docs) using web3.js.

**Specs in the repo:** a full build spec for Market A, a UI spec and mockup, a Trepa payout simulator (HTML), a multichain plan, `TECH-OVERVIEW`, `PROOF`, `DEMO-SCRIPT`, and a leaderboard plan.

**Status:** The full lifecycle is proven on **devnet** (program `6krdS27r9oHpiTwHemWXwcKSns7Dj3616pFwKNDgmE26`).

**Fits:** Solana (Colosseum, Superteam), oracle / data-provider tracks (TxLine), prediction markets, SportFi, on-chain verifiable computation.

---

### 3.6 Delphi — AI memecoin intelligence terminal (Solana)

**One-liner:** Turns crypto-Twitter noise into scored token signals, then lets you swap or launch from the same screen.

**Pipeline:**
1. Ingest tweets through twitterapi.io (webhook + REST).
2. Two-stage Claude pipeline: extract entities, then match narratives against a live token corpus with time-decay scoring.
3. **Scratch Score v2 (0–100):** DexScreener volume, holder distribution, liquidity depth, Jupiter verification, transaction activity and social signal. There's a formula proof doc.
4. Swap through Jupiter. Launch tokens through the **Bags API**.

**Stack:**
- React + Vite on the frontend.
- Express + Supabase on the backend, deployed on Railway with Docker.
- Phantom sign-in (nonce + signature), Helius RPC, Anthropic SDK, Bags SDK.

**Business docs already written:**
- Superteam Agentic Engineering grant application (200 USDG).
- Colosseum crowdedness report: the niche is moderately uncrowded and the closest match is about 5% similar.
- Investor pitch and pitch deck PDF.
- Jupiter developer-experience feedback report.

**Gaps:**
- The README is the Figma template default.
- Repo root is cluttered (`claude-session.jsonl`, log dumps, `Untitled`).
- The UI spec still says "BagsApp".

**Fits:** Solana / Colosseum, Bags, Jupiter, AI + trading, consumer crypto, data / analytics tracks.

---

### 3.7 ARC Name Service (`.arc`)

**One-liner:** Human-readable `.arc` names for Arc addresses, paid in USDC.

**Components (npm workspaces):**
- `contracts` (Hardhat): register, renew, resolve, reverse-resolve, transfer, release, primary name, reserved names, a 30-day grace period, admin and pause.
  - Fees: 5 USDC per year, 50 USDC for names of 4 characters or fewer.
- `sdk`: `resolve`, `reverseLookup`, `isAvailable`, `quotePrice`, `register`, `renew` and more, with a 60s cache.
- `api`: REST endpoints `/resolve`, `/reverse`, `/available`, `/profile`, `/qr`.
- `react`: hooks package, already published to npm.
- `web`: Next.js app with a getting-started guide.

**Already used by:** Synesis and HashPay × ARC.

**Gaps:**
- **No commit-reveal**, so registration can be front-run.
- A single `.arc` TLD.
- The competitive plan against ArcID lists the missing pieces: multiple TLDs (`.agent`, `.usdc`) and a modern wallet UI.

**Fits:** Arc / Circle infrastructure, identity, "public goods" tracks, agent identity (`.agent` TLD).

---

### 3.8 Cuerate RE Agent — image → prompt, pay-per-call

**One-liner:** Another agent sends an AI image and a few cents, and gets back a structured, confidence-scored prompt that would reproduce it.

**Pipeline:**
- **Stage 0 (free, deterministic):** resolution-grid matching to identify the model family, plus EXIF and C2PA checks.
- **Stage 1:** N independent vision passes, merged by an aggregator. Agreement between passes is the confidence signal.
- **Stage 2:** a trust score, from regenerating and comparing or from ensemble agreement.

**Payment:** Returns `402` until the caller pays. OKX.AI A2MCP pay-per-call listing on X Layer.

**History:** Built for the **OKX.AI Genesis Hackathon** (deadline 2026-07-17).

**Stack:** Node + TypeScript, OpenRouter (multi-vendor ensemble), Railway, tests, demo script, `MOCK_LLM` mode.

**Fits:** agent marketplaces, x402 / agent payments, AI provenance / content authenticity (C2PA), multimodal AI tracks.

---

## 4. Side projects and tools

| Project | Spec | Use for hackathons |
|---|---|---|
| **Archer** | Up to 10 players deposit into a 20s round. The pot goes to one player picked with probability weighted by deposit. Express + Socket.io server, Supabase round history, a fallback signer bot, live leaderboard. `Archer.sol` on Arc testnet. **Randomness is `keccak(timestamp, prevrandao, sender)`, which is not safe for real money.** Gemini AI Studio scaffold. | Good gaming or GameFi submission **if** you swap in VRF (Chainlink, Pyth Entropy, Switchboard). That swap is itself the sponsor integration. |
| **contract-info** | One-shot contract inspector. Source and ABI come from Blockscout, then Sourcify, then Etherscan v2. State comes from RPC: ERC-20 metadata, owner, paused, EIP-1967 and EIP-1167 proxy detection. CLI with `--json` plus a web UI. "AI-optimized" dashboard. | Developer-tooling tracks on new EVM chains (Monad, MegaETH, Robinhood, Stable, Plasma). Wrap it as an **MCP server** for "AI dev tools" tracks. |
| **HashPay × ARC** | One HTML page: enter `name.arc` and an amount, it resolves the name through the ANS API or a direct `eth_call`, then builds a HashPay checkout URL. | A demo of composing `.arc` with someone else's product. Fold it into the `.arc` or Synesis submissions rather than submitting it alone. |
| **motion-storyboard** (this repo) | Skill that writes HyperFrames motion-video prompts. Already produced Kickoff's videos. | **Your demo-video step for every submission.** |
| **cryptobob** | Portfolio site showing Cuerate, dotarc, Mantle vaults, Wizz and others. | Your builder profile link on submission forms. Not a project. |
| **ModelBrief** | Python library for ML model reports. 22 of 23 commits are by ChidiebereNjoku. | **Don't submit.** It's someone else's work. |
| **ZerionCLI-fork** | Empty repo. | Delete or ignore. |

---

## 5. Building blocks you can reuse across hackathons

These are the parts that make a "quick tweak" submission realistic:

| Building block | Lives in | Ports to |
|---|---|---|
| Proximity / median-gate settlement engine (TS + Rust, fixed point) | `kickoff/packages/engine`, `Lock-In-/app/engine` | Any chain's escrow; any "how close were you" market (elections, prices, weather, esports) |
| Derivative-lineage royalty splitter | `Cuerate/contracts/CuerateRoyalty.sol`, `WalTV/move/waltube_royalties` | Remixes, datasets, AI models, music stems, templates |
| x402 / HTTP-402 pay-per-call gate | Cuerate `inspire`, RE Agent | Any "agent pays an API" track (Coinbase x402, OKX, Base) |
| Interpret → confirm agent safety pattern + skill router | Synesis `lib/agent-core-v3.ts` | Any "AI agent with a wallet" track |
| Delegated agent vault (EIP-712 link, pause, operator) | `kickoff/contracts/src/AgentVault.sol` | Agentic-finance tracks on any EVM chain |
| Seal-encrypted paywall bound to the policy object ID | `WalTV/move/waltube_premium` | Any Sui / Walrus content-gating idea |
| Multi-source data quorum + signed webhooks | `kickoff/services/kickoff-data` | Oracle / data-provider tracks |
| MCP server + `skill.md` + `llms.txt` agent onboarding | `kickoff/app/api/mcp`, `app/skill.md` | "Make your app agent-native" tracks |
| Name service (contract + SDK + API + React) | `.arc` | Identity on any new chain |
| Video pipeline (HyperFrames + skills) | `motion-design`, `kickoff/videos` | Every submission's demo |

---

## 6. Fix before submitting anything

1. **Write READMEs** for Kickoff (none), Delphi (template), Archer (AI Studio template) and cryptobob. Judges open the README first.
2. **Delphi repo root:** `claude-session.jsonl` and log dumps are public. They were committed on purpose for the grant, but check them for keys, emails or tokens, then move them to `docs/`. No obvious API keys turned up in a pattern scan of any repo, but that scan isn't a full audit.
3. **Archer randomness** must change before any real-money or "secure" framing.
4. **`.arc` front-running:** add commit-reveal before pitching it as infrastructure.
5. **Prior submissions:** Cuerate (Lepton, Arc OSS), the RE Agent (OKX Genesis) and Delphi (Superteam grant) have been submitted before. Many hackathons ban previously submitted projects, or require you to state what was built during the event. Log what's new in each submission.
6. **Rename leftovers:** `@figma/my-make-file` (Cuerate), "BagsApp" (Delphi), `dotarc-wallet` (Synesis). These are fine internally but look unfinished in a judge's view.

---

## 7. Quick tags for matching

Use these when scoring hackathons against the inventory.

- **Arc / Circle / USDC:** Synesis, Cuerate, `.arc`, Archer, HashPay × ARC
- **Solana:** Lock-In, Delphi, Synesis (devnet)
- **Sui / Walrus / Seal:** WalTube, Synesis (MemWal)
- **Robinhood Chain / Arbitrum Orbit / EVM:** Kickoff, contract-info
- **X Layer / OKX:** RE Agent
- **AI agents:** Kickoff (managed agents, MCP), Synesis, Delphi, RE Agent, Cuerate (x402)
- **Payments / micropayments / x402:** Cuerate, RE Agent, Synesis, HashPay
- **Prediction markets / SportFi:** Kickoff, Lock-In
- **Creator economy / social:** Cuerate, WalTube
- **Identity:** `.arc`
- **Gaming:** Archer
- **Dev tooling:** contract-info, motion-storyboard
