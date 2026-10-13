"""Kobo's Money Story: solo Kobo Reels on saving, investing and capital markets.

Usage from studio/: python money.py 1 [2 ...]  -> ../assets/reels/kobo-money-part-N.mp4
Audio + transcripts live in /home/claude/money_audio (partN.wav, partN.json).
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import duo

duo.AUDIO = Path("/home/claude/money_audio")
duo.SERIES = "Kobo's Money Story"
duo.SUBTITLE = "saving &amp; investing, made simple"
duo.TOTAL_PARTS = 5
duo.SLUG = "kobo-money-part"
duo.SOLO = True
duo.TURNS = {n: [(0.0, "K")] for n in range(1, 6)}
duo.FIX = {r"\bAdjo,": "Ajo,", r"\bIsusu,": "esusu,", r"\bLegos\b": "Lagos"}
duo.CARDS = {
    1: [(6.5, 12.4, "👥", "Same salary", "₦100,000 a month each"),
        (29.1, 38.9, "💡", "Pay yourself first", "Save before you spend, not after"),
        (39.2, 48.3, "📅", "One year later", "Tunde: sneakers. Ada: ₦240,000"),
        (48.5, 60.5, "🧺", "Ajo / esusu", "Small amounts, every time, add up"),
        (60.8, 70.8, "✅", "Lesson 1", "It's not what you earn, it's what you keep")],
    2: [(13.1, 24.8, "🧊", "Inflation", "Prices go up, so the same money buys less"),
        (25.0, 40.0, "🍛", "₦1,000 → ₦1,200", "Same money, fewer plates of jollof"),
        (40.3, 51.7, "🪜", "Step 1 save, step 2 grow", "Grow money faster than prices rise"),
        (51.9, 58.3, "📈", "Next: investing", "Follow so you don't miss it")],
}

if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        print(asyncio.run(duo.render_part(n)))
