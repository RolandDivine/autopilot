"""YouTube thumbnails (1280x720 JPEG): one image + 3 words or fewer.

    python studio/yt_thumb.py revoke
"""
import asyncio
import base64
import sys
from pathlib import Path

from playwright.async_api import async_playwright

from ig_options import face

ROOT = Path(__file__).resolve().parent.parent
CSS = face("Jakarta", "plus-jakarta-sans", (800,))

THUMBS = {
    "revoke": {"img": ROOT / "assets/viral/howto-revoke/drain.png", "l1": "REVOKE", "l2": "THIS NOW", "tag": "UNLIMITED"},
}


def html(t):
    img = base64.b64encode(Path(t["img"]).read_bytes()).decode()
    return f"""<html><head><style>{CSS}*{{margin:0;padding:0}}
body{{width:1280px;height:720px;overflow:hidden;position:relative;background:#07080B;font-family:Jakarta}}
.im{{position:absolute;inset:0;background:url(data:image/png;base64,{img}) center/cover;filter:saturate(1.15) contrast(1.08)}}
.fade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,8,11,.96) 0%,rgba(7,8,11,.82) 38%,rgba(7,8,11,0) 68%)}}
.t{{position:absolute;left:56px;top:150px;font:800 150px/.92 Jakarta;letter-spacing:-6px;color:#fff;text-shadow:0 8px 30px rgba(0,0,0,.6)}}
.t b{{color:#FFD84D;font-weight:800}}
.tag{{position:absolute;right:70px;top:90px;font:800 54px Jakarta;color:#fff;background:#E5242C;padding:10px 26px;border-radius:14px;
 transform:rotate(-4deg);box-shadow:0 10px 30px rgba(229,36,44,.5);letter-spacing:1px}}
</style></head><body><div class="im"></div><div class="fade"></div>
<div class="t">{t['l1']}<br><b>{t['l2']}</b></div><div class="tag">⚠ {t['tag']}</div></body></html>"""


async def main(name):
    out = ROOT / "assets" / "youtube" / f"thumb-{name}.jpg"
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1280, "height": 720})
        await pg.set_content(html(THUMBS[name]))
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=str(out), type="jpeg", quality=90)
        await b.close()
    print(out, out.stat().st_size)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
