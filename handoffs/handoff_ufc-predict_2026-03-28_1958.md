# Handoff — mmalogic (UFC Predict) — 2026-03-28 19:58
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_ufc-predict_2026-03-28_1610.md
## GitHub repo: nhouseholder/ufc-predict
## Local path: ~/Library/Mobile Documents/com~apple~CloudDocs/ProjectsHQ/mmalogic/
## Last commit date: 2026-03-28 18:55:37 -0700

---

## 1. Session Summary
User reported ghost X bugs in event history tables (206 cells showing "✗ —" with no dollar amount) and stale hero stats. Session fixed the ghost X bug by adding explicit `*_placed` flags to the registry schema, fixed hero stats to compute from event data instead of stale totals, permanently disabled standalone round bets (user decision), implemented KO slight-fav skip gate (+16.05u backtest improvement), removed Round hero card, and tested 3 additional optimization proposals (GSA gate, KO longshot fallback, KRS modifier) — all showed +0.00u or marginal improvement in walk-forward backtesting. Current version: v11.15.1, combined P/L: +279.26u.

## 2. What Was Done
- **Ghost X fix (v11.14.2)**: Added `ml_placed`, `method_placed`, `round_placed`, `combo_placed` boolean flags to every bout in the registry. Created `fix_registry_placed_flags.py` migration (206 ghost Xs → 0) and `validate_registry_cells.py` validation gate. Updated HistoryPage.jsx and EventBetsDropdown.jsx with four-state BetCell rendering + tooltips.
- **Hero stats pipeline fix (v11.14.3)**: Rewrote `computeSummaryFromRegistry()` to aggregate from event-level data instead of reading stale `registry.totals` flat keys.
- **Standalone round bets disabled (v11.14.4)**: User confirmed standalone round bets were never part of the model. Removed from backtester, track_results.py, and registry. Gained +4.46u.
- **KO slight-fav skip gate (v11.15)**: Walk-forward backtest: +16.05u improvement by skipping 18 KO predictions on slight favorites (-100 to -150 odds).
- **Round hero card removed (v11.15.1)**: 5→4 cards on landing page. Updated grid, copy, and ROI calculation.
- **GSA hybrid SUB gate tested**: +0.00u delta. Reverted.
- **KO longshot DEC fallback tested**: +0.00u delta. Reverted.
- **KRS modifier tested**: +2.80u at boost=2.0 but marginal and fragile. Code left disabled (KO_RESISTANCE_BOOST=0.0).

## 3. What Failed (And Why)
- **GSA hybrid SUB gate (+0.00u)**: Elite grapplers win by DEC 56% of the time — the submission threat creates control, not finishes. See anti-patterns: GSA_GATE_NO_IMPROVEMENT.
- **KO longshot DEC fallback (+0.00u)**: Walk-forward backtester produces different method predictions per event, so targeted fights change. Registry analysis is unreliable for method-swap gates.
- **KRS modifier (+2.80u, marginal)**: Narrow improvement surface — KRS=3.0 crashed to -21u.
- **Key lesson**: Method fallback gates (swap prediction after the fact) show +0.00u in walk-forward backtests. Only gates that skip entire fights survive backtesting.

## 4. What Worked Well
- Explicit `*_placed` flags cleanly solved the ghost X problem
- Computing hero stats from event data is permanently correct
- Running real backtests for every proposal — caught 3 false positives
- KO slight-fav skip gate worked because it skips entire fights, not method swaps

## 5. What The User Wants
- "we really need to make a better system for managing and updating these tables on the website"
- "standalone round bets are NOT part of our algorithm"
- User has many more optimization ideas from fresh agent analysis, wants to continue testing

## 6. In Progress (Unfinished)
All tasks completed. User has additional optimization ideas queued for the next session.

## 7. Blocked / Waiting On
- **UFC Seattle results**: Event is 2026-03-28. Run `track_results.py` after fights complete.
- **Local git repo corruption**: iCloud repo has object corruption. All commits via /tmp clone.

