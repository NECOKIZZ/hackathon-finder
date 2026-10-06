# 008 — Private Dead Man's Switch (shielded ZEC inheritance)

**Status:** Picked (Zecathon, alongside 005 Ajo) · **Captured:** 2026-10-06 · **Origin:** Neco's master plan, Idea A
**Working name:** TBD

---

## 1. One-liner
If you stop checking in, your shielded ZEC passes to your heir on its own. No guardians, no lawyer, nothing visible on-chain.

## 2. Problem
- Estimates put **3–4 million BTC** (roughly a fifth of supply) as lost forever. A large share belonged to holders who died or became incapacitated without passing on their keys.
- With shielded ZEC it's worse: an heir can't even *find* the money on a block explorer. If the keys die with you, the funds are gone and nobody will ever know they existed.
- Today's options: write the seed phrase in a will (the lawyer, the family and anyone who finds the paper can take it), trust guardians, or use a custodian. All of them hand trust or visibility to someone.

## 3. How it works
- **Time-lock encryption (drand tlock):** encrypt something so it can only be opened after a future date. drand is a public randomness network run by many independent organisations, and it publishes a new key every 3 seconds. Nobody has a round's key before that round arrives.
- **Setup:** the owner's app creates a fresh shielded wallet **W1** (the "legacy pocket") and the owner moves ZEC into it. The app time-locks W1's spending key to date **T1** (e.g. 90 days out) and delivers it to the heir.
- **Check-in ("I'm alive"):** the app creates **W2**, moves everything W1 → W2, and time-locks W2's key to **T2**. The heir's old copy now opens an empty wallet. **Revoking = moving the money.** That's the clever bit: a time-lock can't be cancelled, so we make the old one worthless instead.
- **Owner goes silent:** at the latest date, the heir's file opens and the heir's app sweeps the funds into the heir's own shielded wallet.

### Family mode: heirs must agree (2 of 3)
The master plan's multi-key options were **guardians** (people co-sign with FROST, which is trust in people and Ajo's hardest code twice) and **split amounts** (one locked pocket per heir). Family mode is a third, cheaper one.
- **Split the key, not the money.** At each check-in, the app cuts the vault key into **3 pieces (Shamir secret sharing)**. Any 2 pieces rebuild the key; 1 piece reveals nothing.
- Each piece is time-locked to T and sent to **its own heir** in a shielded memo, the same way as the single-heir mode. A piece is ~33 bytes, so it fits easily.
- **After T:** one heir alone opens their piece and gets "you need 1 more family member". When a second heir's app sends its piece over (as a shielded memo), the key is rebuilt and the vault is swept **according to the owner's will**. The split (e.g. 50 / 25 / 25) is written into the locked message, so the app follows it.
- **All heirs also receive the vault's read-only viewing key**, locked to T. So every heir can check the payout matched the will.
- **What it buys:**
  - no single heir can take it alone;
  - **losing one piece doesn't lose the money**;
  - the "heir keeps the file safe" risk is spread across the family.
- **Honest limit:** whoever's app rebuilds the key briefly holds the whole key. A cheating heir who bypasses the app could sweep it all. **Everyone would see it** (viewing key), but it can't be *prevented*. Truly preventing it needs FROST guardians (stretch). Say this on the trust slide.
- Configurable: 2-of-2, 2-of-3, 3-of-5. Single-heir mode is just 1-of-1.
- Cost: ~1–2 days (a Shamir crate, e.g. `vsss-rs`, plus the "send my piece" flow).

### Improvements over the master plan
1. **Deliver the will through Zcash itself.** Each check-in also sends the heir a 0-value shielded note whose **encrypted memo carries the new time-locked key**. No files to email or lose. The memo is only readable by the heir, and the key inside it only opens at T. So the master plan's "heir keeps the file safe" assumption mostly goes away. **VERIFY:** that a tlock ciphertext of a 32-byte key fits a 512-byte memo (binary, not armoured); if not, split it across 2 notes.
2. **The heir's wallet doubles as a "last seen" signal.** Each check-in note tells the heir "still alive, next date T". The heir learns nothing about the amount until it opens.
3. **Grace and reminders:** the app nudges the owner at T − 14 days, T − 3 days and T − 1 day. A check-in must confirm before T.
4. **Comparison slide, not a feature:** the transparent CLTV vault is enforced by the chain but shows everything; guardians/FROST work but you trust people.

