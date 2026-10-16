"""Daily Market Read Short (YouTube crypto channel "Trade Like an Institution", Roland 16 Oct 2026).

Scenario analysis only: levels, "if / then", and where the idea is invalid. Never "buy/sell", never leverage.

    python market_short.py script [date]       -> queue/market/<date>/script.txt (voiceover text) + plan.json
    python market_short.py render [date] [secs...] -> assets/reels/market-<date>.mp4 (or preview PNGs)

Voice: ElevenLabs "Jon - Catalyst" (dSByRdUbTGloB7TFA1qD), worldwide audience. Pull + transcribe with
viral_pull.py market-<date> <voice_url>, which writes assets/viral/market-<date>/voice.json.
"""
import asyncio
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import viral  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
VOICE_ID = "dSByRdUbTGloB7TFA1qD"


def money(x):
    if x >= 100:
        return f"${x:,.0f}"
    if x >= 1:
        return f"${x:,.2f}".rstrip("0").rstrip(".")
    return f"${x:.4g}"


def load(date):
    return json.loads((ROOT / "research" / f"market-{date}.json").read_text())


def scenario(c, short=False):
    t, g, inv = money(c["trigger"]), money(c["target"]), money(c["invalid"]) if c["invalid"] else None
    if c["bias"] == "bullish":
        return f"If it closes above {t}, the next level to watch is {g}. If it loses {inv}, the idea is wrong."
    if c["bias"] == "bearish":
        return f"If it breaks below {t}, the next support is near {g}. Back above {inv}, and the idea is wrong."
    return f"It's stuck between {money(c['lo7'])} and {money(c['hi7'])}. Wait for a close outside that range."


TREND = {"bullish": "bullish", "bearish": "bearish", "range": "sideways"}


def fund_line(c):
    f = (c.get("futures") or {}).get("funding_avg_pct")
    if f is None:
        return ""
    if f >= 0.03:
        return " Funding is running hot, so longs are crowded. Careful."
    if f <= -0.01:
        return " Funding is negative, so shorts are paying longs. Watch for a squeeze."
    return ""


def build_script(date):
    m = load(date)
    d = dt.date.fromisoformat(date)
    gl = m["global"]
    chg = gl["mcap_chg24"]
    coins = {c["symbol"]: c for c in m["coins"]}
    picks = [coins[s] for s in m["picks"][:3]]
    btc = m["btc"]
    parts = [f"Hey, Kobo here. Your daily crypto market read for {d.strftime('%B')} {d.day}.",
             f"The total market is {'up' if chg >= 0 else 'down'} {abs(chg):.1f} percent today, and Bitcoin dominance is {gl['btc_dom']:.0f} percent.",
             f"Bitcoin first. It's at {money(btc['price'])}, and the four-hour trend is {TREND[btc['bias']]}. {scenario(btc)}"]
    for c in picks:
        parts.append(f"Next, {c['name']}. It's at {money(c['price'])}, trend {TREND[c['bias']]}, RSI {c['rsi']:.0f}. {scenario(c)}{fund_line(c)}")
    parts.append("These are scenarios, not signals. Education, not financial advice. Follow, and I'll check these levels tomorrow.")
    text = " ".join(parts)
    out = ROOT / "queue" / "market" / date
    out.mkdir(parents=True, exist_ok=True)
    (out / "script.txt").write_text(text)
    (out / "plan.json").write_text(json.dumps({"date": date, "voice_id": VOICE_ID, "coins": ["BTC"] + [c["symbol"] for c in picks]}, indent=1))
    return text


def chart_svg(c, w=840, h=640):
    cs = c["candles"]
    lv = [c["trigger"], c["target"]] + ([c["invalid"]] if c["invalid"] else [])
    lo = min(min(k[3] for k in cs), *lv)
    hi = max(max(k[2] for k in cs), *lv)
    pad = (hi - lo) * 0.06
    lo, hi = lo - pad, hi + pad
    y = lambda v: h - (v - lo) / (hi - lo) * h  # noqa: E731
    cw = (w - 150) / len(cs)
    body = []
    for i, (_, o, hh, ll, cl_) in enumerate(cs):
        x = 10 + i * cw + cw / 2
        col = "#3DDC97" if cl_ >= o else "#FF4D4D"
        body.append(f"<line x1='{x:.1f}' x2='{x:.1f}' y1='{y(hh):.1f}' y2='{y(ll):.1f}' stroke='{col}' stroke-width='2'/>")
        top, bot = y(max(o, cl_)), y(min(o, cl_))
        body.append(f"<rect x='{x - cw * .35:.1f}' y='{top:.1f}' width='{cw * .7:.1f}' height='{max(bot - top, 1.5):.1f}' fill='{col}' rx='1'/>")
    if c["bias"] == "range":
        lines = [(c["hi7"], "#FFD84D", "Range top"), (c["lo7"], "#FFD84D", "Range bottom")]
    else:
        lines = [(c["trigger"], "#FFD84D", "Trigger"), (c["target"], "#3DDC97", "Next level"), (c["invalid"], "#FF4D4D", "Invalid")]
    for v, col, lab in lines:
        if v is None:
            continue
        yy = y(v)
        body.append(f"<line x1='0' x2='{w - 140}' y1='{yy:.1f}' y2='{yy:.1f}' stroke='{col}' stroke-width='3' stroke-dasharray='12 8'/>")
        body.append(f"<rect x='{w - 138}' y='{yy - 26:.1f}' width='138' height='52' rx='12' fill='{col}'/>")
        body.append(f"<text x='{w - 69}' y='{yy - 2:.1f}' text-anchor='middle' font-size='19' font-weight='800' fill='#07080B' font-family='Jakarta'>{lab}</text>")
        body.append(f"<text x='{w - 69}' y='{yy + 19:.1f}' text-anchor='middle' font-size='19' font-weight='700' fill='#07080B' font-family='Jakarta'>{money(v)}</text>")
    py = y(c["price"])
    body.append(f"<circle cx='{10 + (len(cs) - .5) * cw:.1f}' cy='{py:.1f}' r='9' fill='#fff'/>")
    return f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}'>{''.join(body)}</svg>"


