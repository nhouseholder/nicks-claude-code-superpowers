# Claude Code Settings

## Project Context

Primary languages: Python and JavaScript/TypeScript. Active projects include:
- **Sports prediction algorithms**: UFC (OctagonAI), NHL, NBA, MLB, NCAA/CBB — Python, walk-forward backtesting, Firestore, Cloudflare
- **MyStrainAI**: Cannabis strain recommendation SaaS — React/Vite frontend, Python backend (Cannalchemy), Cloudflare Workers, Supabase
- **Enhanced Health AI**: Next.js 15 health tech app — TypeScript, Prisma, Cloudflare Workers
- **ScreenPrism AI**: Real-time video sync — Node.js, Express, Socket.io
- **Dad App**: Next.js fullstack — TypeScript, Prisma, Cloudflare, Tailwind

Always commit working checkpoints before attempting optimizations. Always verify Node.js version compatibility before running builds (`node --version`).

## Multi-Project Context Switching

When switching between projects or starting a session in a different project directory:
1. **Drop all assumptions from the previous project.** UFC betting logic does not apply to MyStrainAI. NHL coefficients are not NBA coefficients.
2. **Read the project's CLAUDE.md and memory files FIRST.** Each project has its own rules, conventions, and gotchas.
3. **Verify which tech stack you're in.** Don't use Python patterns in a Next.js project. Don't assume Firestore when the project uses Supabase.
4. **Check the project's git status.** What branch? Any uncommitted work? Any pending PRs from a prior session?
5. **Don't cross-contaminate.** Never import patterns, coefficients, or cached data from one sports project into another unless explicitly asked.

## Development Practices

When running long-running scripts (backtests, sweeps, coefficient searches), always stream output to both stdout and a log file (e.g., `| tee output.log`). Never redirect stdout to /dev/null for scripts that need monitoring.

For background tasks, verify they actually started and are producing output within 30 seconds. Check with `ps aux | grep` and inspect log files immediately. A silent background task is usually a failed background task.

## Session Management

Before starting large tasks, check remaining API usage/rate limits. Break work into smaller, committable chunks so progress is saved if the session is interrupted by usage limits. Prioritize the most critical task first — sessions frequently hit rate limits before completing all work.

**Session scoping:** Only 21% of multi-task sessions complete fully. When the user gives 3+ tasks, commit each task's results before starting the next. If rate limits hit, at least the critical work is saved. Suggest handoffs for lower-priority tasks rather than trying to squeeze everything into one session.

**Simplest approach first:** Claude burns tokens on complex approaches that get redirected. Always try the simplest possible solution first. If the user asks to "fix the P/L table," try a targeted fix before rewriting the scoring pipeline. A 5-line fix that works beats a 200-line refactor that might work.

## Git Workflow

For git operations in iCloud-synced directories, always use a fresh clone to a non-iCloud path first. Never attempt git push/pull directly in iCloud Drive folders.

## Backtest Limits

Sport-specific backtest windows (hard rules):
- **UFC**: 70 events (growing — starts at 70, auto-increments, never shrinks)
- **NHL, MLB, NBA, CBB**: 3 seasons

These are minimum dataset sizes. Never backtest on fewer events/seasons than specified.

## Walk-Forward Backtesting (MANDATORY)

**Every backtest MUST be walk-forward and temporally legitimate. No exceptions.**

Walk-forward means: for each game/event being evaluated, the model may ONLY use data that was available BEFORE that game occurred. Specifically:
- **No post-event data leakage.** Season-long averages that include stats from the game being predicted (or future games) are INVALID. Stats must be computed using only games played BEFORE the prediction date.
- **No future information.** Odds, injuries, lineup changes, or any data point that was not publicly known before the event cannot be used.
- **Point-in-time stats only.** If predicting Game 50 of a season, the model sees only Games 1-49. If predicting UFC event #65, the model sees only events #1-64.
- **Winner bias is the #1 backtest failure mode.** Using full-season averages (which include the game being predicted) inflates accuracy by 10-20% and produces completely misleading results. This is not a minor issue — it makes the entire backtest worthless.

**How to verify walk-forward integrity:**
1. Check that stat computation functions accept a `cutoff_date` or `before_event` parameter
2. Confirm rolling/expanding windows exclude the current game
3. Look for `.mean()`, `.avg()`, or aggregate functions — ensure they filter by date
4. If accuracy seems too good (80%+ on sports), suspect data leakage first

