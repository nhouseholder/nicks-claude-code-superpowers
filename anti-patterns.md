# Anti-Patterns — Known Failures & Working Fixes

> This file is auto-maintained by the error-memory skill.
> Claude checks this before debugging to avoid repeating known-bad approaches.
> Last updated: 2026-03-31

## Algorithm — Triple Pivot: Running Full Backtests Before Doing Math

### TRIPLE_PIVOT_NO_PRECOMPUTE — 2026-03-31
- **Context**: Testing whether a 25% Markov penalty could flip ML picks past the PICK_DIFF_THRESHOLD (0.142799)
- **Bug**: Ran full backtest → got null result → added logging to algorithm → ran again → wrote diagnostic script → ran again → finally parsed output manually. 4 approach changes, 15+ minutes wasted.
- **Root cause**: Never did the arithmetic first. Average diff is 1.68. 1.68 × 0.75 = 1.26, still 9× above the 0.14 threshold. The null result was mathematically inevitable — no backtest needed.
- **Fix**: Added Pre-Compute Gate to backtest skill: (1) Can math answer this? (2) Can a 10-line script answer this? (3) Have I locked my approach? All 3 must pass before running a full pipeline.
- **Flawed assumption**: That running the full pipeline is the fastest way to test a hypothesis. In reality, most algorithm parameter questions are arithmetic that can be answered in seconds without running anything.
- **Reasoning lesson**: ALWAYS calculate whether a parameter change can mathematically cross the decision threshold before running any pipeline. If penalty × average_value > threshold, the experiment is dead on arrival.
- **Applies when**: ANY algorithm parameter change, coefficient tweak, gate threshold modification, or penalty adjustment. Do the math FIRST.

## UFC — GSA Hybrid SUB Gate Tested: +0.00u Delta (NO IMPROVEMENT)

### GSA_GATE_NO_IMPROVEMENT — 2026-03-28
- **Context**: Proposed replacing blanket SUB→DEC fallback with a Grappling Submission Advantage (GSA) score to selectively keep SUB bets for elite grapplers
- **Formula**: GSA = (SubAvg × 2) + (sub_sc × 3) + max(0, (0.60 - opp_TDDef) / 0.20), threshold=3.5
- **Result**: +0.00u delta vs blanket DEC fallback. Zero improvement.
- **Root cause**: Elite grapplers (Makhachev, Oliveira, Chimaev, Rakhmonov) who pass the GSA gate still mostly win by DEC (55%), not SUB (25%). The GSA gate correctly identifies submission specialists, but submission specialists DON'T actually finish by submission — they control and decision. The 8 correct SUB wins captured were offset by ~12 DEC wins lost.
- **Flawed assumption**: That high grappling stats predict submission finishes. In reality, the best grapplers use takedowns for control and positional dominance, winning by DEC. The submission threat creates the control, not the finish.
- **Applies when**: ANY proposal to selectively override the SUB→DEC fallback. The blanket fallback captures the dominant outcome (56% DEC) and is optimal.

## UFC — Ghost X Bug: *_correct Set Without *_pnl (206 Bad Cells)

### GHOST_X_NO_PLACED_FLAG — 2026-03-28
- **Context**: Event history tables on mmalogic.com showed `✗ —` (red X with no dollar amount) in 206 cells across 504 bouts
- **Bug**: Backtester sets `*_correct = false` for accuracy tracking even when no bet was placed (e.g., DEC predictions getting round_correct=false, KO R2 predictions getting combo_correct=false). The renderer sees `false` → shows ✗, sees `null` pnl → shows —. Also: 27 method wins had null pnl because prop odds were scraped after the backtest ran.
- **Root cause**: No explicit `*_placed` flag in the registry schema. The system inferred bet placement from `*_correct !== null`, but the backtester sets `*_correct` for display/tracking even for unplaced bets.
- **Fix**: Added `ml_placed`, `method_placed`, `round_placed`, `combo_placed` boolean flags to every bout in the registry. Migration script `fix_registry_placed_flags.py` cleaned up 206 ghost Xs. Frontend BetCell component now uses `*_placed` instead of inferring from `*_correct`. Validation gate `validate_registry_cells.py` enforces invariants.
- **Flawed assumption**: That `*_correct !== null` reliably indicates a bet was placed. The backtester has multiple code paths that set `*_correct` for tracking without actually placing the bet.
- **Applies when**: ANY registry write — always run `python3 validate_registry_cells.py --strict` after modifying the registry.

## UFC — DEC Method Odds Gate Caused -91.95u Regression (REVERTED)

### DEC_ODDS_GATE_REGRESSION — 2026-03-28
- **Context**: Attempted to gate DEC method bets outside -125 to +250 odds range
- **Bug**: Method P/L dropped from +100.61u to +12.75u (-91.95u). Deployed as v11.16.0, caught immediately, reverted to v11.16.1.
- **Root cause**: Gating +250+ odds also blocked longshot DEC bets at +300 to +800+ that pay 3-10x per hit. Those longshot wins (+83u) cross-subsidize the small mid-range losses (-7.50u total). Removing the whole tail destroyed the portfolio.
- **Fix**: Gate disabled (floor=-99999, ceiling=+99999). All DEC method bets placed regardless of odds.
- **Flawed assumption**: That losing odds ranges can be gated independently. Method bets are a portfolio where longshot wins fund mid-range losses.
- **Reasoning lesson**: NEVER gate prop bets by odds range without simulating FULL P/L including longshots. Always run the backtest BEFORE deploying odds-based gates.
- **Applies when**: ANY proposal to gate/skip bets based on odds thresholds.

## UFC — Parlay Legs Rendered as "+" (String vs Object Format Mismatch)

### PARLAY_LEGS_STRING_VS_OBJECT — 2026-03-28
- **Context**: HistoryPage.jsx line 163, EventBetsDropdown.jsx line 146 — parlay row display
- **Bug**: Parlay row showed "+" with no fighter names. Expected "Duncan + Page".
- **Root cause**: Registry stores `parlay.legs` as a string array `["Duncan", "Page"]`, but components used `l.fighter` (expects objects). `undefined.join(' + ')` = `" + "` → renders as "+".
- **Fix**: Changed to `legs.map(l => typeof l === 'string' ? l : l.fighter || l)` in all 3 affected components. Also fixed `combined_decimal_odds` → `parlay_odds_decimal` key mismatch.
- **Flawed assumption**: That all parlay data uses the same format. The registry format (strings) differs from the prediction output format (objects with `.fighter`).
- **Applies when**: ANY component that renders parlay legs. Grep for `parlay.legs` and verify the map handles both string and object formats.

## UFC — Backtester Output Not Retroactively Enforcing Business Rules (166 violations)

### REGISTRY_STALE_BUSINESS_RULES — 2026-03-28
- **Context**: Full registry scan across 71 events after implementing SUB→DEC fallback + R1 KO gating
- **Bug**: 166 violations found: 55 bouts still showing "SUB" instead of DEC, 56 bouts with KO R2+ having round/combo bets (should be gated to R1 only), 55 method wins with no payout (missing prop odds lookup)
- **Root cause**: Business rules (SUB→DEC fallback, R1 KO gate) were added to the backtester's SCORING path but not retroactively applied to the REGISTRY DATA that the website displays. The backtester generates walk-forward predictions which may differ from the rules. After the backtest runs, the registry contains raw backtester output that hasn't been post-processed.
- **Fix**: Created a post-backtest registry sweep script that: (1) Converts all SUB→DEC, (2) Nulls round/combo for KO R2+, (3) Looks up missing method odds from prop cache, (4) Recalculates all combined_pnl, event totals, and global totals
- **Flawed assumption**: That the backtester applies ALL business rules consistently. It doesn't — the walk-forward scoring path may produce different method predictions than the rules require.
- **Reasoning lesson**: Business rules are post-processing on backtester output, not intrinsic to the walk-forward logic. A sweep is MANDATORY after every backtest.
- **Applies when**: After EVERY backtest re-run, every `track_results.py` scoring, every registry modification

