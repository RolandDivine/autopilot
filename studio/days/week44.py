"""Thu 29 – Sat 31 Oct 2026 (Roland, 28 Oct: "do everything from now till Saturday"). Run from studio/:  python days/week44.py

Plan (quality over quantity; Reel daily at 12:00 + Kobo stories at 18:00 via videos.yml, all in the Fish ELITE voice):
  Thu 29  08:00 LinkedIn: building Autopilot, what the data taught me (people photo).  12:00 Reel ex20 fake giveaway.  18:00 Kobo 12.
  Fri 30  08:00 LinkedIn: Nigeria innovating + motivation (people photo).  12:00 Reel ex17 quishing.  18:00 Kobo 13.
  Sat 31  08:00 Instagram carousel: fake job offers (NSITF warning, Oct 2026), abstract cover.  12:00 Reel ex09 voice clone.  18:00 Kobo 14.
Stories 09/11/14/17/21 every day; 21:00 is a plain call to action, not a teaser. No LinkedIn on Saturday.
Facts only from Roland's stated facts and our own analytics; no invented stories.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
GEN = ROOT / "assets" / "gen"

LI_THU = """I built a system that posts my content for me. Then the data humbled me.

In one week it published 19 LinkedIn posts. Total: 1,040 impressions. Zero comments.

In the same stretch, one short Instagram video about a crypto scam got 1,548 views, 23 saves and 11 shares.

Same person. Same system. Very different results.

Here's what building Autopilot taught me:

1. Volume is not a strategy. Nineteen average posts lost to one useful one.

2. The first line decides everything. The video that worked put the viewer's risk in the first sentence. The ones that flopped opened with a greeting, and people swiped away in about 3 seconds.

3. Automation should multiply judgement, not replace it. A machine can post every hour. It can't decide what deserves to be posted.

So I changed the system. One LinkedIn post a day. Stories, not announcements. If a post doesn't solve a real problem, it doesn't ship.

Builders, a question:
What's one thing you automated that made the result worse?

If you're building content systems too and want to compare notes, send me a message."""

LI_FRI = """In January, Google searches for "how to start a business" in Nigeria jumped 80%.

Ten months later, I'd ask a harder question: how many of those businesses actually started?

Wanting it isn't our problem. Young Nigerians are some of the hungriest people I know.

What's missing is structure. Someone to show you the first steps. People building next to you. A deadline that's real.

That's why, as Chief International Adviser for Youth Innovation at the Edo State Ministry of Youth Affairs, I've been designing a six-week technology pilot for about 200 university students. Not a lecture series. A build programme: you leave with something you made.

The hard truths I'd tell every young builder:

→ Motivation starts things. Discipline finishes them.
→ Your environment will beat your willpower. Choose it on purpose.
→ Nobody is coming to hand you the opportunity. But you don't have to build alone.

Nigeria is innovating. The real question is whether we're building the structures that turn ambition into products.

What's the biggest thing stopping young Nigerians from finishing what they start?

If your organisation wants to back young Nigerian builders, send me a message."""

JOB_HOOK = "Paying for a job? ==It's not a job.=="
JOB_SLIDES = [
    [("q", "Roland, a company sent me a job offer on Facebook 🎉 They just want a small \"registration fee\" first."),
     ("r", "Congrats on the hustle 🙏🏾 but stop right there."),
     ("r", "A real employer ==pays you. You don't pay them.==")],
    [("q", "But the letter has a government logo on it 😅"),
     ("r", "Logos and appointment letters are easy to fake."),
     ("r", "This month the NSITF warned that job adverts using its name are fake. ==It isn't recruiting and never charges fees.==")],
    [("r", "**Red flags** 🚩"),
     ("r", "A fee for forms, training, medicals or \"processing\"\nAn offer with no real interview"),
     ("r", "Recruiter only on WhatsApp or Facebook\n==\"Pay today or lose your slot\"==")],
    [("r", "**How to check in 2 minutes** ✅"),
     ("r", "Find the organisation's official website or verified page yourself. Don't use the link they sent."),
     ("r", "Look for the vacancy there. ==No listing? No job.==")],
    [("q", "What if they only want my BVN and bank details \"for salary\"?"),
     ("r", "Not before a real contract and a real interview."),
     ("r", "Your BVN, NIN and bank details are ==a scammer's goldmine.==")],
    [("r", "**One simple rule** 🧠"),
     ("r", "If you have to pay to get the job,"),
     ("r", "==the job is the scam.==")],
    [("r", "Your turn 👇"),
     ("r", "Have you or a friend ever been asked to ==pay for a job?=="),
     ("r", "Tell me what happened. Your story could protect someone. 💬")],
    [("r", "📌 Save this · 📤 Send it to a friend who's job hunting"),
     ("r", "Follow **@defi_ring_master** and turn on 🔔 to join a community learning money safety together."),
     ("r", "Stay sharp out there. 🙏🏾")],
]
JOB_CAP = """How to spot a fake job offer in Nigeria 🚩

If you have to pay to get the job, the job is the scam. The red flags, and the 2-minute check before you send money or your BVN. Swipe →

💬 Comment: have you ever been asked to pay for a job?
📌 Save it · 📤 Send it to a friend who's job hunting
🔔 Follow @defi_ring_master

#jobscam #nigeria #scamawareness #jobsearch"""

