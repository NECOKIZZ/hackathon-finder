# 009 — Chog City: The Landlord's Game (v3)

**Status:** Picked (Chogathon, registered) · **Captured:** 2026-10-16 · **Revised:** v3, 2026-10-16
**Deadline:** Oct 23, 15:00 UTC · **Judging:** Novelty 30% · Fun 20% · Retention 20% · Clarity 15% · Execution 15%
**Sim:** [`prototypes/chog-city/index.html`](../prototypes/chog-city/index.html)
**History:**
- v1: self-playing board with action tiles ([original](../hackathons/2026-10-chogathon/ORIGINAL-README.md)).
- v2: Harberger pricing and the 1904 Landlord's Game story.
- v3 (this file): adds the async shared table and street shares from the [$MONO teardown](../hackathons/2026-10-chogathon/COMPETITOR-MONO.md), real financial systems, NFT-backed credit, and activity-based leverage.

> **Name note:** "Monopoly" is a Hasbro trademark. Lizzie Magie's *The Landlord's Game* (patent 1904) is public domain, and it's our origin story anyway. Working title: **Chog City**.

---

## 0. One line
**A living city where your Chog is your pawn, your wallet and your collateral. Buy shares of streets, collect rent, borrow against your Chog, and survive the week. Whoever plays sharpest gets rich. Whoever sleeps loses leverage.**

## 1. Look and feel (pillar 1: aesthetics)

### Art direction: a toy-box diorama
- A chunky, tilted board floating in space, like a tabletop city made of painted wood and clay.
- Warm real-time lighting: **day and night follow real UTC time**. Street lamps come on at dusk and windows glow.

### The Chog is the character
- The pawn is **your actual Chog's art**, cut out as a standee with squash-and-stretch hops from tile to tile.
- **It wears its wealth** (classic Monopoly imagery, made on-chain):

| Tier | Net worth | Look |
|---|---|---|
| Broke | below 0 / liquidated | Wears a barrel with braces |
| Renter | starting tier | Flat cap |
| Landlord | owns shares in 3+ streets | Top hat and monocle |
| Tycoon | top 10 | Gold chain, cane, a cigar puff |
| Magnate | #1 this season | Gold aura, crown, a coin trail as it walks |

- **Trait-based accessories:** the Chog's real traits show on the standee and grant perks (see §3.6).

### Streets grow as money flows in
- Buildings are driven by each street's liquidity: **empty lot → cottage → shop → tower → neon skyscraper**.
- Every viewer can see where the money is.

### Juice (animations to make)
- **Dice:** tumble with a shadow and settle with a bounce.
- **Rent:** coins arc from the payer's Chog to the shareholders, with a "RENT!" stamp and a cash-register *ka-ching*.
- **Foreclosure:** a gavel slam, a red **FORECLOSED** stamp, and the street's building greys out until it's auctioned.
- **Liquidation:** the Chog's hat flies off, the barrel drops onto it, and its streets float up into the Auction House.
- **Market Open:** at 12:00 UTC a bell rings, a ticker scrolls and the streets reprice.

### The cast (NPC characters, one per financial system)
| Character | Runs |
|---|---|
| **The Banker** (a monocled walrus Chog) | The Bank: the lending pool |
| **Uncle Chog** (shady pawnbroker, gold tooth) | The Pawnshop: NFT-backed loans |
| **The Auctioneer** | The Auction House: liquidations and foreclosures |
| **The Tax Collector** | The Commons: tax and the Prosperity dividend |
| **Madame Odds** | The Insurer: rent insurance |

**Tech, kept realistic for 7 days:** 2D sprites, CSS and Canvas transforms, Lottie or CSS keyframe stamps, Howler.js for sound. The Chog art is pulled from the collection's metadata.

## 2. Core loop
1. **Roll:** your Chog gets **1 roll per hour, storing up to 8**. Rolls you don't use are wasted once you hit the cap.
2. **Land:**
   - **Street:** pay rent to its shareholders, or buy shares in it.
   - **Special tile:** Bank, Pawnshop, Chance, Tax, Jail, Market Close.
3. **Grow:** buy shares of streets on a bonding curve. More liquidity means higher rent and a taller building.
4. **Leverage:** borrow from the Bank or Uncle Chog to buy faster than your cash allows.
5. **Survive:** pay interest, defend your streets against challenges, avoid liquidation.
6. **Collect:** claim rent. How big your claim is depends on your **Hustle** (§4).
7. **Season ends (7 days):** payouts, leaderboards, the city resets (§5).

