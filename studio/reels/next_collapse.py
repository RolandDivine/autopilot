"""'Are we closer to the next financial collapse?' Reel (7 Nov 2026). Roland's public opinion, not financial advice.
Same format as trump_swan (dark, serif-italic titles, avatar, captions, progress bar) plus a WARNING DASHBOARD of 15 lights.
Facts: reports/Next market crash warning patterns.md (FINRA, FactSet, CMG, CoinGecko, AP, Yahoo Finance, TFTC).
"""
import json
from pathlib import Path
from .kit import Y, GRN, RED, GREY, ln, lab, align
from .trump_swan import STYLE, ttl, txt, progress, WHITE

ROOT = Path(__file__).resolve().parents[2]
NAME = "next-collapse"
AMB, OFF = "#ffc83d", "#3a3a42"

B = [  # (sentence, scene or None, caption keywords, key colour)
    ("Are we closer to the next financial collapse than anyone wants to admit?", "hook", "financial collapse", RED),
    ("Before two thousand, two thousand eight, and twenty twenty, the same warning lights came on first.", "years", "warning lights", Y),
    ("I checked every one against today.", "dash", "today.", Y),
    ("Five are on.", None, "Five on.", RED),
    ("And there's one date nobody's watching.", None, "date nobody's watching.", Y),
    ("Light one.", "l1", "one.", RED),
    ("In two thousand, the ten biggest companies were a quarter of the market.", None, "ten biggest quarter", Y),
    ("Today, they're forty percent.", None, "forty percent.", RED),
    ("Light two.", "l2", "two.", RED),
    ("Borrowed money.", None, "Borrowed money.", RED),
    ("Traders owe nearly a record one and a half trillion dollars, and it's starting to roll over, just like before two thousand and two thousand seven.",
     None, "record trillion dollars, roll over,", Y),
    ("Light three.", "l3", "three.", RED),
    ("The riskiest companies' debt is cracking.", None, "riskiest debt cracking.", RED),
    ("That gap has only been this wide in two thousand, two thousand eight, twenty sixteen, and twenty twenty.", None, "only wide", Y),
    ("Light four.", "l4", "four.", RED),
    ("On November fifth, chip stocks fell twelve percent in one day.", None, "chip twelve percent one day.", RED),
    ("The Nasdaq's worst day since March twenty twenty.", None, "worst day", RED),
    ("Light five.", "l5", "five.", RED),
    ("Bitcoin is forty percent off its high, and the big funds are pulling money out.", None, "Bitcoin forty percent pulling money out.", RED),
    ("Then Democrats took both houses of Congress, and the market started pricing a threat to the AI boom.", "congress", "Congress, threat AI boom.", Y),
    ("But here's what's missing.", "missing", "missing.", Y),
    ("In every past crash, jobs broke and a big lender failed.", None, "jobs lender", Y),
    ("Neither has happened.", None, "Neither", Y),
    ("Yet.", None, "Yet.", RED),
    ("My view: this looks more like two thousand than two thousand eight.", "verdict", "view:", Y),
    ("And watch November thirtieth, when Trump Media's billion-dollar debt can come due.", None, "November thirtieth, billion-dollar debt", RED),
    ("Comment SIGNALS and I'll send you my crash watch list.", "cta", "SIGNALS", Y),
]

STATES = ["r"] * 5 + ["a"] * 7 + ["g"] * 3
COL = {"r": RED, "a": AMB, "g": OFF}


def dot(x, y, s, col, at, glow=True):
    sh = f"box-shadow:0 0 {s // 2}px {col};" if glow and col != OFF else ""
    return (f"<div data-in='{at:.2f}' style='position:absolute;left:{x - s / 2:.0f}px;top:{y - s / 2:.0f}px;width:{s}px;height:{s}px;"
            f"border-radius:50%;background:{col};{sh}opacity:0'></div>")


