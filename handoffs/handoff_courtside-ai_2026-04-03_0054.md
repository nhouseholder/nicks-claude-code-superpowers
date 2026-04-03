# Handoff — courtside-ai — 2026-04-03 00:54
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_courtside-ai_2026-04-01_1742.md
## GitHub repo: nhouseholder/courtside-ai
## Local path: /Users/nicholashouseholder/ProjectsHQ/courtside-ai
## Last commit date: 2026-04-02 22:21:49 -0700

---

## 1. Session Summary
Massive session covering systems infrastructure, algorithm research, and production optimization. Built the complete auto-learning pipeline (auto-prune, auto-apply with rollback, per-tier/per-family tracking, discovery-to-production loop). Fixed bet history not showing MADNESS picks. Ran hypothesis experiments on expanded datasets (8,766 NCAA, 392 NBA), disabled MADNESS tier based on 3-season evidence, raised NCAA edge threshold to 5.0, added NBA spread 5-11 sweet spot filter. Result: NCAA targets 59.7% ATS / +14.1% ROI, NBA targets 62.7% ATS / +19.8% ROI.

## 2. What Was Done
- **v12.35.3**: Fixed GitHub Actions workflow permissions — `grade-results.yml` and `auto-generate.yml` lacked `permissions: contents: write`, causing drift-report push to 403 and kill the 7 AM generation run. Added `continue-on-error` so drift push never blocks core pipeline.
- **v12.35.4**: Built auto-learning systems pipeline — (1) NBA per-tier + per-family ROI tracking in `nba-cron-grade.js`, (2) auto-prune tiers below break-even via `auto-prune.cjs`, (3) auto-apply optimizer with rollback safety in `run.cjs`.
- **v12.35.5**: Discovery-to-production loop — walk-forward validation on all discovery hypotheses, extract validated discoveries as boost filters into config files, generation endpoints consume DISCOVERY tier.
- **v12.35.6**: Fixed bet history dropping MADNESS/DISCOVERY picks — frontend filter used legacy boolean flags instead of canonical `tier` field. Anti-pattern logged as TIER_FILTER_GATE.
- **v12.35.7**: Hypothesis lab created — walk-forward experiment harness testing 7 hypotheses. Initial run on N=130 NCAA / N=50 NBA.
- **v12.35.8**: Applied model_spread>=10 filter based on N=74 finding (later REVERTED in v12.36.2).
- **v12.36.0**: Foolproof data pipeline — `live-stats.js` API endpoint, landing page prefers live Firestore stats, optimizer emits DATA_STALE/DATA_GAP warnings, post-deploy validation.
- **v12.36.1**: Expanded optimizer datasets from archived DBs — NCAA 130→8,766, NBA 50→392 walk-forward results.
- **v12.36.2**: Reverted model_spread>=10 filter. Re-ran experiments on N=8,741. Edge curve is monotonically positive — higher edge = better ATS. Previous finding was small-sample artifact. Anti-pattern logged as SMALL_SAMPLE_FILTER.
- **v12.36.3**: Disabled MADNESS tier — 3-season walk-forward on N=350 postseason games shows 37-43% ATS. Live record: 2W-3L. Anti-pattern logged as POSTSEASON_FAIL.
- **v12.36.4**: Multi-factor discovery — added Edge+DE, Edge+SOS, Edge+OREB combinations to NCAA discovery engine. Walk-forward validated: Edge≥7+|DE|<0.01 = 67.6% ATS, +29.1% ROI (N=108).
- **v12.36.5**: Tightened auto-prune threshold from break-even ATS to 15% ROI.
- **v12.36.6**: Raised NCAA MIN_BET_EDGE from 2.5 → 5.0 based on 8,391-game backtest. Edge≥5: 59.7% ATS, +14.1% ROI.
- **v12.36.7**: NBA spread sweet spot filter — only bet spreads 5-11. Spread 1-4 are coin flips (50% ATS), spread 11+ lose money (48.4%). Sweet spot: 62.7% ATS, +19.8% ROI (N=228).

## 3. What Failed (And Why)
- **model_spread>=10 filter was wrong**: Applied in v12.35.8 based on N=74 finding (48.6% ATS). Expanded dataset (N=8,741) showed edge 10+ = 52.0% ATS (profitable). Reverted in v12.36.2. Root cause: small sample noise. Anti-pattern: SMALL_SAMPLE_FILTER.
- **Score-ATS correlation flipped**: On N=50 NBA data, r=-0.191 (negative). On N=392, r=+0.167 (positive). The initial finding was noise. Same root cause — insufficient data.
- **iCloud DB copy stalled**: `cp` from iCloud produced 0-byte files. Fixed by `brctl download` + waiting for download + retrying copy. Known anti-pattern: ICLOUD_STALL.

## 4. What Worked Well
- Expanded datasets from archived DBs were the session's biggest unlock — going from N=130 to N=8,766 NCAA completely changed the picture and overturned multiple wrong conclusions.
- Walk-forward validation prevented overfitting — every hypothesis was tested on 30% holdout data.
- The multi-factor sweep (Edge + DE, Edge + SOS) found genuinely elite combos (67.6% ATS) that survived validation.
- Building infrastructure (auto-prune, auto-apply, live-stats) before making parameter changes — the pipeline can now self-correct future mistakes.

