# 008 — Veil on Elysium (private execution for the token path)

**Status:** Picked (Ascend Builder Competition) · **Captured:** 2026-10-16 · **Origin:** Neco ("port Veil to Elysium: fast spot trading needs privacy")

---

## 1. One-liner
**Launch fair, buy privately, exit privately.** Veil adds private execution to each stage of Elysium's token path. The first product is **sealed-bid fair launches** that can't be sniped, front-run or copy-traded.

## 2. Problem
- On every Elysium launchpad (Signal, Chainzy, PerpMe, Ascend), **bots buy in the first block** and **well-known wallets get copied** the moment they buy.
- Hyperliquid has **no privacy at all**:
  - An Aug 2026 review of Hyperliquid found no shielded transactions, privacy pools or protocol-level ZK.
  - Positions, orders and liquidation levels are all public, and whale liquidation hunting is a known problem.
- **The only fix in progress is a draft.** HIP-6 is a spot dark-pool proposal by pERC20Labs (June 2026), with 2 of its 5 phases done.
- Competitors sell privacy against Hyperliquid. Aster, for example, markets Shield Mode, hidden orders and stealth addresses.
- **None of Elysium's ~55 ecosystem projects does privacy.**

## 3. How it works

### A. Veil Launch: sealed-bid fair launch (MVP)
1. **Create.** A creator sets the token, supply for sale, minimum price, window length and the share of the raise that goes to liquidity.
2. **Commit.** Bidders submit `hash(price, amount, salt)` plus a **fixed-size deposit** (1, 5 or 25 HYPE). Fixed sizes mean the deposit doesn't reveal the real bid.
3. **Reveal.** Once the window closes, each bidder reveals their bid. Unrevealed bids forfeit a small penalty, which discourages griefing.
4. **Settle.** Every winning bid pays **one uniform clearing price**. Fills are pro rata at the margin, and unspent deposits are refunded.
5. **Graduate.** The raised HYPE plus tokens **auto-seed an AMM pool with the liquidity locked**. From there the token continues on the Ascend / Elysium path: AMM, then HyperCore spot, then HIP-3 perps.

### B. Veil Buy (roadmap)
- A shared deposit pool, then buys from fresh unlinkable addresses.
- Needs ZK membership proofs or stealth addresses (ERC-5564).
- Who it's for: KOLs and whales who want to buy launch tokens without being copy-traded.

### C. Veil OTC (roadmap)
- Encrypted RFQ (a request for quote sent to a chosen set of liquidity providers) for large sells of graduated tokens.
- Fills priced at the **HyperCore reference price**, read through Elysium's native HyperCore integration, with a staleness and deviation guard. Both legs settle together or not at all.
- This is the HIP-6 design, but Elysium-native and built for traders.

## 4. Why Elysium
- **Elysium's whole pitch is the token path:** launch, AMM, HyperCore, HIP-3. Veil makes stage 1 fair and the later stages private.
- **Fast blocks (100–200 ms)** make commit, reveal and settle quick enough to feel like a normal launch.
- **The HyperCore integration** gives Veil OTC an honest reference price.
- **Framing:** *private execution, public reference price.* We hide traders' intent, not the market. That fits Elysium's focus on market data.

## 5. Competitors
| Who | What | How Veil differs |
|---|---|---|
| Signal, Chainzy, PerpMe, Ascend | Public bonding-curve or one-transaction launches | Sealed bids, no first-block sniping, uniform price |
| HIP-6 (draft) | Spot dark pool on HyperEVM | Elysium-native, trader UX, starts at launch rather than OTC |
| Aster Shield Mode | Hidden orders on a competing exchange | Lives inside the Hyperliquid stack |

## 6. Hackathon fit
- **Ascend Builder Competition** ($17.5k, Oct 20, rules in their Discord):
  - Veil Launch is a launchpad feature that protects launchpads, so it can **complement Ascend rather than compete with it**.
  - Pitch it as stage 0 of the token path, or as a mode Ascend could offer.
- **Later:** Zecathon (Private Markets) and Elysium mainnet grants. The shielded-note work from 004 and 006 carries over to Veil Buy.

## 7. Reuse
- **The `Veil` codebase:** location and current state still to be confirmed.
- **Commit-reveal and hidden guesses** from idea 006, the private forecast market.
- **The Kickoff escrow pattern** for deposits, refunds and claims.
- **motion-storyboard** for the demo video.

## 8. MVP scope (by Oct 20)
1. **`VeilLaunch.sol` on the Elysium testnet (chain 99801):**
   - `createLaunch`, `commit`, `reveal`, `settle`, `claim` and `refund`.
   - Auto-seeding of the AMM pool and locking of the LP tokens.
   - Foundry tests.
2. **Web app, three screens:** create a launch, place a hidden bid, view results and claim.
3. **Demo:** a normal launch sniped in block 1, side by side with a Veil launch. Video under 3 minutes.

## 9. Risks and open questions
- **Rules:** Ascend's rules, eligibility and "real team" requirement are still unknown. Read their Discord first.
- **Time:** the build clashes with Chogathon (due Oct 23). Split it Fri–Mon for Veil, Tue–Thu for Chogathon.
- **Privacy limits:** deposits and timing are public. Fixed deposit sizes help but don't hide everything. State this clearly in the pitch.
- **Which AMM:** which AMM on the Elysium testnet do we seed? Options include Dex Da Costa, a Uniswap V3 fork through Chainzy, or our own pool.
- **HIP-6:** if it ships, Veil OTC overlaps with it. Veil Launch doesn't.
