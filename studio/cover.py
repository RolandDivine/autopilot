"""Scroll-stopping cover (chosen 15 Oct 2026): a generated realistic-abstract image, full bleed,
with a short hook in big type. Used as the LinkedIn single image and as slide 1 of Instagram carousels.

    from cover import cover
    cover("assets/gen/ice-server.jpg", "Does ChatGPT drink a ==bottle of water== per chat?",
          "queue/2026-10-16/instagram/water-1.jpg", kicker="AI · myth check")

Hook rules: 4–10 words, one ==highlight==, a question or a surprising claim. The image should make
people think "what?" (odd object, odd material, dramatic light). Never use other people's images.
"""
import asyncio
import base64
import html
import re
from pathlib import Path

from playwright.async_api import async_playwright

from ig_options import FONT_CSS

HANDLE = "@defi_ring_master"


def _fmt(t):
    t = html.escape(t)
    return re.sub(r"==(.+?)==", r"<span class='hl'>\1</span>", t).replace("\n", "<br>")


def _html(img, hook, kicker, handle, w, h, pos):
    data = base64.b64encode(Path(img).read_bytes()).decode()
    fs = 92 if len(re.sub("==", "", hook)) < 40 else 80
    top = pos == "top"
    grad = ("linear-gradient(180deg,rgba(0,0,0,.82) 0%,rgba(0,0,0,.45) 38%,rgba(0,0,0,0) 60%)" if top else
            "linear-gradient(0deg,rgba(0,0,0,.88) 0%,rgba(0,0,0,.55) 38%,rgba(0,0,0,0) 62%)")
    place = "top:90px" if top else "bottom:120px"
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{w}px;height:{h}px;overflow:hidden;background:#000}}
.bg{{position:absolute;inset:0;background:url(data:image/jpeg;base64,{data}) center/cover}}
.g{{position:absolute;inset:0;background:{grad}}}
.t{{position:absolute;left:72px;right:72px;{place};color:#fff;font-family:Jakarta}}
.k{{font:700 30px Jakarta;letter-spacing:3px;text-transform:uppercase;color:#FFD84D;margin-bottom:22px}}
.h{{font:800 {fs}px/1.18 Jakarta;letter-spacing:-2px;text-shadow:0 4px 30px rgba(0,0,0,.5)}}
.hl{{color:#111;background:#FFD84D;padding:0 12px;border-radius:10px;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.f{{position:absolute;left:72px;right:72px;bottom:48px;display:flex;justify-content:space-between;font:600 28px Jakarta;color:rgba(255,255,255,.75)}}
</style></head><body><div class=bg></div><div class=g></div>
<div class=t>{f"<div class=k>{html.escape(kicker)}</div>" if kicker else ""}<div class=h>{_fmt(hook)}</div></div>
<div class=f><span>{handle}</span><span>swipe →</span></div></body></html>"""


async def _shoot(doc, out, w, h):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": w, "height": h})
        await pg.set_content(doc, wait_until="load")
        await pg.wait_for_timeout(200)
        await pg.screenshot(path=str(out), type="jpeg", quality=92)
        await b.close()


def cover(img, hook, out, kicker="", handle=HANDLE, size=(1080, 1350), pos="bottom", swipe=True):
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    doc = _html(img, hook, kicker, handle, *size, pos)
    if not swipe:
        doc = doc.replace("<span>swipe →</span>", "<span></span>")
    asyncio.run(_shoot(doc, out, *size))
    return str(out)
