# Chog Monopoly (Monad Edition)

**A Monopoly-style board where every Chog NFT is a self-playing DeFi wallet.**
Built for Chogathon. Your Chog rolls the dice, moves around the board, and trades on real Monad protocols, even while you're offline.

Interactive economy sim: https://claude.ai/artifact/NJwsJPK2SNxMGxHbpVmocu

---

## The idea in plain language

1. **Your Chog gets its own wallet** (an ERC-6551 token-bound account). You deposit funds, and they stay with that Chog. Sell the Chog and you sell the wallet and everything in it.
2. **Once a day, your Chog moves around the board.** The dice are rolled for you, so you don't need to be online.
3. **Where it lands decides what it does:**

| Tile | What happens | Real protocol (planned) |
|---|---|---|
| 🚀 Launch | The Chog launches a token. Other Chogs landing here make a small trade, and the fees go to the owner. | nad.fun |
| 📈 Long | Buys a coin, betting the price rises | Uniswap or Kuru swap |
| 📉 Short | Bets the price falls, with capped leverage | Perpl (perps) |
| 🏦 Bank | Earns steady yield | Curvance or Morpho lending, shMON staking |
| · Rest | Nothing | None |

4. **You pick a personality** (Safe, Balanced, Degen, or custom rules). Your Chog follows it automatically.
5. **Weekly seasons:** the best-performing Chogs split a prize pot funded by game fees.

**Why the NFT is essential:** no Chog means no wallet, no piece on the board, and no income. Selling the Chog transfers its future income stream, and any rent earned before the sale stays with whoever owned it when it was paid.

---

## How the money works (self-sustaining)

- **The game mints nothing.** Every token that moves was first deposited by a player.
- **Gains and losses on trades come from real markets**, not from the game.
- **Fees:**
  - Launch-tile visits: 85% to the token's owner, 10% to the weekly pot, 5% burned.
  - Long and short trades: 0.3% fee to the pot.
  - Launching a token: 25 CHOG (70% pot, 30% burned).
- **No promised yield.** Owners earn only if other Chogs actually land on their tiles.
- **Conservation check:** in the sim, total bankrolls plus pot plus burn must equal total deposits plus external market PnL. The contracts should enforce a matching invariant: total claimable never exceeds the balance held.

---

## Offline play

- The daily roll is derived from an epoch seed and the token ID, and it settles lazily the next time anyone touches the contract.
- A keeper (cron-job.org or Railway) can trigger the roll daily, but anyone can trigger it if the keeper goes down.
- Each Chog has an auto-policy: stake sizes, leverage, bank share, and a minimum bankroll before it launches a token.

---

## Safety rails

- The Chog wallet can only call a **whitelisted adapter contract**, with function-level limits. It never gets arbitrary-call access.
- **Daily loss cap:** stake size is limited so one day's loss can't exceed X% of the bankroll.
- **Isolated margin:** a losing short or long can lose at most its own stake.
- **Anti-sniping:** income is credited to whoever owned the Chog at the time, so nobody can buy a Chog right before claiming.
- **Leverage defaults to off.**

---

## Architecture

- **Contracts (Solidity):**
  - `Board.sol`: registration, movement, tile resolution, fee split
  - `Adapters.sol`: whitelisted calls to nad.fun, a swap router, a perps protocol, and a lender
  - `Seasons.sol`: weekly pot and payouts
- **Chog accounts:** ERC-6551 token-bound accounts hold funds and positions.
- **Backend:** Node.js, Supabase for state, and a keeper for the daily roll. cron-job.org is optional.
- **Frontend:** Next.js board using the real Chog art, plus a wallet-free demo mode.
- **Trait groups (optional set bonus):** an indexer reads existing traits and publishes a Merkle root. This does not change any metadata.

---

## Monad integrations (all need verification before building)

- **nad.fun:** Rust and Python SDKs for trading, and an API flow for token creation (upload image, upload metadata, mine a salt, create).
- **Lending:** Curvance, Morpho, Euler, Aave.
- **Perps:** Perpl (fully on-chain order book).
- **Staking:** FastLane shMON.
- **Prediction tile (stretch):** a small custom parimutuel market. No verified on-chain prediction protocol was found on Monad.

> I have not verified any contract interfaces. Read each protocol's docs and test on a fork or testnet first.

---

## About the sim

The linked sim runs 8 Chogs on a 20-tile board. You control the gold Chog with sliders (long %, short %, leverage, bank share, launch threshold) and can adjust the economy dials: trade fee, visitor trade size, daily loss cap, and market mood.

**Sim assumptions (my guesses, not real nad.fun data):**
- Launched tokens drift slightly down, with a 6% chance of a 60% crash per visit.
- Everyone starts with 100.
- Bank yield is 0.6% per day on the parked share.
- The pot pays the top 3 by bankroll every 7 days (50/30/20).

**Questions to test with it:**
1. Do launch-tile fees earn owners enough to matter?
2. Does the loss cap protect a leveraged Chog in a bear market?
3. Does one Chog snowball by owning most launch tiles?
4. Is the weekly pot large enough to be worth chasing?

---

## Build plan (about 7 days, Monad only)

| Days | Work |
|---|---|
| 1–2 | Fee math, rules, contract skeleton |
| 3–4 | Contracts, tests, adapter whitelist, bot-based economy simulation |
| 5 | Frontend board and registration |
| 6 | Auto-policy, testnet deploy, visual polish |
| 7 | README, demo video, submission buffer |

**Scope priority:** launch tile, long tile, bank tile first. Short tile and the prediction tile are stretch goals. Confirm the real Chogathon deadline on the official site.

---

## Known risks

- **Randomness:** epoch-based seeds are demo-grade, not manipulation-proof.
- **Adapter security:** the adapter is the main attack surface and needs the most testing.
- **Economy balance:** the dials need tuning, or the game can feel dead or abusive.
- **Real losses:** use testnet or tiny amounts for the demo.
- **Competition:** other projects already use ERC-6551 NFT accounts for DeFi (for example StonkBrokers on Robinhood Chain). The differentiator here is the board-game loop and the launch-tile fee economy.
