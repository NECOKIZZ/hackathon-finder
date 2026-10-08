# Veil — BUILD.md (Monad Metropolis)

**Version 2 · 2026-10-08.** Deadline: **13 Oct 2026**. We submit on **12 Oct**, and the 13th is buffer only.
**Name:** Veil. **Chain:** Monad (testnet `10143`, mainnet `143`). **Track:** 04 Trust, Identity & AI Infra.

This is a build playbook for the coding agent that will build Veil. It is written to be followed step by step.

**What ships with this file (the `veil-handoff` bundle):**

| Folder | What it is | How to use it |
|---|---|---|
| `reference-kit/` | **Working, tested reference code**: the ZK circuit, the pool contract, the stream vault, the Cleanverse verified pool, and a JS core that builds proofs. Verified 2026-10-08: 13/13 Forge tests, 31/31 end-to-end checks on anvil, 6/6 circuit attack tests | **Start from this.** Copy it into the new repo in Phase 1, then extend it |
| `gloam/` | Snapshot of github.com/cryptoduke01/gloam: a ZK privacy pool by another builder, live on Robinhood Chain and Tempo | **Read-only reference.** It shows how a working pool was built, deployed and debugged on other chains. Read the matching Gloam file before each module (§4). **Never copy its code** |
| `reference-repos/` | `monagent` and `mm-plugin-perpl` (MetaMask Agent Wallet plugins on Monad); `trustflow` and `spendclear-cleanverse` (Cleanverse integrations on Monad) | Patterns for the mm plugin (Phase 7) and the Cleanverse adapter (Phase 9) |
| `docs-offline/` | Full text of the MetaMask Agent Wallet docs, Mera guide, Chainlink CRE TS docs, Envio docs and Aurora Intents docs | Search these before guessing an API. They are newer than your training data |

---

## 0. Rules for the agent (read first)

1. **Follow the phases in order.** Each phase ends with "Done when". Do not start the next phase until those checks pass. If a check can't pass, stop and report exactly what fails.
2. **Never change the crypto conventions in §3.** Every piece (circuit, contract, SDK, indexer, relayer, plugin) depends on them: the hash order, the public-input order, the ExtData encoding and the memo formats. If you think one is wrong, stop and ask.
3. **Never weaken a check to make something pass.** Don't delete or skip a test, don't remove a `revert`, don't set a verifier to always return `true`, and don't mock a proof.
4. **UI and visual design are up to you.** This file specifies flows, data and error states, not looks. Keep the UI honest: never show a success that didn't happen on-chain.
5. **Never use real money above the caps in §16.** Mainnet is a capped beta.
6. **Secrets only in environment variables:** deployer key, relayer key, X token, API keys. Never commit them. Never prefix server secrets with `NEXT_PUBLIC_`.
7. **New-work rule (hackathon):** create a **fresh public repo** today. Every commit must be made now (Oct 8–12). Gloam is **reference only**. In the README, credit Gloam (design inspiration, MIT), Tornado Nova (the 2-in/2-out design), circomlib, snarkjs, Mera, x402, CRE and Envio.
8. **When a doc and this file disagree on an external API** (Mera, CRE, Envio, MetaMask, Aurora, x402), the doc in `docs-offline/` wins. Note the difference in `docs/NOTES.md`.
9. **Monad charges the gas LIMIT you set, not the gas used.** Always estimate, multiply by 1.15, and pass that as `gas`. Never hardcode a big number.
10. **Commit small and often.** Use clear messages, and push at the end of every phase.

---

## 1. What we are building

> **Pay people and agents on Monad without publishing your payroll, your marketing budget or your agent's spending history. Only the payer and payee see the amount. Proofs are made on your own device; there is no operator who can see anything.**

One shielded pool per stablecoin powers four surfaces:

| Surface | User | What they do |
|---|---|---|
| **Web app** (Next.js) | Founders, finance teams, KOLs, contractors | Passkey sign-in (Mera). Deposit USDC or AUSD, or fund from any chain (Aurora). Send privately. Run payroll from a CSV. Create a KOL campaign and fund it privately. Withdraw. Share a receipt. Verify a receipt |
| **MetaMask Agent Wallet plugin** (`mm veil …`) | AI agents and their owners | An agent pays other agents and paid APIs privately, within caps its owner sets |
| **x402 `shielded` scheme** (merchant middleware + relayer) | API sellers and agent buyers | A paid API accepts private payments next to the normal public `exact` scheme |
| **StreamVault + Chainlink CRE workflow** | Founders → KOLs, employers → staff | The budget streams out as private notes, per verified X impression (CRE) or per second (salaries) |

**Positioning versus what Monad already has** (use this in the README and write-up):

| | Who sees payments | Status on Monad | How Veil differs |
|---|---|---|---|
| Unlink | Its engine generates proofs on its servers and **keeps users' viewing keys** | Mainnet needs an access grant | Proofs on the user's device. No operator |
| TACEO Merces | A network of MPC servers. Compliance attestation required | Mainnet, limited access | Permissionless and self-custodial |
| Category Labs "privacy" | Unknown (teaser on 6 Oct) | Not launched | Built for people and agents now |

**Never claim** "audited", "production-ready" or "untraceable". Deposit and withdrawal amounts are public, and so is timing (§15).

---

## 2. Sponsor bounties (what each needs from us)

Bounty texts are behind the portal login. **The human owner must read them on Day 0** and update this table if anything differs.

| Bounty | Prize | Where in this plan | What judges must SEE |
|---|---|---|---|
| Mera: Best Mera-Powered UX | $2,500 | Phase 6 (onboarding), §3.1 | Face ID → private account in seconds, no seed phrase, restore on another device |
| Mera: One Passkey, Many Keys | $2,500 | §3.1 key tree, Phase 6 Accounts panel | One passkey derives the public wallet, spend key, shareable view key, at-rest key, agent accounts and per-campaign keys |
| MetaMask: Best Agent Wallet Plugin | $2,500 | Phase 7 | `mm veil …` commands: an agent deposits under MetaMask policy, then pays privately within caps |
| Envio: Best Use of Envio | $1,000 | Phase 4 | The wallet syncs the Merkle tree and finds its notes from Envio, plus dashboards |
| Agora: Best Cross-Border Payments App | $10,000 | AUSD pool (Phase 2), payroll (Phase 6) | Private AUSD payroll to people in other countries; AUSD as the default dollar |
| Chainlink: Best workflow with CRE | $3,000 | Phase 8 | CRE reads X impressions with node consensus and its report decides KOL payouts |
| Cleanverse: Best Integration of CVI/CVA | $2,000 | Phase 9 (add if on schedule) | Verified mode: only CVI-verified wallets can deposit or receive withdrawals |
| Aurora: Any-Chain Liquidity | $5,000 | Phase 10 (add if on schedule) | Fund from another chain with a confidential swap, then shield |
| Nansen | $5,000 | Phase 11 (optional) | Relayer screens withdrawal recipients with Nansen data, paid by x402 on Monad |

