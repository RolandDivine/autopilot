"""'How do people make millions from a financial collapse?' — 5-step crash plan Reel (7 Nov 2026).
Roland's public opinion, not financial advice. Same family as trump_swan / next_collapse, with real photos
(Wikimedia Commons, see assets/photos/CREDITS.md) and a recurring CRASH PLAN tracker.
Facts: reports/Preparing for a financial crash.md.
"""
import base64, json
from pathlib import Path
from .kit import Y, GRN, RED, GREY, ln, lab, align
from .trump_swan import STYLE, ttl, txt, progress, WHITE
from .next_collapse import board, chip, stamp

ROOT = Path(__file__).resolve().parents[2]
NAME = "crash-plan"
AMB, GOLD = "#ffc83d", "#f5c542"
STEPS = ["Weak currency → digital dollars, offline", "Cash ready to buy the panic", "Everyday essentials",
         "AI shovels, only when cheap", "Crypto: small slice, long term"]


def img(name):
    return "data:image/jpeg;base64," + base64.b64encode((ROOT / "assets/photos" / f"{name}-s.jpg").read_bytes()).decode()


def photo(name, x, y, w, h, at, credit, pos="center"):
    return (f"<div data-in='{at:.2f}' style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:28px;overflow:hidden;"
            f"background:url({img(name)}) {pos}/cover;box-shadow:0 20px 60px rgba(0,0,0,.6);opacity:0'>"
            f"<div style='position:absolute;inset:0;background:linear-gradient(transparent 60%,rgba(0,0,0,.75))'></div>"
            f"<div style='position:absolute;right:14px;bottom:10px;font:500 18px SpaceG;color:#bbb'>{credit}</div></div>")


B = [  # (sentence, scene or None, caption keywords, key colour)
    ("How do people make millions from a financial collapse?", "hook", "millions financial collapse?", GOLD),
    ("In twenty twenty, one investor turned twenty-seven million dollars of protection into two point six billion.", "ackman",
     "twenty-seven million protection two point six billion.", GOLD),
    ("In two thousand eight, Buffett made billions putting money into Goldman Sachs in the panic.", "buffett", "Buffett billions panic.", GOLD),
    ("They didn't predict the date.", "ready", "didn't predict", Y),
    ("They were ready.", None, "ready.", GRN),
    ("Here's my five-step crash plan, and the split for fifty thousand versus fifty million.", None, "five-step crash plan, split", Y),
    ("Step one.", "s1", "one.", GRN),
    ("Get out of weak money.", None, "weak money.", RED),
    ("Since twenty twenty-one, the naira lost three quarters of its value against the dollar.", None, "naira three quarters", RED),
    ("Fully backed stablecoins, digital dollars, kept theirs.", None, "Fully backed digital dollars,", GRN),
    ("Keep them offline, not on an exchange.", None, "offline,", GRN),
    ("Binance just lost six point three billion to a hack.", None, "six point three billion hack.", RED),
    ("But issuers can still freeze them.", None, "freeze", AMB),
    ("Step two.", "s2", "two.", GRN),
    ("Keep cash ready.", None, "cash ready.", GRN),
    ("Every winner had dry powder when everyone else was forced to sell.", None, "dry powder forced", Y),
    ("Step three.", "s3", "three.", GRN),
    ("Own what people buy in any crisis.", None, "any crisis.", Y),
    ("In the dot-com crash, everyday-goods companies rose twenty-four percent while the market halved.", None,
     "everyday-goods rose twenty-four percent halved.", GRN),
    ("Step four.", "s4", "four.", GRN),
    ("Watch the companies AI can't run without: power, chips, robots.", None, "can't run without: power, chips, robots.", Y),
    ("On November fifth, chip stocks fell twelve percent in a day.", None, "twelve percent", RED),
    ("My view: buy them cheap, never in a panic.", None, "view: cheap, never panic.", Y),
    ("Step five.", "s5", "five.", GRN),
    ("Keep crypto small and long term.", None, "small long term.", Y),
    ("Bitcoin fell more than half from its high.", None, "more than half", RED),
    ("Even billion-dollar families keep it around one percent.", None, "one percent.", Y),
    ("The split?", "split", "split?", Y),
    ("An old crash-tested framework holds stocks, bonds, gold and cash, a quarter each.", None, "crash-tested quarter each.", Y),
    ("In two thousand eight, it fell about three percent.", None, "three percent.", GRN),
    ("Stocks fell half.", None, "half.", RED),
    ("And people who panic sold in two thousand eight?", "stay", "panic sold", RED),
    ("Up two percent three years later.", None, "two percent", RED),
    ("The ones who stayed?", None, "stayed?", GRN),
    ("Up fifty.", None, "fifty.", GRN),
    ("Comment PLAN for my full crash plan.", "cta", "PLAN", Y),
    ("My opinion.", None, "", GREY),
    ("Not financial advice.", None, "", GREY),
]


