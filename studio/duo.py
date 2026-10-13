"""Kobo & Babe: two-bunny talking Reels driven by a voice-over.

Inputs per part (in AUDIO dir): partN.wav and partN.json (timed words from the transcribe workflow).
Speaker turns are set in TURNS below; mouths follow the audio loudness.
Usage from studio/: python duo.py 1 [2 3 ...]  -> ../assets/reels/klaerus-part-N.mp4
"""
import asyncio
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from playwright.async_api import async_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ig_options import FONT_CSS

FPS = 30
AUDIO = Path("/home/claude/kobo_audio")
OUT = Path(__file__).resolve().parents[1] / "assets" / "reels"
SERIES = "Klaerus explained"
TOTAL_PARTS = 5
SLUG = "klaerus-part"
SUBTITLE = "with Kobo &amp; Babe · a 5-part series"
SOLO = False  # True: Kobo alone, centred and bigger

# (time the turn starts, speaker). K = Kobo (host), B = Babe (co-host)
TURNS = {
    1: [(0.0, "K"), (6.3, "B"), (13.4, "K"), (19.8, "B"), (27.3, "K"), (33.0, "B"), (42.1, "K")],
    2: [(0.0, "B"), (9.8, "K"), (18.9, "B"), (29.6, "K"), (33.8, "B"), (44.5, "K"), (46.8, "B"),
        (52.1, "K"), (53.8, "B")],
    3: [(0.0, "K"), (10.5, "B"), (17.8, "K"), (21.8, "B"), (24.9, "K"), (30.2, "B"), (33.5, "K"),
        (35.3, "B"), (48.1, "K")],
    4: [(0.0, "B"), (26.7, "K"), (30.2, "B"), (39.2, "K"), (42.0, "B"), (47.8, "K"), (49.4, "B"),
        (53.7, "K")],
    5: [(0.0, "B"), (15.9, "K"), (23.7, "B"), (32.1, "K")],
}

# key-idea cards that pop up in the middle: (part, start, end, emoji, title, line)
CARDS = {
    1: [(13.4, 19.6, "📈", "Perpetual futures", "Big volume, but leverage, funding and liquidations"),
        (27.6, 38.8, "🎯", "Prediction markets", "Capped risk, but money locked for weeks"),
        (47.8, 55.4, "✨", "Something new", "Klaerus: a Probability Perpetual Market")],
    2: [(9.8, 18.4, "🏦", "Pooled liquidity", "The pool takes the other side of every trade"),
        (22.6, 44.0, "🫁", "Liquidation that breathes", "The boundary moves with real volatility"),
        (47.4, 61.4, "🎁", "20% back", "Get liquidated, get 20% of your stake back")],
    3: [(10.5, 29.9, "✂️", "Cut", "Take profit early, before the timer ends"),
        (30.2, 47.7, "🛑", "Stop", "Exit early with a small loss"),
        (48.1, 59.5, "🗺️", "12-month plan", "Between DeFi trading and crypto games")],
    4: [(2.6, 15.3, "🎰", "LP pool = the house", "A fixed house edge on every payout"),
        (16.0, 22.4, "🐋", "Whale protection", "Max bet size scales with the pool"),
        (30.2, 59.5, "🎲", "Flip Mode", "A fair random draw picks your direction")],
    5: [(3.5, 13.4, "🌉", "Cross-chain", "Bring SOL, OP or ETH. It settles on Arbitrum"),
        (15.9, 23.1, "🧩", "Best of three", "Perps + prediction markets + crypto games"),
        (32.1, 37.2, "🔔", "Follow the build", "@defi_ring_master")],
}

# fix words the speech-to-text misheard
FIX = {r"\bClaris\b": "Klaerus", r"\bClerius\b": "Klaerus", r"\bD-Gens\b": "degens", r"\bSteak\.com": "Stake.com",
       r"\bsaw\b": "SOL", r"it takes up": "it ticks up", r"\bNQATR\b": "NQ-ATR", r"losing you,": "losing. You"}

