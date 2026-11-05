"""Sample Reel: AI trading bot = Ponzi (30s). Phrase times are estimates until the voice is generated."""
Y, TEAL, GRN, RED = "#ffd60a", "#5ec8b8", "#2fd27a", "#ff4d4d"

def P(a, b, text, key=(), color=Y):
    ws = text.split()
    step = (b - a) / len(ws)
    return {"a": a, "b": b, "key": list(key), "color": color,
            "words": [{"w": w, "t": round(a + i * step, 3)} for i, w in enumerate(ws)]}

PHRASES = [
    P(0.3, 2.4, "This is one hundred thousand naira.", [4, 5]),
    P(2.6, 5.6, "An AI trading bot promises you three percent a day.", [6, 7, 8, 9], GRN),
    P(5.8, 7.2, "Sounds small, right?"),
    P(7.4, 9.6, "But compound it for one year,", [4, 5]),
    P(9.7, 12.6, "and it becomes four point eight billion naira.", [3, 4, 5, 6], GRN),
    P(12.9, 16.6, "The best hedge funds on earth are happy with twenty percent a year.", [10, 11]),
    P(16.9, 18.7, "So how is the bot paying you?"),
    P(18.9, 20.9, "With the next person's deposit.", [2, 3], TEAL),
    P(21.2, 22.3, "That's not AI."),
    P(22.4, 23.8, "That's a Ponzi.", [2], RED),
    P(24.2, 28.0, "Comment BOT, and I'll send you my ten-second scam check.", [1]),
]

def ln(d, at, dur, c=Y, w=7, extra=""):
    return f"<path class=ln d='{d}' data-at='{at}' data-d='{dur}' style='stroke:{c};stroke-width:{w};filter:drop-shadow(0 0 10px {c})' {extra}/>"

def lab(x, y, text, at, c=Y, cls="lab"):
    return f"<div class={cls} data-in='{at}' style='left:{x}px;top:{y}px;color:{c};opacity:0'>{text}</div>"

NOTE = ("<svg>" + ln("M240 560 h600 a24 24 0 0 1 24 24 v310 a24 24 0 0 1 -24 24 h-600 a24 24 0 0 1 -24 -24 v-310 a24 24 0 0 1 24 -24 z", 0, 1.3)
        + ln("M300 620 h480 v250 h-480 z", .5, 1.0, TEAL, 3)
        + ln("M540 745 m-70 0 a70 70 0 1 0 140 0 a70 70 0 1 0 -140 0", .9, .8, Y, 5)
        + ln("M515 700 v90 M565 700 v90 M515 700 l50 90 M495 735 h90 M495 755 h90", 1.3, .6, Y, 5) + "</svg>"
        + lab(540, 980, "₦100,000", 1.1))

CURVE = ("<svg>" + ln("M170 1180 H930 M170 1180 V420", 0, .5, "#3a3a42", 3)
         + "".join(ln(f"M{170+i*63} 1180 v14", .2 + i * .03, .2, "#3a3a42", 3) for i in range(13))
         + ln("M170 1175 C 560 1170 760 1120 840 900 S 905 470 925 420", .3, 4.2, GRN, 8) + "</svg>"
         + lab(540, 1215, "12 months · +3% / day", .4, "#8b8b93")
         + "<div class=big data-in='.3' style='left:540px;top:250px;color:#fff;opacity:0' data-count='4800000000' data-from='100000' data-at='.3' data-d='4.4' data-exp=1 data-pre='₦'>₦100,000</div>")

TOWERS = (lab(330, 640, "Hedge fund<br>+20% / yr", .6, Y) + lab(720, 300, "The bot's promise<br>×48,000", 1.6, GRN))

QMARK = ("<svg>" + ln("M420 640 C420 470 660 470 660 610 C660 720 540 730 540 840 V900", 0, 1.1, Y, 14)
         + ln("M540 1010 v2", 1.0, .2, Y, 22) + "</svg>")

PYR = lab(540, 300, "New deposits ↑ pay the top", .5, TEAL)

PONZI = ("<svg>" + ln("M380 560 h320 a40 40 0 0 1 40 40 v220 a40 40 0 0 1 -40 40 h-320 a40 40 0 0 1 -40 -40 v-220 a40 40 0 0 1 40 -40 z",
                       0, 1.0, Y, 8, "data-color-at='1.25' data-c1='#ffd60a' data-c2='#ff4d4d'")
         + ln("M460 690 v40 M620 690 v40 M470 790 h140 M540 560 v-80 M540 470 m-18 0 a18 18 0 1 0 36 0 a18 18 0 1 0 -36 0", .5, .7, Y, 8,
              "data-color-at='1.25' data-c1='#ffd60a' data-c2='#ff4d4d'")
         + ln("M540 940 L760 1200 H320 Z", 1.3, .8, RED, 8) + "</svg>"
         + f"<div class=big data-in='1.3' data-shake='1.3' style='left:540px;top:250px;color:{RED};opacity:0'>PONZI</div>")

CTA = ("<svg>" + "".join(ln(f"M330 {600+i*120} l30 30 l60 -60", .3 + i * .35, .4, GRN, 8) + ln(f"M460 {610+i*120} h300", .45 + i * .35, .4, "#55555c", 6) for i in range(3)) + "</svg>"
       + "<div class=pill data-in='1.6' data-pulse='2' style='top:1040px;opacity:0'>+ COMMENT BOT</div>"
       + lab(540, 1170, "Get the 10-second scam check", 2.0, "#8b8b93"))

SCENES = [
    {"a": 0, "b": 2.6, "html": NOTE},
    {"a": 2.6, "b": 7.3, "three": "chip", "html": lab(540, 220, "AI bot · +3% / day", .4, GRN)},
    {"a": 7.3, "b": 12.8, "html": CURVE},
    {"a": 12.8, "b": 16.8, "three": "towers", "html": TOWERS},
    {"a": 16.8, "b": 18.8, "html": QMARK},
    {"a": 18.8, "b": 21.1, "three": "pyramid", "html": PYR},
    {"a": 21.1, "b": 24.1, "html": PONZI},
    {"a": 24.1, "b": 30.0, "html": CTA},
]

SPEC = {"dur": 30.0, "scenes": SCENES, "phrases": PHRASES, "audio": None}
