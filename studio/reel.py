"""Reel engine v3 (Roland, 5 Nov 2026): line-art essay (glowing SVG drawings) mixed with 3D scenes (three.js),
1080x1920, 30fps, word-by-word captions with keyword highlights, pill CTA. Every frame is a pure function of time
(window.seek(t)), so renders are deterministic.

    python studio/reel.py <name> [preview times...]        name = module in studio/reels/ (SPEC dict)
"""
import functools, http.server, importlib, json, shutil, subprocess, sys, threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
STUDIO = ROOT / "studio"
WORK = Path("/tmp/claude-0/-home-claude/7bf7680f-a27b-5721-8432-9f712c0cf377/scratchpad/reel")
THREE = Path("/home/claude/styles/node_modules/three")
FPS, W, H = 30, 1080, 1920

PAGE = r"""<!doctype html><html><head><meta charset=utf-8>
<style>FONTCSS</style>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;background:#0b0b0d;font-family:Jakarta,sans-serif}
#bg{position:absolute;inset:0;background:radial-gradient(1000px 1100px at 50% 42%,#18181d,#0a0a0c 70%)}
#grain{position:absolute;inset:0;opacity:.08;mix-blend-mode:screen;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='f'%3E%3CfeTurbulence baseFrequency='.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23f)'/%3E%3C/svg%3E")}
canvas{position:absolute;inset:0}
.scene{position:absolute;inset:0;opacity:0}
svg{position:absolute;inset:0;overflow:visible}
.ln{fill:none;stroke-linecap:round;stroke-linejoin:round}
.lab{position:absolute;font:700 34px SpaceG,monospace;letter-spacing:4px;text-transform:uppercase;white-space:nowrap;transform:translate(-50%,0)}
.big{position:absolute;font:800 96px Jakarta;letter-spacing:-2px;white-space:nowrap;transform:translate(-50%,0)}
#capbg{position:absolute;left:0;right:0;top:1230px;height:520px;background:linear-gradient(transparent,rgba(8,8,10,.85) 35%,rgba(8,8,10,.85) 75%,transparent)}
#cap{position:absolute;left:90px;right:90px;top:1380px;text-align:center;font:500 54px/1.32 Jakarta;color:#fff}
#cap .w{color:#5d5d63;transition:none}#cap .w.on{color:#fff}#cap .w.k.on{color:var(--k);font-weight:800}
.pill{position:absolute;left:50%;transform:translate(-50%,0);border:3px solid #ffd60a;color:#ffd60a;border-radius:999px;
 padding:22px 54px;font:800 40px Jakarta;letter-spacing:3px;white-space:nowrap;box-shadow:0 0 40px rgba(255,214,10,.35)}
.vig{position:absolute;inset:0;background:radial-gradient(1200px 1500px at 50% 45%,transparent 55%,rgba(0,0,0,.65))}
</style>
<script type="importmap">{"imports":{"three":"/three/build/three.module.js","three/addons/":"/three/examples/jsm/"}}</script>
</head><body><div id=bg></div><canvas id=gl width=1080 height=1920></canvas><div id=layers></div><div class=vig></div><div id=grain></div><div id=capbg></div><div id=cap></div>
<script type=module>
import * as T from 'three';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
const S = window.SPEC;
const ease=x=>x<0?0:x>1?1:x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2, clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const lerp=(a,b,x)=>a+(b-a)*x;
// ---------- 3D ----------
const R=new T.WebGLRenderer({canvas:document.getElementById('gl'),antialias:true,alpha:true,preserveDrawingBuffer:true});
R.setSize(1080,1920,false);R.toneMapping=T.ACESFilmicToneMapping;R.toneMappingExposure=1.1;R.setClearColor(0x000000,0);
const ENV=new T.PMREMGenerator(R).fromScene(new RoomEnvironment(),0.04).texture;
const mat=(c,o={})=>new T.MeshStandardMaterial(Object.assign({color:c,metalness:.8,roughness:.3},o));
const glow=(c,i=1.6)=>new T.MeshStandardMaterial({color:c,emissive:c,emissiveIntensity:i,metalness:.2,roughness:.4});
function base(){const s=new T.Scene();s.environment=ENV;s.environmentIntensity=.5;
 s.add(new T.AmbientLight(0xffffff,.2));const k=new T.SpotLight(0xfff0d0,120,40,.55,.6);k.position.set(4,10,6);s.add(k);
 const f=new T.Mesh(new T.PlaneGeometry(60,60),mat(0x0c0c0f,{metalness:.7,roughness:.45}));f.rotation.x=-Math.PI/2;s.add(f);
 const c=new T.PerspectiveCamera(32,1080/1920,.1,100);c.setViewOffset(1080,1920,0,300,1080,1920);return {s,c};}
const B={};
B.chip=()=>{const {s,c}=base();const g=new T.Group();s.add(g);
 const chip=new T.Mesh(new T.BoxGeometry(2.2,.3,2.2),mat(0x1d1f25,{metalness:.95,roughness:.25}));chip.position.y=.15;g.add(chip);
 const core=new T.Mesh(new T.BoxGeometry(1.1,.06,1.1),glow(0xffd60a,1.2));core.position.y=.33;g.add(core);
 for(let i=0;i<10;i++)for(const sd of[-1,1]){const p=new T.Mesh(new T.BoxGeometry(.08,.04,.4),mat(0xc9a227));p.position.set(-.9+i*.2,.05,sd*1.25);g.add(p);
   const q=p.clone();q.rotation.y=Math.PI/2;q.position.set(sd*1.25,.05,-.9+i*.2);g.add(q);}
 const bars=[];for(let i=0;i<9;i++){const h=.5+i*.38;const m=new T.Mesh(new T.BoxGeometry(.32,1,.32),glow(0x2fd27a,1.1));m.position.set(-2.2+i*.55,0,-2.2);m.userData.h=h;s.add(m);bars.push(m);}
 const red=new T.PointLight(0x2fd27a,30,10);red.position.set(0,2,-1);s.add(red);
 return {s,c,update:(u)=>{c.position.set(Math.sin(.6+u*.5)*10.5,7.4-u*.8,Math.cos(.6+u*.5)*10.5);c.lookAt(0,.45,-.6);
   bars.forEach((m,i)=>{const k=ease(clamp(u*2.2-i*.18));m.scale.y=Math.max(.001,k*m.userData.h);m.position.y=m.scale.y/2;});
   core.material.emissiveIntensity=1+.5*Math.sin(u*12);}};};
B.towers=()=>{const {s,c}=base();
 const a=new T.Mesh(new T.BoxGeometry(1,1,1),glow(0xffc82e,.55));a.position.set(-1.5,0,0);s.add(a);
 const b=new T.Mesh(new T.BoxGeometry(1,1,1),glow(0x2fd27a,.9));b.position.set(1.5,0,0);s.add(b);
 return {s,c,update:(u)=>{const ka=ease(clamp(u*3));a.scale.y=Math.max(.001,1.2*ka);a.position.y=a.scale.y/2;
   const kb=ease(clamp(u*1.5-.3));b.scale.y=Math.max(.001,30*kb);b.position.y=b.scale.y/2;
   c.position.set(0,4.4,15);c.lookAt(0,1.7,0);}};};
B.pyramid=()=>{const {s,c}=base();const P=[];const rows=5;
 for(let r=0;r<rows;r++){const n=rows-r;for(let i=0;i<n;i++)for(let j=0;j<n;j++){
   const m=new T.Mesh(new T.SphereGeometry(.22,24,16),r==rows-1?glow(0xffd60a,1.4):mat(0x8a8f99,{metalness:.3,roughness:.5}));
   m.position.set((i-(n-1)/2)*.55,.22+r*.48,(j-(n-1)/2)*.55);m.userData.r=r;s.add(m);P.push(m);}}
 const coins=[];for(let i=0;i<40;i++){const m=new T.Mesh(new T.CylinderGeometry(.11,.11,.03,24),glow(0x2fd27a,1.3));s.add(m);coins.push(m);}
 return {s,c,update:(u)=>{c.position.set(Math.sin(u*.8)*10.5,5.2,Math.cos(u*.8)*10.5);c.lookAt(0,1.3,0);
   P.forEach(m=>{const k=ease(clamp(u*2.4-(4-m.userData.r)*.12));m.scale.setScalar(Math.max(.001,k));});
   coins.forEach((m,i)=>{const ph=(u*1.6+i/40)%1;const ang=i*2.4;const rad=(1-ph)*1.5;
     m.position.set(Math.cos(ang)*rad,.2+ph*2.7,Math.sin(ang)*rad);m.rotation.set(ph*9,i,0);m.visible=u>.2;});}};};
B.vault=()=>{const {s,c}=base();const v=new T.Mesh(new T.BoxGeometry(3,3,3),mat(0x3a3d44,{metalness:.95,roughness:.28}));v.position.y=1.5;v.rotation.y=-.5;s.add(v);
 const door=new T.Mesh(new T.CylinderGeometry(1,1,.25,64),mat(0x2c2f36,{metalness:1,roughness:.25}));door.rotation.x=Math.PI/2;door.position.set(0,0,1.55);v.add(door);
 const ring=new T.Mesh(new T.TorusGeometry(1,.06,16,80),glow(0xffd60a,1.4));ring.position.set(0,0,1.68);v.add(ring);
 const cs=[];for(let i=0;i<50;i++){const m=new T.Mesh(new T.CylinderGeometry(.24,.24,.05,32),mat(0xf3ba2f,{metalness:1,roughness:.2,emissive:0x4a3000}));s.add(m);cs.push([m,Math.random()*Math.PI*1.2-.2,1.8+Math.random()*2.6,Math.random()]);}
 return {s,c,update:(u)=>{c.position.set(Math.sin(.4+u*.4)*11,7,Math.cos(.4+u*.4)*11);c.lookAt(0,.8,0);door.rotation.y=-ease(clamp(u*1.5))*1.6;
   cs.forEach(([m,a,d,r])=>{const k=ease(clamp(u*1.6-r*.5));m.position.set(Math.cos(a)*d*k-.4,.05+Math.max(0,(1-k))*1.5,Math.sin(a)*d*k+1.2);m.rotation.set(r*6,r*3,k*4);m.visible=k>0;});}};};
B.wallet3d=()=>{const {s,c}=base();const w=new T.Mesh(new T.BoxGeometry(1.6,.35,2.6),mat(0x16181d,{metalness:.6,roughness:.35}));w.position.y=.6;s.add(w);
 const scr=new T.Mesh(new T.BoxGeometry(1.1,.05,1.3),glow(0x2fd27a,.9));scr.position.set(0,.8,-.3);s.add(scr);
 const b1=new T.Mesh(new T.CylinderGeometry(.16,.16,.08,32),mat(0xc9a227));b1.position.set(-.35,.8,.75);s.add(b1);const b2=b1.clone();b2.position.x=.35;s.add(b2);
 const sh=new T.Mesh(new T.TorusGeometry(2.4,.04,16,120),glow(0x2fd27a,1.2));sh.rotation.x=Math.PI/2;sh.position.y=.6;s.add(sh);
 return {s,c,update:(u)=>{c.position.set(Math.sin(u*1.2)*7,5.5,Math.cos(u*1.2)*7);c.lookAt(0,.4,0);w.position.y=.6+Math.sin(u*6)*.08;scr.position.y=w.position.y+.2;sh.scale.setScalar(.6+ease(clamp(u*2))*.6);}};};
B.ice=()=>{const {s,c}=base();const ice=new T.Mesh(new T.BoxGeometry(2.4,2.4,2.4),new T.MeshPhysicalMaterial({color:0xcfefff,metalness:0,roughness:.12,transmission:.9,thickness:1.5,transparent:true,opacity:.55}));ice.position.y=1.2;s.add(ice);
 const coin=new T.Mesh(new T.CylinderGeometry(.75,.75,.14,64),glow(0x26a17b,.9));coin.rotation.x=Math.PI/2;coin.position.y=1.2;s.add(coin);
 const bl=new T.PointLight(0x88ccff,40,12);bl.position.set(-2,3,-2);s.add(bl);
 return {s,c,update:(u)=>{c.position.set(Math.sin(.5+u*.7)*8,4.5,Math.cos(.5+u*.7)*8);c.lookAt(0,1.1,0);const k=ease(clamp(u*2.2));ice.scale.setScalar(Math.max(.001,k));coin.rotation.z=u*2;}};};
B.quantum=()=>{const {s,c}=base();const g=new T.Group();s.add(g);for(let i=0;i<5;i++){const p=new T.Mesh(new T.CylinderGeometry(1.5-i*.22,1.5-i*.22,.08,64),mat(0xd4a64a,{metalness:1,roughness:.18}));p.position.y=4.2-i*.8;g.add(p);
  for(let j=0;j<6;j++){const t=new T.Mesh(new T.CylinderGeometry(.03,.03,.8,8),mat(0xb87333));const a=j/6*Math.PI*2;t.position.set(Math.cos(a)*(1.1-i*.2),3.8-i*.8,Math.sin(a)*(1.1-i*.2));g.add(t);}}
 const core=new T.Mesh(new T.SphereGeometry(.25,32,16),glow(0x4da3ff,2));core.position.y=.6;g.add(core);
 return {s,c,update:(u)=>{c.position.set(Math.sin(u*.9)*9,3.2,Math.cos(u*.9)*9);c.lookAt(0,2.2,0);core.material.emissiveIntensity=1.5+Math.sin(u*20);}};};
B.nodes=()=>{const {s,c}=base();const N=[];for(let i=0;i<26;i++){const m=new T.Mesh(new T.SphereGeometry(.16,24,12),i==0?glow(0xffd60a,1.6):glow(0x5ec8b8,.8));
  const r=i==0?0:1.2+Math.random()*2.4,a=Math.random()*Math.PI*2,h=i==0?1.6:.4+Math.random()*2.6;m.position.set(Math.cos(a)*r,h,Math.sin(a)*r);s.add(m);N.push(m);}
 const L=[];N.slice(1).forEach((m,i)=>{const g=new T.BufferGeometry().setFromPoints([N[0].position,m.position]);const l=new T.Line(g,new T.LineBasicMaterial({color:0x5ec8b8,transparent:true,opacity:.5}));s.add(l);L.push([l,i]);});
 return {s,c,update:(u)=>{c.position.set(Math.sin(u*1.1)*8,4.5,Math.cos(u*1.1)*8);c.lookAt(0,1.4,0);
   N.forEach((m,i)=>m.scale.setScalar(Math.max(.001,ease(clamp(u*3-i*.06)))));L.forEach(([l,i])=>l.visible=u*3-i*.06>.5);}};};
B.towers2=()=>{const {s,c}=base();const H=[.6,.9,1.3,6];const Ms=H.map((h,i)=>{const m=new T.Mesh(new T.BoxGeometry(.9,1,.9),i==3?glow(0xffd60a,.7):mat(0x8a8f99,{metalness:.6,roughness:.4}));m.position.set(-2.4+i*1.6,0,0);s.add(m);return m;});
 return {s,c,update:(u)=>{c.position.set(1,4.6,14);c.lookAt(0,2,0);Ms.forEach((m,i)=>{const k=ease(clamp(u*2-i*.25));m.scale.y=Math.max(.001,H[i]*k);m.position.y=m.scale.y/2;});}};};
const built={};
// ---------- SVG / layers ----------
const layers=document.getElementById('layers');
S.scenes.forEach((sc,i)=>{const d=document.createElement('div');d.className='scene';d.id='sc'+i;d.innerHTML=sc.html||'';layers.appendChild(d);
 if(sc.three)built[i]=B[sc.three]();});
document.querySelectorAll('.ln').forEach(p=>{const L=p.getTotalLength?p.getTotalLength():1000;p.style.strokeDasharray=L;p.dataset.L=L;});
// ---------- captions ----------
const cap=document.getElementById('cap');
function caption(t){const ph=S.phrases.find(p=>t>=p.a-.05&&t<p.b+.25);if(!ph){cap.innerHTML='';return;}
 if(cap.dataset.id!=ph.a){cap.dataset.id=ph.a;cap.style.setProperty('--k',ph.color||'#ffd60a');
  cap.innerHTML=ph.words.map((w,j)=>`<span class="w${(ph.key||[]).includes(j)?' k':''}">${w.w}</span>`).join(' ');}
 cap.querySelectorAll('.w').forEach((e,j)=>e.classList.toggle('on',t>=ph.words[j].t));
 const k=clamp((t-ph.a+.05)/.2);cap.style.opacity=k;cap.style.transform=`translateY(${(1-ease(k))*24}px)`;}
// ---------- seek ----------
window.seek=(t)=>{
 let gl=null;
 S.scenes.forEach((sc,i)=>{const el=document.getElementById('sc'+i);const lt=t-sc.a, D=sc.b-sc.a;
  let o=clamp(lt/.3)*clamp((sc.b+.3-t)/.3);el.style.opacity=o;
  const z=1+.04*clamp(lt/D);el.style.transform=`scale(${z})`;
  if(o<=0)return;
  el.querySelectorAll('.ln').forEach(p=>{const a=+p.dataset.at||0,d=+p.dataset.d||1;const k=ease(clamp((lt-a)/d));p.style.strokeDashoffset=p.dataset.L*(1-k);});
  el.querySelectorAll('[data-in]').forEach(e=>{const k=ease(clamp((lt-+e.dataset.in)/.35));e.style.opacity=k;
    e.style.translate=`0 ${(1-k)*20}px`;});
  el.querySelectorAll('[data-count]').forEach(e=>{const a=+e.dataset.at,d=+e.dataset.d,v0=+e.dataset.from,v1=+e.dataset.count;
    const k=clamp((lt-a)/d);const v=e.dataset.exp?v0*Math.pow(v1/v0,Math.pow(k,1.6)):lerp(v0,v1,ease(k));
    e.textContent=(e.dataset.pre||'')+Math.round(v).toLocaleString('en-US')+(e.dataset.suf||'');});
  el.querySelectorAll('[data-pulse]').forEach(e=>{const k=1+.05*Math.max(0,Math.sin((lt-+e.dataset.pulse)*6));e.style.scale=k;});
  el.querySelectorAll('[data-shake]').forEach(e=>{const a=+e.dataset.shake;const x=lt-a;const s=x>0&&x<.4?Math.sin(x*70)*14*(1-x/.4):0;e.style.translate=`${s}px 0`;});
  el.querySelectorAll('[data-color-at]').forEach(e=>{const on=lt>=+e.dataset.colorAt;e.style.stroke=on?e.dataset.c2:e.dataset.c1;e.style.filter=`drop-shadow(0 0 10px ${on?e.dataset.c2:e.dataset.c1})`;});
  if(built[i]&&o>0){built[i].update(clamp(lt/D));gl={b:built[i],o};}
 });
 const cv=document.getElementById('gl');
 if(gl){cv.style.opacity=gl.o;R.render(gl.b.s,gl.b.c);}else{cv.style.opacity=0;}
 caption(t);
};
window.ready=1;
</script></body></html>"""


