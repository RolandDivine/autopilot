"""Pull a viral video's generated assets into the repo and transcribe the voice.

    python viral_pull.py <name> <voice_url> [<image_url>=<file.jpg> ...]

-> assets/viral/<name>/voice.mp3, images, voice.json (Whisper word timings), /home/claude/money_audio/<name>.wav
Runs the fetch-images and transcribe workflows (the sandbox can't reach those hosts or HuggingFace).
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "repos/RolandDivine/autopilot/actions/workflows"
BR = Path("/tmp/claude-0/-home-claude/7bf7680f-a27b-5721-8432-9f712c0cf377/scratchpad/ka/r")


def sh(*a, cwd=ROOT):
    return subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout


def wait(wf, after):
    for _ in range(80):
        time.sleep(8)
        r = json.loads(sh("gh", "api", f"{REPO}/{wf}/runs?per_page=1"))["workflow_runs"][0]
        if r["created_at"] >= after and r["status"] == "completed":
            if r["conclusion"] != "success":
                raise SystemExit(f"{wf} failed: {r['html_url']}")
            return
    raise SystemExit(f"{wf} timed out")


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 5))


name, voice = sys.argv[1], sys.argv[2]
d = f"assets/viral/{name}"
items = [{"url": voice, "path": f"{d}/voice.mp3"}]
for a in sys.argv[3:]:
    url, fn = a.rsplit("=", 1)
    items.append({"url": url, "path": f"{d}/{fn}"})
t = now()
sh("gh", "api", "-X", "POST", f"{REPO}/fetch-images.yml/dispatches", "-f", "ref=main", "-f", f"inputs[items]={json.dumps(items)}")
wait("fetch-images.yml", t)
sh("git", "pull", "-q")
wav = Path(f"/home/claude/money_audio/{name}.wav")
sh("ffmpeg", "-loglevel", "error", "-y", "-i", str(ROOT / d / "voice.mp3"), "-ar", "44100", "-ac", "1", str(wav))
sh("git", "pull", "-q", "origin", "kobo-audio-2", cwd=BR)
for f in (BR / "audio").glob("*"):
    f.unlink()
sh("cp", str(wav), str(BR / "audio" / wav.name))
sh("git", "add", "-A", cwd=BR)
sh("git", "commit", "-qm", f"{name} voice", cwd=BR)
sh("git", "push", "-q", "origin", "kobo-audio-2", cwd=BR)
t = now()
sh("gh", "api", "-X", "POST", f"{REPO}/transcribe.yml/dispatches", "-f", "ref=main", "-f", "inputs[branch]=kobo-audio-2")
wait("transcribe.yml", t)
sh("git", "fetch", "-q", "origin", "kobo-audio-2")
(ROOT / d / "voice.json").write_text(sh("git", "show", f"origin/kobo-audio-2:audio/{name}.json"))
for s in json.loads((ROOT / d / "voice.json").read_text()):
    print(s["start"], s["end"], s["text"])
