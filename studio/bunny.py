"""Kobo the bunny: 15-second animated Reels (1080x1920, 30 fps).

Every frame is drawn by render(t) in the page, so the video is deterministic.
Usage from studio/: python bunny.py  -> ../assets/reels/kobo-ai-guess.mp4
"""
import asyncio
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.async_api import async_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ig_options import FONT_CSS

FPS, SECONDS = 30, 15
OUT = Path(__file__).resolve().parents[1] / "assets" / "reels"

BUNNY = """
<svg id="bunny" viewBox="0 0 600 760" width="690" height="874">
  <g id="whole">
    <ellipse cx="300" cy="742" rx="170" ry="16" fill="#000" opacity=".10" id="shadow"/>
    <g id="earL" style="transform-origin:245px 250px">
      <ellipse cx="225" cy="120" rx="52" ry="140" fill="#F7F1EA"/>
      <ellipse cx="225" cy="132" rx="26" ry="104" fill="#F6B8C8"/>
    </g>
    <g id="earR" style="transform-origin:355px 250px">
      <g transform="rotate(14 375 120)">
        <ellipse cx="375" cy="120" rx="52" ry="140" fill="#F7F1EA"/>
        <ellipse cx="375" cy="132" rx="26" ry="104" fill="#F6B8C8"/>
      </g>
    </g>
    <!-- body in a yellow hoodie -->
    <ellipse cx="300" cy="590" rx="175" ry="150" fill="#FFD84D"/>
    <path d="M250 470 L300 520 L350 470" stroke="#E8B800" stroke-width="8" fill="none" stroke-linecap="round"/>
    <rect x="250" y="590" width="100" height="56" rx="20" fill="#F2C300"/>
    <text x="300" y="630" font-family="Jakarta" font-weight="800" font-size="34" text-anchor="middle" fill="#7A5B00">RD</text>
    <g id="armL" style="transform-origin:150px 520px">
      <ellipse cx="128" cy="585" rx="40" ry="78" fill="#FFD84D"/>
      <circle cx="122" cy="655" r="34" fill="#F7F1EA"/>
    </g>
    <g id="armR" style="transform-origin:450px 520px">
      <ellipse cx="472" cy="585" rx="40" ry="78" fill="#FFD84D"/>
      <circle cx="478" cy="655" r="34" fill="#F7F1EA"/>
    </g>
    <ellipse cx="225" cy="728" rx="62" ry="30" fill="#F7F1EA"/>
    <ellipse cx="375" cy="728" rx="62" ry="30" fill="#F7F1EA"/>
    <!-- head -->
    <g id="head" style="transform-origin:300px 420px">
      <ellipse cx="300" cy="350" rx="185" ry="165" fill="#F7F1EA"/>
      <ellipse cx="200" cy="410" rx="36" ry="22" fill="#F6B8C8" opacity=".8"/>
      <ellipse cx="400" cy="410" rx="36" ry="22" fill="#F6B8C8" opacity=".8"/>
      <g id="eyes">
        <g id="eyeL" style="transform-origin:230px 345px">
          <ellipse cx="230" cy="345" rx="30" ry="38" fill="#2B2118"/>
          <circle cx="241" cy="330" r="11" fill="#fff"/><circle cx="222" cy="358" r="5" fill="#fff"/>
        </g>
        <g id="eyeR" style="transform-origin:370px 345px">
          <ellipse cx="370" cy="345" rx="30" ry="38" fill="#2B2118"/>
          <circle cx="381" cy="330" r="11" fill="#fff"/><circle cx="362" cy="358" r="5" fill="#fff"/>
        </g>
      </g>
      <path d="M288 390 Q300 382 312 390 Q300 404 288 390Z" fill="#E87A97"/>
      <ellipse id="mouth" cx="300" cy="428" rx="20" ry="4" fill="#7A2E3E"/>
      <path id="smile" d="M276 418 Q288 432 300 418 Q312 432 324 418" stroke="#7A2E3E" stroke-width="6" fill="none" stroke-linecap="round"/>
    </g>
  </g>
</svg>
"""

