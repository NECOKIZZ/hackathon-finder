# Batch 2 — Hackathon Report (13 listings)

**Researched:** 2026-10-04. "Verified" means checked on the official page or rules myself.

---

## 1. Filtering

| Listing | Out because | Notes |
|---|---|---|
| ETH Lagos 2026 (Web3Bridge) | **On-site** (Lagos, 8–10 Oct) | |
| HackMeridian (Stellar) | **On-site** (Lisbon) | |
| TUM Blockchain & AI | **On-site** (Munich, 30–31 Oct) | |
| ETHGlobal Mumbai | **On-site** (Mumbai, 5–7 Nov) | |
| From Vision to Impact: Web3 for Social Good (SMU) | **On-site final** + **prize "Pending"** | Submissions close 25 Oct; shortlisted teams present in person at SMU Singapore on 26 Nov. Verified |
| Mezo Buildathon Wave 1 | **Not open yet** (16 Oct) + **low prize** ($7k in MEZO tokens over 2 waves) | |
| Portaldot Hacker House | **Not open yet** (kickoff 14 Oct) + **low prize** ($5.2k) | |
| Event Contracts Hackathon | **Couldn't verify it exists** | Not found on dev.events or by search |
| MDBA Youth Blockchain Hackathon | **Youth-only** + prize unknown | Run with the same organisers as BLI (Maryland Blockchain Association). Closes 31 Oct |
| TapeOut Genesis Transistor (X Layer) | **Weak fit** (kept in §3 for reference) | Not chip design: "processors" and "transistors" are TapeOut's names for a **token-issuance launchpad** on X Layer. Mainnet token launch required |

**Survivors:** Circle Grants, BLI Legal Tech Hackathon 2, QIE Hackathon 3.0 (+ TapeOut for reference).

---

## 2. Ranking

| # | Opportunity | Deadline | Money | Competition | Best idea fit | Verdict |
|---|---|---|---|---|---|---|
| **1** | **Circle Grants** | Rolling | **Up to $100k USDC**, milestone-based | Grant review, not a contest | **Synesis** (as it is) · Cuerate · `.arc` · 001 KOL Streams on Arc | 🟢🟢 Best value per hour: your Arc projects already match what Circle asks for |
| **2** | **BLI Legal Tech Hackathon 2** | **~1 Nov** (DoraHacks timer) | $20k headline, but **"prize pool still developing"**; "$10k+ in bounties, support and promotion" | **Very low:** 433 registered, 8 teams, **1 submission so far** | Kickoff (prediction markets) · 004 Proof of Funds (regtech) · 003 ETF League (RWA) | 🟢 Low competition makes up for the uncertain prize. Reuse an existing or planned project rather than a new build |
| **3** | **QIE Hackathon 3.0** | **30 Nov** | $17k, but 1st place is $5k; category winners $500; **half paid only after 3 traction milestones over 90 days** | Unknown | `.arc` → identity on QIE · Cuerate · Archer (EVM ports) | 🟡 Cheap to enter (EVM, so redeploy), but rewards real users and traction, not demos |
| — | TapeOut (X Layer) | October | $14k (8k/4k/2k) | Unknown | 003 ETF League's ticket token, at a stretch | 🔴 It's a token launchpad. Mainnet issuance, trading-abuse clauses, and little in common with our ideas |

---

## 3. The hosts

### Circle Grants (Circle)
- **Who:** issuer of USDC; builder of **Arc**, its stablecoin-native L1 (USDC as gas; mainnet live since 16 Sep 2026).
- **Programme:**
  - Relaunched in May 2026 as **milestone-driven grants, up to $100k in USDC**, plus technical guidance, co-marketing and mentorship.
  - Applications go through Questbook (circle.questbook.app).
- **What they look for:**
  - "**Arc is core to your flow of value, liquidity or settlement**."
  - Circle products as "meaningful building blocks": USDC, Wallets, CCTP, Nanopayments, Gateway.
  - Projects that "expand USDC utility and make the Arc ecosystem stronger".
- **Our fit:**
  - **Synesis** is almost a model application: Arc + Circle user-controlled and developer-controlled wallets + App Kit + CCTP + USDC as gas, with an AI agent on top.
  - **Cuerate**: nanopayments, x402, Circle wallets, open-source royalty contract.
  - **`.arc` names**: infrastructure for the whole ecosystem.
- **What to do:** one application for **Synesis**, with milestones such as (1) Arc mainnet launch, (2) agent skills v4, (3) N monthly active users / volume. Pair it with the **Arc Microgrants** submission (14 Oct, see the October mapping) as early proof of traction.

### BLI Legal Tech Hackathon 2 (Blockchain Legal Institute)
- **Who:** the Blockchain Legal Institute, a legal-education and advocacy group, running this with the Maryland Blockchain Association.
  - Last year: 320 hackers, **91 projects**.
  - Bounty partners included Constellation Network, Internet Computer and Story.
  - Awards ceremony at Capitol Technology University, Maryland.