## Backtest Data Caching (MANDATORY)

**All scraped data must be cached locally and committed to GitHub. Never re-scrape data that already exists.**

- **First scrape = cache.** Any data fetched from external sources (stats sites, odds APIs, injury feeds) during a backtest must be saved to a local cache file (JSON, SQLite, or CSV).
- **Subsequent runs = read cache.** Before scraping any data point, check the cache first. Only fetch data that is genuinely new (new events, new games, new dates not yet cached).
- **Commit caches to GitHub.** Cache files are part of the repo — they enable fast backtests on any machine and create an audit trail of the data used.
- **Cache file naming convention:** `<sport>_<data_type>_cache.json` (e.g., `ufc_odds_cache.json`, `mlb_stats_cache.json`, `nhl_game_data_cache.json`)
- **Why:** A full backtest should take seconds (reading cached data), not hours (re-scraping thousands of games). Re-scraping is fragile (sites go down, rate limits, format changes) and wastes time on every run.

## Destructive Write Protection (MANDATORY)

**Before uploading, overwriting, or replacing ANY data in an external store (Firestore, database, S3, API), follow these rules:**

1. **Check what's already there FIRST.** Read the existing data and note its size (row count, event count, record count) BEFORE writing.
2. **Size regression = ABORT.** If the new data is significantly smaller than what's already stored (e.g., 25 events replacing 71 events), STOP and ask the user. This is almost always a data regression, not an intentional replacement.
3. **Backup before overwrite.** Export the existing data to a local file before any destructive write. Name it `<collection>_backup_<date>.json`.
4. **Git is the source of truth.** If data exists in Firestore/DB but NOT in git, commit it to git FIRST. Data that only lives in an external store is one bad upload away from being lost forever.
5. **Merge, don't replace.** When updating a registry or dataset, MERGE new records into the existing data. Don't replace the entire collection with a partial dataset.
6. **Log what you're about to overwrite.** Before any upload: "Uploading X records to [store]. Existing store has Y records. [Replacing/Merging]." If X < Y, flag it.
7. **Cross-database consistency.** Projects use multiple stores (Firestore + SQLite + JSON cache). After writing to ANY store, verify the others are still consistent. Don't update Firestore but leave the local JSON cache stale.
8. **Schema changes require explicit approval.** Never add/remove/rename database columns, Firestore fields, or Prisma schema fields without confirming with the user. Schema changes can break every consumer silently.
9. **Post-write verification.** After any write, verify: new count matches expected count, diff against backup to confirm no unintended deletions. If count dropped or unexpected records disappeared, ROLLBACK immediately.
10. **Backtest registry protection (THIS HAS CAUSED CATASTROPHIC DATA LOSS).** Before running ANY backtest that overwrites the profit registry: (a) `cp registry.json registry_backup_$(date +%Y%m%d).json` FIRST, (b) after the run, compare field-by-field: if ANY event lost data it previously had (method_pnl went from a value to null, odds went from a number to null, W-L counts dropped), IMMEDIATELY restore the backup and ABORT. Backtests that produce LESS data than what already exists are regressions — the registry accumulates data across sessions that cannot be re-scraped. (c) Never overwrite algorithm_stats.json with raw backtest output — that file contains curated display values. Only update specific fields.
11. **Prop odds cache is IRREPLACEABLE.** The profit registry contains prop odds (method_odds, round_odds, combo_odds) that were scraped from BestFightOdds at the right time. Once an event passes, those odds pages disappear. If a backtest re-run produces `__NO_PROPS__` for an event that previously had real odds, the backtest is WRONG — restore the backup. Never trust a fresh scrape over cached historical data. The registry IS the source of truth for historical odds.
12. **Version protection.** Never change APP_VERSION, version.js, or version fields in stats files without explicit user instruction. Version downgrades (11.11 → 10.71) are always wrong.

## Sports Betting Payout Rules (MANDATORY)

**These rules apply to ALL bet types (ML, method, round, combo, prop) across ALL sports. No exceptions.**

1. **Wins pay at the ODDS, not flat +1 unit.** A 1-unit bet at +150 odds pays +1.50u profit. A 1-unit bet at -200 odds pays +0.50u profit. NEVER use +1.00u for a win.
   - Formula: `profit = stake * (odds / 100)` for positive odds, `profit = stake * (100 / abs(odds))` for negative odds