def tracker(done, at_now):
    """Compact plan tracker: 5 numbered circles at y≈410; steps < done ticked, step `done` ticks at at_now."""
    out = ""
    for i in range(5):
        x = 540 - 2 * 120 + i * 120
        ticked = i < done or i == done
        at = 0 if i < done else at_now
        out += (f"<div data-in='0' style='position:absolute;left:{x - 34}px;top:376px;width:62px;height:62px;border-radius:50%;"
                f"border:3px solid #3a3a42;font:800 30px/62px Jakarta;color:#777;text-align:center;opacity:0'>{i + 1}</div>")
        if ticked:
            out += (f"<div data-in='{at:.2f}' style='position:absolute;left:{x - 34}px;top:376px;width:68px;height:68px;border-radius:50%;"
                    f"background:{GRN};box-shadow:0 0 24px {GRN};font:800 36px/68px Jakarta;color:#0b0b0f;text-align:center;opacity:0'>✓</div>")
    return out


def plan_card(top, ticks, base=0.0, step=.35):
    rows = ""
    for i, s in enumerate(STEPS):
        if ticks:
            mark = f"<span style='color:{GRN}'>✓</span>"
            rows += (f"<div data-in='{base + i * step:.2f}' style='font:700 40px/1.25 Jakarta;color:#fff;margin:18px 0;opacity:0'>{mark} {s}</div>")
        else:
            rows += (f"<div data-in='{base + i * step:.2f}' style='margin:26px 0;height:30px;border-radius:15px;background:#26262c;"
                     f"width:{620 - i * 40}px;opacity:0'></div>")
    return (f"<div data-in='{base:.2f}' style='position:absolute;left:110px;top:{top}px;width:860px;padding:30px 40px;border:3px solid "
            f"{GRN if ticks else '#3a3a42'};border-radius:30px;background:#111116;opacity:0'>"
            f"<div style='font:800 34px SpaceG;letter-spacing:4px;color:{GRN}'>MY CRASH PLAN</div>{rows}</div>")


def pill(top, at, s="MY OPINION · NOT FINANCIAL ADVICE"):
    return (f"<div data-in='{at:.2f}' style='position:absolute;left:50%;top:{top}px;transform:translate(-50%,0);padding:12px 30px;border:2px solid {Y};"
            f"border-radius:999px;font:800 30px Jakarta;color:{Y};letter-spacing:2px;white-space:nowrap;opacity:0'>{s}</div>")


