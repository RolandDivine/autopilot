"""Building blocks for series Reels: line-art icons, counters, charts, lists, CTA, plus 3D scene keys.
A Reel is a list of beats: (sentence, visual). visual=None continues the previous scene.
Timing comes from the voice transcript (align), so scenes cut exactly on the spoken sentence.
"""
import json, re
from pathlib import Path

Y, TEAL, GRN, RED, BLUE, PINK, GREY = "#ffd60a", "#5ec8b8", "#2fd27a", "#ff4d4d", "#4da3ff", "#ff6ad5", "#8b8b93"


def ln(d, at, dur, c=Y, w=7, extra=""):
    return (f"<path class=ln d='{d}' data-at='{at}' data-d='{dur}' "
            f"style='stroke:{c};stroke-width:{w};filter:drop-shadow(0 0 10px {c})' {extra}/>")


def lab(x, y, text, at, c=Y, cls="lab"):
    return f"<div class={cls} data-in='{at}' style='left:{x}px;top:{y}px;color:{c};opacity:0'>{text}</div>"


# 260x260 icons centred on (540, 760); each is a list of path strings drawn in order
ICONS = {
    "key": ["M380 760 m-90 0 a90 90 0 1 0 180 0 a90 90 0 1 0 -180 0", "M380 760 m-30 0 a30 30 0 1 0 60 0 a30 30 0 1 0 -60 0",
            "M470 760 H760 M700 760 v55 M650 760 v40"],
    "lock": ["M400 720 h280 a20 20 0 0 1 20 20 v200 a20 20 0 0 1 -20 20 h-280 a20 20 0 0 1 -20 -20 v-200 a20 20 0 0 1 20 -20 z",
             "M450 720 v-70 a90 90 0 0 1 180 0 v70", "M540 810 v60"],
    "shield": ["M540 560 L720 630 V780 C720 880 640 940 540 980 C440 940 360 880 360 780 V630 Z", "M460 770 l55 55 l105 -110"],
    "phone": ["M440 540 h200 a30 30 0 0 1 30 30 v400 a30 30 0 0 1 -30 30 h-200 a30 30 0 0 1 -30 -30 v-400 a30 30 0 0 1 30 -30 z",
              "M510 580 h60", "M540 950 v2"],
    "wallet": ["M370 640 h340 a20 20 0 0 1 20 20 v240 a20 20 0 0 1 -20 20 h-340 a20 20 0 0 1 -20 -20 v-240 a20 20 0 0 1 20 -20 z",
               "M730 730 h-90 a40 40 0 0 0 0 80 h90", "M650 770 v2", "M390 640 l260 -80 l30 80"],
    "chip": ["M430 650 h220 v220 h-220 z", "M480 700 h120 v120 h-120 z",
             "M460 650 v-40 M500 650 v-40 M540 650 v-40 M580 650 v-40 M620 650 v-40 M460 870 v40 M500 870 v40 M540 870 v40 M580 870 v40 M620 870 v40"],
    "robot": ["M400 640 h280 a40 40 0 0 1 40 40 v200 a40 40 0 0 1 -40 40 h-280 a40 40 0 0 1 -40 -40 v-200 a40 40 0 0 1 40 -40 z",
              "M480 760 v40 M600 760 v40 M490 860 h100", "M540 640 v-70 M540 552 m-18 0 a18 18 0 1 0 36 0 a18 18 0 1 0 -36 0"],
    "warning": ["M540 560 L760 940 H320 Z", "M540 700 v120", "M540 870 v2"],
    "question": ["M440 660 C440 520 640 520 640 650 C640 740 540 750 540 840 V880", "M540 960 v2"],
    "bank": ["M360 680 L540 580 L720 680 Z", "M390 720 v170 M470 720 v170 M610 720 v170 M690 720 v170", "M350 930 h380"],
    "globe": ["M540 760 m-190 0 a190 190 0 1 0 380 0 a190 190 0 1 0 -380 0", "M350 760 h380",
              "M540 570 C440 650 440 870 540 950 C640 870 640 650 540 570"],
    "coin": ["M540 760 m-170 0 a170 170 0 1 0 340 0 a170 170 0 1 0 -340 0", "M540 760 m-120 0 a120 120 0 1 0 240 0 a120 120 0 1 0 -240 0",
             "M575 715 C565 700 512 700 512 725 C512 750 570 745 570 770 C570 796 518 796 508 780 M540 690 v140"],
    "person": ["M540 640 m-70 0 a70 70 0 1 0 140 0 a70 70 0 1 0 -140 0", "M400 940 C400 820 470 760 540 760 C610 760 680 820 680 940"],
    "people": ["M420 680 m-55 0 a55 55 0 1 0 110 0 a55 55 0 1 0 -110 0", "M660 680 m-55 0 a55 55 0 1 0 110 0 a55 55 0 1 0 -110 0",
               "M310 920 C310 820 360 780 420 780 C480 780 530 820 530 920 M550 920 C550 820 600 780 660 780 C720 780 770 820 770 920"],
    "doc": ["M420 560 h180 l80 80 v320 h-260 z", "M600 560 v80 h80", "M470 720 h160 M470 780 h160 M470 840 h110"],
    "camera": ["M370 660 h340 a20 20 0 0 1 20 20 v220 a20 20 0 0 1 -20 20 h-340 a20 20 0 0 1 -20 -20 v-220 a20 20 0 0 1 20 -20 z",
               "M540 790 m-80 0 a80 80 0 1 0 160 0 a80 80 0 1 0 -160 0", "M460 660 l30 -50 h100 l30 50"],
    "mic": ["M500 580 h80 a40 40 0 0 1 40 40 v140 a80 80 0 0 1 -160 0 v-140 a40 40 0 0 1 40 -40 z",
            "M420 760 a120 120 0 0 0 240 0", "M540 880 v70 M470 950 h140"],
    "clock": ["M540 760 m-190 0 a190 190 0 1 0 380 0 a190 190 0 1 0 -380 0", "M540 760 V640 M540 760 L630 820"],
    "building": ["M420 960 V600 h240 v360", "M460 660 h40 M580 660 h40 M460 740 h40 M580 740 h40 M460 820 h40 M580 820 h40", "M380 960 h320"],
    "rocket": ["M540 560 C620 640 640 760 610 860 H470 C440 760 460 640 540 560 Z", "M540 700 m-30 0 a30 30 0 1 0 60 0 a30 30 0 1 0 -60 0",
               "M470 830 L410 910 L480 890 M610 830 L670 910 L600 890", "M510 890 L540 960 L570 890"],
    "plane": ["M330 780 L750 640 L700 700 L560 780 L700 860 L750 920 Z", "M560 780 L470 940 L440 940 L480 800"],
    "chart": ["M360 960 V600 M360 960 H740", "M400 900 L500 820 L580 860 L700 680", "M650 680 h50 v50"],
    "down": ["M360 960 V600 M360 960 H740", "M400 660 L500 760 L580 720 L700 900", "M650 900 h50 v-50"],
    "eye": ["M330 760 C420 640 660 640 750 760 C660 880 420 880 330 760 Z", "M540 760 m-60 0 a60 60 0 1 0 120 0 a60 60 0 1 0 -120 0"],
    "brush": ["M660 560 L720 620 L560 780 L500 720 Z", "M500 720 C440 740 430 800 400 860 C460 850 520 840 560 780"],
    "atom": ["M540 760 m-30 0 a30 30 0 1 0 60 0 a30 30 0 1 0 -60 0", "M540 760 m-210 0 a210 80 0 1 0 420 0 a210 80 0 1 0 -420 0",
             "M540 760 m-210 0 a210 80 60 1 0 420 0 a210 80 60 1 0 -420 0"],
    "car": ["M330 860 V780 L400 680 H680 L750 780 V860 Z", "M420 860 m-45 0 a45 45 0 1 0 90 0 a45 45 0 1 0 -90 0", "M660 860 m-45 0 a45 45 0 1 0 90 0 a45 45 0 1 0 -90 0", "M420 690 L460 770 H620 L660 690"],
    "tag": ["M400 600 h200 l140 160 l-140 160 h-200 z", "M460 760 m-25 0 a25 25 0 1 0 50 0 a25 25 0 1 0 -50 0"],
    "handshake": ["M330 780 L430 700 L520 740 L610 690 L750 780", "M430 700 L380 820 M610 690 L700 840", "M480 800 l60 60 l60 -40"],
    "ice": ["M410 620 h260 v280 h-260 z", "M540 760 m-80 0 a80 80 0 1 0 160 0 a80 80 0 1 0 -160 0", "M430 650 l40 40 M640 870 l-30 -30"],
}


