"""Open (or refresh) the review issue for every queued day that doesn't have one.

    python -m autopilot.review
"""
import datetime as dt
import json

from . import github, load_config
from .lint import lint_slot
from .queue import QUEUE, Slot

LABELS = {"0800": "8 AM", "1300": "1 PM", "1900": "7 PM"}
DAY1 = dt.date(2026, 10, 12)


def render(date):
    cfg = load_config()
    folder = QUEUE / date
    day_no = (dt.date.fromisoformat(date) - DAY1).days + 1
    d = dt.date.fromisoformat(date)
    lines = [f"Autopilot posts these on **{d:%a %d %b}** unless you say otherwise.",
             "",
             "Reply with a comment to control it: `skip 1pm` · `skip 7pm instagram` · `skip all` · `pause` · `resume`.",
             "To change wording, tap the file link, then the pencil icon, edit, and commit before the slot time.",
             ""]
    for slot in cfg["slots"]:
        p = folder / f"{slot}.json"
        if not p.exists():
            continue
        s = Slot(date, slot, p)
        data = s.load()
        issues = lint_slot(data, s)
        lines += [f"---", f"### {LABELS.get(slot, slot)} · {data.get('title', '')}",
                  f"[edit this post](../blob/main/queue/{date}/{slot}.json)", ""]
        x = data.get("x", {})
        if x.get("enabled"):
            lines.append(f"**X** ({len(x.get('posts', []))} tweet{'s' if len(x.get('posts', [])) != 1 else ''})")
            for i, t in enumerate(x.get("posts", []), 1):
                media = f" _[+ {', '.join(t.get('media', []))}]_" if t.get("media") else ""
                lines.append(f"> **{i}.** " + t["text"].replace("\n", "\n> ") + media)
                lines.append(">")
        li = data.get("linkedin", {})
        if li.get("enabled"):
            media = f" _[+ {li['media']}]_" if li.get("media") else ""
            lines.append(f"**LinkedIn**{media}")
            lines.append("> " + li.get("text", "").replace("\n", "\n> "))
            if li.get("first_comment"):
                lines.append(f"\nFirst comment: {li['first_comment']}")
        ig = data.get("instagram", {})
        if ig.get("enabled"):
            lines.append(f"\n**Instagram** _[{len(ig.get('media', []))} slides]_")
            lines.append("> " + ig.get("caption", "").replace("\n", "\n> "))
        if issues:
            lines.append("")
            for lvl, plat, rule, detail in issues:
                mark = "BLOCKED" if lvl == "FAIL" else "check"
                lines.append(f"- **{mark}** · {plat} · {rule} · {detail}")
        lines.append("")
    title = f"Day {day_no} · {d:%a %d %b} · review"
    return title, "\n".join(lines)


def main():
    if not github.available():
        print("GITHUB_TOKEN not set; printing instead")
    today = dt.date.today()
    for folder in sorted(QUEUE.glob("20*-*-*")):
        date = folder.name
        if dt.date.fromisoformat(date) < today - dt.timedelta(days=1):
            continue
        title, body = render(date)
        if not github.available():
            print(title); print(body); continue
        existing = github.find_day_issue(date)
        if existing:
            github.update_issue(existing["number"], title=title, body=body)
            print(f"updated #{existing['number']} {title}")
        else:
            iss = github.create_issue(title, body, [f"day:{date}", "autopilot"])
            print(f"opened #{iss['number']} {title}")


if __name__ == "__main__":
    main()
