"""Render the YouTube channel banner (2560x1440 JPEG). Text stays inside the 1546x423 centre safe area."""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

from ig_options import face

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "youtube" / "banner.jpg"
CSS = face("Jakarta", "plus-jakarta-sans", (500, 700, 800))

HTML = f"""<html><head><style>{CSS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:2560px;height:1440px;background:#07080B;font-family:Jakarta;color:#fff;overflow:hidden;position:relative}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,216,77,.06) 2px,transparent 2px),
 linear-gradient(90deg,rgba(255,216,77,.06) 2px,transparent 2px);background-size:80px 80px}}
.glow{{position:absolute;left:50%;top:50%;width:1800px;height:900px;transform:translate(-50%,-50%);
 background:radial-gradient(ellipse at center,rgba(255,216,77,.16),transparent 65%)}}
.safe{{position:absolute;left:507px;top:508px;width:1546px;height:423px;display:flex;flex-direction:column;
 justify-content:center;align-items:center;text-align:center}}
.kick{{font:700 34px Jakarta;letter-spacing:8px;text-transform:uppercase;color:#FFD84D}}
.h{{font:800 112px/1.02 Jakarta;letter-spacing:-3px;margin:18px 0 22px}}
.h b{{color:#FFD84D}}
.sub{{font:500 36px Jakarta;color:rgba(255,255,255,.8)}}
.pill{{display:inline-block;margin-top:26px;font:700 30px Jakarta;color:#07080B;background:#FFD84D;border-radius:999px;padding:10px 34px}}
</style></head><body><div class="grid"></div><div class="glow"></div>
<div class="safe"><div class="kick">Roland Divine</div>
<div class="h">Keep your crypto <b>safe</b>.<br>Use AI like a pro.</div>
<div class="sub">Step-by-step how-tos · Education, not financial advice</div>
<div class="pill">New video every week</div></div></body></html>"""


async def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 2560, "height": 1440})
        await pg.set_content(HTML)
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=str(OUT), type="jpeg", quality=92)
        await b.close()
    print(OUT, OUT.stat().st_size)


if __name__ == "__main__":
    asyncio.run(main())
