# Handoff — diamond-predictions — 2026-04-08 12:10
## Model: Claude Sonnet 4.6
## Previous handoff: handoff_diamondpredictions_2026-04-08_2250.md
## GitHub repo: nhouseholder/diamond-predictions
## Local path: ~/Projects/diamondpredictions/
## Last commit date: 2026-04-08 11:54:32 -0700

---

## 1. Session Summary
User restored a downed site (apex domain DNS missing), fixed an empty black screen issue, investigated why both MLB and NHL were generating 0 picks, and then improved the system lifecycle to increase pick volume. By end of session: site is live, 18 new Professor MJ systems are registered, system registry pruning rules have been updated (10% ROI floor, -10% season floor), and 25 MLB + 17 NHL systems are ACTIVE. Both pick pipelines ran cleanly — 0 picks today but that is a thin slate/threshold issue, not a bug.

## 2. What Was Done

- **Apex DNS fix**: `diamondpredictions.com` had zero DNS records. Fixed by adding CNAME via authenticated Cloudflare browser session, re-adding the Pages custom domain. Site restored.
- **Cache purge + redeploy**: User saw black screen after DNS fix. Purged Cloudflare cache + triggered fresh deploy. Confirmed working.
- **18 MJ systems registered**: Added 10 MLB and 8 NHL Professor MJ systems to their respective registries as PROBATION (weight 0.7). Commit `09bfcf8`.
- **System activation strategy planned + executed**: Promoted 12 MLB PRUNED systems (ROI 12-19.8%, 80+ fires, 2+ profitable seasons) to PROBATION. Commit `f42d553`.
- **Auto-pruner bug fixed (MLB)**: `_evaluate_probation()` was using `MIN_CUMULATIVE_ROI=20%` which immediately re-pruned all PROBATION systems on every pipeline run. PROBATION was effectively impossible to maintain for any system with ROI < 20%.
- **Pruning rules updated (both sports)**: New rule — prune if cumulative ROI < 10% OR any single season < -10%. Changes: `mlb_predict/lifecycle/prune_rules.py`, `nhl_predict/config.py`, both `pruner.py` files. Commit `857d2bc`.
- **NHL PRUNED weight bug fixed**: All NHL PRUNED systems had `weight: 1.0` in the registry (the explicit `weight` field overrides the state-based `0.0` fallback in `_system_score()`), meaning PRUNED systems were firing at full weight. Fixed: 7 strong PRUNED → PROBATION, 5 bad PRUNED → weight set to 0.0.
- **NHL registry cleanup**: Demoted `Better Team Dog` (-100% ROI) and `Fade Post Blowout` (-22.5%) from ACTIVE → PROBATION. NHL RECOVERY_ROI threshold raised 10% → 15% to match MLB.
- **Both pipelines ran**: MLB: 25 ACTIVE systems (was 12), 0 qualifying picks today. NHL: 17 ACTIVE systems (was 14), 0 qualifying picks (3-game slate).

## 3. What Failed (And Why)

- **Auto-pruner ate all PROBATION systems on first pipeline run**: Placed 22 systems on PROBATION, ran pipeline, all 22 immediately re-pruned. Root cause: `_evaluate_probation()` calls `evaluate_system_pruning()` which applies `MIN_CUMULATIVE_ROI=20%` — any system with ROI < 20% has `should_prune=True`. PROBATION was only stable for ROI ≥ 20% (which would be ACTIVE). Fix: updated cumulative floor to 10%. Lesson: always read `prune_rules.py` before touching the registry.
- **`Fade Off Upset Less Favored`** (ROI 16.3%) could not be promoted: 2025 season was -42.5%, triggering the hard prune rule under the new -10% season floor. Correctly excluded.
- **NHL AutoPruner didn't show transitions during daily pipeline run**: The pipeline ran AutoPruner, but since the registry was set manually (not via the pipeline's normal flow), transitions didn't surface in the main pipeline log. Fix: ran pruner directly to apply and confirm.

## 4. What Worked Well

- Tracing the 0-picks root cause from pipeline logs → registry → `_system_score()` code was systematic and fast.
- Plan-mode workflow kept the pruner fix from being rushed into without fully understanding it.
- Reading `prune_rules.py` docstring ("PROBATION → PRUNED: ROI < 0% or any season < -25%") vs actual code behavior (prunes at < 20%) immediately exposed the inconsistency.

## 5. What The User Wants

- Site running with daily picks generating for both MLB and NHL
- System registry should produce picks without being silenced by over-aggressive pruning
- Clear activation strategy: systems at ROI 10-15% → PROBATION (monitored), ROI 15%+ → ACTIVE, < 10% or bad season → PRUNED
- User quote: "should we be activating more MLB/NHL systems off probation/watch to get more picks?"
- User quote: "prune any system with cumulative ROI < 10%, or if the system had any single season with total ROI < -10%. Apply that to both sports and re-run."
- Walk-forward backtest of MJ systems still pending from prior session

