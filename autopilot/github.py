"""Tiny GitHub REST helper for the daily review issue (runs inside GitHub Actions)."""
import os

import requests

API = "https://api.github.com"


def _h():
    return {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Accept": "application/vnd.github+json"}


def repo():
    return os.environ["GITHUB_REPOSITORY"]


def owner():
    return os.environ.get("GITHUB_REPOSITORY_OWNER", repo().split("/")[0])


def available():
    return bool(os.environ.get("GITHUB_TOKEN") and os.environ.get("GITHUB_REPOSITORY"))


def find_day_issue(date):
    r = requests.get(f"{API}/repos/{repo()}/issues", headers=_h(), timeout=30,
                     params={"labels": f"day:{date}", "state": "all", "per_page": 5})
    r.raise_for_status()
    items = [i for i in r.json() if "pull_request" not in i]
    return items[0] if items else None


def ensure_label(name, color="FFD84D"):
    r = requests.post(f"{API}/repos/{repo()}/labels", headers=_h(), json={"name": name, "color": color}, timeout=30)
    if r.status_code not in (201, 422):  # 422 = already exists
        r.raise_for_status()


def create_issue(title, body, labels):
    for l in labels:
        ensure_label(l)
    r = requests.post(f"{API}/repos/{repo()}/issues", headers=_h(), timeout=30,
                      json={"title": title, "body": body, "labels": labels})
    r.raise_for_status()
    return r.json()


def update_issue(number, **fields):
    r = requests.patch(f"{API}/repos/{repo()}/issues/{number}", headers=_h(), json=fields, timeout=30)
    r.raise_for_status()
    return r.json()


def comment(number, body):
    r = requests.post(f"{API}/repos/{repo()}/issues/{number}/comments", headers=_h(), json={"body": body}, timeout=30)
    r.raise_for_status()


def owner_comments(number):
    r = requests.get(f"{API}/repos/{repo()}/issues/{number}/comments", headers=_h(), timeout=30, params={"per_page": 100})
    r.raise_for_status()
    me = owner().lower()
    return [c["body"] for c in r.json() if c["user"]["login"].lower() == me]