Skip Privy and Dynamic (they conflict with Mera), plus Kuru, Perpl and Community.
Register agents and the demo API in **ERC-8004** (no bounty, but it's named in Track 04): Phase 12.

---

## 3. Crypto conventions (never change these)

All of these are implemented and tested in `reference-kit/`. Field = BN254 scalar field, `p = 21888242871839275222246405745257275088548364400416034343698204186575808495617`.

### 3.1 Keys

```
privKey (spend)  = keccak256("veil-spend-v1" ‖ seed32) mod p
pubKey           = Poseidon(privKey)                      // Poseidon with 1 input
encPriv (view)   = keccak256("veil-enc-v1" ‖ seed32)      // 32 bytes, x25519 private key
encPub           = x25519(encPriv)
Veil address     = "veil:0x" ‖ hex32(pubKey) ‖ hex32(encPub)    // 7 + 128 characters
```

`VeilKeys.fromSeed(seed32)` in `reference-kit/sdk-test/veil-core.mjs` does exactly this.

**Where seeds come from: the Mera key tree.** `prfOutput` (32 bytes) comes from the passkey (Phase 6). `child(i) = deriveEvmKey(prfOutput, i)` uses Mera's documented BIP-44 path `m/44'/60'/0'/0/i`.

| Index `i` | Used as | Notes |
|---|---|---|
| 0 | **Public EOA** (viem account via `createSecp256k1SigningSession`) | Pays gas, deposits, receives withdrawals by default |
| 1 | Seed for the **main Veil account**: `VeilKeys.fromSeed(child(1))` | Spend key + view key of the main balance |
| 2 | **Shareable auditor view key**: a second x25519 key whose public half is registered as the account's "audit key" | Optional. The main `encPriv` from index 1 is already a full view key. Index 2 exists for the "share with my accountant" demo; the app encrypts a copy of each outgoing note to it (`encryptedOutput` stays to the recipient; the audit copy is stored client-side and exportable) |
| 3 | **At-rest key**: AES-256-GCM key = `keccak256("veil-at-rest-v1" ‖ child(3))` | Encrypts the local note cache (Gloam audit M-1 fix) |
| 10 + k | Seed for **agent sub-account k** (k = 0…9) | Each agent has its own Veil address and balance |
| 100 + j | **Campaign admin EOA** for campaign j | Signs StreamVault admin calls. Funded with gas by the relayer drip, so it's never linked to the treasury |
| 200 + j | Seed for the **campaign refund Veil account** j | `adminPubKey` in StreamVault; unspent budget returns here |

Persist the next free `j` and `k` in localStorage. They're not secret. Show this tree in the UI ("Accounts"); it's the Mera "Many Keys" demo.

### 3.2 Notes

```
commitment = Poseidon(amount, pubKey, blinding)           // 3 inputs, in this order
signature  = Poseidon(privKey, commitment, leafIndex)
nullifier  = Poseidon(commitment, leafIndex, signature)
amount < 2^128; blinding = 31 random bytes (always < p)
```

One pool contract per asset, so the asset is NOT part of the note.

### 3.3 Merkle tree

Depth 20. Empty leaf = 0. `zeros[i+1] = Poseidon(zeros[i], zeros[i])`. Node = `Poseidon(left, right)`. Leaves are inserted in event order. The tree root after N inserts must equal the contract's `currentRoot`. **Every root ever produced stays valid** (`knownRoots`), so a proof built against an older root still lands.

### 3.4 Circuit `transaction2x2` (2 inputs, 2 outputs, depth 20)

Public inputs, in this exact order: `[root, publicAmount, extDataHash, inputNullifier[0], inputNullifier[1], outputCommitment[0], outputCommitment[1]]`.

| Constraint | Why |
|---|---|
| Each input: commitment opens with the key; nullifier derived as in §3.2; Merkle path checked **unless amount = 0** (dummy input) | Ownership plus membership |
| `Num2Bits(128)` on every input and output amount | No field wrap-around (Gloam Kensho C2) |
| `inputNullifier[0] != inputNullifier[1]` | No double-spend inside one transaction |
| `sum(in) + publicAmount == sum(out)` (mod p) | Value conservation |
| `extDataHash` squared into a dummy signal | Binds recipient, relayer, fee and memos to the proof |

### 3.5 ExtData and publicAmount

```solidity
struct ExtData { address recipient; int256 extAmount; address relayer; uint256 fee; bytes encryptedOutput1; bytes encryptedOutput2; }
extDataHash  = uint256(keccak256(abi.encode(extData))) % p          // abi.encode of the STRUCT (tuple)
publicAmount = (extAmount - fee) mod p                              // the contract computes it; the prover can't choose
```

| Case | extAmount | fee | Who sends the tx |
|---|---|---|---|
| Deposit | `+amount` | 0 | The depositor's own wallet (tokens are pulled from `msg.sender`) |
| Private transfer | 0 | relayer fee (testnet 0) | Relayer |
| Withdrawal | `−amount` | relayer fee | Relayer (recipient is bound in the proof) |

### 3.6 Memo formats (`encryptedOutputN` / `depositTo` memo)

| Format | Length | Content | Made by |
|---|---|---|---|
| Encrypted | 120 bytes | `ephPub(32) ‖ nonce(24) ‖ XChaCha20-Poly1305(ct of amount(16 BE) ‖ blinding(32 BE), 64 incl. tag)`. Key = HKDF-SHA256(x25519(eph, encPub), info `"veil-note-v1"`, 32 bytes) | SDK, for every `transact` output |
| Plain | 49 bytes | `0x01 ‖ amount(16 BE) ‖ blinding(32 BE)` | Contracts (StreamVault) that can't encrypt |

**Scanner rule:** for each `NewCommitment(commitment, index, memo)`, call `readMemo(encPriv, memo)`. If it returns `{amount, blinding}` and `Poseidon(amount, myPubKey, blinding) == commitment`, the note is yours. **Always recompute the commitment.** A memo can lie.

### 3.7 Events (the indexer and wallets depend on these exact signatures)

```
VeilPool:    NewCommitment(uint256 commitment, uint256 index, bytes encryptedOutput)
             NewNullifier(uint256 nullifier)
StreamVault: PostRegistered(uint256 indexed postId, uint64 indexed xUserId)
             Report(uint256 indexed postId, uint64 impressions, bool valid)
             Payout(uint256 indexed postId, uint256 pubKey, uint256 amount, uint256 blinding, uint256 commitment, uint32 index, bool holdback)
             PostRejected(uint256 indexed postId, uint256 forfeited)
             StreamCreated(uint256 indexed streamId, uint256 pubKey, uint128 ratePerSecond, uint64 start, uint64 end)
             Drip(uint256 indexed streamId, uint256 amount, uint256 blinding, uint256 commitment, uint32 index)
             Closed(uint256 refunded)
Factory:     CampaignCreated(address indexed vault, address indexed admin, bytes32 salt)
```

---

## 4. Gloam map: which Gloam file to read before each module

Gloam solved the same problems on Robinhood Chain and Tempo. **Read the file, understand the lesson, write our own version.** Gloam's design differs from ours: it uses bearer-secret notes, 1 input → 2 outputs, separate circuits, and a multi-asset pool. Don't import those differences.

| Our module | Read in `gloam/` | What to learn | What we do differently |
|---|---|---|---|
| Circuit pipeline | `contracts/circuits/scripts/build-proof-circuits.mjs`, `contracts/circuits/common/merkle_poseidon.circom`, `contracts/circuits/transfer/transfer.circom` | compile → setup → contribute → export; artifact hash pinning; `Num2Bits(128)` range checks | One 2x2 circuit; leaf index bound into the nullifier |
| Poseidon on-chain | `contracts/circuits/scripts/deploy-poseidon.mjs`, `contracts/src/lib/IPoseidon.sol` | Deploy circomlibjs bytecode as separate contracts (guaranteed to match the circuit) | Same approach (`reference-kit/contracts/scripts/gen-poseidon-fixtures.mjs`) |
| Merkle tree | `contracts/src/lib/IncrementalMerkleTreePoseidon.sol` | Precomputed zeros (constructor gas); permanent `knownRoots` | Same idea. Our zeros constants are identical and tested |
| Pool contract | `contracts/src/ShieldPoolPoseidon.sol`, `contracts/audit/*` | `nonReentrant`, checks-effects-interactions, explicit errors, fee-on-transfer check, two-step owner, no admin withdraw | `transact` + `depositTo`, one asset per pool |
| Proof packing | `packages/sdk/src/proof.ts` | **pi_b coordinates must be swapped** for the Solidity verifier | Same (`buildTransaction` in the kit) |
| Poseidon/tree in TS | `packages/sdk/src/poseidon.ts`, `packages/sdk/src/merkle.ts` | circomlibjs `buildPoseidon` once, cached | Kit `MerkleTree` |
| Proving in browser | `app/src/lib/proveClient.ts`, `app/src/lib/circuitArtifacts.ts` | Serve wasm/zkey from `/public/circuits`, check sha256 before use | Same |
| Tree sync | `packages/sdk/src/sync.ts`, `app/src/lib/treeSync.ts`, `app/src/app/api/vault-leaves/` | Replay leaves in exact on-chain order; chunk `getLogs`; verify the root | Envio first, RPC fallback |
| Note encryption | `packages/sdk/src/receiveTag.ts` | Ephemeral ECDH + HKDF + AEAD; base64url encodings | x25519 + XChaCha20-Poly1305 (§3.6) |
| Note vault at rest | `app/src/lib/noteVault.ts`, `app/src/lib/passkeyWrap.ts`, `app/src/lib/secretBox.ts` | Encrypt secrets in localStorage | Key from Mera index 3 |
| Relay | `app/src/lib/relay/server.ts`, `app/src/lib/relay/client.ts`, `app/src/app/api/relay/route.ts` | Dry-run before send; pad gas; nonce retry; rate limits; neutral error messages; screening | Our relayer earns a fee bound in the proof |
| Screening | `app/src/lib/screeningServer.ts`, `app/src/lib/screeningList.json`, `app/scripts/refresh-ofac-list.mjs` | OFAC list snapshot check on public addresses | Same |
| Payroll | `app/src/lib/payroll.ts`, `app/src/lib/payrollSchedule.ts` | **Crash safety**: persist the change note and row state BEFORE submitting; reconcile against `isSpent` on resume; claim links | 2 inputs, so the change can merge |
| Payment requests | `app/src/lib/paymentRequest.ts` | Put request details after `#` so they never reach a server | Same |
| Disclosure | `app/src/lib/disclosure.ts`, `packages/sdk/src/proofs.ts` | Prove one note to one party | Receipt = note opening (§6.9). No extra circuit |
| x402 | `packages/sdk/src/x402.ts`, `examples/pay-x402/`, `packages/mppx-gloam/` | 402 flow; their payer could spend back, so they needed a "sweep" | Key-owned notes, so no sweep |
| Agent limits | `mcp/src/policy.ts`, `mcp/src/spendGuard.ts`, `mcp/src/spendLog.ts`, `mcp/src/noteStore.ts` | Per-payment, per-day and allowed-recipient caps; reserve then settle in a log; file locks | Same rules inside the mm plugin |
| Network registry | `app/src/lib/networks.ts`, `app/src/lib/chain.ts`, `app/src/lib/config.ts` | One record per network; runtime switch | Monad testnet + mainnet |
| Deploy notes | `DEPLOY.md`, `DEPLOY-TEMPO.md`, `contracts/script/DeployTempoPool.s.sol` | Gas caps per chain, record deploy blocks | Monad specifics in Phase 2 |
| Transparency | `app/src/components/transparency/`, `app/src/lib/onchainMetrics.ts` | Public stats only | From Envio |
| Honesty | `README.md` "Honest gates", `contracts/audit/REMEDIATION.md` | What's live vs not; disclose the dev ceremony | Same habit |

---

## 5. Constants

| Name | Value |
|---|---|
| Monad mainnet | chainId `143`, viem `monad` from `viem/chains`, RPC `https://rpc.monad.xyz` (QuickNode, `eth_getLogs` max **100 blocks**), `https://rpc1.monad.xyz` (Alchemy, 1,000 blocks) |
| Monad testnet | chainId `10143`, viem `monadTestnet`, RPC `https://testnet-rpc.monad.xyz` |
| USDC mainnet | `0x754704Bc059F8C67012fEd69BC8A327a5aafb603` (6 decimals; EIP-712 domain name `"USDC"`, version `"2"`) |
| USDC testnet | `0x534b2f3A21130d7a60830c2Df862319e593943A3` (6 decimals) |
| AUSD mainnet | `0x00000000eFE302BEAA2b3e6e1b18d08D69a9012a` (6 decimals; issuer can freeze, pause and upgrade with no timelock) |
| AUSD testnet | None known. Deploy `MockERC20` "tAUSD" (6 decimals) and label it as a mock |
| x402 facilitator (public `exact` scheme) | `https://x402-facilitator.molandak.org`; use `@x402/evm >= 2.22.0` |
| ERC-8004 Identity Registry | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| ERC-8004 Reputation Registry | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |
| CRE forwarders | Testnet: simulation `0xB9F79d863261869B234c481D1f9A7af84AeAd192`, production `0xF8344CFd5c43616a4366C34E3EEE75af79a74482`. Mainnet: simulation `0x9eF6468C5f37b976E57d52054c693269479A784d`, production `0x76c9cf548b4179F8901cda1f8623568b58215E62`. Chain names: `monad-testnet`, `monad-mainnet` |
| Envio HyperSync | `https://monad.hypersync.xyz` (143), `https://monad-testnet.hypersync.xyz` (10143) |
| Aurora Swap API | `https://intents-api.aurora.dev/api/quote/{apiKey}`. Monad USDC asset id (1Click list, re-fetch before use): `nep245:v2_1.omni.hot.tg:143_2dmLwYWkCQKyTjeUPAsGJuiVLbFx` |
| Nansen x402 | `https://api.nansen.ai/api/v1/profiler/address/counterparties` ($0.05), `.../related-wallets` ($0.01). USDC on Monad, 5 requests/s |
| ptau (2^16) | `https://pse-trusted-setup-ppot.s3.eu-central-1.amazonaws.com/pot28_0080/ppot_0080_16.ptau`, sha256 `ed3622a7c79b0b49aadd134ebbc5b77df8c8c59bccebdfd0d9bf2c1a51561cf9`. The Hermez links Gloam used now return **403** |
| Tool versions (verified) | circom 2.2.2, snarkjs 0.7.5, circomlib 2.0.5, circomlibjs 0.1.7, Foundry 1.5.1, solc 0.8.24 (evm `cancun`), OpenZeppelin 5.1.0, viem 2.57, Node 22, `@noble/curves@1`, `@noble/ciphers@1`, `@noble/hashes@1` |
| Gas (measured; Monad adds ≈ +0.9M per proof verify) | `transact` ≈ 1.75M on anvil, **≈ 2.7M on Monad**; `depositTo` ≈ 0.84M; StreamVault `onReport` (1 post) ≈ 1.0M. Always estimate × 1.15 |
| Proof time | ≈ 1.6 s per proof in Node. Browser: 2–5 s (use a Web Worker) |

---

## 6. Phases

### Phase 0: Human setup (owner, Day 0, ~1 hour, can run in parallel with Phase 1)

1. Read every bounty's text in the portal (§2). Note required items such as "deployed on mainnet", "video", "npm package".
2. **Fix the domain now** (e.g. `veil-pay.xyz` or a Vercel subdomain). Mera passkeys are bound to the domain (`rpId`). Changing it later loses every account.
3. Create accounts and keys:

| Service | What | Env var |
|---|---|---|
| GitHub | Fresh public repo `veil-monad` | — |
| Deployer wallet | New EOA with testnet MON (faucet) and later ~5 MON mainnet | `DEPLOYER_PK` |
| Relayer wallet | Separate new EOA with MON | `RELAYER_PK` |
| Chainlink CRE | Account, `cre login`; request Early Access (`cre account access`) | `CRE_ETH_PRIVATE_KEY` (for `--broadcast` simulation) |
| X API | Developer account with tweet lookup (pay-per-use) | `X_BEARER_TOKEN` |
| Envio | Envio Cloud (hosted indexer) account linked to GitHub | — |
| Aurora | API key from studio.aurora.dev (not secret) | `NEXT_PUBLIC_AURORA_KEY` |
| Cleanverse | Ask for sandbox access and the CVA token address on Monad (Discord or portal) | — |
| Agora | Optional: book a Stablecoin API demo (don't depend on it) | — |
| MetaMask | `npm i -g @metamask/agent-wallet@7`, `mm login`, `mm init --mode guard` | — |

**Done when:** domain fixed, repo created, both wallets funded on testnet, CRE logged in, X token works (`curl -H "Authorization: Bearer $X_BEARER_TOKEN" "https://api.x.com/2/tweets?ids=20&tweet.fields=public_metrics"` returns JSON).

---

### Phase 1: Repo and circuit (Day 1 morning)

**Repo layout** (pnpm workspaces):

```
veil-monad/
  circuits/            ← from reference-kit/circuits
  contracts/           ← from reference-kit/contracts (Foundry)
  packages/sdk/        ← @veil/sdk (TypeScript), ported from reference-kit/sdk-test/veil-core.mjs
  packages/mm-plugin/  ← @veil/mm-plugin
  services/relayer/    ← Hono + Node (relayer + gas drip + screening)
  services/cre/        ← CRE workflow (TypeScript, Bun)
  indexer/             ← Envio HyperIndex
  apps/web/            ← Next.js app (UI is your design)
  apps/demo-api/       ← paid API (x402 shielded + exact)
  docs/                ← PRIVACY-MODEL.md, THREAT-MODEL.md, PRIOR-ART.md, NOTES.md
  e2e/                 ← reference-kit/sdk-test e2e + circuit-negative, kept green forever
  deployments/         ← testnet.json, mainnet.json (addresses + deploy blocks)
```

**Steps**

1. `git init`, add `pnpm-workspace.yaml` with `packages/*`, `services/*`, `apps/*`, `indexer`, `e2e`. Add `.gitignore`: `node_modules`, `circuits/build`, `*.ptau`, `contracts/out`, `contracts/cache`, `.env*` (except `.env.example`).
2. Copy `reference-kit/circuits` → `circuits/`. Run `npm i` (or pnpm), then `bash scripts/setup.sh`. This downloads the ptau (75 MB), compiles and makes the keys (~2 min). Pass `-e` to every `snarkjs zkey contribute`, or it hangs waiting for keyboard input; the script already does this.
3. Note the printed `wasm sha256` and `zkey sha256`. Put them in `packages/sdk/src/artifacts.ts` (Phase 3).
4. Copy `circuits/build/Verifier.sol` → `contracts/src/Verifier.sol`.
5. Copy `reference-kit/sdk-test` → `e2e/`. Keep it unchanged: it's the regression suite.

**Done when:** `circuits/build/transaction2x2_js/transaction2x2.wasm` and `transaction2x2_final.zkey` exist; `snarkjs r1cs info` shows 7 public inputs.

**If you ever change the circuit:** rerun setup, copy the new Verifier.sol, redeploy **both** verifier and pools (old pools can't verify new proofs), update hashes, rerun all tests. Avoid this after Day 2.

---

### Phase 2: Contracts (Day 1)

**Steps**

1. Copy `reference-kit/contracts` → `contracts/`. Install libs: `forge install --no-git foundry-rs/forge-std OpenZeppelin/openzeppelin-contracts@v5.1.0`, or with git submodules. Keep `foundry.toml` as is.
2. `forge build && forge test` must pass (13 tests).
3. Run the e2e suite: start `anvil --gas-limit 300000000` in one terminal, then `cd e2e && npm i && node e2e.mjs && node circuit-negative.mjs`. It must show **31 passed** and **6 passed**.
4. **Add these Forge tests** (new file `test/VeilPool.t.sol`). Use the fixture approach from `StreamVault.t.sol` for Poseidon, and a `MockVerifier` that returns a configurable bool **only inside tests**:
   - `transact` reverts with `UnknownRoot` for a random root.
   - `BadPublicAmount` when `publicAmount` ≠ `calculatePublicAmount(extAmount, fee)`.
   - `DepositTooLarge` above `maxDepositAmount`; `DepositsArePaused` when paused (deposit only — withdrawals must still work while paused).
   - `ZeroRecipient` on a withdrawal to `address(0)`; `ZeroRelayer` when `fee > 0` and relayer is 0.
   - `FeeOnTransferToken` with a mock token that burns 1% on transfer.
   - Reentrancy: a mock ERC-20 that calls back into `transact` during `transfer` → reverts (`ReentrancyGuardReentrantCall`).
   - `zeros(i+1) == hasher.poseidon([zeros(i), zeros(i)])` for i = 0…19, and `currentRoot == zeros(20)` after deploy.
   - **Invariant (fuzz):** after random sequences of `depositTo`, `token.balanceOf(pool) == sum of all deposited − sum of all withdrawn`.
5. **Deploy script** `contracts/script/Deploy.s.sol` (Foundry script) or `scripts/deploy.mjs` (viem). Order:
   1. `Poseidon2` and `Poseidon3` from `test/fixtures/poseidon{2,3}.hex` (raw `create`; see `_deployCode` in the tests).
   2. `Groth16Verifier` (from `src/Verifier.sol`).
   3. `VeilPool(verifier, poseidon2, poseidon3, USDC, maxDeposit)` → **USDC pool**.
   4. `VeilPool(…, AUSD or tAUSD, maxDeposit)` → **AUSD pool**.
   5. `StreamVaultFactory()`.
   6. If doing Cleanverse: `MockCviOracle(attester)` and `VerifiedVeilPool(…, USDC or CVA token, maxDeposit, cvi)` → **verified pool**.
   7. Write `deployments/testnet.json`:
      ```json
      { "chainId": 10143, "poseidon2": "0x…", "poseidon3": "0x…", "verifier": "0x…",
        "pools": { "USDC": { "address": "0x…", "token": "0x534b…", "decimals": 6, "deployBlock": 123 },
                   "AUSD": { "address": "0x…", "token": "0x…", "decimals": 6, "deployBlock": 124, "mock": true } },
        "streamVaultFactory": "0x…", "verifiedPool": null, "cvi": null,
        "zkey_sha256": "…", "wasm_sha256": "…" }
      ```
6. Deploy to **Monad testnet**: `forge script script/Deploy.s.sol --rpc-url https://testnet-rpc.monad.xyz --broadcast --private-key $DEPLOYER_PK`. Some forge versions need `--slow` and `--legacy` if EIP-1559 estimation fails. Record each deploy block (needed by Envio and RPC sync).
7. Verify contracts on the explorer if possible (MonadVision / Monadscan; the BlockVision verifier docs are linked from the Monad docs). Not required, but it helps judges.
8. **Testnet smoke test:** point `e2e/e2e.mjs` at testnet with a copy `e2e/testnet-smoke.mjs` that uses deployed addresses, `monadTestnet` and your funded keys. Use the testnet USDC (get it from the faucet) or a `MockERC20`. Run one deposit → transfer → withdraw. **Log `gasUsed` for each and check `gasUsed × 1.15 < gas sent`.**

**Done when:** all Forge tests pass, the e2e suite passes on anvil, and the testnet smoke test passes with real Monad testnet transactions (save the tx hashes in `docs/NOTES.md`). **This is the safety gate for end of Day 1.** If it isn't green by then, report it.

---

### Phase 3: SDK `@veil/sdk` (Day 1 evening → Day 2)

Port `veil-core.mjs` to TypeScript **without changing any formula**. Build with `tsup` (ESM + CJS). Use the same dependencies as the kit.

| File | Exports | Notes |
|---|---|---|
| `constants.ts` | `FIELD_SIZE`, `LEVELS = 20`, `MAX_NOTE_AMOUNT`, `NETWORKS` (from `deployments/*.json`) | One registry; the app and plugin import from here |
| `poseidon.ts` | `poseidon(inputs: bigint[]): Promise<bigint>` | Cache `buildPoseidon()` |
| `keys.ts` | `VeilKeys.fromSeed(seed32)`, `keysFromPrf(prfOutput)` → `{ publicAccountKey, main, auditEnc, atRestKey, agent(k), campaignAdmin(j), campaignRefund(j) }` | Uses Mera's `deriveEvmKey` (copy the 5-line function from `docs-offline/monad-mera-guide.md` — it uses `@scure/bip32` and `@scure/bip39`) |
| `address.ts` | `formatAddress(keys)`, `parseAddress(str)` | Reject pubKey ≥ p and wrong length |
| `note.ts` | `commitmentOf`, `nullifierOf`, `type Note = { amount, pubKey, blinding, index }` | |
| `memo.ts` | `encryptNote`, `decryptNote`, `readMemo` | Exactly as the kit (§3.6) |
| `tree.ts` | `MerkleTree` (`leaves`, `root()`, `path(i)`), plus an incremental cache | The kit rebuilds all layers per call. Add caching: keep `layers` and update only the new leaf's path on insert. Must still equal the kit's output (add a test comparing both for 1, 2, 3, 100, 1,000 leaves) |
| `sync.ts` | `syncFromEnvio(gqlUrl, pool, fromIndex)`, `syncFromRpc(client, pool, fromBlock, chunk=100n)`, `assertRoot(client, pool, root)` | Leaves must be contiguous by `index`. After syncing, `pool.isKnownRoot(localRoot)` must be `true`; otherwise discard and resync from RPC |
| `wallet.ts` | `scanNotes(keys, commitments)`, `spendable(notes, isSpent)`, `balance(notes)` | Spent check: `pool.isSpent(nullifier)` (batch with multicall) or the Envio Nullifier set |
| `coinSelect.ts` | `selectInputs(notes, target)` → `{inputs, change}` or `{needsMerge: [a, b]}` | Rules below |
| `artifacts.ts` | `WASM_SHA256`, `ZKEY_SHA256`, `loadArtifacts(baseUrl)` | Download, sha256-check, cache (IndexedDB in browser) |
| `prover.ts` | `nodeProver(paths)`, `browserProver(urls)` (Web Worker) | Both call `snarkjs.groth16.fullProve` |
| `tx.ts` | `buildTransaction(...)` (kit), `buildDeposit`, `buildTransfer`, `buildWithdraw` | `buildTransfer(to: VeilAddress, amount, fee, relayer)` puts the payment in output 0, change in output 1 |
| `submit.ts` | `submitDirect(walletClient, pool, tx)`, `submitViaRelayer(url, chainId, pool, tx)` | Direct submission is used for deposits. Relayer for transfer and withdraw by default |
| `store.ts` | `NoteStore` (encrypted with the at-rest key; localStorage in browser, a 0600 JSON file in Node) | Store notes plus pending tx state |
| `disclose.ts` | `makeReceipt(note, pool, chainId)`, `verifyReceipt(receipt, client, envio)` | §6.9 |
| `x402.ts` | `shieldedPaymentRequirements(...)`, `payShielded(...)`, `verifyShieldedPayment(...)` | Phase 5 |
| `payroll.ts` | `runPayroll(rows, ctx, onProgress)` | Phase 6 |
| `bigintJson.ts` | `stringify`/`parse` that keep bigint as decimal strings | JSON can't hold bigint; never use `Number` for amounts |

**Coin selection (2 inputs max):**

1. `need = amount + fee`. Sort spendable notes descending.
2. If one note ≥ need → use the smallest such note (+ a dummy).
3. Else, if the two largest notes sum ≥ need → use the smallest pair that covers it.
4. Else → `needsMerge`: first send a **merge transaction** (2 largest notes → 1 note to self, fee 0 if self-submitted, or relayer fee), wait for confirmation, resync, repeat.
5. Change = sum(in) − need, sent to own address as output 1. A zero-amount change is fine (it's still a valid note).

**Rules:**
- All amounts are `bigint` in token units (6 decimals). Parse user input with `parseUnits(str, 6)`. Never use floats.
- Reject a transfer to an address that fails `parseAddress`.
- After every submit: wait for the receipt (`waitForTransactionReceipt`). Then read the `NewCommitment` logs **from the receipt** to learn the new indices immediately. Don't wait for the indexer.
- **Pending state:** before submitting a spend, write `{nullifiers, outputs, status: "pending"}` to the store. On restart, reconcile with `isSpent` (Gloam payroll lesson).

**Tests** (vitest): port every assertion from `e2e.mjs` into TS tests against anvil (spin up anvil in `globalSetup`). Add:
- the tree-cache equivalence test;
- `parseAddress(formatAddress(k))` round trip;
- `readMemo` on plain and encrypted memos;
- coin selection cases (one note, a pair, needs merge, exact match).

**Done when:** `pnpm --filter @veil/sdk test` is green and a Node script using only the SDK does deposit → transfer → withdraw on **testnet** via the relayer stub (direct submission is fine until Phase 5).

---

### Phase 4: Envio indexer (Day 2)

1. `pnpx envio init` in `indexer/` (TypeScript, "from ABI"). Use the VeilPool and StreamVault/Factory ABIs from `contracts/out`. **Pin an exact `envio` version** in package.json; the hosted service rejects `^`, `~` and `latest`.
2. `config.yaml` (adapt to the generated layout; check `docs-offline/envio-full.txt`, sections "Configuration file" and "Dynamic contracts"):

```yaml
name: veil-indexer
contracts:
  - name: VeilPool
    abi_file_path: abis/VeilPool.json
    events:
      - event: NewCommitment(uint256 commitment, uint256 index, bytes encryptedOutput)
      - event: NewNullifier(uint256 nullifier)
  - name: StreamVaultFactory
    abi_file_path: abis/StreamVaultFactory.json
    events:
      - event: CampaignCreated(address indexed vault, address indexed admin, bytes32 salt)
  - name: StreamVault
    abi_file_path: abis/StreamVault.json
    events:
      - event: PostRegistered(uint256 indexed postId, uint64 indexed xUserId)
      - event: Report(uint256 indexed postId, uint64 impressions, bool valid)
      - event: Payout(uint256 indexed postId, uint256 pubKey, uint256 amount, uint256 blinding, uint256 commitment, uint32 index, bool holdback)
      - event: PostRejected(uint256 indexed postId, uint256 forfeited)
      - event: StreamCreated(uint256 indexed streamId, uint256 pubKey, uint128 ratePerSecond, uint64 start, uint64 end)
      - event: Drip(uint256 indexed streamId, uint256 amount, uint256 blinding, uint256 commitment, uint32 index)
      - event: Closed(uint256 refunded)
chains:
  - id: 10143
    start_block: <lowest deploy block from deployments/testnet.json>
    contracts:
      - name: VeilPool
        address: ["<USDC pool>", "<AUSD pool>"]   # add the verified pool if deployed
      - name: StreamVaultFactory
        address: "<factory>"
      - name: StreamVault          # no address: registered dynamically from CampaignCreated
```

3. `schema.graphql`:

```graphql
type Commitment { id: ID! pool: String! index: BigInt! commitment: BigInt! memo: String! blockNumber: BigInt! txHash: String! }
type Nullifier { id: ID! pool: String! nullifier: BigInt! blockNumber: BigInt! }
type PoolStat { id: ID! commitments: BigInt! nullifiers: BigInt! }
type Campaign { id: ID! admin: String! createdAt: BigInt! totalPaid: BigInt! posts: BigInt! }
type Post { id: ID! campaign: String! postId: BigInt! xUserId: BigInt! lastImpressions: BigInt! paid: BigInt! rejected: Boolean! }
type Payout { id: ID! campaign: String! postId: BigInt! pubKey: BigInt! amount: BigInt! blinding: BigInt! commitment: BigInt! index: BigInt! holdback: Boolean! blockNumber: BigInt! }
```

   IDs: `Commitment.id = "<pool>-<index>"`, `Nullifier.id = "<pool>-<nullifier>"`, `Post.id = "<vault>-<postId>"`, `Payout.id = "<txHash>-<logIndex>"`.

4. Handlers: one per event. Write the entity, and update `PoolStat` and `Campaign` counters. For `CampaignCreated`, register the new vault as a dynamic `StreamVault` contract (follow the "contract register" syntax for your Envio version in the docs).
5. Run locally (`pnpm dev`, needs Docker) or deploy to Envio Cloud from GitHub. Add a second chain entry for `143` when mainnet is deployed.
6. **SDK query** (Hasura-style; check the generated GraphQL schema for exact names):

```graphql
query Leaves($pool: String!, $from: numeric!) {
  Commitment(where: {pool: {_eq: $pool}, index: {_gte: $from}}, order_by: {index: asc}, limit: 1000) { index commitment memo }
}
```

   Page by `index` until fewer than 1,000 come back. Pools store addresses lowercased; lowercase before querying.

**Done when:** after a testnet transaction, the GraphQL query returns the new commitments within ~10 s; `syncFromEnvio` rebuilds a tree whose root `isKnownRoot` accepts; stopping Envio makes the SDK fall back to `syncFromRpc` and still work (slower).

---

### Phase 5: Relayer, gas drip, and the x402 `shielded` scheme (Day 2–3)

**Run the relayer as ONE long-lived Node process** (Railway, Render, Fly or a small VM). Serverless functions run in parallel, and parallel instances reuse nonces. Use Hono + viem. Keep a single in-memory send queue, so only one transaction is in flight per relayer key.

#### 5.1 `POST /relay`

Request:
```json
{ "chainId": 10143, "pool": "0x…", "proof": { "a": ["…","…"], "b": [["…","…"],["…","…"]], "c": ["…","…"], "root": "…", "publicAmount": "…", "extDataHash": "…", "inputNullifiers": ["…","…"], "outputCommitments": ["…","…"] }, "extData": { "recipient": "0x…", "extAmount": "-3000000", "relayer": "0x…", "fee": "0", "encryptedOutput1": "0x…", "encryptedOutput2": "0x…" } }
```

All numbers are decimal strings. Checks, in this order (reply `400` with a short code on failure):

1. `chainId` and `pool` are in `deployments/*.json` → else `unknown_pool`.
2. `extData.extAmount <= 0` (the relayer never deposits) → else `deposit_not_relayed`.
3. `extData.relayer == relayer address` → else `wrong_relayer`.
4. `BigInt(fee) >= MIN_FEE[chainId][pool]` (testnet 0; mainnet e.g. 0.02 USDC) → else `fee_too_low`.
5. If `extAmount < 0`: screen `extData.recipient` against the OFAC list (and Nansen, Phase 11) → `403 screened` with a neutral message.
6. Recompute `hashExtData(extData)` locally == `proof.extDataHash` → else `bad_ext_data`.
7. `publicClient.simulateContract({ functionName: "transact", args: [proof, extData], account: relayer })` → decode the revert name (`UnknownRoot`, `NullifierAlreadySpent`, `InvalidProof`, …) and return it.
8. `estimateContractGas` × 1.15 → `writeContract({ gas })` → `waitForTransactionReceipt`.
9. Reply `{ "txHash": "0x…", "status": "success", "commitments": [{ "commitment": "…", "index": 12 }, …] }`, parsed from the receipt's `NewCommitment` logs.

Rate limit: 10 requests per minute per IP and 60 per minute per pool (in-memory). On a `nonce too low`, `replacement` or `already known` error: refetch the nonce and retry **once** (Gloam `relay/server.ts`).

#### 5.2 `GET /status`

Returns `{ relayer, chains: { "10143": { balanceMon, minFee: { "<pool>": "0" }, pools: [...] } } }`. The app shows "relay offline" when this fails, and offers direct submission from the public EOA as a fallback (with a warning that the wallet will be visible).

#### 5.3 `POST /gas-drip`

Funds a fresh **campaign admin EOA** (Mera index 100 + j) with 0.05 MON, so the treasury never pays its gas.
- Request: `{ address, chainId, signature }`, where `signature` = `personal_sign("veil-gas-drip:<address>:<chainId>")` by that address.
- Each address gets one drip only, limited to 5 per IP per day, and only if the address's balance is < 0.01 MON.

#### 5.4 x402 `shielded` scheme (spec)

Uses x402 v2 HTTP headers. All header values are base64 of JSON (see `docs-offline` and coinbase/x402 `specs/transports-v2/http.md`).

**1. Server → client:** `402` with header `PAYMENT-REQUIRED`:

```json
{ "x402Version": 2,
  "resource": { "url": "https://api.veil…/v1/quote", "description": "1 quote" },
  "accepts": [
    { "scheme": "shielded", "network": "eip155:10143", "amount": "10000", "asset": "<USDC token address>",
      "payTo": "veil:0x<pubKey><encPub>", "maxTimeoutSeconds": 60,
      "extra": { "pool": "<USDC VeilPool>", "relayer": "<relayer address>", "relayerUrl": "https://relay…", "fee": "0", "version": "veil-x402-1" } },
    { "scheme": "exact", "network": "eip155:10143", "amount": "10000", "asset": "<USDC token address>",
      "payTo": "<merchant public EOA>", "maxTimeoutSeconds": 60, "extra": { "name": "USDC", "version": "2" } }
  ] }
```

**2. Client:**
1. Picks the `shielded` entry.
2. Checks its guard (§7.3).
3. Builds `buildTransfer(payTo, amount, fee, relayer)`. The payment is output **0**, encrypted to the merchant's `encPub`.
4. Retries with header `PAYMENT-SIGNATURE`:

```json
{ "x402Version": 2, "accepted": { …the shielded entry… },
  "payload": { "proof": { …decimal strings… }, "extData": { … }, "paymentOutput": 0 } }
```

**3. Merchant middleware** (`apps/demo-api`, runs on the merchant's server because it needs the merchant's view key):
1. Decode the payload. `accepted` must deep-equal one of the merchant's current requirements → else `402 invalid_requirements`.
2. `extData.extAmount == 0`, `extData.recipient == 0x0`, `extData.relayer == extra.relayer`, `fee == extra.fee`.
3. `hashExtData(extData) == proof.extDataHash`.
4. `readMemo(merchantEncPriv, extData.encryptedOutput{paymentOutput+1})` → `{amount, blinding}`. Then `Poseidon(amount, merchantPubKey, blinding) == proof.outputCommitments[paymentOutput]` and `amount >= required` → else `402 underpaid`.
5. Idempotency: keep `sha256(header)` in memory for 10 minutes. Second use → `402 replay`. The chain also prevents a double-spend via the nullifier.
6. `POST relayerUrl/relay` with `{chainId, pool, proof, extData}` → on `success`, store the note `{amount, blinding, index}` in the merchant's NoteStore.
7. Respond `200` with the resource and header `PAYMENT-RESPONSE`: `{ "success": true, "transaction": "0x…", "network": "eip155:10143", "payer": "" }`.

**4. The `exact` fallback:** use `@x402/next` or `@x402/core` with the Monad facilitator (`https://x402-facilitator.molandak.org`) for clients that can't pay privately. Optional auto-shield: a cron job calls `depositTo(merchantPubKey, amount, blinding, encryptedMemo)` with collected revenue.

**Done when:** `curl` to the demo API returns 402 with both schemes; a Node script using `@veil/sdk` `payShielded` gets 200 in under 3 s on testnet; tampering any extData field or reusing the header fails; the relayer refuses an underpaid fee.

---

### Phase 6: Web app (Day 2–4; design is yours)

Use Next.js App Router + viem. Only show amounts from the SDK as `formatUnits(x, 6)`.

**Pages and flows (functional requirements):**

| Flow | Requirements |
|---|---|
| **Onboarding (Mera)** | `createPasskeyWithPrfOutput({ rp: { id: <fixed domain>, name: "Veil" }, user: {...} })` on first visit; store `credentialId` and `transports` in localStorage; `getPasskeyPrfOutput({ rpId, credential })` on return. Handle `MeraError` codes: `PRF_UNAVAILABLE` (tell the user to use iCloud Keychain, Google Password Manager or 1Password, or Safari/iOS), `PASSKEY_OPERATION_FAILED` (retry), `CRYPTO_UNAVAILABLE` (needs HTTPS). Derive `keysFromPrf`. Show the Veil address with a copy button |
| **Session** | Hold the session while the tab is open. Call `session.end()` and wipe keys from memory on sign-out or after 15 minutes idle. Re-prompt the passkey for withdrawals and payroll runs |
| **Accounts panel** (Mera "Many Keys") | List the derived keys from §3.1: public EOA (address + MON balance), main Veil address, audit view key (export button), agent accounts (create, list, balances), campaigns (admin EOA + refund address). This is a key demo screen |
| **Deposit** | Choose pool (USDC or AUSD), amount ≤ `maxDepositAmount`. Send `approve` (exact amount) then `transact` (deposit proof) from the public EOA with explicit `gas`. Show "Monad charges the gas limit" in a tooltip. Then show the new private balance |
| **Fund from any chain** | Phase 10 |
| **Balance** | Private balance per pool = sum of unspent notes. Show "syncing" with progress while syncing. Show the last sync time. Never show a stale balance as final |
| **Send** | Input a Veil address, amount, optional note. Coin-select; merge first if needed (tell the user "combining balances"). Prove in a Web Worker with progress. Submit via relayer. Show the tx link. Every error maps to plain language (`NullifierAlreadySpent` → "This balance was already used. Refreshing…", then resync) |
| **Withdraw** | Public address (default: own EOA), amount. Warn: "the amount and recipient will be public". Submit via relayer |
| **Payment request link** | `https://<domain>/pay#to=<veil address>&amount=…&pool=…&ref=…`. The fragment never reaches a server (Gloam `paymentRequest.ts`). Opening it pre-fills Send |
| **Payroll** | Upload a CSV with columns `name,veil_address_or_email,amount,note`, choose a pool (default AUSD). Preview the total + fees and require balance ≥ total. Run rows **sequentially**: persist the row as `preparing` → build → persist pending → submit → `sent` (tx hash) → update the change note. Resume after reload by reconciling with `isSpent`. Rows without a Veil address get a **claim link**: generate a random 32-byte seed, pay to `VeilKeys.fromSeed(seed)`, link = `https://<domain>/claim#<seed hex>`. The claim page derives keys from the fragment, finds the note, and lets the person withdraw to any address (relayer fee taken from the note) or move it to their own Veil address. Export a results CSV (name, amount, status, tx). Optional: an "audit pack" that encrypts each row's note opening to the audit key |
| **Campaigns (founder)** | Create: rate per 1,000 impressions, per-post cap, holdback % (default 20), min lifetime (default 7 days), end date, X handle to require. Derive the admin EOA (index 100 + j) and refund key (200 + j); call `/gas-drip`. `factory.predict(admin, salt)` → fund by **withdrawing from the private balance to the predicted address** (relayed). Then `factory.create(config, salt)` from the admin EOA (`forwarder` = CRE simulation forwarder on testnet). Add KOLs: X user id (numeric; look it up via the X API in a server route) + KOL Veil address → `setKol(xUserId, pubKey, true)`. Dashboard: posts, impressions, paid, held, rejected (Envio). `close()` after end |
| **KOL view** | Paste the campaign link and post URL → extract the post id → `registerPost(postId, xUserId)`. This needs gas, so send it from the KOL's public EOA, or call it via a relayer meta-route `/register-post` that only forwards `registerPost` calls. Show live private earnings: the wallet scans `Payout` events for its pubKey and plain memos (§3.6). Show the rule: "Posts must include #ad and @<project>" |
| **Salary streams** | Admin creates a stream: payee Veil address, monthly amount → `ratePerSecond = monthly / 2,592,000`, start, end. A "Drip now" button plus a cron (relayer `setInterval` every 10 min) calling `drip(id)` on active streams |
| **Receipts** | From history: "Share receipt" creates JSON `{chainId, pool, index, commitment, amount, pubKey, blinding}` → base64url → link `https://<domain>/verify#<data>` |
| **Verify page** (no wallet needed) | Decode → recompute the commitment → fetch the commitment at `index` from Envio (fallback: RPC logs) → equal? Then show "This payment of X USDC to Veil address …abcd exists in the Veil pool, inserted at block N". Nothing else is revealed |
| **Transparency page** | From Envio: TVL per pool (token `balanceOf(pool)`), counts of commitments and nullifiers, campaigns, payouts. No addresses, no per-user data |
| **Settings** | Relayer on/off (off = submit from the public EOA with a warning), export the at-rest-encrypted backup, export the audit view key, sign out |

**Circuit artifacts in the browser:**
- Copy `transaction2x2.wasm` and `transaction2x2_final.zkey` into `apps/web/public/circuits/`.
- Load them with `loadArtifacts` (sha256 pinned).
- Run `snarkjs.groth16.fullProve` in a Web Worker.
- In `next.config`, set `webpack.resolve.fallback = { fs: false, path: false, crypto: false }` (snarkjs and circomlibjs import Node modules).
- The zkey is ~12 MB. Prefetch it after sign-in.

**Done when:** on testnet, a new user can sign up with a passkey, deposit, send privately to a second user (second browser profile), and that user sees the balance; payroll of 3 rows (one claim link) completes and survives a page reload mid-run; the receipt verifies on the verify page in a private window.

---

### Phase 7: MetaMask Agent Wallet plugin `@veil/mm-plugin` (Day 3)

Read first: `docs-offline/metamask-agent-wallet-full.txt` (sections "Build a plugin" and "Plugins" reference), `reference-repos/monagent/packages/plugin-monad/` (structure, `walletExecutor` usage) and `reference-repos/mm-plugin-perpl/README.md` (plugin's own guard, install gotchas, Monad testnet RPC workaround).

1. Start from `git clone https://github.com/MetaMask/agent-wallet-plugin-template`.
2. `package.json` must have:
   - the keyword `oclif-plugin`;
   - `@metamask/agent-wallet` as a **peerDependency** (`^7.0.0`);
   - an `oclif` block (`commands: ./dist/commands`, `bin: mm`, `topicSeparator: " "`);
   - a generated `oclif.manifest.json`;
   - **no** `oclif.hooks` and no `oclif.plugins`.
3. Manifest block (`targetChains` `[10143, 143]`):

| Command id | File | capabilities | dataAccess |
|---|---|---|---|
| `veil:setup` | `src/commands/veil/setup.ts` | `wallet-read`, `wallet-submit` | `accounts` |
| `veil:deposit` | `src/commands/veil/deposit.ts` | `wallet-read`, `wallet-submit` | `balances` |
| `veil:balance` | `src/commands/veil/balance.ts` | — | — |
| `veil:pay` | `src/commands/veil/pay.ts` | — | — |
| `veil:x402:fetch` | `src/commands/veil/x402/fetch.ts` | — | — |
| `veil:withdraw` | `src/commands/veil/withdraw.ts` | `wallet-read` | `accounts` |
| `veil:guard:set` / `veil:guard:get` | `src/commands/veil/guard/*.ts` | — | — |
| `veil:receipt` | `src/commands/veil/receipt.ts` | — | — |
| `veil:skill` | `src/commands/veil/skill.ts` | — | — (prints/installs SKILL.md) |

Keep the plugin-wide `capabilities` empty.

4. **Agent key storage** (`~/.veil/agent-<walletAddress>-<chainId>.json`, mode 0600):
   - **`setup`:** ask the wallet to sign a fixed EIP-712 message twice:
     - domain `{ name: "Veil", version: "1", chainId }`;
     - type `VeilAgentKey { string purpose; address wallet; }`;
     - message `{ purpose: "Derive my Veil agent key. Only sign this in the Veil plugin.", wallet }`.
     It uses `ctx.walletExecutor(io, "veil:setup")` with `kind: "typed-data"`. **If both signatures are equal** (deterministic signing), `seed = keccak256(signature)`; store only `{ mode: "derived" }` and re-derive on each run with one more signature. **If they differ**, generate a random 32-byte seed and store it encrypted with AES-GCM under `VEIL_PASSPHRASE` (env var; refuse to run without it). Print a warning to back it up (`mm veil receipt` / `mm veil setup --export`).
   - Print the agent's Veil address.
5. **Commands:**
   - **`deposit --amount 5 --pool USDC --chain-id 10143`:**
     1. Build the deposit proof locally.
     2. Send `approve` (exact) via `walletExecutor` (`kind: "transaction"`, `{to: token, data}`).
     3. Send `transact` via `walletExecutor`.
     MetaMask policy, simulation and 2FA apply to money **entering** the pool. Handle `[AWAITING_MFA]` (stop and tell the human).
   - **`pay --to veil:0x… --amount 1.5 [--pool USDC]`:** guard check → build transfer → `/relay` → print tx + receipt.
   - **`x402 fetch <url> [--method GET] [--body json] [--max 0.10]`:** §5.4 client. Refuse if the shielded entry's `amount + fee > --max` or the guard denies it. Print the response body.
   - **`withdraw --to 0x… --amount`:** guard check (withdrawals count toward the daily cap) → relay.
   - **`balance`:** sync (Envio) and list per pool.
   - **`guard set --per-payment 1 --daily 10 --allow veil:0x… --expires 2026-10-31`** and **`guard get`:** a policy file `~/.veil/guard-<wallet>.json`. Keep a spend log with reserve → settle/release, like Gloam `mcp/src/spendGuard.ts`. Rolling 24 h window. **No guard file = no spending allowed** (fail closed).
6. Every command supports `--json` (inherited) and returns machine-readable results. Use `CommandError(code, message, hint)` for failures.
7. **README must say plainly:** "Private payments are submitted by the Veil relayer, so MetaMask's outflow policy doesn't see them. The plugin enforces its own caps (guard). Deposits go through MetaMask policy."
8. `skills/veil-payments/SKILL.md` for agents:
   - always run `balance` and `guard get` first;
   - confirm with the human before `pay` or `withdraw` above $1;
   - never retry a failed payment blindly (check `balance` first);
   - stop on `[AWAITING_MFA]`;
   - never print seeds.
9. **Install and test:**

```bash
npm run build
rm -rf node_modules/@metamask/agent-wallet && ln -s "$(npm root -g)/@metamask/agent-wallet" node_modules/@metamask/agent-wallet
mm config set experimentalPlugins true
mm config set experimentalAllowUnverifiedInstalls true
mm plugins install "file:$PWD" --accept-permissions
mm veil setup --chain-id 10143
```

   **Testnet writes through `mm` fail with "Invalid chainId"** unless Monad testnet is declared in `~/.metamask/wallets.json` → `data.customEvmChains` with RPC `https://testnet-rpc.monad.xyz` (see the Perpl README). If that doesn't work, test writes on **mainnet** with $1–2 and the caps from §16.
10. Publish to npm as `@<your-scope>/veil-mm-plugin`, or document the git install.

**Done when:** a terminal session shows `mm veil setup`, `deposit` (approved through MetaMask), `guard set`, then `x402 fetch` against the demo API returning 200, and `guard get` showing the reduced remaining cap. Record this for the demo video.

---

### Phase 8: Chainlink CRE workflow (Day 4)

Read first: `docs-offline/chainlink-cre-ts-full.txt`:
- "Part 1: Project Setup", "Part 2: Fetching Offchain Data" and "Part 4: Writing Onchain" (TS);
- "Using Secrets in Simulation";
- "Simulating Workflows";
- "Forwarder Directory";
- "Service quotas" (limits).

Requires Bun ≥ 1.2.21, CRE CLI ≥ 1.30.0 (Monad testnet) and `@chainlink/cre-sdk` ≥ 1.19.0.

**Limits per run** (design around these):
- 15 HTTP calls;
- 15 EVM reads;
- 5 secret fetches;
- 50 consensus calls;
- 10M gas per write;
- 5 minutes per run;
- cron no faster than every 30 s.

So: **one EVM read per vault** (`activePosts(0, 12)` returns ids, xUserIds and lastImpressions in one call), **one HTTP call per post** (≤ 12 posts per vault per run), **one report write per vault**.

1. `cre init` in `services/cre` → TypeScript, Hello World template, workflow name `veil-impressions`.
2. `config.staging.json`:

```json
{ "schedule": "0 */10 * * * *",
  "chainSelectorName": "monad-testnet",
  "gasLimit": "3000000",
  "vaults": ["0x<campaign vault>"],
  "requiredTag": "#ad",
  "requiredMention": "@yourproject",
  "xApiBase": "https://api.x.com/2" }
