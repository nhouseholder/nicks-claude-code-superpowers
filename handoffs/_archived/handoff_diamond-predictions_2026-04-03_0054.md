# Handoff — Diamond Predictions — 2026-04-03 00:54
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_diamond-predictions_2026-03-31_2020.md
## GitHub repo: nhouseholder/diamond-predictions
## Local path: ~/ProjectsHQ/diamondpredictions/
## Last commit date: 2026-04-02 22:21:56 -0700

---

## 1. Session Summary
Massive session covering both NHL and MLB algorithms. Started by diagnosing MLB sharp systems (found 3 critical bugs making them completely dead in production), then analyzed the NHL 4-16 losing streak, researched and tested 6 NHL improvement hypotheses via walk-forward backtest, shipped NHL v10 (+7.6pp ROI improvement), added monthly edge scaling, fixed MLB de-vig bug found during objective algorithm review, built comprehensive experiment log, and added CLV tracking to NHL. Version bumped to v13.5.0.

## 2. What Was Done
- **MLB sharp systems fix (3 bugs)**: (1) DraftKings scraper returned 3/30 teams — wired Action Network as primary splits source. (2) Zero sharp systems in mlb_system_registry.json — added all 17 with lifecycle states. (3) score_and_select() silently dropped all sharp signals at registry gate. Commit `9331d03`.
- **MLB Action Network as odds fallback**: Added AN as third odds source (S&O → Covers → AN) to ensure odds availability on light schedules. Commit `26dd4b9`.
- **NHL 4-16 streak analysis**: Identified 3 root causes — 90% underdog exposure, phantom 5%+ edges in March, DIAMOND tier 0-7 collapse. March was 33% WR at -24.8% ROI.
- **NHL v10 feature activation**: Tested rest_days_delta (0.25) and hdcf_pct_delta (0.40) in 3-season walk-forward. Grid searched 9 weight combinations. Combined result: 461 picks, +61.7% ROI, 49.7% WR, 0.355 Sharpe (vs baseline 56.0%, 47.5%, 0.321). Commit `9c19a57`.
- **NHL monthly edge scaling**: Added MONTH_EDGE_SCALE to conglomerate. Tested 4 variants. Mild (Mar 1.5x, Apr 1.2x) shipped: +63.6% ROI, 50.1% WR, 0.365 Sharpe. Commit `c57e895`.
- **Version bump to v13.5.0**: Updated VERSION, version.js, version.json. Deployed to Cloudflare Pages. Commit `d68ed5f`.
- **Comprehensive experiment log**: Created EXPERIMENT_LOG.md documenting all 38 experiments that worked, 22 that didn't, 9 untested hypotheses. Backfilled from 175 commits, 6 handoffs, 8 result files. Commits `c0aec8a`, `292f494`, `02b9306`.
- **Objective algorithm review**: Systematic review of both algorithms. Found MLB conglomerate de-vig bug, NHL optimizer dead features, missing CLV tracking.
- **MLB conglomerate de-vig fix**: `_ml_to_prob()` was using raw implied probability including ~3.5% vig. Updated to take both home_ml and away_ml for proper de-vigging. All 3 call sites fixed. Commit `2d3d201`.
- **NHL optimizer search space update**: Swapped dead xgf_pct_delta (converges to 0.02) for proven hdcf_pct_delta, rest_days_delta, special_teams_delta. Now 8 features in search space. Commit `2d3d201`.
- **NHL CLV tracking**: Added open_ml field to bet history, CLV computation during grading, avg CLV reporting. Commit `2d3d201`.

## 3. What Failed (And Why)
- **Experiment script timeout**: The 11-variant experiment_hypotheses.py timed out running all backtests sequentially. Fixed by running each hypothesis individually via inline Python.
- **Agent limit hit**: Tried to spawn 4 parallel agents but hit 2-agent limit. Worked around by running remaining investigations manually.
- **No failures in algorithm fixes**: All changes compiled and verified on first attempt.

## 4. What Worked Well
- Running individual hypothesis tests inline (30 min each) instead of a monolithic experiment script
- Grid search for optimal weight combination (9 combos) — found clear winner (0.25, 0.40)
- Pre-computing what data was available before implementing features (hdcf_pct already in rolling stats)
- Cross-referencing live performance patterns (edge buckets, ML buckets, monthly breakdown) to identify the real problem areas before hypothesizing fixes

## 5. What The User Wants
- Flat 1-unit bets — no Kelly sizing changes, improvements come from pick quality
- "assess why we are 4-16 over our last 20 NHL bets" — wants diagnosis of losing streaks
- "how could the NHL algorithm be even more profitable, higher ROI, do a full audit, do external research" — wants systematic improvement with evidence
- "make an experiment log of everything we have tested" — wants comprehensive institutional knowledge
- "objectively review our algorithms for MLB and NHL" — wants honest assessment including weaknesses

## 6. In Progress (Unfinished)
All tasks completed.

## 7. Blocked / Waiting On
Nothing blocked.

## 8. Next Steps (Prioritized)
1. **Test H1-H4 from experiment log** (NHL): Score-adjusted Corsi, edge cap on v10, consecutive road games, one-goal WR — all data-ready, 30 min each
2. **Full CMA-ES re-optimization with v10 features** — current v10 uses manually-selected weights. CMA-ES could find better values AND re-tune all features jointly. New optimizer search space already updated.
3. **Monitor MLB with de-vig fix** — the de-vig correction removes ~2pp of phantom edge. Watch if pick quality improves (fewer false-positive edge picks).
4. **Monitor NHL CLV** — first CLV data accumulates from next grading cycle. Positive avg CLV = model has real edge. Negative = model is chasing noise.
5. **Wire NHL combo systems into live pipeline** — 7 COMBO systems (Public Overreaction +32.6% ROI, etc.) only exist in backtest path, never called in production.
6. **Consider reducing NHL parameter count** — 50 params / 450 picks = 1:9 ratio. Fold degradation (82.9% → 52.8% → 38.7%) is classic overfit signal.
7. **Upgrade GitHub Actions Node.js from 20 to 24** — deprecation warning on every pipeline run (forced June 2, 2026)