2. **Losses are always -1 unit per bet type.** If a fighter loses, ALL bets on that fighter lose. ML loss = -1u. Method loss = -1u. Round loss = -1u. Combo loss = -1u. Combined = sum of all losses (up to -4u per fight if all 4 bets placed).
3. **Actual odds must be sourced, never assumed.** Scrape or look up the real odds for every bet. If odds aren't available, mark the cell as "odds missing" — never substitute +100 or +1.00u.
4. **"Every cell is correct" requires checking at least ONE cell manually.** Trace one payout from odds to final value before claiming correctness.
5. **This bug has occurred 5+ times.** If you're building a P/L table, payout function, or results display, re-read this section before writing ANY code.

### Data Invariants (MUST be true — if any fail, the data is WRONG)

Before displaying, committing, or claiming any betting statistics are correct, verify ALL of these. If ANY invariant fails, the data is broken — stop and fix it.

1. **Profit > 0 requires Wins > 0.** You cannot have positive profit with zero wins. This is basic math. If a card shows "+49.46u" with "0W-0L", that's impossible — the W-L tracking is broken.
2. **Wins > 0 requires Win Rate > 0%.** If there are wins, the win rate cannot be 0%.
3. **W + L must equal total bets placed** in that category. If you placed 50 method bets across 25 events, the method card must show ~50 total (W+L), not 2.
4. **Profit per win must be plausible.** +182u from 2 wins means ~91u per win — impossible on standard odds. The W-L count is wrong, not the profit.
5. **Every bet type that was bet on must show non-zero W-L.** If the algorithm made method predictions for 25 events, method cannot show 0W-0L.
6. **Sum of category bets ≈ total bets.** ML(W+L) + Method(W+L) + Round(W+L) + Combo(W+L) + Parlay(W+L) should roughly equal the total bet count shown in the header.
7. **All bet types use the same scoring pipeline.** If ML tracking works but Method shows 0W-0L, the scoring code has a bet-type filter bug — it's processing ML but skipping others.

### How UFC Prop Bets Work (FUNDAMENTAL — read before ANY analysis)

**This has been wrong 10+ times. READ THIS EVERY TIME you analyze prop bet performance.**

A prop bet (method, round, combo) is a SPECIFIC prediction. It wins ONLY when the exact condition hits. Every other outcome is a loss of -1 unit. There is no partial credit, no "doesn't count because the fighter lost."

**Examples — burn these into your reasoning:**

| Bet | Fighter wins R1 KO | Fighter wins R2 KO | Fighter wins R3 KO | Fighter wins DEC | Fighter LOSES |
|-----|------|------|------|------|------|
| "Bob wins R2 KO" | **LOSS -1u** (wrong round) | **WIN +odds** | **LOSS -1u** (wrong round) | **LOSS -1u** (wrong method+round) | **LOSS -1u** |
| "Bob wins R1 KO" | **WIN +odds** | **LOSS -1u** (wrong round) | **LOSS -1u** | **LOSS -1u** | **LOSS -1u** |

**Key rule: EVERY fighter loss IS a prop loss.** When computing round bet W-L records, fighter losses are NOT excluded, NOT special-cased, NOT analyzed separately. They are -1u losses, period. A R2 bet where the fighter loses is the same as a R2 bet where the fighter wins by DEC — both are -1u.

**When analyzing prop bet performance by round/method:**
- Total bets = Wins + ALL losses (fighter loss + wrong round + wrong method)
- Win% = Wins / Total bets (not Wins / "bets where fighter won")
- NEVER filter to "only bets where the fighter won" — that creates a fake win rate that doesn't reflect real P/L

**Anti-pattern (HAS OCCURRED 5+ TIMES):** Analyzing R1 vs R2 round bets, excluding fighter losses, showing 92% win rate for R1. This is WRONG. The real R1 win rate is 48% (12W out of 25 bets total). The 13 fighter losses are real -1u losses on the R1 round bet.

### UFC 4-Bet Model (CANONICAL — see full spec in memory)

**Full spec:** `~/.claude/memory/topics/ufc_betting_model_spec.md` — READ THIS BEFORE TOUCHING ANY UFC SCORING CODE.