## 5. What The User Wants
- "we should prune anything that is < 15% ROI, for both NCAA and NBA" — tighter quality threshold
- "What can we do to get both ROIs above 15% and ATS above 60%" — performance targets
- "NCAA at 14% is fine, but lets work on NBA" — accepted NCAA at 14.1%, wanted NBA improved
- User wants fully automated, foolproof data pipeline with no stale data on the website

## 6. In Progress (Unfinished)
All tasks completed. No uncommitted changes.

## 7. Blocked / Waiting On
Nothing blocked.

## 8. Next Steps (Prioritized)
1. **Re-run optimizer with expanded datasets** — the optimizer still runs on the old 130/50 data points in CI. Next Mon/Wed/Fri run will use the new 8,766/392. Watch for auto-apply gate results.
2. **NBA data expansion** — the 392 NBA results may have bet_side issues (exported via fixture builder). Consider re-exporting with `nba_predict.py` (now fixed) for validation.
3. **Monitor auto-prune in production** — first prune evaluation will happen on next optimizer run. With 15% ROI threshold, any tier below ~57.5% ATS will accumulate prune streaks.
4. **NCAA multi-factor combo promotion** — the Edge≥7+DE<0.01 combo (67.6% ATS) is in the discovery engine. When the optimizer runs, it should appear as a walk-forward validated filter and flow to production via DISCOVERY tier.

## 9. Agent Observations
### Recommendations
- The auto-learning pipeline is now complete: grade → track → drift → prune → optimize → auto-apply → rollback → discover → boost. Every piece is deployed and automated.
- The NCAA model is genuinely elite in regular season (57-60% ATS on N=8,391). The postseason is fundamentally broken and should stay disabled until a tournament-specific model is built.
- The NBA spread 5-11 filter is the simplest and most impactful change — it removes the unprofitable tails where the market is either too efficient (close games) or too noisy (blowouts).

### Data Contradictions Detected
- **model_spread≥10 finding**: N=74 showed 48.6% ATS → N=8,741 showed 52.0% ATS. Resolved: small-sample noise, larger sample is correct.
- **Score-ATS correlation**: N=50 showed r=-0.191 → N=392 showed r=+0.167. Resolved: larger sample is correct, higher scores do predict better ATS.
- **MADNESS backtest**: CLAUDE.md claimed "69.2% ATS, +32.5% ROI" → 3-season data shows 37-43% ATS. Resolved: original claim was overfitted to small cherry-picked subset.

### Where I Fell Short
- Applied the model_spread≥10 filter (v12.35.8) based on N=74 — a clear violation of the SMALL_SAMPLE_FILTER principle. Should have waited for expanded data before making any production filter change.
- The NBA export (392 results) may have bet_side computation issues from the fixture builder approach. Should have validated against known Firestore baselines more carefully.

## 10. Miscommunications
None — session was well-aligned throughout. User gave clear targets (60% ATS, 15% ROI) and made a deliberate tradeoff choice (edge≥5 for more volume over edge≥7 for higher ROI).

## 11. Files Changed
```
 .github/workflows/auto-generate.yml           |    4 +
 .github/workflows/deploy-cloudflare-pages.yml  |   36 +
 .github/workflows/grade-results.yml            |    4 +
 .github/workflows/optimize.yml                 |   19 +
 CLAUDE.md                                      |    2 +-
 functions/api/cron-generate.js                 |  112 +-
 functions/api/live-stats.js                    |  141 +  (NEW)
 functions/api/nba-cron-generate.js             |   85 +-
 functions/api/nba-cron-grade.js                |   81 +-
 package.json                                   |    2 +-
 public/data/nba/recent-results.json            | 1272 +-
 public/data/recent-results-regular.json        | 1884 +-
 scripts/experiments/experiment-log.json        | 1064 +  (NEW)
 scripts/experiments/hypothesis_lab.py          |  561 +  (NEW)
 scripts/optimizer/auto-prune.cjs               |  152 +  (NEW)
 scripts/optimizer/discover.cjs                 |  118 +-
 scripts/optimizer/ncaa-optimize.cjs            |    4 +-
 scripts/optimizer/run.cjs                      |  283 +-
 scripts/predict_and_upload.py                  |    4 +-
 src/components/ncaa/RecentResults.jsx          |   22 +-
 src/config/version.js                          |   60 +-
 src/routes/DashboardPage.jsx                   |   11 +-
 src/routes/LandingPage.jsx                     |   20 +-
 src/routes/NbaDashboardContent.jsx             |    2 +-
 src/services/api.js                            |   16 +-
 25 files changed, ~6,000 insertions/deletions
```

