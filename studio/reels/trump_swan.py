"""Trump Media BTC transfer + 'black swan' Reel (6 Nov 2026). Documentary Narrator, global audience.
Style deliberately different from the trend series: serif-italic titles (reference videos), avatar badge,
candle charts, swan motif, a progress bar along the bottom. Facts checked 6 Nov 2026 (CoinDesk, IBTimes, The Block, CoinGecko).
"""
import base64, json
from pathlib import Path
from .kit import Y, GRN, RED, GREY, ln, lab, align

ROOT = Path(__file__).resolve().parents[2]
NAME = "trump-swan"
WHITE = "#f4f4f6"

# (sentence, scene-or-None, caption key word indexes, key colour)
BEATS = [
    ("Trump's company just moved three hundred and forty-three million dollars of Bitcoin to an exchange.", "hook", "Trump's three hundred and forty-three million dollars Bitcoin", Y),
    ("The same day, Bitcoin dumped to about seventy-six thousand.", "crash", "dumped seventy-six thousand.", RED),
    ("But Trump isn't the black swan I'm worried about.", "swan", "black swan", RED),
    ("First, the facts.", "facts", "facts.", Y),
    ("Moving coins to an exchange is usually what you do before you sell.", None, "before sell.", Y),
    ("But it's not a confirmed sale. Not yet.", None, "not confirmed sale.", Y),
    ("Here's the twist.", "twist", "twist.", Y),
    ("Those coins came from wallets tagged as collateral for a billion-dollar debt that can come due on November thirtieth.", None, "collateral billion-dollar debt November thirtieth.", RED),
    ("And more than a billion dollars of trades were force-closed.", "liq", "billion dollars force-closed.", RED),
    ("People betting with borrowed money got wiped out.", None, "borrowed money wiped out.", RED),
    ("A black swan is the event nobody sees coming that changes everything.", "define", "black swan nobody sees", Y),
    ("And stocks fell at the same time.", "together", "stocks fell", RED),
    ("My view: when stocks and crypto fall together, the danger isn't the drop.", "view", "view: together, drop.", Y),
    ("It's being forced to sell at the bottom.", None, "forced sell bottom.", RED),
    ("So before the next swan, run this checklist.", "check", "swan, checklist.", GRN),
    ("Screenshot it.", None, "Screenshot", GRN),
    ("Comment SWAN and I'll send you my full market-crash checklist.", None, "SWAN", Y),
    ("Not financial advice.", None, "", GREY),
]

AVATAR = base64.b64encode((ROOT / "assets/brand/avatar.jpg").read_bytes()).decode()
LORA = base64.b64encode(Path("/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf").read_bytes()).decode()
STYLE = (f"<style>@font-face{{font-family:LoraI;font-style:italic;src:url(data:font/ttf;base64,{LORA})}}"
         ".ttl{position:absolute;left:0;right:0;text-align:center;font:800 76px Jakarta;color:#fff;letter-spacing:-1px}"
         ".ttl i{font:italic 600 84px LoraI;letter-spacing:0}"
         ".card{position:absolute;border:3px solid;border-radius:28px;text-align:center;font:800 64px Jakarta}"
         ".sm{position:absolute;font:600 30px SpaceG;letter-spacing:3px;color:#8b8b93;text-transform:uppercase;white-space:nowrap;transform:translate(-50%,0)}"
         f"body::before{{content:'';position:absolute;z-index:9;left:60px;top:70px;width:76px;height:76px;border-radius:50%;"
         f"background:url(data:image/jpeg;base64,{AVATAR}) center/cover;border:2px solid #333}}"
         "body::after{content:'Roland Divine  ·  @defi_ring_master';position:absolute;z-index:9;left:156px;top:92px;"
         "font:700 28px Jakarta;color:#d8d8dc}</style>")


def ttl(y, plain, italic, at=.05, c=Y):
    return f"<div class=ttl data-in='{at}' style='top:{y}px;opacity:0'>{plain} <i style='color:{c}'>{italic}</i></div>"


def txt(x, y, s, at, size=64, c=WHITE, w=800):
    return (f"<div data-in='{at}' style='position:absolute;left:{x}px;top:{y}px;transform:translate(-50%,0);white-space:nowrap;"
            f"font:{w} {size}px Jakarta;color:{c};opacity:0'>{s}</div>")


def candles(down=True):
    """Candle chart drawing left to right; last candles crash."""
    out, x = [], 200
    o = [700, 680, 690, 660, 670, 650, 700, 820, 980]
    for i in range(len(o) - 1):
        a, b = o[i], o[i + 1]
        red = b > a  # y grows downward => price falls
        c = RED if red else GRN
        top, bot = min(a, b), max(a, b)
        out.append(ln(f"M{x} {top - 30} V{bot + 30}", .1 + i * .12, .2, c, 4))
        out.append(ln(f"M{x} {top} V{bot + 1}", .1 + i * .12, .2, c, 34))
        x += 85
    return "<svg>" + ln("M160 1060 H940", 0, .3, "#2a2a30", 3) + "".join(out) + "</svg>"