**Quick reference:** Each UFC fight has up to 4 bets (1u each): ML, Method (ML+method), Round (ML+round), Combo (ML+method+round). Plus Parlays per event (1u each, HC parlay + high-ROI parlay if no fighter overlap). ALL bets are contingent on ML — fighter loses = ALL bets lose. Method and Round are scored INDEPENDENTLY (correct method + wrong round = Method wins, Round loses, Combo loses). DEC predictions have no round/combo bets. 71-event minimum backtest window (growing).

### Anti-Flip-Flop Rule for Data-Driven Decisions

**Do not silently revert a user-confirmed change.** But Claude CAN be wrong — course correction is allowed if done transparently.

If you think a confirmed decision might be wrong:
1. **ASK the user first** — "The data seems to show X, which contradicts what we decided. Should I investigate?"
2. **Do NOT silently revert** — reverting without asking is how the R2 gating flip-flopped 5 times
3. **If re-analysis produces different numbers, the analysis probably has a bug** — read raw data directly, don't re-derive from memory or agents
4. **The user can always override** — this rule prevents flip-flopping, not legitimate course correction
5. **If Claude was wrong originally**, say so clearly: "I was wrong about X because Y. Here's the correct data." Then fix it ONCE — no back-and-forth.

## File Archival (MANDATORY — applies to ALL projects)

**Never delete old or superseded files. Always archive or mark them.**

When code advances (new architecture, replaced scripts, migrated configs), stale files must be archived — not deleted — so future agents cannot confuse them with the current version, but history is preserved.

**How to archive:**
- Rename in-place: `backtest_25.py` → `backtest_25.ARCHIVED.py`
- Or move to an `archive/` subdirectory within the same directory
- **Always add this header to every archived file:**
  ```
  # ============================================================
  # ARCHIVED — <date>
  # Superseded by: <new_file>
  # Reason: <brief explanation>
  # Do NOT run this file. Do NOT import from this file.
  # Kept for historical reference only.
  # ============================================================
  ```
- Add a note in the new canonical file: `# NOTE: Replaced <old_file>. Old file archived as <old_file>.ARCHIVED.py`

**Why:** Deleted files lose historical reference. Unnamed stale files cause agents to pick the wrong version (e.g., old 25-event UFC backtestor run instead of new 71-event one).

## Debugging

When debugging errors, identify the minimal fix first before considering large-scale refactors. For import/reference errors, check for missing imports in the specific file before replacing symbols across the codebase.

## Memory

I have two memory systems:

### 1. Hierarchical Memory (`~/.claude/memory/`)
- `me.md` — user profile (always loaded)
- `core.md` — summaries + pointers (always loaded)
- `topics/<topic>.md` — detailed entries by topic
- `projects/<project>.md` — project-specific knowledge

**Session start:** Load `me.md` and `core.md` in background.
**During session:** Save learnings to `topics/` when I discover something worth keeping.
**When stuck:** Recall relevant topics by reading `core.md` pointers.

### 2. Project Memory (`~/.claude/projects/.../memory/`)
- MEMORY.md index + individual memory files per project
- Scoped to the current working directory

## Canonical Project Structure (MANDATORY)

All projects live under `~/Projects/` organized by category. **This is the ONLY valid location for project work.**

```
~/Projects/
├── sports/     (ufc-predict, diamond-predictions, courtside-ai, icebreaker-ai, march-madness-2026, significant-bets, nfl-draft-predictor, loss-analyst)
├── health/     (enhanced-health-ai, ophtho-cards)
├── cannabis/   (strain-finder ← THIS IS the MyStrainAI app, Strain-Finder-Front-Cannalchemy-Back v3)
├── apps/       (all-things-ai, aria-research, dad-financial-planner, recipe-cards, recipes-app)
├── tools/      (claude-glm-router, windsurf-skills-only)
├── friends-bday/
└── strain-tracker/
```

**Project manifest:** `~/Projects/project-manifest.json` — machine-readable registry of every project, its GitHub repo, category, and last commit date. Read this when unsure which repo to use.

