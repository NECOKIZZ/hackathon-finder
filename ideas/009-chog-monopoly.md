# 009 — Chog Monopoly: The Landlord's Game, reborn on-chain

**Status:** Picked (Chogathon, registered) · **Captured:** 2026-10-16 · **Revised:** 2026-10-16 (v2, from first principles) · **Origin:** Neco ([original README](../hackathons/2026-10-chogathon/ORIGINAL-README.md))
**Deadline:** Oct 23, 15:00 UTC · **Judging:** Novelty 30% · Fun 20% · Retention 20% · Clarity 15% · Execution 15%

---

## 1. Start from the original game

### What Monopoly is
- Players move around a board, buy properties and charge rent to anyone who lands on them.
- Owning a full colour set multiplies the rent.
- Everyone else slowly goes bankrupt. **The game ends when one player owns everything.**

### Why it was created
- In **1904 Lizzie Magie patented *The Landlord's Game***. It was a teaching tool for the economist **Henry George**'s idea:
  - Landowners get rich just by *owning* land everyone needs.
  - Tenants pay rent they can't avoid.
  - George's proposed fix was to **tax land value and share the money with everyone.**
- Magie's game had **two rule sets:**
  - **"Monopolist":** grab everything and bankrupt the others.
  - **"Prosperity":** when anyone creates wealth, everyone gets a share, and the game is won when the *poorest* player has doubled their money.
- The monopolist rules caught on. Charles Darrow sold a version to Parker Brothers in **1935** and was credited as its inventor. Magie sold them her patent for **$500**.
- **The game everyone plays today was meant as a warning, not an instruction.**

### What it really shows
1. **Owning beats working.** Passing Go pays a fixed salary, but rent keeps growing.
2. **The rich get richer.** Each property bought makes the next one easier to afford.
3. **Early luck compounds.** A good first lap decides most games.
4. **Monopolies multiply returns.** A full colour set doubles rent, then houses multiply it further.
5. **Rent is unavoidable.** If you land, you pay. You don't get a choice.
6. **There's an alternative.** Magie's Prosperity rules show that shared rewards make a different and fairer game.

## 2. Why crypto fits naturally
Crypto runs the Landlord's Game every day:

| Monopoly | Crypto |
|---|---|
| Landlords collecting rent | Protocols, launchpads and LPs collecting fees |
| Passing Go | Airdrops and emissions |
| Colour-set monopolies | Whales and insiders cornering supply |
| One winner, everyone else bankrupt | Rugs, exit liquidity |

Crypto also has **a direct heir to Henry George's fix**: the **Harberger tax**, popularised in *Radical Markets* and by Vitalik Buterin.
- You set your own price for your asset.
- You pay a small tax on that price.
- **Anyone can buy it from you at that price, at any time.**
- The tax goes to a shared pot.

This rule needs **a trustless forced sale**, which only a smart contract can provide. A paper board game can't enforce it. That's why the idea belongs on-chain and not just in an app.

## 3. The game: v2
**One-liner:** *Monopoly the way its inventor intended. Your Chog plays it for you.*

### The pieces
- **Your Chog is your piece and your wallet.** Its ERC-6551 account holds its cash and its properties.
- **Selling the Chog sells its empire.** The properties belong to the Chog, so a landlord Chog is worth more than a bare one. The game adds value to the NFT itself, which is what the Chogathon rule asks for.

### The board (20 tiles)
- **12 properties** in 4 colour sets.
- **Go:** pays your salary from the shared pot.
- **2 Chance tiles.**
- **2 Bank tiles:** real yield on Monad (shMON or a lender).
- **1 Jail.**
- **2 Tax tiles:** they pay into the shared pot.

### Property rules (Harberger-style)
1. **Every owner declares a price** for each property.
2. **Daily tax** = 1% of the declared price, paid into the **shared pot**.
3. **Rent** = 5% of the declared price, paid by any Chog that lands there. A full colour set doubles it.
4. **Buyout:** a Chog landing on an owned property may **buy it at the declared price**, following its owner's auto-rules. The seller always gets the price they set.

This creates **the daily decision**:
- Set the price high: more rent and safe from buyouts, but a big tax bill.
- Set it low: a cheap tax bill, but someone will take it.

