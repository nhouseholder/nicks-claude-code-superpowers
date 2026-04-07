# Handoff — MMALogic (UFC Predict) — 2026-03-26 21:43
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_ufc-predict_2026-03-26_0100.md
## GitHub repo: nhouseholder/ufc-predict
## Local path: ~/Projects/mmalogic/
## Last commit date: 2026-03-26 16:15:26 -0700

---

## 1. Session Summary
Massive session covering 4 major areas: (1) Built and deployed automatic live result tracking via Cloudflare Worker cron, (2) Fixed the Evloev vs Murphy event table — Duncan DEC tiebreaker, parlay legs, prop odds mapping, (3) Added parlay rows and American odds format to all event tables, (4) Conducted DEC tiebreak sweep analysis and updated the /mmalogic command with rules from 4 prior sessions. Site is deployed and verified at v11.9.5.

## 2. What Was Done
- **Live tracking Worker**: Created `workers/live-tracker/` — Cloudflare Worker cron that polls UFCStats during fight windows, scrapes results, scores all 4 bet types, updates Firestore `live_events/{slug}`. Deployed and tested. Commit 15c6a9a.
- **Duncan DEC tiebreaker fix**: Prediction archive showed DEC (tiebreaker fired at gap=0.016 < 0.04), but backtester produced KO. Fixed to match prediction archive. Commit cf5edc9.
- **Duncan DEC odds fix**: BFO f1/f2 mapping was swapped — +850 was Dolidze's DEC, not Duncan's. Fixed to +155. Commit 9cca405.
- **Parlay legs fix**: HC parlay was Murphy+Page (wrong — Murphy was underdog). Fixed to Duncan+Page (top 2 favorites). Commit cf5edc9.
- **Parlay rows in tables**: Added HC/ROI Parlay rows to EventSlideshow and LastWeekPicks. Commits 7b15b57, f9c7a92.
- **American odds format**: All odds now display American format. Added `decimalToAmerican()`. Permanent rule. Commit 46394b5.
- **DEC tiebreak sweep**: All thresholds 0.00-0.12 identical — vectorized path normalizes differently from prediction path.
- **/mmalogic command enrichment**: Added ~30 rules from 4 prior sessions across 5 GitHub syncs.

## 3. What Failed (And Why)
- **DEC tiebreak sweep**: All thresholds identical because vectorized backtest path normalizes KO/DEC/SUB scores. Lesson: scoring paths need alignment before tiebreak tuning.
- **Parallel sweep agents**: 4 agents clobbered the same registry file. Lesson: registry writes must be serialized.

## 4. What Worked Well
- Standalone test script (test.js) validated scoring against registry before deploying
- Cross-checking prediction_archive against backtester output to catch divergence
- Claude in Chrome for live site verification

## 5. What The User Wants
- "I'm so sick of having issues with this table on the front page" — tables must be correct with all 5 bet types and parlays
- "the european odds are confusing to me... we need to be using universal american odds, make that a permanent rule"
- "below christian leroy duncan fight should be a row with each parlay showing whether it won or lost"

## 6. In Progress (Unfinished)
- **DEC tiebreak scoring path alignment**: Vectorized path (line 11930-11960) normalizes differently from prediction path (line 6350-6358). Needs alignment so tiebreak tuning is possible.
- **O'Neill vs Fernandes ML odds**: Still missing from prediction_output.json.

## 7. Blocked / Waiting On
- O'Neill odds: waiting for BFO to list the fight

## 8. Next Steps (Prioritized)
1. **Post-event scoring (March 28)** — Run track_results.py Sunday. Live tracking Worker should auto-populate during the event.
2. **Align vectorized and prediction scoring paths** — Fix normalization difference so DEC_TIEBREAK fires in backtests.
3. **Mobile responsive pass** — HistoryPage and EventBetsDropdown force min-w-[820px] horizontal scroll
4. **Backend P1 fixes** — 8 CF functions with hardcoded admin email

## 9. Agent Observations
### Recommendations
- Live tracking Worker is the right architecture. Consider adding mid-week odds refresh cron.
- The /mmalogic command is ~490 lines — comprehensive but getting long. Consider splitting.
- Backtester scoring path divergence affects more than tiebreakers — any close-call method prediction could differ.

### Where I Fell Short
- Initially set Duncan DEC odds to +850 (wrong f1/f2 mapping). Should have cross-checked against ML odds.
- Parallel sweep wasted tokens — agents clobbered the same file.

## 10. Miscommunications
- User corrected Duncan DEC odds (+155, not +850) — should have validated prop odds against ML odds reasonableness
- User explained parlay P/L is correct at +0.90u (profit, not total return)

## 11. Files Changed
6 commits (15c6a9a → 46394b5), key files:

| File | Action | Why |
|------|--------|-----|
| workers/live-tracker/src/index.js | Created | Live tracking Worker |
| workers/live-tracker/src/test.js | Created | Test script |
| workers/live-tracker/wrangler.toml | Created | Worker cron config |
| workers/live-tracker/package.json | Created | Worker package |
| ufc_profit_registry.json | Modified | Duncan DEC fix, parlay legs fix |
| webapp/frontend/public/data/ufc_profit_registry.json | Modified | Same fixes synced |
| webapp/frontend/src/components/landing/EventSlideshow.jsx | Modified | Parlay rows, American odds |
| webapp/frontend/src/components/landing/LastWeekPicks.jsx | Modified | Parlay rows, American odds |
| webapp/frontend/src/lib/registryData.js | Modified | Pass parlay_roi |

## 12. Current State
- **Branch**: main
- **Last commit**: 46394b5 Display parlay odds in American format, not decimal (2026-03-26 16:15:26 -0700)
- **Build**: Passing
- **Deploy**: Live on mmalogic.com via Cloudflare Pages
- **Uncommitted changes**: algorithm_stats.json, backtest_summary.json, prediction_cache, _audit/, analysis script, 4 backup files
- **Local SHA matches remote**: Yes (46394b5)
- **Version**: v11.9.5

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: Preview server may be running on port 5199

## 14. Session Metrics
- **Duration**: ~4 hours
- **Tasks**: 10/11 (DEC tiebreak alignment deferred)
- **User corrections**: 3
- **Commits**: 6
- **Skills used**: /review-handoff, /mmalogic

## 15. Memory Updates
- Project memory: 3 new feedback files + MEMORY.md index
- anti-patterns.md: BACKTESTER_OVERWRITES_LIVE_PREDICTION
- /mmalogic command: ~30 rules from 4 prior sessions (5 GitHub syncs)

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| /review-handoff | Orient to prior session | Yes |
| /mmalogic | Load UFC domain knowledge | Yes |

## 17. For The Next Agent
Read these files first:
1. This handoff
2. ~/.claude/commands/mmalogic.md (490-line domain knowledge)
3. ~/.claude/anti-patterns.md (UFC entries)
4. CLAUDE.md (project-level)
5. ~/.claude/memory/topics/ufc_betting_model_spec.md (12 scoring rules)

**Canonical local path: ~/Projects/mmalogic/**

### Live Tracking Worker
- URL: https://mmalogic-live-tracker.nikhouseholdr.workers.dev
- Manual trigger: `curl -X POST <url>`
- Secret: FIREBASE_SA_KEY configured

### Upcoming Event
**UFC Fight Night: Adesanya vs. Pyfer — March 28, 2026**
- Live tracking Worker will auto-populate during fight night

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json
2. GATE 2: git fetch && compare local SHA to remote
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md

**Canonical path: ~/Projects/mmalogic/**
**Last verified commit: 46394b5 on 2026-03-26 16:15:26 -0700**
