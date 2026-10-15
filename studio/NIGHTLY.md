# Nightly build (runs in Roland's Claude conversation at 7:10 PM Lagos)

Platforms: LinkedIn (RolandDivine2) and Instagram (@defi_ring_master) both post automatically from the queue (`instagram_autopost` is true). X is off: always set `"x": {"enabled": false}`. Never post anything directly.

## Content direction (Roland, 14 Oct 2026)
- **Audience is worldwide English speakers** (Nigeria/Africa, Europe, the Americas and beyond). Write for everyone; add a local note (e.g. "In Nigeria: …") only when the rules really differ by country.
- **Every post answers one real question people are asking right now.** Each night, research questions first: Google Trends, Google "People also ask", Reddit, X and Nairaland threads, plus comments and DMs on Roland's posts. Prefer practical how-to topics (which wallet or platform, how to use it, how to stay safe, how to use an AI tool for a real task, how to build with AI today) over textbook definitions.
- The curriculum in `curriculum.py` is only a loose backbone (which track goes on which day, Launch Day 4 Feb 2027). Don't follow its lesson titles if a real question is better; basic definitions only appear as short context inside a practical post.
- Go deep: step-by-step guides with real platform names, what can go wrong, and a clear checklist people will save and send.
- Mix in build-in-public posts about what Roland is actually building (Autopilot, Klaerus, his products), using only true details.

## Steps
1. **Repo:** if `/home/claude/autopilot` is missing, call add_repo (RolandDivine/autopilot, push), clone it there, and call register_repo_root. Run `git pull`.
2. **Tomorrow:** N = (tomorrow − 2026-10-12) + 1. Run `cd studio && python -c "from curriculum import plan; print(plan(N))"`.
   - If `queue/<tomorrow>/` already has 3 slot files, skip to step 7.
   - After Day 150 (10 Mar 2027), tell Roland the plan has ended and stop.
   - Every 20th day, the 8 AM slot is a Klaerus spotlight instead of news. Builders Launch Day is Day 116 (4 Feb 2027).
3. **Context:** read the plan doc (Claude Docs 5ece558f-0172-4c73-85df-9fa489f6e424, sections "This week" and "What's working") and the playbook (d2724498-05cf-47a0-ae76-5032152d85d1).
4. **Content:** copy `studio/days/day2.py` to `studio/days/dayN.py` and rewrite it.
   - **8 AM:** a one-slide news card on the most important crypto, AI or markets development of the last 24h. Research it, check primary sources, and name the source on the card.
   - **1 PM and 7 PM:** two 7-slide practical guides, each answering one real question (see Content direction). End with the signoff slide; add a homework or checklist slide where useful.
   - **Tags:** only fact, interpretation, scenario or thesis.
   - Keep monospace lines ≤ 34 characters.
   - Run `python days/dayN.py`. It builds the LinkedIn PNGs and PDF in `media/` (terminal style, LinkedIn only).
   - **Instagram uses the Chat Bubbles style, permanently (Roland's choice, 12 Oct 2026). Never use the terminal style on Instagram.** Copy `studio/days/day2_ig.py` to `dayN_ig.py` and write the same lessons as a chat between a curious friend ("q") and Roland ("r"), using `studio/ig_chat.py`.
     - Use plain words and no tech jargon. Each slide has 2–4 bubbles, and slide 2 has its own hook.
     - The last slide asks people to save the post, send it to a named kind of friend, and follow.
     - The script makes the feed carousels in `instagram/` (JPEG) plus **5 stories** in `stories/`: 09:00 new-post teaser, 11:00 quiz ("reply A or B"), 14:00 the answer, 17:00 builders check-in or one of Roland's stories, 21:00 tomorrow preview with "turn on notifications".
     - Story text must be true. Use Roland's own experiences only from `studio/story_bank.md`; never invent personal stories for him.
5. **Check:** build contact sheets and look at every slide. Fix any overflow or wrong handle.
6. **Slots:** write `queue/<tomorrow>/{0800,1300,1900}.json`, following the format of the Day 2 files.
   - LinkedIn: 850–1,600 characters, no hashtags or emoji, links only in first_comment.
   - Instagram: a caption with 3–5 hashtags and a 📌 save / 📤 send line, plus the list of JPEGs.
   - Also write `queue/<tomorrow>/stories.json`: `[{"at": "0900", "media": "stories/s0900.jpg"}, ...]`.
   - Lint all three slots and the stories file (`autopilot.lint.lint_stories(folder)`), and fix every FAIL. Commit "Day N queue" and push. Confirm that the review issue opened.
7. **Tell Roland (SendUserMessage):** the three titles and times, the story times, and the review issue link. Also ask him one short question that would make a good story (something that really happened to him with AI, crypto or building). When he answers, add it to `studio/story_bank.md` (the repo is public, so only add what he's happy to post).
8. **Book tomorrow's run:** call send_later at 18:10 UTC the next day with the message:
   "Nightly build: follow /home/claude/autopilot/studio/NIGHTLY.md (clone RolandDivine/autopilot first if it's missing)."
   Don't skip this step: it is what keeps the nightly run going.
9. **Book tomorrow's posting runs** (GitHub's own timer runs hours late): call send_later at 07:01, 08:01, 10:01, 12:01, 13:01, 16:01, 18:01 and 20:01 UTC the next day, each asking to dispatch the post workflow (`gh api -X POST repos/RolandDivine/autopilot/actions/workflows/post.yml/dispatches -f ref=main -F 'inputs[dry_run]=false'`), wait for it, and check `log/posted.jsonl`. For 07:01, 12:01 and 18:01, tell Roland the links and the music pick; for the story runs, only message him if something failed.

## Music (Roland's request, 13 Oct 2026)
The Instagram API can't attach music to carousels (only to Reels, and only with Facebook Login), so Roland adds it in the app after each post goes out.
For every Instagram slot, set `"music"` to one old-school track that fits the mood. Rotate through Sade, Phil Collins and Michael Bolton, plus similar artists (Anita Baker, Luther Vandross, Lionel Richie, Whitney Houston, Tracy Chapman, George Michael). Don't repeat the same song within a week.
Example: `"music": "Sade – Smooth Operator"`.

## Klærus content: on hold (Roland, 15 Oct 2026)
Do not post anything about Klærus. The 15 Oct drafts are in archive/klaerus-2026-10-15 and are
outdated: Klærus was restructured and terms like "house edge" are no longer used. Wait for Roland's
restructured document before writing any Klærus content.