def coin_card(c):
    tag = {"bullish": ("BULLISH SETUP", "grn"), "bearish": ("BEARISH SETUP", "red"), "range": ("RANGE", "yel")}[c["bias"]]
    ch = c.get("chg24") or 0
    fut = c.get("futures") or {}
    f = fut.get("funding_avg_pct")
    stats = [f"RSI {c['rsi']:.0f}", f"24h {'+' if ch >= 0 else ''}{ch:.1f}%"]
    if f is not None:
        stats.append(f"Funding {f:+.3f}%")
    return ("<div class='kick'>4H chart · 30 days · CoinGecko</div>"
            f"<div style='display:flex;justify-content:space-between;align-items:baseline'><div class='mid'>{c['symbol']} <span class='sm'>{c['name']}</span></div>"
            f"<div class='mid'>{money(c['price'])}</div></div>"
            f"<div class='{tag[1]}' style='font:800 34px Jakarta;letter-spacing:2px;margin:10px 0 18px'>{tag[0]}</div>"
            f"{chart_svg(c)}"
            f"<div class='sm' style='margin-top:18px;display:flex;gap:28px'>{''.join(f'<span>{s}</span>' for s in stats)}</div>")


def bg_image():
    p = ROOT / "assets" / "market" / "bg.jpg"
    if not p.exists():
        from PIL import Image, ImageDraw
        p.parent.mkdir(parents=True, exist_ok=True)
        im = Image.new("RGB", (1200, 2040), "#07080B")
        dr = ImageDraw.Draw(im)
        for yy in range(2040):
            v = int(7 + 18 * (1 - abs(yy - 700) / 1400))
            dr.line([(0, yy), (1200, yy)], fill=(v, v + 2, v + 10))
        for x in range(0, 1200, 60):
            dr.line([(x, 0), (x, 2040)], fill=(22, 26, 36))
        for yy in range(0, 2040, 60):
            dr.line([(0, yy), (1200, yy)], fill=(22, 26, 36))
        im.save(p, quality=92)
    return p


def spec(date):
    m = load(date)
    plan = json.loads((ROOT / "queue" / "market" / date / "plan.json").read_text())
    coins = {c["symbol"]: c for c in m["coins"]}
    gl = m["global"]
    d = dt.date.fromisoformat(date)
    name = f"market-{date}"

    def timeline(at, dur):
        t_btc = at("bitcoin", nth=2)
        starts = [t_btc]
        after = t_btc + 1
        for _ in plan["coins"][1:]:
            s = at("next", after)
            starts.append(s)
            after = s + 1
        t_end = at("scenarios", after)
        bg = bg_image()
        bgs = [(-1, dur + 1, bg)]
        chg = gl["mcap_chg24"]
        cards = [{"kind": "html", "a": -1, "b": t_btc - .1,
                  "html": f"<div class='kick'>{d.strftime('%a %d %b %Y')}</div><div class='big yel' style='font-size:118px'>DAILY<br>MARKET READ</div>"
                          f"<div class='sm' style='margin-top:30px'>Total market <b class='{'grn' if chg >= 0 else 'red'}'>{'+' if chg >= 0 else ''}{chg:.1f}%</b> · "
                          f"BTC dominance <b>{gl['btc_dom']:.0f}%</b></div>"
                          "<div class='sm' style='margin-top:14px'>Scenarios, not signals.</div>"}]
        for i, sym in enumerate(plan["coins"]):
            b = starts[i + 1] if i + 1 < len(starts) else t_end
            cards.append({"kind": "html", "a": starts[i] - .1, "b": b - .1, "html": coin_card(coins[sym])})
        cards.append({"kind": "html", "a": t_end - .1, "b": dur + 1,
                      "html": "<div class='kick'>Read this first</div><div class='mid'>Scenarios, <span class='yel'>not signals.</span></div>"
                              "<div class='sm' style='margin-top:20px'>Education, not financial advice. Crypto is volatile: size small, always know where you're wrong.</div>"
                              "<div class='mid' style='margin-top:40px;font-size:52px'>Follow for tomorrow's read</div>"})
        return bgs, cards

    s = viral.std(name, timeline, {"Bitcoin": "Bitcoin", "Cobo": "Kobo"})
    return s


if __name__ == "__main__":
    cmd = sys.argv[1]
    date = sys.argv[2] if len(sys.argv) > 2 else dt.datetime.utcnow().date().isoformat()
    if cmd == "script":
        print(build_script(date))
    else:
        pv = [float(x) for x in sys.argv[3:]]
        out = ROOT / "assets" / "reels" / f"market-{date}.mp4"
        print(asyncio.run(viral.render(spec(date), out, pv or None)))