```

3. Secrets: `secrets.yaml` → `secretsNames: { X_BEARER_TOKEN: [X_BEARER_TOKEN_VALUE] }`. Put `X_BEARER_TOKEN_VALUE=…` in `.env` (simulation). Read it **inside the handler**: `runtime.getSecret({ id: "X_BEARER_TOKEN" }).result().value`. Secrets are blocked during handler registration.
4. `main.ts` structure (adapt names to the SDK version in the docs):

```ts
import { CronCapability, HTTPClient, EVMClient, handler, Runner, getNetwork, encodeCallMsg, bytesToHex, hexToBase64,
         LAST_FINALIZED_BLOCK_NUMBER, ConsensusAggregationByFields, median, type Runtime, type NodeRuntime } from "@chainlink/cre-sdk"
import { encodeAbiParameters, parseAbiParameters, encodeFunctionData, decodeFunctionResult, zeroAddress } from "viem"
import { StreamVaultAbi } from "../contracts/abi"   // ABI of StreamVault (activePosts, onReport)

type Config = { schedule: string; chainSelectorName: string; gasLimit: string; vaults: string[];
                requiredTag: string; requiredMention: string; xApiBase: string }

const initWorkflow = (config: Config) => [handler(new CronCapability().trigger({ schedule: config.schedule }), onCron)]

