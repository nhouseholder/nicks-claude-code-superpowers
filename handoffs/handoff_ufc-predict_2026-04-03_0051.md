# Handoff — UFC Predict (MMALogic) — 2026-04-03 00:51
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: First comprehensive handoff for this session
## GitHub repo: nhouseholder/ufc-predict
## Local path: ~/ProjectsHQ/mmalogic/
## Last commit date: 2026-04-03 00:50:29 -0700

---

## 1. Session Summary
Massive session: fixed stale website data pipeline (Firestore overriding static JSON), built temporal career stats cache to eliminate data leakage in backtester, implemented 4 parlay types (HC2/ROI2/HC3/ROI3), added Over/Under bet type with real derived odds, tested 40+ hypotheses, and shipped 8 algorithm improvements totaling ~+100u. Baseline went from +290.30u to +648.51u through a combination of new bet types, algorithm improvements, and pipeline fixes.

## 2. What Was Done
- **Stale hero_stats fix**: hero_stats.json was showing +327.99u instead of registry truth +300.72u. getHeroStats() now always computes from registry. fix_registry auto-syncs derived files.
- **Temporal career stats cache**: Built `build_temporal_stats_cache.py` — 1,852 fighters × 15,593 date-indexed snapshots. Eliminates SLpM/SApM data leakage in walk-forward backtesting.
- **Version alignment**: Fixed triple version mismatch (alg docstring, ALG_VERSION, version.js). sync_and_deploy.py reads version from algorithm file dynamically.
- **Round column permanently removed**: Removed from EventSlideshow, EventBetsDropdown, AdminBacktest, AdminPerformance, HistoryPage. Round bets disabled since v11.14.4.
- **4 parlay types**: Added ROI2 (2-leg value) to backtester. All components now render HC2, ROI2, HC3, ROI3 via centralized `parlayUtils.js`. Combined parlay P/L: +247.64u.
- **Admin Overview fix**: Fixed wrong totals format (flat vs nested), replaced Round Rate with Combo Rate, version from APP_VERSION.
- **Firestore override killed**: Static JSON is sole source of truth. Disabled all Firestore real-time subscriptions for display data. Cache-busting with APP_VERSION.
- **Chinny opponent KO boost** (v11.20): +8.80u. When opponent has StrDef<50 + SApM>4.0, boost KO×1.25, DEC×0.80.
- **KO R2 combo gate expansion**: +30.58u. Combo bets now placed for KO R1 AND R2 predictions.
- **Pace-based R1 override**: +14.20u. High SLpM (≥5.0) fighters get KO R2→R1 override.
- **SYSTEM_SCORE_WEIGHT increase**: 0.05→0.20, +27.55u. Systems layer now meaningfully affects picks.
- **Over/Under bet type**: DEC→Over 2.5 with real derived odds, pillow fight trigger, grinder trigger. O/U: +55.81u (168W-79L). Odds value filter (skip Over < -160) doubled ROI.
- **O/U odds cache**: Built `ufc_ou_odds_cache.json` from prop data — 704 fights with derived O/U odds.
- **Fight-week scraper**: `fight_week_scraper.py` for weight miss/injury detection.
- **O/U on picks page**: FightCard.jsx shows "O/U Over 2.5" row for DEC predictions.
- **Men's-only backtest mode**: `UFC_MENS_ONLY=1` flag for gender-specific analysis/optimization.
- **Gender optimizer infrastructure**: Per-fight constant swapping via `_apply_gender_constants()`. Tested — found -28.56u regression, infrastructure kept but disabled.
- **MIN_OPP_UFC_FIGHTS 2→1**: +4.75u from scoring 31 more fights.
- **Pipeline fixes**: sync_and_deploy.py calls fix_registry as subprocess, includes archive patching, O/U computation.
- **6-step site edit protocol**: Saved to memory — pipeline, universal, knowledge, version, push, deploy.
- **Hypothesis testing protocol**: Start reasonable (flip a few picks), work up, never nuke the model.
- **40+ experiments logged**: backtest_runs/EXPERIMENT_LOG.md has 40 entries.

