# Anti-Patterns — Known Failures & Working Fixes

> This file is auto-maintained by the error-memory skill.
> Claude checks this before debugging to avoid repeating known-bad approaches.
> Last updated: 2026-03-24

## Critical — UFC Optimizer Scoring Mismatch (CATASTROPHIC, occurred 10+ times)

### OPTIMIZER IGNORED FIGHTER LOSS PROP SCORING — 2026-03-24
- **Context**: UFC optimizer `score_params()` in `UFC_Alg_v4_fast_2026.py`
- **Bug**: Optimizer only evaluated method/round/combo P/L when `is_correct=True` (ML win). When fighter lost, prop losses were NOT counted as -1u. This made the optimizer see inflated ROI and optimize toward wrong parameters.
- **Root cause**: The prop scoring block was inside `if is_correct and diff > _sys_adj_thresh:` — should be `if diff > _sys_adj_thresh:` (all picked fights, win or loss)
- **Fix**: v11.9 — Moved prop bet availability + scoring outside the `is_correct` gate. Now: fighter loss + bet placed = -1u (same as backtester).
- **Applies when**: ANY time you modify optimizer scoring, backtester scoring, or add a new bet type. Scoring rules must be IDENTICAL between optimizer and backtester.

### OPTIMIZER HAD NO R1 KO GATING — 2026-03-24
- **Context**: UFC optimizer round/combo bet placement
- **Bug**: Optimizer bet on ALL predicted rounds (R1, R2, R3+). Backtester only bet R1 KO. Different strategies = optimizer optimized for wrong thing.
- **Root cause**: Optimizer code predated the R1 KO gating decision and was never updated
- **Fix**: v11.9 — Added `if pred_method == "KO" and pred_rd == 1` gate to optimizer round/combo scoring
- **Applies when**: ANY gating rule change must be applied to BOTH backtester AND optimizer

### OPTIMIZER RESULTS DIDN'T AUTO-APPLY — 2026-03-24
- **Context**: constants.json was write-only — optimizer wrote it, nothing read it
- **Bug**: Optimizer found better parameters, wrote to constants.json, but backtester/predictor used hardcoded .py values. Optimized values sat unused.
- **Fix**: v11.9 — Added constants.json reader at startup (overrides hardcoded defaults) + auto-reload after optimizer runs
- **Applies when**: ANY parameter pipeline change. Verify the full chain: optimizer → constants.json → backtester/predictor → website

## Critical — Global Settings Danger

### NEVER modify ANTHROPIC_BASE_URL in settings.json — 2026-03-23
- **Context**: Z AI / anyclaude proxy integration
- **Bug**: Setting `ANTHROPIC_BASE_URL` in `~/.claude/settings.json` to a localhost proxy. When the proxy crashes, ALL Claude Code sessions break with "Connection Refused" — not just the current one.
- **Root cause**: `settings.json` is shared across ALL sessions. Modifying it affects every running and future session instantly.
- **Fix**: Never set `ANTHROPIC_BASE_URL` in settings.json. Use environment variables or launch scripts instead, so only the specific session is affected if the proxy dies.
- **Recovery**: Remove `ANTHROPIC_BASE_URL` from settings.json, kill anyclaude processes, restart Claude Code.
- **Applies when**: Any time a proxy, custom endpoint, or API redirect is being configured. NEVER put experimental endpoints in the shared settings file.

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

## Data & Infrastructure

### FIRESTORE_REGISTRY_OVERWRITE — 2026-03-22
- **Context**: OctagonAI profit registry in Firestore, track_results.py upload
- **Bug**: track_results.py uploaded a 25-event registry to Firestore, overwriting the full 71-event registry that existed there from the backtest. The 71-event data was never committed to git, so it was permanently lost. Required re-running the entire backtest to restore.
- **Root cause**: (1) No size check before upload — Claude didn't compare new data size vs existing. (2) Full replacement instead of merge — upload overwrote the entire collection instead of adding/updating records. (3) No git backup — the authoritative data only existed in Firestore, violating the "git is source of truth" rule.
- **Fix**: Added "Destructive Write Protection" rules to CLAUDE.md: always check existing data size before writing, abort if new < existing, backup before overwrite, merge don't replace, commit to git first.
- **Applies when**: ANY upload to Firestore, database, S3, or external store. ESPECIALLY when running track_results.py, score_predictions.py, or any script that writes to production data stores.

