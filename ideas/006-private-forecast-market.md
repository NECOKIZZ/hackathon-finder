# 006 — Private Forecast Market on Zcash (beauty contest / closest-guess)

**Status:** Captured · **Captured:** 2026-10-04 · **Origin:** Neco (from the Zecathon idea list, #19)
**Working name:** TBD

---

## 1. One-liner
A private prediction market: guesses stay hidden until close, participants stay anonymous, only the result is published, and the closest guesses win.

## 2. How it works
- A question opens ("Where will ZEC close Friday?", "Guess 2/3 of the average").
- Players send a shielded stake with their **guess in an encrypted memo** to the market's address.
- At close, the coordinator decrypts guesses, computes payouts with **Kickoff's closest-guess maths** (median gate, accuracy weights), and pays winners shielded.
- Only aggregate results are published (the answer, number of winners). No individual guesses or identities.

**Why private matters:** hidden guesses stop people copying the crowd, and anonymous players can't be targeted.

## 3. Limits
- Zcash has no smart contracts, so a **coordinator** decrypts and pays out, and players trust it. Mitigation: publish a verifiable payout calculation, or use FROST for the payout key.
- Pure "guess 2/3 of the average" is a toy. Real-world questions (prices, macro data, sports) are what make it pass "use on Monday".

## 4. Zecathon fit
**Track:** Private Markets ("the price should be public and the participants should not"). Facts and rules: see [004 §5](004-zcash-proof-of-funds.md#5-zecathon-fit-thezecathoncom).

| Criterion | Score | Why |
|---|---|---|
| Privacy | 🟢 | Guesses and players hidden; only aggregates published |
| Usefulness | 🟡 | Depends on framing as real forecasting, not a game |
| Execution | 🟢 | Simple: memos + shielded payouts + known payout maths (rewritten, since existing code isn't allowed) |
| Originality | 🟡 | Kickoff's idea in a new home. Strong, but it's "prediction markets, private" |

## 5. Reuse
- Kickoff's payout maths and design, **rewritten** for the hackathon.