## 3. What Failed (And Why)
- **CONFOUNDED_COMPARISON**: Initial CTRL_OPP_ADJ showed false +8.08u from different pipeline runs. Caught and logged. See anti-patterns.md CONFOUNDED_COMPARISON.
- **HEAD_SEI_COEFF**: Monotonic regression at every value (0.02-1.0). Head defense already captured by StrDef and SEI composite. Double-counting.
- **Women's separate optimizer**: 51 bouts = 1.5 data points per parameter. Women's-weighted optimizer passed holdout (+7.18u) but combined with men's constants: -28.56u from cascading parlay/event interactions.
- **Gender-specific KD_STRIKE_VALUE**: Dead parameter — values from 14 to 22 all produce identical results. Score exhaustion.
- **Under 1.5 bets**: -9.13u with real odds. Market already prices R1 finishes efficiently.
- **bool() serialization crash**: `is_pass` from fight_breakdowns was a numpy bool that crashed json.dump mid-write, truncating ufc_profit_registry.json to 881 bytes. Fixed with `bool()` cast.
- **Pass fight O/U**: -0.67u. Passes overwhelmingly predict KO (21/26), not DEC.
- **O/U parlays**: -9.19u. Thin edges can't be parlayed.

## 4. What Worked Well
- **Pre-compute gate**: Saved hours by rejecting 12+ hypotheses via registry analysis before running backtests.
- **parlayUtils.js centralization**: Single source of truth for parlay types. Adding/removing a type = one edit.
- **sync_and_deploy.py pipeline**: One command does fix_registry → archive patch → validate → regenerate stats → sync → git push.
- **Real O/U odds derivation**: Computing Over/Under odds from existing DEC prop odds (f1_dec + f2_dec) gave honest P/L numbers.
- **Odds value filter**: Skipping Over bets when odds < -160 doubled ROI from 11.8% to 22.6%.

## 5. What The User Wants
- "whenever you edit the site, you must always: 1) ensure proactive pipeline, 2) universal fix, 3) update agent memory, 4) version bump, 5) sync github, 6) deploy" — Mandatory 6-step protocol for all site edits.
- "start with a large weighting, big enough to flip picks, and work backwards, stop wasting time with values that give the same result" — Hypothesis testing protocol.
- "i'm literally out of patience" (re: stale hero stats) — Firestore override was the root cause, permanently killed.
- User wants men's-specific optimization but data (51 women's bouts) is too limited for separate parameter sets.

## 6. In Progress (Unfinished)
- **Gender-specific optimization**: Infrastructure built (MENS_ONLY_MODE, per-fight constant swapping, optimizer flags), but the combined effect was -28.56u. Needs either (a) 100+ women's bouts for stable optimization, or (b) a simpler 2-3 parameter model instead of full 61-param optimization.
- **Website O/U display**: O/U shows on picks page but NOT in event history tables (HistoryPage, EventBetsDropdown, EventSlideshow). The registry has ou_pnl per bout but no frontend component renders it in tables yet.
- **O/U odds scraping**: `scrape_ou_odds.py` built but untested on live BFO pages. Uses derived odds from prop cache for backtesting.

## 7. Blocked / Waiting On
- **More women's data**: Need 100+ women's bouts (currently 51) for gender-specific optimization to be viable.
- **Real O/U odds from sportsbooks**: Current O/U odds are derived from DEC prop odds. Real DraftKings/BFO O/U lines would improve accuracy.

## 8. Next Steps (Prioritized)
1. **Add O/U to event history tables** — O/U data is in registry but not rendered on HistoryPage, EventBetsDropdown, or EventSlideshow. Low effort, high visibility.
2. **Test more O/U improvements** — Weight class rates (need to populate weight_class field in backtest registry), age-based triggers, conference-specific adjustments.
3. **Run full optimizer on current 550-bout dataset** — The standard optimizer hasn't run since v11.20 changes. A fresh optimization could find better parameters.
4. **Upcoming event: UFC Fight Night: Moicano vs. Duncan** — Picks generated, O/U bets included. Run fight_week_scraper.py Friday for weight miss checks.