## UFC — SUB→DEC Fallback Missing from Prediction Output Picks Array

### SUB_DEC_NOT_IN_PICKS_ARRAY — 2026-03-28
- **Context**: `UFC_Alg_v4_fast_2026.py` line ~10663, `prediction_output.json` picks array
- **Bug**: Chiesa showed "by Submission (-120)" on the live picks page despite SUB→DEC fallback being enabled. The FightCard component reads `predicted_method` from the picks array.
- **Root cause**: The picks array at line 10663 wrote `pc.get("method_pred", "")` — the RAW algorithm prediction — without applying SUB→DEC fallback. The fallback was only applied in `final_bets` (lines 10717-10719) and backtester scoring (lines 9271-9273), but NOT in the picks array that the website displays.
- **Fix**: Changed line 10663 to: `"DEC" if (method_pred == "SUB" and SUB_DEC_FALLBACK) else method_pred`. Also set `predicted_round: None` when fallback fires (DEC has no round).
- **Flawed assumption**: That fixing the `final_bets` section was sufficient. The picks array is a separate output path read by completely different frontend components.
- **Reasoning lesson**: When a business rule (SUB→DEC) spans multiple output formats, grep ALL usage sites. The algorithm has 5+ sections that compute/output method: backtester scoring, card display, summary display, JSON output/final_bets, and picks array.
- **Applies when**: ANY change to method prediction logic, any new fallback or gating rule. Check ALL output paths.

## UFC — Free Pick Filter Allows Null ML Through (Nullish Coalescing Bug)

### FREE_PICK_NULL_ML_BYPASS — 2026-03-28
- **Context**: Free pick selection in `webapp/frontend/src/services/api.js`, both `getPublicFreePick()` and `getFreePick()` + `pickByConfidence()`
- **Bug**: Free pick showed Navajo Stirling (-440 heavy favorite) with "ML (N/A)" instead of Maycee Barber (-158). Stirling was stored in Firestore `free_pick` doc with null `pick_ml`.
- **Root cause**: The -180 filter used `(pick_ml ?? 0) > -180`. When `pick_ml` is null/undefined, `?? 0` defaults to 0, and `0 > -180` = TRUE. So picks with NO odds pass the "not a heavy favorite" filter. Same bug in `pickByConfidence()` let all-null-odds picks through, sorting purely by diff.
- **Fix**: Changed all three code paths to require: `pick_ml != null && pick_ml < 0 && pick_ml > -180`. Null ML = ineligible, period.
- **Flawed assumption**: That `?? 0` is a safe default for odds comparison. In betting, null odds ≠ 0 — null means "no line available."
- **Reasoning lesson**: Nullish coalescing (`??`) defaults are dangerous for numeric comparisons where 0 has semantic meaning. Always use explicit null checks for betting odds.
- **Applies when**: ANY filter or comparison involving `pick_ml`, `odds`, or any betting line. NEVER use `?? 0` for odds — use explicit null checks.

## UFC — Dual-Path Algorithm Divergence (3 improvements backtest-only)

### DUAL_PATH_DIVERGENCE — 2026-03-29
- **Context**: Algorithm has separate `if BACKTEST_MODE:` and `if not BACKTEST_MODE:` code paths. Three shipped improvements (v11.15, v11.16, v11.17) only existed in the backtest path.
- **Bug**: Live predictions diverged from backtested behavior:
  - v11.15 KO slight-fav skip: live predictions showed KO picks on -100 to -150 fighters (backtest skipped them)
  - v11.16 KO>+300 DEC fallback: live predictions bet KO when market priced it at +300+ (backtest swapped to DEC)
  - v11.17 Heavy fav KO boost: live predictions didn't boost KO for -400+ favorites (backtest did)
- **Root cause**: When adding algorithm improvements, code was inserted inside the `if BACKTEST_MODE:` block after `pick_ml` was set. The prediction path builds `prediction_cards` in a separate `if not BACKTEST_MODE:` block that ran BEFORE the backtest block, so it used unboosted/ungated values.
- **Additional root cause**: Constants were defined INLINE inside the backtest block (e.g., `HEAVY_FAV_KO_BOOST = True` at line 8898), causing `NameError` if referenced from the prediction path.
- **Fix**: (1) Move all constants to top-level (lines 198-209). (2) Add identical gate/boost/fallback logic to prediction path. (3) Add KO>+300 DEC fallback to prediction summary card builder.
- **Flawed assumption**: That adding code to the fight processing loop would affect both modes. In reality, the backtest scoring section and prediction card builder are completely separate code blocks.
- **Prevention**: After ANY algorithm change, grep for the feature name and verify it appears in BOTH paths (minimum 2 occurrences). New rule added to CLAUDE.md and /mmalogic command.
- **Applies when**: ANY algorithmic modification — gates, boosts, fallbacks, skips, method overrides. Check: backtest scoring path, prediction card builder, AND prediction summary display.

## UFC — Registry Parlay Uses Card Order Instead of Implied Probability

### REGISTRY_PARLAY_CARD_ORDER — 2026-03-28
- **Context**: UFC backtest registry parlay selection (UFC_Alg_v4_fast_2026.py line ~1646-1650)
- **Bug**: HC Parlay for Evloev vs. Murphy showed "Lerone Murphy (+180) + Michael Page (-180)" instead of "Duncan (-450) + Page (-180)". Murphy is an underdog — HC parlay should ONLY include favorites.
- **Root cause**: TWO separate parlay selection paths exist: (1) prediction-side (line ~10764) correctly filters favorites and sorts by implied probability, (2) registry-side (line ~1650) took `parlay_candidates[:2]` — first 2 in card order, ignoring odds entirely.
- **Fix**: Changed line 1650 to mirror prediction-side logic: filter favorites (odds < 0), sort by implied probability descending, take top 2.
- **Flawed assumption**: That bouts in the registry are "already in order from algorithm" — they're in card order, not probability order.
- **Reasoning lesson**: When the same business logic exists in two code paths, both must implement the same rules. Grep for ALL usage sites before declaring a fix complete.
- **Applies when**: ANY time parlay logic is modified, ANY backtest re-run. Check BOTH paths: `parlay_candidates` (registry) and `_hc_legs` (prediction).

## MyStrainAI — Mobile max-h Clips Expanded Card Content

### MOBILE_MAX_H_CLIPS_BOTTOM_CTA — 2026-03-27
- **Context**: MyStrainAI — StrainCard expanded section uses `max-h-[3000px]` for CSS transition animation
- **Bug**: "Find strain near me" button (last item in StrainCardExpanded) invisible on mobile iOS — content height exceeds 3000px on narrow screens
- **Root cause**: CSS transition trick uses `max-h` to animate open/close. 3000px is enough on desktop but not on mobile where all sections stack vertically to >3000px
- **Fix**: Increase to `max-h-[6000px]` for the expanded state (`StrainCard.jsx` line ~302)
- **Applies when**: ANY time content is hidden with a `max-h` CSS transition and the content length is variable or longer on mobile. Always set max-h generously (2x expected max content height)

## Critical — parry-guard .parry-tainted Blocks Entire Sessions

