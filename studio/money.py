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
duo.FIX = {r"\bAdjo,": "Ajo,", r"\bIsusu,": "esusu,", r"\bLegos\b": "Lagos", r"\bCobo\b": "Kobo", r"\bKubo\b": "Kobo",
           r"\bKubo's": "Kobo's", r"\bNara\b": "naira", r"\bchinchin\b": "chin-chin", r"\bexchange,": "Exchange,", r"\bhow\b(?= money grows)": "her"}
GEN = Path(__file__).resolve().parents[1] / "assets" / "gen"
duo.BG = {3: GEN / "kobo-bg-mango.jpg", 4: GEN / "kobo-bg-market.jpg", 5: GEN / "kobo-bg-phone.jpg"}
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
    3: [(6.6, 12.9, "🥭", "Buy the tree", "Not just the mangoes"),
        (18.9, 28.8, "🌱", "Things that grow or pay you", "Money market funds · T-bills · shares"),
        (28.8, 44.4, "🔁", "Compounding", "₦240,000 → ₦264,000 → interest on interest"),
        (44.6, 54.8, "📏", "3 rules", "Understand it · spread it · be patient"),
        (54.8, 60.1, "🏛️", "Next: the capital market", "Follow so you don't miss it")],
    4: [(5.2, 14.3, "🏭", "Chidi needs a factory", "The bank's interest is too high"),
        (14.8, 22.0, "🏛️", "The capital market", "Where companies raise long-term money from the public"),
        (22.6, 36.3, "🧩", "Option 1: shares", "Own a piece · it can grow · dividends"),
        (37.0, 43.5, "📜", "Option 2: bonds", "You lend · they pay interest · then pay you back"),
        (43.9, 48.0, "🇳🇬", "In Nigeria", "Nigerian Exchange, watched by the SEC"),
        (52.8, 56.6, "⚠️", "Shares can go down too", "Learn before you buy"),
        (57.1, 63.4, "🚩", "Next: spot the scam", "Follow so you don't miss it")],
    5: [(6.4, 13.9, "🚩", "\"Double your money in 30 days\"", "The classic bait"),
        (25.4, 29.5, "🔺", "Ponzi scheme", "Old investors paid with new investors' money"),
        (29.6, 48.3, "🛑", "4 red flags", "Guaranteed returns · hurry · recruit · unregistered"),
        (48.6, 55.2, "🔎", "Check the regulator", "In Nigeria: the SEC"),
        (55.2, 59.1, "✅", "Save · grow · protect", "Share this with someone who needs it")],
}

if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        print(asyncio.run(duo.render_part(n)))
