"""Day 13 · Sat 24 Oct 2026. Run from studio/:  python days/day13.py
08:00 Instagram: pays off the 23 Oct teaser ("Do you know where your seed phrase should never be?"). No LinkedIn on weekends.
13:00 = Zero to One part 2 (already built, don't touch).
21:00 story teases Sun 25 Oct 08:00 (AI voice-clone scam calls + the family safe word).
Cover style: people photo + editorial headline (Roland, 23 Oct: people covers are more attractive), chat written as a conversation.
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import li_editorial  # noqa: E402
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "queue" / "2026-10-24"
GEN = ROOT / "assets" / "gen"

slides = [
    [("q", "Roland, where should I keep my seed phrase? 🤔"),
     ("r", "Good question. Most people get this wrong, so let's fix it today."),
     ("r", "First: whoever has those 12 or 24 words ==has your money.== Full stop.")],
    [("q", "I took a screenshot so I won't forget it 😅"),
     ("r", "Please delete it today 🙏🏾"),
     ("r", "Screenshots sync to the cloud, get backed up, get shared by accident. ==Never a screenshot.==")],
    [("r", "**Where your seed phrase should NEVER be** 🚫"),
     ("r", "Screenshots or photos\nNotes apps, Google Drive, iCloud, email"),
     ("r", "WhatsApp \"message to self\"\n==Any website or form that asks for it==")],
    [("q", "But what if \"support\" asks for it to fix my wallet?"),
     ("r", "That's a scammer. Every single time."),
     ("r", "No real exchange, wallet or support agent ==will ever ask for your seed phrase.==")],
    [("r", "**Where it SHOULD be** ✅"),
     ("r", "Written on paper (or stamped on a metal backup), offline."),
     ("r", "Kept somewhere safe from fire, water and curious visitors. Some people keep ==two copies in two places.==")],
    [("r", "**Bonus for bigger amounts** 🔐"),
     ("r", "A hardware wallet keeps your keys off your phone and laptop."),
     ("r", "Your seed phrase is the backup. ==Guard the paper like cash.==")],
    [("r", "Your turn 👇"),
     ("r", "Be honest: where is your seed phrase right now? ==Paper, screenshot, or \"I don't know\"?== 😅"),
     ("r", "No judgement. Comment and I'll help you fix it. 💬")],
    [("r", "📌 Save this · 📤 Send it to the friend with a screenshot of their seed phrase"),
     ("r", "Follow **@defi_ring_master** and turn on 🔔 to join a community learning crypto safety together."),
     ("r", "Education, not financial advice.")],
]
cap = """Where to keep your seed phrase, and where it should never be. 🔑

Screenshots, cloud notes, WhatsApp-to-self, \"support\" forms: the places that get wallets drained, and the safe way to store it. Swipe →

💬 Comment: where is your seed phrase right now? No judgement.
📌 Save it · 📤 Send it to the friend with a screenshot of theirs
🔔 Follow @defi_ring_master
Education, not financial advice.

#crypto #cryptosecurity #seedphrase #web3"""

TEASER = ("people-call.png", "Do you know a scammer can ==clone your voice== from a few seconds of audio?", "Tomorrow · 8 AM")
STORIES = {
    "s0900": ("people-seed.png", "Where is your seed phrase right now? ==The safe way is on my page.==", "New post · tap my profile"),
    "s1100": ("people-seed.png", "Have you ever ==screenshotted== a seed phrase or password?", "Reply 👇"),
    "s1400": ("coin-collapse.jpg", "Would you trust a \"stablecoin\" paying ==20% a year?==", "Reply 👇"),
    "s1700": ("people-seed.png", "Delete that screenshot today. ==Paper beats cloud.==", "Tap my profile · today's post"),
    "s2100": None,
}


def build():
    IG, ST, MEDIA = Q / "instagram", Q / "stories", Q / "media"
    for d in (IG, ST, MEDIA):
        d.mkdir(parents=True, exist_ok=True)
    html = li_editorial.cover_html(GEN / "people-seed.png", "Crypto safety", "Your seed phrase is your money. ==Store it like it.==",
                                   "Where it should never be, and where it should.")
    asyncio.run(li_editorial._shoot([(html, IG / "seed-0.jpg")]))
    rest = carousel(slides, "Crypto · safety", IG, "seed", offset=1)
    media = ["instagram/seed-0.jpg"] + [f"instagram/{Path(p).name}" for p in rest]
    import re
    alt = ["Photo: a young man writing a list of words on a paper card. Text: Your seed phrase is your money. Store it like it."] + \
          ["Chat: " + " ".join(re.sub(r"[*=]", "", t).replace("\n", ", ") for _, t in s) for s in slides]
    (Q / "0800.json").write_text(json.dumps({
        "title": "How to: store your seed phrase (and where it should never be)", "kind": "lesson", "x": {"enabled": False},
        "linkedin": {"enabled": False},
        "instagram": {"enabled": True, "caption": cap, "media": media, "music": "Earth, Wind & Fire – September", "alt": alt}},
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