def icon(name, label, c=Y):
    paths = ICONS[name]
    svg = ("<svg><g transform='translate(540 760) scale(1.35) translate(-540 -760)'>"
           + "".join(ln(p, .1 + i * .25, .6, c, 6) for i, p in enumerate(paths)) + "</g></svg>")
    return svg + (lab(540, 1040, label, .5, c) if label else "")


def count(v0, v1, pre="", suf="", label="", c=GRN, exp=False, d=2.2):
    e = " data-exp=1" if exp else ""
    return (f"<div class=big data-in='.1' style='left:540px;top:640px;color:#fff;opacity:0' data-count='{v1}' data-from='{v0}' "
            f"data-at='.15' data-d='{d}'{e} data-pre='{pre}' data-suf='{suf}'>{pre}{v0:,}{suf}</div>"
            + "<svg>" + ln("M300 820 H780", .2, 1.0, c, 6) + "</svg>" + (lab(540, 880, label, .5, c) if label else ""))


def curve(kind="up", label="", c=GRN):
    d = "M170 1100 C 560 1095 760 1050 840 860 S 905 520 925 470" if kind == "up" else "M170 520 C 420 540 520 640 640 860 S 860 1080 925 1100"
    return ("<svg>" + ln("M170 1110 H930 M170 1110 V460", 0, .4, "#3a3a42", 3) + ln(d, .2, 1.6, c, 8) + "</svg>"
            + (lab(540, 1150, label, .4, GREY) if label else ""))