const onCron = (runtime: Runtime<Config>) => {
  const net = getNetwork({ chainFamily: "evm", chainSelectorName: runtime.config.chainSelectorName })
  if (!net) throw new Error("unknown chain")
  const evm = new EVMClient(net.chainSelector.selector)
  const token = runtime.getSecret({ id: "X_BEARER_TOKEN" }).result().value
  for (const vault of runtime.config.vaults) {
    // 1 EVM read
    const res = evm.callContract(runtime, { call: encodeCallMsg({ from: zeroAddress, to: vault as `0x${string}`,
      data: encodeFunctionData({ abi: StreamVaultAbi, functionName: "activePosts", args: [0n, 12n] }) }),
      blockNumber: LAST_FINALIZED_BLOCK_NUMBER }).result()
    const [ids, users] = decodeFunctionResult({ abi: StreamVaultAbi, functionName: "activePosts", data: bytesToHex(res.data) }) as [bigint[], bigint[], bigint[]]
    if (ids.length === 0) continue
    const imps: bigint[] = [], valid: boolean[] = []
    for (let i = 0; i < ids.length; i++) {
      // 1 HTTP call per post, median across nodes; valid encoded as 0/1 so median = majority
      const r = runtime.runInNodeMode(
        (nr: NodeRuntime<Config>) => fetchPost(nr, token, ids[i], users[i]),
        ConsensusAggregationByFields<{ impressions: number; valid: number }>({ impressions: median<number>(), valid: median<number>() })
      )().result()
      imps.push(BigInt(Math.floor(r.impressions))); valid.push(r.valid >= 1)
    }
    const payload = encodeAbiParameters(parseAbiParameters("uint256[] ids, uint64[] imps, bool[] valid"), [ids, imps, valid])
    const report = runtime.report({ encodedPayload: hexToBase64(payload), encoderName: "evm", signingAlgo: "ecdsa", hashingAlgo: "keccak256" }).result()
    evm.writeReport(runtime, { receiver: vault, report, gasConfig: { gasLimit: runtime.config.gasLimit } }).result()
  }
  return "ok"
}

