"""9:30 PM Lagos: make sure tomorrow's posts are in the queue. If not, open an alert issue."""
import datetime as dt

from . import github
from .queue import QUEUE, lagos_now


def main():
    tomorrow = (lagos_now() + dt.timedelta(days=1)).date().isoformat()
    slots = sorted(p.name for p in (QUEUE / tomorrow).glob("*.json")) if (QUEUE / tomorrow).is_dir() else []
    if len(slots) >= 3:
        print(f"ok: {tomorrow} has {slots}")
        return
    print(f"::warning title=queue missing::{tomorrow} has {slots}")
    if github.available() and not github.find_day_issue(f"missing-{tomorrow}"):
        github.ensure_label("action-needed", "D73A4A")
        github.create_issue(
            f"Tomorrow's posts are missing ({tomorrow})",
            f"The queue for {tomorrow} has {len(slots)} of 3 posts, so nothing new will go out tomorrow.\n\n"
            "Fix: open your Claude conversation and say \"build tomorrow's posts\".",
            [f"day:missing-{tomorrow}", "action-needed"])


if __name__ == "__main__":
    main()
