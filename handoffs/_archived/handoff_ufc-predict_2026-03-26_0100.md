# Handoff — MMALogic (UFC Predict) — 2026-03-26 01:00
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_ufc-predict_2026-03-25_1927.md
## GitHub repo: nhouseholder/ufc-predict
## Local path: ~/Projects/mmalogic/
## Last commit date: 2026-03-26 00:18:17 -0700

---

## 1. Session Summary
Massive session: full site audit (frontend + backend), followed by extensive data fixes. Fixed 10 P0 frontend issues, re-scored the entire 71-event registry via backtester, scraped missing prop odds from BFO, added Combo columns and Parlay rows across all table components, generated the 2nd parlay, verified the "Apply & Regenerate" pipeline works, and conducted detailed KO R2 routing and ML bracket profitability analyses. Planned (but didn't implement) automatic live tracking via Cloudflare Worker cron.

## 2. What Was Done
- **Site audit (P0 fixes)**: LiveFightCard/AdminPicks confidence % → diff, Scoreboard/AdminPerformance/AdminOverview/AdminBacktest/LastWeekPicks missing combo+parlay in combined P/L, ResultLogger FLAT_UNIT_PAYOUT fix, App.jsx 404 route, loss-protection.js try/catch — commit aa7fd64
- **safePnl logic fix**: EventBetsDropdown now returns -1u for losses regardless of odds availability (was exiting early on null odds) — commit 4a61d9b
- **EventSlideshow**: Grid expanded from 3 to 5 columns (added Combo + Parlay) — commit 4a61d9b
- **registryData.js**: computeLatestFightsFromRegistry now includes parlay data — commit 4a61d9b
- **Prop odds scrape**: Scraped 48 prop odds from BFO for Page vs Patterson and Duncan vs Dolidze (Evloev vs Murphy event) — commit 29d3624
- **Registry fixes**: Page method win +2.10u, Duncan method loss -1u, Vallejos round/combo gating nulled, Delgado round/combo -1u — commit 39f8878
- **Full backtest re-score**: 71-event cache-only backtest with correct R1 KO gating, SUB gating. Parlay totals aggregated from event-level data — commit c0294ac
- **2nd parlay generated**: Scraped Stirling (-440) and Simon (-158) ML odds from BFO UFC Seattle page. HC Parlay: Chiesa + Stirling. ROI Parlay: Simon + Barber — commit bf51a03
- **AdminBacktest overhaul**: Added Combo column, Parlay row, safePnl for losses, all 5 types in chart/totals — commit f09076a
- **"Apply & Regenerate" verification**: Confirmed full pipeline works (Firestore → GitHub Actions → algorithm → ingest)
- **KO R2 routing analysis**: Deterministic script (analysis_ko_r2_routing.py), R1 routing -40.4% ROI, DEC routing -1.1%, gating confirmed correct
- **ML bracket profitability**: All brackets profitable, -300 to -399 thinnest edge (+2.7%), -500+ strongest (+9.6%)
- **Permanent rules saved**: Never accept missing odds, always re-run backtester instead of manual patches, all tables must show 5 bet types, AdminBacktest must match EventBetsDropdown format

## 3. What Failed (And Why)
- **Cross-query data inconsistency**: KO R2 analysis ran 3 times with different name-matching logic, producing shifting numbers. User rightfully called it out. Lesson: always use a standalone script with assertions for data analysis, never ad-hoc queries.
- **Wholesale registry re-score**: Attempted to manually re-score all 507 bouts, changed totals dramatically (ML went from 83u to 112u). Restored from backup. Lesson: only the backtester should re-score — manual patches diverge from its logic.
- **BFO scraper import timeout**: Importing the full 9000-line algorithm just to call the scraper functions failed twice (stuck on initialization). Workaround: wrote standalone cloudscraper-based BFO scrape.

## 4. What Worked Well
- Running the actual backtester (`UFC_BACKTEST_MODE=1 UFC_CACHE_ONLY=1`) to fix all scoring issues at once instead of manual patches
- Standalone analysis scripts (analysis_ko_r2_routing.py) with assertions and full audit trails
- Direct BFO scraping via cloudscraper for targeted odds backfill
- Checking Cloudflare and GitHub secrets via CLI to verify pipeline configuration

## 5. What The User Wants
- **Data accuracy is #1**: "YOU MAY NEVER ACCEPT MISSING ODDS. NEVER. ALWAYS ACTIVATE ODDS SCRAPERS TO BACKFILL."
- **Tables must be complete**: Every event table must show all 5 bet types with correct +/- units per cell
- **Automatic live tracking**: Wants fight results to populate automatically during fight night without manual admin work
- **Cross-query consistency**: User brought in another AI to audit my numbers — expects reproducible, citable data

## 6. In Progress (Unfinished)
- **Automatic live tracking via Cloudflare Worker cron**: Plan approved at ~/.claude/plans/tingly-wobbling-stroustrup.md. Needs implementation: port UFCStats scraping to JS, set up Worker cron for Saturday nights, auto-update Firestore live_events doc. Must be working before March 28 fight night.
- **O'Neill vs Fernandes ML odds**: Still missing from prediction_output.json (not on BFO UFC Seattle page). Auto-refresh cron should catch it.

## 7. Blocked / Waiting On
- **O'Neill odds**: Waiting for BFO to list the fight (may be on a different event page)
- **Live tracking implementation**: Needs a fresh session with full token budget

## 8. Next Steps (Prioritized)
1. **Implement automatic live tracking** — Plan approved, must be working before March 28 fight night. Read ~/.claude/plans/tingly-wobbling-stroustrup.md
2. **Refresh O'Neill odds** — Check BFO again, update prediction_output.json if found
3. **Mobile responsive pass** — HistoryPage and EventBetsDropdown force min-w-[820px] horizontal scroll
4. **Remaining backend P1 fixes** — 8 CF functions with hardcoded admin email, timingSafeEqual length leak
5. **Post-event scoring (March 28)** — Run track_results.py Sunday after Adesanya vs Pyfer event

## 9. Agent Observations
### Recommendations
- The backtester's scoring of fighter-loss prop bets is inconsistent (leaves method_pnl/round_pnl as null instead of -1u for many bouts). This is by design in the current code but means the frontend must use safePnl to fill in losses. Consider fixing the backtester to always record -1u for placed-bet losses.
- The prop odds cache has 17-23 fights per event with __NO_PROPS__ — the scraper runs too early. Consider adding a mid-week re-scrape cron (Wednesday/Thursday) to catch newly-posted prelim odds.
- BFO event names don't match the algorithm's event names (e.g., "UFC Seattle" vs "UFC Fight Night: Adesanya vs. Pyfer"). The scraper's event-name matching needs improvement.

### Where I Fell Short
- Presented inconsistent numbers across 3 queries for the KO R2 analysis before being called out. Should have written a standalone script from the start.
- Accepted missing prop odds initially (displayed "—" instead of scraping). The permanent rule is now in place but the failure already wasted the user's time.
- Tried to manually patch the registry instead of re-running the backtester. The wholesale re-score produced wildly different numbers and had to be reverted.

## 10. Miscommunications
- User had to correct me multiple times about never accepting missing odds — this is now a permanent non-negotiable rule
- User brought in another AI to validate my data analysis numbers, which revealed cross-query inconsistency. Valid criticism, now addressed with standalone scripts.

## 11. Files Changed
31 files changed, 17982 insertions, 9507 deletions across 7 commits (aa7fd64 → f09076a)

| File | Action | Why |
|------|--------|-----|
| App.jsx | Modified | Added 404 catch-all route |
| EventBetsDropdown.jsx | Modified | safePnl: losses return -1u without odds |
| EventSlideshow.jsx | Modified | 5-column grid (added Combo + Parlay) |
| LastWeekPicks.jsx | Modified | Added combo+parlay to totals |
| LiveFightCard.jsx | Modified | Confidence % → diff format |
| AdminPicks.jsx | Modified | Confidence % → diff format |
| AdminBacktest.jsx | Modified | Full overhaul: Combo col, Parlay row, safePnl |
| AdminPerformance.jsx | Modified | Added combo+parlay to combined P/L |
| AdminOverview.jsx | Modified | Added parlay to combined P/L |
| Scoreboard.jsx | Modified | Added combo P/L tracking |
| ResultLogger.jsx | Modified | FLAT_UNIT_PAYOUT fix (null odds → null) |
| registryData.js | Modified | computeLatestFightsFromRegistry includes parlay |
| loss-protection.js | Modified | try/catch on Firebase JSON.parse |
| ufc_profit_registry.json | Modified | Full re-score from backtester |
| ufc_prop_odds_cache.json | Modified | Scraped Page/Duncan/Stirling/Simon odds |
| prediction_output.json | Modified | Added Stirling/Simon ML odds, 2nd parlay |

## 12. Current State
- **Branch**: main
- **Last commit**: f09076a AdminBacktest: add Combo column, Parlay row, safePnl for all bet types (2026-03-26 00:18:17 -0700)
- **Build**: Passing (verified in /tmp/octagonai-deploy)
- **Deploy**: Auto-deployed to mmalogic.com via Cloudflare Pages
- **Uncommitted changes**: handoff.md, prediction_cache update, _audit/ dir, analysis script, 2 backup files
- **Local SHA matches remote**: Yes (f09076a = f09076a)
- **Version**: v11.9.5

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: None for this project (other projects have servers running)

## 14. Session Metrics
- **Duration**: ~3 hours
- **Tasks**: 12/13 (live tracking planned but not implemented)
- **User corrections**: 3 (missing odds, inconsistent data, table errors)
- **Commits**: 7 (aa7fd64 → f09076a)
- **Skills used**: /full-handoff, /site-audit

## 15. Memory Updates
- **anti-patterns.md**: Added MISSING_ODDS_ACCEPTED_WITHOUT_SCRAPING permanent rule
- **ufc_website_maintenance_rules.md**: Added rules 20-29 (losses don't need odds, all 5 types in summaries, never accept missing odds, R1 KO gating in registry, always re-run backtester, parlays in tables, Apply & Regenerate works, AdminBacktest must match EventBetsDropdown)
- **analysis_ko_r2_routing.py**: Saved deterministic analysis script for future reference

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| /site-audit | Full 6-phase website audit | Yes — found 80 issues, fixed 10 P0 |
| /full-handoff | Session handoff | Yes |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff
2. ~/.claude/plans/tingly-wobbling-stroustrup.md (live tracking plan — TOP PRIORITY)
3. ~/.claude/anti-patterns.md (especially MISSING_ODDS_ACCEPTED_WITHOUT_SCRAPING)
4. ~/.claude/memory/topics/ufc_website_maintenance_rules.md (29 rules including new ones)
5. CLAUDE.md (project-level)
6. ~/.claude/CLAUDE.md (global rules)
7. _audit/ directory (6 phase reports from site audit)

**Canonical local path for this project: ~/Projects/mmalogic/**
**Do NOT open this project from iCloud or /tmp/. Use the path above.**

### Current Numbers (v10.68 params, 71 events, post-backtest)
| Bet Type | W-L | P/L |
|----------|-----|-----|
| ML | 300W-114L | +89.59u |
| Method | 146W-184L | +82.80u |
| Round | 29W-48L | +18.36u |
| Combo | 25W-52L | +73.96u |
| Parlay | 31W-33L | +34.22u |
| **Combined** | | **+298.93u** |

### Upcoming Event
**UFC Fight Night: Adesanya vs. Pyfer — March 28, 2026**
- 7 picks (6 active + 1 pass), 2 parlays (HC + ROI)
- O'Neill still missing ML odds
- LIVE TRACKING MUST BE WORKING BEFORE THIS EVENT

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/Projects/mmalogic/**
**Last verified commit: f09076a on 2026-03-26 00:18:17 -0700**
