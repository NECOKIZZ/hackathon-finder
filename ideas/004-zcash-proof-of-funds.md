# 004 — Zcash Proof of Funds (pure ZK)

**Status:** Captured · **Captured:** 2026-10-04 · **Origin:** Neco (from the Zecathon idea list, #4)
**Working name:** TBD

---

## 1. One-liner
Prove "I can pay X" from a Zcash shielded wallet without revealing your balance, your address, your history, or anything that links to your future payments.

## 2. Problem
Anyone who has to prove they can pay has to over-share:
- **Visa applications:** embassies demand full bank statements.
- **OTC trades:** counterparties want proof of funds before holding a deal.
- **Rentals, loans, crowdfunding pledges.**
- **Auctions:** only bidders who can actually pay should bid.

Even exchanges can't easily prove reserves of shielded ZEC. Today's options are to reveal everything, or to trust a third party.

## 3. How it works
**The proof states:** "I own a Zcash Orchard coin that (1) exists on-chain, (2) is mine, (3) is unspent as of block N, and (4) is worth ≥ X." Nothing else is revealed.

- **Exists:** Merkle path from the note commitment to an Orchard anchor (Sinsemilla hash, as in Zcash's own spend circuit).
- **Mine:** prove knowledge of the keys that derive the note's address. Sign the verifier's challenge with a re-randomized key, so the proof can't be replayed and the real key stays hidden.
- **Unspent (the hard part):**
  - Revealing the nullifier would link the proof to the later spend.
  - Instead, build an **indexed (sorted) Merkle tree of all published Orchard nullifiers**. Anyone can rebuild it from the chain to check our root.
  - In-circuit, compute the note's nullifier privately and prove it falls *between two adjacent leaves*, i.e. it isn't in the set. Same technique Aztec uses for nullifier non-membership.
- **≥ X:** range check on the note value.
- **Simplification:** the wallet first merges coins into **one note ≥ X** (a normal shielded self-transfer), so the circuit proves a single note.

**The verifier learns:** someone owns ≥ X, unspent, as of block N. **Not** the exact amount, address, history, or anything linkable to future spends. No throwaway account, no handing over keys.

**Inherent limit:** "unspent as of block N" is like a dated bank statement. Zcash can't lock the coin afterwards.

## 4. Ways to generate the proof
| Approach | Notes |
|---|---|
| **A. Custom halo2 circuit (preferred)** | Zcash's own proving system, no trusted setup. Reuse audited `halo2_gadgets` (Sinsemilla, Poseidon, ECC); adapt parts of the `orchard` crate's circuit. Hardest to write, but pure maths. Claude can write it, with cheat tests (low value, spent note, someone else's note, replay) for every constraint |
| B. zkVM (SP1 / RISC Zero) | Plain Rust using the `orchard` crate. Easier to write; proving may be slow (Pallas curve maths). Measure in a 3-day test |
| C. TEE agent | Enclave checks the wallet and signs an attestation. Easiest, but trusts hardware, which Zcash judges may dislike. Fallback only |
| (Rejected) Throwaway "proof wallet" + viewing key | Practical, but Neco dislikes handing over a viewing key and locking funds in a separate account |

## 5. Zecathon fit (thezecathon.com)
**Facts** (from the site's data file, 2026-10-04):
- Build window **28 Sep – 28 Oct 2026, 23:59 UTC**. Judging 29 Oct – 22 Nov; winners 23 Nov.
- **Prizes:** 5 tracks × $15k (Shielded Payments, Private Markets, Cross-Chain, Core & Tooling, Wildcard) + **$20k grand prize** + $5k community bounties. The split is marked "placeholder" in the source.
- **Criteria:**
  - Privacy: "leaks are disqualifying".
  - Usefulness: "would someone use this on Monday".
  - Execution: "working beats ambitious".
  - Originality: "built for this hackathon".
- **Rules:**
  - All code written in the build window (libraries are fine).
  - Open source at submission.
  - **One submission per account, one track.**
  - Prizes paid in shielded ZEC.

**Track:** **Core & Tooling** (a primitive other apps plug into), or Private Markets ("prove you can pay before you bid").

| Criterion | Score | Why |
|---|---|---|
| Privacy | 🟢 | Only "≥ X as of block N" is revealed. Needs a written threat model |
| Usefulness | 🟢 | Visas, OTC, rentals, auction eligibility, exchange reserves |
| Execution | 🟡 | Biggest risk: the non-membership circuit plus the nullifier indexer |
| Originality | 🟢 | Long-wished-for, with no working tool for shielded Zcash |

## 6. Build outline (if picked)
1. Exists + ≥ X circuit (days 1–3)
2. Ownership + challenge binding (4–7)
3. Unspent via indexed nullifier tree (8–12)
4. Nullifier indexer publishing roots per block (10–14)
5. CLI prover, web verifier, merge-coins wallet step (15–20)
6. Threat model, testnet demo, video, docs (21–24)

**Fallback:** if step 3 stalls, submit ownership + amount + indexer, and present "unspent" as the next milestone.

## 7. Open questions
- How many Orchard nullifiers exist (sets the indexed tree's size and indexing time)?
- Chain data access from the build environment (lightwalletd / Zebra)?
- Which `orchard` circuit pieces are private and need adapting (credit them)?
- Repo: new repo, private until submission (must be public by 28 Oct).
