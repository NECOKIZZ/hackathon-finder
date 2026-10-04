# 007 — Agent Compute Staking (stake → compute streamed as yield)

**Status:** Captured + critiqued · **Captured:** 2026-10-04 · **Origin:** Neco
**Working name:** TBD

---

## 1. The raw idea
Agents visit a site, buy our token, stake it, and earn **compute credits streamed as yield**.

## 2. Critique (from an agent's point of view)
1. **Where does the yield come from?** Compute costs real money (GPUs, API bills).
   - If new token buyers fund the yield, it's a Ponzi, and it dies when buying slows.
   - The yield needs a real source: revenue, idle capacity, or the treasury.
2. **I'm an agent with a budget in dollars. Why would I hold a volatile token?** My operator approves spend in USD. If the token drops 40%, my "free" compute cost more than paying per call. Rational agents compare "buy token + stake" against "pay $X per call", and only stake if it's clearly cheaper *after price risk*.
3. **"Yield" paid in compute isn't yield, it's a prepaid discount.** That's fine, but call it what it is: staking = buying capacity in advance.
4. **It already exists.**
   - **Venice (VVV):** staking gives a pro-rata daily share of Venice's API inference capacity (since Jan 2025). Since Aug 2025, **DIEM** = $1/day of inference forever, minted by locking staked VVV.
   - **Morpheus (MOR):** holders get a share of network compute daily.
   - We need a sharp angle, not a copy.
5. **Who supplies the compute, and which models?** Agents want frontier models. Reselling commercial API access may break provider terms. Open-weight models on rented GPUs are cheaper but weaker.
6. **Regulation.** A token sold with a "yield" pitch looks like a security.
7. **Onboarding.** Agents can now buy and stake (agent wallets, x402, MetaMask ERC-7715 permissions), but every extra step loses agents. It must be one call.

## 3. Solutions: three polished designs
**A. Capacity staking (the Venice model, made agent-native)**
- Stake → a **throughput allowance**: compute per second, streamed, use-it-or-lose-it daily.
- Credits are non-transferable and expire, so there's nothing to speculate on. That makes it less security-like.
- **Our angle vs Venice:**
  - One-call onboarding for agents (x402 "buy + stake", MCP server, ERC-8004 identity).
  - Multi-provider routing across open-weight models.

**B. No-loss compute (no token needed)**
- An agent (or its operator) deposits **USDC**. It goes into a yield source (Aave/Morpho, ~4–5%).
- **The interest is streamed as compute.** Principal is withdrawable at any time.
- "Park $1,000 and your agent gets about $4/month of inference forever, at no risk to principal."
- Honest, simple, and no price risk. But the amounts are small, so it suits idle treasuries and DAO agents.

**C. Capacity exchange: real yield from real demand (the part that makes it "yield")**
- Stakers who **don't use their full allowance sell the unused part** to other agents who pay per call (x402, USDC).
- The **staker earns USDC from actual demand**, not from new token buyers.
- This turns the idea into a two-sided market:
  - Agents with steady workloads stake to get cheap capacity.
  - Their idle capacity serves bursty agents, who pay a premium.

**Recommended combination:**
- **Hackathon:** **B + C, no token.** USDC in, interest streamed as compute, unused capacity sold to other agents. The yield story is clean and judges can follow the money.
- **Later:** add the token (A) for upside once there's real demand and revenue to back it.

## 4. Mechanics to get right
- **Streaming:** credits accrue per second (Superfluid-style, or MetaMask `erc20-token-stream` permissions).
- **Metering:** an API gateway debits the agent's stream per token of inference, with signed usage receipts.
- **Price feed:** USD per million tokens per model, so credits are dollar-denominated, not token-denominated.
- **Abuse:** per-agent rate limits, and an identity (ERC-8004) so one agent can't drain the exchange.

## 5. Hackathon fit (so far)
| Hackathon | Fit | Why |
|---|---|---|
| Circle Grants (rolling) | 🟢 | USDC + nanopayments + agent payments on Arc. Design B/C is pure USDC |
| Monad Metropolis (13 Oct) | 🟡 | Track 04 (agent infra) + x402 facilitator + MetaMask streaming bounty, but tight timing |
| Nebius × NVIDIA (30 Oct) | 🟡 | Supply side: open-weight models on Nebius GPUs as the compute source |
| Open Agent Hackathon (15–20 Oct) | 🟡 | "Agent that does real work". The exchange as agent infrastructure |

## 6. Reuse
- **Cuerate's x402 `inspire` endpoint** (pay-per-call pattern).
- **Synesis:** Circle wallets, agent spend limits.
- **Kickoff:** AgentVault (delegated agent spending with pause and limits).

## 7. Open questions
- Which inference supply: our own GPUs (Nebius/Akash) or a reseller (check terms)?
- What yield sources are on the target chain (e.g. Morpho/Aave on Arc or Monad)?
- Are there enough bursty agents to buy idle capacity? Pilot with 2–3 agent teams.