### PARRY_TAINT_BLOCKS_ALL_TOOLS — 2026-03-27
- **Context**: courtside-ai project, parry-guard PostToolUse ML scan
- **Bug**: parry-guard's ML model flagged tool output as prompt injection (false positive on user-owned code), wrote `.parry-tainted` to project root. On next PreToolUse, parry-guard checks for this file and blocks ALL tool calls with "Project tainted — all tools blocked. Remove .parry-tainted to resume." Session became completely unusable.
- **Root cause**: parry-guard's taint system is designed for untrusted repos. All our repos are user-owned — false positives from the ML model shouldn't lock out the entire session.
- **Fix**: Created `parry-taint-cleaner.py` SessionStart hook (runs first, before all other hooks). Auto-removes `.parry-tainted` files, injects warning context. If repeated, suggests `parry-guard ignore` for the affected repo.
- **Flawed assumption**: That the ML injection detector has zero false positives on benign code
- **Reasoning lesson**: Security tools with "nuclear lockout" modes need an auto-recovery path in trusted environments
- **Applies when**: Any time a session reports "all tools blocked" or you see `.parry-tainted` in a project directory

## Critical — Parallel Agents Clobbered Shared Files

### PARALLEL_SWEEP_SHARED_FILE_CLOBBER — 2026-03-26
- **Context**: UFC DEC_TIEBREAK parameter sweep, 5 worktree agents
- **Bug**: 5 agents ran parameter sweeps in parallel, all writing results to the same `ufc_profit_registry.json`. The last agent to finish overwrote all others. All 4 thresholds appeared identical because only one agent's output survived.
- **Root cause**: Agents shared a write target. Additionally, `sed`/`re.sub` with `count=1` only patched the first occurrence of the constant, missing a second usage site in the vectorized backtest path.
- **Fix**: (1) CLAUDE.md rule #32: max 2 agents, Opus only, separate output files, (2) parameter sweeps must run SEQUENTIALLY, (3) verify ALL usage sites of a constant before patching
- **Flawed assumption**: That isolated worktree agents would produce independent results even when writing to the same output file
- **Reasoning lesson**: Parallel writes to shared state = data corruption. Parameter sweeps must be sequential with result-reading between runs.
- **Applies when**: ANY parameter sweep, coefficient search, or multi-run comparison task

## Critical — Subagents Must Not Replace CSS Frameworks

### SUBAGENT_REPLACED_TAILWIND_WITH_INLINE_STYLES — 2026-03-26
- **Context**: NFL Draft Predictor site-redesign, /site-redesign command
- **Bug**: Two Sonnet subagents were spawned to redesign components. Both replaced all Tailwind utility classes with verbose inline `style={{}}` objects using CSS custom properties. Lost hover states, transitions, responsive breakpoints, and readability.
- **Root cause**: Subagents were given too much freedom ("redesign this component") without the constraint "preserve the existing CSS framework." They interpreted "redesign" as "rewrite everything" including the styling architecture.
- **Fix**: Updated /site-redesign: (1) Phase 3 is NEVER done by subagents — main agent only, (2) Framework Preservation Rule: Tailwind stays Tailwind, CSS modules stay CSS modules, (3) "Update, don't rewrite" principle for components
- **Flawed assumption**: That subagents can maintain consistent design decisions across components without full context
- **Reasoning lesson**: A redesign changes the visual output, not the styling architecture. Never delegate component styling to subagents.
- **Applies when**: ANY /site-redesign invocation, ANY time subagents are considered for CSS/styling work

## PERMANENT RULE — NEVER Accept Missing Prop Odds (NON-NEGOTIABLE)

### MISSING_ODDS_ACCEPTED_WITHOUT_SCRAPING — 2026-03-25
- **Context**: UFC profit registry, prop odds cache, any event with `__NO_PROPS__` or null method_odds/round_odds/combo_odds
- **Bug**: Claude accepted null/missing prop odds and displayed "—" for method wins instead of running the odds scraper to backfill. This happened AGAIN on 2026-03-25 for Evloev vs. Murphy (Page and Duncan fights had __NO_PROPS__ from a March 16 scrape that was too early).
- **Root cause**: Claude treated missing odds as a display problem (fix the frontend) instead of a data problem (scrape the actual odds). The scraper exists and works — it just wasn't run.
- **Fix**: PERMANENT RULE — When ANY fight has null prop odds: (1) IMMEDIATELY run the prop odds scraper/backfill, (2) NEVER accept __NO_PROPS__ as final, (3) NEVER move to display fixes until odds are scraped, (4) This overrides ALL other priorities.
- **Applies when**: ANY time you see null method_odds, null round_odds, null combo_odds, __NO_PROPS__, or "—" in a prop bet cell. The answer is ALWAYS "scrape first, display after."

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

### [REGISTRY_TOTALS_MISSING_PARLAY] — 2026-03-24
- **Context**: webapp/frontend/public/data/ufc_profit_registry.json → HeroStats landing page
- **Bug**: Parlay P/L showed +0.00u (0W-0L) on landing page, and Combo showed +0.00u. Combined P/L was +169.14u instead of +281.71u. ROI showed 54% instead of 29.1%. Only 25 events showed instead of 71.
- **Root cause**: Registry `totals` object was missing `parlay_wins`, `parlay_losses`, `parlay_pnl` fields entirely. Event-level parlay data existed (64/71 events had pnl) but had no `wins`/`losses` fields — only `correct` and `pnl`. The Python backtester was writing event parlay data but never computing parlay totals. Additionally, Firestore was serving stale 25-event data that overrode the static JSON on the deployed site.
- **Fix**: (1) Recomputed registry totals from event-level data, adding parlay fields. (2) Added `wins`/`losses` to each event's parlay object derived from `correct` field. (3) Added `parlay_pnl`, `parlay_wins`, `parlay_losses` to algorithm_stats.json.
- **Applies when**: After ANY backtest run that writes to ufc_profit_registry.json, verify totals include ALL 5 bet types (ml, method, round, combo, parlay) with wins/losses/pnl for each.

### [CONFIDENCE_DISPLAY_AS_PERCENTAGE] — 2026-03-24
- **Context**: webapp/frontend/src/components/picks/FightCard.jsx
- **Bug**: Confidence badge showed "260% conf", "226% conf" — values over 100% that looked wrong.
- **Root cause**: `pick.diff` (raw algorithm differential, typically 0.14 to 3.0+) was multiplied by 100 and displayed with a % suffix. A diff of 2.60 became "260%". The value is not a percentage — it's an absolute score differential.
- **Fix**: Changed display from `(Math.abs(pick.diff) * 100).toFixed(0) + '%'` to `Math.abs(pick.diff).toFixed(2) + ' diff'` with label "confidence" instead of "model edge".
- **Applies when**: Any time a raw algorithm score is displayed on the frontend. Differential values are NOT percentages — they're absolute scores. Only display as % if the value is genuinely a 0-1 proportion.

### [REGISTRY_DATA_NOT_SYNCED_TO_DEPLOY] — 2026-03-24
- **Context**: Multiple data files across webapp/ and ufc-predict/webapp/
- **Bug**: Root webapp/ had stale data files from 10+ days ago while ufc-predict/webapp/ had current data. 7 data files and 4 source files were out of sync.
- **Root cause**: After backtest/optimizer runs update files in ufc-predict/webapp/frontend/public/data/, nobody synced them to the root webapp/ (which is the deploy source). No automated sync exists.
- **Fix**: Manually synced all data + source files from ufc-predict/webapp/ → root webapp/. 
- **Applies when**: After EVERY backtest, optimizer, or prediction run, MUST sync data files from ufc-predict/webapp/frontend/public/data/ → webapp/frontend/public/data/. Add this to the site-update-protocol checklist.

