"""Landscape how-to videos for YouTube "Trade Like an Institution" (Roland, 17 Oct 2026).

1920x1080, same engine as viral.py (Kobo host, word captions, animated cards), no stock UI screenshots:
platform steps are shown as clean step cards, keycaps and our own chart drawn from CoinGecko data.

    python howto.py tradingview            -> assets/reels/howto-tradingview.mp4
    python howto.py tradingview 3 40 90    -> preview PNGs
Voice: ElevenLabs Oluwadamilare (VzScgb5Pi0A6lafMNQpm), script in queue/howto/<name>.txt;
pull + transcribe with viral_pull.py howto-<name> <voice_url>.
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import viral  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BRAND = "<div class='brand'>Trade Like an <b>Institution</b></div>"


def keys(*ks):
    return "".join(f"<span style='display:inline-block;font:800 54px Jakarta;color:#07080B;background:#FFD84D;border-radius:16px;"
                   f"padding:8px 26px;margin:0 10px 0 0;box-shadow:0 8px 0 #B89400'>{k}</span>" for k in ks)


def step(n, title, body, keycaps=None):
    k = f"<div style='margin-top:34px'>{keys(*keycaps)}</div>" if keycaps else ""
    return (f"<div class='kick'>Step {n} of 6</div><div class='mid' style='font-size:76px'>{title}</div>"
            f"<div class='sm' style='margin-top:22px;font-size:40px'>{body}</div>{k}")


def ema(vals, n):
    k, out, e = 2 / (n + 1), [], vals[0]
    for v in vals:
        e = v * k + e * (1 - k)
        out.append(e)
    return out


def chart(candles, show_ema=False, levels=None, alert=False, w=1180, h=460):
    cs = candles[-90:]
    closes = [c[4] for c in candles]
    em = ema(closes, 50)[-90:]
    lo, hi = min(c[3] for c in cs), max(c[2] for c in cs)
    pad = (hi - lo) * .08
    lo, hi = lo - pad, hi + pad
    y = lambda v: h - (v - lo) / (hi - lo) * h  # noqa: E731
    cw = (w - 40) / len(cs)
    out = []
    for i, (_, o, hh, ll, cl) in enumerate(cs):
        x = 10 + i * cw + cw / 2
        col = "#3DDC97" if cl >= o else "#FF4D4D"
        out.append(f"<line x1='{x:.1f}' x2='{x:.1f}' y1='{y(hh):.1f}' y2='{y(ll):.1f}' stroke='{col}' stroke-width='2'/>")
        top, bot = y(max(o, cl)), y(min(o, cl))
        out.append(f"<rect x='{x - cw * .35:.1f}' y='{top:.1f}' width='{cw * .7:.1f}' height='{max(bot - top, 1.5):.1f}' fill='{col}'/>")
    if show_ema:
        pts = " ".join(f"{10 + i * cw + cw / 2:.1f},{y(v):.1f}" for i, v in enumerate(em))
        out.append(f"<polyline points='{pts}' fill='none' stroke='#5AA9FF' stroke-width='4'/>")
        out.append(f"<text x='{w - 330}' y='{y(em[-1]) + 36:.1f}' font-size='26' font-weight='800' fill='#5AA9FF' font-family='Jakarta'>EMA 50</text>")
    for v, lab in (levels or []):
        yy = y(v)
        out.append(f"<line x1='0' x2='{w}' y1='{yy:.1f}' y2='{yy:.1f}' stroke='#FFD84D' stroke-width='3' stroke-dasharray='14 8'/>")
        out.append(f"<text x='{w - 10}' y='{yy - 12:.1f}' text-anchor='end' font-size='28' font-weight='800' fill='#FFD84D' font-family='Jakarta'>{lab}</text>")
    if alert and levels:
        yy = y(levels[0][0])
        out.append(f"<text x='{w - 330}' y='{yy + 12:.1f}' font-size='44' font-family='Jakarta'>🔔</text>")
    return f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}'>{''.join(out)}</svg>"


def market():
    files = sorted((ROOT / "research").glob("market-*.json"))
    m = json.loads(files[-1].read_text())
    btc = next(c for c in m["coins"] if c["symbol"] == "BTC")
    return btc


def money(x):
    return f"${x:,.0f}"


def tradingview_spec():
    btc = market()
    cs = btc["candles"]
    recent = cs[-42:]  # ~7 days of 4h candles
    hi, lo = max(c[2] for c in recent), min(c[3] for c in recent)
    lv = [(hi, f"7-day high {money(hi)}"), (lo, f"7-day low {money(lo)}")]

    def chart_card(title, **kw):
        return f"<div class='kick'>BTC / USDT · 4H · our chart, CoinGecko data</div><div class='mid' style='font-size:52px;margin-bottom:18px'>{title}</div>{chart(cs, **kw)}"

    def timeline(at, dur):
        s = [at("step", nth=k) for k in range(1, 7)]
        t_rec = at("that's", s[5] + 2)
        t_rem = at("remember", t_rec)
        t_slash = at("slash", s[3])
        t_rsi = at("r", t_slash) if False else s[3] + (s[4] - s[3]) * .55
        t_alt = at("alt", s[4])
        bg = viral.ROOT / "assets" / "market" / "bg-land.jpg"
        if not bg.exists():
            from PIL import Image, ImageDraw
            im = Image.new("RGB", (2040, 1200), "#07080B")
            dr = ImageDraw.Draw(im)
            for yy in range(1200):
                v = int(7 + 16 * (1 - abs(yy - 450) / 900))
                dr.line([(0, yy), (2040, yy)], fill=(v, v + 2, v + 10))
            for x in range(0, 2040, 60):
                dr.line([(x, 0), (x, 1200)], fill=(22, 26, 36))
            for yy in range(0, 1200, 60):
                dr.line([(0, yy), (2040, yy)], fill=(22, 26, 36))
            im.save(bg, quality=92)
        bgs = [(-1, dur + 1, bg)]
        H = "html"
        cards = [
            {"kind": H, "a": -1, "b": s[0] - .1, "html": "<div class='kick'>How to · Trading platforms</div>"
             "<div class='big yel' style='font-size:110px;letter-spacing:-3px'>Set up TradingView<br>like an institution</div>"
             "<div class='mid' style='margin-top:26px;font-size:54px'>Free · 6 steps · 2 minutes</div>"},
            {"kind": H, "a": s[0] - .1, "b": s[1] - .1, "html": step(1, "Create a free Basic account", "tradingview.com → Sign up.<br>"
             "Crypto prices are <b class='grn'>real-time</b> on the free plan.<br>Limits: <b>2 indicators per chart</b>, a few price alerts.")},
            {"kind": H, "a": s[1] - .1, "b": s[2] - .1, "html": step(2, "Pick the market", "Symbol search (top left) → type", ["BTCUSDT"])
             + "<div class='sm' style='margin-top:26px;font-size:36px'>Choose a big exchange: that's where the volume is.</div>"},
            {"kind": H, "a": s[2] - .1, "b": s[2] + (s[3] - s[2]) * .5, "html": step(3, "Pick your timeframe", "No menu needed. Type on your keyboard:", ["2", "4", "0", "Enter"])
             + "<div class='sm' style='margin-top:26px;font-size:36px'>240 minutes = the <b class='yel'>4-hour chart</b>. Check the daily first, then come down.</div>"},
            {"kind": H, "a": s[2] + (s[3] - s[2]) * .5, "b": s[3] - .1, "html": chart_card("Clean 4-hour chart")},
            {"kind": H, "a": s[3] - .1, "b": t_rsi, "html": step(4, "Add 2 indicators", "Open indicators:", ["/"])
             + "<div class='sm' style='margin-top:26px;font-size:40px'>1. <b style='color:#5AA9FF'>EMA</b>, length <b>50</b>: the trend<br>2. <b class='yel'>RSI</b>: is the move stretched?</div>"},
            {"kind": H, "a": t_rsi, "b": s[4] - .1, "html": chart_card("Trend: EMA 50", show_ema=True)},
            {"kind": H, "a": s[4] - .1, "b": t_alt + 2.5, "html": step(5, "Mark your levels", "Horizontal line:", ["Alt", "H"])
             + "<div class='sm' style='margin-top:26px;font-size:40px'>One at the recent <b class='grn'>high</b>, one at the recent <b class='red'>low</b>.<br>That's where big orders sit.</div>"},
            {"kind": H, "a": t_alt + 2.5, "b": s[5] - .1, "html": chart_card("Your levels", show_ema=True, levels=lv)},
            {"kind": H, "a": s[5] - .1, "b": s[5] + (t_rec - s[5]) * .45, "html": step(6, "Let the chart call you", "Set an alert at your level:", ["Alt", "A"])},
            {"kind": H, "a": s[5] + (t_rec - s[5]) * .45, "b": t_rec - .1, "html": chart_card("Alert set: stop staring at the screen", show_ema=True, levels=lv, alert=True)},
            {"kind": "checks", "a": t_rec - .1, "b": t_rem - .1, "kick": "Your setup", "title": "Clean chart, clear plan",
             "items": [{"t": "1 market · 1 timeframe", "d": .4}, {"t": "2 indicators · 2 levels", "d": 1.4}, {"t": "1 alert", "d": 2.4}]},
            {"kind": H, "a": t_rem - .1, "b": dur + 1, "html": "<div class='kick'>Read this first</div><div class='mid'>Scenarios, <span class='yel'>not certainties.</span></div>"
             "<div class='sm' style='margin-top:20px;font-size:40px'>Always know where your idea is wrong.<br>Education, not financial advice.</div>"
             "<div class='mid' style='margin-top:40px;font-size:56px'>Subscribe for the daily market read</div>"},
        ]
        return bgs, cards

    s = viral.std("howto-tradingview", timeline, {"TradingView.": "TradingView", "Kubo": "Kobo"})
    s.update({"land": True, "brand": BRAND})
    return s


SPECS = {"tradingview": tradingview_spec}

if __name__ == "__main__":
    name = sys.argv[1]
    pv = [float(x) for x in sys.argv[2:]]
    out = ROOT / "assets" / "reels" / f"howto-{name}.mp4"
    print(asyncio.run(viral.render(SPECS[name](), out, pv or None)))
