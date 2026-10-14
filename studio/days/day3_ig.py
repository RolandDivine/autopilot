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

buy1 = [
    [("q", "Roland, I want to buy my first crypto. How do I not get scammed? 😬"),
     ("r", "Smart question. Here's my **5-step safety checklist.**"),
     ("r", "Works in any country. Swipe → 👇")],
    [("r", "**Step 1: pick a regulated exchange.**"),
     ("r", "Check your country's financial regulator list ==before== you sign up."),
     ("r", "Download the app from the **official website**, not from an ad link.")],
    [("r", "**Step 2: lock the door first.** 🔒"),
     ("r", "Strong unique password + 2FA with an ==authenticator app== (not SMS)."),
     ("q", "And if \"support\" DMs me?"),
     ("r", "Real support ==never DMs you first.== Block them.")],
    [("r", "**Step 3: start with a test amount.**"),
     ("r", "Buy a little → send a little to your wallet → check it arrived."),
     ("r", "Only then move more. ==Crypto mistakes can't be undone.==")],
    [("r", "**Step 4: know your local rules.** 🌍"),
     ("q", "Like what?"),
     ("r", "Example, Nigeria 🇳🇬: Binance stopped naira deposits and P2P in 2024. Use **SEC-licensed** platforms."),
     ("r", "Buying P2P? ==Wait for the money in your bank==, not a screenshot.")],
    [("r", "**Step 5: guard your recovery phrase.** 🗝️"),
     ("r", "Those 12–24 words = ==full access to your money.=="),
     ("r", "Write it on paper. Never type it into a website or chat. Anyone asking for it is a thief.")],
    [("q", "Saving this right now 📌"),
     ("r", "**Save it** for when you're ready to buy 📌"),
     ("r", "Send it to the friend who just said \"I want to try crypto\" 😄"),
     ("r", "Follow **@defi_ring_master** for practical crypto, no hype. Not financial advice.")],
]

robot1 = [
    [("q", "Roland, how are you posting 3 times a day while running companies? 👀"),
     ("r", "I don't. **My robot does.** 🤖"),
     ("r", "I built it with AI. Swipe for the blueprint → 👇")],
    [("q", "Wait, you built your own posting robot??"),
     ("r", "Yes. It posts to LinkedIn and Instagram at **8 AM, 1 PM and 7 PM.**"),
     ("r", "I review everything the night before and can ==cancel any post with one comment.==")],
    [("r", "**Step 1: describe it in plain words.**"),
     ("r", "\"Post my content at 8, 1 and 7. Let me review it the night before. Let me cancel anything.\""),
     ("r", "That was ==the whole plan.==")],
    [("r", "**Step 2: use free building blocks.** 🧱"),
     ("r", "📦 GitHub: stores the posts and runs them on a timer\n📲 Official LinkedIn + Instagram tools\n🤖 Claude (AI): wrote and fixed the code"),
     ("q", "No developer team? 😮"), ("r", "==None.==")],
    [("r", "**Step 3: ship it, then fix what breaks.**"),
     ("r", "Day 2: GitHub's timer ran **hours late**. So we added a backup trigger."),
     ("r", "==Real use finds real problems.== That's normal.")],
    [("r", "**The blueprint has changed.** 🚀"),
     ("r", "Before: a team, months, lots of money.\nNow: ==one person, days, mostly free tools.=="),
     ("r", "The skill now is knowing **what** to build, and steering the AI.")],
    [("q", "What should I build first? 🤔"),
     ("r", "The task that **annoys you every week.** Start there."),
     ("r", "Send this to the friend who keeps saying \"I have an idea\" 😄"),
     ("r", "Follow **@defi_ring_master** and build with me 🛠️")],
]

stories = {
    "s0900": [("r", "**New post is up** ☀️"), ("r", "$672 million of borrowed-money bets got wiped out in one day. Here's why."),
              ("r", "Tap my profile to read it 👆")],
    "s1100": [("r", "**Quick quiz** 🧠"), ("q", "Someone buying your crypto sends a screenshot of their payment. You…\n\nA) release the crypto\nB) wait until the money shows in your bank"),
              ("r", "Reply with **A or B** 👇 Answer at 2 PM.")],
    "s1400": [("r", "**Answer: B** ✅"), ("r", "Fake payment screenshots are one of the most common crypto scams. Only the money in your account counts."),
              ("r", "Full safety checklist is on my page 📌")],
    "s1700": [("r", "**Real talk** 🛠️"), ("r", "I have ==six products== I built but never launched."),
              ("r", "The blocker was money for building. AI has made building cheaper and faster, so I'm changing my approach:"),
              ("r", "**Push it out. Let people test it.** Then decide. Build with me 👇")],
    "s2100": [("r", "**Tomorrow** 📅"), ("r", "More real questions, answered properly."),
              ("q", "What do YOU want to know about crypto, AI or building?"),
              ("r", "Send me your question 👇 and ==turn on notifications== 🔔")],
}

if __name__ == "__main__":
    print(carousel(news, "Market news", IG, "news3")[-1])
    print(carousel(buy1, "Crypto safety guide", IG, "buy1")[-1])
    print(carousel(robot1, "Build in public", IG, "robot1")[-1])
    for k, v in stories.items():
        print(story(v, "Daily story", ST, k))