function fetchPost(nr: NodeRuntime<Config>, token: string, id: bigint, xUserId: bigint) {
  const http = new HTTPClient()
  const resp = http.sendRequest(nr, { method: "GET",
    url: `${nr.config.xApiBase}/tweets/${id}?tweet.fields=public_metrics,author_id,text`,
    headers: { Authorization: `Bearer ${token}` } }).result()
  if (resp.statusCode !== 200) return { impressions: 0, valid: 0 }          // deleted or not found → invalid
  const j = JSON.parse(new TextDecoder().decode(resp.body))
  if (!j.data) return { impressions: 0, valid: 0 }
  const text = String(j.data.text ?? "").toLowerCase()
  const ok = String(j.data.author_id) === xUserId.toString()
    && text.includes(nr.config.requiredTag.toLowerCase())
    && text.includes(nr.config.requiredMention.toLowerCase())
  return { impressions: Number(j.data.public_metrics?.impression_count ?? 0), valid: ok ? 1 : 0 }
}

export async function main() { const runner = await Runner.newRunner<Config>(); await runner.run(initWorkflow) }
```

   **Check against the docs:**
   - the exact header field shape in `sendRequest`;
   - whether `secret.value` is the right property;
   - the `ConsensusAggregationByFields` and `median` import names;
   - how `runInNodeMode` passes extra arguments (if closures over `token` aren't allowed, fetch the secret inside node mode, still ≤ 5 secret calls total).

   If a 404 for a deleted post makes `sendRequest` throw, catch it and return `valid: 0`.
5. **Simulation that writes on-chain:**
   1. Deploy the campaign with `forwarder = 0xB9F79d863261869B234c481D1f9A7af84AeAd192` (testnet MockKeystoneForwarder).
   2. Run `cre workflow simulate veil-impressions --target staging-settings --broadcast` (needs `CRE_ETH_PRIVATE_KEY` funded with testnet MON).
   3. The report lands through the mock forwarder in `StreamVault.onReport`. Confirm the `Report` and `Payout` events on the explorer.
6. **If Early Access is granted:** deploy the workflow (`cre workflow deploy`), and create a new campaign with `forwarder = 0xF8344CFd5c43616a4366C34E3EEE75af79a74482` (testnet) or `0x76c9…5E62` (mainnet). The vault's forwarder can't be changed after creation (by design).
7. **Demo fallback** if the X API is unavailable: set `xApiBase` to a mock endpoint in `apps/demo-api` (`/mock-x/tweets/:id`) that returns the same JSON shape. **Label it clearly** in the demo ("mock X API for the recording"). Never present mock data as real.

**Done when:** one simulation with `--broadcast` produces `Report` + `Payout` events on testnet for a real (or clearly labelled mock) post, and the KOL's wallet shows the new private balance.

---

### Phase 9: Cleanverse verified mode (Day 4, if on schedule)

- Already in the kit:
  - `VerifiedVeilPool` (overrides `_beforeDeposit` and `_beforeWithdraw` to require `cvi.isVerified(addr)`);
  - `ICviOracle`;
  - `MockCviOracle` (attester sets expiry per wallet).
- **Adapter for real Cleanverse attestations** (only if sandbox access arrives):
  - write `CleanverseCviAdapter is ICviOracle`, which stores attestations submitted with an EIP-712 signature from Cleanverse's attester key and returns `isVerified = valid && !revoked && now < expiry`;
  - pattern: `reference-repos/trustflow/contracts/src/oracles/CleanverseAttestationAdapter.sol`. Don't copy it; follow the idea.
- App:
  - a "Verified pool" toggle on Deposit;
  - if the wallet isn't verified, show "Get verified with Cleanverse A-Pass" (link) and, on testnet, a "demo attest" button that calls a server route signing `attest(wallet, now + 30 days)` with the attester key.
- Write-up: "Every coin in the verified pool entered from a verified identity and can only leave to one. Transfers inside stay private. Enforcement is in the contract, not the UI."

**Done when:** an unverified wallet's deposit reverts with `NotVerified(address)`; after attestation it succeeds; a withdrawal to an unverified address reverts.

---

### Phase 10: Aurora fund-from-any-chain (Day 5, if on schedule)

1. `GET https://intents-api.aurora.dev/api/tokens/{apiKey}` → `tokens[]` with `assetId`, `blockchain`, `symbol`, `decimals`. Cache it for a few minutes. Never build asset ids by hand. Destination: the entry with `blockchain: "monad"` and `symbol: "USDC"` (currently `nep245:v2_1.omni.hot.tg:143_2dmLwYWkCQKyTjeUPAsGJuiVLbFx`). Rate limits: 100 requests per 10 s and 2,000 per hour per key; poll status every 5–10 s, not faster.
2. Quote:

