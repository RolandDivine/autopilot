"""Day 11 · Thu 22 Oct 2026. Run from studio/:  python days/day11.py
08:00 pays off the 21 Oct teaser ("Do you know your phone can show you which apps were listening?"): Instagram carousel.
LinkedIn (Thursday) = the YouTube clip, posted by post_video.py (entry "liclip"), so the 0800 slot has LinkedIn off.
21:00 story teases 23 Oct 08:00 (stop ChatGPT / Claude / Gemini training on your chats).
No 1300/1900 slots: Instagram is 1 carousel a day and LinkedIn is 1 post a day (21 Oct rules).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "queue" / "2026-10-22"
GEN = ROOT / "assets" / "gen"

# search: "is my phone listening to me", "which apps are using my microphone", "app privacy report iphone"
hook = "Your phone keeps a log of ==which apps were listening.=="
slides = [
    [("q", "Roland, is my phone listening to me? 🎙️"),
     ("r", "You don't have to guess."),
     ("r", "iPhone and Android both keep a record of ==which apps used your mic and camera.==")],
    [("r", "**iPhone: App Privacy Report** 🍎"),
     ("r", "Settings → **Privacy & Security** → scroll down → **App Privacy Report.**"),
     ("r", "Tap ==Turn On App Privacy Report.==")],
    [("r", "**What it shows** 📋"),
     ("r", "The last **7 days**: which apps used your **microphone, camera, location, photos and contacts.**"),
     ("r", "Plus ==which websites each app contacted.==")],
    [("r", "**Android: Privacy dashboard** 🤖"),
     ("r", "Settings → **Security & privacy** → **Privacy** → **Privacy dashboard** (names vary by phone)."),
     ("r", "It shows ==which apps used the mic, camera and location== recently.")],
    [("r", "**The live warning lights** 🟠🟢"),
     ("r", "iPhone: an **orange dot** = mic in use, a **green dot** = camera."),
     ("r", "Android: a **green icon** top-right when the mic or camera is on. ==Tap it to see which app.==")],
    [("q", "Found an app that shouldn't have it?"),
     ("r", "iPhone: Settings → Privacy & Security → **Microphone** → switch it off for that app."),
     ("r", "Android: tap the app in the dashboard → **Permissions** → ==Don't allow.==")],
    [("r", "Check it tonight. It takes 2 minutes. ⏱️"),
     ("r", "📌 Save this. 📤 Send it to the friend who thinks their phone is spying on them."),
     ("r", "Follow **@defi_ring_master** for AI and tech that protects you.")],
]
cap = """How to see which apps used your microphone and camera, on iPhone and Android. 🎙️

Your phone already keeps the log: the App Privacy Report and the Privacy dashboard. Where to find them, what the warning dots mean, and how to cut an app off. Swipe →

📌 Save it
📤 Send it to the friend who thinks their phone is spying on them

#privacy #iphone #android #cybersecurity"""
alt = ["A glowing smartphone in the dark. Text: Your phone keeps a log of which apps were listening.",
       "Chat: is my phone listening? iPhone and Android both record which apps used your mic and camera.",
       "Chat: iPhone. Settings, Privacy and Security, App Privacy Report, Turn On App Privacy Report.",
       "Chat: it shows the last 7 days of mic, camera, location, photos and contacts use, and websites contacted.",
       "Chat: Android. Settings, Security and privacy, Privacy, Privacy dashboard.",
       "Chat: orange dot means mic in use and green dot means camera on iPhone; green icon on Android.",
       "Chat: turn off the microphone permission for an app on iPhone or Android.",
       "Chat: check it tonight, save this and send it to a friend. Follow defi_ring_master."]

TEASER = ("glass-dome-brain.jpg", "Do you know your AI chats ==may be training the AI?==", "Tomorrow · 8 AM")
STORIES = {
    "s0900": ("phone-glow.jpg", "Which apps used your mic this week? ==The 2-minute check is on my page.==", "New post · tap my profile"),
    "s1100": ("phone-glow.jpg", "Have you ever felt ==your phone was listening?==", "Reply 👇"),
    "s1400": ("pig-phone.jpg", "Ever got a ==\"wrong number\" text== from a very friendly stranger?", "Reply 👇"),
    "s1700": ("phone-glow.jpg", "Checked which apps used your camera? ==It takes 2 minutes.==", "Tap my profile · today's post"),
    "s2100": None,
}


def build():
    IG, ST = Q / "instagram", Q / "stories"
    for d in (IG, ST):
        d.mkdir(parents=True, exist_ok=True)
    cover(GEN / "phone-glow.jpg", hook, IG / "phone-0.jpg", kicker="Tech · privacy")
    rest = carousel(slides, "AI, crypto & tech", IG, "phone", offset=1)
    media = ["instagram/phone-0.jpg"] + [f"instagram/{Path(p).name}" for p in rest]
    (Q / "0800.json").write_text(json.dumps({
        "title": "How to: see which apps used your mic and camera", "kind": "lesson", "x": {"enabled": False},
        "linkedin": {"enabled": False},
        "instagram": {"enabled": True, "caption": cap, "media": media, "music": "Michael Jackson – Human Nature", "alt": alt}},
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