def compare(items):
    """2D bars: items = [(label, value, color)], value 0..1"""
    n = len(items)
    w = 640 // n
    out = "<svg>" + ln("M200 1060 H880", 0, .4, "#3a3a42", 3)
    labs = ""
    for i, (t, v, c) in enumerate(items):
        x = 220 + i * w + w // 2 - 10
        h = int(520 * v)
        out += ln(f"M{x} 1060 V{1060 - h}", .3 + i * .35, .9, c, 70)
        labs += lab(x, 1090, t, .4 + i * .35, c)
    return out + "</svg>" + labs


def stamp(word, c=RED, sub=""):
    return (f"<div class=big data-in='.05' data-shake='.05' style='left:540px;top:680px;color:{c};opacity:0;font-size:120px'>{word}</div>"
            + (lab(540, 860, sub, .4, GREY) if sub else ""))


def checklist(items, c=GRN, title=""):
    out = "<svg>"
    labs = ""
    y0 = 560
    for i, t in enumerate(items):
        y = y0 + i * 150
        out += ln(f"M210 {y} l30 30 l60 -60", .2 + i * .45, .35, c, 9)
        labs += (f"<div data-in='{.3 + i * .45}' style='position:absolute;left:330px;top:{y - 38}px;width:640px;"
                 f"font:700 40px/1.2 Jakarta;color:#fff;opacity:0'>{t}</div>")
    if title:
        labs += lab(540, 420, title, 0, Y)
    return out + "</svg>" + labs


def cta(word, sub):
    return (f"<div class=pill data-in='.2' data-pulse='.8' style='top:900px;opacity:0'>{word}</div>" + lab(540, 1030, sub, .5, GREY))