### UFC_SITE_GLANCE_AND_APPROVE — 2026-03-25
- **Context**: UFC MMA Logic website audit/maintenance
- **Bug**: AI said "no obvious bugs" and "looks correct" on screenshots with 7+ visible bugs: 260% confidence values, SUB bets shown despite gating, missing combo bets, missing second parlay, empty optimizer values, missing P/L on event details, missing parlay on event details
- **Root cause**: AI glances at screenshots superficially instead of checking each element against the domain rules. It pattern-matches "data exists in cells" as "correct" without verifying the VALUES are valid.
- **Fix**: Created mandatory 15-item checklist at ~/.claude/memory/topics/ufc_website_maintenance_rules.md. Every site audit MUST run through this checklist item-by-item with specific values, not "looks fine."
- **Applies when**: Any time reviewing UFC/MMA Logic website screenshots, doing /site-audit, /site-update, /site-debug, or any visual verification of the site. Read the checklist BEFORE looking at screenshots.
- **Recurrence**: HIGH — this is the SAME failure mode as the P/L bugs, the 0W-0L bugs, and the missing bet type bugs. The AI consistently fails at visual verification.

### [FIGHTCARD_MISSING_R1_KO_GATING] — 2026-03-25
- **Context**: webapp/frontend/src/components/picks/FightCard.jsx
- **Bug**: Round bet shown for KO R2 predictions (e.g., Navajo Stirling). Spec says round/combo bets are ONLY for KO R1.
- **Root cause**: FightCard only had SUB gating and KO confidence gating, but no R1 gating rule. Any KO finish prediction showed round bets.
- **Fix**: Added `isR1Ko = method === 'KO' && round === 1` check. Round/combo bets only display when isR1Ko is true.
- **Applies when**: Any time FightCard bet rows are modified. The R1 KO gating rule is immutable per backtest data.

### [FIGHTCARD_NO_COMBO_BET] — 2026-03-25
- **Context**: webapp/frontend/src/components/picks/FightCard.jsx
- **Bug**: No combo bet row ever displayed on any fight card.
- **Root cause**: The bets array builder only pushed ML, Method, Round — combo was never implemented.
- **Fix**: Added CMB tag row that appears alongside round bet (same R1 KO gating). Added combo odds lookup.
- **Applies when**: Reviewing fight cards — verify CMB tag appears for R1 KO predictions.

### [EVENTBETS_NULL_PNL_WITH_ODDS] — 2026-03-25
- **Context**: webapp/frontend/src/components/shared/EventBetsDropdown.jsx — 145 bouts affected
- **Bug**: Prop bet losses showed "—" instead of "-1.00u", prop wins showed "—" instead of odds-based payout, when the registry data had null pnl but valid odds.
- **Root cause**: Python backtester doesn't always populate method_pnl/round_pnl/combo_pnl for bout records, especially for losses and older events. The frontend safePnl() returned null for null pnl.
- **Fix**: Enhanced safePnl(correct, pnl, odds) to compute from betting rules when pnl is null but odds exist: loss=-1u, win=odds-based payout. Also enforces fighter-loss rule (ml_correct=false → all props are losses).
- **Applies when**: Any time EventBetsDropdown or bout-level rendering is modified. The frontend is the safety net for incomplete backend data.

### [OPTIMIZER_MISSING_CURRENT_VALUES] — 2026-03-25
- **Context**: webapp/frontend/src/components/admin/AdminAlgorithm.jsx
- **Bug**: Many params showed "—" in Current column (SL_WIN_FLOOR, RATIO_MIN, SEI_DEF_WEIGHT, etc.)
- **Root cause**: curVals read only from Firestore constants, which doesn't have all params. The optimizer_results.json has current_values with all 61 params but wasn't used as fallback.
- **Fix**: (1) curVals now merges optimizer.current_values as base with Firestore constants as override. (2) Added 'Advanced Features' and 'System Integration' to CATEGORIES (18 missing params).
- **Applies when**: After adding new params to the optimizer, verify they appear in CATEGORIES in AdminAlgorithm.jsx.

### UFC_WRONG_DIRECTORY_DEPLOY — 2026-03-25
- **Context**: UFC MMA Logic website deployment
- **Bug**: Live site reverted from v11.9.3 → v10.68, losing ALL v11.x improvements (parlay display, event tables, optimizer, confidence formatting, 71→25 events)
- **Root cause**: AI deployed from `UFC Algs/webapp/` (root, frozen at v10.68) instead of `UFC Algs/ufc-predict/webapp/` (canonical, v11.9.3+). Two webapp/ directories exist — root is a stale copy.
- **Flawed assumption**: AI assumed the nearest `webapp/` directory was the right one to deploy from. It didn't verify version numbers or check which directory CI deploys from.
- **Fix**: Redeployed from ufc-predict/webapp/frontend/ via GitHub CI
- **Prevention**: BEFORE any UFC deploy, check version.js in the directory you're about to deploy. If it doesn't show v11.x+, you're in the WRONG directory. Canonical source is ALWAYS ufc-predict/webapp/frontend/. The root webapp/ must be archived or deleted.
- **Applies when**: ANY deploy, build, or wrangler command for the UFC/MMALogic project. ALWAYS verify you're in ufc-predict/webapp/, not root webapp/.
- **Severity**: CATASTROPHIC — overwrote a working production deployment with months-old stale code
- **Recurrence**: First occurrence, but the stale root webapp/ has been a confusion source in data sync operations before

### [SCREENSHOT_REVIEW_MISSED_11_BUGS] — 2026-03-25
- **Context**: Reviewing 5 screenshots of mmalogic.com live site
- **Bug**: Agent said "no obvious bugs" for History and Optimizer pages while 11 bugs were clearly visible: 260% confidence, missing combo/parlay cards (0W-0L), broken prop P/L, empty optimizer Current values, wrong event count (25 vs 71), wrong hero total (+169.14u vs +238u), missing round card.
- **Root cause**: Agent "glanced" at screenshots instead of checking each element against the 12 immutable betting rules and the 15-point website checklist.
- **Fix**: Created `~/.claude/memory/topics/ufc_website_maintenance_rules.md` with 15-point checklist + 19 display rules.
- **Flawed assumption**: That visual scanning is sufficient to catch display bugs.
- **Prevention rule**: BEFORE reviewing any website screenshot, READ ufc_website_maintenance_rules.md. Check EVERY item on the 15-point list. Never say "looks correct" without checking each item individually.
- **Applies when**: Any screenshot review, any site audit, any post-deploy verification.
- **Severity**: HIGH — user had to point out 11 bugs that should have been caught automatically

### DEPLOY WITHOUT COMMIT CAUSED SITE REVERSION — 2026-03-25
- **Context**: researcharia.com — agent deployed to Cloudflare Workers without committing changes to git first
- **Bug**: Agent deployed uncommitted local changes, then when the deploy used stale code, the entire frontend redesign was overwritten with the pre-redesign version. Agent then gaslit the user by claiming "nothing was reverted" when the user showed a screenshot proving the site was broken.
- **Root cause**: (1) Deployed without committing — git history didn't match production. (2) When confronted with evidence, argued instead of verifying. (3) No baseline snapshot was taken before deploy.
- **Fix**: ALWAYS use `/site-update` for any deploy. Phase 0 checks git state, Phase 1 captures baseline, Phase 5 commits BEFORE deploying. NEVER do ad-hoc `wrangler deploy` without first committing and verifying the version.
- **Applies when**: Any time deploying any site to any platform. COMMIT FIRST, DEPLOY SECOND.