## 6. In Progress (Unfinished)

- **MJ systems backtest**: 18 MJ systems registered without walk-forward validation. Several MJ systems with ROI 5-9% auto-pruned this session (correct). Remaining PROBATION MJ systems:
  - MLB: `MJ Cold Teams Home` (14.8%), `MJ Pummeled Pitchers` (14.9%), `MJ Big Upset Rematch` (14.5%)
  - NHL: `MJ Hot Teams Fade` (13.8%), `MJ Streak Breaker` (14.7%), `MJ Hot Scorers Fade` (13.6%), `MJ Porous Defense Dog` (10.4%)
  - These need walk-forward backtest vs `backtest_baseline_v11.24.0.json` before promotion to ACTIVE.
- **NHL playoff transition**: Regular season ends ~2026-04-18. Verify playoff mode is active in `scripts/nhl/daily_pipeline.py` and that `Playoff R1 Road Fav` system (ACTIVE, 20% ROI) is correctly scoped.

## 7. Blocked / Waiting On

- **NHL goalie systems** (Fade Overperformer, Cold Goalie Bounce, Elite Goalie Bounce, Fade Hot Goalie, Fade Backup Fav, Goalie Edge Dog, ST Edge Dog): 0 picks, 0% ROI — waiting on goalie data integration. Do NOT demote — they'll fire once data is wired.
- `Better Team Dog` (NHL PROBATION, -100% ROI, 1 pick) and `Fade Post Blowout` (-22.5%, 6 picks): auto-pruner skips systems with < 15 picks. Monitor; they'll be pruned once they accumulate enough picks.

## 8. Next Steps (Prioritized)

1. **Verify picks generate on a normal game day** — today was thin (15 MLB games 0 qualifying, 3 NHL 0 qualifying). Run `python3 scripts/daily_pipeline.py --picks-only --date [tomorrow]` to confirm picks flow end-to-end on a full slate.
2. **Walk-forward backtest remaining MJ PROBATION systems** — 3 MLB + 4 NHL. Compare against `backtest_baseline_v11.24.0.json`. Promote to ACTIVE if they validate; auto-pruner will handle failures.
3. **NHL playoff mode check** — review `scripts/nhl/daily_pipeline.py` for playoff transition logic before April 18.
4. **Commit runtime artifacts** — `prediction_log.json`, `system_bets_log.json`, `data/splits_cache/2026-04-08.json` have local changes. Minor but keeps repo clean.

## 9. Agent Observations

### Recommendations
- The system registry lifecycle is now correct: PROBATION stable at ROI 10-14.9%, auto-prunes at < 10% or any season < -10%, promotes to ACTIVE at ≥ 15%. This is the right design — don't touch the thresholds again without a plan.
- If 0 picks persist on full-slate days, the bottleneck is likely `SCORE_THRESHOLD = 0.75` in `mlb_predict/config.py` or the conglomerate EV minimum — not the system registry. Investigate there next.
- NHL recovery threshold is now 15% (raised from 10% this session) to match MLB. This is consistent and correct.

### Data Contradictions Detected
- NHL PRUNED systems: `weight: 1.0` in registry JSON vs code expecting `lifecycle_mult = 0.0` for PRUNED state. The `weight` field (line 701-702, `nhl_predict/algorithms/systems.py`) takes precedence over the state fallback. Resolution: always set BOTH `state: PRUNED` AND `weight: 0.0` in NHL registry entries. Confirmed fixed.

### Where I Fell Short
- Should have read `pruner.py` and `prune_rules.py` before proposing the PRUNED → PROBATION promotions in the plan. The auto-pruner reversion was entirely predictable from reading those files. The extra pipeline run and registry restore loop cost time.

## 10. Miscommunications

- Proposed 12% ROI as the promotion threshold; user corrected to 10% as the universal pruning floor. No confusion — user direction was clear and immediate.

## 11. Files Changed

```
mlb_predict/lifecycle/prune_rules.py               |   4 +-
mlb_predict/lifecycle/pruner.py                    |   9 +-
mlb_predict/webapp/frontend/functions/data/picks.json |   4 +-
mlb_predict/webapp/frontend/public/data/homepage-stats.json | 4 +-
mlb_predict/webapp/frontend/public/data/nhl-bet-history.json | 2 +-
mlb_predict/webapp/frontend/public/data/nhl-predictions-today.json | 6 +-
mlb_predict/webapp/frontend/public/data/picks.json | 4 +-
mlb_predict/webapp/frontend/public/data/predictions_today.json | 4 +-
mlb_predict/webapp/frontend/public/data/version.json | 2 +-
mlb_predict/webapp/frontend/src/version.js         |   2 +-
mlb_system_registry.json                           | 646 +++
nhl_predict/__init__.py                            |   2 +-
nhl_predict/config.py                              |   5 +-
nhl_predict/lifecycle/pruner.py                    |  16 +-
nhl_system_registry.json                           | 190 ++
27 files changed, 1027 insertions(+), 296 deletions(-)
```

