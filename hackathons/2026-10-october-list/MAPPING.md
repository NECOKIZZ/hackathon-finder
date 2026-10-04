# October 2026 — Hackathons Mapped to the Idea Bank

**Mapped:** 2026-10-04. **Source:** @_HEISEMMA's October list ([SOURCE.md](SOURCE.md)), 44 entries.
"Verified" means I checked the official page or rules myself. Everything else comes from the list and needs checking before you commit.

**What we're matching against:**
- **001** KOL Impression Streams
- **002** Busha for Stocks
- **C-Cuerate:** Cuerate + its variants (WalTube, RE Agent)
- **C-Kickoff:** Kickoff / Lock-In proximity markets
- **C-Synesis:** Synesis agentic wallet + `.arc` names
- **Delphi:** AI memecoin terminal

**Strength:**
- 🟢 **Strong:** the idea matches the theme, the required tech is reachable, and the deadline is workable.
- 🟡 **Medium:** a real fit with one big gap (time, required stack or rule risk).
- 🔴 **Weak / no fit.**
- ⚫ **Closed / unreachable:** deadline passed or effectively passed.

---

## 1. The October slate (recommended)

| Priority | Hackathon | Deadline | Entry | Strength | Why |
|---|---|---|---|---|---|
| **1** | **Colosseum Crypto World's Fair: Robinhood Chain track** (+ shot at the 20 × $15k standout prizes) | **12 Oct**, 11:59pm PT | **C-Kickoff** (as it is, plus a disclosed delta) | 🟢🟢 | Kickoff is *already on Robinhood Chain*. 76 of its 154 commits fall after 14 Sep (the contest start). The rules allow pre-existing code with disclosure and judge only work done in the window |
| **2** | **BNB Hack: Tokenized Stocks Edition** | **11 Oct**, 12:00 UTC | **002 Busha for Stocks** | 🟢🟢 | Almost an exact brief. It *requires* tokenized stocks (bStocks, Ondo or xStocks) on BSC mainnet, which **removes 002's main blocker** (no stocks on Monad) |
| **3** | **Monad Metropolis** | **13 Oct** | **001 KOL Impression Streams** | 🟢 | Track 03 plus a large bounty stack (see `../2026-10-monad-metropolis/SPONSORS.md`) |
| **4** | **Arc Microgrants Mainnet Challenge** | **14 Oct** | **C-Synesis / Cuerate / `.arc`** on Arc mainnet | 🟢 (low effort) | 20 × $500 USDC, non-dilutive. Needs a deployable link + public repo. Arc mainnet launched 16 Sep and your Arc apps are on testnet. Redeploying to mainnet is a quick $500 shot |
| 5 | Qloo Agentic Hackathon | 30 Oct | **001** variant (taste-matched KOL ↔ project) or **C-Cuerate** (taste-aware prompt discovery) | 🟡 | $25k, 3 winners. Qloo's taste graph has to be what makes the agent better |
| 6 | PayPal + AI ("Build what's next") | 12 Nov | **001** off-chain variant (KOL payouts via PayPal) or a C-Synesis agent | 🟡 | $60k+. PayPal APIs + agents. *Couldn't verify the event page; confirm it exists first* |

**Workload reality check:**
- Items 1–3 are due on **11, 12 and 13 Oct**, three deadlines on consecutive days.
- **Kickoff (1) needs the least new work** because it's mostly done.
- **BNB (2)** and **Monad (3)** are each a full build.
- Solo, doing all three well in 7–9 days is a stretch.
- **Suggested order:** Kickoff polish *first* (2 days), then whichever of 002 or 001 you're more excited about (6 days), then Arc microgrant redeploys (1 day). Only attempt the third build if you have help.

---

## 2. Every entry, mapped

### Web3 / crypto