SFX = {
    "whoosh": "anoisesrc=color=pink:d=0.5:a=0.5,bandpass=f=2000:w=1800,afade=t=in:d=0.25,afade=t=out:st=0.25:d=0.25,volume=0.35",
    "impact": "sine=f=46:d=0.9,volume=1.5,afade=t=out:st=0.05:d=0.85",
    "ticks": "aevalsrc=0.16*sin(2*PI*2600*t)*lt(mod(t\\,0.085)\\,0.01):d=3.0:s=48000,afade=t=out:st=2.6:d=0.4",
    "pop": "sine=f=880:d=0.12,afade=t=out:d=0.12,volume=0.5",
}


def mix_audio(spec, dur):
    """Voice + light sound design (whoosh on each cut, plus the spec's own hits) + a soft bed, mixed in numpy."""
    import numpy as np
    SR = 48000
    tmp = WORK / "sfx"
    tmp.mkdir(parents=True, exist_ok=True)

    def load(path):
        raw = str(tmp / (Path(path).name + ".raw"))
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(path), "-ar", str(SR), "-ac", "1", "-f", "f32le", raw], check=True)
        return np.fromfile(raw, dtype=np.float32)

    for k, f in SFX.items():
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f, str(tmp / f"{k}.wav")], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    f"sine=f=55:d={dur},volume=0.05,tremolo=f=0.2:d=0.5,afade=t=in:d=1,afade=t=out:st={dur-1.5}:d=1.5",
                    "-ar", str(SR), str(tmp / "bed.wav")], check=True)
    n = int(dur * SR)
    mix = np.zeros(n, np.float32)
    v = load(ROOT / spec["audio"])[:n]
    mix[:len(v)] += v
    b = load(tmp / "bed.wav")[:n]
    mix[:len(b)] += b
    cache = {k: load(tmp / f"{k}.wav") for k in SFX}
    events = [("whoosh", max(0, sc["a"] - 0.2)) for sc in spec["scenes"][1:]] + [tuple(e) for e in spec.get("sfx", [])]
    for k, at in events:
        snd, i = cache[k], int(at * SR)
        if i < n:
            j = min(n, i + len(snd))
            mix[i:j] += snd[:j - i]
    mix = np.clip(mix / max(1.0, float(np.abs(mix).max()) / 0.95), -1, 1).astype(np.float32)
    mix.tofile(str(tmp / "mix.raw"))
    out = tmp / "mix.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", str(tmp / "mix.raw"), str(out)], check=True)
    return out