def scene_html(key, T):
    if key == "hook":
        mini = board(250, 22, 10, {i: ("r", 0) for i in range(5)})
        return (STYLE + mini.replace("left:", "left:", 1)
                + "<div class=ttl data-in='0' style='top:600px;font-size:88px;line-height:1.15;opacity:0'>How do people<br>make "
                  f"<i style='color:{GOLD};font-size:118px'>millions</i><br>from a collapse?</div>")
    if key == "ackman":
        t = T("twenty-seven")
        return (photo("ackman", 240, 300, 600, 560, 0, "Photo: Senate Democrats, CC BY 2.0")
                + lab(540, 900, "BILL ACKMAN · MARCH 2020", .2, GREY)
                + f"<div class=big data-in='{t:.2f}' style='left:540px;top:960px;color:{GOLD};opacity:0' data-count='27' data-from='0' "
                  f"data-at='{t:.2f}' data-d='.8' data-pre='$' data-suf='M'>$0M</div>"
                + stamp(1080, "→ $2,600,000,000", T("billion.") - .6, GRN, 80))
    if key == "buffett":
        return (photo("buffett", 120, 300, 420, 560, 0, "Photo: US ITA, public domain")
                + photo("goldman", 560, 300, 400, 560, .3, "Photo: Westmc9th, public domain")
                + lab(330, 900, "WARREN BUFFETT", .2, GREY) + lab(760, 900, "GOLDMAN SACHS", .4, GREY)
                + stamp(990, "2008: +$3B", T("billions") - .1, GOLD, 96))
    if key == "ready":
        return (ttl(240, "They were", "ready", T("ready.") - .1, GRN) + plan_card(420, False, .2, .15)
                + f"<div class=sm data-in='{T('split') - .1:.2f}' style='left:540px;top:1060px;opacity:0;color:{Y}'>+ THE SPLIT: $50K VS $50M</div>")
    if key == "s1":
        tn = T("naira")
        return (ttl(225, "Step", "one", c=GRN) + tracker(0, T("freeze") + .2)
                + txt(540, 490, "WEAK MONEY → DIGITAL DOLLARS", T("weak"), 46, WHITE)
                + "<svg>" + ln("M200 620 C380 630 520 660 620 710 S800 760 880 770", tn - .3, 1.4, RED, 8) + "</svg>"
                + lab(260, 580, "₦380 = $1 (2021)", tn - .2, GREY) + lab(800, 800, "₦1,500 = $1 (2026)", tn + .8, RED)
                + stamp(850, "−75% VS USD", T("three") + .2, RED, 64)
                + chip(300, 980, "OFFLINE WALLET ✓", T("offline,") - .1, GRN)
                + chip(780, 980, "$6.3B HACK", T("hack.") - .4, RED, True)
                + f"<div class=sm data-in='{T('freeze') - .3:.2f}' style='left:540px;top:1100px;opacity:0;color:{AMB}'>⚠ Issuers can still freeze stablecoins</div>")
    if key == "s2":
        bars = "".join(ln(f"M{380 + i * 0} {1000 - i * 50} h320", T("cash") + i * .12, .3, GRN, 36) for i in range(6))
        return (ttl(225, "Step", "two", c=GRN) + tracker(1, T("sell.") - .3)
                + txt(540, 500, "KEEP CASH READY", T("cash"), 60, WHITE) + "<svg>" + bars + "</svg>"
                + stamp(1060, "DRY POWDER", T("dry"), GOLD, 92)
                + f"<div class=sm data-in='{T('forced'):.2f}' style='left:540px;top:1170px;opacity:0'>buy when others are forced to sell</div>")
    if key == "s3":
        tt = T("twenty-four")
        return (ttl(225, "Step", "three", c=GRN) + tracker(2, tt + 1.0)
                + photo("walmart", 140, 480, 800, 420, 0, "Photo: FLGALine1999, CC0")
                + lab(540, 940, "EVERYDAY ESSENTIALS · 2000–02 CRASH", .3, GREY)
                + chip(320, 1000, "STAPLES +24%", tt - .1, GRN, True) + chip(760, 1000, "S&amp;P 500 −49%", T("halved.") - .2, RED, True))
    if key == "s4":
        icons = ("M300 1000 h120 v-120 h-120 z M320 880 v-20 M360 880 v-20 M400 880 v-20 M320 1000 v20 M360 1000 v20 M400 1000 v20 "
                 "M660 1010 h120 M700 1010 v-60 l60 -60 l50 30 M810 920 l20 20")
        return (ttl(225, "Step", "four", c=GRN) + tracker(3, T("panic.") - .2)
                + photo("power", 140, 480, 800, 360, 0, "Photo: Foto3821, CC0")
                + lab(540, 880, "POWER · CHIPS · ROBOTS", T("power,") - .2, Y)
                + stamp(960, "CHIPS −12% IN A DAY", T("twelve") - .1, RED, 70)
                + pill(1090, T("view:") - .1))
    if key == "s5":
        return (ttl(225, "Step", "five", c=GRN) + tracker(4, T("percent.") + .2)
                + txt(540, 490, "CRYPTO: SMALL &amp; LONG TERM", T("small"), 50, WHITE)
                + "<svg>" + ln("M180 600 C330 570 400 590 470 660 S640 860 900 900", T("Bitcoin") - .2, 1.4, RED, 8) + "</svg>"
                + lab(230, 560, "$126K", T("Bitcoin"), GREY) + lab(860, 940, "$59K", T("half") - .3, RED)
                + chip(540, 1000, "FAMILY OFFICES: ~1% CRYPTO", T("billion-dollar") - .1, Y) + pill(1120, .3))
    if key == "split":
        def col(x, title, rows, at):
            r = "".join(f"<div style='display:flex;justify-content:space-between;font:700 36px/1.5 Jakarta;color:#fff'><span>{a}</span>"
                        f"<span style='color:{c}'>{b}</span></div>" for a, b, c in rows)
            return (f"<div data-in='{at:.2f}' style='position:absolute;left:{x}px;top:420px;width:420px;padding:26px 30px;border:3px solid #3a3a42;"
                    f"border-radius:26px;background:#111116;opacity:0'><div style='font:800 44px Jakarta;color:{GOLD}'>{title}</div>{r}</div>")
        small = [("Stocks", "25%", WHITE), ("Bonds", "25%", WHITE), ("Gold", "25%", GOLD), ("Cash*", "25%", GRN)]
        big = [("Stocks/private", "~70%", WHITE), ("Bonds", "~14%", WHITE), ("Cash", "9%", GRN), ("Gold", "2–3%", GOLD), ("Crypto", "~1%", AMB)]
        return (pill(240, .05) + col(80, "$50K saver", small, T("crash-tested") - .2) + col(560, "$50M family", big, T("quarter") + .3)
                + stamp(900, "2008: −3%", T("three") - .1, GRN, 84) + chip(540, 1020, "STOCKS −49%", T("half.") - .1, RED, True)
                + "<div data-in='.6' style='position:absolute;left:0;right:0;top:1150px;text-align:center;font:500 26px Jakarta;color:#8b8b93;opacity:0'>*Roland's version: digital dollars · Published frameworks, not advice</div>")
    if key == "stay":
        return (ttl(240, "Sold vs", "stayed", .05, GRN)
                + "<svg>" + ln("M360 1000 V960", T("two") - .2, .4, "#55555e", 160) + ln("M720 1000 V560", T("fifty.") - .3, .8, GRN, 160) + "</svg>"
                + lab(360, 1040, "SOLD IN 2008", T("panic") , GREY) + lab(720, 1040, "STAYED", T("stayed?"), GRN)
                + stamp(800, "+2%", T("two"), "#9a9aa3", 90).replace("left:540px", "left:360px")
                + stamp(420, "+50%", T("fifty."), GRN, 110).replace("left:540px", "left:720px")
                + "<div class=sm data-in='.4' style='left:540px;top:1110px;opacity:0'>Fidelity, 7.1M 401(k) accounts, 2008→2011</div>")
    if key == "cta":
        return (plan_card(260, True, .1, .2)
                + f"<div class=pill data-in='{T('PLAN') - .2:.2f}' data-pulse='{T('PLAN') + .3:.2f}' style='top:1000px;opacity:0'>COMMENT “PLAN”</div>"
                + "<div class=sm data-in='.6' style='left:540px;top:1120px;opacity:0'>My opinion · Not financial advice · Data as of 7 Nov 2026</div>")
    raise KeyError(key)