## 4. Who sees what
| | Public | Heir before T | Heir after T | drand |
|---|---|---|---|---|
| A vault exists | ❌ | ✅ (gets check-in notes) | ✅ | ❌ |
| Amount | ❌ | ❌ | ✅ | ❌ |
| Check-ins happen | ❌ (ordinary shielded txs) | ✅ | ✅ | ❌ |
| Can spend | Owner only | ❌ | ✅ if the owner went silent (family mode: only once enough heirs combine pieces) | ❌ |
| Payout matched the will | ❌ | ❌ | ✅ (family mode: every heir, via viewing key) | ❌ |

## 5. Honest trust assumptions
- **drand doesn't leak a key early.** That needs a threshold of its independent operators to collude. Minimal, not zero.
- **drand still exists at T.** T is never more than about 90 days away, so this only fails if drand shuts down *and* the owner dies within the same window. Say it on the risk slide.
- **Checking in late:** if the owner misses T, the heir can open the file, even if the owner turns out to be fine. Reminders and a buffer make that unlikely.
- tlock libraries are unaudited (the Rust crate says so).
- **Family mode:** the heir who rebuilds the key holds it briefly. Cheating is visible to the other heirs, not prevented.

## 6. Judge's verdict (vs Ideas B and C from the master plan)
| | **A: Dead man's switch** | C: Sealed-bid auction | B: OTC escrow |
|---|---|---|---|
| Story | 🟢🟢 Lost BTC + "invisible money dies with you" | 🟡 | 🟡 |
| Prior art | **Inheritance already wins:** Legacy Vault won Zama's Dec 2025 builder track; several EVM versions at ETHGlobal. **None on shielded Zcash found** | Whisper exists; needs a coordinator | **Aegis Gate (FROST 2-of-3 escrow) is already a Zecathon entry**, plus Zafe, Steward |
| Difficulty | 🟢 Low–medium: wallet ops + tlock. No circuits, no FROST | 🟡 | 🔴 FROST |
| Demo | 🟢🟢 Live unlock on a 2-minute timer | 🟢 | 🟡 |
| Shares code with Ajo | 🟢 The same Rust Zcash core: keys, scanning, memos, sweeping | 🟡 | 🟢 FROST, but that's Ajo's riskiest part, doubled |

**Pick A.** Drop C and B.

## 7. Zecathon fit
- **Rule check:** "one submission per account, one track". Two products need **two team accounts**, one per product. **VERIFY** with the organisers.
- **Tracks:** Ajo → **Shielded Payments**. Dead man's switch → **Core & Tooling** ("a primitive any wallet can add") or **Wildcard**. Different tracks, so the two don't compete with each other.

## 8. MVP scope (~8–10 days of work)
| Piece | Build |
|---|---|
| Shared core (with Ajo) | Rust: create a shielded key, scan an address, build/sign/broadcast a sweep, send a memo (librustzcash, testnet lightwalletd) |
| Time-lock | `tlock_age` (Rust, wasm-compatible) against **drand quicknet** (3 s rounds) |
| App | Tiny web or desktop app with three buttons: **Create vault** · **I'm alive** · **Claim** |
| Family mode | Shamir 2-of-3 split per check-in, one piece per heir, "send my piece" + rebuild + sweep by the will's split. **Core, not stretch** (~1–2 days) |
| Demo | 2-minute timer. The heir tries to open it early and fails; the owner checks in and the old key opens an empty wallet; the owner goes silent; it unlocks live and the heir sweeps. Then show the explorer: nothing to see. **Family finale:** 3 heirs; one tries alone ("need 1 more"); a second joins; it unlocks and pays 50/25/25; every heir sees that the split matched |
| Stretch | Reminder bot · guardian (FROST) mode reusing Ajo's FROST code (fixes family mode's "rebuilder holds the key" limit) |

## 9. Open questions
- Is a 0-value Orchard output with a memo allowed and relayed? (Otherwise send dust.)
- tlock ciphertext size vs the 512-byte memo.
- Desktop (shared with Ajo's Tauri shell) or web?
- Family mode: should the will's split also be enforced by paying each heir from a separate pocket? Safer, but it gives up "one lost piece doesn't lose the money" for each heir's own pocket.
