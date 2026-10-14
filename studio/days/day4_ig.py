"""Day 4 · Thu 15 Oct 2026 · Instagram in the Chat Bubbles style. Run from studio/: python days/day4_ig.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ig_chat import carousel, story

Q = Path(__file__).resolve().parents[2] / "queue" / "2026-10-15"
IG, ST = Q / "instagram", Q / "stories"

news = [
    [("q", "Roland, why did Bitcoin drop yesterday? 📉"),
     ("r", "The US inflation number came out at **3.7%**."),
     ("r", "Markets expected **3.6%**. That tiny gap moved everything."),
     ("q", "Just 0.1%??")],
    [("r", "Yes. Hotter inflation → interest rates may go ==up again== → safe bonds pay more."),
     ("r", "So some money leaves risky things like crypto. Bitcoin fell about **$1,000 in minutes.**")],
    [("q", "So what's the lesson?"),
     ("r", "Markets move on ==surprises==, not on the number itself."),
     ("r", "Know the big dates. Don't panic-sell on a red candle. 📌 Save this.")],
]

wallet1 = [
    [("q", "Roland, which crypto wallet should I use? There are too many 😵‍💫"),
     ("r", "Let's make it simple. First, know the **2 kinds** of wallet."),
     ("r", "Swipe → 👇")],
    [("r", "**Custodial:** the exchange holds your keys. Like money in a **bank**."),
     ("r", "**Self-custody:** you hold the keys. Like ==cash in your own safe.=="),
     ("q", "Which is better?")],
    [("r", "Small amounts, still learning? A **regulated exchange** is fine."),
     ("r", "Holding for the long term? ==Your own wallet.==")],
    [("r", "**Hot wallet:** an app on your phone or browser. Easy, but online."),
     ("r", "**Cold wallet:** a small hardware device. Offline, ==hardest to hack.== 🔒")],
    [("r", "**Setting one up safely:**"),
     ("r", "1️⃣ Download from the **official site** only\n2️⃣ Write your recovery phrase on **paper**. No screenshots, no cloud\n3️⃣ ==Send a test amount first==")],
    [("q", "What mistakes should I avoid? 😬"),
     ("r", "❌ Wrong network: same coin, different chain = money lost\n❌ Fake wallet apps\n❌ \"Sync your wallet\" sites ==asking for your phrase==")],
    [("q", "This cleared everything up 🙌"),
     ("r", "**Save this** before you set up a wallet 📌"),
     ("r", "Send it to the friend who keeps all their crypto on one app 😅"),
     ("r", "Follow **@defi_ring_master** for practical crypto. Not financial advice.")],
]

aicv1 = [
    [("q", "Roland, can AI really help me get a job? 🤔"),
     ("r", "Yes, if you use it right. Here's how to write a CV that gets ==interviews.=="),
     ("r", "Swipe → 👇")],
    [("q", "Can't I just type \"write my CV\"?"),
     ("r", "You'll get a generic CV that sounds like ==everyone else's.== 😴"),
     ("r", "Instead, give it **the job ad** + **your real experience.**")],
    [("r", "**Step 1: the prompt** ✍🏾"),
     ("r", "\"Here is the job ad and my experience. Rewrite my bullet points for this role. Use numbers. ==Don't invent anything.==\"")],
    [("r", "**Step 2: turn duties into results.**"),
     ("r", "❌ \"Managed social media\"\n✅ \"Grew Instagram from 2k to 9k followers in 6 months\""),
     ("r", "Ask yourself: ==what did my work change?== (Use your own real numbers.)")],
    [("r", "**Step 3: beat the robot filter** 🤖"),
     ("r", "Many companies scan CVs with software first."),
     ("r", "Ask the AI: \"Which keywords from the job ad are ==missing from my CV?==\"")],
    [("r", "**Step 4: you have the final say.**"),
     ("r", "Read every line out loud. Is it **true**? Does it sound like **you**?"),
     ("r", "==AI drafts. You decide.== ✅")],
    [("q", "Doing this tonight 🙋🏾"),
     ("r", "**Save this** for your next application 📌"),
     ("r", "Send it to the friend who's been job hunting for months 🤝🏾"),
     ("r", "Follow **@defi_ring_master** for AI that does real work")],
]

stories = {
    "s0900": [("r", "**New post is up** ☀️"), ("r", "US inflation came in 0.1% hotter than expected, and Bitcoin dropped $1,000 in minutes. Here's why."),
              ("r", "Tap my profile to read it 👆")],
    "s1100": [("r", "**Quick quiz** 🧠"), ("q", "A website says: \"Type your 12-word phrase to sync your wallet.\" You…\n\nA) type it in\nB) close the site, it's a scam"),
              ("r", "Reply with **A or B** 👇 Answer at 2 PM.")],
    "s1400": [("r", "**Answer: B** ✅"), ("r", "No real wallet or exchange will ever ask for your recovery phrase. Anyone who has it can take everything."),
              ("r", "Full wallet guide is on my page 📌")],
    "s1700": [("r", "**How I actually use AI** 🧠"), ("r", "Every Sunday night I talk my week through with my AI agents. They're linked to my calendar and email, and they nudge me all week."),
              ("r", "But here's the truth: ==AI is an efficiency tool.== You still have to be the one with the ideas."),
              ("r", "You steer. AI speeds you up 🚀")],
    "s2100": [("r", "**Tomorrow** 📅"), ("r", "More real questions, answered properly."),
              ("q", "What do YOU want to know about crypto, AI or building?"),
              ("r", "Send me your question 👇 and ==turn on notifications== 🔔")],
}

if __name__ == "__main__":
    print(carousel(news, "Market news", IG, "news4")[-1])
    print(carousel(wallet1, "Crypto wallet guide", IG, "wallet1")[-1])
    print(carousel(aicv1, "AI guide", IG, "aicv1")[-1])
    for k, v in stories.items():
        print(story(v, "Daily story", ST, k))