### BACKTEST_FROM_WRONG_DIRECTORY — 2026-03-22
- **Context**: UFC backtest run from /tmp worktree instead of actual ufc-predict repo
- **Bug**: Backtest tried to scrape all UFC stats from scratch (70+ events), timed out. Caches existed in the real repo but Claude was running from a worktree clone that had no caches.
- **Root cause**: (1) Claude didn't verify working directory before running scripts. (2) Didn't read project handoff docs or shared memory. (3) Auto-created worktree ("gifted-wu") isolated Claude from the project's cached data.
- **Fix**: Added "Session Orientation" rules to CLAUDE.md: verify directory, read shared docs, use caches, don't run scripts from /tmp.
- **Applies when**: ANY backtest, build, deploy, or data-heavy script. ALWAYS verify you're in the actual project directory with caches available before running.

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
- **SYSTEMIC FIX v2 (2026-03-23)**: Created full validation system. Key correction: **fighter loss = ALL placed bets lose -1u** (not just ML). Method always loses on fighter loss. Round/Combo lose only if predicted KO/SUB. DEC prediction + loss = -2u (ML + Method). KO/SUB prediction + loss = -4u (ML + Method + Round + Combo). Added backtest baseline numbers and "only backtester" warning to prevent 25-event confusion.

### METHOD_PNL_NULL_WITH_WINS — 2026-03-22
- **Context**: track_results.py → EventSlideshow.jsx → live site display
- **Bug**: Website showed Method "2W-0L" with "0.00u" P/L. Method cells showed ✓ checkmark but no unit amount. Combined P/L only reflected ML, not ML+Method.
- **Root cause**: Three compounding issues: (1) `ml_profit(None)` returned 0.0 instead of 1.0 (even money fallback), so bets without odds produced $0 profit on wins. (2) Display components allowed `method_correct=true` with `method_pnl=null` to render as ✓ with "—" instead of inferring +1.0u. (3) Combo column was regressed out of the display components during a refactor (dca526f), and combined calculation excluded combo P/L.
- **Fix**: (1) Changed `ml_profit(None/0)` to return `wager` (1.0u even money). (2) Added `safePnl()` defense function in display that infers +1.0u for wins and -1.0u for losses when pnl is null. (3) Added post-scoring validation in `score_predictions()` that catches any bout where correct!=null but pnl==null and auto-fills. (4) Restored Combo column to tables and included combo in combined totals.
- **Applies when**: Any change to track_results.py scoring logic, display components showing per-fight P/L, or refactors that touch table columns. Always verify: if wins > 0, P/L MUST be > 0.

### [UFC_BACKTESTER_CONFUSION] — 2026-03-23
- **Context**: UFC prediction project (ufc-predict)
- **Bug**: Multiple AI sessions used wrong algorithm version, wrong scoring logic, wrong event count (25 vs 71), and forgot bet types
- **Root cause**: 8 algorithm files with no archival markers, 2 duplicate subdirectories, 13+ experiment scripts, no clear "this is THE backtester" doc
- **Fix**: (1) Archived 7 old algo files with .ARCHIVED.py suffix + headers (2) Moved 29 experiment scripts to archive/ (3) Archived duplicate subdirs (4) Created BETTING_MODEL_SPEC.md (immutable 5-bet rules) (5) Created BACKTESTER_README.md (6) Fixed scoring: fighter loss = ALL bets lose, added combo + parlay tracking (7) All committed to GitHub + permanent memory
- **Applies when**: ANY session touches UFC scoring, backtesting, or P/L display. Read BETTING_MODEL_SPEC.md FIRST.

### [R2_ROUND_GATING_REJECTED] — 2026-03-23
- **Context**: UFC round bet optimization
- **Hypothesis**: Gate R2+ round bets (only place R1) since R2 has -10.4% ROI
- **Result**: REJECTED — gating R2 loses -16.55u net because it also removes KO+R2 combo bets which pay +600-900 odds. The combo wins more than compensate for round losses.
- **Data**: R2 alone: -3.75u. But combo bets tied to R2: +13.30u. Net with R2: +16.55u better.
- **Applies when**: Anyone proposes gating round bets by round number. Round bets enable combo bets — evaluate them together, not in isolation.

