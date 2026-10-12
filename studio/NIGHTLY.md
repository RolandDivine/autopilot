# Nightly build (runs in Roland's Claude conversation at 7:10 PM Lagos)

Platforms: LinkedIn (RolandDivine2) posts automatically from the queue. Instagram (@defi_ring_master) posts automatically only when `config.json` has `"instagram_autopost": true`; otherwise Roland posts it by hand. X is off: always set `"x": {"enabled": false}`. Never post anything directly.

## Steps
1. **Repo:** if `/home/claude/autopilot` is missing, call add_repo (RolandDivine/autopilot, push), clone it there, and call register_repo_root. Run `git pull`.
2. **Tomorrow:** N = (tomorrow − 2026-10-12) + 1. Run `cd studio && python -c "from curriculum import plan; print(plan(N))"`.
   - If `queue/<tomorrow>/` already has 3 slot files, skip to step 7.
   - After Day 150 (10 Mar 2027), tell Roland the plan has ended and stop.
   - Every 20th day, the 8 AM slot is a Klaerus spotlight instead of news. Builders Launch Day is Day 116 (4 Feb 2027).
3. **Context:** read the plan doc (Claude Docs 5ece558f-0172-4c73-85df-9fa489f6e424, sections "This week" and "What's working") and the playbook (d2724498-05cf-47a0-ae76-5032152d85d1).
4. **Content:** copy `studio/days/day2.py` to `studio/days/dayN.py` and rewrite it.
   - **8 AM:** a one-slide news card on the most important crypto, AI or markets development of the last 24h. Research it, check primary sources, and name the source on the card.
   - **1 PM and 7 PM:** two 7-slide lessons taught from zero. Each has a homework slide and ends with the signoff slide.
   - **Tags:** only fact, interpretation, scenario or thesis.
   - Keep monospace lines ≤ 34 characters.
   - Run `python days/dayN.py`. It builds the LinkedIn PNGs and PDF in `media/` and the Instagram JPEGs in `instagram/`.
5. **Check:** build contact sheets and look at every slide. Fix any overflow or wrong handle.
6. **Slots:** write `queue/<tomorrow>/{0800,1300,1900}.json`, following the format of the Day 2 files.
   - LinkedIn: 850–1,600 characters, no hashtags or emoji, links only in first_comment.
   - Instagram: a caption with 3–5 hashtags, plus the list of JPEGs.
   - Lint all three slots and fix every FAIL. Commit "Day N queue" and push. Confirm that the review issue opened.
7. **Tell Roland (SendUserMessage):** the three titles and times, plus the review issue link. If instagram_autopost is false, also send the three Instagram captions and the JPEGs (SendUserFile, one group per post).
8. **Book tomorrow's run:** call send_later at 18:10 UTC the next day with the message:
   "Nightly build: follow /home/claude/autopilot/studio/NIGHTLY.md (clone RolandDivine/autopilot first if it's missing)."
   Don't skip this step: it is what keeps the nightly run going.
