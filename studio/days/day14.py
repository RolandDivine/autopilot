"""Day 14 · Wed 28 Oct 2026. Run from studio/:  python days/day14.py
08:00 Instagram: how to spot a fake bank credit alert (Nigeria). Abstract Figma cover (Roland, 27 Oct: back to abstract covers).
08:00 LinkedIn (abstract cover, Roland 27 Oct): Klærus story (Roland, 27 Oct: storytelling, Klærus leads). Hook rides the trending prediction-market news
      (US midterms 3 Nov; Google Finance now shows Kalshi/Polymarket odds). Facts only from /areas/klaerus.md. No pitch.
12:00 Reel (videos.yml): address poisoning part 2. 18:00 Kobo part 11 (stories).
21:00 story = simple call to action, not a teaser.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "queue" / "2026-10-28"
GEN = ROOT / "assets" / "gen"

# search: "how to know fake alert", "fake credit alert nigeria", "fake transfer receipt"
hook = "That credit alert ==might be fake.== Check this first."
slides = [
    [("q", "Roland, a buyer just sent me a credit alert. Can I release the goods? 🤔"),
     ("r", "Not yet 🙏🏾"),
     ("r", "An SMS or a screenshot ==is not money.== Only your account balance is.")],
    [("q", "But the alert has my bank's name on it 😅"),
     ("r", "Sender names on SMS can be faked."),
     ("r", "Fake alert apps and edited receipts look ==exactly like the real thing.==")],
    [("r", "**How to check in 30 seconds** ✅"),
     ("r", "Open your bank app (or dial your bank's USSD code yourself)."),
     ("r", "Look at your ==actual balance and transaction history.== Not the SMS.")],
    [("r", "**Red flags** 🚩"),
     ("r", "\"I've sent it, check your phone\" + pressure to hurry"),
     ("r", "A receipt screenshot instead of money\n==A \"mistaken transfer\" they want you to refund fast==")],
    [("q", "What if they say they sent too much and want the extra back?"),
     ("r", "Classic trick."),
     ("r", "Confirm the money in your balance first. If it's real, ==let your bank handle the reversal.==")],
    [("r", "**Simple rule for sellers** 🛍️"),
     ("r", "No balance, no goods."),
     ("r", "Same rule for crypto P2P: ==release only after the money shows in your account.==")],
    [("r", "Your turn 👇"),
     ("r", "Have you (or someone you know) ever received a ==fake alert?=="),
     ("r", "Tell me what happened. Your story could save someone. 💬")],
    [("r", "📌 Save this · 📤 Send it to a friend who sells online"),
     ("r", "Follow **@defi_ring_master** and turn on 🔔 to join a community learning money safety together."),
     ("r", "Education, not financial advice.")],
]
cap = """How to spot a fake bank credit alert (Nigeria) 🚨

An SMS or a receipt screenshot is not money. Here's the 30-second check every seller and P2P trader should do before releasing goods or crypto. Swipe →

💬 Comment: have you ever received a fake alert?
📌 Save it · 📤 Send it to a friend who sells online
🔔 Follow @defi_ring_master
Education, not financial advice.

#fakealert #nigeria #scamawareness #onlinebusiness"""

li_hook = "Right on direction. ==Wrong on timing.=="
li = """Prediction markets are everywhere this week.

With the US midterms on 3 November, odds from Kalshi and Polymarket now show up inside Google Finance. Millions of people are reading probabilities instead of opinions.

It made me think about a problem I've lived with for years.

I've often been right about where a market was going, and wrong about when. Right on direction, wrong on timing. In trading, that can cost as much as being wrong.

I wasn't alone. In my trading community of about 200 people, the complaint was the same: we read direction well, and timing punished us.

When I started trading on Polymarket, something clicked. Elections and events get a price between 0 and 100. A probability. Everyone can see what the crowd believes.

But short-term price direction, the thing traders argue about every single day, had no clean probability scale.

That gap is why I'm building Klærus.

Honest update: the launch is taking longer than I wanted. I'd rather get it right than get it fast. And I'm looking for people who want to help with marketing, distribution and social.

So, a question for traders and builders:
When you've been wrong in a market, was it the direction or the timing?

Tell me in the comments. And if you'd like to help build Klærus, send me a message."""

STORIES = {
    "s0900": ("fake-alert.png", "That credit alert ==might be fake.== The 30-second check is on my page.", "New post · tap my profile"),
    "s1100": ("fake-alert.png", "Have you ever received a ==fake credit alert?==", "Reply 👇"),
    "s1400": ("twin-keys.jpg", "Do you copy wallet addresses ==from your history?==", "Reply 👇"),
    "s1700": ("fake-alert.png", "No balance, no goods. ==Check the app, not the SMS.==", "Tap my profile · today's post"),
    "s2100": ("phone-glow.jpg", "Learning crypto and money safety? ==Follow and turn on 🔔==", "Send this to a friend"),
}


def build():
    IG, MEDIA, ST = Q / "instagram", Q / "media", Q / "stories"
    for d in (IG, MEDIA, ST):
        d.mkdir(parents=True, exist_ok=True)
    cover(GEN / "fake-alert.png", hook, IG / "alert-0.jpg", kicker="Money · safety")
    rest = carousel(slides, "Money · safety", IG, "alert", offset=1)
    media = ["instagram/alert-0.jpg"] + [f"instagram/{Path(p).name}" for p in rest]
    alt = ["Abstract image: a glass phone whose green bank notification is peeling off like a sticker. Text: That credit alert might be fake. Check this first."] + \
          ["Chat: " + " ".join(re.sub(r"[*=]", "", t).replace("\n", ", ") for _, t in s) for s in slides]
    cover(GEN / "arrow-hourglass.png", li_hook, MEDIA / "klaerus-cover.jpg", kicker="Building Klærus", handle="Roland Divine", swipe=False)
    (Q / "0800.json").write_text(json.dumps({
        "title": "How to: spot a fake bank credit alert + Klærus story", "kind": "lesson", "x": {"enabled": False},
        "linkedin": {"enabled": True, "text": li, "media": "media/klaerus-cover.jpg"},
        "instagram": {"enabled": True, "caption": cap, "media": media, "music": "Earth, Wind & Fire – September", "alt": alt}},
        indent=1, ensure_ascii=False))
    st = []
    for at, (img, text, foot) in STORIES.items():
        cover(GEN / img, text, ST / f"{at}.jpg", kicker=foot, size=(1080, 1920), pos="top", swipe=False)
        st.append({"at": at[1:], "media": f"stories/{at}.jpg"})
    (Q / "stories.json").write_text(json.dumps(st, indent=2))


if __name__ == "__main__":
    build()
    print("built", Q)