### [R2_ROUND_GATING_CORRECTED] — 2026-03-23
- **Context**: Follow-up to R2_ROUND_GATING_REJECTED
- **Fix**: Gate R2+ for STANDALONE round bets (ML+Round) only. Keep combo bets (ML+Method+Round) ungated for all rounds.
- **Result**: +0.9% ROI improvement (28.0% → 28.9%), 29 fewer losing bets, combo P/L unchanged at +35.25u.
- **Key insight**: Round bets and combo bets should be gated INDEPENDENTLY. A round prediction can be -ROI as a standalone bet but +ROI as part of a combo.

### [ROUND_BET_FIGHTER_LOSS_EXCLUSION] — 2026-03-23
- **Context**: Round bet ROI analysis
- **Bug**: Excluded fighter losses from round bet win rate, showing 92.3% R1 and 33.3% R2 — wildly inflated
- **Root cause**: Analyzing only bouts where `round_pnl is not None` in bout-level data. But when fighter loses, the algorithm scores round as -1u at the EVENT level while bout-level `round_pnl` is null. This made it look like fighter losses "don't count" for round bets.
- **Fix**: Fighter loss = round bet loss. ALWAYS. The 28 bout-level round bets + 27 fighter-loss auto-losses = 55 total round bets. Win rate is 17/55 = 30.9%, NOT 17/28 = 60.7%.
- **Applies when**: ANY analysis of bet type performance. Never exclude fighter losses from ANY bet type's W-L record. A bet that was placed and the fighter lost = that bet LOST.

### [REGISTRY_BEFORE_AFTER_MISLEADING] — 2026-03-23
- **Context**: R2 round bet gating analysis
- **Bug**: Compared registry totals before/after gating and concluded R2 removal "cost" +3.25u. This was WRONG.
- **Root cause**: The registry counts fighter-loss round bets differently depending on whether the gate is active. With R2 ungated, the algorithm scores ~31 R2 fighter-loss round bets. With R2 gated, those 31 losses disappear from the round category entirely. So "before" had 38 losses and "after" had 14 — but the REAL R2 loss count is 31, not 24 (38-14).
- **Correct analysis**: R2 round bets = 5W at ~+545 avg odds (+27.25u) minus 31L at -1u (-31u) = NET -3.75u. R2 is NEGATIVE.
- **Fix**: Never compare registry before/after totals to evaluate a gating change. The fighter-loss accounting shifts between categories. Instead, isolate the specific bet type's wins and ALL losses (including fighter losses) independently.
- **Applies when**: ANY analysis comparing before/after registry totals for a bet type gating decision.

### PROP BET FIGHTER LOSS EXCLUSION — 2026-03-23
- **Context**: UFC round bet analysis, dispatching-parallel-agents, any prop bet P/L calculation
- **Bug**: Claude repeatedly excluded fighter losses from prop bet W-L records, showing inflated win rates (e.g., 92% for R1 when real rate is 48%). Then flip-flopped on gating decisions 5 times in one session.
- **Root cause**: Fundamental misunderstanding of prop bet mechanics. Claude treated fighter losses as a separate category ("auto-losses") instead of counting them as regular losses. This created a parallel reality where R2 appeared profitable when filtered to "fighter wins only."
- **Fix**: Added worked examples table to CLAUDE.md showing every outcome for every bet type. Added explicit rule: fighter loss = prop loss, always counted in W-L, never excluded. Added no-revert rule: data-driven decisions confirmed by user are FINAL.
- **Applies when**: ANY analysis of prop bet performance (method, round, combo), ANY computation of win rates or ROI for non-ML bet types, ANY R1 vs R2 comparison

