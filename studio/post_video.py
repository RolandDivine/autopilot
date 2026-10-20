"""python studio/post_video.py <json under repo> <key> [nostory] [ytonly]: Reel + LinkedIn + IG story (auto-split under 60 s) + YouTube Short, prints links."""
import json, re, subprocess, sys, time
R = "repos/RolandDivine/autopilot"
def sh(*a): return subprocess.run(a, check=True, capture_output=True, text=True, cwd="/home/claude/autopilot").stdout
sh("git", "pull", "-q")
f, key = sys.argv[1], sys.argv[2]
d = json.load(open(f"/home/claude/autopilot/{f}"))[key]
def now(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 5))
def run(wf, fields):
    t = now()
    sh("gh", "api", "-X", "POST", f"{R}/actions/workflows/{wf}/dispatches", "-f", "ref=main", *sum([["-f", f"inputs[{k}]={v}"] for k, v in fields.items()], []))
    for _ in range(120):
        time.sleep(10)
        r = json.loads(sh("gh", "api", f"{R}/actions/workflows/{wf}/runs?per_page=3"))["workflow_runs"]
        r = [x for x in r if x["created_at"] >= t]
        if r and r[-1]["status"] == "completed":
            r = r[-1]; break
    else:
        return wf, "timed out", ""
    jobs = json.loads(sh("gh", "api", f"{R}/actions/runs/{r['id']}/jobs"))["jobs"]
    notes = []
    for j in jobs:
        for a in json.loads(sh("gh", "api", f"{R}/check-runs/{j['id']}/annotations")):
            notes.append(f"{a['title']}: {a['message']}")
    return wf, r["conclusion"], " | ".join(notes) or r["html_url"]
def yt():
    if not d.get("youtube"):  # Roland, 16 Oct: YouTube is crypto-only
        return ("youtube", "skipped (not crypto)", "")
    desc = re.sub(r"\n?📤.*\n?📌.*\n", "\n", d["reel_caption"]).strip() + "\n\nFollow for more: Instagram @defi_ring_master · LinkedIn Roland Divine"
    tags = ",".join(re.findall(r"#(\w+)", d["reel_caption"])) or "ai,crypto"
    res = run("youtube-publish.yml", {"paths": d["video"], "title": (d["title"][:90] + " #Shorts"), "description": desc, "tags": tags, "privacy": "public"})
    m = re.search(r"youtube\.com/shorts/([\w-]+)", res[2])
    if m and d.get("playlist"):
        run("youtube-admin.yml", {"ops": json.dumps([{"op": "add_to_playlist", "playlist": d["playlist"], "video_ids": [m.group(1)]}])})
    return res
if "ytonly" in sys.argv:
    print(yt()); sys.exit()
print(run("instagram-publish.yml", {"kind": "reel", "paths": d["video"], "caption": d["reel_caption"]}))
print(run("linkedin-publish.yml", {"media": d["video"], "text": d["li_text"], "title": d["title"]}))
def story_parts(video):
    """Instagram story videos must be 60 s or less (Roland, 20 Oct 2026: split, don't skip).
    Longer videos are cut at the quietest pause nearest each 55 s mark and committed to assets/reels/stories/."""
    root = "/home/claude/autopilot"
    dur = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video))
    if dur <= 59.5:
        return [video]
    err = subprocess.run(["ffmpeg", "-i", video, "-af", "silencedetect=noise=-35dB:d=0.25", "-f", "null", "-"],
                         cwd=root, capture_output=True, text=True).stderr
    pauses = [(float(a) + float(b)) / 2 for a, b in zip(re.findall(r"silence_start: ([\d.]+)", err),
                                                         re.findall(r"silence_end: ([\d.]+)", err))]
    n = int(dur // 55) + 1
    cuts, start = [], 0.0
    for _ in range(n - 1):
        target = start + (dur - start) / (n - len(cuts))
        ok = [t for t in pauses if start + 15 < t < start + 59 and dur - t > 3]
        cut = min(ok, key=lambda t: abs(t - target)) if ok else min(start + 58, (start + dur) / 2)
        cuts.append(cut)
        start = cut
    bounds = [0.0] + cuts + [dur]
    stem = video.rsplit("/", 1)[-1][:-4]
    out = []
    for i, (a, b) in enumerate(zip(bounds, bounds[1:])):
        f = f"assets/reels/stories/{stem}-{chr(97 + i)}.mp4"
        sh("mkdir", "-p", "assets/reels/stories")
        sh("ffmpeg", "-loglevel", "error", "-y", "-ss", f"{a:.2f}", "-i", video, "-t", f"{b - a:.2f}", "-c:v", "libx264", "-crf", "21",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", f)
        out.append(f)
    sh("git", "add", *out)
    subprocess.run(["git", "commit", "-qm", f"story cuts: {stem}"], cwd=root)
    sh("git", "pull", "-q", "--rebase")
    sh("git", "push", "-q")
    return out
if "nostory" not in sys.argv:  # stories are on by default (Roland, 20 Oct 2026)
    print(run("instagram-publish.yml", {"kind": "stories", "paths": " ".join(story_parts(d["video"]))}))
print(yt())