| Hackathon | Deadline | Prize (verified?) | Best match | Strength | Notes |
|---|---|---|---|---|---|
| **Colosseum: Crypto World's Fair** | 12 Oct 11:59pm PT | ✅ Grand $30k · 20 × $15k · Public Goods $5k · University $5k · **Solana $100k/10** · **Tempo $100k/10** · **Hyperliquid $100k/10** · **Zcash $100k/10** · **Ethereum L1 $25k/5** · **Base $25k/5** · **Arbitrum $25k/5** · **Robinhood Chain $25k/5** · $2.5M seed | **C-Kickoff → Robinhood track** · Lock-In → Solana track · Delphi → Solana track | 🟢🟢 | **Rules:** pre-existing code allowed if disclosed; judged only on work 14 Sep – 12 Oct. **One team per person, one submission per team.** Criteria: functionality, impact, novelty, UX, open source, business plan |
| **BNB Hack: Tokenized Stocks** | 11 Oct 12:00 UTC | ✅ $20k: 6k/4k/3k/2k/1k + 2 × $2k (Best Agentic Wallet Use, Best BNB Agent Studio Use) | **002** | 🟢🟢 | Must use **Binance Web3 API modules**. **bStocks, Ondo or xStocks must be central.** BSC mainnet only, executed on PancakeSwap. **25% of the score is a mandatory Developer Experience Report.** Demo ≤4 min. **Excluded:** US, CA, NL, UK, JP and sanctioned regions. Build window 16 Sep – 11 Oct |
| **Monad Metropolis** | 13 Oct | ✅ (see the Metropolis folder) | **001** | 🟢 | New work since 1 Sep |
| **Arc Microgrants** | 14 Oct | ✅ 20 × $500 USDC | C-Synesis, Cuerate, `.arc`, Archer | 🟢 | Prototypes and experiments welcome. Deployable link + public repo. Announced by 21 Oct. Rolling review, so submit early |
| Solana Mobile: Clock In | 8 Oct | ✅ $125k to top 10 ($30k → $5k) + $10k SKR | Lock-In / Delphi as Android apps | 🟡 → 🔴 | Needs a working **Android APK** + publishing to the dApp Store. 4 days and no mobile build: skip |
| Bitget AI Hackathon S2 | 8 Oct (list says "status") | $50k USDT (unverified) | **Delphi** (AI market intelligence) | 🟡 | AI trading agents + market intel with Qwen, Chainbase, Kaito. Delphi's narrative pipeline fits, but I couldn't find the rules; 4 days |
| Mezo Buildathon, Wave 1 | 16 Oct – 15 Nov | $7k in MEZO over 2 waves | C-Synesis (MUSD payments agent) | 🔴 | Bitcoin/MUSD; small prize paid in a token |
| HackCanton S3 | 9 Oct | $50k | — | 🔴 | DAML / enterprise privacy. Off-stack |
| BLI Legal Tech Hackathon 2 | 31 Oct | $20k | (Cleanverse-style compliance) | 🔴 | Regtech / legal automation. No idea in the bank |
| Tapeout Genesis (X Layer) | Oct | $14k | — | 🔴 | Circuit/processor design |
| Portaldot Hacker House | 6 Nov | $5.2k | — | 🔴 | Small; ink!/Solidity |
| Road to Colosseum MVP | 5 Oct | 8k USDG | — | ⚫ | Tomorrow; pre-Colosseum MVP. Colosseum itself is better |
| Arbitrum Open House | 4 Oct | $115k | — | ⚫ | Today |
| Ryo-chan Virtual Hackathon | 11 Nov | $15k in tokens + Tokyo trip | (agents/dashboards) | 🟡? | Couldn't read the page. Tracks: agents, dashboards, skills, social. Paid in tokens. Revisit later |

### AI / agents

| Hackathon | Deadline | Prize | Best match | Strength | Notes |
|---|---|---|---|---|---|
| **Qloo Agentic** | 30 Oct | ✅ $25k (15k/6k/4k) | **001** (taste-matched KOLs) / C-Cuerate | 🟡 | Must use Qloo's API inside an agent and beat "LLM-only". Live demo, public repo, OSS license. Open worldwide |
| **PayPal + AI** | 12 Nov | $60k+ (unverified) | 001 (fiat payout variant), C-Synesis | 🟡 | Event page not verified |
| Open Agent Hackathon | registration 13 Oct; build 15–20 Oct | up to $20k (unverified) | C-Synesis / Kickoff agents | 🟡 | "Build an agent that does real work". 1–5 per team. Prize detail not public |
| Graph Hacks (FalkorDB) | 15–18 Oct | $20k hardware + cash | C-Synesis (agent memory on a graph) | 🟡 | Graph DB as agent memory. Synesis's memory architecture fits; prizes are mostly hardware |
| Nebius × NVIDIA | 30 Oct | $50k+ | (generic agentic) | 🔴 | Open-weight models on Nebius GPUs. No natural idea |
| #neathack | 10–11 Oct | $10k + jobs | contract-info (dev tooling) | 🔴 | 48h observability sprint; clashes with the slate |
| Life After Code (GitLab) | 27 Oct | TBA | — | 🔴 | DevSecOps agents |
| WeAreDevelopers × Band | 5 Oct | $10k | — | ⚫ | |
| Anna AI App Builder | 31 Oct | $6k | — | 🔴 | |
| 3alet (Mozaik) | 31 Oct | $1k | — | 🔴 | |
| Gemma 4 Developer Agent (Kaggle) | 12 Nov | $65k | — | 🔴 | ML fine-tuning |

### Not our lane (ML research, hardware, VR, telecom, games)

