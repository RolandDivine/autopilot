"""Daily market read data (Actions -> market). Public CoinGecko API, no key.

Writes research/market-<date>.json: market context, per-coin indicators from 4h candles (30 days),
futures positioning (funding, open interest) and a ranked list of scenario setups.
Education only: setups are "if / then / invalid below" scenarios, never instructions.
"""
import datetime as dt
import json
import os
import time
from pathlib import Path

import requests

API = "https://api.coingecko.com/api/v3"
ROOT = Path(__file__).resolve().parents[1]
STABLE = {"usdt", "usdc", "dai", "fdusd", "usde", "tusd", "usdd", "pyusd", "usds", "busd", "usd1", "rlusd", "susde", "usdtb", "bsc-usd", "usdf", "usdy"}
WRAPPED = ("wrapped", "staked", "bridged", "wbtc", "weth", "steth", "wsteth", "cbbtc", "lbtc", "weeth", "reth", "jitosol", "msol")


def get(path, **params):
    for a in range(6):
        r = requests.get(f"{API}/{path}", params=params, timeout=60, headers={"accept": "application/json"})
        if r.status_code == 429:
            time.sleep(20 + 10 * a)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"rate limited: {path}")


def ema(xs, n):
    k, out = 2 / (n + 1), []
    for x in xs:
        out.append(x if not out else out[-1] + k * (x - out[-1]))
    return out


def rsi(closes, n=14):
    gains = [max(b - a, 0) for a, b in zip(closes, closes[1:])]
    losses = [max(a - b, 0) for a, b in zip(closes, closes[1:])]
    ag, al = sum(gains[:n]) / n, sum(losses[:n]) / n
    for g, l in zip(gains[n:], losses[n:]):
        ag, al = (ag * (n - 1) + g) / n, (al * (n - 1) + l) / n
    return 100 if al == 0 else 100 - 100 / (1 + ag / al)


def atr(c, n=14):
    trs = [max(h - l, abs(h - pc), abs(l - pc)) for (_, _, h, l, _), (_, _, _, _, pc) in zip(c[1:], c[:-1])]
    return sum(trs[-n:]) / n


def rnd(x):
    return float(f"{x:.4g}") if x < 1000 else round(x, -1 if x < 10000 else -2)


def analyse(m, candles):
    closes = [k[4] for k in candles]
    price = m["current_price"]
    e20, e50 = ema(closes, 20)[-1], ema(closes, 50)[-1]
    r = rsi(closes)
    a = atr(candles)
    wk = candles[-42:]  # last 7 days of 4h candles
    hi7, lo7 = max(k[2] for k in wk), min(k[3] for k in wk)
    hi30, lo30 = max(k[2] for k in candles), min(k[3] for k in candles)
    score = 0
    if price > e20 > e50:
        score += 2
    elif price < e20 < e50:
        score -= 2
    elif price > e50:
        score += 1
    else:
        score -= 1
    if 55 <= r <= 70:
        score += 1
    elif 30 <= r <= 45:
        score -= 1
    near_hi = (hi7 - price) / price < 0.025
    near_lo = (price - lo7) / price < 0.025
    score += 1 if near_hi and score > 0 else 0
    score -= 1 if near_lo and score < 0 else 0
    vm = (m.get("total_volume") or 0) / max(m.get("market_cap") or 1, 1)
    bias = "bullish" if score >= 2 else "bearish" if score <= -2 else "range"
    if bias == "bullish":
        trigger, target, invalid = hi7, max(hi30, hi7 + 2 * a), min(e50, lo7)
        if target <= trigger * 1.01:
            target = trigger + 2 * a
    elif bias == "bearish":
        trigger, target, invalid = lo7, min(lo30, lo7 - 2 * a), max(e50, hi7)
        if target >= trigger * 0.99:
            target = trigger - 2 * a
    else:
        trigger, target, invalid = hi7, lo7, None
    return {"id": m["id"], "symbol": m["symbol"].upper(), "name": m["name"], "price": price,
            "chg24": m.get("price_change_percentage_24h_in_currency"), "chg7d": m.get("price_change_percentage_7d_in_currency"),
            "mcap_rank": m.get("market_cap_rank"), "vol_mcap": round(vm, 3),
            "ema20": rnd(e20), "ema50": rnd(e50), "rsi": round(r, 1), "atr": rnd(a),
            "hi7": rnd(hi7), "lo7": rnd(lo7), "hi30": rnd(hi30), "lo30": rnd(lo30),
            "bias": bias, "score": score, "trigger": rnd(trigger), "target": rnd(target),
            "invalid": rnd(invalid) if invalid else None,
            "candles": [[k[0], k[1], k[2], k[3], k[4]] for k in candles[-60:]]}


def futures():
    out = {}
    try:
        for t in get("derivatives"):
            if t.get("contract_type") != "perpetual" or not t.get("index_id"):
                continue
            s = t["index_id"].upper()
            d = out.setdefault(s, {"oi": 0.0, "fund": [], "venues": 0})
            d["oi"] += float(t.get("open_interest") or 0)
            if t.get("funding_rate") is not None:
                d["fund"].append(float(t["funding_rate"]))
            d["venues"] += 1
    except Exception as e:
        print("::warning title=derivatives::", e)
    return {s: {"open_interest_usd": round(d["oi"]), "funding_avg_pct": round(sum(d["fund"]) / len(d["fund"]), 4) if d["fund"] else None,
                "venues": d["venues"]} for s, d in out.items()}


def main():
    today = dt.datetime.utcnow().date().isoformat()
    g = get("global")["data"]
    mk = get("coins/markets", vs_currency="usd", order="market_cap_desc", per_page=80, page=1,
             price_change_percentage="24h,7d,30d")
    coins = [m for m in mk if m["symbol"].lower() not in STABLE and not any(w in m["id"] for w in WRAPPED)][:int(os.environ.get("N", "35"))]
    fut = futures()
    res = []
    for m in coins:
        try:
            c = get(f"coins/{m['id']}/ohlc", vs_currency="usd", days=30)
            if len(c) >= 60:
                a = analyse(m, c)
                a["futures"] = fut.get(a["symbol"])
                res.append(a)
        except Exception as e:
            print(f"::warning title={m['id']}::{e}")
        time.sleep(float(os.environ.get("SLEEP", "4")))
    btc = next((x for x in res if x["symbol"] == "BTC"), None)
    picks = sorted([x for x in res if x["symbol"] != "BTC" and x["bias"] != "range"],
                   key=lambda x: (abs(x["score"]), x["vol_mcap"]), reverse=True)[:4]
    out = {"date": today, "generated": dt.datetime.utcnow().isoformat(timespec="minutes") + "Z",
           "global": {"mcap_usd": g["total_market_cap"]["usd"], "mcap_chg24": g["market_cap_change_percentage_24h_usd"],
                      "btc_dom": g["market_cap_percentage"]["btc"]},
           "btc": btc, "picks": [p["symbol"] for p in picks], "coins": res,
           "note": "Scenarios for education, not financial advice."}
    p = ROOT / "research" / f"market-{today}.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(out, indent=1))
    print(f"::notice title=market read::BTC {btc and btc['bias']} | picks: {', '.join(out['picks'])} | coins analysed: {len(res)}")


if __name__ == "__main__":
    main()
