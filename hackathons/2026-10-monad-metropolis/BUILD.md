# Monad Metropolis — BUILD.md

**Written:** 2026-10-07 · **Deadline:** 13 Oct 2026 (submit on **12 Oct**, keep the 13th as buffer) · **Working name:** `Veil` (placeholder; rename before the domain is fixed, see §9 Day 0)

This is the build plan for a **self-custodial private payments layer on Monad**. One shielded core powers three products:
1. Private agent payments over x402.
2. Private payroll.
3. Private payment streams from founders to KOLs. This is our own addition, and it absorbs idea 001.

Every sponsor integration below was chosen because the product needs it, not as decoration. Read §0 and §2 first.

---

## 0. Decisions at a glance

| Decision | Choice | Why |
|---|---|---|
| Track | **04 Trust, Identity & AI Infra** (alternative: 02) | Their "best fit" is "cryptography, protocol design, agent frameworks". We're a ZK pool plus agent payments, using passkey accounts (Mera) and ERC-8004, both named in the track. Track 02 also fits (payroll, streams), but it's the most crowded track. If the portal already has a track locked, check whether it can be changed |
| Privacy core | **Our own key-owned UTXO pool**, with proofs generated on the user's device (Groth16, circom). **One pool contract per asset** | Our edge over what's already on Monad (§2): no operator ever sees anything. Separate pools per asset remove the bug class behind Gloam's worst finding (H1 cross-asset drain) |
| Circuit | **One circuit**: 2 notes in, 2 notes out. A signed `publicAmount` covers deposits, private transfers and withdrawals | One circuit, one verifier and one trusted setup to get right in 6 days |
| Plan B | If the core isn't green end-to-end on testnet by **end of 8 Oct**, switch the privacy core to the **Unlink SDK on `monad-testnet`** and keep every product on top | Protects the deadline. We lose the "no operator" edge, so this is a fallback, not the plan |
| Onboarding | **Mera** passkeys as the only wallet layer. No Privy or Dynamic | Mera is Monad's own tool, and "One Passkey, Many Keys" fits our key tree exactly (§5.1). Mixing wallet SDKs weakens every one of those bounties |
| Assets | **USDC** first, then **AUSD**. A CVA token pool only if Cleanverse gives us one | USDC has x402 and Aurora support. AUSD is the largest stablecoin on Monad and the target of Agora's $10k bounty |
| Networks | Build on **testnet (10143)**. Ship a **capped mainnet (143)** deployment on day 5 | MetaMask Agent Wallet writes work reliably only on mainnet (§5.2). Being live on mainnet with caps also beats Unlink's gated mainnet |
| Gloam | **Reference only.** We read how they did things on other chains. **No copied code.** Credit it in the README as design inspiration | New-work rule plus honesty. We already have read access to the public repo (`/home/user/cryptoduke01/gloam`), so you don't need to download it |

**Bounties we go for:**
- **Core:** Mera ×2, MetaMask Agent Wallet Plugin, Envio, Agora Cross-Border, Chainlink CRE. That's **$21.5k**.
- **Add if on schedule:** Cleanverse ($2k), Aurora ($5k).
- **Optional:** Nansen ($5k).
- **Skip:** Privy and Dynamic (they conflict with Mera), Kuru, Perpl, Community.

---

## 1. What we're building

> **Pay people and agents on Monad without publishing your payroll, your marketing budget or your agent's spending history. Only the payer and payee see the amount. You can prove any payment to anyone you choose.**

| Surface | User | What they do |
|---|---|---|
| **Web app** (Next.js) | Founders, finance teams, KOLs | Passkey sign-in (Mera). Deposit USDC or AUSD (or fund from any chain via Aurora). Private send, payroll from a CSV, campaigns that pay KOLs per verified impression, withdraw, share a receipt |
| **MetaMask Agent Wallet plugin** (`mm veil …`) | AI agents and their owners | An agent pays other agents and paid APIs privately, within caps its owner sets |
| **x402 `shielded` scheme + facilitator** | API sellers and agent buyers | A paid API accepts private payments next to the standard public `exact` scheme |
| **Campaign / stream vault + CRE workflow** | Founders → KOLs | The budget streams to KOLs as private notes, per verified X impression (or per second for salaries) |

The demo moments judges remember:
1. An agent buys an API call. The explorer shows a shielded transaction and nothing else. Settled in about 1–2 s.
2. Payroll for 5 people in Lagos and Nairobi paid in AUSD, with no amounts on-chain.
3. A KOL's private balance climbs while their post's impressions climb. The project's treasury never appears anywhere.

---

## 2. Positioning: what Monad already has, and our angle

| | How it works | Who sees your payments | Status on Monad | Gap we fill |
|---|---|---|---|---|
| **Unlink** | ZK notes, but **its engine generates the proofs on its own servers and keeps users' viewing and nullifier keys** ("the Engine retains them to decrypt note memos") | The Unlink engine (operator) | Mainnet needs an **access grant**. Open on testnet | No operator at all. Proofs are made on the user's device |
| **TACEO Merces** | MPC nodes plus collaborative ZK | The MPC network. Compliance attestation required | Mainnet "limited access", private USDC with caps | Permissionless and self-custodial |
| **Category Labs** | "Privacy is coming". Teaser on 6 Oct, aimed at institutions | Unknown | Not launched | Built for people and agents now, not institutions later |
| **Gloam** (other chains) | Bearer-secret notes, 1 note in and 2 out, separate circuits for shield, transfer and unshield | Nobody | Not on Monad | Our own design for Monad: key-owned notes, merging notes, proof-bound relaying, streams |

**Pitch line:** *"Unlink and Merces bring privacy to institutions through an operator. Veil gives it to people and their agents directly: proofs made on your own device, nothing for anyone to see, settled in one Monad block."*