There are **no turns**: one shared table, and you play whenever you're there (borrowed from $MONO).

## 3. Mechanics (pillar 2: the NFT and its value)

### 3.1 The Chog is the wallet
- Each Chog has an ERC-6551 account. **Every street share, loan, insurance policy and coin lives inside the Chog.**
- **Sell the Chog, sell the empire:** the marketplace listing shows the Chog's **Empire Value**, its in-game book value.
- **That creates a real trade:** buy an under-priced Chog whose empire is worth more than its price, then strip it or run it. The NFT's market price and its in-game value pull on each other.

### 3.2 Street shares (the Exchange)
- Share price = street liquidity ÷ shares. Buying raises the price, selling lowers it, with a 2% spread that goes to the Commons.
- Rent is set by liquidity and paid **pro rata to shareholders**.
- Full colour set bonus: if your Chog holds 25%+ of every street in a colour, your rent share doubles.

### 3.3 The Bank (a real lending pool)
- **Anyone can deposit $CHOG / MON and earn interest** paid by borrowers. The pool is real DeFi, with utilisation-based rates.
- Players borrow against their **street shares** (mortgages, Monopoly's own mechanic made real), up to 50% loan-to-value.

### 3.4 Uncle Chog's Pawnshop (borrow against your NFT)
Two tiers:

| Tier | What you pledge | Borrow up to | If you fall below the limit |
|---|---|---|---|
| **Empire pledge** | Everything inside the Chog (shares, cash) | 50% of Empire Value | Your **empire** is liquidated. You keep the NFT |
| **Real pawn** | **The Chog NFT itself** goes into escrow | 30% of the Chog's appraised value + 50% of Empire Value | **The Chog itself is auctioned**, with everything in it. High risk, big leverage |

- **Appraisal:** a time-weighted average of the collection's recent sales, plus trait rarity. Needs an oracle or marketplace data on Monad. **Open question.**
- **Interest:** about 2% per day in-game, so the clock is always ticking.

### 3.5 The Auction House (where the drama is)
- Liquidated empires and foreclosed streets are sold in **15-minute Dutch auctions**.
- Only players online can bid, and bargains go to whoever is watching.
- **Liquidation hunters** can track Chogs near their limit on a public **"Danger Board"**.

### 3.6 Traits are perks (the NFT's rarity matters)
- The Chog's real traits map to small, capped perks. Examples:
  - Gold horns: −8% rent paid.
  - Laser eyes: 1 free reroll per day.
  - Hoodie: +1 roll stored.
- **Cap all perks at about 10%**, so it's skill first and rarity second. Rarer Chogs are a bit stronger, so the floor price tracks the game.

### 3.7 Rent the Chog (for holders who won't play)
- Lend your Chog to a player, using delegation without transferring the NFT.
- The player runs the empire. **The owner takes a cut** (for example 30% of profits) automatically.
- Absent holders earn, players without a Chog can join, and **demand for Chogs goes up.**

### 3.8 Madame Odds' Insurance (stretch goal)
- Buy cover against big rent bills. Players can underwrite policies and earn the premiums.

### 3.9 Challenges (Harberger-lite, stretch goal)
- Anyone can **challenge** a share block at the current price plus 20%.
- The holder has **1 hour to defend**, by matching the price and paying a defence fee into the Commons. If they don't, it's sold to the challenger at that price.
- Asleep? You get paid, but you lose the street.

## 4. Pillar 3: play when you want, but absence costs leverage
| Mechanic | If you're active | If you're away |
|---|---|---|
| **Rolls** (1 per hour, store 8) | Use every roll, see more of the board | Rolls past 8 are wasted |
| **Hustle** (0.5–1.5×) | Rises with actions: rolls, trades, bids, defences | Drops 0.1 every 6 hours idle. **Rent claims are multiplied by Hustle.** The cut you lose goes to the Commons dividend |
| **Upkeep** | Tapping "tend" once a day on your streets keeps rent at 100% | Untended streets slide to 70% rent ("tenants leave"), and the building shows cracks |
| **Interest** | You can repay, refinance or add collateral | Keeps running, and liquidation can happen while you sleep |
| **Auctions and challenges** | You can grab bargains and defend | You miss them |
| **Autopilot** | Optional | **The Chog's agent plays conservatively** (rolls, pays, never borrows) for a 5% fee. You survive, but you don't thrive |

**The design rule:** nobody is forced to play, but the city keeps moving, and **the money flows to whoever is paying attention.**


## 4b. Chat and negotiation
- **City Hall:** a public group chat. Every big rent payment, deal, margin call and liquidation is announced there, and players trash-talk and advertise deals.
- **DMs:** private negotiation with any Chog. Offers are **structured cards** ("buy 2× Hash Quay at 42 each") that settle as **atomic swaps** on accept: shares and cash move in one transaction, so nobody gets scammed.
- **Bots** send unprompted offers: landlords try to complete their colour sets, and vultures DM you when your health is red ("I'll take your shares at 85% before Uncle Chog does").

## 4c. Wall Street retention: fresh money in
- **Margin calls:** when your health drops below 1.2 you get a public 📣 margin call. You can **top up from your own wallet**; fresh money pays down your debt first.
- **Nearly broke?** Top up to stay in the game, or ride it out and wait for the Prosperity dividend.
- **Why it works:** people top up rather than lose their position. That's the same loss aversion that keeps traders adding margin. **Every top-up is new money entering the city**: it grows the Bank, the curves and the Commons, and feeds the pot everyone competes for.
- **Responsible design:**
  - Practice City (play money) is the default.
  - Per-season top-up caps on the live city.
  - Clear liquidation maths.
  - No pressure loops on minors.

## 5. Seasons and money flow
- **Season:** 7 days. At the end:
  - The Commons pot pays **50% to the top 10 by net worth** (Monopolist) and **50% equally to every Chog that played** (Prosperity, Magie's 1904 rule).
  - Street shares are bought back at the curve price and the city resets.
- **Where the money comes from:**
  - Player deposits.
  - Bank interest paid by borrowers.
  - Spreads, tax and upkeep, which go to the Commons.
- **The game mints nothing.** Contract invariant: total claimable ≤ balance held.
- **Money for the demo:** a **Practice City** with play money (for judges), plus an optional live city with small $CHOG stakes.

## 6. Ways to get rich (strategy space)
- **The Landlord:** buy early into cheap streets and farm rent.
- **The Leverage Lord:** borrow at the Pawnshop and buy aggressively. A big upside, liquidation risk.
- **The Banker:** don't play. Deposit in the Bank and earn interest from everyone who does.
- **The Vulture:** hunt the Danger Board and buy liquidations at the Auction House.
- **The Arbitrageur:** buy Chogs on the marketplace whose Empire Value is above their price.
- **The Underwriter:** sell insurance and pray (stretch goal).

## 7. MVP for 7 days (Oct 16–23)
**Must have:**
1. **Contracts (Monad testnet):**
   - `City`: rolls, movement, street share curve, rent, Hustle.
   - `Bank`: deposits and mortgages.
   - `Pawnshop`: the empire-pledge tier.
   - `AuctionHouse`: Dutch auctions.
   - A 6551 account per Chog.
2. **Frontend:**
   - The diorama board with growing buildings.
   - The Chog standee with wealth tiers.
   - The dice, rent and foreclosure animations.
   - Panels: My Chog (Empire Value, Hustle, loans), the Danger Board, the Auction House.
3. **Bots** so the Practice City feels alive.

**Stretch:** real-pawn tier (NFT escrow), rent-the-Chog, insurance, challenges, trait perks, day/night cycle.

**Cut:** real stock or nad.fun-backed tiles.

## 8. Risks
1. **Scope:** this is a lot for 7 days alongside Veil. Order of work: board and shares, then Pawnshop and auctions, then Hustle. Everything else is a bonus.
2. **Appraising the NFT:** no known oracle for Chog prices on Monad. The fallback is a fixed appraisal per trait tier.
3. **Real-pawn tier:** people can lose real NFTs. Ship it in Practice City first, and make it opt-in with clear warnings.
4. **Gambling and securities optics:** frame it as a strategy game, keep play money the default, keep stakes small.
5. **Balance:** tune interest, Hustle decay and rent in the sim before writing contracts.
6. **Chog collection facts:** contract, chain, metadata access. Still to confirm.