## 8. Next Steps (Prioritized)
1. **Score UFC Seattle results** — run track_results.py, then /mmalogic to update site
2. **Continue optimization testing** — user has more ideas from fresh agent analysis
3. **Fix local git repo** — re-clone from GitHub to fix iCloud object corruption
4. **Monitor KRS modifier** — code at KO_RESISTANCE_BOOST=0.0, can enable at 2.0 if warranted

## 9. Agent Observations
### Recommendations
- Method fallback gates don't survive walk-forward backtesting. Only full-fight skips work.
- Run `validate_registry_cells.py --strict` after EVERY registry write.
- Registry-level analysis overestimates method-swap improvements. Always backtest immediately.

### Data Contradictions Detected
- Registry analysis for KO slight-fav skip: +11.43u. Backtest: +16.05u (walk-forward predictions differ).
- Registry method totals (214W-241L) vs backtester (161W-201L) — registry counted bets without real odds.

### Where I Fell Short
- Ran 3 method-swap gates sequentially before recognizing the +0.00u pattern. Should have identified the structural issue after the first one.

## 10. Miscommunications
- User thought negative Round P/L on hero meant R1 gate wasn't working. Clarified the gate was working; user then revealed round bets were never intended.

## 11. Files Changed
19 files changed across 7 commits:

| File | Action | Why |
|------|--------|-----|
| fix_registry_placed_flags.py | Created | Migration script for *_placed flags |
| validate_registry_cells.py | Created | Post-write validation gate |
| UFC_Alg_v4_fast_2026.py | Modified | *_placed, round disabled, KO skip, KRS (disabled) |
| track_results.py | Modified | *_placed flags, round disabled |
| ufc_profit_registry.json | Modified | All data corrections + backtest results |
| HistoryPage.jsx | Modified | Four-state BetCell + tooltips |
| EventBetsDropdown.jsx | Modified | Four-state BetCell |
| registryData.js | Modified | Event-level aggregation for hero stats |
| HeroStats.jsx | Modified | Removed Round card, 4-col grid |
| version.js | Modified | 11.14 → 11.15.1 |
| CLAUDE.md | Modified | Baselines, rules, anti-patterns updated |

## 12. Current State
- **Branch**: main
- **Last commit**: 8bd0fd3 v11.15.1 (2026-03-28 18:55:37 -0700)
- **Build**: passing
- **Deploy**: deployed via GitHub CI (all commits auto-deployed)
- **Uncommitted changes**: KRS code reverted locally (disabled, non-critical)
- **Local SHA matches remote**: NO — iCloud git corruption. GitHub at 8bd0fd3 is authoritative.

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: none running

## 14. Session Metrics
- **Duration**: ~120 minutes
- **Tasks**: 8 completed / 8 attempted
- **User corrections**: 1 (round bets not part of model)
- **Commits**: 7
- **Skills used**: /mmalogic (2x), /review-handoff

## 15. Memory Updates
- feedback_no_standalone_round_bets.md — PERMANENT: no standalone round bets
- anti-patterns.md — GHOST_X_NO_PLACED_FLAG, GSA_GATE_NO_IMPROVEMENT
- CLAUDE.md — baselines v11.15, round disabled, KO skip gate, 6th anti-pattern

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| /mmalogic | Deploy v11.14.2 and v11.15.1 | Yes |
| /review-handoff | Session start orientation | Yes |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff
2. Previous: handoff_ufc-predict_2026-03-28_1610.md
3. ~/.claude/anti-patterns.md
4. Project CLAUDE.md
5. EVENT_TABLE_SPEC.md
6. feedback_no_standalone_round_bets.md

**Canonical local path: ~/Library/Mobile Documents/com~apple~CloudDocs/ProjectsHQ/mmalogic/**
**NOTE: Local git repo has object corruption. Use /tmp clones for all git ops.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/Library/Mobile Documents/com~apple~CloudDocs/ProjectsHQ/mmalogic/**
**Last verified commit: 8bd0fd3 on 2026-03-28 18:55:37 -0700**
