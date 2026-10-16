# Chogathon ideation: ownership in real life

**Date:** 2026-10-16
**Inputs:**
- The Grok session: NFT as the account, "pay the token", building with NFTs what used to be built with wallets.
- Real-world ownership problems (sources below).
- Pokémon cards: Collector Crypt, Courtyard, PSA grading.
- Studio Mirai on Sui.

## 1. Where ownership breaks in daily life
| Problem | Evidence |
|---|---|
| **The paperwork doesn't travel with the thing** | Apple's warranty and AppleCare stay with the original owner and serial number. Activation Lock bricks second-hand iPhones until the previous owner releases them |
| **The handover is where scams happen** | 26% of buyers from unofficial ticket sellers say they have received a fake at least once. A common scam: the seller sends a screenshot as "proof", gets paid, and the ticket never existed. Oasis fans lost more than £2M |
| **Someone else holds your money** | In one California survey, 36% of tenants never got their deposit back. Tenants won 70%+ of the court cases they brought, but few sue |
| **Checking authenticity is slow and costly** | PSA's backlog peaked around 12.4M cards (July 2026). The cheapest realistic grading tier is about $80 per card |
| **Fakes copy the certificate itself** | A Jan 2026 conviction involved fake PSA labels on about $2M of cards. Slabs themselves are being cloned |

## 2. What Pokémon cards teach
- **The slab is the trust layer.** A graded case with a cert number anyone can look up. People pay for the slab, not just the card.
- **Vaulted cards can be traded instantly.**
  - Courtyard keeps cards in Brink's vaults. Redeeming the physical card burns the token.
  - Collector Crypt reached about **$1B** in cumulative trading volume. It processed **$209M of gacha (pack-opening) sales in June 2026 alone**, and more than 30% of users have redeemed physical cards.
- **Sealed product is a market of its own.** Unopened packs and boxes trade at a premium, because the mystery is the value. Opening one (the rip) is an event.
- **Condition and history set the price.** A 1st edition PSA 10 is worth far more than a played copy of the same card.

## 3. What Studio Mirai teaches (NFT brand on Sui)
- **NFTs that change state:** Prime Machin images go from black-and-white to colour.
- **Swappable traits** in the Enforcer Machin collection (composable objects).
- **Coda tickets:**
  - The artist sets resale price rules to stop scalpers.
  - The ticket **changes its look after entry**, so the stub becomes a souvenir.
  - Attendees later get perks sent to them.
- **Prints come with NFT certificates of authenticity.**

## 4. Ideas: the Chog does the job a wallet, slab or certificate used to do

### A. Chog Slab: every Chog is a sealed case
- **What it is:** a container tied to the token ID (ERC-6551, or a simple `balance[tokenId]` vault). **Anyone can put things in:** $CHOG, MON, tokens, other NFTs, tickets, IOUs.
- **Who owns the contents:** whoever holds the Chog. Selling the Chog sells the case and everything in it, in **one atomic transfer**, so a screenshot scam is impossible.
- **Its cert page** works like a PSA lookup: what's inside, when it was sealed, and the Chog's full on-chain history.
- **Problems it solves:** scams at handover, and paperwork that doesn't travel with the item.

### B. Sealed Chogs: the unopened-pack moment
- **Gifts arrive sealed:** friends, brands or launches drop gifts into a Chog, locked until a reveal date or until the owner **cracks** it.
- **A Chog with unopened gifts trades as "sealed product".**
- **The crack** is a ritual: animated, shareable, the "rip".
- **Retention:** gifts pile up and there's a reveal day.
- **Honest note:** token transfers on Monad are public, so true hidden contents need a commit-reveal escrow design. MVP option: lock-until-date with the contents hidden in the UI only.

### C. Leave your Chog at the counter: a deposit without cash
- **The analogy:** like leaving your ID card at a bike rental.
- **How it works:** lock your Chog as the bond for a deal with someone you don't know: an OTC trade, borrowing gear, a meetup booking (a no-show bond). Ownership stays with you, under a lien. The contract releases the Chog when both sides confirm, or after a timeout.
- **Why it's better than a cash deposit:** nobody can hold your deposit hostage, because the release rules are code.