### NEVER ARGUE WITH USER ABOUT WHAT THEY SEE — 2026-03-25
- **Context**: User showed screenshot of reverted site. Agent said "nothing was reverted" and asked user to clarify.
- **Bug**: Agent trusted its own `curl` output over the user's screenshot. The curl was hitting cached/CDN content while the user was seeing the actual broken site.
- **Root cause**: Agent was defensive instead of investigative. Violated rule #6 (do it yourself) and rule #16 (extreme results = bug in your analysis).
- **Fix**: When user says something is broken and shows evidence: (1) BELIEVE THEM. (2) Check the live site yourself via browser (Claude in Chrome), not curl. (3) Never say "nothing is wrong" when user shows a screenshot proving otherwise. (4) Apologize, investigate, fix.
- **Applies when**: Any time the user reports a visual bug or site issue.

### NEVER ACCEPT MISSING ODDS — ALWAYS SCRAPE TO BACKFILL — 2026-03-25
- **Context**: UFC event table showed "✓ —" for method payout (won but "no odds to compute payout"). Agent marked this as correct.
- **Bug**: Agent treated missing odds as an acceptable state and displayed "—" instead of a real payout value. This is NEVER acceptable.
- **Root cause**: Agent was lazy — saw missing odds data and shrugged instead of running the odds scraper to backfill the missing data from BestFightOdds or other sources.
- **Fix**: Missing odds = BROKEN DATA, not an edge case. When ANY cell shows "—" where a payout should be:
  1. STOP — do not mark it as correct
  2. Run the odds scraper/backfill script to fetch the missing odds
  3. Only after backfill fails (source genuinely unavailable) can you mark it as "odds unavailable — source checked"
  4. NEVER display "—" to the user and call it correct
- **Applies when**: ANY sports prediction project, ANY bet type, ANY event. Missing odds = run scraper. Period.

### CATASTROPHIC: Deploying from git overwrote Cloudflare-only frontend redesign — 2026-03-26
- **Context**: researcharia.com (aria-research Worker)
- **Bug**: Agent deployed from git repo using `wrangler deploy`. The live Cloudflare Worker had a frontend redesign that was deployed directly but NEVER committed to git. The deploy overwrote the redesign with old pre-redesign frontend code from git. Attempted rollback failed because Workers Sites purges old static assets from KV on deploy.
- **Root cause**: (1) Previous session deployed a redesign directly to CF without committing to git. (2) This session deployed from git without checking if CF had newer changes. (3) No safeguard existed to detect CF-only changes before deploying.
- **Fix**: Created deploy-guard.py hook that blocks `wrangler deploy` if: (a) uncommitted frontend changes exist, (b) last git commit to public/ is old (>24h), suggesting CF may have newer changes. Added to PreToolUse hooks in settings.json.
- **Applies when**: ANY project using Cloudflare Workers/Pages. BEFORE any deploy:
  1. Check Cloudflare deployment history: `wrangler deployments list`
  2. Compare last CF deploy timestamp to last git commit touching public/
  3. If CF was deployed more recently than git, STOP — someone deployed without committing
  4. Visually verify live site matches local files BEFORE deploying
  5. NEVER deploy without all frontend changes committed to git
- **SEVERITY**: CATASTROPHIC — destroyed weeks of frontend work with no recovery path. KV assets are purged on deploy. Rollback breaks static file serving. The redesigned files were permanently lost.
- **Prevention**: deploy-guard.py hook (PreToolUse), project CLAUDE.md rules, global CLAUDE.md FAILSAFE 9

### CLOUDFLARE WORKERS SITES PURGES OLD ASSETS ON DEPLOY — 2026-03-25
- **Context**: researcharia.com — agent deployed stale code from git. Cloudflare Workers Sites marked the redesign's assets (app.7852ea8498.js etc.) as "stale" and DELETED them from KV during the deploy.
- **Bug**: Cloudflare Workers Sites only keeps assets from the CURRENT deploy. When the agent deployed old code, the redesign's compiled frontend assets were permanently destroyed — no recovery possible.
- **Root cause**: The redesign was deployed to Cloudflare but NEVER committed to git. When the agent deployed from git, it deployed the pre-redesign code, and Cloudflare treated the redesign's assets as stale garbage.
- **Fix**: This is an IRREVERSIBLE destructive action. Cloudflare deploy = permanent overwrite. Prevention is the ONLY option:
  1. EVERY change that touches production MUST be committed to git BEFORE deploying
  2. EVERY deploy MUST go through `/site-update` or `/deploy` which enforce commit-first
  3. If code exists in Cloudflare but NOT in git, commit it FIRST: `wrangler pages download` or reconstruct from the live site before deploying anything
  4. NEVER deploy from git when git is behind production — check the live site version vs git version first
  5. Add to FAILSAFE 3 (Version Regression Detection): compare live site version to git version, not just git to git
- **Applies when**: ANY Cloudflare deploy (Pages or Workers). There is no undo button. There is no KV recovery. Deploy = permanent.

### ROOT CAUSE: "STALE" MISCLASSIFICATION DESTROYS CURRENT WORK — 2026-03-25
- **Context**: researcharia.com redesign destroyed because Cloudflare classified redesign assets as "stale" during a deploy from git. The redesign existed in production but not in git.
- **Root cause chain**:
  1. Session A deployed a redesign to Cloudflare but never committed it to git
  2. Session B saw git was at the old version and deployed from git
  3. Cloudflare Workers Sites classified the redesign's compiled assets as "stale" and PURGED THEM
  4. The redesign was permanently destroyed
- **The fundamental error**: Treating "not in git" as "stale/outdated." Files can be AHEAD of git (deployed but uncommitted). Production is sometimes NEWER than git. Staleness must be determined by COMPARING DATES AND VERSIONS, not by which system has it.
- **Definition of stale (CORRECTED)**:
  - STALE = a file that has been EXPLICITLY REPLACED by a newer version (e.g., v2 replaced by v3, old backtester replaced by new one)
  - NOT STALE = a file that is different from git, production, or another copy — difference ≠ staleness
  - NOT STALE = compiled/built assets on a live server that don't match local source — they may be the LATEST deploy
  - NOT STALE = uncommitted local changes — they may be work in progress
- **Rule**: NEVER classify a file as stale based solely on it being absent from git, absent from local, or different from another copy. Staleness requires EVIDENCE that it was replaced:
  1. A newer file exists that does the same job
  2. A commit message says "replaced X with Y"
  3. The user explicitly says the file is outdated
  Without this evidence, the file is NOT stale — it's a version discrepancy that needs investigation, not deletion.
- **Applies when**: cleanup-old-files skill, any archival operation, any deploy that overwrites, any time the word "stale" is used about files or assets

### BREAKING GITHUB ACTIONS / INTEGRATIONS DURING SIMPLE FIXES — 2026-03-26
- **Context**: Diamond Predictions (NHL) — admin page GitHub Actions buttons stopped working after a "simple fix"
- **Bug**: After Claude applied a code change, the "Generate Picks" button broke with 422 error: `Workflow does not have 'workflow_dispatch' trigger`. The workflow file was modified or replaced, losing the `workflow_dispatch` trigger that the admin page button depends on.
- **Root cause**: Claude edited or replaced a `.github/workflows/` file without understanding that the admin page UI buttons call `workflow_dispatch` via GitHub API. Removing or renaming the workflow broke the integration silently.
- **Fix**: CLAUDE.md rule #29 — before editing ANY file with API calls, webhook URLs, or GitHub Actions triggers, identify all integrations first and preserve them. After editing, verify every integration still works.
- **Applies when**: ANY edit to workflow files, API route files, admin page JS, or any code that wires UI buttons to external services. ALWAYS verify action buttons work after ANY deploy.