| File | Action | Why |
|------|--------|-----|
| `mlb_predict/lifecycle/prune_rules.py` | Modified | `MIN_CUMULATIVE_ROI` 20→10, `HARD_NEGATIVE_SEASON_THRESHOLD` -25→-10 |
| `mlb_predict/lifecycle/pruner.py` | Modified | `_evaluate_probation()` re-simplified; PROBATION now stable at ROI 10-14.9% |
| `mlb_system_registry.json` | Modified | 12 PRUNED→PROBATION, 7 PROBATION→ACTIVE, 8 correctly pruned by new rules |
| `nhl_predict/config.py` | Modified | `PRUNER_MIN_CUMULATIVE_ROI` 20→10, `PRUNER_RECOVERY_ROI` 10→15, new `PRUNER_SEASON_FLOOR=-10` |
| `nhl_predict/lifecycle/pruner.py` | Modified | Season floor check replaces `negative_seasons >= 2` |
| `nhl_system_registry.json` | Modified | 7 PRUNED→PROBATION, 3 PROBATION→ACTIVE, 4 MJ pruned, 5 PRUNED weights fixed 1.0→0.0 |
| `mlb_predict/webapp/frontend/public/data/picks.json` | Modified | 0-picks state published by pipeline run |
| `mlb_predict/webapp/frontend/public/data/nhl-predictions-today.json` | Modified | 0-picks state published by pipeline run |

## 12. Current State

- **Branch**: main
- **Last commit**: `857d2bc Update pruning rules and run pick generation pipelines (2026-04-08 11:54:32 -0700)`
- **Build**: Frontend deployed to Cloudflare Pages. Live at diamondpredictions.com.
- **Deploy**: ✓ Deployed — both pipelines ran and published 0-picks state
- **Uncommitted changes**: `prediction_log.json`, `system_bets_log.json`, `data/splits_cache/2026-04-08.json`, `logs/daily_pipeline_2026-04-08.log`, `logs/pipeline_history.json`, `nhl-bet-history.json` — runtime artifacts, not critical
- **Local SHA matches remote**: YES — both at `857d2bc`, `2026-04-08 11:54:32 -0700`

## 13. Environment

- **Node.js**: v25.6.1
- **Python**: 3.9.6
- **Dev servers**: None running

## 14. Session Metrics

- **Duration**: ~3 hours
- **Tasks**: 8 completed / 8 attempted
- **User corrections**: 2 (pruning threshold direction; model switch to Sonnet)
- **Commits**: 3 (`09bfcf8`, `f42d553`, `857d2bc`)
- **Skills used**: full-handoff

## 15. Memory Updates

- No new entries added to `anti-patterns.md` this session.
- **Recommended anti-pattern to log**: NHL registry weight field overrides state fallback in `_system_score()`. When debugging NHL system scoring, always check BOTH `weight` field AND `state` in `nhl_system_registry.json` — they can be inconsistent if the registry was set manually.

## 16. Skills Used

| Skill | Purpose | Helpful? |
|-------|---------|----------|
| full-handoff | Session wrap-up and state preservation | Yes |

## 17. For The Next Agent

Read these files first (in order):
1. This handoff (`~/Projects/diamondpredictions/HANDOFF.md`)
2. `~/.claude/anti-patterns.md`
3. `~/Projects/diamondpredictions/CLAUDE.md`
4. `~/Projects/diamondpredictions/MUST_READ.md`
5. `~/Projects/diamondpredictions/mlb_predict/lifecycle/prune_rules.py` — source of truth for pruning thresholds
6. `~/Projects/diamondpredictions/mlb_system_registry.json` — MLB system states (25 ACTIVE, 7 PROBATION, 35 PRUNED)
7. `~/Projects/diamondpredictions/nhl_system_registry.json` — NHL system states (17 ACTIVE, 10 PROBATION, 9 PRUNED)

**Critical context:**
- PROBATION systems (ROI 10-14.9%) are intentionally stable — do NOT manually prune. Auto-pruner manages transitions.
- NHL `_system_score()` uses `weight` field when present — always update BOTH `state` AND `weight` when changing NHL registry entries.
- MLB daily pipeline runs at 2 PM UTC (Mar-Oct). NHL has separate schedule.
- `SCORE_THRESHOLD = 0.75` in `mlb_predict/config.py` controls pick generation threshold.

**Canonical local path for this project: ~/Projects/diamondpredictions/**
**Last verified commit: 857d2bc on 2026-04-08 11:54:32 -0700**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: `git fetch && compare local SHA to remote` — git pull if behind
3. GATE 3: Read this handoff + MUST_READ.md + anti-patterns.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/Projects/diamondpredictions/**
**Last verified commit: 857d2bc on 2026-04-08 11:54:32 -0700**
