"""Day 2 · Tue 13 Oct 2026 · Instagram in the Chat Bubbles style. Run from studio/: python days/day2_ig.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ig_chat import carousel, story

Q = Path(__file__).resolve().parents[2] / "queue" / "2026-10-13"
IG, ST = Q / "instagram", Q / "stories"

news = [
    [("q", "Roland, why is everyone talking about a US number tomorrow? 🤔"),
     ("r", "It's the **US inflation number** (CPI). It comes out **Wed 1:30 PM Lagos time**."),
     ("q", "Why should crypto people care?")],
    [("r", "Because it can move crypto prices more than most crypto news."),
     ("r", "High inflation → interest rates stay high → safe bonds pay more → ==less money goes into risky things like crypto.=="),
     ("q", "And if it comes in low?")],
    [("r", "Often the opposite. More money flows back into risk."),
     ("r", "Forecast: **3.6% a year** (last month 3.4%). Prices react to the surprise, not the number."),
     ("r", "You don't need to trade it. Just don't panic if prices swing. 📌 Save this.")],
]

ai2 = [
    [("q", "Roland, how does ChatGPT actually work? 🤔"),
     ("r", "Easier than you think. **3 simple steps.** No tech words, I promise."),
     ("q", "Ok, explain like I'm 10"), ("r", "Swipe → 👇")],
    [("r", "**Step 1: it read a huge library.**"),
     ("r", "Books, websites, articles. From all that reading it learned ==patterns== in how words fit together."),
     ("q", "Like how I know \"good\" usually comes before \"morning\"?"), ("r", "Exactly that 👌")],
    [("r", "**Step 2: your words get cut into small pieces.**"),
     ("r", "\"How do I save money?\" becomes [How] [do] [I] [save] [money] [?]"),
     ("r", "Those pieces are called ==tokens==.")],
    [("r", "**Step 3: it guesses the next word.**"),
     ("r", "Type \"The capital of Nigeria is…\" and it picks ==Abuja==. Not Lagos. Because that's the most likely next word."),
     ("q", "So it's just guessing?? 😮")],
    [("r", "Very smart guessing, one word at a time, until the answer is done."),
     ("r", "That's why it can sound **100% sure** and still be ==wrong==."),
     ("q", "So I should check what it says?"), ("r", "Always. It drafts, you decide ✅")],
    [("r", "**Your 2-minute task:**"),
     ("r", "Ask an AI a question you already know the answer to. Then ask: \"How sure are you, and where is this from?\""),
     ("r", "Notice what it admits 👀")],
    [("q", "This was actually easy to understand 🙌"),
     ("r", "**Save it** so you remember 📌"),
     ("r", "Send it to a friend who uses ChatGPT every day 😄"),
     ("r", "New lesson every day. Follow **@defi_ring_master**")],
]

build1 = [
    [("q", "Roland, why do most people never launch the thing they're building? 🤔"),
     ("r", "It's rarely a bad idea. It's **3 traps.**"), ("r", "Swipe → 👇")],
    [("r", "**Trap 1: building in secret.**"),
     ("r", "Months of work that nobody has seen… then you find out ==nobody needed it.=="),
     ("q", "Oof. So what do I do?"), ("r", "Show people early. Even a sketch on paper is enough.")],
    [("r", "**Trap 2: waiting for perfect.**"),
     ("r", "\"One more feature.\" \"One more week.\" \"After the redesign.\""),
     ("r", "==Launch day never comes.==")],
    [("r", "**Trap 3: no deadline.**"),
     ("r", "No date → no pressure → no finish."),
     ("q", "So the fix is…"), ("r", "Pick a date. And ==tell someone.==")],
    [("r", "**Your 2-minute task:**"),
     ("r", "Write one sentence: \"I will launch ______ by ______.\""),
     ("r", "Our Launch Day is **4 Feb 2027**. Build with me 🛠️")],
    [("q", "I'm in 🙋🏾‍♂️"),
     ("r", "**Save this** so you can check your sentence later 📌"),
     ("r", "Send it to the friend who's \"been working on something\" for a year 😄"),
     ("r", "Follow **@defi_ring_master** for the full Builders track")],
]

stories = {
    "s0900": [("r", "**New post is up** ☀️"), ("r", "Why one US number tomorrow could move crypto more than any crypto headline."),
              ("r", "Tap my profile to read it 👆")],
    "s1100": [("r", "**Quick quiz** 🧠"), ("q", "When AI answers you, is it…\n\nA) looking up the answer\nB) guessing the most likely next word"),
              ("r", "Reply with **A or B** 👇 Answer at 2 PM.")],
    "s1400": [("r", "**Answer: B** ✅"), ("r", "AI guesses the most likely next word, one word at a time. That's why it can sound sure and still be wrong."),
              ("r", "Full lesson is on my page 📌")],
    "s1700": [("r", "**Builders check-in** 🛠️"), ("r", "Today's lesson asked you to write one sentence:"),
              ("r", "\"I will launch ______ by ______.\""), ("r", "==Reply with yours.== I'll read every one 👇")],
    "s2100": [("r", "**Tomorrow** 📅"), ("r", "Crypto lesson 2: what a blockchain is, in plain words."),
              ("r", "==Turn on post notifications== so you don't miss it 🔔")],
}

if __name__ == "__main__":
    print(carousel(news, "Market news", IG, "news2")[-1])
    print(carousel(ai2, "AI lesson 2", IG, "ai2")[-1])
    print(carousel(build1, "Builders lesson 1", IG, "build1")[-1])
    for k, v in stories.items():
        print(story(v, "Daily story", ST, k))