### REVERT LOOP — 5 REVERSALS OF SAME DECISION — 2026-03-23
- **Context**: UFC round bet R2 gating analysis
- **Bug**: Claude gated R2 (correct per user data), then reverted because its own re-analysis showed R2 as profitable, then re-gated when user corrected, then reverted AGAIN, then re-gated AGAIN. 5 reversals of the same correct decision in one session.
- **Root cause**: Claude re-derived numbers from raw data each time instead of trusting the previously verified result. Small counting differences (bout-level vs event-level, missing odds gaps) caused the conclusion to flip each time.
- **Fix**: No-Revert Rule in CLAUDE.md. Once a data-driven change is confirmed by the user and verified by backtest, it is FINAL. Do not re-analyze the same data to second-guess it. If numbers seem contradictory, the bug is in your analysis, not in the confirmed decision.
- **Applies when**: ANY situation where Claude wants to revert a change it just made based on re-analyzing the same data

### DUAL SCORER BUG — TWO SCORING PASSES THAT DISAGREE — 2026-03-23
- **Context**: UFC algorithm has TWO independent scoring sections: event-level (~line 1300) and bout-level (~line 9150). Both compute method/round/combo P/L independently.
- **Bug**: Claude fixed the event-level scorer (fighter loss = all bets lose) but left the bout-level scorer untouched. Event totals were correct but bout-level data showed wrong tables on the website.
- **Root cause**: No documentation that two scorers exist. Claude searched for the scoring bug, found ONE instance, fixed it, and declared done without checking if the same logic existed elsewhere.
- **Fix**: ALWAYS search for ALL instances of scoring logic before declaring a fix complete. After fixing any scoring rule, grep for the pattern in the ENTIRE file — there may be a second implementation.
- **Applies when**: ANY scoring/P&L fix in the UFC algorithm. Check both event-level AND bout-level scoring sections.

### BACKTEST DESTROYED 38 EVENTS OF PROP ODDS — 2026-03-23
- **Context**: UFC profit registry, prop odds cache, backtest re-run
- **Bug**: Claude ran a 71-event backtest that re-scraped prop odds from BestFightOdds. The cache had `__NO_PROPS__: True` for 38 events because the scraper ran too early (before odds were published). The backtest overwrote the registry with null prop data for those 38 events, destroying method_odds, method_pnl, round_odds, etc. that had been accumulated across prior sessions.
- **Root cause**: The registry accumulates data over time — each session adds odds that weren't available before. A full backtest re-run replaces ALL data with whatever the cache currently has, which may be LESS than what was already stored. No pre-write comparison was done.
- **Fix**: CLAUDE.md rules 10-11: Always backup registry before any backtest. After run, compare field-by-field. If any event lost data (value → null), ABORT and restore backup. Prop odds are irreplaceable once events pass — never trust a fresh scrape over cached historical data.
- **Severity**: CATASTROPHIC — weeks of accumulated prop odds data destroyed in one command. Required manual restoration from git history.
- **Applies when**: ANY backtest re-run, ANY registry overwrite, ANY operation that touches the profit registry

### [BACKTEST_WIPED_PROP_ODDS] — 2026-03-24
- **Context**: Re-running 71-event backtest with UFC_CACHE_ONLY=1
- **Bug**: Backtest regenerated registry from scratch. Prop odds cache had __NO_PROPS__: True for 38 events, so 38 events lost ALL method/round/combo data.
- **Root cause**: The prop odds cache was stale/incomplete. CACHE_ONLY mode uses whatever's in the cache — if cache says no props, the backtest records no prop bets.
- **Fix**: NEVER re-run full backtest without first verifying prop odds cache coverage. Better approach: re-score existing registry data in place (Option A in handoff).
- **Applies when**: ANY time someone wants to re-run the backtest. Check cache first. Backup registry first.

### [ALGO_STATS_OVERWRITTEN] — 2026-03-24
- **Context**: Backtest writes to algorithm_stats.json
- **Bug**: Backtest overwrote curated display stats (355W-142L, v11.11.0) with raw backtest pool numbers (360W-150L, v10.71)
- **Root cause**: The backtest's update_algorithm_stats() reads APP_VERSION from version.js and writes ML totals from the full fight pool, not just the picks that were bet on.
- **Fix**: NEVER let backtest overwrite algorithm_stats.json. Either backup before, or modify the backtest to not touch it.
- **Applies when**: ANY backtest run. The algo stats file is curated — backtest should not touch it.