- **This year (verified on DoraHacks):**
  - Virtual. One "All BUIDLs" track. Deadline per the DoraHacks timer ~1 Nov 2026 (listed as 31 Oct elsewhere).
  - 2 bounties (details not public).
  - Git repo and video **not mandatory**.
  - Themes:
    - **RWA:** tokenization of real estate, carbon, art, agriculture.
    - **LegalTech & RegTech:** data privacy for minors, **KYC / on-chain legal docs**, legal automation.
    - **AI x Blockchain:** autonomous agents, **prediction markets**, hybrid AI.
    - **Web3 for Social Good:** DID, community voting, anti-corruption.
    - **GameFi & NFT.**
    - **Green Tech.**
- **The catch:** "Prize pool is still developing … may be subject to withdrawal or change." Treat $20k as a ceiling, not a promise. The prizes partly include promotion, law-firm mentoring and investor pitching.
- **Our fit (low-effort reuse):**
  - **Kickoff**, framed as *AI agents + prediction markets*: live, multi-agent, with real settlement.
  - **004 Zcash Proof of Funds**, framed as *privacy-preserving KYC / proof of funds* (visas, compliance). Only once it exists for Zecathon. Check whether Zecathon allows submitting the same project to other hackathons; nothing says it doesn't.
  - **003 ETF League / 002 Busha for Stocks**, framed as *RWA + compliance*, after BNB Hack.
- **What to do:** submit whatever we've built by then. With one submission so far, a polished entry stands out.

### QIE Hackathon 3.0 (QIE Blockchain)
- **Who:** QIE, an **EVM-compatible L1** that calls itself a "global transaction and identity layer".
  - Products: QIE Wallet, **QIEDEX** (DEX), **QIE Pass** (reusable KYC'd identity, "a KYC-verified Google sign-in for Web3").
  - Claims 360+ live dApps.
  - Runs **four hackathons a year**.
- **This edition (verified):**
  - **Mainnet only.** Build window 1 Aug – 30 Nov; demo week 1–5 Dec; winners 10 Dec.
  - **Theme:** "Build the company, not the demo".
  - **Tracks:** DeFi & financial infra · AI + autonomous agents · consumer & social · commerce & real world · developer tooling.
  - **Prizes:** 1st $5k, 2nd $3k, 3rd $2k; category winners $500 each; specials: Most Traction $2.5k, Community Choice $1k, Best Student Team $1k.
  - **Payout model:** **50% at award, 50% after 3 traction milestones in 90 days** (wallets, volume, recurring users, merchants, revenue).
- **Our fit:**
  - Porting EVM contracts is cheap: `.arc` name service → names on QIE, integrated with **QIE Pass**; Cuerate royalties; Archer.
  - But winning means **real users on QIE**, which is effort beyond the build.
- **What to do:** low priority. Only port something if it can get real users there (e.g. a names service tied to QIE Pass).

### TapeOut / Ignix (X Layer), for reference
- **What it is:** Ignix × Metagents launchpad on OKX's X Layer (chain 196).
  - You deploy a "processor" through the TapeOut factory, set "transistor" supply and price, and get at least one "circuit" made with it. In plain terms: you issue an asset with set supply and pricing, and products are built on it.
  - The winning design becomes the "Ignix Genesis Transistor".
  - Judged on innovation, ecosystem integration, asset-issuance design, contract security and growth.
  - Mainnet required. Wash trading disqualifies.
- **Why skip:** it's a token launch competition. Reputational and regulatory risk is high, and it doesn't match our strengths.

---

## 4. Recommendation
1. **This week:** draft the **Circle Grant application for Synesis** (biggest money, no deadline pressure, existing work counts).
2. **By ~1 Nov:** submit **one** project to **BLI**. Whichever of Kickoff / Proof of Funds / ETF League is most polished by then. Very low competition.
3. **Skip** QIE unless we want a long-term presence on that chain. **Skip** TapeOut.

## Sources
- [BLI Legal Tech Hackathon 2 (DoraHacks)](https://dorahacks.io/hackathon/legal-hack-2026/detail)
- [Previous BLI × MDBA hackathon recap](https://internshala.com/competitions/mdba-youth-blockchain-hackathon/)
- [QIE Hackathon 3.0](https://hackathon.qie.digital)
- [QIE 2026 hackathon announcement](https://www.theblock.co/press-releases/qie-blockchain-announces-2026-hackathon-for-builders-ready-to-launch-real-web3-projects-394120)
- [QIE identity layer explainer](https://bingx.com/pl-pl/learn/article/what-is-qie-blockchain-qie-web3-identity-layer-how-does-it-work)
- [Circle Developer Grants](https://www.circle.com/grant)
- [Circle grants relaunch (Arc community)](https://community.arc.io/home/blogs/circle-developer-grants-program-relaunches-2026-05-14)
- [First 2026 Circle grant recipients](https://circle.com/blog/announcing-the-first-circle-grant-recipients-in-2026)
- [Web3 for Social Good (DoraHacks)](https://dorahacks.io/hackathon/web3-social-good-2026/detail)
- [TapeOut Hackathon (Ignix)](https://ignix.bot/x_campaign)
- [dev.events online Web3 hackathons](https://dev.events/hackathons/ON/web3)
