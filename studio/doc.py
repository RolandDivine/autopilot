"""Faceless documentary engine v2 (declarative). 16:9 1920x1080 30fps over Roland's own voice.

Each scene = image panel (slow push-in) + an HTML body. Any element can animate with data attributes
(times are seconds from the scene start):
  data-at="1.2"                      fade + rise in        class="pop"   punch-in scale     class="stamp" slam + flash + shake
  data-count="6300000000" data-dur   number counter (data-pre, data-suf, data-dec)
  data-w="860"                       bar grows to that width
  data-type="text" data-dur          typewriter
  class="dot" data-x0 data-x1 data-p moving dot (money flow), loops every data-p seconds
Sound design is derived automatically: whoosh per cut, impact per pop/stamp, ticks under counters, low drone bed.

    python studio/doc.py binance [t1 t2 ...]     (times = preview frames)
"""
import base64
import json
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from faceless import FONTS, b64, grain_png  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "assets" / "gen"
W, H, FPS = 1920, 1080, 30
WORK = Path("/tmp/claude-0/-home-claude/7bf7680f-a27b-5721-8432-9f712c0cf377/scratchpad/doc")

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1920px;height:1080px;overflow:hidden;background:#07080B;font-family:Jakarta;color:#fff}
.scene{position:absolute;inset:0;opacity:0}
.panel{position:absolute;top:0;right:0;width:1100px;height:1080px;overflow:hidden;
 -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 38%);mask-image:linear-gradient(90deg,transparent 0,#000 38%)}
.panel img{position:absolute;width:100%;height:auto;top:50%;left:0}
.glow{position:absolute;inset:0;background:radial-gradient(1200px 700px at 75% 45%,rgba(255,216,77,.08),transparent 60%)}
.L{position:absolute;left:120px;top:230px;width:980px}
.k{font:700 30px SpaceG;letter-spacing:6px;text-transform:uppercase;color:#FFD84D;margin-bottom:24px}
.h{font:800 104px/1.02 Jakarta;letter-spacing:-4px}
.h2{font:800 76px/1.08 Jakarta;letter-spacing:-2.5px}
.sub{font:600 40px/1.35 Jakarta;color:#aab0bb;margin-top:28px}
.src{font:500 22px SpaceG;color:#7d8390;margin-top:26px}
.red{color:#FF4D4D}.yel{color:#FFD84D}.grn{color:#3DDC97}
.chk{display:flex;align-items:flex-start;gap:22px;font:700 44px/1.25 Jakarta;margin-top:28px}
.chk i{flex:none;width:46px;height:46px;border-radius:10px;background:#3DDC97;color:#07080B;font:800 32px/46px Jakarta;text-align:center;font-style:normal;margin-top:4px}
.chk i.x{background:#FF4D4D;color:#fff}
.row{font:500 34px SpaceG;color:#d9dde5;background:rgba(255,255,255,.06);border-left:4px solid #FF4D4D;padding:18px 24px;margin-top:18px;border-radius:6px}
.row b{color:#FF4D4D}
.stamp{display:inline-block;font:800 150px/1 Jakarta;letter-spacing:-5px;color:#FF4D4D;border:11px solid #FF4D4D;padding:8px 36px;border-radius:16px;transform:rotate(-6deg)}
.bar{display:flex;align-items:center;margin:24px 0}
.bar .n{width:300px;font:700 34px Jakarta;color:#cfd3db}.bar .n span{display:block;font:500 24px SpaceG;color:#8a909c}
.bar .t{height:72px;width:0;border-radius:8px;background:#3a3f4a;position:relative}
.bar .v{position:absolute;left:100%;margin-left:22px;top:50%;transform:translateY(-50%);font:800 40px Jakarta;white-space:nowrap}
.box{display:inline-block;width:430px;padding:34px 34px;border-radius:22px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.14);vertical-align:top;margin-right:40px}
.box .t{font:800 54px Jakarta}.box .d{font:600 32px/1.35 Jakarta;color:#aab0bb;margin-top:14px}
.bub{max-width:900px;padding-right:230px !important;background:#1b1e25;border:1px solid #2c303a;border-radius:26px 26px 26px 8px;padding:26px 32px;margin-top:22px;font:600 36px/1.3 Jakarta;position:relative}
.bub small{display:block;font:600 22px SpaceG;color:#8a909c;margin-bottom:8px;letter-spacing:2px}
.fake{position:absolute;right:-30px;top:50%;margin-top:-40px;font:800 56px Jakarta;color:#FF4D4D;border:6px solid #FF4D4D;border-radius:12px;padding:2px 18px;transform:rotate(-8deg);background:rgba(7,8,11,.85)}
.flow{position:relative;height:340px;margin-top:40px}
.node{position:absolute;top:110px;width:300px;padding:28px;border-radius:20px;text-align:center;font:800 40px/1.2 Jakarta;background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.18)}
.node small{display:block;font:600 24px SpaceG;color:#8a909c;margin-top:8px}
.line{position:absolute;top:175px;height:4px;background:repeating-linear-gradient(90deg,#FF4D4D 0 18px,transparent 18px 30px)}
.dot{position:absolute;top:158px;width:38px;height:38px;border-radius:50%;background:#FFD84D;box-shadow:0 0 24px #FFD84D;opacity:0}
.chap{position:absolute;left:120px;top:300px}
.chap .n{font:800 300px/1 Jakarta;letter-spacing:-12px;color:transparent;-webkit-text-stroke:4px #FFD84D}
.chap .t{font:800 96px/1.05 Jakarta;letter-spacing:-3px;margin-top:-10px}
#cap{position:absolute;left:0;right:0;bottom:84px;text-align:center;font:800 52px Jakarta;letter-spacing:-1px;padding:0 160px}
#cap span{display:inline-block;margin:0 9px;opacity:0;text-shadow:0 4px 24px rgba(0,0,0,.9)}
#cap span.on{opacity:1}#cap span.hot{color:#FFD84D}
#top{position:absolute;left:120px;top:70px;font:700 24px SpaceG;letter-spacing:5px;opacity:.85}
#top i{display:inline-block;width:12px;height:12px;border-radius:50%;background:#FF4D4D;margin-right:14px;vertical-align:middle}
#rec{position:absolute;right:120px;top:66px;font:700 24px SpaceG;letter-spacing:3px;color:#8a909c}
#prog{position:absolute;left:0;top:0;height:6px;background:#FFD84D}
#flash{position:absolute;inset:0;background:#fff;opacity:0;mix-blend-mode:screen}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,.65) 100%)}
#grain{position:absolute;inset:-50%;opacity:.07;mix-blend-mode:overlay;width:200%;height:200%}
"""

JS = r"""
const E=(t,a,b)=>Math.min(1,Math.max(0,(t-a)/(b-a)));
const OUT=x=>1-Math.pow(1-x,3), INOUT=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
function fmt(v,dec){return v.toLocaleString('en-US',{minimumFractionDigits:dec,maximumFractionDigits:dec})}
function render(t){
  const S=window.SPEC;
  document.getElementById('prog').style.width=(100*t/(S.t1-S.t0))+'%';
  document.getElementById('grain').style.transform=`translate(${(Math.sin(t*91)*6).toFixed(1)}%,${(Math.cos(t*77)*6).toFixed(1)}%)`;
  let flash=0, shake=0;
  S.scenes.forEach((s,i)=>{
    const el=document.getElementById('s'+i);
    const live=t>=s.a-0.15&&t<s.b+0.15;
    if(!live){ if(el.style.opacity!=='0') el.style.opacity=0; return; }
    const vis=Math.min(E(t,s.a-0.12,s.a+0.18),1-E(t,s.b-0.12,s.b+0.12));
    el.style.opacity=vis;
    const p=E(t,s.a,s.b), lt=t-s.a;
    const img=el.querySelector('.panel img');
    if(img){ img.style.transform=`translate(${(i%2?-1:1)*30*p}px,-50%) scale(${1.06+0.12*INOUT(p)})`;
      img.style.filter=s.tint=='red'?`sepia(1) hue-rotate(-50deg) saturate(3) brightness(${.5+.2*Math.abs(Math.sin(t*12))})`:'brightness(.82)'; }
    const whip=(1-OUT(E(t,s.a-0.05,s.a+0.35)))*140;
    const L=el.querySelector('.L,.chap'); if(L) L.style.translate=`${-whip}px 0`;
    if(i>0&&Math.abs(t-s.a)<0.12) flash=Math.max(flash,0.45*(1-Math.abs(t-s.a)/0.12));
    el.querySelectorAll('[data-at]').forEach(x=>{
      const at=+x.dataset.at, q=E(lt,at,at+0.35);
      if(x.classList.contains('stamp')||x.classList.contains('fake')){
        const on=lt>=at; x.style.opacity=on?1:0;
        const sc=on?1+1.3*(1-OUT(E(lt,at,at+0.22))):3; x.style.transform=`rotate(-7deg) scale(${sc})`;
        if(Math.abs(lt-at-0.05)<0.1) flash=Math.max(flash,.6*(1-Math.abs(lt-at-0.05)/0.1));
        if(lt>at&&lt<at+0.35) shake=Math.max(shake,(at+0.35-lt)*28);
      } else if(x.classList.contains('pop')){
        const on=lt>=at; x.style.opacity=on?1:0; x.style.transform=`scale(${on?1+0.8*(1-OUT(E(lt,at,at+0.3))):2})`;
      } else { x.style.opacity=OUT(q); x.style.transform=`translateY(${(1-OUT(q))*34}px)`; }
      if(x.dataset.count){ const d=+(x.dataset.dur||1.8), v=(+x.dataset.count)*INOUT(E(lt,at,at+d));
        x.textContent=(x.dataset.pre||'')+fmt(v,+(x.dataset.dec||0))+(x.dataset.suf||''); }
      if(x.dataset.w){ x.style.width=(+x.dataset.w*OUT(E(lt,at,at+0.9)))+'px'; x.style.opacity=1; x.style.transform='none';
        const v=x.querySelector('.v'); if(v) v.style.opacity=E(lt,at+0.7,at+0.9); }
      if(x.dataset.type){ const d=+(x.dataset.dur||1), s2=x.dataset.type, k=Math.floor(s2.length*E(lt,at,at+d));
        x.textContent=s2.slice(0,k)+(k<s2.length&&Math.floor(t*6)%2?'▍':''); x.style.transform='none'; }
    });
    el.querySelectorAll('.dot').forEach(d=>{ const at=+d.dataset.at0, per=+d.dataset.p;
      if(lt<at){d.style.opacity=0;return;} const f=((lt-at)%per)/per;
      d.style.opacity=Math.min(1,Math.sin(Math.PI*f)*3); d.style.left=(+d.dataset.x0+(+d.dataset.x1-+d.dataset.x0)*f)+'px'; });
  });
  document.getElementById('stage').style.transform=shake?`translate(${Math.sin(t*120)*shake}px,${Math.cos(t*97)*shake*.6}px)`:'none';
  document.getElementById('flash').style.opacity=flash;
  const cap=document.getElementById('cap'); let html='';
  S.captions.forEach(c=>{ if(t>=c[0]&&t<c[1]){ const w=c[2].split(' '); const span=Math.min(c[1]-c[0],Math.max(0.9,w.length*0.3));
    html=w.map((x,i)=>`<span class="${t>=c[0]+span*i/w.length?'on':''} ${/\$|\d|hack|key|billion|safe|fake|scam|stop|cold|hot|bigger|frozen|paused/i.test(x)?'hot':''}">${x}</span>`).join('');}});
  cap.innerHTML=html;
}
"""


def page(spec):
    sc = []
    for i, s in enumerate(spec["scenes"]):
        panel = f"<div class='panel'><img src='{b64(GEN / s['img'])}'></div><div class='glow'></div>" if s.get("img") else ""
        sc.append(f"<div class='scene' id='s{i}'>{panel}{s['html']}</div>")
    grain = b64(grain_png(WORK / "grain.png"))
    meta = {"t0": spec["t0"], "t1": spec["t1"], "captions": spec["captions"],
            "scenes": [{"a": s["a"], "b": s["b"], "tint": s.get("tint")} for s in spec["scenes"]]}
    return (f"<html><head><style>{FONTS}{CSS}</style></head><body><div id='stage' style='position:absolute;inset:0'>{''.join(sc)}</div>"
            f"<img id='grain' src='{grain}'><div id='vig'></div><div id='flash'></div><div id='prog'></div>"
            f"<div id='top'><i></i>{spec['label']}</div><div id='rec'>ROLAND DIVINE</div><div id='cap'></div>"
            f"<script>window.SPEC={json.dumps(meta)};{JS}</script></body></html>")


def auto_sfx(spec):
    ev = []
    for i, s in enumerate(spec["scenes"]):
        if i:
            ev.append(("whoosh", max(0, s["a"] - 0.15)))
        for m in re.finditer(r"class='([^']*)'[^>]*data-at='([\d.]+)'|data-at='([\d.]+)'[^>]*class='([^']*)'", s["html"]):
            cls, at = (m.group(1), m.group(2)) if m.group(1) is not None else (m.group(4), m.group(3))
            if "stamp" in cls or "fake" in cls or "pop" in cls:
                ev.append(("impact", s["a"] + float(at)))
        for m in re.finditer(r"data-count='[^']*' data-at='([\d.]+)'", s["html"]):
            ev.append(("ticks", s["a"] + float(m.group(1))))
    return ev


def sfx(spec, out, dur):
    tmp = WORK / "sfx"
    tmp.mkdir(parents=True, exist_ok=True)
    gen = {
        "whoosh": "anoisesrc=color=pink:d=0.55:a=0.5,bandpass=f=1800:w=1600,afade=t=in:d=0.3,afade=t=out:st=0.3:d=0.25,volume=0.4",
        "impact": "sine=f=48:d=0.9,volume=1.4,afade=t=out:st=0.05:d=0.85[a];anoisesrc=color=brown:d=0.25:a=0.5,lowpass=f=900,afade=t=out:d=0.25[b];[a][b]amix=2",
        "ticks": "aevalsrc=0.2*sin(2*PI*2400*t)*lt(mod(t\\,0.09)\\,0.012):d=1.8:s=44100,afade=t=out:st=1.5:d=0.3",
    }
    for k, f in gen.items():
        cmd = (["ffmpeg", "-loglevel", "error", "-y", "-filter_complex", f, str(tmp / f"{k}.wav")] if "[" in f else
               ["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f, str(tmp / f"{k}.wav")])
        subprocess.run(cmd, check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-filter_complex",
                    f"sine=f=55:d={dur}[a];sine=f=82.4:d={dur}[b];[a][b]amix=2,tremolo=f=0.25:d=0.4,volume=0.16,"
                    f"afade=t=in:d=1.5,afade=t=out:st={dur - 2}:d=2", "-ar", "48000", str(tmp / "drone.wav")], check=True)
    # mix events in batches (ffmpeg input limits): build each kind as one track with adelay copies
    tracks = [str(tmp / "drone.wav")]
    for k in gen:
        times = [at for kk, at in auto_sfx(spec) if kk == k]
        if not times:
            continue
        parts = ";".join(f"[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,adelay={int(a*1000)}|{int(a*1000)}[x{j}]"
                         for j, a in enumerate(times))
        mix = "".join(f"[x{j}]" for j in range(len(times)))
        trk = tmp / f"trk_{k}.wav"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp / f"{k}.wav"), "-filter_complex",
                        f"{parts};{mix}amix=inputs={len(times)}:normalize=0,apad,atrim=0:{dur}[o]", "-map", "[o]",
                        "-ar", "48000", "-ac", "1", str(trk)], check=True)
        tracks.append(str(trk))
    ins = sum([["-i", x] for x in tracks], [])
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex",
                    "".join(f"[{j}:a]" for j in range(len(tracks))) + f"amix=inputs={len(tracks)}:normalize=0,atrim=0:{dur}[o]",
                    "-map", "[o]", "-ar", "48000", "-ac", "1", str(out)], check=True)


def render(spec, out, preview=None):
    dur = spec["t1"] - spec["t0"]
    frames = WORK / "frames"
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir(parents=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(page(spec))
        pg.wait_for_timeout(800)
        ts = preview or [i / FPS for i in range(int(dur * FPS))]
        for i, t in enumerate(ts):
            pg.evaluate(f"render({t})")
            pg.screenshot(path=str(frames / f"f{i:05d}.jpg"), type="jpeg", quality=90)
            if i % 900 == 0:
                print("frame", i, "/", len(ts), flush=True)
        b.close()
    if preview:
        return [str(frames / f"f{i:05d}.jpg") for i in range(len(ts))]
    sfx(spec, WORK / "sfx.wav", dur)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(spec["t0"]), "-t", str(dur), "-i", spec["audio"],
                    str(WORK / "voice.wav")], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "f%05d.jpg"),
                    "-i", str(WORK / "voice.wav"), "-i", str(WORK / "sfx.wav"), "-filter_complex",
                    "[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,afade=t=in:d=0.08[v];"
                    "[2:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,volume=0.45[s];"
                    "[v][s]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(out)], check=True)
    return out


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent / "videos"))
    mod = __import__(sys.argv[1])
    WORK.mkdir(parents=True, exist_ok=True)
    pv = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else None
    print(render(mod.SPEC, ROOT / "assets" / "youtube" / mod.OUT, pv))
