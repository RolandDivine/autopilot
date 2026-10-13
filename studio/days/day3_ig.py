"""Day 3 · Wed 14 Oct 2026 · Instagram in the Chat Bubbles style. Run from studio/: python days/day3_ig.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ig_chat import carousel, story

Q = Path(__file__).resolve().parents[2] / "queue" / "2026-10-14"
IG, ST = Q / "instagram", Q / "stories"

news = [
    [("q", "Roland, what happened in crypto yesterday? 😳"),
     ("r", "Bitcoin slipped from about **$84,200 to $81,000**."),
     ("r", "And in one day, ==$672 million== of borrowed-money bets got wiped out."),
     ("q", "Wiped out how??")],
    [("r", "People borrowed money to make **bigger bets** on prices going up."),
     ("r", "When the price fell, the exchange closed their trades automatically. That's called a ==liquidation==."),
     ("r", "**$586M** of it was people betting on prices going UP.")],
    [("q", "So what's the lesson?"),
     ("r", "Borrowed money makes wins bigger… and ==losses bigger too.=="),
     ("r", "And today at **1:30 PM Lagos**, the US inflation number lands. More swings are possible."),
     ("r", "Learn first. Never bet borrowed money. 📌 Save this.")],
]

crypto2 = [
    [("q", "Roland, everyone says \"blockchain\"… what actually is it? 🤔"),
     ("r", "It's simpler than it sounds. Think of an **ajo** 📒"),
     ("r", "Swipe → 👇")],
    [("r", "Your ajo group keeps **one book**: who paid, how much, when."),
     ("q", "Okay…"),
     ("r", "Problem: ==one person holds the book.== They could change it and nobody would know 😬")],
    [("r", "Now imagine **everyone in the group** has the same copy of the book."),
     ("q", "So if one person changes theirs?"),
     ("r", "Everyone else says ==\"that's not what my book says\"== ❌")],
    [("r", "A blockchain is that, but with **thousands of computers** around the world."),
     ("r", "Each page is a ==block==. Each block is linked to the one before it, like a ==chain==."),
     ("q", "Ahh, block + chain 💡")],
    [("q", "Who writes the new pages?"),
     ("r", "Special computers take turns, and they must ==put money on the line== to do it."),
     ("r", "If they cheat, **they lose money**. So honesty pays.")],
    [("r", "**Your 2-minute task:**"),
     ("r", "Explain blockchain to a friend using ==only the ajo book example.=="),
     ("r", "If they get it, you've got it too ✅")],
    [("q", "Wow, it finally makes sense 🙌"),
     ("r", "**Save this** so you can explain it next time 📌"),
     ("r", "Send it to the friend who keeps saying \"crypto is just a scam\" 😄"),
     ("r", "Follow **@defi_ring_master** for lesson 3: Bitcoin")],
]

build2 = [
    [("q", "Roland, what's this 150-day build challenge? 👀"),
     ("r", "We go from **no idea** to a **launched product**, together."),
     ("r", "Launch Day: ==4 Feb 2027==. Swipe → 👇")],
    [("q", "But I don't even have an idea 😅"),
     ("r", "**Perfect.** We don't start with ideas."),
     ("r", "We start with ==problems you face every week.==")],
    [("r", "**The road, in 5 stages:**"),
     ("r", "1️⃣ Find a real problem (by 10 Nov)\n2️⃣ Check people actually want it fixed (by 10 Dec)\n3️⃣ Build and test it (by 9 Jan)\n4️⃣ Get launch-ready\n5️⃣ ==Launch Day: 4 Feb== 🚀")],
    [("q", "Do I need to know how to code?"),
     ("r", "No. Many tools today let you build ==without code==, and AI helps a lot."),
     ("r", "We'll cover all of it, step by step.")],
    [("r", "**The rules:**"),
     ("r", "✅ Ship small, ship often\n✅ Show your work in public\n✅ Talk to real people\n✅ ==Done beats perfect==")],
    [("r", "**Your 2-minute task:**"),
     ("r", "Comment ==\"I'm in\"== and one thing that annoys you every week."),
     ("r", "That list is where we start 🛠️")],
    [("q", "I'm in 🙋🏾"),
     ("r", "**Save this** so you remember the dates 📌"),
     ("r", "Send it to the friend who always says \"I have an idea…\" 😄"),
     ("r", "Follow **@defi_ring_master** to build with me")],
]

stories = {
    "s0900": [("r", "**New post is up** ☀️"), ("r", "$672 million of borrowed-money bets got wiped out in one day. Here's why."),
              ("r", "Tap my profile to read it 👆")],
    "s1100": [("r", "**Quick quiz** 🧠"), ("q", "A blockchain is most like…\n\nA) one bank's private record book\nB) a record book everyone holds a copy of"),
              ("r", "Reply with **A or B** 👇 Answer at 2 PM.")],
    "s1400": [("r", "**Answer: B** ✅"), ("r", "Everyone holds the same copy, so nobody can quietly change the record."),
              ("r", "Full lesson is on my page 📌")],
    "s1700": [("r", "**Real talk** 🛠️"), ("r", "I have ==six products== I built but never launched."),
              ("r", "The blocker was money for building. AI has made building cheaper and faster, so I'm changing my approach:"),
              ("r", "**Push it out. Let people test it.** Then decide. Build with me 👇")],
    "s2100": [("r", "**Tomorrow** 📅"), ("r", "Crypto lesson 3: Bitcoin, explained for beginners.\nAI lesson 3: what an AI \"model\" really is."),
              ("r", "==Turn on post notifications== so you don't miss it 🔔")],
}

if __name__ == "__main__":
    print(carousel(news, "Market news", IG, "news3")[-1])
    print(carousel(crypto2, "Crypto lesson 2", IG, "crypto2")[-1])
    print(carousel(build2, "Builders lesson 2", IG, "build2")[-1])
    for k, v in stories.items():
        print(story(v, "Daily story", ST, k))
