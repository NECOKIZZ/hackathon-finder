# 005 — Ajo: Private Savings Circle on Zcash

**Status:** Captured · **Captured:** 2026-10-04 · **Origin:** Neco (from the Zecathon idea list, #6)
**Working name:** TBD

---

## 1. One-liner
A rotating savings circle (ajo / esusu / tontine) on Zcash. Members contribute every period and one member takes the pot each round. Members can audit who paid; the public sees nothing.

## 2. Problem
- Ajo and esusu circles run today across Nigeria, West Africa and the diaspora (and as tontines and ROSCAs worldwide).
- They depend on a trusted organiser and on WhatsApp screenshots as receipts.
- Moving them onto a public chain would expose every member's finances. On a shielded chain, they don't have to be exposed.

## 3. How it works
- Create a circle: members, contribution amount, period, payout order.
- Each member sends a shielded contribution to the circle's pot, with an **encrypted memo tagging circle, round and member**.
- **A viewing key for the pot is shared only with members.** Each member's app shows who has paid this round, the pot balance and the next recipient. Outsiders see nothing.
- On the due date, the pot pays the round's recipient, shielded.
- Late or missed payments are flagged to members (the social pressure of real ajo).

**Who holds the pot:**
- MVP: the organiser's wallet, as in real ajo, but every contribution and payout is auditable by members.
- Upgrade: **FROST threshold signing**, so several members must co-sign each payout and no single organiser can run off with the money.

## 4. Why Zcash
- Privacy from the public, transparency inside the circle. Exactly ajo's social contract.
- Payments are cheap and cross-border, for diaspora members.

## 5. Zecathon fit
**Track:** Shielded Payments. Facts and rules: see [004 §5](004-zcash-proof-of-funds.md#5-zecathon-fit-thezecathoncom).

| Criterion | Score | Why |
|---|---|---|
| Privacy | 🟢 | Must show nothing is visible from outside, and the viewing key only goes to members |
| Usefulness | 🟢🟢 | Passes "use on Monday" literally: these groups exist today |
| Execution | 🟢 | Shielded payments + memos + viewing keys. Achievable in 24 days |
| Originality | 🟢 | Cultural, authentic to Neco's context, memorable |

## 6. Risks and open questions
- Organiser trust in the MVP (FROST upgrade path).
- Wallet integration: which SDK (ZODL reference wallet / librustzcash) gives memos and viewing keys most easily?
- Naira on/off-ramp is out of scope; contributions are in ZEC.