## 9. Agent Observations
### Recommendations
- The algorithm has reached diminishing returns on single-parameter changes — most features are "score exhausted" (changes don't cross the 0.14 pick threshold). Future gains likely come from (a) new bet types like O/U, (b) more data (events 72+), or (c) structural changes to the scoring model.
- The O/U bet type is the biggest untapped opportunity. Current +55.81u from 247 bets. Improving DEC prediction accuracy would directly increase O/U profits.
- Women's MMA optimization needs a different approach: instead of full 61-param optimization, use 2-3 targeted adjustments (DEC tiebreak, KO dampen, pick threshold) that can be validated on 51 bouts without overfitting.

### Data Contradictions Detected
- O/U P/L with estimated odds (+99.82u) vs real derived odds (+55.81u) — a +44u overestimate from using +200 for Under 1.5 when real odds were -100 to -150.
- Combined P/L varies by ±10u depending on pipeline order (fix_registry vs archive_patch interaction). The archive patcher recalculates totals and can shift numbers.

### Where I Fell Short
- Wasted time sweeping KD_STRIKE_VALUE (14-22 all identical) when pre-compute could have detected score exhaustion.
- Gender constant swapping caused a -28.56u regression that wasn't caught by individual holdout tests — should have tested combined effect in a smaller scope first.
- bool() serialization crash on is_pass field corrupted the registry multiple times before being diagnosed.
- Multiple git conflicts from auto-update cron jobs running in parallel with manual pushes.

## 10. Miscommunications
- User said 4 parlay types are HC2, HC3, ROI2, ROI3. I initially included "Mega" parlay which the user clarified doesn't exist. Fixed by replacing Mega with ROI2 in the backtester.
- User wanted separate men's/women's optimizers. I initially built a men's-only backtest (just filtering women) instead of the intended per-fight constant swapping. Corrected after user feedback.

## 11. Files Changed
Major files touched this session (50+ commits):

| File | Action | Why |
|------|--------|-----|
| UFC_Alg_v4_fast_2026.py | MODIFIED | v11.20-11.21: chinny KO boost, KO R2 combos, pace R1 override, system weight increase, O/U fields, women's adjustments, gender optimizer infrastructure, MENS_ONLY_MODE, bool() fix |
| fix_registry_placed_flags.py | MODIFIED | O/U bet computation, combo estimation, all-parlay totals, pillow fight trigger, grinder trigger, odds value filter |
| sync_and_deploy.py | MODIFIED | Calls fix_registry as subprocess, O/U in totals, hero_stats includes O/U, archive patch step |
| patch_registry_from_archive.py | MODIFIED | O/U preservation in event/global totals |
| webapp/frontend/src/lib/parlayUtils.js | CREATED | Single source of truth for parlay types |
| webapp/frontend/src/lib/registryData.js | MODIFIED | Firestore killed, cache-busting, O/U in summaries, all parlays |
| webapp/frontend/src/lib/adminData.js | MODIFIED | Static JSON priority over Firestore |
| webapp/frontend/src/components/landing/EventSlideshow.jsx | MODIFIED | Round removed, all parlays, O/U |
| webapp/frontend/src/components/shared/EventBetsDropdown.jsx | MODIFIED | All parlays, combined P/L |
| webapp/frontend/src/routes/HistoryPage.jsx | MODIFIED | All parlays, rnd crash fix |
| webapp/frontend/src/components/admin/AdminOverview.jsx | MODIFIED | Correct nested totals, version from APP_VERSION |
| webapp/frontend/src/components/admin/AdminBacktest.jsx | MODIFIED | All parlays, round removed |
| webapp/frontend/src/components/landing/LastWeekPicks.jsx | MODIFIED | All parlays |
| webapp/frontend/src/components/picks/FightCard.jsx | MODIFIED | RND removed, O/U bet row added |
| build_temporal_stats_cache.py | CREATED | Temporal career stats for walk-forward integrity |
| ufc_temporal_stats_cache.json | CREATED | 15,593 snapshots for 1,852 fighters |
| ufc_ou_odds_cache.json | CREATED | 704 fights with derived O/U odds |
| fight_week_scraper.py | CREATED | Scrapes weigh-in results for weight misses |
| scrape_ou_odds.py | CREATED | Scrapes BFO for real O/U odds |
| backtest_runs/EXPERIMENT_LOG.md | MODIFIED | 40+ experiment entries |

## 12. Current State
- **Branch**: main
- **Last commit**: 73449aa Experiment: gender-specific KD_STRIKE_VALUE — REJECTED (2026-04-03 00:50:29)
- **Build**: Passes (verified vite build 1.89s)
- **Deploy**: Deployed via GitHub CI (Cloudflare Pages)
- **Uncommitted changes**: backtest artifacts (backtest_summary.json, fight_breakdowns.json, optimizer_results.json, ufc_backtest_registry.json), deleted constants_mens.json
- **Local SHA matches remote**: YES (73449aa)

## 13. Environment
- **Node.js**: v25.x (with NODE_OPTIONS=--max-old-space-size=4096 for builds)
- **Python**: 3.9.6
- **scipy**: 1.13.1 (installed this session for optimizer)
- **Dev servers**: None running

## 14. Session Metrics
- **Duration**: ~8 hours
- **Tasks**: 35+ completed / 40+ attempted
- **User corrections**: 5 (Mega parlay naming, men's optimizer scope, women's optimization approach, hypothesis testing protocol, KD strike value dead parameter)
- **Commits**: 50+
- **Skills used**: mmalogic, backtest, various

## 15. Memory Updates
- **anti-patterns.md**: STALE_HERO_STATS, CONFOUNDED_COMPARISON entries added
- **feedback_site_edit_protocol.md**: 6-step mandatory checklist for all site edits
- **feedback_stale_derived_data.md**: hero_stats/algo_stats must match registry
- **project_round_column_removed.md**: Round permanently removed from all tables
- **feedback_hypothesis_testing_protocol.md**: Start reasonable, work up, never nuke model
- **feedback_mmalogic_site_edit_protocol.md**: Global memory version of 6-step protocol
- **ufc_website_maintenance_rules.md**: Updated rules 1, 3, 21, added rules 30-31

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| mmalogic | Site edits, domain knowledge | Yes — essential for all website changes |
| backtest | Hypothesis testing | Yes — pre-compute gate saved hours |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff
2. ~/.claude/anti-patterns.md
3. CLAUDE.md (project root)
4. backtest_runs/EXPERIMENT_LOG.md (40+ experiments)
5. webapp/frontend/src/lib/parlayUtils.js (parlay single source of truth)
6. fix_registry_placed_flags.py (O/U logic, combo estimation, all business rules)

**Canonical local path for this project: ~/ProjectsHQ/mmalogic/**
**Do NOT open this project from iCloud or /tmp/. Use the path above.**

**Current baseline: +648.51u** (71 events, v11.20, after full pipeline)

| Stream | P/L | Record |
|--------|-----|--------|
| ML | +121.91u | 380W-143L |
| Method | +155.29u | 161W-195L |
| Combo | +87.76u | 30W-60L |
| O/U | +55.81u | 168W-79L |
| Parlays | +247.64u | HC2+ROI2+HC3+ROI3 |
| **Combined** | **+648.51u** | |

**Pipeline command:** `python3 sync_and_deploy.py --commit` (does everything: fix_registry → archive patch → validate → regenerate stats → sync → git push → CI deploy)

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/ProjectsHQ/mmalogic/**
**Last verified commit: 73449aa on 2026-04-03 00:50:29**