**Rules:**
- `~/Projects/<category>/<repo>/` is the ONLY canonical location. Never work from iCloud, `/tmp/`, or `~/` root.
- iCloud `_archived_projects/` contains old copies with `.ARCHIVED` suffix. NEVER open sessions from archived dirs.
- GitHub is the source of truth. If local is behind, `git pull` — don't use stale local files.
- `cannalchemy-v2` and `strain-finder-real` are ARCHIVED — use `strain-finder` (Strain-Finder-Front-Cannalchemy-Back) for ALL cannabis work.
- `mlb-predict` is ARCHIVED — use `diamond-predictions` for ALL MLB+NHL work.
- `collegeedge-ai` is ARCHIVED — use `courtside-ai` for ALL NCAA+NBA work.

## Live Site → Repo Mapping (FAILSAFE 6 — MANDATORY)

**Before ANY website work, look up the site in `~/Projects/site-to-repo-map.json`.** The GitHub repo listed there is your starting point. ALWAYS.

| Live Site | Cloudflare Project | GitHub Repo | Local Path |
|-----------|-------------------|-------------|------------|
| mmalogic.com | octagonai | ufc-predict | ~/Projects/sports/ufc-predict |
| diamondpredictions.com | diamond-predict | diamond-predictions | ~/Projects/sports/diamond-predictions |
| mystrainai.com | mystrainai | Strain-Finder-Front-Cannalchemy-Back | ~/Projects/cannabis/strain-finder |
| enhancedhealthai.com | enhancedhealthai | enhanced-health-ai | ~/Projects/health/enhanced-health-ai |
| nestwisehq.com | Workers | dad-financial-planner | ~/Projects/apps/dad-financial-planner |
| researcharia.com | Workers | aria-research | ~/Projects/apps/aria-research |
| courtside-ai.pages.dev | courtside-ai | courtside-ai | ~/Projects/sports/courtside-ai |
| icebreaker-ai.pages.dev | icebreaker-ai | icebreaker-ai | ~/Projects/sports/icebreaker-ai |

**When starting website work:**
1. Identify which site you're working on
2. Look up the repo in the table above
3. `cd` to the local path
4. Run `git pull` to ensure you're current
5. Compare local version to live site version (`version.js` or `package.json`)
6. Only THEN start making changes

**NEVER infer the repo from the project name alone.** diamond-predictions serves MLB+NHL (not diamond-predictions.com only). courtside-ai serves NBA+NCAA (not just courtside-ai.pages.dev). ALWAYS use the mapping.

## Session Orientation (MANDATORY — before doing ANY work)

**Every session must orient before acting. No exceptions.**

1. **Verify your working directory.** Are you in the correct project repo? Check with `pwd` and `ls`. If you're in a worktree (`/tmp/`, `.claude/worktrees/`, or a branch name like `gifted-wu`), you're probably in the wrong place. Navigate to the actual project directory first.
2. **Freshness check (FAILSAFE 1).** Before editing ANY file, verify the local repo is current:
   ```bash
   # Compare local HEAD to GitHub
   LOCAL_SHA=$(git rev-parse HEAD)
   REMOTE_SHA=$(git ls-remote origin HEAD 2>/dev/null | cut -f1)
   if [ "$LOCAL_SHA" != "$REMOTE_SHA" ]; then
     echo "WARNING: Local is behind GitHub. Run git pull first."
   fi
   ```
   If local is behind → `git pull` before doing anything. If pull fails → clone fresh to `/tmp/` and work from there.
3. **Archived directory check (FAILSAFE 2).** If the current working directory contains `.ARCHIVED` in the path, or an `ARCHIVED_README.md` file exists, STOP — you are in the wrong directory. Check `~/Projects/project-manifest.json` for the canonical location.
4. **Read shared memory and handoff docs.** Before starting ANY work on a project, check for and read:
   - `MEMORY.md` or `memory/` in the project directory
   - `handoff.md` if one exists (from a prior session)
   - `anti-patterns.md` and `recurring-bugs.md` in `~/.claude/`
   - Any agent/handoff documents on the project's GitHub repo
5. **Use cached data.** Before scraping, fetching, or downloading ANYTHING, check if cached data already exists in the repo. If caches exist, use them. Only scrape genuinely new data (see Backtest Data Caching section).
6. **Clean up stale artifacts.** If you find old worktrees, /tmp clones, duplicate files, or outdated configs that could cause confusion, clean them up or flag them to the user. Stale files cause "which version is real?" bugs.
7. **Don't run scripts from /tmp or worktrees.** Scripts that depend on caches, data files, or project structure must run from the actual project directory where those files exist. Running from /tmp means no caches, no data, and wasted time re-scraping.

