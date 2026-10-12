"""Highlight covers + the 'Start here' story set (1080x1920)."""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

from ig_options import FONT_CSS, HANDLE

OUT = Path("/tmp/claude-test/stories")
BASE = "*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1920px;overflow:hidden}"

# Highlight covers: the icon sits in the centre so Instagram's circle crop keeps it.
COVERS = [("start", "★", "Start here"), ("crypto", "₿", "Crypto 101"), ("ai", "AI", "AI 101"),
          ("build", "⚒", "Build"), ("klaerus", "K", "Klaerus"), ("qa", "?", "Q&A"), ("news", "◉", "News")]


def cover(icon):
    size = 300 if len(icon) == 1 else 230
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{BASE}"
            "body{background:#FFD84D;display:flex;align-items:center;justify-content:center}"
            f".i{{font-family:Bricolage;font-weight:800;font-size:{size}px;color:#111;line-height:1}}"
            f"</style></head><body><div class='i'>{icon}</div></body></html>")


STORY_CSS = ("body{background:#FFFFFF;font-family:Jakarta;color:#111;padding:260px 96px 420px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start}"
             ".k{display:inline-block;background:#FFD84D;font-weight:800;font-size:40px;padding:16px 34px;border-radius:999px}"
             "h1{font-family:Bricolage;font-weight:800;font-size:120px;line-height:1.02;margin:50px 0 50px;letter-spacing:-1px}"
             "p{font-size:52px;line-height:1.42;margin-bottom:34px}.row{display:flex;gap:30px;align-items:center;font-size:54px;margin:30px 0}"
             ".n{flex:0 0 120px;height:120px;border-radius:32px;background:#111;color:#FFD84D;display:flex;align-items:center;justify-content:center;font:800 56px Bricolage}"
             ".hl{background:#FFD84D;padding:0 10px;border-radius:8px;font-weight:800}"
             ".foot{position:absolute;left:96px;right:96px;bottom:250px;font-size:38px;color:#888}")

STORIES = [
    ("1", "<span class='k'>Start here</span><h1>Hi, I'm Roland 👋</h1>"
          "<p>I build in crypto and AI, and I teach what I know in plain words.</p>"
          "<p>No jargon. No hype. <span class='hl'>One easy lesson a day.</span></p>"),
    ("2", "<span class='k'>What you'll learn</span><h1>3 things, from zero</h1>"
          "<div class='row'><div class='n'>₿</div>Crypto: what it is and how to stay safe</div>"
          "<div class='row'><div class='n'>AI</div>AI: use it for work and to get jobs</div>"
          "<div class='row'><div class='n'>⚒</div>Build: launch your own product</div>"),
    ("3", "<span class='k'>How it works</span><h1>150 days. 1 lesson a day.</h1>"
          "<p>Every post is short enough to read in 2 minutes.</p>"
          "<p>Every lesson ends with a <span class='hl'>2-minute task</span> so you actually learn it.</p>"),
    ("4", "<span class='k'>The goal</span><h1>Launch Day: 4 Feb 2027</h1>"
          "<p>By then you'll understand crypto and AI, and you'll have launched something real.</p>"
          "<p>I'm building in public alongside you.</p>"),
    ("5", "<span class='k'>Your first step</span><h1>Start with lesson 1</h1>"
          "<p>Tap my profile and read the first post.</p>"
          "<p>Then <span class='hl'>turn on post notifications</span> so you don't miss a day.</p>"
          "<p>Got a question? Send me a DM. I read them.</p>"),
]


def story(body):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{BASE}{STORY_CSS}</style></head>"
            f"<body>{body}<div class='foot'>{HANDLE} · education, not financial advice</div></body></html>")


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for key, icon, _ in COVERS:
            await pg.set_content(cover(icon), wait_until="load")
            await pg.screenshot(path=str(OUT / f"cover-{key}.jpg"), type="jpeg", quality=92)
        for key, body in STORIES:
            await pg.set_content(story(body), wait_until="load")
            await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(OUT / f"start-here-{key}.jpg"), type="jpeg", quality=92)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
    from PIL import Image, ImageDraw
    # preview: covers as circles, and the story set side by side
    covers = Image.new("RGB", (len(COVERS) * 200 + 40, 260), "white")
    d = ImageDraw.Draw(covers)
    for i, (key, _, label) in enumerate(COVERS):
        im = Image.open(OUT / f"cover-{key}.jpg").crop((0, 420, 1080, 1500)).resize((150, 150))
        mask = Image.new("L", (150, 150), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 149, 149), fill=255)
        covers.paste(im, (40 + i * 200, 30), mask)
        d.text((40 + i * 200 + 20, 200), label, fill="#111")
    covers.save(OUT / "preview-covers.png")
    sheet = Image.new("RGB", (5 * 380 + 60, 700), "#E9E9E9")
    for i in range(5):
        sheet.paste(Image.open(OUT / f"start-here-{i+1}.jpg").resize((360, 640)), (30 + i * 380, 30))
    sheet.save(OUT / "preview-start-here.png")
    print("done")
