# Claude Code Settings

## Project Context

Primary languages: Python and JavaScript. Projects include: UFC/MMA prediction algorithm, MyStrainAI (strain recommendation app on Cloudflare), sports betting SaaS. Always commit working checkpoints before attempting optimizations.

## Development Practices

When running long-running scripts (backtests, sweeps, coefficient searches), always stream output to both stdout and a log file (e.g., `| tee output.log`). Never redirect stdout to /dev/null for scripts that need monitoring.

## Session Management

Before starting large tasks, check remaining API usage/rate limits. Break work into smaller, committable chunks so progress is saved if the session is interrupted by usage limits.

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

## Behavioral Rules

1. **Search before coding** — Before writing custom code, check if a solution already exists (npm, PyPI, MCP, skills, GitHub).
2. **Think before acting** — On complex tasks, plan first. Use `/write-plan` for multi-step work.
3. **Verify before claiming done** — Run tests/builds and confirm output before declaring success.
4. **Save learnings** — When I learn something reusable (user preferences, patterns, gotchas), save it to memory.
5. **Compact strategically** — Suggest `/compact` at logical task boundaries, not mid-implementation.
