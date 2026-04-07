# Handoff — mmalogic — 2026-03-31 20:45
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_ufc-predict_2026-03-31_1510.md
## GitHub repo: nhouseholder/ufc-predict
## Local path: ~/Projects/mmalogic/
## Last commit date: 2026-03-31 18:15:41 -0700

---

## 1. Session Summary
User wanted three things: fix 3-leg parlay overlap (HC3/ROI3), build permanent autonomous odds scraping pipeline, and integrate Markov chain V2 fight simulation into the algorithm. Parlays were already correct (no overlap). Odds pipeline built with `check_prop_odds.py` + workflow fixes. Markov V2 was fully built, tested across 3 integration approaches (disagree penalty, agree boost, method ensemble), and rejected — algo outperforms Markov on every metric. Code preserved but disabled.

## 2. What Was Done
- **3-leg parlay overlap verification**: Confirmed HC3 and ROI3 have zero fighter overlap. ROI3 already excludes HC3 legs. No code change needed.
- **Version bump to v11.18.3**: Algorithm + version.js synchronized via /mmalogic agent.
- **Autonomous odds scraping pipeline**: Created `check_prop_odds.py` (gates workflow on missing odds), fixed push race conditions in both `refresh-prop-odds.yml` and `run-predictions.yml` (stash/rebase pattern), added odds cache files to commit list.
- **Markov chain V2 full implementation**: Built `_markov_build_matrix()`, `_markov_simulate()`, `markov_diff_modifier()` in algorithm. Monte Carlo simulation with STANDING/CLINCH/GROUND states, KO/SUB/DEC absorbing outcomes. Calibrated to match real UFC finish distributions (~40% KO, ~10% SUB, ~50% DEC).
- **Markov diagnostic tooling**: Created `markov_integration_test.py` (4 sanity check scenarios), `markov_diagnostic_v2.py` (backtest parser), in-algorithm diagnostic collector dumping `markov_diagnostic_v2.json` (501 fights).
- **Markov 3-approach evaluation**: Tested disagree penalty (+0.00u, algo 79.7% when Markov disagrees), agree boost (+0.00u, diff exhaustion), method ensemble (algo 55.4% vs Markov 46.8%). All rejected.
- **Experiment log**: Two experiments documented in `backtest_runs/EXPERIMENT_LOG.md` — parlays accepted, Markov rejected.
- **Memory updates**: Created `feedback_regenerate_picks_after_alg_push.md` and `feedback_auto_scrape_missing_odds.md`.

## 3. What Failed (And Why)
- **Markov disagree penalty**: Algo is MORE accurate (79.7%) when Markov disagrees than baseline (75.4%). Skipping those picks would cost -47.10u. Root cause: Markov career-stats model lacks fight-specific context the algorithm has.
- **Markov agree boost**: +0.00u because average differential is 1.68 and a 10% boost doesn't change any picks that are already above the 0.14 threshold. Diff exhaustion problem.
- **Markov method ensemble**: Algo 55.4% method accuracy vs Markov 46.8%. Ensemble helped DEC (+0.8pp) but hurt KO (-3.9pp). Net negative.
- **Initial Markov calibration**: Decision bias (87% A in even matchup) due to `>=` tiebreak, SUB rate near 0%. Fixed with noise injection and rate tuning.
- **backtest_output.txt empty**: Algorithm's Tee class + quiet mode = no stdout. Fixed with `_markov_diag_results` list dumped to JSON.

## 4. What Worked Well
- **In-algorithm diagnostic collector**: Dumping per-fight Markov data to JSON was the right approach — avoided parsing stdout.
- **Stash/rebase pattern for push races**: Clean solution for GitHub Actions concurrent push conflicts.
- **check_prop_odds.py gating**: Properly gates the refresh workflow so it only scrapes when odds are actually missing.
- **Disciplined experiment methodology**: Tested 3 distinct Markov integration approaches before rejecting. No premature deployment.

## 5. What The User Wants
- Autonomous systems that work without intervention: "make it permanent and autonomous and unavoidable" (re: odds scraping)
- No giving up on hard engineering: "Last time you gave up because it was a significant engineering task. Well guess what, no giving up, that's what you're for."
- Hypothesis-driven development with clear accept/reject criteria
- Markov preserved for future iteration — user sees it as promising long-term

## 6. In Progress (Unfinished)
All tasks completed. Markov disabled but code preserved for future work.

## 7. Blocked / Waiting On
Nothing blocked.

