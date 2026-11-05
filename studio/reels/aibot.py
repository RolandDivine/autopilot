"""Sample Reel: AI trading bot = Ponzi (27s), Documentary Narrator voice, global audience (dollars)."""
Y, TEAL, GRN, RED = "#ffd60a", "#5ec8b8", "#2fd27a", "#ff4d4d"

def P(a, b, text, key=(), color=Y):
    ws = text.split()
    step = (b - a) / len(ws)
    return {"a": a, "b": b, "key": list(key), "color": color,
            "words": [{"w": w, "t": round(a + i * step, 3)} for i, w in enumerate(ws)]}

def T(text, times, b, key=(), color=Y):
    ws = text.split()
    assert len(ws) == len(times), (text, len(ws), len(times))
    return {"a": times[0], "b": b, "key": list(key), "color": color, "words": [{"w": w, "t": t} for w, t in zip(ws, times)]}

# word times from the Documentary Narrator take (assets/vo/aibot-usd.mp3, transcribed)
PHRASES = [
    T("This is one thousand dollars.", [0.0, .2, .38, .55, .72], 1.8, [2, 3, 4]),
    T("An AI trading bot promises you three percent a day.", [1.9, 2.2, 2.58, 2.98, 3.26, 3.7, 3.98, 4.32, 4.64, 4.84], 5.4, [6, 7, 8, 9], GRN),
    T("Sounds small, right?", [5.58, 5.76, 6.32], 6.8),
    T("But compound it for one year,", [6.92, 7.1, 7.54, 7.72, 7.88, 8.14], 8.45, [4, 5]),
    T("and it becomes forty-eight million dollars.", [8.48, 8.82, 8.92, 9.2, 9.84, 10.2], 10.8, [3, 4, 5], GRN),
    T("The best hedge funds on earth are happy with twenty percent a year.", [10.94, 11.18, 11.44, 11.68, 11.92, 12.14, 12.36, 12.64, 12.92, 13.1, 13.42, 13.74, 13.94], 14.4, [10, 11]),
    T("So how is the bot paying you?", [14.48, 14.64, 14.82, 14.96, 15.08, 15.28, 15.58], 16.3),
    T("With the next person's deposit.", [16.48, 16.64, 16.82, 17.06, 17.5], 18.2, [2, 3], TEAL),
    T("That's not AI.", [18.36, 18.6, 18.8], 19.5),
    T("That's a Ponzi.", [19.64, 19.86, 19.92], 20.7, [2], RED),
    T("Comment BOT, and I'll send you my ten-second scam check.", [20.84, 21.06, 21.68, 22.22, 22.4, 22.54, 22.7, 22.84, 23.38, 23.74], 26.6, [1]),
]

def ln(d, at, dur, c=Y, w=7, extra=""):
    return f"<path class=ln d='{d}' data-at='{at}' data-d='{dur}' style='stroke:{c};stroke-width:{w};filter:drop-shadow(0 0 10px {c})' {extra}/>"

def lab(x, y, text, at, c=Y, cls="lab"):
    return f"<div class={cls} data-in='{at}' style='left:{x}px;top:{y}px;color:{c};opacity:0'>{text}</div>"

NOTE = ("<svg>" + ln("M240 560 h600 a24 24 0 0 1 24 24 v310 a24 24 0 0 1 -24 24 h-600 a24 24 0 0 1 -24 -24 v-310 a24 24 0 0 1 24 -24 z", 0, .7)
        + ln("M300 620 h480 v250 h-480 z", .2, .6, TEAL, 3)
        + ln("M540 745 m-70 0 a70 70 0 1 0 140 0 a70 70 0 1 0 -140 0", .4, .5, Y, 5)
        + ln("M570 712 C560 696 512 696 512 722 C512 748 570 742 570 768 C570 794 518 794 508 778 M540 688 v114", .6, .5, Y, 6) + "</svg>"
        + lab(540, 980, "$1,000", .6))

CURVE = ("<svg>" + ln("M170 1180 H930 M170 1180 V420", 0, .5, "#3a3a42", 3)
         + "".join(ln(f"M{170+i*63} 1180 v14", .2 + i * .03, .2, "#3a3a42", 3) for i in range(13))
         + ln("M170 1175 C 560 1170 760 1120 840 900 S 905 470 925 420", .3, 4.2, GRN, 8) + "</svg>"
         + lab(540, 1215, "12 months · +3% / day", .4, "#8b8b93")
         + "<div class=big data-in='.3' style='left:540px;top:250px;color:#fff;opacity:0' data-count='48000000' data-from='1000' data-at='.2' data-d='3.3' data-exp=1 data-pre='$'>$1,000</div>")

TOWERS = (lab(330, 640, "Hedge fund<br>+20% / yr", .6, Y) + lab(720, 300, "The bot's promise<br>×48,000", 1.6, GRN))

QMARK = ("<svg>" + ln("M420 640 C420 470 660 470 660 610 C660 720 540 730 540 840 V900", 0, 1.1, Y, 14)
         + ln("M540 1010 v2", 1.0, .2, Y, 22) + "</svg>")

PYR = lab(540, 300, "New deposits ↑ pay the top", .5, TEAL)

PONZI = ("<svg>" + ln("M380 560 h320 a40 40 0 0 1 40 40 v220 a40 40 0 0 1 -40 40 h-320 a40 40 0 0 1 -40 -40 v-220 a40 40 0 0 1 40 -40 z",
                       0, 1.0, Y, 8, "data-color-at='1.57' data-c1='#ffd60a' data-c2='#ff4d4d'")
         + ln("M460 690 v40 M620 690 v40 M470 790 h140 M540 560 v-80 M540 470 m-18 0 a18 18 0 1 0 36 0 a18 18 0 1 0 -36 0", .5, .7, Y, 8,
              "data-color-at='1.57' data-c1='#ffd60a' data-c2='#ff4d4d'")
         + ln("M540 940 L760 1200 H320 Z", 1.55, .6, RED, 8) + "</svg>"
         + f"<div class=big data-in='1.57' data-shake='1.57' style='left:540px;top:250px;color:{RED};opacity:0'>PONZI</div>")

CTA = ("<svg>" + "".join(ln(f"M330 {600+i*120} l30 30 l60 -60", .3 + i * .35, .4, GRN, 8) + ln(f"M460 {610+i*120} h300", .45 + i * .35, .4, "#55555c", 6) for i in range(3)) + "</svg>"
       + "<div class=pill data-in='1.6' data-pulse='2' style='top:1040px;opacity:0'>+ COMMENT BOT</div>"
       + lab(540, 1170, "Get the 10-second scam check", 2.0, "#8b8b93"))

SCENES = [
    {"a": 0, "b": 1.9, "html": NOTE},
    {"a": 1.9, "b": 6.9, "three": "chip", "html": lab(540, 220, "AI bot · +3% / day", .4, GRN)},
    {"a": 6.9, "b": 10.9, "html": CURVE},
    {"a": 10.9, "b": 14.45, "three": "towers", "html": TOWERS},
    {"a": 14.45, "b": 16.45, "html": QMARK},
    {"a": 16.45, "b": 18.35, "three": "pyramid", "html": PYR},
    {"a": 18.35, "b": 20.8, "html": PONZI},
    {"a": 20.8, "b": 27.0, "html": CTA},
]

SPEC = {"dur": 27.0, "scenes": SCENES, "phrases": PHRASES, "audio": "assets/vo/aibot-usd.mp3",
        "sfx": [("ticks", 7.1), ("impact", 19.92), ("pop", 22.4)]}