CTA = ("circuit-lock.jpg", "Learning money and crypto safety? ==Follow and turn on 🔔==", "Send this to a friend")
DAYS = {
    "2026-10-29": {
        "li": (LI_THU, "people-builder-dash.png", "19 posts lost to ==one good video.==", "Building Autopilot", None),
        "stories": {
            "s0900": ("coin-siphon.jpg", "\"Send 1 Bitcoin, get 2 back\"? ==It's always a scam.==", "New Reel at 12 · tap my profile"),
            "s1100": ("coin-siphon.jpg", "Have you seen a ==crypto giveaway livestream?==", "Reply 👇"),
            "s1400": ("coin-siphon.jpg", "Nobody doubles your crypto. ==Nobody.==", "Today's Reel · tap my profile"),
            "s1700": ("fake-alert.png", "Got a credit alert today? ==Check the app, not the SMS.==", "Tap my profile"),
            "s2100": CTA,
        },
    },
    "2026-10-30": {
        "li": (LI_FRI, "people-students.png", "Ambition isn't the gap. ==Structure is.==", "Nigeria · building",
               "Source: Google Search data for Nigeria, first two weeks of January 2026 (reported by Techeconomy)."),
        "stories": {
            "s0900": ("qr-sticker.png", "Don't scan that QR code ==until you check this.==", "New Reel at 12 · tap my profile"),
            "s1100": ("qr-sticker.png", "Do you scan QR codes ==to pay?==", "Reply 👇"),
            "s1400": ("qr-sticker.png", "A QR code is just a link. ==Treat it like one.==", "Today's Reel · tap my profile"),
            "s1700": ("coin-siphon.jpg", "This week: fake alerts, SIM swaps, ==fake giveaways, QR scams.==", "Catch up · tap my profile"),
            "s2100": ("circuit-lock.jpg", "Which scam should I explain next? ==Reply 👇==", "Your question could be next"),
        },
    },
    "2026-10-31": {
        "ig": True,
        "stories": {
            "s0900": ("job-envelope.png", "Job offer asking you to pay? ==It's not a job.==", "New post · tap my profile"),
            "s1100": ("job-envelope.png", "Have you ever been asked to ==pay for a job?==", "Reply 👇"),
            "s1400": ("phone-glow.jpg", "Your brother calls, crying. ==Is it really him?==", "New Reel · tap my profile"),
            "s1700": ("phone-glow.jpg", "Set a family code word ==this weekend.==", "Today's Reel · tap my profile"),
            "s2100": CTA,
        },
    },
}


def build(day, d):
    Q = ROOT / "queue" / day
    ST, MEDIA, IG = Q / "stories", Q / "media", Q / "instagram"
    for x in (ST, MEDIA):
        x.mkdir(parents=True, exist_ok=True)
    slot = {"x": {"enabled": False}, "linkedin": {"enabled": False}, "instagram": {"enabled": False}}
    if "li" in d:
        text, img, hook, kicker, src = d["li"]
        cover(GEN / img, hook, MEDIA / "li-cover.jpg", kicker=kicker, handle="Roland Divine", swipe=False)
        slot["linkedin"] = {"enabled": True, "text": text, "media": "media/li-cover.jpg"}
        if src:
            slot["linkedin"]["first_comment"] = src
        slot.update({"title": f"LinkedIn: {kicker}", "kind": "story"})
    if d.get("ig"):
        IG.mkdir(parents=True, exist_ok=True)
        # Roland, 30 Oct: chat-first carousels got ~2x the views of designed covers, so the first slide is the chat itself
        for old in IG.glob("job-*.jpg"):
            old.unlink()
        rest = carousel(JOB_SLIDES, "Money · safety", IG, "job", offset=0)
        media = [f"instagram/{Path(p).name}" for p in rest]
        alt = ["Chat: " + " ".join(re.sub(r"[*=]", "", t).replace("\n", ", ") for _, t in s) for s in JOB_SLIDES]
        slot["instagram"] = {"enabled": True, "caption": JOB_CAP, "media": media, "music": "Sade – Smooth Operator", "alt": alt}
        slot.update({"title": "How to: spot a fake job offer (Nigeria)", "kind": "lesson"})
    (Q / "0800.json").write_text(json.dumps(slot, indent=1, ensure_ascii=False))
    st = []
    for at, (img, text, foot) in d["stories"].items():
        cover(GEN / img, text, ST / f"{at}.jpg", kicker=foot, size=(1080, 1920), pos="top", swipe=False)
        st.append({"at": at[1:], "media": f"stories/{at}.jpg"})
    (Q / "stories.json").write_text(json.dumps(st, indent=2))
    print("built", Q)


if __name__ == "__main__":
    for day, d in DAYS.items():
        if len(sys.argv) < 2 or day in sys.argv[1:]:
            build(day, d)
