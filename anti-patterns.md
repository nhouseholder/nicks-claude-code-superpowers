# Anti-Patterns — Known Failures & Working Fixes

> This file is auto-maintained by the error-memory skill.
> Claude checks this before debugging to avoid repeating known-bad approaches.
> Last updated: 2026-03-16

## Build & Environment

### Node 25 Rollup deadlock — 2026-03-16
- **Context**: Vite/Rollup builds on Node.js 25+
- **Failed approach**: Running `vite build` without env override — hangs indefinitely
- **Why it failed**: Node 25 has a worker thread deadlock bug with Rollup's parser
- **Working fix**: Set `ROLLUP_PARSE_WORKERS=0` before build commands
- **Applies when**: Any Vite/Rollup build on Node 25+

### OpenViking ollama provider — 2026-03-16
- **Context**: OpenViking ov.conf embedding configuration with Ollama
- **Failed approach**: Setting `"provider": "ollama"` in embedding.dense config
- **Why it failed**: OpenViking only accepts providers: openai, volcengine, vikingdb, jina
- **Working fix**: Use `"provider": "openai"` with `"api_base": "http://localhost:11434/v1"` and `"api_key": "ollama"` — Ollama's OpenAI-compatible endpoint works fine
- **Applies when**: Configuring OpenViking with local Ollama models

### OpenViking server host binding — 2026-03-16
- **Context**: OpenViking server startup with no API key
- **Failed approach**: Setting `"host": "0.0.0.0"` with `"root_api_key": null`
- **Why it failed**: Security check blocks unauthenticated non-localhost binding
- **Working fix**: Use `"host": "127.0.0.1"` for local-only access without API key
- **Applies when**: Running OpenViking server locally without authentication

## Code Patterns

### Import/reference errors — minimal fix first — 2026-03-16
- **Context**: Any project, any language
- **Failed approach**: Replacing symbols across the entire codebase when seeing an import error
- **Why it failed**: Shotgun approach causes unintended side effects in unrelated files
- **Working fix**: Check for missing imports in the specific file first. Only expand scope if the issue is genuinely systemic.
- **Applies when**: Debugging import errors, reference errors, undefined symbol errors

## API & Integration

## Framework-Specific

## Project-Specific

### Git operations in iCloud Drive — 2026-03-16
- **Context**: Any project stored in iCloud Drive (`~/Library/Mobile Documents/com~apple~CloudDocs/`)
- **Failed approach**: Running `git push` or `git pull` directly in iCloud-synced directories
- **Why it failed**: iCloud sync conflicts with git's file operations, causing corruption or failed pushes
- **Working fix**: Clone to a non-iCloud path first (`~/tmp/` or `/tmp/`), do git operations there
- **Applies when**: Any git push/pull in directories under iCloud Drive

### Polling Background Processes Instead of Diagnosing — 2026-03-20
- **Context**: Any long-running background task (backtests, scraping, builds)
- **Failed approach**: Checking process status 8+ times ("still running?", "any output yet?") with no new information each time
- **Why it failed**: Each status check is a wasted tool call (~50-100 tokens). The process was hung on network I/O but this wasn't diagnosed until check #8.
- **Working fix**: Check once. If no progress, immediately diagnose (CPU%, lsof, network state). Also do pre-flight checks: verify required inputs (cache files, data) exist BEFORE starting the task.
- **Applies when**: Starting any process with `run_in_background` or any task expected to take >60 seconds

## Courtside AI — Grading Pipeline

### Self-healing window too small — 2026-03-21
- **Context**: NCAA/NBA picks not appearing in recent results despite games finishing
- **Bug**: `live-results.js` and `nba-live-results.js` self-healing only checked yesterday + day-before-yesterday (2-day window). If grading failed 3+ consecutive days, older dates fell off permanently.
- **Root cause**: Design flaw — 2-day window assumed grading would only fail 1-2 days at most
- **Fix**: Extended self-healing to 7 days. Both endpoints now loop `daysAgoCT(1)` through `daysAgoCT(7)` and heal any missing dates.
- **Applies when**: Any grading gap investigation. Check self-healing window first.

