# Ajo (hidden-winner mode) — BUILDING.md

**Status:** spec, not built · **Date:** 2026-10-06 · **Idea:** [005](../../ideas/005-ajo-savings-circle.md) · **Prior art:** [005-ajo-prior-art](../../ideas/005-ajo-prior-art.md)
**Target:** Zecathon, **Shielded Payments** track. Deadline **Wed 28 Oct 2026, 23:59 UTC** (22 days from today). One submission, open source, code written in the window (libraries allowed).

---

## 1. The product in one paragraph
A savings circle (ajo) on shielded Zcash. Everyone pays the same amount every round, and each round **one member who hasn't collected yet is picked at random and gets the whole pot**. Members can check that everyone paid, that the pot went out, and that it went to someone who was allowed to win. **Only the winner knows it was them.** Outsiders see nothing at all. No single person holds the money: the pot needs several members to approve each payout. Each member also puts down a one-round deposit, so if someone stops paying, the next winner still gets a full pot.

## 2. Locked rules (MVP)
| Rule | Value |
|---|---|
| Circle size | **3–10 members** (circuits are sized for 16 slots, so we can grow later without new circuits) |
| Contribution | Fixed amount in ZEC per round, set at creation |
| Round length | Set at creation, in blocks (demo: ~30 min on testnet; real: weekly/monthly) |
| Rounds | **N rounds for N members.** Everyone collects exactly once |
| Deposit | **One contribution**, paid at join, returned at the end |
| Pot custody | **FROST t-of-n** shielded address. `t = ⌊n/2⌋ + 1`. Looks like one ordinary wallet on-chain |
| Who wins a round | Among members who haven't collected yet, **the lowest secret score wins** (§5). Scores are random and can't be linked to members |
| Payout | Whole pot for that round (contributions received − tx fee) to a **fresh address** the winner supplies |
| Missed payment | Deposit covers it. The missing member is **suspended** from draws until they repay (§6) |
| Paid member stops paying | Deposit covers one round, **and they lose their privacy**: members are told "member X collected and stopped paying" (§6) |
| Contributions | From any Zcash wallet (Zashi etc.) via a **ZIP-321 payment link/QR with a pre-filled memo**. Our app is not a wallet |

## 3. Who sees what
This is the core of the pitch. Put it on a slide.

