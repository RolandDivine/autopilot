# Studio: how the nightly session builds a day

1. `python studio/curriculum.py` shows the plan. Use `plan(day)` to get the day's two lessons, and see whether slot 1 is News or a Klaerus spotlight (every 20th day).
2. Write the slides with the brand module. `studio/example_day1.py` shows the tone and layout.
   ```
   cd studio && RD_PLATFORM=x_linkedin python - <<'PY'
   from rd_terminal import *; from export import export
   s = [slide(0,7, command("learn crypto --lesson 2/100") + h1("...")), ..., signoff(6,7,"...")]
   export(s, "caption", "../queue/2026-10-13/media", "crypto2")
   PY
   ```
   This gives `crypto2-1.png … crypto2-7.png` plus `crypto2.pdf`. `RD_PLATFORM=x_linkedin` must be set so the slides show @RolandDivine2.
3. Write `queue/YYYY-MM-DD/{0800,1300,1900}.json` (format at the top of `autopilot/queue.py`):
   - X: a 2–6 tweet thread. The first tweet carries `media/<name>-1.png` (the cover). Don't link in the first tweet.
   - LinkedIn: the full text, `"media": "media/<name>.pdf"` and `"media_title"`. Put sources or links in `first_comment`.
4. Run `python -c "import json,sys;from autopilot.lint import lint_slot;..."` (or `pytest`), then commit and push to main. The review issue opens automatically.
