"""Pinned intro post for @defi_ring_master (Chat Bubbles). Run from studio/: python days/intro_ig.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ig_chat import carousel

OUT = Path(__file__).resolve().parents[2] / "assets" / "intro"

slides = [
    [("q", "Wait… who are you and why should I follow? 🤔"),
     ("r", "Hi 👋🏾 I'm **Roland**. I build in crypto and AI."),
     ("r", "For the next 150 days I'm teaching both **from zero**. No jargon. No hype."), ("r", "Swipe → 👇")],
    [("q", "How did you even get into crypto?"),
     ("r", "2019. I was in 300 level at UNIBEN when a friend mentioned \"trading digital assets\"."),
     ("r", "It clicked fast, because my grandpa used to show me ==the stock pages in the newspaper.==")],
    [("q", "So it's been smooth since then?"),
     ("r", "Not at all 😅 I made **every beginner mistake**: borrowed money, too much risk, greed."),
     ("r", "I lost it all in ==one morning.== It took me 3 months away and a full year of practice to come back."),
     ("r", "That's why I teach ==risk first.==")],
    [("q", "What will I actually learn here?"),
     ("r", "**3 things, one lesson a day:**"),
     ("r", "₿ **Crypto:** what it is, how to stay safe, how to think about investing\n🤖 **AI:** use it to work faster and get jobs\n🛠️ **Build:** launch your own product")],
    [("q", "And the end goal?"),
     ("r", "**Launch Day: 4 Feb 2027.**"),
     ("r", "By then you'll understand crypto and AI, and you'll have ==launched something real.=="),
     ("r", "I'm building in public alongside you 🤝🏾")],
    [("q", "Ok I'm in. Where do I start? 🙋🏾"),
     ("r", "**Follow @defi_ring_master** and turn on post notifications 🔔"),
     ("r", "📌 Save this post so you can come back to it"),
     ("r", "📤 Send it to the friend who keeps asking you about crypto or AI 😄"),
     ("r", "Education, not financial advice.")],
]

CAPTION = (
    "Start here 👋🏾\n\n"
    "I'm Roland. I build in crypto and AI, and for the next 150 days I'm teaching both from zero, "
    "plus how to launch your own product.\n\n"
    "1 easy lesson a day. Plain words. No hype.\n\n"
    "📌 Save this\n📤 Send it to a friend who's curious about crypto or AI\n\n"
    "Education, not financial advice.\n\n#crypto #ai #learncrypto #buildinpublic #lagos"
)

if __name__ == "__main__":
    print(carousel(slides, "Start here", OUT, "intro"))