```js
const res = await fetch(`https://intents-api.aurora.dev/api/quote/${AURORA_KEY}`, { method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ dry: false, confidentiality: "advanced", swapType: "EXACT_INPUT", amount: "<atomic origin units>",
    originAsset, destinationAsset, depositType: "ORIGIN_CHAIN", recipient: "<user's Monad public EOA>",
    recipientType: "DESTINATION_CHAIN", refundTo: "<user's origin address>", refundType: "ORIGIN_CHAIN",
    slippageTolerance: 100, deadline: new Date(Date.now() + 10 * 60_000).toISOString() }) })
const { quote } = await res.json()   // quote.depositAddress, amountOut, minAmountOut
```

3. Show the deposit address, QR and amount. The user sends from any wallet on the origin chain.
4. Optionally `POST /api/deposit/submit/{apiKey}` with the origin tx hash to speed up detection. Poll `GET /api/status/{apiKey}?depositAddress=…` every 5–10 s until `SUCCESS`, `REFUNDED` or `FAILED`.
5. On `SUCCESS`, show "Funds arrived on Monad" and a one-click **Shield now** (Deposit flow with the received amount).
6. Explain in the UI: "Confidential mode hides where the money came from. Shielding hides where it goes next."

**Done when:** a small real swap (e.g. 2 USDC from Base) arrives on the Monad EOA and gets shielded; screenshot both steps for the write-up.

---

### Phase 11: Nansen screening (optional, only if everything else is green)

- In the relayer, for every withdrawal recipient: call `POST https://api.nansen.ai/api/v1/profiler/address/counterparties` paid via x402 (`@x402/fetch` with the relayer's Monad USDC wallet).
- Refuse when counterparties include labels you configure as high-risk (e.g. sanctioned or exploiter labels — inspect real responses first).
- Cache per address for 24 h. Never block on a Nansen outage: fall back to the OFAC list only, and log it.
- Note: label endpoints aren't available via x402.

