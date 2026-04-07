# Handoff — Diamond Predictions — 2026-04-03 16:05
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_diamond-predictions_2026-04-03_0054.md
## GitHub repo: nhouseholder/diamond-predictions
## Local path: ~/ProjectsHQ/diamondpredictions/
## Last commit date: 2026-04-03 15:50:41 -0700

---

## 1. Session Summary
Massive NHL optimization session. Tested 4 hypotheses (H1-H4), shipped edge cap 0.10 (+12pp ROI), zeroed 7 noise weights (overfit reduction), and skipped DIAMOND tier (+8.5pp ROI). Combined: +21.3pp ROI improvement over v10 baseline. Also verified MLB de-vig fix improved backtest from 18.0% to 28.2% ROI, updated homepage stats, and aligned NHL playoff params. Deployed v13.6.0.

## 2. What Was Done
- **H1-H4 hypothesis testing**: Ran 14 walk-forward backtests. H1 (score-adjusted Corsi), H3 (consecutive road games), H4 (one-goal W%) all rejected — no improvement. H2 (edge cap 0.10) shipped: +12.1pp ROI, +2.3pp WR, halves fold degradation.
- **Zero 7 noise weights**: Zeroed pyth_wpct, xgf_pct, b2b_fatigue, recent_form_7, sos, rest_advantage, playoff_race in WP_FEATURE_WEIGHTS. Fold 3 OOS improved 67.0% → 72.0% ROI. Effective params reduced 48 → 41.
- **Skip DIAMOND tier**: Added SKIP_DIAMOND=true to params + 3 lines in conglomerate.py. DIAMOND was 44% WR (+50.8% ROI) vs PLATINUM 56% WR (+84.9%). Removing it: +8.5pp portfolio ROI.
- **MLB de-vig backtest verification**: Re-ran 3-season walk-forward. ROI improved 18.0% → 28.2% (+10.2pp). 784 picks vs old 827 (43 phantom-edge picks removed).
- **MLB homepage stats regeneration**: Updated homepage-stats.json with corrected numbers, profit curve, tier breakdown.
- **NHL playoff params alignment**: Zeroed same 5 noise weights in playoff_params_v1.json. 10/22 WP features now zeroed in playoff mode.
- **Version bump to v13.6.0**: Updated VERSION, version.js, version.json.
- **Verified no NHL/MLB picks today**: Manually ran algorithm on 2 NHL games — both below edge threshold. PHI@NYI: 1.24% edge (min 1.7%). STL@ANA: 1.99% edge (min 4.98% after April 1.2x scaling).
- **Objective algorithm assessment**: Graded NHL (B+) and MLB (C+) across 10+ dimensions with concrete data.
- **MLB WinProb gate test**: Attempted stat model directional gate on SILVER picks — no effect (stat model doesn't cover SILVER games). Reverted.

## 3. What Failed (And Why)
- **H1 score-adjusted Corsi**: All weights degraded ROI (-0.7pp best case). Already captured by hdcf_pct_delta.
- **H3 consecutive road games**: All weights degraded ROI (-1.5pp best case). Redundant with rest_days + travel_fatigue features.
- **H4 one-goal win %**: Matched baseline at best (+0.30 weight: 63.5% vs 63.6%). Signal too weak.
- **MLB WinProb directional gate on SILVER picks**: Zero effect — stat model has no predictions for games where SILVER picks fire (no overlap between stat model coverage and systems-only picks).
- **Worktree bash-guard conflict**: Session ran in git worktree, bash-guard hook blocked all git push commands. Required user to run push commands manually from canonical directory.

## 4. What Worked Well
- Pre-compute gating before backtests saved time
- Fold stability analysis (degradation comparison) more informative than aggregate ROI
- Incremental testing: baseline → edge cap → zero weights → DIAMOND skip, each verified independently
- Live data validation: edge cap 0.10 confirmed by live 2025-26 data (2 bets >10% edge were both losses)

## 5. What The User Wants
- "proceed with queue items" — systematic execution of prioritized improvements
- "objectively assess our algorithm for NHL and MLB and grade them across each subaspect" — honest, data-backed assessment
- "ensure each change adds ROI historically in the backtestor before implementing" — no changes without backtest validation
- Flat 1-unit bets, improvements from pick quality not sizing

## 6. In Progress (Unfinished)
All tasks completed.

## 7. Blocked / Waiting On
- **NHL CLV tracking**: Only 1/689 bets have CLV data. Needs grading cycles to accumulate.
- **MLB conglomerate**: Produces 0 picks in production. All live volume from SILVER (systems-only) bets. Stat model directional gate tested — doesn't help (no overlap).

## 8. Next Steps (Prioritized)
1. **CMA-ES re-optimization with pruned feature set** — 15 active weights on cleaner search space. Highest ceiling improvement. ~3-4 hours compute.
2. **Wire 4 profitable MLB COMBO systems into production** — Public Overreaction (+32.6%), Steam Reversal (+15.8%), Travel Sharp (+10.4%), Rest Advantage Sharp (+9.4%). Currently backtest-only.
3. **Re-evaluate pruned MLB systems with de-vig fix** — 41/54 systems PRUNED with bugged ROI. Some may recover.
4. **Fix cross-sport contamination in MLB odds cache** — NHL game IDs leaking into MLB odds_cache.json.
5. **Fix generate_webapp_data.py Python 3.9 compatibility** — Uses `dict | list` type hints (3.10+). Add `from __future__ import annotations`.
6. **Test H9 (division/conference features) for NHL** — Untested hypothesis from experiment log.

## 9. Agent Observations
### Recommendations
- Edge cap 0.10 is the most impactful change — reduces overfitting fundamentally by removing picks where the model is miscalibrated.
- DIAMOND skip removes profitable picks (+50.8% ROI) but improves portfolio quality. CMA-ES re-optimization might find a way to make DIAMOND work by re-tuning agreement's effect on probability.
- MLB's biggest structural problem: conglomerate never fires in production. Entire output is SILVER (systems-only) with no ML filter.
- generate_webapp_data.py failing on Python 3.9 means homepage stats can only be updated manually.

### Data Contradictions Detected
- MLB homepage showed 18.0% ROI while corrected backtest shows 28.2%. Now fixed.

### Where I Fell Short
- MLB WinProb gate was structurally impossible — could have detected by checking stat_picks_generated (282) vs sys_picks_generated (3424) ratio.
- Worktree bash-guard conflict required multiple user interventions for push.

## 10. Miscommunications
None — session aligned.

## 11. Files Changed
| File | Action | Why |
|------|--------|-----|
| `nhl_data/optimized_params_v10.json` | Modified | Edge cap 0.10, zero 7 weights, SKIP_DIAMOND |
| `data/optimized_params_v10.json` | Modified | Mirror of above |
| `nhl_predict/algorithms/conglomerate.py` | Modified | SKIP_DIAMOND logic (3 lines) |
| `nhl_predict/algorithms/winprob.py` | Modified | Added 3 candidate features (H1/H3/H4 — weight=0) |
| `nhl_data/playoff_params_v1.json` | Modified | Zeroed 5 noise weights for playoff consistency |
| `mlb_predict/webapp/frontend/public/data/homepage-stats.json` | Modified | De-vig corrected stats |
| `EXPERIMENT_LOG.md` | Modified | Added 7 new experiment entries |
| `nhl_data/h1_h4_experiment_results.json` | Created | H1-H4 raw backtest results |
| `scripts/nhl/test_h1_h4.py` | Created | Reusable hypothesis testing script |
| `VERSION` | Modified | 13.5.4 → 13.6.0 |
| `mlb_predict/webapp/frontend/src/version.js` | Modified | 13.6.0 |
| `mlb_predict/webapp/frontend/public/data/version.json` | Modified | 13.6.0 |

## 12. Current State
- **Branch**: main
- **Last commit**: fad8687 Merge branch 'claude/gallant-bell' (2026-04-03 15:50:41 -0700)
- **Build**: untested locally (CI/CD builds on GitHub Actions)
- **Deploy**: v13.6.0 deployed to Cloudflare Pages (auto-triggered by push)
- **Uncommitted changes**: none (clean)
- **Local SHA matches remote**: yes (fad8687)

## 13. Environment
- **Node.js**: N/A (CI uses v22)
- **Python**: 3.9.6 (local), 3.11 (CI)
- **Dev servers**: none

## 14. Session Metrics
- **Duration**: ~300 minutes
- **Tasks**: 12/13 completed (MLB WinProb gate attempted but reverted)
- **User corrections**: 0
- **Commits**: 5 (3c6802c, 21298d7, 8487c88, 2ef75f4, fad8687)
- **Skills used**: /review-handoff, /whats-next (2x), /full-handoff

## 15. Memory Updates
- No anti-patterns logged
- EXPERIMENT_LOG.md updated with 7 new entries (H1-H4, zero weights, DIAMOND skip, MLB de-vig verification)
- 45 total experiments now documented

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| /review-handoff | Session orientation | Yes |
| /whats-next | Generate recommendations (2x) | Yes |
| /full-handoff | This handoff | Yes |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff (HANDOFF.md)
2. EXPERIMENT_LOG.md — 45 experiments documented, 7 added this session
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
**Last verified commit: fad8687 on 2026-04-03 15:50:41 -0700**