**What we never claim:** "audited", "production-ready", or "untraceable". Deposit and withdrawal amounts are public, and so is timing. Say so (§6).

---

## 3. Rules we build under

1. **New-work rule.** Use a fresh public repo (`veil-monad`) with every commit made from 7 Oct on. The README has a "Prior art and dependencies" section that names Gloam (design reference, MIT), Tornado Nova (the 2-in/2-out design), circomlib, snarkjs, `poseidon-solidity`, `@category-labs/mera`, x402 and the CRE SDK.
2. **No copied Gloam code.** Read Gloam for how it handled each chain's quirks (§7). Write our own code. When a Gloam lesson shapes a decision, cite the Gloam doc in our design notes. That shows the work is our own.
3. **Honesty.** Disclose the dev trusted setup, testnet status, mainnet caps and the privacy limits in the README and the write-up. Never show a fake private success.
4. **KOL streams pay only for disclosed ads.** The CRE workflow checks that the post contains the sponsor disclosure (`#ad` or the platform's paid-partnership label) and tags the project before paying anything. We make payment private, not sponsorship.

---

## 4. Architecture

```
                         ┌──────────────── Mera passkey (one passkey → HD key tree) ─────────────────┐
                         │ m/…/0 public EOA (gas, deposits) · m/…/1 shielded spend key · m/…/2 view+enc key │
                         │ m/…/10+i agent sub-accounts · m/…/100+j campaign admin keys                     │
                         └────────────────────────────────────────────────────────────────────────────┘
   Web app (Next.js)            mm plugin (`mm veil …`)            Paid API (x402 seller)
        │  proves in browser          │ proves in Node                 │ 402 → accepts [shielded, exact]
        ▼                             ▼                                ▼
   ┌────────────────────── @veil/sdk (TS): keys · notes · prover · encrypt · tree sync · tx build ──────┐
   └─────────────────────────────────────────────┬──────────────────────────────────────────────────────┘
                                                 │ proof + extData (recipient, relayer, fee, encrypted outputs bound in proof)
                                                 ▼
                     Relayer / x402 facilitator (Hono)  ── screens (OFAC list, Nansen opt.) ── pays gas in MON
                                                 │
   Monad ─────────────────────────────────────────▼──────────────────────────────────────────────────────
   VeilPool[USDC] · VeilPool[AUSD] · (VeilPool[CVA])      ← Groth16 verifier (2-in/2-out), Poseidon tree depth 20
        ▲ depositTo(pubKey, amount) (on-chain commitment, no proof)
   StreamVault (per campaign clone) ◄── CRE KeystoneForwarder.onReport(postId, impressions) ◄── CRE workflow (X API)
   ERC-8004 Identity/Reputation (agents + merchants)       Cleanverse CVI adapter (deposit/withdraw gate on CVA pool)
        │ events
        ▼
   Envio HyperIndex (GraphQL): commitments + encrypted outputs + nullifiers + campaigns → tree sync, note discovery, dashboards
   Aurora Intents (confidential swap) ── fund from any chain → USDC on Monad → shield
```

---

## 5. Sponsor integrations, in depth

Each subsection covers why the sponsor is core to the product, what we build, the demo moment and the effort. Bounty text sits behind the portal login. **Read every one in the portal on Day 0** and adjust here.

### 5.1 Mera: "Best Mera-Powered UX" + "One Passkey, Many Keys" ($2.5k + $2.5k) · **Core**

**Facts:**
- Package: `@category-labs/mera`.
- `createPasskeyWithPrfOutput()` / `getPasskeyPrfOutput()` produce 32 bytes. These become a BIP-39 mnemonic, then a seed, then keys via `deriveEvmKey()` on path `m/44'/60'/0'/0/{index}`.
- `createSecp256k1SigningSession()` → `toViemAccount()`.
- Requires the WebAuthn **PRF** extension. Works with iCloud Keychain, 1Password and Google Password Manager. On desktop Chrome, only Google Password Manager passkeys work; locally saved Chrome passkeys throw `PRF_UNAVAILABLE`.
- **The passkey is tied to the `rpId` (domain).** Change the domain and every user loses their account.

**Why it's core:** a private wallet has more keys than a normal one. One passkey gives the whole key tree:

| Index | Key | Used for |
|---|---|---|
| 0 | Public EOA (secp256k1) | Gas, the public side of deposits and withdrawals, ERC-8004 identity |
| 1 | **Shielded spend key** → `spendPriv = H(child₁) mod p`, `pubKey = Poseidon(spendPriv)` | Owning and spending notes |
| 2 | **View and encryption key** (x25519 from `child₂`) | Decrypting incoming notes. **Shareable with an auditor** without giving away spending power |
| 3 | **At-rest key** (AES-GCM from `child₃`) | Encrypting the local note store, which fixes Gloam's audit finding M-1 (secrets stored in plaintext localStorage) |
| 10 + i | **Agent sub-accounts** | Each agent gets its own shielded balance and caps. Revoke an agent without touching the main balance |
| 100 + j | **Campaign admin keys** | One fresh key per KOL campaign, so campaigns can't be linked to each other or to the treasury |

**Demo moment:** Face ID once → an "Accounts" panel shows the main balance, a view key shared with the accountant, two agent accounts and three campaigns, all from one passkey. Then restore on a phone with the same passkey and everything is back.

**Effort:** 0.5 day. **Risks:**
- The PRF limit on desktop Chrome, so demo on Safari or iOS.
- Fix the production domain before any real passkey is created.

### 5.2 MetaMask: "Best Agent Wallet Plugin" ($2.5k) · **Core**

**Facts** (from `docs.metamask.io/llms-agent-wallet-full.txt` and existing Metropolis entries):
- **Packaging:**
  - A plugin is an npm package with the `oclif-plugin` keyword and an `@metamask/agent-wallet` **peer** dependency.
  - Its `mm` manifest block declares `schemaVersion: 1`, `minCliVersion`, and `commands[]` with `capabilities` (`wallet-read`, `wallet-submit`), `dataAccess` and `targetChains`.
  - Start from the template at `github.com/MetaMask/agent-wallet-plugin-template`.
- **Writing commands:**
  - Commands extend `PluginCommand` and implement only `execute(io)`.
  - `ctx.walletExecutor(io, id)` handles transactions, message signing and typed-data signing, all **policy-gated by MetaMask** (simulation, Blockaid, Guard Mode allowlists, rolling 24-hour outflow limit, 2FA).
  - `ctx.publicClient(chainId)` does reads.
  - Plugins run in-process and unsandboxed. The session, token and mnemonic are never exposed.
- **Chains:**
  - Monad `143` is covered.
  - **Testnet writes fail** with "Invalid chainId" through MetaMask's RPC proxy (MonAgent's report). The Perpl plugin works around it by declaring the chain in `~/.metamask/wallets.json` → `data.customEvmChains`.