There's no single right answer, and that tension is the game. It replaces the "cards" idea from v1.

### Two ways to win (Magie's two rule sets)
Each weekly season, the shared pot (taxes, Tax tiles, 10% of all rent) is split two ways:
- **50% Monopolist prize:** split among the top 3 by net worth.
- **50% Prosperity dividend:** **shared equally by every active Chog.**

The weekly hook: *"The pot paid every Chog 3.2 CHOG this week, and the top landlord took 40."*

### Offline play
- The contract rolls for every Chog once a day. A keeper triggers it, and anyone else can too.
- Your Chog follows **auto-rules**:
  - The most it will pay to buy a property.
  - Whether it will buy out others.
  - How it re-prices its own properties (for example, raise prices by 10% after a buyout attempt).
- **Morning report:** *"While you slept: Marina Ave earned 12 rent, you paid 4 tax, Chog #412 bought out Pier St at your price of 80. Rank #5. Dividend so far: 3.1."* It comes as a shareable card for X.

### How it answers the original's problems
- **Snowballing** is solved by the Harberger rules: nobody can hold a monopoly forever if it's under-priced.
- **Early luck** is dampened by the shared dividend and the weekly reset.
- **"Plays itself, so it's boring":** the daily re-pricing and the buyout drama give owners something to do.

## 4. Money rules
- The game **mints nothing**. All money comes from player deposits.
- Bank tiles earn real yield. There are no promised returns.
- **Contract invariant:** total claimable ≤ balance held.
- **Safety rails:**
  - The Chog wallet only calls a whitelisted adapter.
  - Daily loss cap.
  - No leverage.
  - Income goes to whoever owned the Chog when it was paid.
- **$CHOG** is used for deposits, the tax and the pot. That earns the bonus points, and the amounts stay small because $CHOG liquidity is thin (~$18k).

## 5. MVP scope (7 days, alongside Veil)
**Must have:**
1. `Board.sol`:
   - Register a Chog (which creates its ERC-6551 account).
   - Daily roll and movement.
   - Harberger properties: declare a price, daily tax, rent, buyout, colour-set bonus.
   - Go, Tax, Jail and Chance tiles.
   - Shared pot and season payout (50% Monopolist, 50% Prosperity).
2. **Randomness:** Pyth Entropy if it's on Monad (check first). Otherwise, epoch seed + block hash, labelled as demo-grade.
3. **Keeper** for the daily roll and lazy settlement.
4. **Frontend:**
   - The board in Chog art, a "my Chog" page (properties, prices, auto-rules), the morning report.
   - **Judge / demo mode** with test Chogs and bots.
5. **Sim update:** retune the existing economy sim to the tax / rent / buyout model.

**Nice to have:** a Bank tile with real yield (shMON or a lender), trait perks, the X share card.

**Cut:** perps, nad.fun launches, swap tiles. They go on the roadmap.

## 6. Pitch
- **Hook:** "Monopoly was invented in 1904 as a warning about landlords. We built the version its inventor wanted, and your Chog plays it."
- **Mechanism:** "Every property is always for sale at the owner's own price. Taxes go to everyone."
- **NFT:** "Your Chog is the piece and the wallet. Sell the Chog, sell the empire."
- **Demo video (≤ 3 min):**
  1. Magie's patent (5 seconds).
  2. Register a Chog.
  3. Set prices.
  4. Fast-forward a week with bots: buyouts and morning reports.
  5. Season split (Monopolist vs Prosperity).
  6. A landlord Chog sold on a marketplace.

## 7. Risks and open questions
1. **The Chog NFT collection:** contract, chain, holders. Confirm before choosing mainnet or testnet.
2. **Balancing the tax and rent rates:** 1% and 5% are placeholders. Tune them in the sim.
3. **Hard for new players:** "declare your price" needs a one-line explanation and a sensible default (the auto-rules set it).
4. **Clashes with Veil** (Oct 20). Give Chogathon priority if time gets short.
5. **Gambling optics:** frame it as a strategy game, keep amounts small, and offer a no-money demo mode.
6. **ERC-6551 registry on Monad:** check it's at the canonical address.
