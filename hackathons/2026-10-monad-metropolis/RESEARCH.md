# Monad Metropolis — Research Report

**Researched:** 2026-10-04 · **Deadline:** **13 Oct 2026 (9 days left)** · **Status:** applications open at [hackathon.monad.xyz](https://hackathon.monad.xyz)
**Source:** [monad.xyz/developers/hackathons/metropolis](https://monad.xyz/developers/hackathons/metropolis), Monad docs. Per-bounty requirements sit behind the portal login and still need to be read there (see §8).

---

## 1. The facts

| | |
|---|---|
| Organizer | Monad Foundation |
| Format | Online, global. One-day hacker houses in 7 cities; Singapore on 6 Oct is the only one left |
| Build window | 1 Sep → 13 Oct |
| Judging | 14 → 27 Oct, per track. Winners announced 3 Nov |
| Pool | $250k+ |
| Team | Solo or team allowed. No prior on-chain experience needed |
| Submit | Working product + public project profile: **demo, short write-up, code link** |
| Chain | Monad mainnet (chain ID 143). EVM bytecode-compatible, 300 ms blocks, 600 ms finality, sub-cent fees, MON for gas, native USDC from Circle |
| After | Project profile stays live. Teams can join **DeltaV** (800+ Monad startups: credits, intros, office hours). Top teams get invited to a residency |

### The new-work rule (read this first)
> "Can I submit an existing project? Yes, if the work you submit is new. Bring an existing team and existing context, but what you show on 13 Oct should have been built during the six weeks."
> "Open sourcing is encouraged but not required. Judges need to be able to verify what you built during the six weeks."

**What this means for us:**
- Work in a **fresh repo**, where every commit falls inside the window.
- Reused libraries (engines, pipelines) can come in as **dependencies**, and the README should say so.
- The demo should show only what was built for Metropolis.
- Polishing an old repo and resubmitting it won't qualify.

---

## 2. Prize structure

| Prize | Amount | Notes |
|---|---|---|
| 4 tracks | $30k each, **$10k to each of 3 teams** | You pick one track when you apply |
| Grand champion | $25k | Chosen across all tracks |
| Winner perks | ~$69k in kind | Security scan (ack3, $15k), RPC, Tenderly, Zerion, Envio hosting and similar. Only goes to winners |
| Sponsor bounties | Listed below, on top of track prizes | Open to every team |

**Sponsor bounties listed on the page:**

| Bounty | Prize | Fit for us |
|---|---|---|
| Agora: Best Cross-Border Payments App on Monad | **$10,000** | High (Synesis) |
| Agora: Best Mobile Trading App on Monad | $10,000 | Low |
| Kuru: Build the Next Consumer Trading App | $5,000 | Low–Med |
| Kuru: Bring New Assets and Markets | $5,000 | Med (proximity markets as a new market type) |
| Perpl: Best use of Perpl's API | $5,000 | Low |
| Perpl: Best Analytics / Risk Tool | $3,000 | Med (contract-info, Delphi-style scoring) |
| Dynamic: Best Use of Dynamic | $5,000 | Med (wallet onboarding) |
| Privy | $5,000 | Med (Kickoff already uses Privy) |
| Nansen: Best use of Nansen | $5,000 | Low–Med |
| Best Community Team Project | $5,000 | Low (we're solo) |
| Bring Any-Chain Liquidity to Monad | $5,000 | Low |
| Chainlink: Best workflow with CRE | $3,000 | Med (CRE for an off-chain data/AI step) |
| Mera: Best Mera-Powered UX on Monad | $2,500 | **High** |
| Mera: One Passkey, Many Keys | $2,500 | **High** |
| Best Agent Wallet Plugin | $2,500 | **High** (Synesis or Kickoff AgentVault) |
| Best Integration of CVI/CVA | $2,000 | Unknown, check portal |
| Envio: Best Use of Envio | $1,000 | Med (indexer) |
| Alchemy / Hunyuan / KIMI / Qwen | credits | Ignore |

---

## 3. The four tracks and what judges want

The page gives a "best fit" profile and three example builds for each track. Those examples tell you what the judges want to see.

| # | Track | Best fit (their words) | Example builds | Our fit |
|---|---|---|---|---|
| 01 | Onchain Finance & Trading | "Teams who have shipped a trading, lending, or market-making product before" | Fully on-chain order books; perps with per-block funding; undercollateralised lending on on-chain credit | **Med.** Kickoff and Lock-In are shipped markets, but not the kind they describe |
| 02 | Consumer Products & Payments | "Product teams who care more about a user's first five minutes than the architecture" | **A payments app that never mentions a blockchain**; per-second subscriptions; **shared wallets / group spending that settle up** | **High.** This is Synesis's core rule ("never show crypto complexity") |
| 03 | Social, Attention & Culture | "Teams who have **grown a community**, not only built one" | **A feed where curation is paid for by the people who benefit**; portable ticketing; **markets on cultural outcomes** | Good idea fit (Cuerate paid likes, proximity markets), but weak team fit: no community traction |
| 04 | Trust, Identity & AI Infra | "Teams comfortable with cryptography, protocol design, or **agent frameworks**" | Passkey (P256/WebAuthn) accounts; **agent identity and reputation under ERC-8004**; **provenance for generated media that survives re-encoding** | **Highest.** The Cuerate RE Agent plus Cuerate lineage hit 2 of the 3 examples |

### What Monad itself is pushing
Each of these has its own guide in Monad's docs, which suggests the Foundation is promoting them. Using them shows you're aligned with the ecosystem:
- **Mera:** passkey → deterministic EOA, client-side only, no bundler, no MPC. Works on web and iOS/Android. ([docs](https://docs.monad.xyz/guides/mera))
- **x402 Facilitator:** hosted, covers gas, **USDC on Monad**, mainnet and testnet. Monad's API Hub already has 66 pay-per-call services. ([docs](https://docs.monad.xyz/tooling-and-infra/agentic-payments))
- **ERC-8004:**
  - Identity Registry `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
  - Reputation Registry `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`
  - Validation Registry: "coming soon"
  - Tooling: agent0 SDK in TS and Python. ([docs](https://docs.monad.xyz/guides/erc-8004))
- **AUSD (Agora):** the largest stablecoin on Monad, at about $73M.

---

## 4. Our projects scored against Metropolis

Scores run from 1 to 5. "New-work cost" is how much has to be built from scratch to meet the rule.

| Project | Best track | Idea fit | Bounty stack | New-work cost (9 days) | Verdict |
|---|---|---|---|---|---|
| Cuerate RE Agent + Cuerate lineage | **04** | 5 | Mera ×2, x402, Envio, Agent Wallet Plugin | Medium: new registry contract, robust-hash matching, 8004 + x402 wiring, UI | **Primary pick** |
| Synesis (agentic wallet) | **02** | 5 | **Agora $10k**, Mera ×2, Agent Wallet Plugin | High: the Arc/Circle stack has to become Monad + Mera + AUSD | **Strong alternative** |
| Kickoff / Lock-In proximity engine | 01 or 03 | 3 | Kuru "new markets", Privy | Low to port, but a port is weak "new work" | Skip unless reframed |
| Cuerate (paid curation feed) | 03 | 4 | — | Medium | Track 03 favours community traction we don't have |
| contract-info | 01 (Perpl Analytics/Risk) | 2 | Perpl $3k | Low | Possible small side bounty |
| Archer | — | 1 | — | — | Skip |

---

## 5. Recommended play

### Primary: Track 04, "Provenance for generated media that survives re-encoding"
**Why:**
- It matches two of the track's three example builds (media provenance, ERC-8004 agent identity).
- It reuses the RE Agent pipeline as a dependency.
- Track 04's "best fit" profile (crypto, protocols, agent frameworks) narrows the field more than Track 02's.

**The core insight:** C2PA metadata is **stripped** whenever a platform re-encodes a file. That's the real problem behind the track's wording. Provenance that survives has to live **off the file**: an on-chain record keyed by a **perceptual hash** (e.g. PDQ or pHash), which still matches after compression, resizing and light crops.

**Working concept (to be refined at the ideation step):**
1. **Register.** At generation or post time, a creator signs in with a **Mera passkey** and registers `perceptual hash + prompt + model + parent lineage` on Monad. 300 ms blocks make this feel instant.
2. **Verify.** Anyone drops in an image, even a screenshot or re-encoded copy. An **Envio** index of registry events finds the nearest hash by Hamming distance, then returns the creator, prompt, lineage and registration time.
3. **Fallback agent.** With no registry match, the **RE Agent** (registered under **ERC-8004**, paid per call through **Monad's x402 facilitator** in USDC) reconstructs a likely prompt and model family with a trust score. Callers leave **reputation feedback** in the 8004 Reputation Registry.
4. **Royalties (optional).** Port Cuerate's lineage split so derivatives pay upstream.

**Bounties this could stack:** Mera ×2 ($5k), Best Agent Wallet Plugin ($2.5k), Envio ($1k). x402 and ERC-8004 have no bounty but align with Monad's own docs.

**Ceiling:** $10k track + $25k grand champion + ~$8.5k bounties.

### Alternative: Track 02, a cross-border payment app that never mentions crypto
Synesis's agent core (interpret → PIN confirm, triggers, recurring payments) becomes a consumer remittance and group-spend app on Monad:
- Mera passkey onboarding.
- **AUSD** rails, aimed at **Agora's $10k cross-border bounty**.
- Human names instead of addresses.
- "Split this with Tolu and Ada" group settle-up, which is one of the track's own examples.

Higher bounty upside, but a heavier port in 9 days, and Track 02 will be the most crowded track.

**Do both only if** the portal allows more than one project per person. Check this when applying.

---

## 6. 9-day plan (primary)

| Day | Date | Work |
|---|---|---|
| 0 | 4 Oct | **Apply in the portal.** Read every bounty's exact requirements. Pick Track 04. Create the fresh repo |
| 1–2 | 5–6 Oct | Registry contract (Foundry) on Monad testnet; perceptual-hash library + robustness test set (re-encode, resize, crop) |
| 3 | 7 Oct | Envio indexer + Hamming-distance lookup API |
| 4 | 8 Oct | Mera passkey sign-in + register flow in the UI |
| 5 | 9 Oct | RE Agent fallback behind x402 (Monad facilitator) + ERC-8004 registration + reputation write |
| 6 | 10 Oct | Verify page: drop image → provenance card. Deploy to Monad mainnet |
| 7 | 11 Oct | Your review. Bug bash. Robustness numbers for the write-up ("matches after X% JPEG, Y% resize") |
| 8 | 12 Oct | Demo video (motion-storyboard + screen capture), write-up, README |
| 9 | 13 Oct | Submit with a buffer. Don't submit on deadline day |

---

## 7. Risks

- **New-work verification.** Fresh repo, dated commits, and the README lists reused components (RE Agent pipeline) as prior work.
- **Perceptual-hash limits.** Hashes survive re-encoding and resizing, but not heavy crops or edits. State the measured limits honestly; judges in this track will probe it.
- **Validation Registry isn't live** on Monad yet, so use only Identity + Reputation.
- **Track 04 judges are technical,** so the demo has to show the mechanism, not just the UI.
- **9 days solo.** Cut royalties (step 4) first if time runs short.

---

## 8. Open questions (answer from the portal)

1. Exact requirements for the Mera, Agent Wallet Plugin, Envio and Agora bounties.
2. Can one person submit more than one project or enter more than one track?
3. Does the submission have to run on mainnet, or is testnet enough?
4. Country restrictions in the official rules.
5. Is there a required demo-video length or format?