---

### Phase 12: ERC-8004 registration (Day 5, 30 min)

- Register the demo API ("Veil Quote API") and each demo agent in the Identity Registry `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`. Use the agent0 SDK or direct calls; check the Monad ERC-8004 guide.
- Put the agent's Veil address in its registration metadata so agents can pay it privately.
- Optional: after a paid x402 call, the agent leaves feedback in the Reputation Registry `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`.

---

### Phase 13: Mainnet capped beta (Day 5)

1. Deploy the same contracts to **143** with `maxDepositAmount = 100_000_000` ($100) per transaction.
2. Deploy pools for USDC and AUSD. The real AUSD freezes; disclose it.
3. Set relayer `MIN_FEE` (e.g. 20,000 = $0.02) and fund the relayer with ~2 MON.
4. Add chain 143 to Envio, the SDK `NETWORKS` and the app network switch (default: testnet for judges; mainnet behind a toggle with a "beta, capped" label).
5. Do one real deposit → transfer → withdraw of $1 and save the tx links.
6. **Never raise caps during the hackathon.** If something looks wrong, `setDepositsPaused(true)`. Withdrawals keep working.

---

### Phase 14: Docs, demo, submission (Day 5)

1. `README.md`:
   - what Veil is;
   - live links (app, demo API, relayer status, verify page, Envio GraphQL);
   - contract addresses (testnet + mainnet);
   - how to run locally;
   - a "What's live / what's not" table;
   - the sponsor integration list (one paragraph each, naming exact files);
   - **Prior art and dependencies** (Gloam design reference, Tornado Nova, circomlib, snarkjs, Mera, x402, CRE, Envio, OpenZeppelin).
2. `docs/PRIVACY-MODEL.md` (§15 content), `docs/THREAT-MODEL.md` (§12 table plus trust assumptions: dev ceremony, relayer can censor but not steal, issuer freeze, X API trust in CRE).
3. Demo video (≤ 3 min) following §17.
4. Submission form: Track 04, every bounty from §2 that is built, repo link, demo link, video.

---

## 7. Detailed requirements that apply everywhere

### 7.1 Error codes → user messages

| Revert / code | Message |
|---|---|
| `UnknownRoot` | "Your wallet is out of date. Syncing and retrying…" (resync, rebuild, retry once) |
| `NullifierAlreadySpent` | "This balance was already used. Refreshing your balance." |
| `InvalidProof` / `BadExtDataHash` / `BadPublicAmount` | "Something went wrong building this payment. Nothing was sent." (log details) |
| `DepositTooLarge` | "The beta limit is $X per deposit." |
| `DepositsArePaused` | "Deposits are paused. You can still send and withdraw." |
| `NotVerified` | "This pool is for verified identities only." |
| Relayer `screened` | "This address can't receive funds through Veil." |
| Relayer offline | "Private sending is temporarily unavailable. Try again in a minute." |
| `PRF_UNAVAILABLE` | "This passkey provider doesn't support Veil. Use iCloud Keychain, Google Password Manager or 1Password." |

### 7.2 Things that are always public (show these in the UI where relevant)

- Deposit amounts and depositor address.
- Withdrawal amounts and recipient.
- `depositTo` recipient pubKey and amount (StreamVault payouts, drips, refunds).
- Campaign rates and per-post payouts.
- That a shielded transaction happened, and when.

### 7.3 Agent guard (plugin)

- **Policy:** `{ perPayment, daily, allowedRecipients[] (empty = any), expiresAt, pools[] }`.
- **Spend log:** `{ id, ts, amount, fee, to, status: reserved|settled|released, txHash }`.
- **Check order:**
  1. Not expired.
  2. The pool is allowed.
  3. `amount + fee ≤ perPayment`.
  4. Recipient allowed (if the list is non-empty).
  5. `sum(reserved + settled in the last 24 h) + amount + fee ≤ daily`.
  6. Reserve → submit → settle, or release on failure.
- Use a file lock (Gloam `mcp/src/fileLock.ts` idea) so parallel agent runs can't overspend.

---

## 8. Day plan (Oct 8–12)

| Day | Date | Phases | Done when |
|---|---|---|---|
| 1 | Wed 8 Oct | 0, 1, 2, start 3 | **Testnet smoke test green** (deposit → transfer → withdraw on Monad testnet) |
| 2 | Thu 9 Oct | 3, 4, 5.1–5.3, start 6 (onboarding, deposit, send) | Two browser users exchange a private payment on testnet; Envio sync works |
| 3 | Fri 10 Oct | 5.4 (x402), 7 (mm plugin), 6 (withdraw, receipts, verify) | `mm veil x402 fetch` gets 200 from the demo API |
| 4 | Sat 11 Oct | 6 (payroll, campaigns, KOL, streams), 8 (CRE), 9 (Cleanverse) | CRE simulation pays a KOL on testnet; payroll of 3 rows works |
| 5 | Sun 12 Oct | 10 (Aurora), 12, 13 (mainnet), 14 (docs, video, **submit**) | Submitted; links work in a private window |
| — | Mon 13 Oct | Buffer only: fixes, no features | — |

**Cut order if behind:**
1. Nansen.
2. Aurora.
3. Salary streams UI.
4. Cleanverse.
5. Mainnet (stay on testnet; the mm demo then needs `customEvmChains`).
6. Payroll claim links.