### Hardcoded EST timezone in GitHub Actions — 2026-03-21
- **Context**: Grading cron running 1 hour late during daylight saving time (March-November)
- **Bug**: `auto-generate.yml` and `grade-results.yml` used `timezone(timedelta(hours=-5))` which is EST. During DST, the correct offset is -4 (EDT), causing grading to run at 8 AM EDT instead of 7 AM.
- **Root cause**: Python's `timezone(timedelta(hours=N))` is a fixed offset, not DST-aware
- **Fix**: Replaced with `zoneinfo.ZoneInfo('America/Chicago')` which handles DST automatically
- **Applies when**: ANY date/time computation in GitHub Actions or Python scripts. NEVER use fixed UTC offsets — always use named timezones.

### Missing graded results ≠ missing picks — 2026-03-21
- **Context**: User sees gaps in recent results and assumes grading is broken
- **Root cause**: Often the ML pipeline simply didn't generate picks for those dates (0 games passed APEX/AGREE/MADNESS filters). Self-healing can't grade what was never predicted.
- **Diagnosis**: Check Firestore `predictions` collection for the date — if empty, no picks were generated. This is expected behavior, not a grading bug.
- **Applies when**: Investigating "missing results" — always verify predictions exist before assuming grading failed.

### Environment Setup Spiral — Don't Debug Infrastructure When the Bug Is Logic — 2026-03-21
- **Context**: Running backtests or long scripts that require caches, clones, symlinks, env vars
- **Failed approach**: Spent 40+ tool calls debugging cache staleness, manifest mismatches, curl vs requests differences, shallow clone issues — when the actual bug was `UFC_NUM_EVENTS=0` causing `0 >= 0 = True` (loop exits immediately)
- **Why it failed**: Assumed the problem was infrastructure (caching) when it was a trivial logic bug. Never mentally traced the env var value through downstream code.
- **Working fix**: (1) Use zero-iteration to trace env var values through all code paths before setting them. (2) When testing parameter changes, write a 10-line isolated script instead of running the full pipeline. (3) If the full pipeline fails, check the SIMPLEST explanations first (wrong value, missing input, trivial logic error) before diving into infrastructure debugging.
- **Applies when**: Setting env vars for scripts, running A/B parameter tests, any "it works in isolation but not in the pipeline" situation

### 0 NCAA PICKS — MISSING TIER FIELD + NEUTRAL_SITE — 2026-03-21
- **Context**: predict_and_upload.py → predictions.json → isActionablePick()
- **Bug**: 0 picks shown for 3+ days despite 50+ games occurring
- **Root cause**: FOUR compounding failures:
  1. `predict_and_upload.py` never set `tier` field on predictions → `isActionablePick()` requires tier
  2. `neutral_site` field never included in predictions.json → MADNESS tier couldn't detect tournament games
  3. Firestore upload fails (Cloudflare 403 bot protection) → `cron-generate.js` can't assign tiers server-side
  4. `auto_predict.sh` env vars not exported to Python subprocess (`source` without `set -a`)
- **Fix**: 
  - Added MONEYLINE/AGREE/APEX/MADNESS tier assignment logic directly in `predict_and_upload.py`
  - Added `neutral_site` and `is_neutral` fields to predictions.json output
  - Used `set -a` / `set +a` around `source ~/.courtside-env` for auto-export
  - Pipeline no longer depends on Firestore upload for tier visibility
- **Applies when**: Adding new tier fields, changing pick visibility logic, modifying prediction pipeline output fields. Always verify the FULL chain: pipeline → Firestore/static → API endpoint → frontend filter.

### SETDEFAULT_DOESNT_OVERRIDE — 2026-03-21
- **Context**: nhl_predict/algorithms/conglomerate.py predict_game_all_tiers
- **Bug**: `setdefault()` was used to "relax" thresholds, but setdefault never overrides existing keys
- **Root cause**: setdefault only sets a key if it doesn't already exist — when params dict has production thresholds, they're never relaxed
- **Fix**: Changed to direct assignment: `relaxed["KEY"] = value`
- **Applies when**: Any time you want to override/force a dict value — never use setdefault for that

