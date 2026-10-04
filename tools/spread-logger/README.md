# Weekend spread logger

Records prices of the same stock tokens across DEX pools so we can measure how far they drift apart while US markets are closed, and how fast the gaps close.

- **Runs on GitHub Actions** (`.github/workflows/spread-logger.yml`). No Claude credits used.
- **Schedule (UTC):**
  - Every 15 min from Friday 20:00 to Monday 13:45.
  - Every 2 hours on weekdays as a baseline.
  - About 1,400 Actions minutes a month; private repos get 2,000 free.
- **Output:** `data/spreads/YYYY-MM-DD.csv`, one row per pool per run. Columns: time, market open flag, symbol, chain, DEX, pair, quote, USD price, liquidity, 24h volume.
- **Source:** DexScreener public API. DEX pools only (no centralized exchanges).
- **Stop it:** GitHub → Actions → "Weekend spread logger" → ⋯ → Disable workflow. Or delete the workflow file.
- **Run once by hand:** Actions → "Weekend spread logger" → Run workflow.