**Never cut:** Forge tests, e2e suite, Envio sync, plugin guard, honest README.

---

## 9. Tests that must stay green (CI)

Add a GitHub Actions workflow running on every push:
1. `cd contracts && forge test`
2. `cd circuits && bash scripts/setup.sh` (cache the ptau), then `e2e`: start anvil, `node e2e.mjs`, `node circuit-negative.mjs`
3. `pnpm --filter @veil/sdk test`
4. Lint and typecheck for every package.

If CI is too slow because of the ceremony, commit `circuits/build/*_final.zkey` via Git LFS or a release asset, and skip setup in CI. **Never commit the ptau.**

---

## 10. Known gotchas (each one cost someone hours)

| Gotcha | Fix |
|---|---|
| Hermez/zkevm ptau links return 403 | Use the PSE ppot URL in §5 |
| `snarkjs zkey contribute` hangs forever | Always pass `-e="<random hex>"` |
| Proof verifies in JS but `InvalidProof` on-chain | pi_b coordinates must be swapped (`[[b01,b00],[b11,b10]]`); public input order must be §3.4 |
| `BadExtDataHash` | `abi.encode` of the struct as a **tuple** (viem `encodeAbiParameters([{type:"tuple", components:[…]}], [ext])`), then `% p`. Field order exactly as §3.5 |
| Local root ≠ on-chain root | Leaves out of order or missing; both outputs of a `transact` are inserted in order (output 0 then 1); `depositTo` inserts one |
| `eth_getLogs` errors on Monad | RPCs cap ranges at 100–1,000 blocks; chunk by 100, or use Envio |
| Transactions cost more than expected | Monad charges the gas **limit**; send `estimate × 1.15` |
| `PRF_UNAVAILABLE` on desktop Chrome | Locally saved Chrome passkeys lack PRF. Use Google Password Manager, iCloud Keychain or 1Password; demo on Safari or iOS |
| Accounts "disappear" after a domain change | Passkeys are bound to `rpId`. Fix the domain on Day 0 |
| mm plugin: "window.addEventListener is not a function" | Two copies of `@metamask/agent-wallet`; symlink the global one into `node_modules` |
| mm testnet writes stuck on "Submitting…" | MetaMask's RPC proxy rejects 10143; declare `customEvmChains` or use mainnet |
| CRE `getSecret` fails | Only call it inside a trigger handler |
| CRE simulation consensus looks trivial | Simulation runs one node; real BFT consensus happens only when deployed |
| CRE write reverts with `NotForwarder` | The vault's `forwarder` must be the simulation forwarder when simulating, the production one when deployed |
| Envio Cloud deploy rejected | `envio` version must be exact (no `^`) |
| Next.js build fails on snarkjs | webpack fallback `fs: false, path: false, crypto: false`; run proving in a Web Worker |
| JSON serialization of amounts | bigint → decimal strings everywhere (API bodies, localStorage) |
| Payroll double-pays after reload | Persist pending state before submit; reconcile with `isSpent` on resume |
| AUSD/USDC frozen by issuer | Can't be fixed in code. Separate pools, caps, disclosure |
| Relayer nonce collisions | One process, one in-memory queue, retry once on nonce errors |

---

## 11. Lessons from Gloam's audits (with the test that proves we avoided each)

| Gloam finding | Our protection | Test |
|---|---|---|
| H-P1/C1: client-supplied commitment at deposit → pool drained | Deposits only via proof (`publicAmount` computed on-chain) or `depositTo` (commitment computed on-chain) | e2e "TS extDataHash == Solidity", `BadPublicAmount` test, `depositTo` note opens in TS |
| H1: cross-asset swap broke solvency | One pool per asset, no swaps | Balance invariant fuzz test |
| Kensho C2: field overflow | `Num2Bits(128)` on all amounts | `circuit-negative.mjs` 2^128 and field-wrap cases |
| Relayer could redirect funds | `extDataHash` binds recipient, relayer, fee and memos | e2e tamper tests (`BadExtDataHash`, `InvalidProof`) |
| Bearer notes: payer could spend back (x402 "sweep") | Key-owned notes | e2e "A cannot prove a spend of B's note" |
| M-1: plaintext secrets in localStorage | At-rest key from Mera index 3 | Manual check: localStorage holds only ciphertext |
| L-1: memo event revealed sender | Memos inside pool events; relayer is `msg.sender` | Look at the event on the explorer |
| M-4: reversible protections / admin withdraw | No admin withdraw; verifier immutable; two-step owner; pause only stops deposits | Forge test: withdrawals work while paused |
| F-2: issuer freeze | Disclosure + caps + separate pools | README |
| Stale-root rejections under load | Permanent `knownRoots` | e2e "proof against an older root still lands" |

---

## 12. Threat model summary (put in `docs/THREAT-MODEL.md`)

| Actor | Can | Cannot |
|---|---|---|
| Relayer | Refuse or delay transactions; see IPs and timing | Change recipient, amount or fee; spend notes |
| Envio indexer | Serve wrong or missing data (wallet detects it via `isKnownRoot`) | Spend or forge notes |
| Pool owner | Pause deposits; change the deposit cap | Move funds; change the verifier; block withdrawals |
| CRE / X API | Misreport impressions (bounded by caps per post and campaign) | Pay a non-allowlisted KOL; exceed the budget |
| Token issuer (USDC/AUSD) | Freeze the pool's balance | — |
| Dev ceremony participants | Forge proofs if all contributors colluded (disclosed: dev ceremony) | — |
| Public observer | See deposits, withdrawals, `depositTo` payouts, timing | Link deposits to withdrawals or private transfers; see private amounts |

---

## 13. Repository files to create early

- `.env.example`: `DEPLOYER_PK=`, `RELAYER_PK=`, `MONAD_TESTNET_RPC=https://testnet-rpc.monad.xyz`, `MONAD_RPC=https://rpc.monad.xyz`, `X_BEARER_TOKEN=`, `CRE_ETH_PRIVATE_KEY=`, `NEXT_PUBLIC_RELAYER_URL=`, `NEXT_PUBLIC_ENVIO_URL=`, `NEXT_PUBLIC_AURORA_KEY=`, `VEIL_PASSPHRASE=`, `CVI_ATTESTER_PK=`
- `deployments/testnet.json`, `deployments/mainnet.json` (§Phase 2)
- `docs/NOTES.md`: a running log of tx hashes, deviations from this file and decisions

---

## 14. Definition of done (whole project)

- [ ] Every "Done when" in Phases 1–8 passes; 9–12 if built.
- [ ] CI green.
- [ ] Testnet: deposit, private send, withdraw, payroll, receipt verify, x402 via mm plugin, CRE payout. All demonstrated with tx links in `docs/NOTES.md`.
- [ ] Mainnet capped beta: one real $1 round trip.
- [ ] README with live links, addresses, honest status, prior art.
- [ ] Demo video ≤ 3 min.
- [ ] Submitted on 12 Oct.

---

## 15. Privacy model (put in `docs/PRIVACY-MODEL.md` and the write-up)

- **Hidden:**
  - who paid whom inside the pool;
  - private transfer amounts;
  - links between deposits and withdrawals;
  - a KOL's or employee's total earnings across campaigns and where they cash out;
  - an agent's spending history.
- **Public:**
  - deposit and withdrawal amounts and addresses;
  - `depositTo` payouts (StreamVault) and campaign rates;
  - timing;
  - the existence of shielded transactions.
- **Privacy is only as strong as the anonymity set.** Advise users:
  - wait before withdrawing;
  - withdraw round amounts;
  - use fresh withdrawal addresses.
- **No operator can see your payments.** Proofs are made on your device. The relayer only sees an already-proven transaction.
- **Disclosure is opt-in:** a receipt reveals one note; the audit view key reveals incoming notes to whoever holds it.
- **Dev trusted setup:** fine for a testnet/beta, not for production.

---

## 16. Mainnet beta limits

| Setting | Value |
|---|---|
| `maxDepositAmount` per pool | 100 USDC / 100 AUSD (`100_000_000`) |
| Total exposure target | ≤ $500 across pools |
| Relayer MON balance | ~2 MON (top up as needed) |
| Campaign budgets | ≤ $50 |
| Pause procedure | `setDepositsPaused(true)` from the owner key; withdrawals keep working |

---

## 17. Demo script (≤ 3 min)

1. **0:00** The problem: an explorer view of a public payroll wallet. "Privacy that needs an operator isn't private."
2. **0:20** Face ID → Veil account. The Accounts panel: one passkey → public wallet, private account, audit key, two agents, campaigns (Mera ×2).
3. **0:40** Fund from Base via Aurora (confidential) → Shield. Say what's hidden at each step.
4. **1:00** Payroll: CSV of 5 payees in Lagos and Nairobi, in AUSD. The explorer shows only shielded transactions (Agora).
5. **1:30** Terminal: Claude Code + `mm veil x402 fetch` buys an API call in ~2 s. Show `guard get`, then verify the merchant's receipt (MetaMask, x402).
6. **2:10** Campaign: KOL post with #ad → CRE simulation report → the KOL's private balance increases. The treasury is never visible (CRE).
7. **2:40** Transparency page (Envio). Verified pool (Cleanverse). Close: "No operator. Proofs on your device. Settled in one Monad block."

---

## 18. Sources

**Monad:**
- docs.monad.xyz: guides/mera, guides/x402, tooling-and-infra/privacy, tooling-and-infra/agentic-payments, developer-essentials/differences, developer-essentials/opcode-pricing, reference/rpc-differences, guides/erc-8004
- monad.xyz/blog/privacy-comes-to-monad-with-unlink

**Unlink:** docs.unlink.xyz (trust-model, supported-chains)

**MetaMask:** docs.metamask.io/llms-agent-wallet-full.txt (offline copy included), github.com/MetaMask/agent-wallet-plugin-template

**Chainlink CRE:** docs.chain.link/cre/llms-full-ts.txt (offline copy included)

**Envio:** docs.envio.dev/llms-full.txt (offline copy included)

**Aurora:** docs.intents.aurora.dev/llms-full.txt (offline copy included)

**x402:** github.com/coinbase/x402 `specs/x402-specification-v2.md`, `specs/transports-v2/http.md`

**Nansen:** docs.nansen.ai/getting-started/agentic-payments/x402-payments

**AUSD risk:** governance.aave.com/t/agora-usd-ausd-on-aave-monad-assessments/25251

**Prior art:**
- github.com/cryptoduke01/gloam (snapshot included; MIT packages; reference only)
- Tornado Nova (2-in/2-out design)
- github.com/0xbow-io/privacy-pools-core (Apache-2.0)

**Earlier research in our repo:** `RESEARCH.md`, `SPONSORS.md` (same folder as this file).
