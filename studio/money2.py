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
duo.BG = {6: GEN / "kobo-bg-phone.jpg", 7: GEN / "kobo-bg-phone.jpg", 8: GEN / "kobo-bg-market.jpg", 9: GEN / "kobo-bg-mango.jpg", 10: GEN / "kobo-bg-phone.jpg"}
duo.CARDS = {
    6: [(4.9, 12.8, "💸", "Paid Friday, broke Wednesday", "Where does the money go?"),
        (13.3, 17.6, "🧾", "Small things add up", "Snacks · data · rides · little transfers"),
        (18.2, 37.9, "🥧", "The 50/30/20 rule", "50% needs · 30% wants · 20% future"),
        (37.9, 43.4, "🏦", "Pay your future first", "20% moves out the day money lands"),
        (43.6, 56.0, "📝", "Track one month", "She found $300 a year she forgot about"),
        (56.2, 65.5, "🗺️", "A budget is a map", "Not a cage"),
        (65.6, 71.0, "⏭️", "Next: the surprise bill", "Follow so you don't miss it")],
    7: [(5.0, 14.9, "📱", "The phone breaks", "Repair: $400"),
        (14.9, 21.0, "📈", "Tunde borrowed", "With interest, $400 became $600"),
        (21.0, 31.9, "🛟", "Ada has an emergency fund", "Money only for surprises"),
        (32.0, 35.6, "🚫", "Not for sales or parties", "Job loss · hospital · broken phone"),
        (35.6, 45.6, "📏", "How much?", "3–6 months of basic expenses. Start with 1"),
        (45.6, 55.1, "🏦", "Where?", "Safe and easy to reach. Not crypto, not shares"),
        (55.2, 64.6, "✅", "Crisis → inconvenience", "That's what the fund does"),
        (64.6, 69.0, "⏭️", "Next: good debt vs bad debt", "Follow so you don't miss it")],
    8: [(3.6, 14.4, "⚖️", "Not all debt is the same", "Some pays you. Some eats you"),
        (14.4, 17.5, "✅", "Good debt", "Cheetie's loan buys a machine that earns more"),
        (17.5, 30.9, "❌", "Bad debt", "Emeka: 40% interest for sneakers"),
        (30.9, 42.4, "🧪", "The simple test", "Will it help me earn or save more than it costs?"),
        (42.4, 49.5, "🪤", "Trap 1: minimum payments", "Pay only the minimum and you pay for years"),
        (49.5, 56.2, "📱", "Trap 2: loan apps", "Huge fees, harassment when you miss a payment"),
        (56.2, 64.9, "📋", "Already in debt?", "List them all. Pay the most expensive first"),
        (64.9, 70.7, "⏭️", "Next: what is Bitcoin, really?", "Follow so you don't miss it")],
    9: [(7.4, 17.4, "📒", "A shared notebook", "Every payment, copied on thousands of computers"),
        (17.4, 25.6, "🚫", "No bank owns it", "To cheat, you'd have to fool most of them at once"),
        (25.6, 32.6, "⛓️", "That notebook = a blockchain", "Bitcoin is the money that lives on it"),
        (35.5, 42.6, "🔢", "Only 21 million, ever", "Nobody can print more"),
        (42.6, 48.4, "🌍", "Send to anyone, anywhere", "No bank needed"),
        (48.4, 57.0, "📉", "The honest part", "It has dropped more than 70% before"),
        (57.0, 63.6, "🏠", "Never your rent money", "Never your emergency fund"),
        (63.6, 70.0, "⏭️", "Next: where do you keep crypto?", "Follow so you don't miss it")],
    10: [(6.1, 12.3, "🏦", "Option 1: the exchange", "Easy, but the exchange holds the keys"),
         (12.3, 19.9, "⚠️", "If it's hacked or goes bust", "Like FTX in 2022, coins can get stuck"),
         (19.9, 32.9, "🔑", "Option 2: your own wallet", "A wallet holds keys, not coins"),
         (32.9, 43.9, "📝", "The seed phrase", "12 or 24 words. Whoever has them has the money"),
         (43.9, 54.4, "🚫", "Kobo's rules", "Paper only. No screenshot, cloud or chat"),
         (54.4, 63.0, "🙅🏾", "Never type it into a website", "No real support agent will ever ask"),
         (63.0, 70.1, "⚖️", "Not your keys, not your coins", "Lose your keys, lose your coins"),
         (70.1, 74.0, "⏭️", "Next: the digital dollar", "Follow so you don't miss it")],
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