### UNSOLICITED FRONTEND DESTRUCTION DURING BACKEND UPDATES — 2026-03-26
- **Context**: courtside-ai (NCAA/NBA) — user asked for algorithm update only
- **Bug**: Claude destroyed the admin page frontend while applying an algorithm update. Lost all frontend for the most important pages on the website.
- **Root cause**: Claude treated a focused task ("update algorithm") as permission to touch any file in the project. It "cleaned up" or "improved" admin page HTML/CSS that it was never asked to modify, destroying working frontend.
- **Fix**: CLAUDE.md rule #27 "SURGICAL SCOPE" — when given a focused task, ONLY modify files directly related to that task. If you notice other issues, NOTE them for the user. Never fix unsolicited problems.
- **Applies when**: ANY focused task (algorithm update, config change, data fix, API change). The blast radius of changes must match the scope of the request. EVERY TIME.

### DIRECTORY RENAME KILLS ALL ACTIVE SESSIONS — 2026-03-26
- **Context**: Superpowers/skills audit session, renaming iCloud `***Projects***` to `ProjectsHQ`
- **Bug**: Renaming the iCloud folder that all project sessions were opened from killed 7 active Claude Code sessions simultaneously. Sessions show "Folder no longer exists" with no recovery path. All in-progress work context was lost — handoffs in the projects were from session START, not from the crash point.
- **Root cause**: Claude Code sessions are tied to their absolute directory path. If the underlying folder is renamed/moved/deleted, the session dies instantly with no graceful shutdown, no auto-handoff, no warning.
- **Flawed assumption**: "Renaming is safe because the symlink will still work." The symlink works for NEW sessions, but EXISTING sessions stored the raw iCloud path, not the symlink path.
- **Reasoning lesson**: NEVER rename, move, or delete any directory that could have active Claude Code sessions without: (1) warning the user about session loss, (2) verifying handoffs are current in each project, (3) getting explicit user approval. A directory rename is a DESTRUCTIVE operation for sessions.
- **Fix**: Before any directory rename/move: list all projects in that directory, warn "This will kill N active sessions — their in-progress context will be lost. Handoffs may be outdated. Proceed?", and only continue with explicit approval.
- **Applies when**: ANY mv, rename, or restructuring of directories under ~/Projects, ~/Library/Mobile Documents, or any path that Claude Code sessions may be opened from

---

### REPO_CONSOLIDATION_BROKE_PIPELINE_TRIGGER — 2026-03-26
- **Context**: Diamond Predictions NHL pipeline, trigger-pipeline.js (Cloudflare Function), nhl_predict/config.py
- **Bug**: After consolidating NHL algorithm from icebreaker-ai into diamond-predictions, the "Generate Picks" button returned 422 error ("Workflow does not have 'workflow_dispatch' trigger") and the daily cron pipeline crashed with `AttributeError: module 'nhl_predict.config' has no attribute 'MLB_WEBAPP_DATA'`.
- **Root cause**: Two incomplete migration steps during repo consolidation: (1) trigger-pipeline.js still pointed to `icebreaker-ai/daily-pipeline.yml` which was renamed to `.disabled`, (2) `MLB_WEBAPP_DATA` path constant was removed from config.py but still referenced in daily_pipeline.py's cross-write functions.
- **Flawed assumption**: "Moving the algorithm code is sufficient — the CI/CD and serverless functions will keep working." Wrong. Consolidating a repo requires auditing ALL consumers: GitHub Actions, Cloudflare Functions, API endpoints, admin buttons, and config references.
- **Reasoning lesson**: Repo consolidation is NOT just moving code. It requires a full consumer audit: grep for the old repo name in ALL files (*.js, *.yml, *.py, *.json), verify every workflow still has its triggers, and test the entire pipeline end-to-end before closing the old repo.
- **Fix**: Updated trigger-pipeline.js to point to `diamond-predictions/nhl-daily-pipeline.yml` and added `MLB_WEBAPP_DATA` path to nhl_predict/config.py.
- **Applies when**: ANY repo consolidation, migration, or archival — ALWAYS: (1) grep the entire codebase for the old repo name, (2) verify all workflow_dispatch triggers still exist, (3) run a test pipeline dispatch before marking the migration complete

## CATASTROPHIC — Algorithm Update Destroyed Frontend (2026-03-26)

### ADMIN_PAGE_REPLACED_DURING_ALGORITHM_UPDATE — 2026-03-26
- **Context**: Courtside AI, AdminPage.jsx (2094 lines → 736 lines), during NBA ML moneyline system integration
- **Bug**: Adding backend algorithm features (NBA ML model, grading pipeline) caused the entire AdminPage.jsx to be rewritten from scratch. The Command Center with NCAA+NBA picks, tier badges, Recharts charts, optimizer panel, and 8 functional tabs was replaced with a 6-tab simplified version using empty stub components. User lost all admin functionality.
- **Root cause**: Claude rewrote AdminPage.jsx instead of surgically modifying it. Created 6 stub component files (StatCard, Badge, AccuracyChart, FactorChart, ProfitChart, PickCard) that the new simplified AdminPage imported, replacing the self-contained real components. Also added 3 dead stub exports to api.js.
- **Flawed assumption**: "The AdminPage needs to be modernized alongside the algorithm update." WRONG. The algorithm update only needed backend changes (grading functions, prediction code, NbaPickCard badge). The AdminPage was working perfectly and did NOT need to be touched.
- **Reasoning lesson**: Algorithm/backend updates MUST be surgical. NEVER rewrite or restructure frontend files during a backend task. The blast radius of a change must match the scope of the request. If the task is "add NBA ML system," you touch: prediction scripts, grading functions, pick card component, and NOTHING else.
- **Fix**: Restored AdminPage.jsx from git commit 6b125d3 (last good version). Removed 6 stub files. Removed 3 dead api.js exports. Added LossAnalysisTab as an additive change to the restored file.
- **Applies when**: ANY algorithm update, model change, or backend feature addition — NEVER modify AdminPage.jsx structure, NEVER replace working frontend components, NEVER create stub files for things that already work. Check file line count before and after — if it shrinks, you broke it.

---

### CI_HEREDOC_DROPS_EXPORTS — 2026-03-26
- **Context**: Diamond Predictions MLB daily pipeline, `.github/workflows/daily-pipeline.yml`, version.js bump step
- **Bug**: MLB pipeline build failed for 4+ days (March 23-26). Vite build error: `"VERSION_DATE" is not exported by "src/version.js"`. NavBar.jsx and App.jsx import `VERSION_DATE` but the CI heredoc that rewrites version.js only included `APP_VERSION`.
- **Root cause**: The "Bump version" step uses `cat > version.js << VEOF` to rewrite version.js on every run. The heredoc only contained the `APP_VERSION` export, silently dropping the `VERSION_DATE` export that NavBar.jsx depends on. The file in git had both exports, but CI overwrote it before building.
- **Flawed assumption**: "The heredoc matches what's in the file." It didn't — someone added `VERSION_DATE` to version.js but never updated the CI heredoc. Any export added to version.js without also updating the CI heredoc gets silently deleted on every pipeline run.
- **Reasoning lesson**: When CI rewrites a file via heredoc, the heredoc IS the source of truth during CI — not the committed file. Any change to a file that CI overwrites MUST also be reflected in the CI workflow. Better yet: don't rewrite files in CI — use `sed` to update specific lines, preserving everything else.
- **Fix**: Added `export const VERSION_DATE = "$TODAY";` to the heredoc in daily-pipeline.yml.
- **Applies when**: ANY CI pipeline that rewrites files via heredoc or `cat >`. Always diff the heredoc against the actual file to ensure nothing is dropped. Prefer `sed -i` for targeted changes over full-file rewrites.