def board(cy, s, gap, lit, base_at=0.0, labels=False):
    """lit: {index: (state, at)} lights shown on; the rest are dark outlines."""
    out, w = "", 5 * s + 4 * gap
    for i in range(15):
        x = 540 - w / 2 + s / 2 + (i % 5) * (s + gap)
        y = cy + (i // 5 - 1) * (s + gap)
        out += (f"<div data-in='{base_at:.2f}' style='position:absolute;left:{x - s / 2:.0f}px;top:{y - s / 2:.0f}px;width:{s - 6}px;"
                f"height:{s - 6}px;border-radius:50%;border:3px solid #2c2c33;background:#141418;opacity:0'></div>")
        if i in lit:
            st, at = lit[i]
            out += dot(x, y, s, COL[st], at)
    if labels:
        for j, name in zip((12, 13, 14), ("JOBS", "BANKS", "DOLLAR")):
            x = 540 - w / 2 + s / 2 + (j % 5) * (s + gap)
            out += lab(x, cy + s + gap + s / 2 + 18, name, base_at + .4, GREY)
    return out


def strip(n_on, at_now):
    """Mini dashboard under the title: lights before n_on already red, light n_on turns red now."""
    lit = {i: ("r", 0) for i in range(n_on)}
    lit[n_on] = ("r", at_now)
    return board(440, 26, 12, lit)


def chip(x, y, s, at, c=WHITE, shake=False):
    sk = f" data-shake='{at:.2f}'" if shake else ""
    return (f"<div data-in='{at:.2f}'{sk} style='position:absolute;left:{x}px;top:{y}px;transform:translate(-50%,0);padding:12px 26px;"
            f"border:3px solid {c};border-radius:16px;font:800 46px Jakarta;color:{c};opacity:0'>{s}</div>")


def stamp(y, s, at, c=RED, size=84):
    return (f"<div class=big data-in='{at:.2f}' data-shake='{at:.2f}' style='left:540px;top:{y}px;color:{c};opacity:0;"
            f"font-size:{size}px;white-space:nowrap'>{s}</div>")


def scene_html(key, T):
    """T(word, after=0) -> time of that word relative to this scene's start."""
    if key == "hook":
        return (STYLE + "<div data-in='0' data-pulse='0.1' style='position:absolute;left:140px;top:520px;width:800px;height:800px;border-radius:50%;"
                "background:radial-gradient(circle,rgba(255,77,77,.22),transparent 65%);opacity:0'></div>"
                "<div class=ttl data-in='0' style='top:600px;font-size:92px;line-height:1.15;opacity:0'>Are we closer<br>to the next<br>"
                f"<i style='color:{RED};font-size:120px'>collapse?</i></div>")
    if key == "years":
        out = ttl(260, "The same", "warning lights")
        for i, (yr, w) in enumerate((("2000", "thousand,"), ("2008", "eight,"), ("2020", "twenty,"))):
            at = T(w) - .1
            out += chip(540, 560 + i * 190, yr, at, WHITE, True)
            out += "<svg>" + ln(f"M720 {600 + i * 190} l40 20 l30 -10 l40 50", at + .15, .4, RED, 6) + "</svg>"
        return out
    if key == "dash":
        five = T("Five")
        lit = {i: ("r", five + i * .12) for i in range(5)}
        return (ttl(260, "Today's", "dashboard") + board(760, 110, 56, lit)
                + stamp(1060, "5 OF 15 ON", five + .7)
                + f"<div class=sm data-in='{T('date') - .1:.2f}' style='left:540px;top:1170px;opacity:0;color:{Y}'>+ 1 date nobody's watching</div>")
    if key == "l1":
        t40 = T("forty")
        return (ttl(225, "Light", "one", c=RED) + strip(0, .3)
                + "<svg>" + ln("M360 1100 V940", T("quarter") - .2, .6, OFF, 150) + ln("M720 1100 V840", t40 - .2, .8, RED, 150) + "</svg>"
                + lab(360, 1120, "2000: 25%", T("quarter"), GREY) + lab(720, 1120, "NOW", t40, RED)
                + f"<div class=big data-in='{t40:.2f}' style='left:720px;top:700px;color:{RED};opacity:0' data-count='40' data-from='0' "
                  f"data-at='{t40:.2f}' data-d='1' data-pre='' data-suf='%'>0%</div>"
                + "<div class=sm data-in='.6' style='left:540px;top:530px;opacity:0'>Top 10 companies' share of the S&amp;P 500</div>")
    if key == "l2":
        tr = T("trillion")
        return (ttl(225, "Light", "two", c=RED) + strip(1, .3)
                + txt(540, 510, "BORROWED MONEY", T("Borrowed"), 60, WHITE)
                + f"<div class=big data-in='{tr - .6:.2f}' style='left:540px;top:600px;color:{Y};opacity:0;font-size:84px' data-count='1480000000000' "
                  f"data-from='0' data-at='{tr - .6:.2f}' data-d='1.4' data-pre='$' data-suf=''>$0</div>"
                + "<svg>" + ln("M200 1080 C400 1060 520 900 640 820 C700 790 760 800 860 900", T("roll") - .8, 1.2, Y, 8) + "</svg>"
                + stamp(860, "PEAK &amp; ROLL", T("roll") + .3, RED, 64) + chip(540, 1120, "2000 · 2007", T("seven.") - .6, GREY))
    if key == "l3":
        out = (ttl(225, "Light", "three", c=RED) + strip(2, .3) + txt(540, 510, "RISKIEST COMPANY DEBT", T("riskiest"), 56, WHITE)
               + lab(540, 590, "CCC bonds: 13%+ above US government bonds", T("cracking."), RED))
        for i, (yr, w) in enumerate((("2000", "thousand,"), ("2008", "eight,"), ("2016", "sixteen,"), ("2020", "twenty."))):
            out += chip(300 + (i % 2) * 480, 700 + (i // 2) * 150, yr, T(w, T("gap")) - .1, AMB)
        return out + chip(540, 1010, "2026?", T("twenty.", T("gap")) + .6, RED, True)
    if key == "l4":
        return (ttl(225, "Light", "four", c=RED) + strip(3, .3)
                + "<svg>" + ln("M160 1000 H940", 0, .3, "#2a2a30", 3)
                + "".join(ln(f"M{240 + i * 110} {720 - i * 10} V{790 - i * 10}", .2 + i * .1, .2, GRN, 34) for i in range(5))
                + ln("M790 680 V1000", T("twelve") - .3, .4, RED, 40) + "</svg>"
                + stamp(1060, "CHIPS −12% IN ONE DAY", T("twelve"), RED, 72)
                + f"<div class=sm data-in='{T('worst') - .1:.2f}' style='left:540px;top:1170px;opacity:0'>Nasdaq-100: worst day since March 2020</div>")
    if key == "l5":
        return (ttl(225, "Light", "five", c=RED) + strip(4, .3)
                + "<svg>" + ln("M180 600 C330 570 380 590 460 650 S640 820 900 860", .3, 1.6, RED, 8) + "</svg>"
                + txt(540, 510, "BITCOIN", .2, 56, WHITE)
                + stamp(930, "−40% FROM HIGH", T("forty") + .2, RED, 80)
                + lab(540, 1100, "−$440M LEFT US BITCOIN FUNDS IN 3 DAYS", T("pulling"), Y))
    if key == "congress":
        dome = ("M330 1000 H750 M360 1000 V900 M420 1000 V900 M480 1000 V900 M540 1000 V900 M600 1000 V900 M660 1000 V900 M720 1000 V900 "
                "M340 900 H740 M380 900 C380 760 700 760 700 900 M540 780 V720")
        return (ttl(250, "Both houses", "flip", c=Y) + "<svg>" + ln(dome, .1, 1.4, WHITE, 6) + "</svg>"
                + stamp(1080, "AI DATA CENTRES: PAUSED?", T("threat") - .1, Y, 64))
    if key == "missing":
        lit = {i: ("r", 0) for i in range(5)}
        lit.update({i: ("a", .3 + (i - 5) * .08) for i in range(5, 12)})
        return (ttl(250, "What's", "missing") + board(700, 110, 56, lit, labels=True)
                + f"<div class=ttl data-in='{T('Yet.') - .05:.2f}' data-shake='{T('Yet.'):.2f}' style='top:1070px;opacity:0'>"
                  f"<i style='color:{RED};font-size:130px'>Yet.</i></div>")
    if key == "verdict":
        tn = T("November")
        return (f"<div data-in='.05' style='position:absolute;left:50%;top:250px;transform:translate(-50%,0);padding:14px 34px;border:2px solid {Y};"
                f"border-radius:999px;font:800 34px Jakarta;color:{Y};letter-spacing:2px;white-space:nowrap;opacity:0'>MY OPINION · NOT FINANCIAL ADVICE</div>"
                + f"<div class=ttl data-in='.4' style='top:400px;opacity:0'>2000 <i style='color:{RED}'>&gt;</i> 2008</div>"
                + f"<div class=card data-in='{tn - .2:.2f}' style='left:290px;top:600px;width:500px;height:380px;border-color:{RED};color:{RED};padding-top:40px;opacity:0'>"
                  f"<span style='font:700 40px Jakarta;color:#aaa'>WATCH</span><br><span style='font-size:150px;line-height:1.1'>30</span><br>NOV</div>"
                + lab(540, 1030, "$1B TRUMP MEDIA NOTES CAN BE CALLED", T("debt") - .2, RED))
    if key == "cta":
        lit = {i: (s, 0) for i, s in enumerate(STATES) if s != "g"}
        items = "".join(f"<div style='font:700 44px Jakarta;color:#fff;margin:12px 0'>☐ {t}</div>"
                        for t in ("Junk-bond spreads", "The US dollar", "Jobless claims"))
        return (board(400, 60, 34, lit)
                + f"<div data-in='.3' style='position:absolute;left:170px;top:600px;width:740px;padding:24px 40px;border:3px solid {GRN};"
                  f"border-radius:28px;opacity:0'><div style='font:800 34px SpaceG;letter-spacing:3px;color:{GRN}'>MY WATCH LIST</div>{items}</div>"
                + f"<div class=pill data-in='{T('SIGNALS') - .1:.2f}' data-pulse='{T('SIGNALS') + .4:.2f}' style='top:1010px;opacity:0'>COMMENT “SIGNALS”</div>"
                + "<div class=sm data-in='.6' style='left:540px;top:1130px;opacity:0'>My opinion · Not financial advice · Data as of 7 Nov 2026</div>")
    raise KeyError(key)


def make_spec():
    tr = json.load(open(ROOT / "assets/vo" / f"{NAME}.json"))
    words = [w for seg in tr for w in seg["words"]]
    times = align([b[0] for b in B], words)
    end = words[-1][1]
    dur = round(end + 3.0, 2)
    flat, phrases, scenes = [], [], []
    for i, ((text, sc, kw, col), ts) in enumerate(zip(B, times)):
        nxt = times[i + 1][0] if i + 1 < len(times) else end + .3
        want = kw.split()
        ws = text.split()
        phrases.append({"a": ts[0], "b": nxt - .05, "key": [j for j, w in enumerate(ws) if w in want], "color": col,
                        "words": [{"w": w, "t": t} for w, t in zip(ws, ts)]})
        flat += list(zip(ws, ts))
        if sc:
            if scenes:
                scenes[-1]["b"] = ts[0]
            scenes.append({"a": 0 if not scenes else ts[0], "key": sc})
    scenes[-1]["b"] = dur
    phrases[-1]["b"] = dur - .3
    out = []
    for s in scenes:
        def T(word, after=None, a=s["a"]):
            lo = a if after is None else a + after
            for w, t in flat:
                if t >= lo - .01 and w == word:
                    return round(t - a, 2)
            raise KeyError(word)
        out.append({"a": s["a"], "b": s["b"], "html": scene_html(s["key"], T) + progress(s["a"], s["b"], dur)})
    st = {s["key"]: s["a"] for s in scenes}
    W = lambda w, after=0: next(t for x, t in flat if x == w and t >= after)  # noqa: E731
    sfx = [("impact", W("thousand,")), ("impact", W("eight,")), ("impact", W("twenty,")), ("impact", W("Five")),
           ("impact", st["l1"] + .3), ("ticks", W("forty")), ("impact", st["l2"] + .3), ("ticks", W("trillion") - .6),
           ("impact", st["l3"] + .3), ("impact", W("twenty.", st["l3"]) + .6), ("impact", st["l4"] + .3), ("impact", W("twelve")),
           ("impact", st["l5"] + .3), ("impact", W("Yet.")), ("pop", st["verdict"] + .05), ("impact", W("November", st["verdict"]) - .2),
           ("pop", W("SIGNALS") - .1)]
    return {"dur": dur, "scenes": out, "phrases": phrases, "audio": f"assets/vo/{NAME}.mp3", "sfx": sfx}


SPEC = make_spec() if (ROOT / "assets/vo" / f"{NAME}.json").exists() else None