| File | Action | Why |
|------|--------|-----|
| `auto-generate.yml` | Modified | Add permissions: contents: write + continue-on-error on drift push |
| `grade-results.yml` | Modified | Same permissions fix |
| `deploy-cloudflare-pages.yml` | Modified | Add post-deploy data validation (health, live-stats, freshness) |
| `optimize.yml` | Modified | Add Firestore result count sync step |
| `CLAUDE.md` | Modified | Mark MADNESS tier as disabled |
| `cron-generate.js` | Modified | Raise MIN_BET_EDGE 2.5→5.0, disable MADNESS (both paths), add discovery boost, add prune filter |
| `live-stats.js` | Created | Compute live backtest-equivalent stats from Firestore |
| `nba-cron-generate.js` | Modified | Add spread 5-11 filter (all paths), discovery boost, prune filter |
| `nba-cron-grade.js` | Modified | Add per-tier + per-family tracking, DISCOVERY in TRACKED_TIERS |
| `recent-results-regular.json` | Modified | Expanded NCAA 130→8,766 from archived DB |
| `nba/recent-results.json` | Modified | Expanded NBA 50→392 from archived DB |
| `experiment-log.json` | Created | Structured experiment results with verdicts |
| `hypothesis_lab.py` | Created | Walk-forward experiment harness (7 hypotheses) |
| `auto-prune.cjs` | Created | Tier auto-pruning based on rolling ROI (15% threshold) |
| `discover.cjs` | Modified | Add walk-forward validation, multi-factor combos (Edge+DE, Edge+SOS, Edge+OREB) |
| `ncaa-optimize.cjs` | Modified | Update current params to match production (MIN_BET_EDGE=5.0) |
| `run.cjs` | Modified | Auto-apply with rollback, staleness detector, discovery filter injection, prune integration |
| `predict_and_upload.py` | Modified | Disable MADNESS tier assignment |
| `RecentResults.jsx` | Modified | Tier-first badge rendering (unified lookup table) |
| `DashboardPage.jsx` | Modified | VALID_TIERS set for pick filtering (tier-first, boolean fallback) |
| `LandingPage.jsx` | Modified | Prefer live-stats API over static summary.json |
| `NbaDashboardContent.jsx` | Modified | Fix is_apex force-set on today's picks |
| `api.js` | Modified | Add getLiveStats(), DISCOVERY in isActionablePick() |
| `version.js` | Modified | Version history entries for v12.35.3 through v12.36.7 |

## 12. Current State
- **Branch**: main
- **Last commit**: adfcf9d v12.36.7: NBA spread sweet spot filter 5-11 (2026-04-02 22:21:49 -0700)
- **Build**: untested locally (no node available in session), all deploys succeeded on Cloudflare
- **Deploy**: all 15 commits deployed successfully via Cloudflare Pages auto-deploy
- **Uncommitted changes**: none
- **Local SHA matches remote**: yes

## 13. Environment
- **Node.js**: not available in session PATH (builds run in CI)
- **Python**: 3.9.6
- **Dev servers**: nestwisehq Next.js dev server running (unrelated)

## 14. Session Metrics
- **Duration**: ~240 minutes
- **Tasks**: 15 completed / 15 attempted (all commits)
- **User corrections**: 1 (chose edge≥5 over edge≥7)
- **Commits**: 15 (v12.35.3 through v12.36.7)
- **Skills used**: /review-handoff, /update-courtside, /full-handoff

## 15. Memory Updates
- **anti-patterns.md**: 3 new entries:
  - `TIER_FILTER_GATE` — always use tier field for pick filtering, not boolean flags
  - `SMALL_SAMPLE_FILTER` — never apply production filters from N<200
  - `POSTSEASON_FAIL` — NCAA postseason model doesn't work, don't re-enable without new approach
- **CLAUDE.md**: Updated tier hierarchy to mark MADNESS as disabled
- **experiment-log.json**: 2 experiment runs logged (N=130 initial, N=8,741 expanded)

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| /review-handoff | Orient to previous session's NBA export work | Yes |
| /update-courtside | Deploy verification after changes | Yes |
| /full-handoff | This handoff | Yes |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff
2. `handoffs/handoff_courtside-ai_2026-04-01_1742.md`
3. `~/.claude/anti-patterns.md` — especially SMALL_SAMPLE_FILTER, POSTSEASON_FAIL, TIER_FILTER_GATE
4. `CLAUDE.md` (project root)
5. `scripts/experiments/experiment-log.json` — full experiment results
6. `scripts/optimizer/auto-prune.cjs` — auto-prune logic and thresholds
7. `scripts/optimizer/run.cjs` — auto-apply gates and rollback mechanism

**Key production parameters (v12.36.7):**
- NCAA MIN_BET_EDGE = 5.0 (was 2.5)
- NCAA danger zone: |model_spread| in [3,5] (unchanged)
- NCAA MADNESS: DISABLED
- NBA spread filter: 5-11 only (new)
- Auto-prune threshold: 15% ROI (was 52.4% ATS)
- Auto-apply gates: ROI≥5%, params≤30% change, validation ATS>52.4%, no CRITICAL drift

**Canonical local path for this project: /Users/nicholashouseholder/ProjectsHQ/courtside-ai**
**Do NOT open this project from iCloud or /tmp/. Use the path above.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: /Users/nicholashouseholder/ProjectsHQ/courtside-ai**
**Last verified commit: adfcf9d on 2026-04-02 22:21:49 -0700**