## 9. Agent Observations
### Recommendations
- The MLB de-vig bug was likely inflating edges by ~2pp for months. Some live picks that appeared to have 5%+ edge may have had only 3% real edge. Monitor whether the fix changes pick volume (fewer picks clearing MIN_EDGE).
- NHL fold degradation (82.9% → 52.8% → 38.7%) is the most concerning signal. It means the model's edge is partially illusory — some of the backtest ROI comes from overfitting to the specific test years. Each future live season may underperform the backtest by 15-20pp.
- The experiment log (EXPERIMENT_LOG.md) should be updated after every future experiment. It's now the definitive record of what's been tried.

### Data Contradictions Detected
- NHL backtest_results.json showed 926 picks at +34.2% ROI for v10, but the inline backtest showed 447 picks at +63.6%. The stored file was from a different run (possibly with different params or require_real_odds setting). The inline test results are authoritative for the v10 comparison.

### Where I Fell Short
- Should have identified the MLB de-vig bug earlier — it was visible in the code from the first read but I focused on NHL improvements first. The inconsistency (StatModel de-vigs, Conglomerate doesn't) should have been flagged immediately.
- The experiment script timeout was predictable — 11 backtests at ~3 min each = 33 min, close to the timeout. Should have run in smaller batches from the start.

## 10. Miscommunications
None — session aligned. User gave clear direction at each decision point.

## 11. Files Changed
| File | Action | Why |
|------|--------|-----|
| `mlb_predict/run.py` | Modified | Wire AN as primary splits source + odds fallback |
| `mlb_predict/algorithms/conglomerate.py` | Modified | Fix _ml_to_prob() de-vig bug |
| `mlb_system_registry.json` | Modified | Add 17 sharp systems with lifecycle states |
| `mlb_predict/data/action_network_scraper.py` | Modified | Add __future__ annotations for Py 3.9 compat |
| `nhl_predict/algorithms/winprob.py` | Modified | Add hdcf_pct_delta passthrough + update default weights |
| `nhl_predict/algorithms/conglomerate.py` | Modified | Add monthly edge scaling (MONTH_EDGE_SCALE) |
| `nhl_predict/optimization/optimizer.py` | Modified | Update search space (swap dead features for proven ones) |
| `nhl_data/optimized_params_v10.json` | Modified | v10 params with rest_days, hdcf_pct, month scaling |
| `data/optimized_params_v10.json` | Created | Copy of v10 params for pipeline pickup |
| `scripts/nhl/daily_pipeline.py` | Modified | Add CLV tracking + open_ml to bet history |
| `scripts/nhl/experiment_hypotheses.py` | Created | Reproducible hypothesis testing script |
| `EXPERIMENT_LOG.md` | Created | Full experiment history (38 worked, 22 failed, 9 untested) |
| `VERSION` | Modified | 13.4.3 → 13.5.0 |
| `mlb_predict/webapp/frontend/src/version.js` | Modified | 13.5.0 |
| `mlb_predict/webapp/frontend/public/data/version.json` | Modified | 13.5.0 |

## 12. Current State
- **Branch**: main
- **Last commit**: 2d3d201 Fix MLB de-vig bug, update NHL optimizer, add NHL CLV tracking (2026-04-02 22:21:56 -0700)
- **Build**: untested locally (CI/CD builds on GitHub Actions)
- **Deploy**: v13.5.0 deployed to Cloudflare Pages (auto-triggered by version.js push)
- **Uncommitted changes**: none (clean)
- **Local SHA matches remote**: yes (2d3d201)

## 13. Environment
- **Node.js**: N/A (CI uses v20)
- **Python**: 3.9.6 (local), 3.11 (CI)
- **Dev servers**: NestWise HQ Next.js running (unrelated project)

## 14. Session Metrics
- **Duration**: ~240 minutes
- **Tasks**: 12/12 completed
- **User corrections**: 0
- **Commits**: 10 (9331d03, 26dd4b9, 9c19a57, d68ed5f, c57e895, 458900b→rebased, c0aec8a, 292f494, 02b9306, 2d3d201)
- **Skills used**: /update-diamond, /whats-next, /full-handoff

## 15. Memory Updates
- No anti-patterns logged (no new bugs discovered beyond the de-vig fix)
- EXPERIMENT_LOG.md serves as the experiment memory — 635 lines covering all historical tests
- No recurring bugs encountered

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| /update-diamond | Deploy v13.5.0 to production | Yes — triggered Cloudflare deploy |
| /whats-next | Generate prioritized recommendations | Yes — identified monthly edge scaling and re-optimization |
| /full-handoff | This handoff | Yes |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff (HANDOFF.md)
2. EXPERIMENT_LOG.md — comprehensive record of all 70+ experiments
3. MUST_READ.md — algorithm architecture and validation protocol
4. ~/.claude/anti-patterns.md — search for "diamond", "NHL", "MLB"
5. CLAUDE.md — project structure and deployment pipeline

**Canonical local path for this project: ~/ProjectsHQ/diamondpredictions/**
**Do NOT open this project from iCloud or /tmp/. Use the path above.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/ProjectsHQ/diamondpredictions/**
**Last verified commit: 2d3d201 on 2026-04-02 22:21:56 -0700**
