"""Day 12 · Fri 23 Oct 2026. Run from studio/:  python days/day12.py
08:00 Instagram: pays off the 22 Oct teaser ("Do you know your AI chats may be training the AI?").
08:00 LinkedIn (Friday = Nigeria + motivation): principle-led, no invented anecdote (Roland hasn't sent a story yet).
21:00 story teases Sat 24 Oct 08:00 (where your seed phrase should never be). No LinkedIn on weekends.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "queue" / "2026-10-23"
GEN = ROOT / "assets" / "gen"

# search: "how to stop chatgpt from training on my data", "turn off gemini activity", "claude help improve"
hook = "Your AI chats ==may be training the AI.== Turn it off."
slides = [
    [("q", "Roland, does ChatGPT learn from what I type? 🤔"),
     ("r", "By default, it can."),
     ("r", "ChatGPT, Claude and Gemini can all use your chats to ==improve their models== unless you switch it off.")],
    [("r", "**ChatGPT** 💬"),
     ("r", "Settings → **Data controls** → **Improve the model for everyone** → ==off.=="),
     ("r", "Quick private chat? Use **Temporary Chat:** not used for training.")],
    [("r", "**Claude** 🧠"),
     ("r", "Settings → **Privacy** → **Help improve Claude** → ==off.=="),
     ("r", "It takes 10 seconds.")],
    [("r", "**Gemini** ✨"),
     ("r", "gemini.google.com → **Activity** → turn off ==Gemini Apps Activity== (\"Keep Activity\")."),
     ("r", "Google still keeps chats for up to **72 hours** to run the service.")],
    [("r", "**The catch** ⚠️"),
     ("r", "Switching it off works from now on."),
     ("r", "It doesn't pull back what you typed before. ==Delete old chats you regret.==")],
    [("q", "So what should I never paste in?"),
     ("r", "Passwords, ID numbers, bank details, seed phrases."),
     ("r", "And ==client or company data== you don't have permission to share.")],
    [("r", "Do it tonight. Three apps, two minutes. ⏱️"),
     ("r", "📌 Save this. 📤 Send it to the friend who pastes everything into ChatGPT."),
     ("r", "Follow **@defi_ring_master** for AI that protects you.")],
]
cap = """How to stop ChatGPT, Claude and Gemini from training on your chats. 🧠

The exact setting in each app, the one that keeps a private chat private, and what you should never paste in. Swipe →

📌 Save it
📤 Send it to the friend who pastes everything into ChatGPT

#ai #chatgpt #privacy #productivity"""
alt = ["A glowing brain under a glass dome. Text: Your AI chats may be training the AI. Turn it off.",
       "Chat: does ChatGPT learn from what I type? ChatGPT, Claude and Gemini can use chats to improve models unless switched off.",
       "Chat: ChatGPT, Settings, Data controls, Improve the model for everyone, off. Temporary Chat is not used for training.",
       "Chat: Claude, Settings, Privacy, Help improve Claude, off.",
       "Chat: Gemini, Activity, turn off Gemini Apps Activity. Google keeps chats up to 72 hours.",
       "Chat: the catch. Turning it off works from now on; delete old chats you regret.",
       "Chat: never paste passwords, ID numbers, bank details, seed phrases or client data.",
       "Chat: do it tonight, save this and send it to a friend. Follow defi_ring_master."]

li_hook = "Nigeria isn't short of talent. ==It's short of finishing.=="
li = """Nigeria isn't short of talent. It's short of finishing.

Young Nigerians are some of the most creative builders anywhere. The gap is rarely ideas or intelligence. It's what happens after the excitement wears off.

Three hard truths about building here:

→ Nobody is coming to save the project. Power, data, funding: plan around what you can't control, then do the part you can control, every day.

→ Discipline beats motivation. Motivation gets you to start. A daily routine, even one focused hour, is what gets you to version one.

→ Alone is slower than together. Find two or three people who actually ship, show each other your work every week, and hold each other to dates.

Nigeria will be built by people who keep showing up when nobody is clapping.

What's one habit that kept you consistent when the motivation ran out?"""

TEASER = ("circuit-lock.jpg", "Do you know where your seed phrase ==should never be?==", "Tomorrow · 8 AM")
STORIES = {
    "s0900": ("glass-dome-brain.jpg", "Is your AI learning from your chats? ==The 2-minute fix is on my page.==", "New post · tap my profile"),
    "s1100": ("glass-dome-brain.jpg", "What do you paste into ChatGPT that ==you probably shouldn't?==", "Reply 👇"),
    "s1400": ("twin-keys.jpg", "Do you check ==the whole wallet address== before you send?", "Reply 👇"),
    "s1700": ("glass-dome-brain.jpg", "Turned off AI training yet? ==Three apps, two minutes.==", "Tap my profile · today's post"),
    "s2100": None,
}


def build():
    IG, MEDIA, ST = Q / "instagram", Q / "media", Q / "stories"
    for d in (IG, MEDIA, ST):
        d.mkdir(parents=True, exist_ok=True)
    cover(GEN / "glass-dome-brain.jpg", hook, IG / "aipriv-0.jpg", kicker="AI · privacy")
    rest = carousel(slides, "AI, crypto & tech", IG, "aipriv", offset=1)
    media = ["instagram/aipriv-0.jpg"] + [f"instagram/{Path(p).name}" for p in rest]
    cover(GEN / "chrome-hourglass.jpg", li_hook, MEDIA / "finish-cover.jpg", kicker="Nigeria · building", handle="Roland Divine", swipe=False)
    (Q / "0800.json").write_text(json.dumps({
        "title": "How to: stop ChatGPT, Claude and Gemini training on your chats", "kind": "lesson", "x": {"enabled": False},
        "linkedin": {"enabled": True, "text": li, "media": "media/finish-cover.jpg"},
        "instagram": {"enabled": True, "caption": cap, "media": media, "music": "Stevie Wonder – Isn't She Lovely", "alt": alt}},
        indent=1, ensure_ascii=False))
    img, text, foot = TEASER
    cover(GEN / img, text, ST / "s2100.jpg", kicker=foot, size=(1080, 1920), pos="top", swipe=False)
    st = []
    for at, v in STORIES.items():
        if v is not None:
            img, text, foot = v
            cover(GEN / img, text, ST / f"{at}.jpg", kicker=foot, size=(1080, 1920), pos="top", swipe=False)
        st.append({"at": at[1:], "media": f"stories/{at}.jpg"})
    (Q / "stories.json").write_text(json.dumps(st, indent=2))


if __name__ == "__main__":
    build()
    print("built", Q)