### D. Ticket stubs in your Chog (the Studio Mirai pattern)
- An event ticket is issued *into* your Chog, with price-capped resale.
- After the event it becomes a **permanent stamp** on that Chog.
- Organisers send perks to every Chog that attended.
- **Your Chog becomes a passport** of everywhere it has been.

### E. Chog Patina: NFTs that age like cards
- **The art changes with this token's real on-chain life:**
  - days held → foil
  - gifts received → stickers
  - deals honoured → a gold edge
  - events attended → stamps
- **The grade:** a PSA-style score on the cert page.
- **The result:** every Chog becomes one of a kind through its story. It's the visual layer that ties A–D together.

### F. Pay the Chog (from the Grok session)
- Tips, invoices, bounties and payroll are **addressed to a token ID**.
- Any unclaimed balance is part of the price when the Chog is sold.

## 5. Recommendation
**Combine A, B and E into one product: "Chog Slab". Fill it, seal it, trade it, crack it.**

**Against the judging criteria:**
- **Novelty (30%):** the Chog becomes a graded, sealed container. That's the slab model, rebuilt on-chain.
- **Fun (20%):** the crack moment, plus sealed gifts from friends.
- **Retention (20%):** patina grows over time, gifts pile up, reveal days.
- **Clarity (15%):** "Pokémon slabs, but the case is your Chog."
- **Execution (15%):** small contracts and a polished cert page with the crack animation.

**The Chog is essential:** the token ID is the address, the case and the certificate. Without the Chog nothing works.

**$CHOG is the default filler** (bonus points).

**MVP (7 days):**
1. `SlabVault`:
   - `deposit(tokenId, token, amount, unlockAt)` and `crack(tokenId)` (requires `ownerOf`).
   - A minimum deposit, so nobody can spam a Chog with dust.
2. A history indexer, then a grade and patina layers.
3. Frontend:
   - The slab view (the Chog in a case, with a cert number).
   - Gift a Chog.
   - Crack it.
   - A public cert lookup.

## Sources
- iPhone resale: [Apple Community: used iPhone locked](https://discussions.apple.com/thread/254774396) · [The Apple Byte: used iPhone drawbacks](https://theapplebyte.net/used-iphone-drawbacks/)
- Ticket scams: [Surfshark: concert ticket fraud](https://surfshark.com/research/chart/concert-ticket-fraud) · [1 in 4 get fakes (Interaksyon)](https://interaksyon.philstar.com/?p=315154) · [Oasis scams](https://www.hellorayo.co.uk/forth/uk/news/oasis-ticket-scams) · [Swiss NCSC](https://www.bacs.admin.ch/en/25w12-en)
- Deposits: [Tenants Together](https://www.tenantstogether.org/node/8539)
- Pokémon grading: [Grading turnaround 2026](https://www.pokemonpricetracker.com/blog/posts/pokemon-card-grading-turnaround-times-2026-complete-guide) · [Spotting fakes 2026](https://www.pokemonpricetracker.com/blog/posts/spot-fake-pokemon-cards-in-2026-authentication-guide)
- Collector Crypt: [$1B volume](https://cryptobriefing.com/collector-crypt-1b-volume-solana-revenue/) · [Jupiter gacha, $209M in June](https://app.dealroom.co/news/feed/jupiter-launches-pokemon-card-gacha-with-collector-crypt-which-processed-209m-in-june)
- Courtyard: [DappRadar](https://dappradar.com/?p=31171) · [Crypto Briefing](https://cryptobriefing.com/pokemon-cards-nfts-tokenized-collectibles/)
- Studio Mirai: [Sui blog](https://www.sui.io/blog/studio-mirai-pfp-nft-music-platform) · [Docs](https://docs.sm.xyz/)