- **x402:** the built-in helper only supports public `exact` / EIP-3009.
- **Competition:**
  - MonAgent already covers public x402 payments and ERC-8004.
  - The Perpl plugin introduced the "enrolled key + plugin's own guard" pattern.
  - **No one has done private payments.**

**What we build (`@veil/mm-plugin`):**

| Command | Capability | What it does |
|---|---|---|
| `mm veil setup` | `wallet-submit` (typed-data) | Enrolls a shielded key for this agent. It derives from an EIP-712 signature if signatures turn out deterministic (**test on Day 3**). Otherwise it generates the key locally and encrypts it at rest. Prints a `veil1…` address |
| `mm veil deposit --amount --asset` | `wallet-submit` | Approve, then `transact` with a deposit proof, both through MetaMask's executor, so MetaMask's policy and simulation cover money **entering** the pool |
| `mm veil balance` / `history` | `wallet-read` | Reads from the Envio index, decrypts with the view key |
| `mm veil pay --to veil1… --amount` | none (relayed) | Generates the proof locally and submits through the relayer, so the agent's wallet never appears |
| `mm veil x402 fetch <url> --max` | none | Pays a 402 endpoint with the `shielded` scheme, falling back to `exact` only if allowed |
| `mm veil guard set/get` | none | **The plugin's own caps**: per-payment, rolling 24 h, payee allowlist, expiry. Required because relayed private spends bypass MetaMask's outflow policy. Say so explicitly in the README (the Perpl plugin did the same) |
| `mm veil withdraw --to 0x…` | none | Relayed. The recipient is bound inside the proof |
| `mm veil receipt <tx>` | none | Prints a disclosure the payee or an auditor can verify (§6.5) |

Also ship `skills/veil-payments/SKILL.md` so Claude Code, Codex and others drive it safely: read first, confirm writes, never retry blindly, stop on `[AWAITING_MFA]`.

**Demo moment:** a Claude Code agent with `mm` buys three API calls. MetaMask shows the one-time deposit under Guard Mode. The explorer shows three shielded pool transactions and none from the agent's address. `mm veil guard get` shows the remaining daily cap.

**Effort:** 1 day. **Risks:**
- Plugins are beta. Pin `@metamask/agent-wallet@7`.
- Symlink the host's `@metamask/agent-wallet` into `node_modules`, or the consent hook fails. The Perpl plugin README documents this.

### 5.3 x402 and Monad's facilitator (no bounty; Monad's own priority) · **Core**

**Facts:**
- Facilitator: `https://x402-facilitator.molandak.org` (`/supported`, `/verify`, `/settle`). It **pays gas** and supports mainnet and testnet.
- Use `@x402/evm >= 2.22.0`.
- Monad USDC uses the EIP-712 domain `name: "USDC"`, `version: "2"`.
- USDC addresses: mainnet `0x754704Bc059F8C67012fEd69BC8A327a5aafb603`, testnet `0x534b2f3A21130d7a60830c2Df862319e593943A3`.
- Schemes: `exact` (EIP-3009) and `upto` (Permit2).

**What we build:** a custom x402 v2 scheme named **`shielded`** on `eip155:143` / `eip155:10143`.
1. The server's 402 response lists `accepts: [{scheme:"shielded", payTo:"veil1…", asset, amount}, {scheme:"exact", …Monad facilitator…}]`.
2. The client builds a 2-in/2-out transfer to `payTo`. The payment output is **encrypted to the payee's view key**. The relayer fee is bound in `extData`.
3. The client retries with `PAYMENT-SIGNATURE` = `{proof, publicInputs, extData}`.
4. **Our facilitator** checks, in under 50 ms:
   - The proof verifies (snarkjs).
   - The root is known.
   - The nullifiers are unspent.
   - `extDataHash` matches.
   - It decrypts the output with the merchant's view key, which the merchant runs itself or delegates, and checks the amount and asset.
   It then submits `transact` and waits for receipt (~0.6 s finality).
5. The server returns 200.
6. **No sweep step is needed**, unlike Gloam's design. Notes belong to the payee's key, so the payer can't spend them back.

Merchants that receive public `exact` payments can opt into **auto-shield**: the facilitator calls `depositTo(merchantPubKey, amount)` (§6.2), so revenue still becomes private.

**Demo moment:** run `curl` against the paid API → 402 → pay → 200, under 2 s, with no amount shown on the explorer. **Effort:** 0.75 day, shared with the relayer.

### 5.4 Envio: "Best Use of Envio" ($1k) · **Core**

**Facts:** HyperIndex supports Monad mainnet and testnet (HyperSync `https://monad-testnet.hypersync.xyz`). It runs event handlers and serves a GraphQL API, with hosted deploys.