SWAN = ("M800 820 C770 930 560 990 420 930 C350 900 340 850 380 820 C420 790 470 800 500 770 C540 720 470 680 440 620 "
        "C410 560 430 500 480 490 C520 482 545 505 548 530 L600 548 L548 552 C540 575 505 580 495 600 C480 640 560 690 570 740 "
        "C620 700 720 690 800 640 C780 700 830 760 800 820 Z")


def scene_html(key):
    if key == "hook":
        return (STYLE + txt(540, 330, "TRUMP MEDIA", .05, 92) + txt(540, 450, "&#8595; EXCHANGE", .3, 64, GREY, 700)
                + f"<div class=big data-in='.25' style='left:540px;top:640px;color:{Y};opacity:0' data-count='343000000' data-from='0' "
                  "data-at='.3' data-d='2' data-pre='$' data-suf=''>$0</div>"
                + "<svg>" + ln("M260 820 H820", .3, 1.0, Y, 6) + "</svg>" + lab(540, 880, "4,259 BTC  ·  5 NOV", .6, Y))
    if key == "crash":
        return (ttl(250, "Bitcoin", "dumps", c=RED) + candles()
                + f"<div class=big data-in='1.0' data-shake='1.0' style='left:540px;top:1080px;color:{RED};opacity:0;font-size:104px'>~$76K &#9660;5.6%</div>")
    if key == "swan":
        return ("<svg><g transform='translate(540 760) scale(1.2) translate(-600 -720)'>" + ln(SWAN, .05, 1.2, WHITE, 6) + "</g></svg>"
                + ttl(300, "The real", "black swan?", .5, RED))
    if key == "facts":
        return (ttl(260, "The", "facts")
                + f"<div class=card data-in='.6' style='left:120px;top:520px;width:390px;height:330px;border-color:{GRN};color:{GRN};padding-top:70px;opacity:0'>MOVED<br><span style='font-size:110px'>&#10003;</span></div>"
                + f"<div class=card data-in='5.3' style='left:570px;top:520px;width:390px;height:330px;border-color:{Y};color:{Y};padding-top:70px;opacity:0'>SOLD<br><span style='font-size:110px'>?</span></div>"
                + "<div class=sm data-in='1' style='left:540px;top:910px;opacity:0'>on-chain data shows a transfer, not a sale</div>")
    if key == "twist":
        return (ttl(260, "The", "twist")
                + "<svg><g transform='translate(540 640) scale(.8) translate(-540 -760)'>"
                + ln("M400 720 h280 a20 20 0 0 1 20 20 v200 a20 20 0 0 1 -20 20 h-280 a20 20 0 0 1 -20 -20 v-200 a20 20 0 0 1 20 -20 z", .9, .6, Y, 7)
                + ln("M450 720 v-70 a90 90 0 0 1 180 0 v70", 1.3, .5, Y, 7) + "</g></svg>"
                + lab(540, 820, "TAGGED: NOTES COLLATERAL", 1.4, Y)
                + txt(540, 900, "$1B debt", 3.8, 92, WHITE)
                + f"<div class=big data-in='5.4' data-shake='5.4' style='left:540px;top:1030px;color:{RED};opacity:0;font-size:88px'>DUE FROM 30 NOV</div>")
    if key == "liq":
        return (f"<div class=big data-in='.1' style='left:540px;top:520px;color:{RED};opacity:0' data-count='1000000000' data-from='0' "
                "data-at='.15' data-d='1.8' data-pre='$' data-suf='+'>$0</div>"
                + "<svg>" + ln("M200 690 H880", .2, .8, RED, 6)
                + ln("M300 860 h150 a40 40 0 0 1 0 80 h-150 a40 40 0 0 1 0 -80 z", .4, .5, GREY, 7)
                + ln("M630 860 h150 a40 40 0 0 1 0 80 h-150 a40 40 0 0 1 0 -80 z", .4, .5, GREY, 7)
                + ln("M500 880 l40 20 l-20 20 l40 20", 1.2, .3, RED, 7) + "</svg>"
                + lab(540, 740, "FORCE-CLOSED · LIQUIDATED", .5, RED)
                + lab(540, 1010, "BORROWED MONEY", 3.8, RED))
    if key == "define":
        return (ttl(260, "Black", "swan", c=Y) + txt(540, 470, "/ noun /", .3, 40, GREY, 600)
                + "".join(txt(540, 600 + i * 130, w, .9 + i * .55, 76, c) for i, (w, c) in
                          enumerate([("RARE", WHITE), ("UNEXPECTED", WHITE), ("MASSIVE IMPACT", RED)])))
    if key == "together":
        return ("<svg>" + ln("M160 1060 H940 M160 1060 V520", 0, .3, "#2a2a30", 3)
                + ln("M180 560 C380 580 500 640 600 760 S820 980 920 1010", .2, 1.4, RED, 8)
                + ln("M180 640 C380 650 500 700 600 820 S820 1000 920 1040", .35, 1.4, Y, 8) + "</svg>"
                + lab(300, 470, "STOCKS", .4, Y) + lab(760, 470, "CRYPTO", .4, RED) + ttl(260, "Falling", "together", .1, RED))
    if key == "view":
        return (f"<div data-in='.05' style='position:absolute;left:50%;top:250px;transform:translate(-50%,0);padding:14px 34px;border:2px solid {Y};"
                f"border-radius:999px;font:800 34px Jakarta;color:{Y};letter-spacing:2px;white-space:nowrap;opacity:0'>MY VIEW · NOT FINANCIAL ADVICE</div>"
                + "<svg>" + ln("M180 560 C380 580 520 700 640 880 S820 1010 900 1020", .3, 1.6, RED, 8)
                + f"</svg>"
                + txt(540, 420, "The danger isn't the drop.", 1.0, 56)
                + f"<div class=big data-in='4.3' data-shake='4.3' style='left:540px;top:1060px;color:{RED};opacity:0;font-size:78px'>FORCED TO SELL</div>")
    if key == "check":
        items = ["No borrowed money (no leverage)", "Headline? Check: transfer or sale", "Emergency fund outside crypto",
                 "Only hold what can drop 50%", "Savings not on one exchange"]
        out, labs = "<svg>", ""
        for i, t in enumerate(items):
            y = 470 + i * 112
            out += ln(f"M150 {y} l26 26 l52 -52", .6 + i * .5, .3, GRN, 8)
            labs += (f"<div data-in='{.7 + i * .5}' style='position:absolute;left:250px;top:{y - 34}px;width:760px;"
                     f"font:700 42px/1.2 Jakarta;color:#fff;opacity:0'>{t}</div>")
        return (ttl(250, "Before the next", "swan", c=Y) + out + "</svg>" + labs
                + f"<div class=pill data-in='3.9' data-pulse='4.5' style='top:1040px;opacity:0'>COMMENT “SWAN”</div>"
                + "<div class=sm data-in='4.2' style='left:540px;top:1160px;opacity:0'>Not financial advice · figures as of 6 Nov 2026</div>")
    raise KeyError(key)


