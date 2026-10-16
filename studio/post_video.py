"""python studio/post_video.py <json under repo> <key> [story] [ytonly]: Reel + LinkedIn (+ IG story) + YouTube Short, prints links."""
import json, subprocess, sys, time
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
import re
def yt():
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
if "story" in sys.argv:
    print(run("instagram-publish.yml", {"kind": "stories", "paths": d["video"]}))
print(yt())
