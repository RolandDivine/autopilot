"""Facebook Page admin. OPS env = JSON list of ops; each op's result is printed, failures don't stop the rest.

  {"op": "show"}                                       current Page details
  {"op": "info", "about": "...", "description": "...", "website": "..."}
  {"op": "picture", "path": "assets/facebook/profile.jpg"}
  {"op": "cover", "path": "assets/facebook/cover.jpg"}
  {"op": "name", "name": "..."}                        Meta usually only allows this in the app
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot.fb_client import FacebookClient, FacebookError  # noqa: E402

RAW = "https://raw.githubusercontent.com/{}/main/{}"


def url(path):
    return RAW.format(os.environ.get("GITHUB_REPOSITORY", "RolandDivine/autopilot"), path)


def run(c, o):
    op = o["op"]
    if op == "show":
        return c._req("GET", c.page_id, params={"fields": "name,username,about,description,website,category,link,picture{url},cover"})
    if op == "info":
        data = {k: o[k] for k in ("about", "description", "website") if k in o}
        out = {}
        for k, v in data.items():  # one field at a time, so one refusal doesn't block the others
            try:
                out[k] = c._req("POST", c.page_id, data={k: v})
            except FacebookError as e:
                out[k] = f"FAILED {e}"
        return out
    if op == "picture":
        return c._req("POST", f"{c.page_id}/picture", data={"picture": url(o["path"])})
    if op == "cover":
        photo = c._req("POST", f"{c.page_id}/photos", data={"url": url(o["path"]), "published": "false"})
        return c._req("POST", c.page_id, data={"cover": photo["id"], "no_feed_story": "true"})
    if op == "name":
        return c._req("POST", c.page_id, data={"name": o["name"]})
    raise ValueError(f"unknown op {op}")


def main():
    c = FacebookClient()
    bad = 0
    for o in json.loads(os.environ["OPS"]):
        try:
            print(f"[{o['op']}] OK", json.dumps(run(c, o))[:600])
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"[{o['op']}] FAILED {e}")
    print(f"::notice::{bad} op(s) failed" if bad else "::notice::all ops done")


if __name__ == "__main__":
    main()