def progress(a, b, dur):
    """Bottom progress bar: solid up to a, drawing from a to b during the scene."""
    x0, x1 = 60 + 960 * a / dur, 60 + 960 * b / dur
    return ("<svg>" + ln("M60 1880 H1020", 0, .01, "#26262c", 8)
            + (ln(f"M60 1880 H{x0:.0f}", 0, .01, Y, 8) if x0 > 61 else "")
            + ln(f"M{x0:.0f} 1880 H{x1:.0f}", 0, b - a, Y, 8) + "</svg>")


def make_spec():
    tr = json.load(open(ROOT / "assets/vo" / f"{NAME}.json"))
    words = [w for seg in tr for w in seg["words"]]
    times = align([b[0] for b in BEATS], words)
    end = words[-1][1]
    dur = round(end + 2.4, 2)
    phrases, scenes = [], []
    for i, ((text, sc, kw, col), ts) in enumerate(zip(BEATS, times)):
        want = kw.split()
        key = [j for j, w in enumerate(text.split()) if w in want]
        nxt = times[i + 1][0] if i + 1 < len(times) else end + .3
        phrases.append({"a": ts[0], "b": nxt - .05, "key": key, "color": col,
                        "words": [{"w": w, "t": t} for w, t in zip(text.split(), ts)]})
        if sc:
            if scenes:
                scenes[-1]["b"] = ts[0]
            scenes.append({"a": 0 if not scenes else ts[0], "key": sc})
    scenes[-1]["b"] = dur
    phrases[-1]["b"] = dur - .3
    out = [{"a": s["a"], "b": s["b"], "html": scene_html(s["key"]) + progress(s["a"], s["b"], dur)} for s in scenes]
    st = {s["key"]: s["a"] for s in scenes}
    sfx = [("impact", .9), ("impact", st["crash"] + 1.0), ("impact", st["swan"] + .4), ("pop", st["facts"] + .6), ("pop", st["facts"] + 5.3),
           ("impact", st["twist"] + 5.4), ("ticks", st["liq"] + .15), ("impact", st["view"] + 4.3),
           ("ticks", st["check"] + .6), ("pop", st["check"] + 3.9)]
    return {"dur": dur, "scenes": out, "phrases": phrases, "audio": f"assets/vo/{NAME}.mp3", "sfx": sfx}


SPEC = make_spec() if (ROOT / "assets/vo" / f"{NAME}.json").exists() else None