## 8. Next Steps (Prioritized)
1. **Markov V3: fight-specific features** — Add reach differential, stance matchup, recent form, cage vs no-cage. Career stats alone are too generic. See EXPERIMENT_LOG.md "Future Directions."
2. **Markov method prop betting** — Use simulation method probabilities to identify value in method prop markets (separate from score modification).
3. **Odds pipeline monitoring** — Verify the Wed/Thu/Fri/Sat scheduled scrapes are working for the next event. First real test will be this week.
4. **v11.19 hypothesis testing** — Continue backtest experiments. The 3-leg parlays added +128.68u additive revenue.

## 9. Agent Observations
### Recommendations
- The Markov approach has merit but needs richer features. Career stats alone produce a weaker signal than the algorithm's composite scoring. Fight-specific context (reach, stance, recent momentum) could close the gap.
- The diff exhaustion problem (avg 1.68, threshold 0.14) means ANY small score modifier will struggle to flip picks. Future modifiers need to target pick selection earlier in the pipeline, not post-diff.
- The autonomous odds pipeline should be monitored for its first real-world run this week.

### Data Contradictions Detected
No data contradictions.

### Where I Fell Short
- Initially tried parsing `backtest_output.txt` which was empty — should have checked file size first.
- Markov calibration required multiple iterations (decision bias, SUB rate) — could have validated the simulation engine more thoroughly before integration.

## 10. Miscommunications
None — session aligned. User gave clear direction and expectations throughout.

## 11. Files Changed
```
 UFC_Alg_v4_fast_2026.py                            |  274 +-
 algorithm_stats.json                               |    8 +-
 backtest_runs/EXPERIMENT_LOG.md                    |  190 +
 backtest_summary.json                              |    2 +-
 check_prop_odds.py                                 |   75 +
 markov_diagnostic_v2.json                          |  new
 markov_diagnostic_v2.py                            |  new
 markov_integration_test.py                         |  new
 .github/workflows/refresh-prop-odds.yml            |    4 +
 .github/workflows/run-predictions.yml              |   11 +
 prediction_cache/ufc_fight_night_moicano_vs_duncan |  326 +
 ufc_backtest_registry.json                         | 7086 +-
 ufc_profit_registry.json                           | 1318 +-
 ufc_prop_odds_cache.json                           |  172 +
 ufc_systems_registry.json                          |    2 +-
 webapp/frontend/public/data/*                      |  updated
 webapp/frontend/src/config/version.js              |    2 +-
```

| File | Action | Why |
|------|--------|-----|
| UFC_Alg_v4_fast_2026.py | Modified | Added Markov simulation functions + constants (MARKOV_ENABLED=False) |
| backtest_runs/EXPERIMENT_LOG.md | Modified | Logged parlay + Markov experiments |
| check_prop_odds.py | Created | Gates odds refresh workflow on missing odds |
| markov_diagnostic_v2.json | Created | 501-fight diagnostic output from Markov backtest |
| markov_diagnostic_v2.py | Created | Parses backtest output for Markov diagnostics |
| markov_integration_test.py | Created | Standalone Markov simulation sanity checks |
| .github/workflows/*.yml | Modified | Push race fix (stash/rebase) + odds cache commits |
| webapp/frontend/src/config/version.js | Modified | Bumped 11.18.2 → 11.18.3 |

## 12. Current State
- **Branch**: main
- **Last commit**: f702b44 v11.18.3: Markov chain V2 experiment (tested, rejected) + registry data refresh (2026-03-31)
- **Build**: untested (no frontend build run this session)
- **Deploy**: N/A — no frontend deploy this session
- **Uncommitted changes**: none
- **Local SHA matches remote**: yes

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: none running

## 14. Session Metrics
- **Duration**: ~120 minutes
- **Tasks**: 3/3 completed (parlay overlap, odds pipeline, Markov V2)
- **User corrections**: 0
- **Commits**: 15 (14 prior + 1 final)
- **Skills used**: /mmalogic (version bump), /full-handoff

## 15. Memory Updates
- `feedback_regenerate_picks_after_alg_push.md` — PERMANENT: verify picks regenerated after every alg push
- `feedback_auto_scrape_missing_odds.md` — PERMANENT: missing odds = auto-scrape, props post Wed/Thu, never accept "no odds" until Sat night

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| /mmalogic | Bump version.js (hook-gated) | Yes — only way past site guard hook |
| /full-handoff | Generate comprehensive handoff | Yes |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff
2. handoff_ufc-predict_2026-03-31_1510.md (previous session)
3. ~/.claude/anti-patterns.md
4. CLAUDE.md (project instructions)
5. backtest_runs/EXPERIMENT_LOG.md (experiment history)
6. AGENTS.md (scoring/baseline rules)

**Canonical local path for this project: ~/Projects/mmalogic/**
**Do NOT open this project from iCloud or /tmp/. Use the path above.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/Projects/mmalogic/**
**Last verified commit: f702b44 on 2026-03-31**