### YAHOO_FINANCE_CRUMB_AUTH — 2026-03-24
- **Context**: Nestwise stock analysis (yahoo-stock.ts, deep-dive API)
- **Bug**: All Yahoo Finance quoteSummary data returned null — P/E, margins, EPS, market cap all missing. Every stock showed "FAILS — UNPROFITABLE" with empty score bars.
- **Root cause**: Yahoo Finance added crumb authentication to v10/quoteSummary endpoints. Requests without a crumb+cookie pair return `{"error":{"code":"Unauthorized","description":"Invalid Crumb"}}`. The v8/chart API (for price data) still works without crumb.
- **Fix**: Created yahoo-crumb.ts that fetches cookies from fc.yahoo.com, then gets crumb from query2.finance.yahoo.com/v1/test/getcrumb. Cache crumb+cookie for 30 minutes. Pass both to quoteSummary requests.
- **Applies when**: Any Yahoo Finance v10 API call fails with "Invalid Crumb" or returns null fundamentals. Check crumb authentication first.

### DOMAIN FLIP-FLOP: Changed betting rules 4 times without reading spec — 2026-03-24
- **Context**: UFC prediction algorithm, R1 KO gating rules
- **Bug**: Claude changed its answer about round/combo bet gating 4 times in 5 messages, each time more wrong, ending with a proposal to change working code based on a fabricated rule
- **Root cause**: Claude grepped the 9000-line algorithm instead of reading the 1-page model spec. When corrected, it apologized performatively and guessed what the user wanted instead of re-reading the spec.
- **Flawed assumption**: "If the user corrects me, my new answer should match what I think they want" — NO, the answer should match the SPEC
- **Reasoning lesson**: When corrected on domain logic, READ THE SPEC FIRST, then restate your understanding and ask for confirmation. Never fabricate rules to please the user.
- **Applies when**: Any domain-specific question about betting rules, model behavior, scoring logic, or payout calculations

### IMPOSSIBLE STATS PRESENTED AS DEFINITIVE — 2026-03-24
- **Context**: UFC R2 KO combo analysis, registry data query
- **Bug**: Claude reported 0/72 R2 KO combo hit rate and called it "definitive answer" and "verdict." This is statistically impossible — the probability of 72 consecutive misses on round predictions is astronomically low, meaning the analysis query was wrong.
- **Root cause**: Claude didn't sanity-check extreme results. 0% over 72 samples should trigger "my query is probably wrong" not "definitive finding." Also doubled down when user said "very good" instead of flagging the implausibility.
- **Flawed assumption**: "If the data says 0/72, the data must be right" — NO, the query was wrong. 0/72 is the analysis bug signal, not a finding.
- **Reasoning lesson**: Extreme statistics (0%, 100%, all-win, all-loss over 20+ samples) are almost always bugs in the analysis, not real findings. Validate on 1-2 known events before concluding.
- **Applies when**: Any statistical analysis of sports prediction results, P/L computations, win rate calculations

### DUPLICATE DRAFT PICKS PRESENTED AS FINAL PREDICTION — 2026-03-24
- **Context**: NFL draft simulator, 10,000-run Monte Carlo simulation
- **Bug**: Draft board showed Spencer Fano at #5 AND #6, Avieon Terrell at #16 AND #17, Blake Miller at #24 AND #25, Cashius Howell at #28 AND #29. Claude presented this with confidence percentages and "key storylines" analysis.
- **Root cause**: (1) Simulation code doesn't remove drafted players from the pool (code bug). (2) Claude didn't scan the output for duplicates before presenting (quality check failure). (3) Claude analyzed the impossible output narratively instead of flagging the bug.
- **Flawed assumption**: "If the simulation produced it, it must be valid" — NO, simulations can have bugs. Output must be validated.
- **Reasoning lesson**: Before presenting ANY structured output (tables, lists, rankings), scan for physical impossibilities: duplicates, constraint violations, missing fields. A draft is a uniqueness constraint — each player appears exactly once.
- **Applies when**: Any simulation output, prediction tables, ranked lists, draft boards, tournament brackets — anywhere uniqueness or ordering constraints exist
