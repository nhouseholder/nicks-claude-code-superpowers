# Handoff — courtside-ai — 2026-04-03 18:30
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_courtside-ai_2026-04-03_0054.md
## GitHub repo: nhouseholder/courtside-ai
## Local path: /Users/nicholashouseholder/ProjectsHQ/courtside-ai
## Last commit date: 2026-04-03 18:24:22 -0700

---

## 1. Session Summary
Massive algorithm revision session. Audited both NCAA and NBA algorithms, discovered NCAA Elo-Signal is break-even (50% ATS), disabled it, restored the ML pipeline from iCloud archive, reversed the NCAA spread gate (spread<10 instead of ≥7 = +8% ATS), retrained P(cover) v3, added NBA rest filter, built 10 named NCAA situational betting systems (MLB-style), created a Systems page, and deployed everything. 16 commits, v12.37.0 → v12.39.2.

## 2. What Was Done
- **v12.37.1**: NBA spread filter 5-11 → 3-11 — fixed 4-day blackout
- **v12.37.2**: Filtered SELECT/UNSCORED from stats (NCAA 42.5%→45.8%, NBA 60.8%→64.4%)
- **v12.37.3**: Cleanup/rebuild endpoints. ML pipeline restored from iCloud. launchd installed. Python deps installed.
- **v12.37.4**: Drift throttle bypass when optimizer applied. Drift baselines fixed.
- **v12.37.5**: REVERTED Elo params. Elo-Signal backtest proof: 50-51% ATS (N=2,121). Dead.
- **v12.38.0**: DISABLED Elo-Signal entirely. ML pipeline or nothing.
- **v12.39.0**: ALGORITHM REVISION — spread gate reversed, MIN_BET_EDGE 5→7, P(cover) v3 (35 features), NBA rest filter. NCAA test: 63.3%, NBA test: 63.2%.
- **v12.39.1**: Systems page (/systems) with walk-forward tables.
- **v12.39.2**: NCAA Situational Systems Engine — 10 named systems, 3+ convergence = 65.6% ATS. Integrated into pipeline.
- **Infrastructure**: Purged 41 toxic picks, rebuilt season_performance, updated experiment log (4 entries).

## 3. What Failed (And Why)
- **v12.37.0 optimizer params wrong**: Applied ML-optimized params to Elo-Signal. Backtest proved Elo-Signal = 50% regardless. Reverted v12.37.5.
- **AGREE_TIER=8 test**: N=7. Violated SMALL_SAMPLE_FILTER. Skipped.

## 4. What Worked Well
- Elo-Signal backtest was definitive (2,121 games). Spread gate reversal was the session's biggest discovery (close games = 70% ATS). MLB systems architecture ported cleanly to NCAA. P(cover) v3 independently confirmed spread reversal via dog_x_spread weight.

## 5. What The User Wants
- "we need to totally rework it until it can be 60% ATS minimum"
- "we should have NCAA and NBA betting systems" — MLB-style named situational systems
- "start with designing situational systems from backtest data"

## 6. In Progress (Unfinished)
All tasks completed. No uncommitted changes.

## 7. Blocked / Waiting On
- ML pipeline first run: launchd fires 8 AM ET 4/4. NCAA season effectively over.

## 8. Next Steps (Prioritized)
1. **Validate ML pipeline runs tomorrow** — check logs, verify Firestore predictions have ML features
2. **Build NBA situational systems engine** — same pattern as NCAA ncaa_systems.py
3. **Activate NBA playoff tiers** — PLAYOFF_AGREE/PLAYOFF_DEFENSE for April playoffs
4. **Add live per-system tracking to grading** — cron-grade.js tracks per-system W-L (like MLB tracker)
5. **System grade feedback loop** — live grades auto-update engine weights

## 9. Agent Observations
### Recommendations
- The spread gate reversal is the biggest find. Close games (0-5) with high ML edge are the model's sweet spot. This should be investigated for NBA too.
- NCAA systems engine needs live tracking — currently only backtest data shows on the Systems page.
- P(cover) v3's dog_x_spread feature provides independent confirmation of the spread reversal.

### Data Contradictions Detected
- Elo-Signal optimizer said K=20 was "better" (60.4% validation) but Elo-Signal-specific backtest showed 50.0%. Resolved: optimizer was testing wrong model's data.

### Where I Fell Short
- Applied optimizer params before verifying the optimizer targeted the right model (1 wasted commit).
- Didn't catch spread gate issue earlier — a simple bucket analysis would have found it months ago.

## 10. Miscommunications
- User asked for "systems" — initially built tier-level page. User clarified they meant MLB-style named situational systems. Corrected by studying Diamond Predictions architecture.

## 11. Files Changed
37 files changed, 5139 insertions(+), 1289 deletions(-)

Key files: cron-generate.js, generate-picks.js, nba-cron-generate.js, predict_and_upload.py, ncaa_systems.py (new), SystemsPage.jsx (new), systems.json (new), elo_signal_backtest.py (new), ALGORITHM_VERSION.md (new), pcover_weights.json (v3), live-stats.js, live-results.js, cron-grade.js, nba-cron-grade.js, summary.json, experiment-log.json

## 12. Current State
- **Branch**: claude/intelligent-pasteur (worktree), merged to main
- **Last commit**: ff3e070 (2026-04-03 18:24:22 -0700)
- **Build**: untested locally, all Cloudflare deploys succeeded
- **Deploy**: 16 commits deployed via auto-deploy
- **Uncommitted changes**: none
- **Local SHA matches remote**: yes

## 13. Environment
- **Node.js**: N/A in session
- **Python**: 3.9.6 + XGBoost 2.1.4, Pandas 2.3.3, scikit-learn 1.6.1
- **launchd**: com.courtside.daily-predict ACTIVE

## 14. Session Metrics
- **Duration**: ~300 minutes
- **Tasks**: 16 completed / 16 attempted
- **User corrections**: 2
- **Commits**: 16
- **Skills used**: /review-handoff, /whats-next (x2), /full-handoff

## 15. Memory Updates
- experiment-log.json: 4 new entries (SPREAD_GATE_REVERSAL, PCOVER_V3, NBA_REST_FILTER, ELO_SIGNAL_DEAD, NCAA_SYSTEMS_DISCOVERY)
- ALGORITHM_VERSION.md: new file
- CLAUDE.md: version updated

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| /review-handoff | Orient to previous session | Yes |
| /whats-next | Strategic recommendations (x2) | Yes |
| /full-handoff | This handoff | Yes |

## 17. For The Next Agent
Read these files first:
1. This handoff
2. `handoffs/handoff_courtside-ai_2026-04-03_0054.md`
3. `~/.claude/anti-patterns.md`
4. `CLAUDE.md` + `ALGORITHM_VERSION.md`
5. `scripts/ncaa_systems.py`
6. `scripts/experiments/experiment-log.json`

**Key params (v12.39.2):** NCAA edge 7-10, spread<10, P(cover) v3 (35 feat), Elo-Signal DISABLED, 10 named systems with convergence threshold 3.0. NBA spread 3-11, rest filter, AGREE≥5.

**Canonical local path: /Users/nicholashouseholder/ProjectsHQ/courtside-ai**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
1. GATE 1: Check ~/Projects/site-to-repo-map.json
2. GATE 2: git fetch && compare SHAs
3. GATE 3: Read this handoff + anti-patterns.md

**Last verified commit: ff3e070 on 2026-04-03 18:24:22 -0700**