| Hackathon | Deadline | Prize | Strength |
|---|---|---|---|
| Meta VR Start Developer Competition | 18 Nov | $1M | 🔴 (Quest apps) |
| ARC Prize 2026 | 2 Nov | ~$700–850k | 🔴 (reasoning research) |
| Amazon Developer Hackathon | 23 Oct | $138k | 🔴 (Fire TV / Alexa+ / Ring) |
| RSNA Knee (Kaggle) | 22 Oct | $77k | 🔴 |
| Enveda CASMI (Kaggle) | 14 Dec | $50k | 🔴 |
| OpenCV AI Competition | 26 Oct | $12k | 🔴 (the RE Agent's vision angle is a stretch) |
| Qollab × IonQ Quantum | reg 6 Oct | $10k + compute | 🔴 |
| Raspberry Pi RP2350 challenge | 31 Oct | $20k | 🔴 |
| Run October Jam | 2 Nov | $30k | 🔴 (games/interactive) |
| GSMA MENA Open Gateway | 30 Oct | top-3 cash TBA | 🔴 |
| OneAquaHealth IEEE | 4 Oct | $3.5k | ⚫ |
| Veles Hack | reg 5 Oct | €3k | ⚫ |

---

## 3. The three strongest matches in detail

### 3.1 Kickoff → Colosseum Robinhood Chain track
- **Prize path:** Robinhood track ($25k / 5 = **$5k each**), and the same project can also compete for the **20 × $15k standout** pool and the $30k grand prize. Colosseum also offers $2.5M in accelerator seed checks.
- **Rules fit:** "Teams may begin development before the hackathon, but products are judged only on work completed between 14 Sep and 12 Oct. Must disclose past development." Kickoff in that window includes:
  - agent accounts (AgentVault deployed 25 Sep);
  - managed agents with three strategy personas;
  - MCP + OAuth access for agents;
  - FPL settlement with an instant-settle pipeline;
  - live PnL, PnL share cards;
  - listing agent;
  - mobile UX;
  - 4 motion videos.
- **What to add in 8 days:**
  - A README, which it doesn't have yet.
  - A "Built during World's Fair" changelog.
  - Exercise the agent claim path end to end.
  - Push the Robinhood-native angle from `docs/future-upgrades/kickoff-robinhood-chain-alignment.md`: park the idle pool in Morpho for yield, and AI-agent finance as the chain's stated pillar.
- **Judging fit:**
  - Business plan: there's a proper revenue model, a 10% take.
  - UX: Privy plus no-crypto wording.
  - Novelty: proximity payouts instead of win/lose.
  - Open source: currently private. **Consider making it public for submission**, since open source is a judging criterion.
- **Conflict:** Colosseum allows one submission per team. Kickoff can't enter Monad as well unless it's a separate, new build.

### 3.2 002 Busha for Stocks → BNB Hack: Tokenized Stocks
- **Why it's a strong match:** the brief asks for "autonomous agents, trading interfaces, portfolio tools, dashboards, Telegram bots, or MCP servers using tokenized equities". A Nigerian-first naira-to-stocks app is a clear consumer angle on that.
- **Requirements to meet:**
  - Binance Web3 API modules.
  - One of bStocks, Ondo or xStocks *central*.
  - PancakeSwap on BSC mainnet.
  - The **Developer Experience Report** is worth 25% of the score, and it's easy points for someone who writes detailed docs (Delphi's Jupiter DX report is a template).
- **Special prizes worth aiming at:**
  - **Best Agentic Wallet Use ($2k):** "buy ₦5k of Apple every Friday" as an agent with a capped spending permission (Synesis's interpret → confirm pattern).
  - **Best BNB Agent Studio Use ($2k).**
- **Eligibility:** Nigeria isn't excluded (US, CA, NL, UK and JP are).

### 3.3 001 KOL Impression Streams → Monad Metropolis
See `../2026-10-monad-metropolis/SPONSORS.md` §14: Chainlink CRE oracle, MetaMask streaming permission, Privy X login, Nansen shill-and-dump guard, Agora AUSD cross-border payouts, Aurora any-chain funding.

**Secondary home:** Colosseum's **Tempo track** ($100k / 10). Tempo is a payments chain, and 001 is a payments product. But it's one Colosseum submission per team, and Kickoff is the stronger Colosseum entry.

---

## 4. Next actions
1. **Register on Colosseum today** (colosseum.com, before 12 Oct 11:59pm PT) and decide whether Kickoff goes public.
2. **Register for BNB Hack** (Google Form on the page) if you're doing 002.
3. **Apply to Metropolis** if you're doing 001.
4. **Arc Microgrants:** redeploy one Arc app to Arc mainnet and submit early (rolling review).
5. Check **Bitget AI S2** and **PayPal + AI** pages before counting on them.

## Sources
- [Colosseum World's Fair](https://colosseum.com/worldsfair) and [Official Rules PDF](https://colosseum.com/legal/Crypto%20World's%20Fair%20Hackathon%20Rules.pdf)
- [BNB Hack: Tokenized Stocks](https://bnbchain.org/en/hackathons/tokenized-stocks)
- [Arc microgrant program](https://phemex.com/news/article/arc-launches-10000-usdc-microgrant-program-for-earlystage-projects-97006)
- [Solana Mobile Clock In](https://solanamobile.com/blog/clock-in-the-solana-mobile-hackathon)
- [Qloo Agentic Hackathon](https://qloo.devpost.com/)
- [Open Agent Hackathon](https://hackathon.genai.works/)
- [Colosseum launch coverage](https://cryptobriefing.com/colosseum-crypto-worlds-fair-hackathon/)