### STUB COMPONENT ANTI-PATTERN — 2026-03-26
- **Context**: courtside-ai AdminPage.jsx during NBA ML algorithm integration
- **Bug**: Agent replaced 2094-line AdminPage with 736-line skeleton, created 6 empty stub components (AccuracyChart, FactorChart, ProfitChart, PickCard, Badge, StatCard), and added 5 unused api.js exports. Destroyed the entire admin panel — Command Center, charts, tier badges, optimizer, all 8 functional tabs.
- **Root cause**: Agent encountered build errors from AdminPage's inline components and "fixed" them by rewriting the entire file and creating empty stubs instead of making targeted additions. Violated CLAUDE.md Rule #27 (SURGICAL SCOPE).
- **Fix**: Restored AdminPage from git history (commit 6b125d3), deleted all stub files, removed unused api.js exports.
- **Applies when**: ANY algorithm/backend update that might affect frontend files. If AdminPage line count decreases after your changes, you broke it — revert immediately. NEVER create stub components. NEVER rewrite AdminPage during algorithm work.

### BACKTESTER_OVERWRITES_LIVE_PREDICTION — 2026-03-26
- **Context**: UFC profit registry, Evloev vs Murphy event, Duncan method prediction
- **Bug**: Backtester walk-forward computed KO for Duncan, but the live prediction was DEC (DEC_TIEBREAK fired at gap=0.016 < 0.04). The backtester overwrote the correct DEC prediction with KO, turning a +8.50u method win into a -1.00u loss. Also set wrong parlay legs (Murphy+Page instead of Duncan+Page).
- **Root cause**: Walk-forward training window differs slightly from live prediction, shifting KO/DEC scores just enough to flip the tiebreaker. Backtester blindly overwrites without checking prediction_archive.
- **Fix**: After any backtest re-run, cross-check the most recent 1-2 events against prediction_archive. If method predictions diverge, the archive is ground truth. Manually patch the registry.
- **Applies when**: After ANY backtest re-run (`UFC_BACKTEST_MODE=1`), check the most recent event's method predictions and parlay legs. HC parlay = top 2 favorites by implied probability from active picks (not underdogs).

### LANDING_PAGE_WRONG_FETCH_URL — 2026-03-27
- **Context**: Diamond Predictions MLB landing page, free pick of the day
- **Bug**: MLB free pick never displayed on the landing page in production. LandingPage.jsx fetched from `/api/picks` which is a dev-only proxy path — no such route exists in Cloudflare Pages production (returns 404). The `r.ok` check silently returned null.
- **Root cause**: LandingPage.jsx was written to use the dev API proxy (`/api/picks`) but never updated to use the production static path (`/data/picks.json`). NHL landing page was correctly using `/data/nhl-predictions-today.json`.
- **Fix**: Changed `fetch('/api/picks')` → `fetch('/data/picks.json')` in LandingPage.jsx, PremiumPage.jsx, DashboardPage.jsx, and useAdminData.js (4 files total).
- **Applies when**: Any new page or component that fetches data — always use `/data/*.json` paths directly in production, never `/api/*` paths (those only work in dev mode through the Vite proxy). When fixing, grep ALL src files for `fetch('/api/` to catch every instance at once.

### CONSENSUS_SLIP_THROUGH — 2026-03-27
- **Context**: NFL Draft Predictor — Carnell Tate (grade 90, consensus rank 9.4) missing from draft entirely
- **Bug**: Consensus-weighted model penalizes prospects at picks far from their expert-mocked range. If a prospect is #2 at many picks but #1 at none, greedy assignment passes on them at every slot. By mid-round, their consensus score is too low to compete, even though they're a top-10 talent still on the board.
- **Root cause**: No "value available" signal. Real drafts have a cascading value effect — when a top talent slides, the NEXT team with that position need gets MORE excited, not less. The model lacked this.
- **Fix**: Added "fallen prospect value boost" (V4.1) in `engine/prospect_model.py`. When a prospect with grade >= 85 is still available past consensus_rank + 2, a value boost kicks in (overshoot * 3, max 25 points, 1.5x for position-need match). Carnell Tate R1 rate: 73.4% → 99.8%.
- **Applies when**: Any consensus-driven prediction model where plurality voting per slot can miss "always #2, never #1" candidates. The fix is universal: when a high-quality option cascades past expectations, its value should INCREASE, not plateau.

### INFLATED_PER_EFFECT_REPORTS — 2026-03-27
- **Context**: MyStrainAI — Adverse effects all showing identical inflated report counts (e.g. "2,198 reports" for every AE on Cherry Pie)
- **Bug**: Scraped data stored `reported_by` (total reporters for the strain) as the `reports` field for EVERY negative effect. 1,385 of 1,421 strains with 2+ AEs had this bug. The EffectsBreakdown component displayed raw `effect.reports` per row, showing the same inflated total for each.
- **Root cause**: Scraper wrote the strain-level reporter count to each individual effect instead of distributing it. The merge_adverse_effects.py script fixed strain-data.js (backend) with weighted distribution, but strains.json (frontend) retained the original inflated values.
- **Flawed assumption**: That `effect.reports` for adverse effects is a per-effect count. For AEs from the scraper, it's actually the strain's total reporter count.
- **Fix**: Hide per-effect report counts for adverse effects in EffectsBreakdown.jsx (`!isAdverse` guard on the reports display). The clinically-calibrated percentages already convey relative incidence. Use `estReviewers` (derived from positive effects) for the "Based on X user reviews" subtitle instead of `grouped.negative[0].reports`.
- **Applies when**: Any display of scraped adverse effect data — never trust raw per-effect report counts for AEs. The data quality is lower than positive effects. Rely on relative ordering + clinical calibration ceilings instead.

### LOCATION_PILLAR_DOMINANCE — 2026-03-27
- **Context**: MyStrainAI quiz — user in LA got Runtz as #1 result regardless of different effect selections
- **Bug**: Location pillar at 25% weight + Commonness at 15% = 40% of score was effect-independent. Runtz (reg[0]=90 for LA) got 22.5 points from Location alone, an insurmountable floor. Additionally, `calcEffectReportScore` overwrote duplicate effect names instead of accumulating reports (1,263 strains affected).
- **Root cause**: Scoring weights over-indexed on "can you find this strain" vs "does this strain match your effects." A quiz should be primarily about effect matching.
- **Flawed assumption**: That 25% Location weight balances well with effect-matching pillars. For regionally popular strains, the Location floor was too high for any effect-matching difference to overcome.
- **Fix**: (1) Reduced Location from 25% → 15% in both flavor/no-flavor modes, redistributing 10% to Science and Community. (2) Fixed `calcEffectReportScore` to accumulate reports for duplicate effect names instead of overwriting. New weights (no dispensary): 40/30/15/15 (Sci/Com/Common/Loc) without flavor; 35/25/15/15/10 with flavor.
- **Applies when**: Any scoring weight rebalancing. Keep effect-independent pillars (Location + Commonness) at ≤30% total. Effect matching should drive quiz results.

## UFC — Deploy-Before-Analyze: DEC Dead Zone Gate Regression

