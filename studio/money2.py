"""Kobo's Money Story, Season 2 (parts 6-15): solo Kobo Reels voiced on Fish ELITE (audio bank, 18 Oct 2026).

Usage from repo root: python studio/money2.py 6 [7 ...]  -> assets/reels/kobo-money-part-N.mp4
Audio: assets/vo/koboNN.mp3 + koboNN.json, copied to /home/claude/money_audio2/partN.wav/json first.
"""
import asyncio
import subprocess
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import duo  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
duo.AUDIO = Path("/home/claude/money_audio2")
duo.SERIES = "Kobo's Money Story"
duo.SUBTITLE = "Season 2 · money, made simple"
duo.TOTAL_PARTS = 15
duo.SLUG = "kobo-money-part"
duo.SOLO = True
duo.TURNS = {n: [(0.0, "K")] for n in range(6, 16)}
duo.FIX = {r"\bCobo\b": "Kobo", r"\bKubo\b": "Kobo", r"\bKubo's": "Kobo's"}
GEN = ROOT / "assets" / "gen"
duo.BG = {6: GEN / "kobo-bg-phone.jpg", 7: GEN / "kobo-bg-phone.jpg", 8: GEN / "kobo-bg-market.jpg"}
duo.CARDS = {
    6: [(4.9, 12.8, "💸", "Paid Friday, broke Wednesday", "Where does the money go?"),
        (13.3, 17.6, "🧾", "Small things add up", "Snacks · data · rides · little transfers"),
        (18.2, 37.9, "🥧", "The 50/30/20 rule", "50% needs · 30% wants · 20% future"),
        (37.9, 43.4, "🏦", "Pay your future first", "20% moves out the day money lands"),
        (43.6, 56.0, "📝", "Track one month", "She found $300 a year she forgot about"),
        (56.2, 65.5, "🗺️", "A budget is a map", "Not a cage"),
        (65.6, 71.0, "⏭️", "Next: the surprise bill", "Follow so you don't miss it")],
}


def prep(n):
    src = ROOT / "assets" / "vo" / f"kobo{n:02d}"
    duo.AUDIO.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{src}.mp3", "-ar", "44100", "-ac", "1",
                    str(duo.AUDIO / f"part{n}.wav")], check=True)
    shutil.copy(f"{src}.json", duo.AUDIO / f"part{n}.json")


if __name__ == "__main__":
    args = sys.argv[1:]
    pv = [float(x) for x in args[1:]] if len(args) > 1 else None
    for n in map(int, args[:1] if pv else args):
        prep(n)
        print(asyncio.run(duo.render_part(n, pv)))