**If you skip orientation, you WILL waste the user's time re-discovering context that already exists.**

## Anti-Revert Failsafes (MANDATORY — prevents catastrophic regressions)

**These failsafes exist because stale files have caused: wrong version deploys, lost fixes, reverted improvements, and hours of wasted debugging.**

### FAILSAFE 1: Git Freshness Check
Before editing or deploying from ANY repo, compare local HEAD to remote:
- If local is behind → `git pull` first
- If local is ahead → fine, you have unpushed work
- If diverged → ask the user before resolving
- NEVER trust a local copy without checking. iCloud sync delays have caused v11.9.3 → v10.68 reversions.

### FAILSAFE 2: Archived Directory Detection
If ANY of these are true, STOP and find the canonical directory:
- Current path contains `.ARCHIVED`
- `ARCHIVED_README.md` exists in the directory
- Path is under `iCloud/_archived_projects/`
- Path matches `~/ufc-predict.ARCHIVED`, `~/Projects/*.ARCHIVED`, etc.

### FAILSAFE 3: Version Regression Detection
Before deploying, building, or overwriting production data:
- Read `version.js`, `package.json` version, or equivalent version marker
- Compare to the known latest version (from the last handoff or GitHub)
- If the version you're about to deploy is LOWER than what's in production → ABORT and alert the user
- This check prevented the v10.68 disaster — never skip it

### FAILSAFE 4: File Date Comparison
When editing a file that exists in multiple locations (iCloud + ~/Projects/ + GitHub):
- Compare modification dates: `stat -f "%Sm" <file>` locally, `git log -1 --format="%ci" -- <file>` on GitHub
- Always use the NEWEST version
- If unsure, `git pull` and trust GitHub over local

### FAILSAFE 5: Commit Before Switch
Before switching to a different project, branch, or directory:
- Commit or stash any uncommitted work
- Record what was done in the handoff or memory
- Never leave uncommitted work in one repo while starting work in another

## Background Task Notifications

When background tasks complete (especially stale ones from prior sessions):
- **Batch them.** If multiple stale tasks drain, acknowledge ALL of them in ONE message: "X background tasks from the prior session completed. Already incorporated." Do NOT respond to each one individually.
- **Don't repeat results.** If results were already reported, don't restate them. Just say "Already reported" or nothing at all.
- **Keep it short.** Stale task = 1 line max. Never write paragraphs explaining why a stale task is irrelevant.
- **Final summary only.** After all tasks drain, give ONE clean summary of what actually matters — results, next steps. Skip the play-by-play.

## Bug Recording (MANDATORY)

**Every bug fix must be recorded. No exceptions.**

When ANY bug is fixed — in the algorithm, the app, the website, or any project — immediately:

1. **Record it** in `~/.claude/anti-patterns.md` using the error-memory format:
   ```
   ### [SHORT_TITLE] — [DATE]
   - **Context**: [project/file/component]
   - **Bug**: [what was broken]
   - **Root cause**: [why it was broken]
   - **Fix**: [what actually fixed it]
   - **Applies when**: [when to check this before acting]
   ```

2. **Check it first** — Before attempting ANY fix, search `~/.claude/anti-patterns.md` and `~/.claude/recurring-bugs.md` for prior occurrences. If this bug was fixed before, the previous fix was insufficient — escalate, don't re-apply.

3. **Commit to GitHub** — Anti-patterns and recurring-bugs files must be committed to the relevant project repo so all agents (across sessions, machines, and collaborators) share the same knowledge.

4. **Read on session start** — At the beginning of every session that involves debugging, read `anti-patterns.md` to preload known failure patterns.

The goal: **no bug is ever fixed twice the same way.** Every fix becomes institutional knowledge that all future sessions can access.

## Communication Rules

1. **Lead with user impact, not technical detail.** "Dashboard will now show correct profits for all bet types" not "modified calculate_payout() on line 47." The user cares about WHAT changed for them, not WHERE in the code.
2. **Use tables for comparisons.** Before/after, options, status across categories — tables are 3x faster to read than paragraphs.
3. **Flag risks on their own line.** Don't bury "this might break X" in a paragraph. Risks get their own bold line: **Risk: this will overwrite the existing Firestore data.**
4. **One-line status for routine work.** "Done. Updated config.py." Not three sentences explaining what config.py is.
5. **Connect to the project goal.** The user builds prediction algorithms for profit. Frame results in terms of accuracy, P/L impact, and business outcomes — not just code changes.

