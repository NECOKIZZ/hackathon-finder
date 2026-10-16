# 009 — Chog Monopoly

**Status:** Picked (Chogathon, registered) · **Captured:** 2026-10-16 · **Origin:** Neco ([original README](../hackathons/2026-10-chogathon/ORIGINAL-README.md))
**Deadline:** Oct 23, 15:00 UTC · **Judging:** Novelty 30% · Fun 20% · Retention 20% · Clarity 15% · Execution 15%

---

## 1. One-liner
**Monopoly where your Chog plays for you.** Every Chog is both a game piece and a wallet. It rolls every day, even while you sleep: it buys properties, collects rent and trades on real Monad markets. You make one decision a day and wake up to see what happened.

## 2. Why the Chog NFT is essential (the main Chogathon rule)
1. **The Chog is the piece.** No Chog, no seat on the board.
2. **The Chog is the wallet.** It has an ERC-6551 token-bound account holding its bankroll and properties.
3. **The Chog is the asset.** Properties belong to the Chog, not to you. **Selling the Chog sells its rent stream**, so a Chog with 3 properties is worth more than a bare one. The game adds value to the NFT itself.
4. **Traits matter (optional).** A Chog's existing traits give a small perk, for example +5% rent or one free shield per week. An off-chain index publishes a Merkle root of the traits, and no metadata changes.

## 3. Core loop: what changed from the original
The original had action tiles (Launch, Long, Short, Bank) but **no ownership**, and ownership is the heart of Monopoly's fun. The new loop is **land, buy, collect rent.**

### Board (20 tiles)
| Tile | Count | What happens |
|---|---|---|
| 🏠 **Property** | 12 (4 colour groups of 3) | Unowned: your Chog may buy it, following its personality rules. Owned by someone else: you pay rent (X% of your bankroll, capped). **Owning a full colour group doubles the rent** |
| 🏦 **Bank** | 2 | Park part of the bankroll for yield. Real integration: one lender or shMON |
| 📈 **Market** | 2 | A small long trade on a real swap. Real integration: one DEX |
| 🎲 **Chance** | 2 | A random event card: bonus, tax, move, or free shield |
| 🚔 **Jail** | 1 | Skip a day, with no rent collected or paid |
| 🏁 **Go** | 1 | Season fee goes to the pot, plus a small bonus |

### How rent flows
- Rent is a direct transfer from the visitor's Chog wallet to the owner's: **85% to the owner, 10% to the weekly pot, 5% burned.**
- No forced memecoin buys. The flow is deterministic, easy to explain, and easy to audit.
- **Stretch:** the owner can launch a token for their property group (nad.fun). Rent then buys that token instead, giving owners a $CHOG / nad.fun bonus.

### Daily decision (for Fun and Retention)
Before each daily roll, the owner picks **one of 3 cards** (for example ⚡ Double rent today, 🛡 Shield from rent, 🔁 Re-roll once). **If you forget, the Chog's personality picks for you.** This keeps the "plays while you're offline" promise but gives a reason to open the app every day.

### Morning report (for Retention)
- *"While you slept: your Chog landed on Marina Ave and bought it. It paid 2 rent and collected 9. Bankroll +4.1%. Rank #3 this season."*
- A shareable card for X: the Chog art plus that day's result.

### Seasons
- Weekly. The pot comes only from fees.
- Top 3 by net worth (bankroll + properties at cost) split it 50 / 30 / 20.
- Properties reset each season, which stops one Chog from snowballing forever.

## 4. Money rules (unchanged from the original, kept tight)
- The game **mints nothing**. Every token moving was deposited by a player.
- Trading gains and losses come only from real markets. **No promised yield.**
- **Invariant enforced in the contract:** total claimable ≤ balance held.
- **Safety rails:**
  - The Chog wallet can only call a whitelisted adapter.
  - Daily loss cap.
  - Leverage off. Perps are cut from the MVP.
  - Income goes to whoever owned the Chog when it was paid.

## 5. MVP scope (7 days, alongside Veil)
**Must have:**
1. `Board.sol`:
   - Register a Chog (which creates its ERC-6551 account).
   - Daily roll and movement.
   - Buy properties, pay rent, colour-group bonus.
   - Cards, Jail, Go and the pot.
2. **Randomness:** a verifiable random number from Pyth Entropy if it's on Monad (check first). Otherwise, epoch seed + block hash, labelled as demo-grade.
3. **Keeper:** a daily roll that anyone can trigger.
4. **Frontend:**
   - The board in Chog art, a "my Chog" page, card picking, the morning report.
   - **Judge / demo mode:** test Chogs, so judges can play without owning one.
5. **Bank tile with one real integration.** Pick one: shMON staking or a single lender.

**Nice to have:** a Market tile with one real swap, trait perks, the X share card.

**Cut:** perps (Short tile), nad.fun token creation, a prediction tile.

## 6. Pitch (for "Clarity")
- **Line 1:** "Monopoly where your Chog plays for you."
- **Line 2:** "Every Chog is a wallet. Its properties earn rent from other Chogs. Sell the Chog, sell the empire."
- **Demo video (≤ 3 min):**
  1. Register a Chog.
  2. Pick a card.
  3. Fast-forward 7 days with bots.
  4. Morning reports.
  5. Season payout.
  6. A Chog with properties sold on a marketplace.

## 7. Risks and open questions
1. **The Chog NFT collection itself:** contract address, supply, number of holders, and which chain (Monad mainnet?). Needed before choosing between mainnet and testnet.
2. **Testnet or mainnet:** judges need access, so demo mode is required either way.
3. **$CHOG liquidity is thin** (~$18k across Monad pools). Use $CHOG for fees, entry and bonuses, not large swaps.
4. **ERC-6551 registry on Monad:** check it's at the canonical address. If not, deploy it.
5. **Time:** this clashes with Veil (Ascend, Oct 20). Chogathon has 50 winners and you're registered, so give it priority if time gets short.
6. **Gambling optics:** dice plus money. Frame it as a strategy game with capped losses, use small amounts, and keep a no-money demo mode.
7. **Economy balance:** reuse the existing sim to tune the rent %, the cap and the property prices.