**Why it's core, not decoration:**
- Monad's public RPCs cap `eth_getLogs` at **100 blocks** (QuickNode and the Foundation's RPC) or 1,000 blocks (Alchemy, Ankr), with blocks every 300 ms.
- A wallet has to rebuild the Merkle tree from **every** commitment and trial-decrypt **every** encrypted output to find its notes. Over raw RPC that means thousands of calls. Gloam needed its own server endpoint for this (`/api/vault-leaves`). **Envio is our sync layer.**

**What we build:**
- Entities: `Commitment{index, value, encryptedOutput, pool, block}`, `Nullifier{value}`, `Pool{root, nextIndex, tvl}`, `Campaign{…}`, `StreamPayout{campaign, postId, amount}` (amounts public by design, §5.6), `RelayStat{…}`.
- The SDK syncs from GraphQL, then **checks the rebuilt root against the on-chain `isKnownRoot`** (never trust the indexer blindly), falling back to RPC.
- The transparency page and the campaign and KOL dashboards also read from Envio.

**Effort:** 0.5 day.

### 5.5 Agora: "Best Cross-Border Payments App" ($10k) · **Core**

**Facts:**
- AUSD on Monad: `0x00000000eFE302BEAA2b3e6e1b18d08D69a9012a`, **6 decimals**.
- It's an omnichain token (LayerZero OFT), with the same address on Ethereum.
- **The issuer can mint, burn, pause and freeze, and there's no timelock** (Aave risk assessment).
- It's the largest stablecoin on Monad.

**Why it's core:**
- Cross-border payroll and creator payouts are exactly where privacy matters. Today a Lagos contractor paid on-chain has their income and employer published.
- AUSD is the **default unit** in the payroll and campaign screens, not one option among several.

