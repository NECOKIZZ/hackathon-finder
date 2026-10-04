"""Log tokenized-stock prices across DEX pools, to measure weekend price gaps.

Stdlib only. Each run appends one row per pool to data/spreads/YYYY-MM-DD.csv.
Prices come from the DexScreener public API (no key needed).
"""
import csv
import json
import os
import time
import urllib.request
from datetime import datetime, timezone

# Same stock, several issuers: xStocks (x), Ondo (on), Binance bStocks (B).
SYMBOLS = [
    "TSLAx", "NVDAx", "AAPLx", "SPYx", "QQQx",
    "TSLAon", "NVDAon", "AAPLon", "SPYon", "QQQon",
    "TSLAB", "NVDAB", "AAPLB",
]
MIN_LIQUIDITY_USD = 1_000
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "spreads")
FIELDS = ["ts_utc", "us_market_open", "symbol", "chain", "dex", "pair",
          "quote", "price_usd", "liquidity_usd", "volume_24h_usd"]


def us_market_open(now):
    # Regular session 09:30-16:00 New York. Approximated in UTC for daylight time
    # (13:30-20:00); holidays ignored. Good enough to split weekend from weekday.
    if now.weekday() >= 5:
        return False
    minutes = now.hour * 60 + now.minute
    return 13 * 60 + 30 <= minutes < 20 * 60


def fetch(symbol):
    url = f"https://api.dexscreener.com/latest/dex/search?q={symbol}"
    req = urllib.request.Request(url, headers={"User-Agent": "spread-logger/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp).get("pairs") or []


def main():
    now = datetime.now(timezone.utc).replace(microsecond=0)
    is_open = us_market_open(now)
    rows = []
    for symbol in SYMBOLS:
        try:
            pairs = fetch(symbol)
        except Exception as exc:  # one bad symbol shouldn't kill the run
            print(f"{symbol}: fetch failed: {exc}")
            continue
        for p in pairs:
            if p["baseToken"]["symbol"].lower() != symbol.lower():
                continue
            liquidity = (p.get("liquidity") or {}).get("usd") or 0
            if liquidity < MIN_LIQUIDITY_USD or not p.get("priceUsd"):
                continue
            rows.append({
                "ts_utc": now.isoformat(),
                "us_market_open": int(is_open),
                "symbol": symbol,
                "chain": p["chainId"],
                "dex": p["dexId"],
                "pair": p["pairAddress"],
                "quote": p["quoteToken"]["symbol"],
                "price_usd": p["priceUsd"],
                "liquidity_usd": round(liquidity),
                "volume_24h_usd": round((p.get("volume") or {}).get("h24") or 0),
            })
        time.sleep(0.5)  # stay well under the API rate limit

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{now.date().isoformat()}.csv")
    new_file = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerows(rows)
    print(f"{now.isoformat()} market_open={is_open} wrote {len(rows)} rows to {path}")


if __name__ == "__main__":
    main()