# (start, end, text): what Kobo says
LINES = [
    (0.7, 2.7, "Hi! I'm **Kobo** 🐰"),
    (2.9, 5.3, "Ever wondered how **AI** answers you? 🤔"),
    (5.5, 9.7, "It picks the ==most likely== next word 👇"),
    (9.9, 12.4, "One word at a time. **Very smart guessing!**"),
    (12.6, 15.0, "So always ==double-check it== ✅"),
]

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
%(font)s
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#EFE7DE;font-family:Jakarta;color:#111}
.top{position:absolute;left:64px;right:64px;top:110px;display:flex;align-items:center;gap:22px;background:#fff;border-radius:30px;padding:22px 30px}
.av{width:76px;height:76px;border-radius:50%%;background:#FFD84D;display:flex;align-items:center;justify-content:center;font:800 32px Jakarta}
.bub{position:absolute;left:90px;right:90px;top:400px;background:#fff;border-radius:44px;padding:40px 46px;font-size:62px;line-height:1.28;
     box-shadow:0 10px 30px rgba(0,0,0,.08);transform-origin:50%% 100%%;opacity:0}
.bub:after{content:"";position:absolute;bottom:-30px;left:50%%;margin-left:-20px;border:22px solid transparent;border-top:30px solid #fff;border-bottom:0}
.hl{background:#FFD84D;padding:0 10px;border-radius:8px;font-weight:800}
.card{position:absolute;z-index:2;left:90px;right:90px;top:700px;background:#fff;border-radius:40px;padding:38px 44px;opacity:0;box-shadow:0 10px 30px rgba(0,0,0,.08)}
.prompt{font-size:46px;font-weight:700;min-height:62px}
.cursor{display:inline-block;width:5px;height:48px;background:#111;vertical-align:-6px;margin-left:4px}
.row{display:flex;align-items:center;gap:20px;margin-top:26px;font-size:42px}
.row .w{width:170px;font-weight:700}.row .bar{height:46px;border-radius:14px;background:#E5DED5;flex:1;position:relative;overflow:hidden}
.row .fill{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:14px;background:#C9C1B6}
.row.win .fill{background:#FFD84D}.row .p{width:110px;text-align:right;font-weight:800}
#bunny{position:absolute;left:195px;top:1000px}
.foot{position:absolute;left:0;right:0;top:760px;text-align:center;font-size:44px;font-weight:800;opacity:0}
.foot span{background:#111;color:#fff;padding:18px 34px;border-radius:999px}
</style></head><body>
<div class="top"><div class="av">RD</div><div><b style="font-size:34px">Roland Divine</b>
<div style="font-size:27px;color:#6b7280">AI in 15 seconds · with Kobo</div></div></div>
%(bubbles)s
<div class="card" id="card"><div class="prompt"><span id="typed"></span><span class="cursor" id="cur"></span></div>
 <div class="row win" id="r0"><div class="w">Abuja</div><div class="bar"><div class="fill"></div></div><div class="p">0%%</div></div>
 <div class="row" id="r1"><div class="w">Lagos</div><div class="bar"><div class="fill"></div></div><div class="p">0%%</div></div>
 <div class="row" id="r2"><div class="w">Kano</div><div class="bar"><div class="fill"></div></div><div class="p">0%%</div></div>
</div>
%(bunny)s
<div class="foot" id="foot"><span>Follow @defi_ring_master</span></div>
<script>
const LINES=%(lines)s;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const easeOutBack=x=>{const c=1.7;x=clamp(x);return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const ease=x=>{x=clamp(x);return x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2};
const $=id=>document.getElementById(id);
const PROMPT="The capital of Nigeria is…";
const ROWS=[92,6,2];
function render(t){
  // bubbles pop in and out
  let talking=false;
  LINES.forEach(([a,b],i)=>{const el=$('b'+i);
    const k=t<a?0:t<a+.28?easeOutBack((t-a)/.28):t<b-.2?1:clamp((b-t)/.2);
    el.style.opacity=k>0?Math.min(1,k*1.4):0;
    el.style.transform=`scale(${.6+.4*k}) translateY(${(1-k)*30}px)`;
    if(t>a+.2&&t<b-.4)talking=true;});
  // entrance + idle bob + final happy hops
  let y=0;
  if(t<.7) y=(1-easeOutBack(t/.7))*700;
  y+=Math.sin(t*2*Math.PI*1.1)*8;
  if(t>12.7) y-=Math.abs(Math.sin((t-12.7)*Math.PI*1.6))*90;
  const squash=t>12.7?1+.05*Math.sin((t-12.7)*Math.PI*3.2):1;
  $('whole').style.transform=`translateY(${y}px) scale(${1/squash},${squash})`;
  $('whole').style.transformOrigin='300px 740px';
  $('head').style.transform=`rotate(${Math.sin(t*2.2)*4}deg)`;
  $('earL').style.transform=`rotate(${-6+Math.sin(t*3.1)*7}deg)`;
  $('earR').style.transform=`rotate(${6+Math.sin(t*3.1+1)*9}deg)`;
  // blink every ~3 s
  const bt=(t+.8)%%3.2, s=bt<.14?Math.max(.08,Math.abs(bt-.07)/.07):1;
  $('eyeL').style.transform=$('eyeR').style.transform=`scaleY(${s})`;
  // mouth: open while talking, smile otherwise
  const open=talking?6+Math.abs(Math.sin(t*17))*24*(.6+.4*Math.abs(Math.sin(t*5))):0;
  $('mouth').setAttribute('ry',Math.max(.1,open));$('mouth').style.opacity=talking?1:0;$('smile').style.opacity=talking?0:1;
  // arms: wave hello, point up at the card, cheer at the end
  let ar=Math.sin(t*2)*4, al=-Math.sin(t*2)*4;
  if(t>.7&&t<2.7) ar=-120+Math.sin(t*14)*22;
  if(t>5.5&&t<9.7) ar=-150+Math.sin(t*3)*5;
  if(t>12.7){ar=-130+Math.sin(t*10)*15;al=130-Math.sin(t*10)*15;}
  $('armR').style.transform=`rotate(${ar}deg)`;$('armL').style.transform=`rotate(${al}deg)`;
  // the "next word" card
  const c=t<5.6?0:t<5.9?ease((t-5.6)/.3):t<9.5?1:clamp((9.8-t)/.3);
  $('card').style.opacity=c;$('card').style.transform=`translateY(${(1-c)*40}px)`;
  const n=Math.floor(clamp((t-6)/1.2)*PROMPT.length);$('typed').textContent=PROMPT.slice(0,n);
  $('cur').style.opacity=(Math.floor(t*3)%%2)?1:0;
  ROWS.forEach((v,i)=>{const g=ease((t-7.4-i*.15)/.9);const r=$('r'+i);
    r.querySelector('.fill').style.width=(v*g)+'%%';r.querySelector('.p').textContent=Math.round(v*g)+'%%';
    r.style.opacity=t<7.3?.25:1;});
  const f=ease((t-13.2)/.4);$('foot').style.opacity=f;$('foot').style.transform=`translateY(${(1-f)*30}px)`;
}
render(0);
</script></body></html>"""


def fmt(s):
    import re
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"==(.+?)==", r"<span class='hl'>\1</span>", s)


def build_html():
    import json
    bubbles = "".join(f"<div class='bub' id='b{i}'>{fmt(t)}</div>" for i, (_, _, t) in enumerate(LINES))
    return PAGE % {"font": FONT_CSS, "bubbles": bubbles, "bunny": BUNNY,
                   "lines": json.dumps([[a, b] for a, b, _ in LINES])}


async def main(name="kobo-ai-guess"):
    frames = Path("/tmp/bunny_frames")
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir()
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(build_html(), wait_until="load")
        await pg.wait_for_timeout(300)
        for i in range(FPS * SECONDS):
            await pg.evaluate(f"render({i / FPS})")
            await pg.screenshot(path=str(frames / f"f{i:04d}.jpg"), type="jpeg", quality=90)
        await b.close()
    out = OUT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "f%04d.jpg"),
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-movflags", "+faststart",
                    str(out)], check=True)
    return out


if __name__ == "__main__":
    print(asyncio.run(main()))
