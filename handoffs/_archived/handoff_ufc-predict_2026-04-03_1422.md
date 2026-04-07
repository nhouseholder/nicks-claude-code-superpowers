# Handoff — UFC Predict (MMALogic) — 2026-04-03 14:22
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_ufc-predict_2026-04-03_0051.md
## GitHub repo: nhouseholder/ufc-predict
## Local path: ~/ProjectsHQ/mmalogic/
## Last commit date: 2026-04-03 14:21:51 -0700

---

## 1. Session Summary
Built complete Over/Under bet type from scratch — Under 2.5 trigger, split thresholds, conflict resolution, real derived odds, and frontend integration across all pages. Tested women's ML ROI (rejected), exhaustive hedge analysis (rejected), 28+ Over conditions. Baseline: +621.48u to +759.20u. Algorithm v11.21.1 with 5 active bet types.

## 2. What Was Done
- **O/U on all tables**: EventSlideshow, EventBetsDropdown, HistoryPage, AdminBacktest, AdminPerformance, LastWeekPicks, HeroStats (5th card), AdminOverview. Cyan color.
- **Under 2.5 trigger**: avg_dec < 0.45 (DEC) / < 0.35 (KO/SUB). +74.34u Under, +107.50u Over = +181.84u O/U total.
- **Conflict resolution**: When Under fires on DEC, drop method bet (saves -11.35u). Exhaustive 6-action cross-tab per cell.
- **Real derived odds**: 618 fights from DEC props. ±400 odds cap.
- **Prediction pipeline**: Under trigger, split threshold, SUB→DEC handling, drop_method_for_under in picks JSON, FightCard suppression.
- **FightCard combo key fix**: red_ko_rd1 (not red_combo_ko_rd1).
- **Pipeline**: track_results.py has "ou", registryData.js has O/U in time windows, sync_and_deploy has O/U in algorithm_stats.
- **Women's ML ROI**: REJECTED -38.95u. Hedge analysis: REJECTED -54.22u.
- **CLAUDE.md**: Baseline to v11.21.1, O/U decision tree, 5 bet types.
- **11 experiments logged** + complete O/U reference section in EXPERIMENT_LOG.md.

## 3. What Failed (And Why)
- **Women's ML adjustments**: -38.95u. 73 bouts too volatile. Constants reverted.
- **DEC+Under signal conflict**: Initially restricted Under to non-DEC (-41.51u cost). Reversed after ROI analysis.
- **Hedge strategy**: -54.22u. Both-plus-money bouts are low-confidence passes. 33% ML loss rate kills 2u risk.
- **Worktree file divergence**: Python ran main repo files, not worktree edits. ~30 min debugging.

## 4. What Worked Well
- **Pre-compute screening**: 17 Under + 28 Over conditions tested via registry scan before any backtest.
- **Exhaustive 6-action cross-tab**: Proved every cell is optimal.
- **Incremental analysis**: Always checked NEW value beyond existing triggers.

## 5. What The User Wants
- "what matters is the ROI based on real odds" — ROI is the decision metric
- "any combo that has a real ROI >22.5% we should implement" — acceptance threshold
- "we have to know for EACH if there is a contradiction, how to handle" — per-cell optimal action

## 6. In Progress (Unfinished)
All tasks completed. O/U fully integrated.

## 7. Blocked / Waiting On
- Real Under odds from sportsbooks (derived odds only)
- Women's optimization (need 150+ bouts)
- Weight class field not populated in registry

## 8. Next Steps (Prioritized)
1. **Moicano vs Duncan (April 5)** — fight_week_scraper.py, verify odds
2. **Full optimizer run** — 550-bout dataset with O/U interactions
3. **Weight-class O/U** — populate weight_class, test per-division thresholds
4. **Temporal DEC rate cache** — O/U uses non-temporal career stats (leakage risk)
5. **Real O/U odds scraping** — live Under lines for upcoming events

## 9. Agent Observations
### Recommendations
- DEC rate dominates O/U signal. All other stats add near-zero incremental. Don't re-test.
- Algorithm at diminishing returns on O/U tuning. Future gains from real odds or structural changes.
- Work on main branch directly for algorithm changes — worktree causes Python file divergence.

### Data Contradictions Detected
- O/U P/L varies ±5u by pipeline order. Always rerun from clean O/U state.
- Derived Under odds at +1900 (Chiesa) were math-correct but market-unrealistic. ±400 cap resolves.

### Where I Fell Short
- 30 min debugging worktree file divergence. Should check __file__ immediately.
- Shipped DEC+Under conflict then reverted. Should do ROI analysis first.

## 10. Miscommunications
- User correctly identified DEC+Under as contradictory. Resolved by dropping DEC method bet.
- User caught +19u payout as impossible. Led to ±400 odds cap.

## 11. Files Changed
35 commits. Key files: UFC_Alg_v4_fast_2026.py, fix_registry_placed_flags.py, 10 frontend components, sync_and_deploy.py, track_results.py, ufc_ou_odds_cache.json, CLAUDE.md, EXPERIMENT_LOG.md.

## 12. Current State
- **Branch**: main
- **Last commit**: 2965a74 (2026-04-03 14:21:51)
- **Build**: Passes (1.7s)
- **Deploy**: Live via GitHub CI
- **Uncommitted**: None
- **Local = Remote**: Yes

## 13. Environment
- **Node.js**: v25.x
- **Python**: 3.9.6
- **Dev servers**: None

## 14. Session Metrics
- **Duration**: ~6 hours
- **Tasks**: 15+ completed / 20+ attempted
- **User corrections**: 4
- **Commits**: 35+
- **Skills used**: mmalogic, backtest, whats-next, full-handoff

## 15. Memory Updates
- CLAUDE.md: Baseline v11.21.1, O/U decision tree, 5 bet types
- EXPERIMENT_LOG.md: 11 experiments + O/U reference section

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| mmalogic | Site edits | Yes |
| backtest | Pre-compute screening | Yes |
| whats-next | Session planning | Yes |
| full-handoff | This handoff | Yes |

## 17. For The Next Agent
1. This handoff
2. CLAUDE.md (updated baseline + O/U decision tree)
3. backtest_runs/EXPERIMENT_LOG.md (O/U reference section)
4. ~/.claude/anti-patterns.md
5. fix_registry_placed_flags.py (O/U logic, lines 371-470)

**Canonical local path: ~/ProjectsHQ/mmalogic/**

**Current baseline: +759.20u** (71 events, v11.21.1)

| Stream | P/L | Record |
|--------|-----|--------|
| ML | +93.84u | 375W-145L |
| Method | +162.87u | 153W-163L |
| Combo | +93.26u | 31W-60L |
| O/U (Over) | +107.50u | 222W-59L |
| O/U (Under) | +74.34u | 103W-54L |
| Parlays | +227.39u | HC2+ROI2+HC3+ROI3 |
| **Combined** | **+759.20u** | |

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
1. GATE 1: Check ~/Projects/site-to-repo-map.json
2. GATE 2: git fetch && compare SHAs
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md

**Canonical path: ~/ProjectsHQ/mmalogic/**
**Last verified commit: 2965a74 on 2026-04-03 14:21:51**
