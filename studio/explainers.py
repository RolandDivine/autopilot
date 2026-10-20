"""Explainer Reels from the Fish ELITE audio bank (assets/vo/exNN-*.mp3, 18 Oct 2026).

    python studio/explainers.py ex01-halving            -> assets/reels/ex01-halving.mp4
    python studio/explainers.py ex01-halving 5 30 60    -> preview PNGs
Setup per video: assets/viral/<name>/voice.{mp3,json} and /home/claude/money_audio/<name>.wav (see prep()).
"""
import asyncio
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import viral  # noqa: E402

ROOT = viral.ROOT
GEN = ROOT / "assets" / "gen"
FOLLOW = viral.FOLLOW


def prep(name):
    d = ROOT / "assets" / "viral" / name
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "assets" / "vo" / f"{name}.mp3", d / "voice.mp3")
    shutil.copy(ROOT / "assets" / "vo" / f"{name}.json", d / "voice.json")
    Path("/home/claude/money_audio").mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(d / "voice.mp3"), "-ar", "44100", "-ac", "1",
                    f"/home/claude/money_audio/{name}.wav"], check=True)


def halving_spec():
    def timeline(at, dur):
        t_every, t_cuts, t_new, t_blocks = at("every"), at("cuts"), at("new"), at("every", 15)
        t_2009, t_april, t_next, t_why = at("2009"), at("april"), at("next"), at("why")
        t_fewer, t_21, t_careful, t_past = at("fewer"), at("21"), at("careful"), at("past")
        t_markets, t_learn, t_see = at("markets"), at("learn"), at("see")
        bgs = [(-1, dur + 1, GEN / "hourglass-half.jpg")]
        cards = [
            {"kind": "html", "a": -1, "b": t_cuts - .1,
             "html": "<div class='kick'>Crypto · explained</div><div class='mid'>Every ~4 years, Bitcoin does what<br><span class='yel'>no central bank does.</span></div>"},
            {"kind": "stat", "a": t_cuts, "b": t_new - .1, "kick": "The halving", "value": "½", "cls": "yel",
             "label": "It cuts its own money printing in half"},
            {"kind": "html", "a": t_new, "b": t_blocks - .1,
             "html": "<div class='kick'>Where new bitcoin comes from</div><div class='mid'>A reward paid to <span class='yel'>miners</span>,</div>"
                     "<div class='sm' style='margin-top:16px'>the computers that secure the network.</div>"},
            {"kind": "stat", "a": t_blocks, "b": t_2009 - .1, "kick": "Every 210,000 blocks", "value": "~4 years", "cls": "yel",
             "label": "the block reward halves"},
            {"kind": "bars", "a": t_2009, "b": t_next - .1, "kick": "Bitcoin per block", "title": "The reward keeps halving", "max": 50,
             "bars": [{"t": "50", "v": 50, "q": "2009"}, {"t": "25", "v": 25, "q": "2012"}, {"t": "12.5", "v": 12.5, "q": "2016"},
                      {"t": "6.25", "v": 6.25, "q": "2020"}, {"t": "3.125", "v": 3.125, "q": "Apr 2024"}]},
            {"kind": "timeline", "a": t_next, "b": t_why - .1, "kick": "What's next", "title": "The next halving",
             "pts": [{"x": 15, "t": "Apr 2024", "s": "3.125 BTC"}, {"x": 55, "t": "~2028", "s": "1.5625 BTC"},
                     {"x": 88, "t": "~2140", "s": "last bitcoin"}]},
            {"kind": "stat", "a": t_why, "b": t_careful - .1, "kick": "Why it matters", "value": "21M", "cls": "yel",
             "label": "the most bitcoin that will ever exist", "sub": "Fewer new coins every day"},
            {"kind": "html", "a": t_careful, "b": t_learn - .1,
             "html": "<div class='kick'>But careful</div><div class='mid'>Past halvings came before big price runs.</div>"
                     "<div class='mid red' style='margin-top:14px'>That's not a rule.</div>"
                     "<div class='sm' style='margin-top:16px'>The halving is known years in advance.</div>"},
            {"kind": "html", "a": t_learn, "b": t_see - .3,
             "html": "<div class='kick'>Kobo's rule</div><div class='mid'>Learn how it works.<br><span class='yel'>Don't bet your rent on a pattern.</span></div>"
                     "<div class='sm' style='margin-top:16px'>Education, not financial advice.</div>"},
            {"kind": "html", "a": t_see - .3, "b": dur + 1, "html": FOLLOW.format("Crypto, explained straight.")},
        ]
        return bgs, cards

    return viral.std("ex01-halving", timeline)


SPECS = {"ex01-halving": halving_spec}

if __name__ == "__main__":
    name = sys.argv[1]
    prep(name)
    pv = [float(x) for x in sys.argv[2:]]
    out = ROOT / "assets" / "reels" / f"{name}.mp4"
    print(asyncio.run(viral.render(SPECS[name](), out, pv or None)))
