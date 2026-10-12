import datetime as dt
import json

import pytest

from autopilot import control, lint, post, queue
from autopilot.linkedin_client import escape_commentary

UTC = dt.timezone.utc


def slot_json(**over):
    d = {
        "title": "Test",
        "kind": "lesson",
        "x": {"enabled": True, "posts": [{"text": "Money is a shared story. Here's how it works."},
                                         {"text": "Part two."}]},
        "linkedin": {"enabled": True, "text": "Money is a shared story.\n\nHere's how it works (simply).",
                     "first_comment": "Source: example"},
    }
    d.update(over)
    return d


@pytest.fixture
def q(tmp_path, monkeypatch):
    monkeypatch.setattr(queue, "QUEUE", tmp_path / "queue")
    monkeypatch.setattr(queue, "LOG", tmp_path / "log" / "posted.jsonl")
    monkeypatch.setattr(control, "CONTROL", tmp_path / "control.json")
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    def add(date, slot, data):
        p = tmp_path / "queue" / date / f"{slot}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data))
        return p
    return add


def at_lagos(date, hhmm):
    d = dt.date.fromisoformat(date)
    return dt.datetime(d.year, d.month, d.day, int(hhmm[:2]) - 1, int(hhmm[2:]), tzinfo=UTC)


def test_due_window(q):
    q("2026-10-13", "1300", slot_json())
    assert queue.due_slots(at_lagos("2026-10-13", "1259")) == []
    assert len(queue.due_slots(at_lagos("2026-10-13", "1300"))) == 1
    assert len(queue.due_slots(at_lagos("2026-10-13", "1529"))) == 1   # late GitHub run still posts
    assert queue.due_slots(at_lagos("2026-10-13", "1531")) == []      # too late: don't post stale


def test_overnight_slot_seen_after_midnight(q):
    q("2026-10-13", "1900", slot_json())
    # 19:00 + 150 min grace = 21:30, still same day; but yesterday's folder is scanned too
    assert len(queue.due_slots(at_lagos("2026-10-13", "2100"))) == 1


def test_never_posts_twice(q):
    q("2026-10-13", "0800", slot_json())
    now = at_lagos("2026-10-13", "0805")
    queue.record("2026-10-13/0800", "x", {"status": "posted"})
    queue.record("2026-10-13/0800", "linkedin", {"status": "posted"})
    assert queue.due_slots(now) == []


def test_dry_run_posts_nothing_and_logs_nothing(q, capsys):
    q("2026-10-13", "0800", slot_json())
    rc = post.run(dry_run=True, now_utc=at_lagos("2026-10-13", "0801"))
    out = capsys.readouterr().out
    assert rc == 0
    assert "[dry-run] X post" in out
    assert not queue.LOG.exists()


def test_skip_and_pause_parsing():
    c = control.parse(["skip 1pm", "Skip 7pm X\nnothing else"])
    assert control.is_skipped(c, "1300", "x") and control.is_skipped(c, "1300", "linkedin")
    assert control.is_skipped(c, "1900", "x") and not control.is_skipped(c, "1900", "linkedin")
    assert not control.is_skipped(c, "0800", "x")
    assert control.parse(["skip all"])["skip"] >= {("0800", None), ("1300", None), ("1900", None)}
    assert control.parse(["pause"])["pause"] is True
    assert control.parse(["pause", "resume"])["pause"] is False
    assert control.parse(["looks good"])["pause"] is None


def test_paused_blocks_posting(q, capsys):
    q("2026-10-13", "0800", slot_json())
    control.set_paused(True)
    post.run(dry_run=True, now_utc=at_lagos("2026-10-13", "0801"))
    assert "paused" in capsys.readouterr().out


def test_lint_blocks_long_tweet_and_wrong_handle():
    bad = slot_json(x={"enabled": True, "posts": [{"text": "a" * 281}, {"text": "follow @defi_ring_master"}]})
    rules = {(p, r) for lvl, p, r, d in lint.lint_slot(bad) if lvl == "FAIL"}
    assert ("x", "too-long") in rules and ("x", "wrong-handle") in rules
    assert lint.blocked_platforms(lint.lint_slot(bad)) == {"x"}


def test_lint_counts_urls_as_23():
    t = "read " + "https://example.com/" + "x" * 300
    assert lint.x_length(t) == 5 + 23


def test_lint_banned_but_ok_when_warning_about_it():
    assert lint.lint_slot(slot_json(linkedin={"enabled": True, "text": "Earn passive income now"}))
    ok = slot_json(linkedin={"enabled": True, "text": "Anyone promising passive income is a red flag."})
    assert not [i for i in lint.lint_slot(ok) if i[0] == "FAIL"]


def test_linkedin_escaping():
    assert escape_commentary("Step (1): read [this]") == r"Step \(1\): read \[this\]"
    assert escape_commentary("#crypto rocks") == "#crypto rocks"
    assert escape_commentary("@me") == r"\@me"


def test_linkedin_token_roundtrip(tmp_path, monkeypatch):
    from autopilot import li_token
    monkeypatch.setattr(li_token, "FILE", tmp_path / "li.enc")
    monkeypatch.setenv("LINKEDIN_CLIENT_SECRET", "s3cret")
    monkeypatch.delenv("LINKEDIN_ACCESS_TOKEN", raising=False)
    li_token.save({"access_token": "abc", "person_urn": "urn:li:person:1", "expires": "2026-12-11"})
    assert b"abc" not in (tmp_path / "li.enc").read_bytes()
    assert li_token.load()["access_token"] == "abc"
    assert "client_id=78hozpq7114k7y" in li_token.sign_in_link()