KOBO_COLORS = {"fur": "#F7F1EA", "inner": "#F6B8C8", "hood": "#FFD84D", "hood2": "#F2C300", "seam": "#E8B800",
               "badge": "RD", "badgeText": "#7A5B00"}
BABE_COLORS = {"fur": "#E9D2BE", "inner": "#F4A6BC", "hood": "#C9B6F2", "hood2": "#B39DEB", "seam": "#9F86E0",
               "badge": "♥", "badgeText": "#5B3FA8"}


def bunny_svg(pid, c, bow=False):
    bowsvg = ("<g transform='translate(378 40) rotate(18)'><path d='M0 0 L-38 -24 L-38 24Z' fill='#FF6FA0'/>"
              "<path d='M0 0 L38 -24 L38 24Z' fill='#FF6FA0'/><circle r='12' fill='#FF4F8B'/></g>") if bow else ""
    return f"""
<svg id="{pid}" class="bun" viewBox="0 -30 600 790" width="470" height="619">
 <g id="{pid}-whole">
  <ellipse cx="300" cy="742" rx="170" ry="16" fill="#000" opacity=".10"/>
  <g id="{pid}-earL" style="transform-origin:245px 250px">
   <ellipse cx="225" cy="120" rx="52" ry="140" fill="{c['fur']}"/><ellipse cx="225" cy="132" rx="26" ry="104" fill="{c['inner']}"/>
  </g>
  <g id="{pid}-earR" style="transform-origin:355px 250px"><g transform="rotate(14 375 120)">
   <ellipse cx="375" cy="120" rx="52" ry="140" fill="{c['fur']}"/><ellipse cx="375" cy="132" rx="26" ry="104" fill="{c['inner']}"/>
  </g>{bowsvg}</g>
  <ellipse cx="300" cy="590" rx="175" ry="150" fill="{c['hood']}"/>
  <path d="M250 470 L300 520 L350 470" stroke="{c['seam']}" stroke-width="8" fill="none" stroke-linecap="round"/>
  <rect x="250" y="590" width="100" height="56" rx="20" fill="{c['hood2']}"/>
  <text x="300" y="631" font-family="Jakarta" font-weight="800" font-size="34" text-anchor="middle" fill="{c['badgeText']}">{c['badge']}</text>
  <g id="{pid}-armL" style="transform-origin:150px 520px">
   <ellipse cx="128" cy="585" rx="40" ry="78" fill="{c['hood']}"/><circle cx="122" cy="655" r="34" fill="{c['fur']}"/></g>
  <g id="{pid}-armR" style="transform-origin:450px 520px">
   <ellipse cx="472" cy="585" rx="40" ry="78" fill="{c['hood']}"/><circle cx="478" cy="655" r="34" fill="{c['fur']}"/></g>
  <ellipse cx="225" cy="728" rx="62" ry="30" fill="{c['fur']}"/><ellipse cx="375" cy="728" rx="62" ry="30" fill="{c['fur']}"/>
  <g id="{pid}-head" style="transform-origin:300px 440px">
   <ellipse cx="300" cy="350" rx="185" ry="165" fill="{c['fur']}"/>
   <ellipse cx="200" cy="410" rx="36" ry="22" fill="{c['inner']}" opacity=".8"/><ellipse cx="400" cy="410" rx="36" ry="22" fill="{c['inner']}" opacity=".8"/>
   <g id="{pid}-eyeL" style="transform-origin:230px 345px"><ellipse cx="230" cy="345" rx="30" ry="38" fill="#2B2118"/>
    <circle cx="241" cy="330" r="11" fill="#fff"/><circle cx="222" cy="358" r="5" fill="#fff"/></g>
   <g id="{pid}-eyeR" style="transform-origin:370px 345px"><ellipse cx="370" cy="345" rx="30" ry="38" fill="#2B2118"/>
    <circle cx="381" cy="330" r="11" fill="#fff"/><circle cx="362" cy="358" r="5" fill="#fff"/></g>
   <path d="M288 390 Q300 382 312 390 Q300 404 288 390Z" fill="#E87A97"/>
   <ellipse id="{pid}-mouth" cx="300" cy="428" rx="20" ry="4" fill="#7A2E3E"/>
   <path id="{pid}-smile" d="M276 418 Q288 432 300 418 Q312 432 324 418" stroke="#7A2E3E" stroke-width="6" fill="none" stroke-linecap="round"/>
  </g>
 </g>
</svg>"""


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#EFE7DE;font-family:Jakarta;color:#111}
.top{position:absolute;left:56px;right:56px;top:96px;display:flex;align-items:center;gap:22px;background:#fff;border-radius:30px;padding:22px 30px}
.av{width:76px;height:76px;border-radius:50%;background:#FFD84D;display:flex;align-items:center;justify-content:center;font:800 32px Jakarta}
.part{margin-left:auto;white-space:nowrap;background:#111;color:#fff;font-weight:800;font-size:28px;padding:10px 20px;border-radius:999px}
.prog{position:absolute;left:56px;right:56px;top:236px;height:10px;border-radius:9px;background:#DDD3C8;overflow:hidden}
.prog i{display:block;height:100%;width:0;background:#111}
.bub{position:absolute;left:56px;right:56px;top:330px;min-height:300px;background:#fff;border-radius:46px;padding:40px 46px;
     font-size:60px;line-height:1.3;font-weight:600;box-shadow:0 10px 30px rgba(0,0,0,.08)}
.bub .who{font-size:30px;font-weight:800;margin-bottom:12px;letter-spacing:.5px}
.bub .w{color:#B9AFA4}.bub .w.said{color:#111}.bub .w.now{background:#FFD84D;color:#111;border-radius:10px;padding:0 6px;margin:0 -6px}
.tail{position:absolute;width:0;height:0;border:26px solid transparent;border-top:36px solid #fff;border-bottom:0;top:0}
.card{position:absolute;left:110px;right:110px;top:960px;background:#111;color:#fff;border-radius:36px;padding:30px 38px;
      display:flex;gap:26px;align-items:center;opacity:0}
.card .e{font-size:70px}.card b{display:block;font-size:44px}.card span{font-size:32px;color:#D6D0C8;line-height:1.3}
.bun{position:absolute;top:1212px}
#kobo{left:40px}#babe{right:40px}
.name{position:absolute;top:1838px;font-size:30px;font-weight:800;padding:8px 22px;border-radius:999px;background:#fff}
.foot{position:absolute;left:0;right:0;top:268px;text-align:center;font-size:24px;color:#8a8075}
"""

JS = """
const D=__DATA__;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const ease=x=>{x=clamp(x);return x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2};
const $=id=>document.getElementById(id);
let lastPhrase=-1;
function speakerAt(t){let s=D.turns[0][1];for(const [a,k] of D.turns){if(t>=a)s=k;}return s;}
function rig(p,t,talk,level,listen,phase){
  const bob=Math.sin(t*2*Math.PI*1.0+phase)*6;
  $(p+'-whole').style.transform=`translateY(${bob - (talk?level*10:0)}px)`;
  $(p+'-whole').style.transformOrigin='300px 740px';
  const tilt=listen?Math.sin(t*1.3+phase)*5+4*(p=='kobo'?1:-1):Math.sin(t*2.2+phase)*3;
  $(p+'-head').style.transform=`rotate(${tilt}deg) translateY(${talk?-level*6:0}px)`;
  $(p+'-earL').style.transform=`rotate(${-6+Math.sin(t*3.1+phase)*6}deg)`;
  $(p+'-earR').style.transform=`rotate(${6+Math.sin(t*3.1+phase+1)*8}deg)`;
  const bt=(t+phase)%3.4, s=bt<.14?Math.max(.08,Math.abs(bt-.07)/.07):1;
  $(p+'-eyeL').style.transform=$(p+'-eyeR').style.transform=`scaleY(${s})`;
  const open=talk?Math.sqrt(Math.max(0,level))*30:0;
  $(p+'-mouth').setAttribute('ry',Math.max(.1,open));$(p+'-mouth').style.opacity=open>1.5?1:0;
  $(p+'-smile').style.opacity=open>1.5?0:1;
  const g=talk?Math.sin(t*4+phase)*10*level:0;
  $(p+'-armR').style.transform=`rotate(${talk?-25-g*2:Math.sin(t*2)*3}deg)`;
  $(p+'-armL').style.transform=`rotate(${talk?18+g:-Math.sin(t*2)*3}deg)`;
}
function render(t){
  const f=Math.min(D.env.length-1,Math.floor(t*D.fps));
  const lv=D.env[f];
  const sp=speakerAt(t);
  rig('kobo',t,sp=='K',lv,sp!='K',0);
  rig('babe',t,sp=='B',lv,sp!='B',1.7);
  $('prog').style.width=(100*t/D.dur)+'%';
  // current phrase
  let pi=-1;for(let i=0;i<D.phrases.length;i++){if(D.phrases[i].s<=t+.05)pi=i;}
  if(pi>=0){
    const ph=D.phrases[pi];
    if(pi!==lastPhrase){
      $('who').textContent=ph.k=='K'?'KOBO':'BABE';$('who').style.color=ph.k=='K'?'#B38600':'#6A4FC2';
      $('txt').innerHTML=ph.w.map((w,i)=>`<span class="w" id="w${i}">${w[2]}</span>`).join(' ');
      $('tail').style.left=(ph.k=='K'?250:740)+'px';lastPhrase=pi;
    }
    ph.w.forEach((w,i)=>{const el=$('w'+i);el.className='w'+(t>=w[1]?' said':(t>=w[0]?' now':''));});
    const pop=ease((t-ph.s)/.18);$('bub').style.transform=`scale(${.96+.04*pop})`;
    $('bub').style.opacity=1;
  }
  // tail position under the bubble
  $('tail').style.top=($('bub').offsetTop+$('bub').offsetHeight-2)+'px';
  // cards
  let shown=false;
  for(const c of D.cards){const [a,b]=c;if(t>=a&&t<b){
    if($('card').dataset.k!=String(a)){$('card').dataset.k=String(a);$('ce').textContent=c[2];$('ct').textContent=c[3];$('cl').textContent=c[4];}
    const k=Math.min(ease((t-a)/.35),ease((b-t)/.3));$('card').style.opacity=k;$('card').style.transform=`translateY(${(1-k)*30}px)`;shown=true;}}
  if(!shown)$('card').style.opacity=0;
}
"""


def load(n):
    words = []
    for s in json.loads((AUDIO / f"part{n}.json").read_text()):
        words += s["words"]
    turns = TURNS[n]

    def spk(t):
        k = turns[0][1]
        for a, s in turns:
            if t + 0.05 >= a:
                k = s
        return k

    out = []
    for a, b, w in words:
        if out and not w.startswith(" "):  # piece of the previous word ("20" + "%", "fast" + "-paced")
            out[-1][1] = b
            out[-1][2] += w.strip()
            continue
        out.append([a, b, w.strip(), spk(a)])
    # fix mishearings at the text level, word by word joined then re-split
    joined = " ".join(w[2] for w in out)
    for pat, rep in FIX.items():
        joined = re.sub(pat, rep, joined)
    fixed = joined.split(" ")
    if len(fixed) == len(out):
        for w, f in zip(out, fixed):
            w[2] = f
    else:  # replacement changed word count; apply per word instead
        for w in out:
            for pat, rep in FIX.items():
                w[2] = re.sub(pat, rep, w[2])
    # phrases: same speaker, at most 9 words, break on sentence end or a pause
    phrases, cur = [], []
    for i, w in enumerate(out):
        end = cur[-1][2][-1:] if cur else ""
        if cur and (w[3] != cur[-1][3] or len(cur) >= 11 or w[0] - cur[-1][1] > 0.6
                    or (end in ".?!" and len(cur) >= 3) or (end in ",;" and len(cur) >= 6)):
            phrases.append(cur)
            cur = []
        cur.append(w)
    if cur:
        phrases.append(cur)
    phr = [{"s": p[0][0], "k": p[0][3], "w": [[w[0], w[1], w[2]] for w in p]} for p in phrases]
    # loudness envelope per video frame (mouth opening)
    y, sr = sf.read(AUDIO / f"part{n}.wav", dtype="float32")
    if y.ndim > 1:
        y = y.mean(axis=1)
    dur = len(y) / sr
    hop = sr // FPS
    env = np.array([np.sqrt(np.mean(y[i:i + hop] ** 2)) for i in range(0, len(y), hop)])
    env = env / (np.percentile(env, 95) + 1e-9)
    env = np.clip(env, 0, 1.15)
    env = np.convolve(env, [0.25, 0.5, 0.25], mode="same")
    env[env < 0.12] = 0
    return {"turns": turns, "phrases": phr, "env": [round(float(v), 3) for v in env], "fps": FPS, "dur": dur,
            "cards": CARDS.get(n, [])}, dur


def html(n, data):
    body = f"""
<div class="top"><div class="av">RD</div><div><b style="font-size:34px">{SERIES}</b>
<div style="font-size:27px;color:#6b7280">{SUBTITLE}</div></div>
<div class="part">PART {n}/{TOTAL_PARTS}</div></div>
<div class="prog"><i id="prog"></i></div>
<div class="bub" id="bub" style="opacity:0"><div class="who" id="who"></div><div id="txt"></div></div>
<div class="tail" id="tail"></div>
<div class="card" id="card"><div class="e" id="ce"></div><div><b id="ct"></b><span id="cl"></span></div></div>
{bunny_svg('kobo', KOBO_COLORS)}{bunny_svg('babe', BABE_COLORS, bow=True)}
<div class="name" style="left:208px;color:#B38600">Kobo</div><div class="name" style="right:210px;color:#6A4FC2">Babe</div>
<div class="foot">@defi_ring_master · education, not financial advice</div>"""
    if SOLO:
        body += ("<style>#babe,.name{display:none}#kobo{left:305px;top:1230px;transform:scale(1.25);transform-origin:50% 100%}.card{top:780px!important;z-index:3}#tail{left:516px!important}"
                 "</style>")
    js = JS.replace("__DATA__", json.dumps(data))
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{CSS}</style></head>"
            f"<body>{body}<script>{js}</script></body></html>")


async def render_part(n, preview_times=None):
    data, dur = load(n)
    page_html = html(n, data)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(page_html, wait_until="load")
        await pg.wait_for_timeout(300)
        if preview_times:
            shots = []
            for t in preview_times:
                await pg.evaluate(f"render({t})")
                f = f"/tmp/claude-test/duo{n}_{t}.png"
                await pg.screenshot(path=f)
                shots.append(f)
            await b.close()
            return shots
        frames = Path(f"/tmp/duo_frames_{n}")
        shutil.rmtree(frames, ignore_errors=True)
        frames.mkdir()
        total = int(dur * FPS)
        for i in range(total):
            await pg.evaluate(f"render({i / FPS})")
            await pg.screenshot(path=str(frames / f"f{i:05d}.jpg"), type="jpeg", quality=85)
        await b.close()
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{SLUG}-{n}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.jpg"),
                    "-i", str(AUDIO / f"part{n}.wav"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "21",
                    "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-shortest", "-movflags", "+faststart", str(out)],
                   check=True)
    shutil.rmtree(frames, ignore_errors=True)
    return out


if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        print(asyncio.run(render_part(n)))