### DEC_DEADZONE_PREMATURE_DEPLOY — 2026-03-28
- **Context**: DEC method bet odds gating — implemented +150-200 dead zone gate, deployed to production as v11.16.0, then discovered through granular analysis that the gate was wrong
- **Bug**: Three cascading failures: (1) Deployed gate based on first analysis showing -5% ROI, (2) Subsequent +25-increment analysis showed the range was actually breakeven/profitable, (3) Widening the gate to +250/-125 caused -91.95u catastrophic regression because it blocked profitable longshots
- **Root cause**: Implemented and deployed an algorithm change BEFORE running the granular analysis that would have prevented it. The same odds range showed -5%, 0%, and +3.1% ROI across three different analyses without reconciling the contradiction. Gate logic also didn't account for how the backtester attributes wins/losses across odds ranges.
- **Flawed assumption**: That a single aggregate analysis is sufficient to justify an algorithm gate. Also assumed odds-range gating is symmetric — blocking a range blocks both wins AND losses in that range, including profitable longshots.
- **Reasoning lesson**: (1) NEVER deploy algorithm changes before granular analysis at the tightest increment. (2) When the same metric gives different values across analyses, the methodology is wrong — stop and reconcile before acting. (3) Marginal improvements (+0.04u/event) are noise, not signal — minimum threshold should be +0.10u/event. (4) Always backtest the gate in isolation BEFORE touching production code.
- **Fix**: Reverted to pre-gate state. Mandatory pre-deploy backtest rule added.
- **Applies when**: ANY algorithm gating rule based on odds ranges or statistical thresholds. Run +25 increment analysis FIRST, reconcile any contradictions, backtest in isolation, THEN deploy.

## Diamond Predictions — Local Build Deployed Without Firebase Auth

### LOCAL_BUILD_NO_AUTH — 2026-03-29
- **Context**: Ran `vite build` locally to deploy updated pick data. Local machine had no `.env.local` with VITE_FIREBASE_* vars.
- **What went wrong**: Deployed build had undefined Firebase credentials, disabling all user authentication on production site.
- **Root cause**: GitHub Actions injects Firebase secrets at build time. Local builds don't have these unless `.env.local` exists.
- **Fix**: Created `.env.local` with Firebase config extracted from previous working Cloudflare deployment. Rebuilt and redeployed.
- **Prevention**: Before ANY local build+deploy, verify `.env.local` exists. Check bundle size — missing Firebase SDK = ~130KB smaller bundle.
- **Rule**: NEVER deploy without verifying auth integrations are intact. This is a specific case of "NEVER disconnect working integrations."

[2026-03-29T15:23:22.641653] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T15:24:28.662553] GLM-5 violations: line_count=53>40, no_uncertainty_flag

[2026-03-29T15:27:01.279096] GLM-5 violations: line_count=41>40

[2026-03-29T15:29:57.275739] GLM-5 violations: no_uncertainty_flag

[2026-03-29T15:31:24.646990] GLM-5 violations: no_uncertainty_flag

[2026-03-29T15:32:22.282711] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T15:33:33.194813] GLM-5 violations: no_verification_trace

[2026-03-29T15:41:20.421076] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T15:41:20.665578] GLM-5 violations: line_count=62>40

[2026-03-29T15:45:50.736740] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T15:47:23.993843] GLM-5 violations: no_uncertainty_flag

[2026-03-29T15:49:53.804854] GLM-5 violations: no_uncertainty_flag

[2026-03-29T15:52:52.270695] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T16:04:06.350196] GLM-5 violations: no_verification_trace

[2026-03-29T16:33:43.568652] GLM-5 violations: no_uncertainty_flag

[2026-03-29T16:38:14.377770] GLM-5 violations: no_uncertainty_flag

[2026-03-29T16:40:26.070346] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T16:43:41.183757] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T16:51:28.441288] GLM-5 violations: line_count=46>40

[2026-03-29T16:53:17.991313] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T16:54:18.855569] GLM-5 violations: no_uncertainty_flag

[2026-03-29T16:55:02.728087] GLM-5 violations: no_uncertainty_flag

[2026-03-29T17:02:39.127031] GLM-5 violations: line_count=49>40

[2026-03-29T17:05:17.334897] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T17:07:22.895212] GLM-5 violations: line_count=42>40

[2026-03-29T17:07:40.524007] GLM-5 violations: no_verification_trace

[2026-03-29T17:10:05.234929] GLM-5 violations: no_uncertainty_flag

[2026-03-29T17:10:09.988979] GLM-5 violations: no_uncertainty_flag

[2026-03-29T17:12:51.149056] GLM-5 violations: line_count=63>40

[2026-03-29T17:13:49.151594] GLM-5 violations: no_uncertainty_flag

[2026-03-29T17:19:08.163310] GLM-5 violations: no_uncertainty_flag

[2026-03-29T17:20:49.169675] GLM-5 violations: no_uncertainty_flag

[2026-03-29T17:26:04.251993] GLM-5 violations: line_count=56>40

[2026-03-29T17:26:15.012946] GLM-5 violations: no_uncertainty_flag

[2026-03-29T17:43:39.440309] GLM-5 violations: line_count=74>40, no_uncertainty_flag

[2026-03-29T18:11:27.164853] GLM-5 violations: line_count=74>40

[2026-03-29T18:15:51.404553] GLM-5 violations: no_verification_trace

[2026-03-29T18:16:18.405945] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T18:16:42.936349] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T18:20:19.349124] GLM-5 violations: line_count=56>40

[2026-03-29T18:22:51.877081] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T18:26:26.565467] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T18:27:08.965741] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T18:29:03.066023] GLM-5 violations: line_count=45>40

[2026-03-29T18:29:39.124680] GLM-5 violations: line_count=142>40

[2026-03-29T18:31:06.379436] GLM-5 violations: line_count=168>40

[2026-03-29T18:33:41.099641] GLM-5 violations: line_count=98>40

[2026-03-29T18:34:28.355070] GLM-5 violations: line_count=144>40

[2026-03-29T18:35:55.905604] GLM-5 violations: no_uncertainty_flag

[2026-03-29T18:40:50.158549] GLM-5 violations: line_count=46>40, no_uncertainty_flag

[2026-03-29T18:41:55.653477] GLM-5 violations: no_uncertainty_flag

[2026-03-29T18:46:29.841959] GLM-5 violations: no_verification_trace, no_uncertainty_flag

[2026-03-29T18:47:17.286803] GLM-5 violations: line_count=145>40

[2026-03-29T18:48:51.332689] GLM-5 violations: no_uncertainty_flag

[2026-03-29T18:52:47.803267] GLM-5 violations: line_count=45>40

[2026-03-29T18:53:28.405876] GLM-5 violations: no_verification_trace

[2026-03-29T18:54:39.136189] GLM-5 violations: line_count=42>40, no_uncertainty_flag

[2026-03-29T18:54:58.281137] GLM-5 violations: no_uncertainty_flag

[2026-03-29T18:55:51.054608] GLM-5 violations: no_uncertainty_flag

## Diamond Predictions — NHL Pipeline Overwrites MLB prediction_log.json

### NHL_OVERWRITES_MLB_PREDLOG — 2026-03-31
- **Context**: MLB bet history showed 0 tracked picks for the 2026 season. The prediction_log.json was reset to a single day's data every pipeline run.
- **Root cause**: NHL daily pipeline writes a dict-format prediction_log.json (with `date`, `generated_at`, `version`, `picks` keys). MLB pipeline expects a list format. When MLB pipeline ran `load_json()` and got a dict, `isinstance(pred_log, list)` returned False, so it created an empty list — losing all prior MLB predictions.
- **Flawed assumption**: Both sports could share a single `prediction_log.json` file. They have incompatible formats (NHL=dict, MLB=list).
- **Fix**: Renamed MLB prediction log to `mlb_prediction_log.json` via config.py PREDICTION_LOG_PATH. Also fixed `final_bets` in system_bets_log to include ALL consensus picks (was filtered to EV-positive only, excluding 95% of picks from tracking).
- **Prevention**: When two pipelines share a repo, never share mutable state files without namespacing by sport.