| | Outsiders | Members | Winner | Nobody |
|---|---|---|---|---|
| The circle exists | ❌ | ✅ | ✅ | |
| Who paid this round, and how much | ❌ | ✅ | ✅ | |
| Pot balance | ❌ | ✅ | ✅ | |
| A payout happened, its amount and time | ❌ | ✅ | ✅ | |
| The payout went to an eligible, not-yet-paid member (proven) | ❌ | ✅ | ✅ | |
| **Who won the round** | ❌ | ❌ | ✅ (only their own wins) | ✅ hidden |
| Who has already collected | ❌ | ❌ | Only themselves | ✅ hidden |
| Who stopped paying after collecting | ❌ | ✅ (that's the penalty) | ✅ | |

**In one line:** outsiders see nothing; members can check everything except who won; only the winner knows.

## 4. Architecture
```
 Member's own Zcash wallet (Zashi, Ywallet…)
   │  pays contribution + deposit via ZIP-321 link (memo: circle|round|member)
   │  gives a fresh receive address when they win
   ▼
 ┌─────────────── Ajo app (one per member, Tauri desktop: Rust core + web UI) ───────────────┐
 │  Circle client, not a wallet. Holds: member secret s · FROST key share · pot viewing key │
 │                                                                                           │
 │  chain watcher ── scans pot address with viewing key (lightwalletd) → contributions, pot │
 │  prover ───────── Noir circuits (§5): score proof, claim proof, unpaid proof            │
 │  verifier ─────── checks every proof before this member's FROST share signs anything    │
 │  FROST signer ─── DKG at setup; signs payout transactions (PCZT) after checks           │
 └──────────────────────┬────────────────────────────────────────────────────────────────────┘
                        │ encrypted posts only (circle key)
                        ▼
               Relay / bulletin board (small Rust/Axum server)
               append-only log per circle: setup msgs, scores, claims, signing rounds
               sees ciphertext + IPs only; cannot spend, cannot read
```
**Key idea: Zcash has no smart contracts, so the members' apps are the contract.** Each app verifies the proofs and only then releases its FROST signature share. A payout happens only if a majority of apps agree the rules were followed.

**Stack**
- **Rust core:** `librustzcash` (`zcash_client_backend` for scanning, `pczt` for building/signing the payout), ZF `frost-core` + `reddsa` (re-randomized FROST over Pallas for Orchard), Noir verifier.
- **Circuits:** **Noir** (UltraHonk: no trusted setup), Poseidon2 hash. Proving in-app.
- **Shell:** Tauri (desktop). Rust does the crypto; a React UI runs in the webview.
- **Relay:** Axum + SQLite, ~300 lines. Same "blind relay" idea as Zafe.
- **Network:** Zcash testnet + a public lightwalletd.

**Read before writing code (libraries and references, not copied code):**
- [Aegis Gate](https://github.com/angelraph/aegis-gate): FROST 2-of-3 Orchard spends from Rust/WASM, in this same hackathon.
- [Zafe](https://github.com/zafe-cash/zafe): `zafe-core` does DKG, FROST and PCZT for a shared shielded vault (MIT/Apache).
- ZF `frost-tools` / `frost-client` docs: the reference FROST flow for Zcash.

## 5. The hidden draw (the new part)
### Setup (once)
1. Each member's app makes a random secret **`s`** and publishes a commitment **`C = H(s, "member")`** next to their name. Everyone gets the list of N commitments, `commits[]`.
2. FROST DKG makes the pot's key. Everyone derives and confirms the same pot address and the shared **full viewing key**.
3. Each member pays their deposit.

Three values come from `s`, and none can be linked to the others without knowing `s`:
| Value | Formula | Public? |
|---|---|---|
| Commitment | `C = H(s, "member")` | Yes, next to the member's name |
| Round score | `score_r = H(s, "score", circle, r, R_r)` | Yes, but anonymous |
| Claim tag (nullifier) | `nf = H(s, "claim", circle)` | Only when that member wins. Then it goes on the **spent list** forever |

### Each round `r`
| Step | What happens | Who sees what |
|---|---|---|
| 1. Pay | Everyone pays the contribution with a memo. Apps check it with the viewing key | Members see who paid |
| 2. Seed | At a block height fixed when the round opened, `R_r = H(block hash at that height, circle, r)`. Nobody knows it in advance and nobody controls it | Public to members |
| 3. Scores | **Every** member's app posts one encrypted message to the relay at a random time in the window. Unpaid members post `(score_r, score proof)`. Already-paid members post a same-size dummy | Members see the valid scores, not who posted which |
| 4. Winner | The lowest valid score wins. Only its owner can tell, because only they know `s` | Winner: "it's me". Others: "it's not me" |
| 5. Claim | The winner posts `(fresh address, nf, claim proof)` | Members see a valid claim to an address nobody recognises |
| 6. Pay out | Each app checks the claim proof, that `nf` isn't on the spent list, and that the amount equals the pot. Then it signs. At `t` shares, the payout is broadcast. `nf` goes on the spent list | Members see the payout in the viewing key: amount, a fresh address |

The last unpaid member always wins the last round. Even then, the others only know "it wasn't me", not who it was.

### Circuits (Noir, fixed size 16)
**A. Score proof**: "I'm an unpaid, unsuspended member, and this is my score this round."
- Public: `commits[16]`, `spent[16]`, `suspended[16]`, `circle`, `r`, `R_r`, `score`
- Private: `s`
- Checks:
  - `H(s,"member")` is one of `commits`;
  - `H(s,"member")` is not in `suspended`;
  - `H(s,"claim",circle)` is not in `spent`;
  - `score == H(s,"score",circle,r,R_r)`.

**B. Claim proof**: "I own the winning score, and this is my claim tag."
- Public: `commits[16]`, `circle`, `r`, `R_r`, `score`, `nf`, `addr_hash`
- Private: `s`
- Checks:
  - membership as in A;
  - `score` matches;
  - `nf == H(s,"claim",circle)`;
  - `addr_hash` is a public input, so the proof is bound to the address and can't be replayed to another one.

**C. Unpaid proof**: "Named member X hasn't collected yet." Used only by someone who missed a payment (§6).
- Public: `C_X`, `spent[16]`, `circle`
- Private: `s`
- Checks: `H(s,"member") == C_X`; `H(s,"claim",circle)` is not in `spent`.

Why it's fair: every `s` is fixed before any seed is known, and each seed comes from a future block. So each unpaid member's score is effectively a fresh random number every round, and the lowest one is a uniform pick among unpaid members.

## 6. Missed payments
"Privacy is for people who keep paying."
1. At the round's due height, the apps see that member X hasn't paid. The pot uses X's deposit to cover the missing contribution, so the winner still gets a full pot.
2. X has one round to either:
   - **post an unpaid proof (C)**: X hasn't collected yet, so they're added to `suspended` and can't win until they repay the deposit. Members learn "X is late and hasn't collected yet". That's a small leak, and only for the person who missed a payment; or
   - **not post it**: members are told **"X collected and stopped paying"**. The privacy of someone who defaults after collecting is the penalty. Social pressure comes back, as in real ajo.
3. If defaults go beyond the deposits, later pots shrink. Every winner faces the same rule, so a smaller pot doesn't reveal who won.
4. At the end, each member's remaining deposit is returned to the address in their app.

## 7. Edge cases
| Case | Rule |
|---|---|
| A winner doesn't claim within the window | The 2nd-lowest score may claim in the next window, and so on. The unclaimed member stays unpaid |
| An unpaid member is offline at scoring time | They're just not in this round's draw. Their app auto-posts when online. The final round extends until the last member posts |
| Fewer than `t` signers online | The payout waits. The UI shows "waiting for 1 more approval" |
| Duplicate or junk posts | Ignored: only valid score proofs count, and one `s` yields one score per round |
| Tied scores | Practically impossible with a 254-bit hash. If it happens, the lower score in byte order wins |
| Seed block reorg | Use the block at the fixed height after 10 confirmations |

## 8. Threat model (be upfront: Zecathon disqualifies leaks)
| Attacker | Can they… | Answer |
|---|---|---|
| The public | See the circle, amounts, members, winners? | No. All shielded |
| A member | Tell who won? | No. Scores and claims are unlinkable to commitments without `s` |
| A member | Win twice, or win as a paid member? | No. Their `nf` is on the spent list, so the score proof fails |
| A member | Bias the draw? | No. `s` is fixed before the seed; the seed is a future block hash |
| The organiser | Run off with the pot? | No. FROST needs `t` of `n` |
| `t` colluding members | Steal the pot? | **Yes.** Same as any multisig. Pick `t` as a majority |
| The relay operator | Read posts? | No, they're encrypted to the circle. **But it sees IP addresses**, and if it also teams up with a member it could match "who posted a dummy". Mitigations: every member posts one same-size message per phase, at random times; Tor is optional. Write this down |
| `n−1` members comparing notes | Learn who's left? | Yes, by elimination. That can't be avoided |
| A member who misses a payment | Keep privacy? | Partly (unpaid) or no (paid). By design |

## 9. Repo layout (new public repo at submission, private until then)
```
ajo/
  circuits/        score/, claim/, unpaid/ (Noir) + cheat tests
  core/            Rust: circle state machine, memo format, FROST, PCZT payout, proof verify
  relay/           Axum bulletin board
  app/             Tauri shell + React UI
  scripts/         5-member testnet e2e
  docs/            PRIVACY.md (public / members / winner / nobody), THREAT_MODEL.md
```

## 10. Build plan (22 days)
| Days | Work | Done when |
|---|---|---|
| 1–2 | **Spikes:** (a) FROST 2-of-3 DKG + sign one Orchard testnet spend; (b) scan a viewing key for incoming memos; (c) Noir proof verified from Rust | All three green, or switch to the fallback |
| 3–6 | Circuits A/B/C + **cheat tests**: wrong `s`, paid member scoring, suspended member scoring, claim with someone else's score, replay to a new address, wrong seed | All cheat tests fail as expected, in CI |
| 5–9 | Pot: DKG flow, shared address + viewing key, payout PCZT signed by `t` apps | 3 local apps pay a test address |
| 8–11 | Relay + round state machine (pay → seed → score → claim → sign) | One full round, headless |
| 10–14 | Tauri UI: create/join circle, pay link/QR, round screen ("not you this round" / "you won, enter address"), member audit view | Clickable demo |
| 15–17 | Deposits, missed-payment flow, suspension, end-of-circle refunds | Default scenario passes |
| 18–20 | 5-member testnet e2e, PRIVACY.md, THREAT_MODEL.md | Full circle on testnet, tx links recorded |
| 21–22 | Demo video, README, submit | Submitted before 28 Oct 23:59 UTC |

**Fallback ladder (decide by day 2, re-check on day 12)**
1. ZK stalls → **visible random order** (layer 1): same pipeline; scores are posted under names, nothing to prove. Still a pitch nobody else has.
2. FROST stalls → the organiser's app holds the pot key, but still only pays after verifying proofs. Present FROST as the next milestone.
3. Tauri/native trouble → CLI per member + a read-only web dashboard for the demo.

## 11. Demo script (3 min)
1. Five people (five app windows) create a circle: 0.01 ZEC/round, 5 rounds. Show the DKG and the same pot address on every screen.
2. Each pays from Zashi by scanning the QR. Every member's screen ticks off "paid ✅".
3. The draw: four screens say "not you this round", one says **"you won"**. The winner pastes a fresh address. Approvals 1/3 → 2/3 → 3/3 → paid.
4. A block explorer shows only an ordinary shielded transaction. **"This is everything the public sees."**
5. The member audit view: every payment in and out, the amount, "paid to an eligible member ✅ (proof verified)", **winner: hidden**.
6. Skip ahead: member 3 misses a payment. The deposit covers it, and member 3 is asked to prove they're unpaid or be named.
7. Close on the who-sees-what table (§3).

## 11b. Stretch: payout as a claim link (idea from XENIA)
[XENIA](https://github.com/jadonamite/XENIA) (Starknet, STRK20) sends private payments as **claim links**: the money waits behind a URL, and whoever opens it claims it into a wallet, with no setup beforehand. We can't reuse its code (different chain, and Zecathon needs our own code), but the idea fits ajo's users:
- **No wallet needed to win.** When you win, your app makes a throwaway Orchard key and gives its address as the claim address (§5 step 5). The pot pays it. The hidden-winner property is unchanged: it's still a fresh address only you control.
- **Claim later, or forward it.** Sweep it into Zashi whenever you like, or turn it into a link (the key sits in the URL fragment, so it never reaches a server) and send it on WhatsApp, e.g. to Mum in Lagos.
- **Warning in the UI:** a link is cash. Anyone holding it can spend it. Sweep it as soon as it arrives.
- Zcash's own draft for this is **ZIP 324 (URI-encapsulated payments)**. Check wallet support; if none, our app does the sweep with `librustzcash`.
- Cost ~1–2 days after day 17. Demo moment: "the winner didn't even have a Zcash wallet."

## 12. Open questions (day-1 spike answers most)
- Does ZF's FROST tooling sign **Orchard** spends via PCZT end to end on testnet today? (Aegis Gate says yes. Copy its approach, not its code.)
- How are the pot's non-spend key parts (`nk`, `rivk`) generated and shared after DKG? Follow ZF's guidance / Zafe's `upstream-asks.md`.
- Testnet or mainnet for judging? Aegis Gate runs a mainnet beta with tiny caps. We could do the same in the last week.
- Noir vs halo2: Noir is faster for us to build. Halo2 is Zcash-native and might impress judges more. Stay on Noir unless the spike says verifying from Rust is painful.
- ZIP-321 memo support in Zashi: confirm a payment link with a pre-filled memo works on testnet.