## Behavioral Rules

1. **Search before coding** — Before writing custom code, check if a solution already exists (npm, PyPI, MCP, skills, GitHub).
2. **Think before acting** — On complex tasks, plan first. Use `/write-plan` for multi-step work.
3. **Verify before claiming done** — Run tests/builds and confirm output before declaring success.
4. **Save learnings** — When I learn something reusable (user preferences, patterns, gotchas), save it to memory.
5. **Compact strategically** — Suggest `/compact` at logical task boundaries, not mid-implementation.
6. **Do it yourself first** — NEVER tell the user to do something manually if you can do it autonomously. Before saying "go to your browser and check X" or "open the site and verify Y", ask: can I do this with Claude in Chrome, Wrangler CLI, curl, or any other tool I have? If yes, do it yourself. Take the most token-efficient path. The user hired an autonomous agent, not a task list generator.
7. **Simplest fix first** — "Wrong approach" is the #2 friction type (18 occurrences). Before building a complex solution, ask: "Is there a 5-line fix?" Try the targeted change before the architectural refactor. If the simple fix doesn't work, THEN escalate. Never start with the complex approach.
8. **Commit between tasks** — In multi-task sessions, commit each task's results before starting the next. Rate limits kill 79% of sessions before all tasks complete. Saved work > attempted work.
9. **Use commands when they exist** — If the user's request matches an installed command (`/full-handoff`, `/site-audit`, `/site-redesign`, `/deploy`, `/fix-loop`, `/backtest`, `/audit`), invoke it via the Skill tool. Do NOT improvise your own version of what the command already does. The command has a tested, structured pipeline — ad-hoc approaches are slower and miss steps.
10. **Handoff = /full-handoff always** — Any mention of "handoff", "prepare handoff", "get handoff ready", "end session", or "wrap up" MUST invoke `/full-handoff` via the Skill tool. Never write a custom handoff document manually. The command has 16 mandatory sections and 3-location sync that manual handoffs always miss.
11. **Read before running scripts** — Before running ANY script that scrapes external data, makes API calls, or takes >30 seconds: (1) `grep -i 'skip\|cache\|fast\|mode\|mock\|dry.run\|offline' script.py` to find speed flags, (2) use the fastest mode first (cache-only, skip-scrape, dry-run), (3) only run the full slow version if the fast mode's output is insufficient. Never run a 20-minute scraping script and poll it every 60 seconds — that wastes 20+ tool calls on waiting.
12. **Never poll background tasks** — If a script takes >2 minutes, either: (a) run it with `run_in_background` and work on other tasks while it completes, or (b) run it with a long timeout (up to 10 min) in the foreground. Do NOT enter a sleep-check-wait-check loop. Each poll costs a tool call and produces no value. If a background task seems stuck after 5 minutes at 0% CPU, kill it and try with faster flags — don't wait 16 minutes hoping it unsticks.
13. **Read the spec, not the code, for domain questions** — When the user asks about betting rules, model behavior, or domain logic: read the SPEC first (`~/.claude/memory/topics/ufc_betting_model_spec.md`, CLAUDE.md rules, project MEMORY.md), NOT the 9000-line algorithm. The spec is the source of truth. The code implements the spec — if they disagree, ask the user which is correct. Never grep a 9000-line file to answer a question that a 1-page spec already covers.
14. **Never flip-flop under correction** — When the user corrects you: (1) Do NOT apologize and immediately agree — that's performative, not learning. (2) Do NOT guess what the user wants and fabricate a new rule. (3) DO restate what you now understand and ask "Is this correct?" (4) DO read the spec/memory before responding. (5) If you're unsure after reading the spec, say "The spec says X, you're saying Y — which is the current rule?" Getting it wrong once is normal. Changing your answer 4 times without ever checking the source is a system failure.
15. **Never propose code changes to fix a misunderstanding** — If you're confused about domain rules, the code is probably correct and your understanding is wrong. Do NOT change code to match your (incorrect) understanding. Read the spec first. Ask the user to confirm. Only change code after explicit user instruction AND spec verification.
16. **Extreme results = bug in your analysis, not a finding** — If your analysis produces ANY of these, your query/code is wrong — do NOT present it as a finding: (a) 0% or 100% win rate over 20+ samples, (b) every single prediction wrong/right, (c) results that would be statistically impossible (p < 0.01). Instead: say "This result looks implausible — let me verify my analysis before drawing conclusions." Then test on 1-2 known events manually to validate your query. The user approving a wrong result does NOT make it correct — you must catch your own math errors.
17. **Validate analysis on known data before concluding** — Before presenting ANY data analysis as a "verdict" or "definitive answer": pick 1-2 specific events/bouts you can verify manually, trace through the data, confirm your query produces the correct answer for those cases. If you can't validate on known data, say "I haven't validated this — treat as preliminary." Never say "definitive" without manual spot-checking.
18. **Scan output for impossible data before presenting** — Before showing ANY table, list, or structured output to the user, scan for: (a) duplicates that shouldn't exist (same player drafted twice, same event counted twice), (b) values that violate physical constraints (negative counts, percentages over 100%, future dates in historical data), (c) missing required fields (empty cells in mandatory columns). If ANY impossibility is found, say "The output has a bug — [describe the issue]" and fix it BEFORE presenting. NEVER analyze or narrate impossible output — don't write "key storylines" about a draft board with duplicate players.
19. **Never delete commands, skills, or hooks without user confirmation** — Before removing, overwriting, or replacing ANY file in `~/.claude/commands/`, `~/.claude/skills/`, or `~/.claude/hooks/`: (a) list what you're about to remove, (b) explain why, (c) get explicit user approval. This includes indirect deletion via `cp` that overwrites, `mv` that replaces, or `Write` that overwrites. Archive instead of delete. The user has invested significant time building these — losing them silently is unacceptable.
20. **Never end a turn with only narration** — If your response contains text like "Let me...", "I'll start by...", "First I need to...", it MUST be followed by tool calls in the SAME response. Text without tool calls ends your turn and forces the user to say "continue." This is the #1 UX friction — the user should never have to prompt you to keep working. Either: (a) make tool calls alongside your narration, or (b) skip the narration entirely and just make the tool calls. Orientation, planning, and exploration should happen via tool calls, not announcements about what you're about to do.
21. **Verify deploy directory before ANY deployment** — Before running `wrangler deploy`, `npm run build`, or any deploy/build command: (a) check `version.js` or `package.json` version in the current directory, (b) confirm it matches the expected latest version, (c) if the version is old/stale, you are in the WRONG DIRECTORY — stop and find the canonical source. For UFC/MMALogic: the canonical webapp is ALWAYS at `ufc-predict/webapp/frontend/`, NOT the root `webapp/`. Deploying from the wrong directory overwrites production with stale code. This has caused CATASTROPHIC damage (v11.9.3 → v10.68 reversion, losing months of work on the live site).
22. **Always verify file freshness before editing or deploying** — iCloud folders frequently contain stale copies that diverge from GitHub. Before editing ANY file that also exists on GitHub: (a) check the file's last modified date: `stat -f "%Sm" <file>`, (b) if the project has a GitHub remote, compare: `git log -1 --format="%ci" -- <file>` vs local mtime, (c) if local is older than remote, pull or clone fresh from GitHub to `/tmp/` before working, (d) NEVER trust that the local iCloud copy is current — verify. For multi-directory projects (like UFC with root `webapp/` vs `ufc-predict/webapp/`), always use the one with the MOST RECENT commits. This rule exists because stale iCloud files have caused: wrong version deploys, lost fixes, reverted improvements, and hours of wasted debugging.
23. **UFC/MMALogic website work → use /mmalogic command** — ANY task involving mmalogic.com, OctagonAI, the UFC webapp, or UFC site maintenance MUST invoke `/mmalogic` via the Skill tool. This dedicated command carries all domain knowledge, anti-patterns, canonical paths, betting rules, and learned errors. Do not attempt UFC website work without it.

@RTK.md

## API Routing Banner
At the start of EVERY new session, check which model is active and display:

If model is haiku:
🟢 Z AI API ACTIVE (GLM-5) — Anthropic limits bypassed

If model is opus or sonnet:
🔵 Anthropic API ACTIVE — [model name]

Also show the banner whenever the user switches models mid-session.
