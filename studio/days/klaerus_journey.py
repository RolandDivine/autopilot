"""Klaerus build-journey stories (Chat Bubbles + real demo screenshots). Run from studio/."""
import asyncio
import base64
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ig_chat
from ig_chat import fmt, NAME, HANDLE
from ig_options import FONT_CSS

SHOTS = Path("/home/claude/klaerus_shots")
OUT = Path(__file__).resolve().parents[2] / "assets" / "klaerus"


def crop(name, y0, y1):
    """Crop by 430-wide frame coordinates, regardless of screenshot scale."""
    im = Image.open(SHOTS / name).convert("RGB")
    s = im.width / 430
    im = im.crop((0, int(y0 * s), im.width, int(y1 * s)))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.width / im.height


def page(bubbles, shot, label="Building Klaerus"):
    src, ratio = shot if shot else (None, None)
    img = ""
    if src:
        img = f"<div class='shot'><img src='{src}'></div>"
    body = "".join(f"<div class='b {w}'>{fmt(t)}</div>" for w, t in bubbles)
    css = ("*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1920px;overflow:hidden}"
           "body{background:#EFE7DE;font-family:Jakarta;color:#111;padding:230px 64px 300px;position:relative}"
           ".top{display:flex;align-items:center;gap:22px;background:#fff;border-radius:30px;padding:24px 30px;margin-bottom:36px}"
           ".av{width:80px;height:80px;border-radius:50%;background:#FFD84D;display:flex;align-items:center;justify-content:center;font:800 34px Jakarta}"
           ".b{max-width:86%;padding:28px 34px;border-radius:34px;font-size:44px;line-height:1.36;margin-bottom:22px}"
           ".q{background:#fff;border-top-left-radius:8px}.r{background:#D9FDD3;margin-left:auto;border-top-right-radius:8px}"
           ".hl{background:#FFD84D;padding:0 8px;border-radius:6px;font-weight:800}"
           ".shot{margin:10px auto 0;width:92%;background:#fff;border-radius:36px;padding:14px;box-shadow:0 8px 30px rgba(0,0,0,.10)}"
           ".shot img{width:100%;display:block;border-radius:24px}"
           ".foot{position:absolute;left:64px;right:64px;bottom:220px;font-size:28px;color:#6b6257;display:flex;justify-content:space-between}")
    top = (f"<div class='top'><div class='av'>RD</div><div><b style='font-size:34px'>{NAME}</b>"
           f"<div style='font-size:27px;color:#6b7280'>{label} · online</div></div></div>")
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{css}</style></head>"
            f"<body>{top}{body}{img}<div class='foot'><span>{HANDLE}</span><span>demo · play money</span></div></body></html>")


STORIES = [
    ("k1", [("q", "Roland, what's this Klaerus you keep building? 👀"),
            ("r", "A trading app for **short moves**. Pick if Bitcoin goes up or down in the next minutes, and see your ==exact risk before you trade.==")],
     ("01-market.jpg", 0, 270)),
    ("k2", [("r", "**Before you trade**, it shows you everything:"),
            ("r", "Where you get ==liquidated==, and the ==most you can win==. No surprises.")],
     ("03-ticket-1m.jpg", 350, 590)),
    ("k3", [("r", "**During the trade, you're in control.**"),
            ("r", "==Cut== takes your profit early. ==Stop== limits a loss. You don't just watch and pray 🙏🏾")],
     ("04-live-trade.jpg", 708, 852)),
    ("k4", [("q", "And Flip mode?"),
            ("r", "Flip picks your direction for you, with a fixed band on both sides. Touch the band, and the trade is over.")],
     ("07-flip-ticket.jpg", 500, 735)),
    ("k5", [("r", "**My real demo trades tonight:**"),
            ("r", "1 tiny win, 1 ==liquidation==, 1 Cut in profit."),
            ("r", "Risk is real, even in a good app. That's why it shows you the risk first.")],
     ("10-history.jpg", 380, 660)),
    ("k6", [("q", "When can I use it?"),
            ("r", "It's still in demo (play money) while we finish the last pieces."),
            ("r", "I'm sharing the whole build here. ==Follow the journey== 🛠️"),
            ("r", "Education, not financial advice.")],
     None),
]


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for key, bubbles, shot in STORIES:
            html = page(bubbles, crop(*shot) if shot else None)
            await pg.set_content(html, wait_until="load")
            await pg.wait_for_timeout(200)
            if await pg.evaluate("document.body.scrollHeight > window.innerHeight + 2"):
                print("OVERFLOW", key)
            await pg.screenshot(path=str(OUT / f"{key}.jpg"), type="jpeg", quality=92)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
    ims = [Image.open(OUT / f"{k}.jpg").resize((360, 640)) for k, *_ in STORIES]
    S = Image.new("RGB", (len(ims) * 370 + 10, 660), "#555")
    for i, im in enumerate(ims):
        S.paste(im, (10 + i * 370, 10))
    S.save("/tmp/claude-test/klaerus.png")
    print("ok")