def make_spec():
    tr = json.load(open(ROOT / "assets/vo" / f"{NAME}.json"))
    words = [w for seg in tr for w in seg["words"]]
    times = align([b[0] for b in B], words)
    end = words[-1][1]
    dur = round(end + 2.6, 2)
    flat, phrases, scenes = [], [], []
    for i, ((text, sc, kw, col), ts) in enumerate(zip(B, times)):
        nxt = times[i + 1][0] if i + 1 < len(times) else end + .3
        want, ws = kw.split(), text.split()
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
        def T(word, a=s["a"]):
            for w, t in flat:
                if t >= a - .01 and w == word:
                    return round(t - a, 2)
            raise KeyError(word)
        out.append({"a": s["a"], "b": s["b"], "html": scene_html(s["key"], T) + progress(s["a"], s["b"], dur)})
    st = {s["key"]: s["a"] for s in scenes}
    W = lambda w, after=0: next(t for x, t in flat if x == w and t >= after)  # noqa: E731
    sfx = [("ticks", W("twenty-seven")), ("impact", W("billion.") - .6), ("impact", W("billions")), ("pop", st["ready"] + .2)]
    for k, w in (("s1", "freeze"), ("s2", "sell."), ("s3", "twenty-four"), ("s4", "panic."), ("s5", "percent.")):
        sfx += [("impact", st[k] + .2), ("pop", W(w, st[k]) + (1.0 if k == "s3" else .2))]
    sfx += [("impact", W("hack.") - .4), ("impact", W("twelve")), ("impact", W("three", st["split"]) - .1),
            ("impact", W("fifty.")), ("pop", W("PLAN") - .2)]
    return {"dur": dur, "scenes": out, "phrases": phrases, "audio": f"assets/vo/{NAME}.mp3", "sfx": sfx}


SPEC = make_spec() if (ROOT / "assets/vo" / f"{NAME}.json").exists() else None
