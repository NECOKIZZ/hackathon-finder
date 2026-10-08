# Veil reference kit (verified)

Verified on 2026-10-08 with circom 2.2.2, snarkjs 0.7.5, circomlib 2.0.5, circomlibjs 0.1.7,
Foundry 1.5.1 (solc 0.8.24), Node 22, viem 2.57.

| Check | Result |
|---|---|
| `contracts`: `forge test` (StreamVault 11 + VerifiedVeilPool 2) | 13/13 pass |
| `sdk-test`: `node e2e.mjs` against anvil (deposit, private transfer + relayer fee, merge 2 notes, withdraw, depositTo, stale root, StreamVault payout spent by the KOL, tamper/replay/limits) | 31/31 pass |
| `sdk-test`: `node circuit-negative.mjs` (2^128 output, field wrap, unbalanced, same nullifier twice, fake input) | 6/6 pass |

## Run it

```bash
# 1. circuits (creates build/ with wasm, zkey, Verifier.sol; ~2 min)
cd circuits && npm i && bash scripts/setup.sh && cp build/Verifier.sol ../contracts/src/Verifier.sol && cd ..

# 2. contracts
cd contracts
forge install --no-git foundry-rs/forge-std OpenZeppelin/openzeppelin-contracts@v5.1.0   # if lib/ is missing
forge build && forge test && cd ..

# 3. end-to-end against a local chain
anvil --gas-limit 300000000 &          # separate terminal
cd sdk-test && npm i && node e2e.mjs && node circuit-negative.mjs
```

Measured gas (Ethereum pricing, anvil): `transact` ≈ 1.74–1.79M, `depositTo` ≈ 0.84M, StreamVault `onReport` (1 post) ≈ 0.99M.
On Monad add ≈ 0.9M per `transact` (ecPairing is 5× and ecMul 5× more expensive), so budget ≈ 2.7M and set
`gas = estimate × 1.15` (Monad charges the gas LIMIT, not gas used).

Proof time (Node, one core): ≈ 1.6 s per 2-in/2-out proof.