def render(name, preview=None):
    from reels.series import REELS
    if name in REELS:
        from reels.kit import build
        tr = json.load(open(ROOT / "assets" / "vo" / f"{name}.json"))
        words = [w for seg in tr for w in seg["words"]]
        spec = build(REELS[name], words, f"assets/vo/{name}.mp3")
    else:
        spec = importlib.import_module(f"reels.{name}").SPEC
    WORK.mkdir(parents=True, exist_ok=True)
    srv_root = WORK / "site"
    if srv_root.exists():
        shutil.rmtree(srv_root)
    srv_root.mkdir()
    (srv_root / "three").symlink_to(THREE)
    from faceless import FONTS
    html = PAGE.replace("FONTCSS", FONTS)
    html = html.replace("<script type=module>", f"<script>window.SPEC={json.dumps(spec)}</script><script type=module>", 1)
    (srv_root / "index.html").write_text(html)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8766), functools.partial(
        type("Q", (http.server.SimpleHTTPRequestHandler,), {"log_message": lambda *a: None}), directory=str(srv_root)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    frames = WORK / f"{name}-frames"
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir()
    dur = spec["dur"]
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto("http://127.0.0.1:8766/index.html")
        pg.wait_for_function("window.ready===1")
        pg.wait_for_timeout(1200)
        ts = preview or [i / FPS for i in range(int(dur * FPS))]
        for i, t in enumerate(ts):
            pg.evaluate(f"window.seek({t})")
            pg.screenshot(path=str(frames / f"f{i:05d}.jpg"), type="jpeg", quality=92)
        b.close()
    srv.shutdown()
    if preview:
        return frames
    out = ROOT / "assets" / "reels" / f"{name}.mp4"
    audio = mix_audio(spec, dur) if spec.get("audio") else None
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "f%05d.jpg")]
    if audio:
        cmd += ["-i", str(audio), "-c:a", "aac", "-b:a", "192k", "-t", str(dur)]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    return out


if __name__ == "__main__":
    sys.path.insert(0, str(STUDIO))
    n = sys.argv[1]
    pv = [float(x) for x in sys.argv[2:]] or None
    print(render(n, pv))
