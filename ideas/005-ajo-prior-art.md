# 005 — Ajo: Prior Art and Iterations

**Researched:** 2026-10-06 · **Feeds:** [005 Ajo](005-ajo-savings-circle.md) · Zecathon (28 Oct) and Midnight Buildathon Wave 3 (27 Oct – 16 Nov)

The question: has anyone built a private ajo/ROSCA before, did it win, and what can we take from it? Short answer: **plenty of public on-chain ajo, a few private ones, and nobody on shielded Zcash.** The private ones each solved one piece; none solved all of it.

---

## 1. Closest prior art

| Project | Where | What it did | Result | Gap we exploit |
|---|---|---|---|---|
| **[Sharibo](https://github.com/Jessepriase/sharibo)** | Stellar Hacks: Real-World ZK | 5 members fund a pot; the winner claims it with a Groth16 proof of "I'm an unpaid member", to a fresh address. Nobody, not even members, can link the payout to a member | No prize mentioned | **Deposits are fully public.** Only one round demoed, no rotation order, no default handling |
| **[Àjọ (KaJota)](https://github.com/KaJota-inc/kajota-zama)** | Zama Developer Program | A confidential PoolTogether on FHEVM, branded as esusu. The same encrypted rail runs 3 modes: random draw (Premium Bonds), **sealed-bid chit fund** (homomorphic argmax over encrypted bids), survivorship tontine. Adds a "trust circle": encrypted spend mandate for agents + shared encrypted fraud registry | Sepolia, 32 tests | It's prize savings (yield lottery), not a real rotation. Nobody in Nigeria runs ajo like that |
| **Silent Loan Circle** ([forum post](https://forum.midnight.network/t/midnight-hackathon-experience-feedback-next-bus-stop/448)) | Midnight hackathon | Privacy-preserving ROSCA in Compact, Next.js UI, Lace wallet | Didn't win; author got an MLH fellowship invite | Prototype only. The write-up is about toolchain pain (wasm imports, Node 23 crashes). **Direct warning for our Midnight build** |
| **[Saving Circles](https://ethglobal.com/showcase/saving-circles-bmgxr)** | ETHGlobal Buenos Aires | Public ROSCA. Chainlink VRF picks each round's winner; optional bids raise your odds; **seats are NFTs** you can trade | **Won the Chainlink prize** | No privacy at all. Shows judges like "fair draw nobody can rig" and "your seat is an asset" |
| **[CircleFi](https://github.com/feyisaralawal/circleFi-contract)** | Soroban | Each member locks a **deposit that covers a missed round**, so the recipient is always paid in full. Permissionless `settle()`, public default counter | — | Public. But it's the cleanest answer to ajo's #1 problem (someone stops paying after collecting) |
| Ajo / Ajo Circle / Ronda / AjoShield | Stellar ×4+, Solana | Contract-held pot, fixed schedule, USDC | Many forks of one template | All public. **Ajo itself is crowded; private ajo isn't** |

### Zcash projects we'd stand next to at Zecathon
| Project | What | Why it matters to us |
|---|---|---|
| **[Aegis Gate](https://github.com/angelraph/aegis-gate)** | 2-of-3 FROST escrow on shielded Zcash, **Zecathon Wildcard entry**, mainnet beta, Rust + WASM in-browser signing | Proves FROST on Orchard is doable inside the window. Also means **"we use FROST" alone won't impress judges**: it has to serve the ajo story |
| **[Zafe](https://github.com/zafe-cash/zafe)** | t-of-n FROST shared vault from members' phones; blind relay never sees keys/amounts; looks like a single-user wallet on-chain | Exactly the custody layer our "upgrade" describes. `zafe-core` (DKG, FROST, PCZT) is MIT/Apache. Usable as a library (Zecathon allows libraries; our code must be new) |

### The Zama projects you flagged
FHEsplit (private expense splitting), SecSanta (anonymous group gifting with encrypted contributions, iExec TEE + Zama FHE), Cibon (private carbon-credit distribution), Zama LLM Docs. *(The X posts are behind a login wall; these come from your summary.)* Common thread: **a group pot or group ledger where members contribute but amounts and identities stay hidden.** SecSanta is the closest relative: encrypted contributions to a shared group outcome. FHEsplit is the "settle up" half of ajo. None of them rotate a pot. Takeaway: Zama rewards **everyday group money made private**, which is exactly ajo's pitch.

Also: the Zama Dec 2025 bounty winners list includes **FHEVM Example Factory (@./Neco)**. That's prior FHE credibility worth a line in the submission bio.

---

## 2. Iterations worth stealing (ranked by value ÷ effort for Zecathon)

### A. Deposit covers a missed round (from CircleFi) — **do this** 🟢🟢
Ajo's real failure mode: a member collects early, then stops paying. Today it's handled by shame.
- On join, each member sends a one-round deposit into the circle's **FROST vault** (shielded).
- If a member misses a round, the co-signers pay the recipient from that member's deposit. Members see the cover in their viewing-key feed.
- At the end, unused deposits are returned.
- **Pitch line:** "The person after you always gets paid in full, and nobody outside knows any of it happened."
- Fits Zcash: no contract needed, it's just a FROST-signed payout with a memo. Fits Midnight better still: the contract enforces it.

### B. FROST custody from day one, not "upgrade" (from Aegis Gate / Zafe) — **do this** 🟢
- Aegis Gate is already in the same hackathon with FROST. An organiser-wallet MVP will look weaker next to it.
- Make the pot a t-of-n FROST address (e.g. organiser + 2 members, 2-of-3). The organiser *proposes* the payout; members *approve*. On-chain it looks like one normal shielded wallet.
- Lean on ZF's FROST libraries (and read `zafe-core` for the PCZT signing flow). Budget: if FROST stalls by day ~12, fall back to the organiser wallet + "FROST in progress".

### C. Payout-order modes (from Saving Circles + Àjọ) — **one extra mode, not three** 🟡
| Mode | Real-world name | How on Zcash |
|---|---|---|
| Fixed order | Classic ajo | Set at creation |
| Fair draw | Lottery ajo | Commit-reveal: everyone commits a hash in an encrypted memo, then reveals; seed = hash of reveals + a future block hash. Nobody, including the organiser, can rig it |
| Sealed bid | Chit fund (India), "I need it now" ajo | Members bid how much discount they'd accept to go first; bids are committed in memos, revealed together, winner's discount shared among the others |

Pick **fair draw** as the second mode: cheap, visual, and it answers "the organiser always gives himself turn 1". Sealed-bid is a strong Midnight-version feature (private state does it natively).

### D. Proof of reliable saver: reuse the scrapped 004 idea here — **stretch / pitch slide** 🟡
"Own something without exposing it" doesn't need its own project. It becomes Ajo's credit story:
- After a circle completes, the circle's FROST key signs an **attestation**: "member X paid 12/12 rounds on time in a circle of size N". No amounts, no other members, no addresses.
- A lender or a new circle verifies the signature. A member's ajo history becomes portable credit without exposing their finances. (Savings circles "should count as credit" is already a live argument in fintech.)
- Hackathon version: signed attestation + verify page. No custom ZK circuit, so none of 004's execution risk.

### E. Anonymous claim (from Sharibo) — **Midnight version only** 🟡
In ajo, members *should* know who got paid; that's the social contract. So hiding the claimant from members is wrong for Zcash. But for Midnight's private-state scoring, "prove you're an unpaid member without revealing which one" + "contract checks no double claim" is a strong 40%-on-private-state feature. Make it optional per circle.

### Skip
- **Prize-savings/yield** (Àjọ, Fumbo, Sotto, SaveTogether…): Zama Season 4 already has ~10 of these. Different product.
- **NFT seats** (Saving Circles): no NFTs on Zcash; trading seats leaks membership.
- **Agent mandates / fraud oracle** (Àjọ): clever, but scope creep for 22 days.

---

## 3. Positioning against the field

| | Public sees deposits | Public sees payouts | Organiser can run off | Missed round handled | Members can audit |
|---|---|---|---|---|---|
| Stellar/Solana ajo templates | Yes | Yes | No (contract) | Some | Yes |
| Sharibo | **Yes** | No | No | No | Partly |
| Àjọ (Zama) | No | No | No | n/a (not a rotation) | n/a |
| WhatsApp ajo today | No | No | **Yes** | Shame | Screenshots |
| **Ours (Zcash)** | **No** | **No** | **No (FROST)** | **Deposit cover** | **Yes (viewing key)** |

One-liner for judges: **"Real ajo, the way it already works on WhatsApp, minus the organiser who can disappear and minus the public ledger. Nothing leaks outside the circle; nothing is hidden inside it."**

---

## 4. Changes to the 005 plan
1. Promote FROST from "upgrade" to core (fallback: organiser wallet).
2. Add deposit-covers-missed-round.
3. Add fair-draw payout order as the one extra mode.
4. Pitch slide (stretch: build): portable "reliable saver" attestation. This is where 004 lives on.
5. Midnight version differs on purpose: contract-enforced deposit, sealed-bid mode, optional anonymous claim. Pin Node LTS and the Compact toolchain on day 1 (Silent Loan Circle's lesson).
6. Write the privacy section as *public / members-only / nobody*, like 004 §7.

## 5. Open questions
- Does ZF's FROST tooling support Orchard spends + memos in a browser/WASM flow we can build in ~10 days? (Aegis Gate says yes; check its stack first.)
- Which Zcash network does Zecathon judge on: testnet, or mainnet after NU7/Ironwood? Aegis Gate mentions both.
- Deposit size: one full round per member (simple), or less, with a cap on how many defaults it covers?