**What we build:**
- A dedicated `VeilPool[AUSD]`.
- Payroll: CSV upload, then a sequence of 2-in/2-out transfers in AUSD. Each run produces change notes for the next. With 300 ms blocks, 10 payees take about 15–25 s including proving.
- Payees without a Veil address get a **claim link**: the note is encrypted to a one-time key carried in the URL fragment.
- KOL campaigns are priced in AUSD.
- x402 merchants can price in AUSD via the `shielded` scheme (EIP-3009 isn't needed, so AUSD works where `exact` might not).

**Freeze risk:** if the issuer freezes the pool contract, every AUSD note is stuck. Gloam documented the same unfixable issue as F-2. Disclose it, keep caps, and keep USDC as a separate pool so one freeze can't touch the other.

**Effort:** 0.5 day on top of the core. **Open:**
- Read the bounty text.
- Agora's Stablecoin API (mint/redeem to bank) needs a demo booking. Ask on Day 0, but don't depend on it.

### 5.6 Chainlink CRE: "Best workflow with CRE" ($3k) · **Core (KOL streams)**

**Facts:**
- TypeScript SDK `@chainlink/cre-sdk`. Monad testnet needs CLI v1.30.0+ and SDK v1.19.0+.
- Simulation is open to everyone. **Deploying to the live network needs Early Access** (`cre account access` or app.chain.link/cre/request-access).
- `cre workflow simulate --broadcast` writes on-chain through a **MockKeystoneForwarder**.
- The consumer contract implements `IReceiver.onReport` (use `ReceiverTemplate`).

| Forwarder | Monad testnet | Monad mainnet |
|---|---|---|
| Simulation (`MockKeystoneForwarder`) | `0xB9F79d863261869B234c481D1f9A7af84AeAd192` | `0x9eF6468C5f37b976E57d52054c693269479A784d` |
| Production (`KeystoneForwarder`) | `0xF8344CFd5c43616a4366C34E3EEE75af79a74482` | `0x76c9cf548b4179F8901cda1f8623568b58215E62` |

**Why it's core:** CRE decides who gets paid. Several independent nodes fetch the post's numbers and agree on them before any money moves, so no server of ours sets a KOL's pay.

**The workflow** (cron, every 10 min):
1. Read active campaign posts from `StreamVault` (EVM read).
2. For each post, call `GET /2/tweets?ids=…&tweet.fields=public_metrics,text,author_id` on the X API. The bearer token is a CRE secret.
3. Nodes agree on the **median** `impression_count`.
4. Validate: the `author_id` matches the registered KOL, and the text contains `#ad` plus the project tag.
5. Encode `(campaign, postId, impressions, disclosedOk)` and write through the forwarder.
6. `StreamVault._processReport` handles the rest:
   - Pays only the increase (`max(0, new − last)`) × rate, capped per post and per campaign.
   - Splits 80% paid now and 20% held back until the minimum post lifetime.
   - Pays by calling `pool.depositTo(kolPubKey, amount, blinding, encOut)`.

**Demo:** the simulation with `--broadcast` against testnet is enough to show it working. Also apply for Early Access on Day 0. If it's granted, deploy and show the production forwarder.

**Effort:** 1 day (vault plus workflow). **Risks:**
- X API cost and how fresh impression counts are (impressions update with a lag; say so).
- How the bounty treats simulation versus deployment. Read the bounty text.

### 5.7 Cleanverse: "Best Integration of CVI/CVA" ($2k) · **Add if on schedule**

**Facts:**
- CVI is an A-Pass identity credential bound to a wallet. CVA is a verified "A-Token" stablecoin.
- Their own hackathon awarded **30 of 100 points for integration depth** — "whether verification is enforced where value actually moves".
- Developer docs aren't public. Previous Monad entries (TrustFlow, SpendClear) coded against an `ICVI` / attestation-oracle interface with a mock, plus an adapter for Cleanverse's signed attestations.

**What we build:** a **verified pool mode**.
- `VeilPool[CVA]`, or a `verifiedOnly` flag on any pool, checks `cvi.isVerified(depositor)` on deposit and `cvi.isVerified(recipient)` on withdrawal. Every coin in the pool therefore came from a verified identity, and that is the anonymity set.
- This is the "compliant privacy" story without an operator. The rules apply where tokens enter and leave the pool, and payments inside stay private.
- Use a mock CVI on testnet and an adapter for real Cleanverse attestations.

**Day 0:** ask Cleanverse (Discord or the portal) for sandbox access and the CVA token address on Monad. **Effort:** 0.5 day.

### 5.8 Aurora Intents: "Bring Any-Chain Liquidity to Monad" ($5k) · **Add if on schedule**

**Facts:**
- The Swap API is `POST https://intents-api.aurora.dev/api/quote/{apiKey}`. Keys are self-serve from Intents Studio.
- **Confidential Intents** is a single flag on the quote request. It hides the origin wallet and the route, but **settlement on the destination chain stays public**.
- The widget supports `confidentialMode: public | confidential | user-choice`.
- Monad tokens on the route: MON, **USDC**, USDT0 `0xe7cd86e13ac4309349f30b3435a9d337750fc82d`. **No AUSD**.
- Persistent deposit addresses need Aurora's approval, so don't depend on them.
- Integrator fee: 60% to us, 40% to Aurora.

**Why it fits:** "fund your private balance from any chain without linking your old wallet."
1. A confidential swap brings USDC from Base, Solana, Tron or elsewhere to the user's Mera EOA on Monad, so the origin is hidden.
2. The app shields it straight away, so the destination is hidden too.
3. Result: a private path from start to finish across chains.
4. To get AUSD, users swap USDC → AUSD inside our app later (optional via Kuru Flow).

**Effort:** 0.5 day.

### 5.9 Nansen: "Best use of Nansen" ($5k) · **Optional**

**Facts:**
- Pay per call via x402 in **USDC on Monad**, with no API key.
- `/api/v1/profiler/address/related-wallets` costs $0.01 and `/counterparties` costs $0.05.
- **Label endpoints aren't available over x402.** Rate limit: 5 requests/s.

**Possible use:**
- The relayer screens the depositor (from the app) and every withdrawal recipient with `counterparties`. It refuses if the wallet's counterparties include flagged entities.
- Pay for those calls with x402 on Monad from the relayer's own wallet.

**Caveat:** this is an off-chain policy, not enforced by the contract. **Only build it if everything else is green.**

### 5.10 Not pursuing

- **Privy / Dynamic:** they conflict with Mera (pick one wallet layer).
- **Kuru / Perpl:** no honest fit while private trading is out of scope (Gloam's H1 shows private swaps break solvency).
- **Community:** we're a solo team.
- **AI credits:** irrelevant.

**ERC-8004** has no bounty, but register the merchant API and the demo agents for free alignment with Track 04:
- Identity Registry `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- Reputation Registry `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`

---

## 6. Protocol specification (what we write ourselves)

### 6.1 Keys, notes, addresses

```
spendPriv        = H("veil-spend", child₁) mod p          // p = BN254 scalar field
pubKey           = Poseidon(spendPriv)
commitment       = Poseidon(amount, pubKey, blinding)     // one pool per asset → asset not in the note
signature        = Poseidon(spendPriv, commitment, leafIndex)
nullifier        = Poseidon(commitment, leafIndex, signature)
veil address     = bech32m("veil", pubKey ‖ x25519EncPub)
encryptedOutput  = x25519-XSalsa20-Poly1305(encPub_recipient, {amount, blinding})  // AEAD, so a fake memo can't be forged
```

### 6.2 Circuit `transaction2x2.circom` (depth 20)

- **Public inputs (7):** `root, publicAmount, extDataHash, inNullifier[2], outCommitment[2]`.
- **Constraints:**
  1. For each input: `pubKey = Poseidon(privKey)`, the commitment opens, the nullifier is derived as above, and the Merkle path checks against `root` **when amount ≠ 0** (dummy inputs skip the path check).
  2. For each output: the commitment opens and `Num2Bits(128)` holds on the amount.
  3. `inNullifier[0] != inNullifier[1]`.
  4. `Σin + publicAmount == Σout` in the field.
  5. `extDataHash` is a public input that's only "used", meaning it's bound by being squared into a dummy constraint.
- **Trusted setup:**
  - Hermez `powersOfTau28_hez_final_16.ptau`, then a phase-2 setup with 2–3 contributions and a beacon.
  - Commit the zkey hashes. Label it a **dev ceremony**.

### 6.3 `VeilPool.sol` (one per ERC-20)

- **`transact(Proof, ExtData)`**, where `ExtData = {recipient, extAmount (int256), relayer, fee, encOut1, encOut2}`:
  - Require `isKnownRoot(root)` (**permanent** root history, so proofs made before a busy block still land).
  - Require both nullifiers unspent and `extDataHash == keccak(abi.encode(extData)) % p`.
  - Require `publicAmount == (extAmount − fee) mod p`, the proof verifying, and `|extAmount| ≤ cap`.
  - Effects first: mark nullifiers spent, insert both commitments, emit `NewCommitment(commitment, index, encOut)` ×2 and `NewNullifier` ×2.
  - Interactions last:
    - If `extAmount > 0`: `transferFrom(msg.sender)`.
    - If `extAmount < 0`: `transfer(recipient)`.
    - If `fee > 0`: `transfer(relayer)`.
  - Use SafeERC20 and `nonReentrant`.
- **`depositTo(pubKey, amount, blinding, encOut)`** (no proof; used by `StreamVault`, auto-shield and payouts):
  - The contract **computes** `commitment = Poseidon(amount, pubKey, blinding)` on-chain, so the amount is bound and Gloam's C1 bug can't happen.
  - Then `transferFrom(msg.sender)`.
  - Trade-off: it reveals that this pubKey received this amount. Spends stay unlinkable, because nullifiers need `spendPriv`. Use per-campaign or one-time pubKeys.
- **Merkle tree:** incremental Poseidon tree (`poseidon-solidity` `PoseidonT3`), with precomputed zero values.
- **Admin:**
  - Owner can **pause deposits only** and **lower** caps. No function moves pool funds. Verifier immutable.
  - Ownership is two-step.
  - Gloam's M-4 lesson: no reversible protections and no `emergencyWithdraw` pretending to be a backstop.
- **Gas on Monad:**
  - Monad charges 5× Ethereum's gas for pairing checks, so one verify is about 0.9M gas for pairings plus about 0.2M for the scalar multiplications on 7 public inputs.
  - Add about 0.45M for two tree inserts. Budget about 1.8M per `transact`.
  - **Monad charges the gas limit you set, not the gas used.** Estimate, then add 15%. Never hardcode 5M.

### 6.4 Relayer and x402 facilitator (one Hono service)

- **Endpoints:**
  - `POST /relay` takes `{proof, extData}`. Same checks as the contract, plus `eth_call` dry-run, then send.
  - `POST /x402/verify` and `POST /x402/settle` implement the `shielded` scheme.
  - `GET /status`.
- **Rules:**
  - The relayer can only submit or refuse. The recipient and fee are bound in the proof.
  - Screening: an OFAC list snapshot on withdrawal recipients, optionally Nansen.
  - Rate limits per IP and per merchant.
  - **The relayer never holds keys or notes.**
- **Meta-transactions:** for campaign admin actions, so a campaign key never needs MON and can't be linked by its gas funding.

### 6.5 Disclosure (no extra circuit)

- **Receipt:** reveal one note's `{amount, pubKey, blinding, leafIndex}`. The verifier recomputes the commitment, finds it at `leafIndex` via Envio, and checks the on-chain root. This proves "X paid Y this amount" and nothing else.
- **Auditor view:** share the index-2 view key, which decrypts everything incoming and nothing spendable.
- **Stretch:** proof of funds ≥ X needs a new circuit. Skip it.

### 6.6 `StreamVault` (one clone per campaign, made by a factory)

- **Funding:** the project withdraws from its shielded balance **to the vault address** via the relayer. Its treasury never appears.
- **Meters:**
  - `ImpressionMeter`: CRE `onReport`, §5.6.
  - `TimeMeter`: `drip()`, callable by anyone, pays `elapsed × ratePerSecond` for salaries and subscriptions (Track 02's per-second example).
- **Payouts:** `pool.depositTo(kolPubKey, amount, blinding = Poseidon(campaign, postId, epoch), encOut)`.
- **Holdback:** released after the minimum post lifetime, or refunded to the project's pubKey if the post is deleted.
- **Caps:** per post, per KOL and per campaign. Unspent budget goes back to the project's shielded address.
- **Visibility:** the rate and per-post payouts are **public by design**, since CRE math runs on-chain. The KOL's wallet, their combined earnings across campaigns, and where they cash out stay private. Say this plainly in the write-up.

---

## 7. Lessons from Gloam (read before writing code)

Each source is a Gloam doc in `/home/user/cryptoduke01/gloam`. "Test" is the test that proves we avoided the problem.

| Gloam problem | Source | What we do | Test |
|---|---|---|---|
| **H-P1 / C1**: `shield()` accepted a client-made commitment, so an attacker could fake a big note and drain the pool | `contracts/audit/GLOAM-BUG-REPORT.md` | No unproven commitments, ever. Deposits go through the circuit (`publicAmount`) or `depositTo`, which computes the commitment on-chain | Forge: a deposit with mismatched `extAmount` / `publicAmount` reverts. A fuzz test shows `depositTo` commitments always equal Poseidon(amount, …) |
| **H1**: cross-asset private swaps broke per-asset solvency | `contracts/audit/H1-SWAP-SOLVENCY.md` | One pool per asset. No in-pool swaps | Invariant test: `token.balanceOf(pool) ≥ Σ unspent note amounts` |
| **F-1**: a decimals mismatch in rate math | `contracts/audit/REMEDIATION.md` | Single-asset pools. Campaign rates in the token's own units. USDC and AUSD both have 6 decimals | Unit tests at 6 decimals with boundary amounts |
| **F-2**: an issuer freezing the pool freezes every note | `contracts/audit/TEMPO-COMPLIANCE-DESIGN.md` | Separate USDC and AUSD pools, caps, disclosure. Never claim `emergencyWithdraw` saves you | Documented in the README |
| **Field overflow** (Kensho C2) | `contracts/circuits/transfer/transfer.circom` | `Num2Bits(128)` on every amount | Circuit test: an amount of `p−1` fails to prove |
| **Public-input order drift** between circuit and contract | Kensho second pass | One source of truth for input order, plus a parity test | CI: a proof made in TS verifies in Forge (ffi or a fixture), and a single-field tamper fails |
| **Merkle zeros mismatch** | Kensho second pass | Generate the zeros from circomlibjs into Solidity constants with a script | Test: TS root == Solidity root after 1, 2 and 1,000 inserts |
| **Relayer can redirect funds** | `packages/sdk/src/relay.ts` (they bound the recipient) | `extDataHash` binds recipient, relayer, fee and both encrypted outputs | Forge: changing any extData field reverts |
| **Bearer secrets let the payer spend back** (forced the x402 "sweep") | `packages/sdk/src/x402.ts` | Key-owned notes: a nullifier needs `spendPriv` | SDK test: the payer can't build a valid spend of the payee's note |
| **M-1**: plaintext note secrets in localStorage | `GLOAM-BUG-REPORT.md` | AES-GCM under the Mera-derived at-rest key (index 3) | Manual check: localStorage holds only ciphertext |
| **L-1**: the memo event revealed the sender | `GLOAM-BUG-REPORT.md` | Encrypted outputs go out in the pool event, from the relayer's `msg.sender` | Look at the event in the explorer |
| **Tempo gas**: hardcoded limits broke | Gloam commit "Tempo: let the wallet estimate gas" | Estimate, +15%. Monad charges the full limit | Run on testnet with the receipt's `gasUsed` logged |
| **Slow tree sync** | Gloam `app/src/lib/treeSync.ts` + `/api/vault-leaves` | Envio, plus a root check, plus RPC fallback in 100-block chunks | Kill Envio → the app still syncs (slowly) |
| **Mixed hash schemes / stale pools in the UI** | `contracts/ARCHITECTURE.md` ("App must not default to them") | One registry file per network. Old deploys removed from the app | — |

**How to use Gloam during the build:**
- Before writing each module, read the matching Gloam file: `networks.ts` → our network registry, `treeSync.ts`, `relay.ts`, the payroll components.
- Note its chain-specific handling in a comment like `// cf. gloam: <file> — we differ because …`.
- Then write ours.

---

## 8. Repo layout (`veil-monad`, fresh, public)

```
veil-monad/
  circuits/            transaction2x2.circom, keypair, merkle; scripts/setup.sh (ptau → zkey → verifier.sol); test/
  contracts/           Foundry: VeilPool, Verifier, PoseidonT3/T4 (poseidon-solidity), StreamVault(+Factory), CviAdapter, mocks; test/ (unit, fuzz, invariant)
  packages/sdk/        @veil/sdk — keys (Mera tree), note, encrypt, prover (snarkjs, browser+node), tree (Envio+RPC), tx builder, x402 scheme
  packages/mm-plugin/  @veil/mm-plugin — `mm veil …` + skills/veil-payments/SKILL.md
  services/relayer/    Hono — /relay, /x402/{verify,settle}, screening, meta-tx
  services/cre/        CRE TS workflow — impressions → StreamVault.onReport
  indexer/             Envio HyperIndex config + handlers
  apps/web/            Next.js — onboarding (Mera), wallet, payroll, campaigns, KOL view, verify page, transparency
  apps/demo-api/       paid API (x402: shielded + exact)
  docs/                PRIVACY-MODEL.md, THREAT-MODEL.md, PRIOR-ART.md
```

---

## 9. Day-by-day plan

**Calendar clash:** BNB Hack (11 Oct, 12:00 UTC) and Colosseum World's Fair (12 Oct) are also marked 🎯 in `TIMELINE.md`. This plan needs about 5 full days. **Decide today which of the three gets dropped or reduced.** Otherwise all three will be weak.

| Day | Date | Build | Done when |
|---|---|---|---|
| **0** | **7 Oct (today)** | Read every bounty's text in the portal. **Fix the name and domain (Mera rpId)**. Create the repo. Request access: CRE Early Access, Aurora API key, Cleanverse sandbox, Envio account, X API token, Agora demo. Write the circuit, run the trusted setup | Circuit compiles. A proof is made and verified in TS |
| **1** | 8 Oct | `VeilPool` + verifier + Poseidon. Forge tests from §7 (C1, double spend, extData tamper, overflow, parity, zeros, reentrancy, invariant). Deploy to **testnet**. SDK: keys, notes, encryption, transact builder. End-to-end in Node: deposit → transfer → withdraw | **Plan B gate**: e2e green on testnet by end of day, or switch to Unlink |
| **2** | 9 Oct | Envio indexer (hosted). Relayer `/relay`. Web app: Mera onboarding + key tree panel, deposit, balance, private send, withdraw, receipt and verify page | A judge can sign in with Face ID and send privately on testnet |
| **3** | 10 Oct | x402 `shielded` scheme + facilitator + demo paid API. **mm plugin** (setup/deposit/pay/x402/guard/withdraw/receipt) + SKILL.md. Test `mm` writes (mainnet, or testnet via `customEvmChains`). Check whether typed-data signatures are deterministic | An agent pays the API privately through `mm veil x402 fetch` |
| **4** | 11 Oct | Payroll (CSV, AUSD pool, claim links). `StreamVault` + factory + TimeMeter. CRE workflow simulated with `--broadcast` into the vault. KOL dashboard. Cleanverse verified mode (mock + adapter) | A KOL's balance increases from a CRE report on testnet |
| **5** | 12 Oct | **Mainnet**: deploy USDC + AUSD pools with caps (e.g. $100 per transaction, $5k TVL) and the relayer. Aurora fund-from-any-chain (if green). Register in ERC-8004. README, PRIVACY-MODEL, prior art. **Demo video**. Write-up. **Submit** | Submitted, with links working in a private browser window |
| — | 13 Oct | Buffer only. No new features | — |

**What to cut, in order, if behind:**
1. Nansen.
2. Aurora.
3. TimeMeter.
4. Cleanverse.
5. Mainnet (stay on testnet, but the `mm` demo then needs `customEvmChains`).
6. Payroll claim links.

**Never cut:** the Forge tests in §7, Envio sync, and the mm plugin guard.

---

## 10. Checks before every push to main

- `forge test` (unit + fuzz + invariant), the circuit tests, and the SDK end-to-end against a local fork. All green.
- The proof parity fixture is regenerated after any circuit change, and the zkey hash is updated in the SDK.
- No secrets in the repo: `DEPLOYER_PK`, `X_BEARER`, `AURORA_KEY` and similar only in env or CRE secrets.
- Gas: the logged `gasUsed` × 1.15 ≤ the limit sent.
- The README's "what's live / what's not" table matches what's actually deployed (Gloam's "honest gates" habit).

---

## 11. Demo script (3 minutes)

1. **0:00** The problem. Open the Monad explorer on someone's payroll wallet: every salary is visible. One line: "Privacy that needs an operator isn't private."
2. **0:20** Face ID → a Veil account. The **Accounts** panel shows everything derived from one passkey (Mera ×2).
3. **0:40** Fund from Base via Aurora (confidential), then shield. Explain what's hidden at each step.
4. **1:00** Payroll: upload a CSV of 5 AUSD payees in Lagos and Nairobi and run it. The explorer shows only shielded transactions (Agora).
5. **1:30** Terminal: a Claude Code agent with `mm veil x402 fetch` buys an API call in about 1–2 s. Show the guard cap, then the payee's receipt being verified (MetaMask, x402).
6. **2:10** Campaign: the KOL posts with `#ad`, the CRE report lands, and the KOL's private balance increases. The project treasury appears nowhere (CRE).
7. **2:40** Envio-powered transparency page: TVL, transaction counts, nothing personal. Verified mode with Cleanverse. Close: "no operator, client-side proofs, one Monad block."

---

## 12. Submission checklist

- [ ] The public repo has every commit after 7 Oct. README with a "Prior art and dependencies" section crediting Gloam as design inspiration.
- [ ] Live app URL (testnet plus capped mainnet) and contract addresses on the explorer.
- [ ] mm plugin published on npm (or installable from git) with install steps.
- [ ] Demo video, 3 minutes or less.
- [ ] Write-up: problem, how it works, sponsor integrations (one paragraph each, naming the exact file), privacy model and limits, dev ceremony disclosed.
- [ ] Every bounty selected in the portal: Mera ×2, MetaMask, Envio, Agora Cross-Border, Chainlink CRE (+ Cleanverse, Aurora if built).
- [ ] Track 04 selected.

---

## 13. Risks and open questions

| Risk | Mitigation |
|---|---|
| The ZK core slips (circuits are the long pole) | Plan B gate at the end of Day 1 (Unlink testnet). Keep the circuit minimal: one circuit, no extra features |
| Overloaded calendar (BNB on 11 Oct, Colosseum on 12 Oct) | Decide today (§9) |
| Mera PRF unavailable in the judge's browser | The demo video uses Safari or iOS. The README lists supported authenticators. Read-only mode lets anyone browse without signing in |
| MetaMask agent wallet signatures may not be deterministic | Fall back to a locally generated, encrypted key plus `mm veil export` |
| X API impression delay or cost | Poll every 10 min. Pay only increases. Cap per post. State the delay |
| CRE Early Access not granted in time | Simulation with `--broadcast` is a real on-chain write. Confirm with the bounty text |
| Issuer freeze on AUSD or USDC | Separate pools, caps, disclosure |
| Privacy limits (amounts visible at deposit and withdrawal, timing) | Explain in PRIVACY-MODEL.md. In the UI, suggest round amounts and a delay before withdrawing |
| Regulatory optics of a privacy pool | Verified mode (Cleanverse), OFAC screening at the relayer, receipts and view keys, the disclosed-ad rule for KOL streams |
| Bounty texts unknown | Day 0: read them all and update §5 |

---

## 14. Sources

**Monad:**
- [Privacy providers](https://docs.monad.xyz/tooling-and-infra/privacy)
- [Unlink on Monad](https://monad.xyz/blog/privacy-comes-to-monad-with-unlink)
- [Mera guide](https://docs.monad.xyz/guides/mera)
- [x402 guide](https://docs.monad.xyz/guides/x402)
- [Agentic payments](https://docs.monad.xyz/tooling-and-infra/agentic-payments)
- [Differences from Ethereum](https://docs.monad.xyz/developer-essentials/differences)
- [Opcode pricing](https://docs.monad.xyz/developer-essentials/opcode-pricing)
- [RPC differences](https://docs.monad.xyz/reference/rpc-differences)
- [Metropolis page](https://monad.xyz/developers/hackathons/metropolis)

**Category Labs privacy tease:**
- [Startup Fortune](https://startupfortune.com/monad-teases-privacy-tech-at-singapore-summit-and-mon-jumps-18/)

**Unlink:**
- [Docs](https://docs.unlink.xyz/)
- [Supported chains](https://docs.unlink.xyz/supported-chains)
- [Trust model](https://docs.unlink.xyz/trust-model)
- [Quickstart](https://docs.unlink.xyz/quickstart)

**MetaMask:**
- [Agent Wallet docs (full)](https://docs.metamask.io/llms-agent-wallet-full.txt)
- [Plugin template](https://github.com/MetaMask/agent-wallet-plugin-template)
- [MonAgent](https://github.com/zakyirsyaad/monagent)
- [mm-plugin-perpl](https://github.com/akugone/mm-plugin-perpl)

**Chainlink CRE:**
- [CRE docs (TS, full)](https://docs.chain.link/cre/llms-full-ts.txt)
- [Supported networks](https://docs.chain.link/cre/supported-networks-ts)

**Envio:**
- [Monad testnet](https://envio.dev/chains/monad-testnet)

**Agora / AUSD:**
- [AUSD on Aave Monad: assessment](https://governance.aave.com/t/agora-usd-ausd-on-aave-monad-assessments/25251)

**Aurora:**
- [Intents docs (full)](https://docs.intents.aurora.dev/llms-full.txt)
- 1Click token list (`1click.chaindefuser.com/v0/tokens`)

**Nansen:**
- [x402 payments](https://docs.nansen.ai/getting-started/agentic-payments/x402-payments.md)

**Cleanverse:**
- [Build hackathon](https://cleanverse.com/hackathon)
- [TrustFlow](https://github.com/pranay123-stack/trustflow)
- [SpendClear](https://github.com/Cubiczan/spendclear-cleanverse)

**Prior art:**
- [Gloam](https://github.com/cryptoduke01/gloam) (MIT; design reference only)
- [Privacy Pools core](https://github.com/0xbow-io/privacy-pools-core) (Apache-2.0)
- Tornado Nova (2-in/2-out design)

**Earlier research in this repo:** [`RESEARCH.md`](RESEARCH.md), [`SPONSORS.md`](SPONSORS.md).