def visual(v):
    """Turn a compact tuple into scene dict fields."""
    kind, *a = v
    if kind == "3d":
        return {"three": a[0], "html": lab(540, 220, a[1], .4, a[2] if len(a) > 2 else Y) if len(a) > 1 else ""}
    f = {"icon": icon, "count": count, "curve": curve, "compare": compare, "stamp": stamp, "list": checklist, "cta": cta}[kind]
    return {"html": f(*a)}


# ---------- timing ----------
def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def align(sentences, words):
    """Anchor script words to transcript words that match exactly (in order); interpolate the rest."""
    tw = [(w[0], norm(w[2])) for w in words if norm(w[2])]
    flat = [w for s in sentences for w in s.split()]
    sn = [norm(w) for w in flat]
    times = [None] * len(flat)
    j = 0
    for i, w in enumerate(sn):
        if not w:
            continue
        for k in range(j, min(j + 8, len(tw))):
            if tw[k][1] == w:
                times[i] = tw[k][0]
                j = k + 1
                break
    # interpolate gaps
    last_t, last_i = 0.0, -1
    known = [(i, t) for i, t in enumerate(times) if t is not None] + [(len(flat), words[-1][1])]
    out_t = [0.0] * len(flat)
    ki = 0
    prev_i, prev_t = -1, 0.0
    for i_k, t_k in known:
        for i in range(prev_i + 1, i_k):
            frac = (i - prev_i) / (i_k - prev_i)
            out_t[i] = round(prev_t + (t_k - prev_t) * frac, 2)
        if i_k < len(flat):
            out_t[i_k] = round(t_k, 2)
        prev_i, prev_t = i_k, t_k
    res, p = [], 0
    for s in sentences:
        n = len(s.split())
        res.append(out_t[p:p + n])
        p += n
    return res


NUMW = set("zero one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion percent point".split())
STOP = set("the a an and or but so to of in on for with is are was were it its it's that this you your my i we they he she be by at as from not no can will just than then there their our".split())


def keywords(text, vis):
    """Highlight numbers, words echoed by the on-screen visual, else the strongest word near the end."""
    ws = text.split()
    shown = ""
    if vis:
        shown = " ".join(str(x) for x in vis[1:] if isinstance(x, str)).lower()
    keys = []
    for i, w in enumerate(ws):
        n = norm(w)
        if not n:
            continue
        if n in NUMW or n.replace("-", "").isdigit() or any(ch.isdigit() for ch in n) or w.isupper() and len(n) > 1:
            keys.append(i)
        elif n not in STOP and len(n) > 3 and n in norm(shown) and len(keys) < 3:
            keys.append(i)
    if not keys:
        cand = [i for i, w in enumerate(ws) if norm(w) not in STOP and len(norm(w)) > 4]
        keys = cand[-1:] if cand else []
    return keys


def build(reel, transcript_words, audio, dur_tail=2.6):
    """reel = {"beats": [(sentence, visual or None, key_word_indexes, color)], "sfx": [...]}"""
    sents = [b[0] for b in reel["beats"]]
    times = align(sents, transcript_words)
    end_audio = transcript_words[-1][1]
    phrases, scenes = [], []
    for i, (b, ts) in enumerate(zip(reel["beats"], times)):
        text, vis = b[0], b[1]
        key = keywords(text, vis)
        col = b[3] if len(b) > 3 else Y
        nxt = times[i + 1][0] if i + 1 < len(times) else end_audio + .3
        phrases.append({"a": ts[0], "b": nxt - .05, "key": key, "color": col,
                        "words": [{"w": w, "t": t} for w, t in zip(text.split(), ts)]})
        if vis is not None:
            if scenes:
                scenes[-1]["b"] = ts[0]
            sc = visual(vis)
            sc["a"] = 0 if not scenes else ts[0]
            scenes.append(sc)
    dur = round(end_audio + dur_tail, 2)
    scenes[-1]["b"] = dur
    phrases[-1]["b"] = dur - .3
    return {"dur": dur, "scenes": scenes, "phrases": phrases, "audio": audio, "sfx": reel.get("sfx", [])}