### MISSING_WINNER_FIELD_IN_ARCHIVE — 2026-03-21
- **Context**: scripts/daily_pipeline.py ingest_results(), backtester.py line 228
- **Bug**: ingest_results() creates game records without a "winner" field. Backtester skips games where winner is None.
- **Root cause**: build_archives.py sets "winner" but ingest_results() (live pipeline) didn't
- **Fix**: Added `"winner": home_team if home_goals > away_goals else away_team` to record dict
- **Applies when**: Adding new fields to game records — always check if backtester needs them

### DIRECT_URL_NAVIGATION_SPA — 2026-03-21
- **Context**: diamond-predictions SportContext.jsx, App.jsx
- **Bug**: Direct URL navigation to /nhl/* showed MLB content because SportContext defaults to localStorage (mlb)
- **Root cause**: SPA renders index.html for all routes, but SportContext didn't check URL path on init
- **Fix**: Added getSportFromURL() that checks window.location.pathname for /nhl prefix, plus explicit /nhl routes in App.jsx
- **Applies when**: Any SPA with multiple "modes" driven by URL paths — always check URL on initial load

### NCAA/NBA grading skips picks silently — 2026-03-22
- **Context**: All 6 grading files (cron-grade, live-results, grade-picks for NCAA+NBA)
- **Bug**: Predictions store short team names ("High Point") but ESPN returns full names ("High Point Panthers"). The `norm()` exact-match on `away|home` keys failed silently, incrementing `skipped++` without any error log. Every pick was skipped, resulting in 0 graded results.
- **Root cause**: `scoreMap[key]` required exact normalized string match. Short name "highpoint" ≠ "highpointpanthers".
- **Fix**: Added `findInMap()` helper that tries exact match first, then prefix matching (either name is a prefix of the other). Applied to all 6 grading files.
- **Applies when**: Any grading code that maps predictions to ESPN scores by team name. Always use fuzzy/prefix matching, never exact-only.

### Tier field priority wrong in grading — 2026-03-22
- **Context**: cron-grade.js line 247, live-results.js line 230, grade-picks.js lines 304/397
- **Bug**: Graded results used `pred.system_tier_label` as primary tier field, but v12.29.0+ predictions use `pred.tier`. Results got wrong tier labels.
- **Root cause**: `system_tier_label` was the original field name from early versions. New predictions use `tier` field exclusively.
- **Fix**: Changed all tier resolution to `pred.tier || pred.system_tier_label || fallback_chain`.
- **Applies when**: Any code that reads the tier from a prediction document. Always check `pred.tier` first.

### WRONG EVENT PROCESSED — 2026-03-22
- **Context**: UFC Sunday pipeline (track results → backtest → predictions)
- **Bug**: Pipeline processed "Namajunas vs. Cortez" (71st event in reverse chronology, ~2 years old) instead of "Murphy vs. Evloev" (the actual event that just occurred)
- **Root cause**: Algorithm's event listing returned events in reverse chronological order and Claude blindly processed whatever came back without verifying it was the correct/current event
- **Fix**: Added "Data Freshness Gate" to proactive-qa — before processing ANY event results, verify the event name/date matches reality via web search. Added temporal verification trigger to sanity-check.
- **Applies when**: Any time processing "last night's event", "today's game", or any time-sensitive data pipeline. ALWAYS verify the event/game is the correct one before running the full pipeline.

### COMBO_PAYOUT_ZERO — 2026-03-22
- **Context**: OctagonAI website P/L tracking table
- **Bug**: Combo bets showed 33W-48L = -48.00u. All 33 wins contributed $0 profit — only losses counted.
- **Root cause**: Win payout formula was broken for combo bet type. Code counted losses (-1u each) but returned 0 for wins instead of calculating payout from odds.
- **Reasoning failure**: Claude treated "fix the table" as a mechanical code edit (Sonnet-tier) instead of a math verification task (Opus-tier). Never spot-checked: "33 wins at juicy odds = $0 profit? That's impossible."
- **Fix**: Fixed payout formula for combo bets. Added arithmetic spot-check to zero-iteration skill.
- **Additional failure**: "Fix" introduced regressions — ML, Method, Round P/L all decreased from known-good values. Claude broke working calculations while fixing the combo column.
- **Applies when**: Any task involving P/L calculations, payout formulas, or financial data. Always verify with a concrete example before claiming done. Route to Opus, not Sonnet.

### IMPOSSIBLE_STATS_DISPLAYED (RECURRING x5) — 2026-03-22
- **Context**: OctagonAI website front page performance dashboard
- **Bug**: Cards show logically impossible data: "+49.46u profit with 0W-0L", "+118.51u with 0W-0L", "100% win rate on 2W-0L but +182u profit" (91u/win impossible). Claude displayed and verified these as "correct."
- **Root cause**: TWO compounding failures: (1) Scoring pipeline processes ML bets correctly but skips or miscounts Method/Round/Combo/Parlay W-L records. (2) Claude does not apply basic math sanity checks — "positive profit from zero wins" is a logical impossibility that should be caught before any domain knowledge.
- **Reasoning failure**: Claude treats statistics display as a "rendering task" instead of a "data integrity task." It checks if the UI renders without errors, not whether the NUMBERS make sense. "Every cell is correct" was claimed without checking if any cell was mathematically possible.
- **Fix**: Added 7 mandatory data invariants to CLAUDE.md. Must verify: profit>0 requires wins>0, wins>0 requires WR>0%, W+L=total bets, profit/win is plausible, all bet types show non-zero records, category sums ≈ total.
- **Applies when**: ANY statistics display, dashboard, summary card, performance page, or aggregate data. Before claiming correct, check EACH card against the invariants. If even ONE fails, the data pipeline is broken.

### FLAT_UNIT_PAYOUT_BUG (RECURRING x5) — 2026-03-22
- **Context**: ALL bet types across ALL P/L tables, event results, backtests
- **Bug**: Wins display as +1.00u regardless of actual odds. Method wins at +150 show +1.00u instead of +1.50u. This has occurred 3+ times across combo, method, and prop bets.
- **Root cause**: Claude defaults to "win = +1 unit" mental model instead of "win = payout at odds". This is a DOMAIN KNOWLEDGE gap, not a code bug. Claude does not instinctively understand that sports bet payouts are odds-dependent.
- **Additional failure**: When a fighter LOSES, Claude sometimes only records the ML loss (-1u) but forgets the method/prop losses (-1u each). A loss on fighter X means ALL bets on fighter X lose.
- **Fix**: Mandatory rules added to CLAUDE.md: wins pay at odds (not flat +1u), losses = -1u per bet type, actual odds must be sourced. See "Sports Betting Payout Rules" in CLAUDE.md.
- **ESCALATION**: This is a 3x recurrence. Previous fixes (COMBO_PAYOUT_ZERO, METHOD_PNL_NULL_WITH_WINS) were insufficient because they fixed specific bet types instead of the root mental model. The CLAUDE.md rule is the systemic fix.
- **Applies when**: ANY P/L calculation, payout formula, results table, event tracking, or bet display. ALWAYS re-read CLAUDE.md "Sports Betting Payout Rules" before touching payout code.

### METHOD_PNL_NULL_WITH_WINS — 2026-03-22
- **Context**: track_results.py → EventSlideshow.jsx → live site display
- **Bug**: Website showed Method "2W-0L" with "0.00u" P/L. Method cells showed ✓ checkmark but no unit amount. Combined P/L only reflected ML, not ML+Method.
- **Root cause**: Three compounding issues: (1) `ml_profit(None)` returned 0.0 instead of 1.0 (even money fallback), so bets without odds produced $0 profit on wins. (2) Display components allowed `method_correct=true` with `method_pnl=null` to render as ✓ with "—" instead of inferring +1.0u. (3) Combo column was regressed out of the display components during a refactor (dca526f), and combined calculation excluded combo P/L.
- **Fix**: (1) Changed `ml_profit(None/0)` to return `wager` (1.0u even money). (2) Added `safePnl()` defense function in display that infers +1.0u for wins and -1.0u for losses when pnl is null. (3) Added post-scoring validation in `score_predictions()` that catches any bout where correct!=null but pnl==null and auto-fills. (4) Restored Combo column to tables and included combo in combined totals.
- **Applies when**: Any change to track_results.py scoring logic, display components showing per-fight P/L, or refactors that touch table columns. Always verify: if wins > 0, P/L MUST be > 0.
