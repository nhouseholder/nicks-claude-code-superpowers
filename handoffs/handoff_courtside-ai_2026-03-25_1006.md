# Handoff — Courtside AI — 2026-03-24 9:30 PM CT

## Session Summary
Major session: Added NBA UNDERDOG tier (new dog ATS signal, +16-28% ROI), expanded pick analysis dropdowns to all users, ran comprehensive underdog ML/ATS backtests for both NBA and NCAA, and fixed 3 critical backend grading bugs that caused NCAA results to silently disappear.

## What Was Done

### 1. NCAA Standalone Tiers Removed (v12.29.0)
- Removed SCRAPPY, SURGE, MISMATCH, EXPLOIT from production
- All 4 failed tournament viability test (<5% ROI in March Madness)
- Files: `cron-generate.js`, `generate-picks.js`, `PicksPage.jsx`, `api.js`, `bets.js`, `RecentResults.jsx`

### 2. Pick Analysis Dropdowns (all users)
- Removed admin-only gate on NCAA `buildExplanation()` dropdown
- Enhanced NCAA dropdown: P(cover), EV estimate, all 9 stat edges, rest advantage, edge tier labels
- Enhanced NBA dropdown: spread analysis, EV calc, ML agreement, injuries, public betting
- Both show "View Analysis" button for all users
- Files: `src/routes/PicksPage.jsx`, `src/components/nba/NbaPickCard.jsx`

### 3. NBA Underdog Backtest Research
- Tested ~35 NBA underdog ML strategies — NONE consistently profitable
- Tested ~45 NBA underdog ATS strategies — found strong signals
- **Winner: "Model Edge 3+ + DE > 0"** — 310 bets, 59.4% ATS, +13.3% ROI, p=0.008
- **Refinements found:** ME5+ DE>0 (Premium, +16.2%), ME7+ DE>0 (Ultra, +28.0%)
- All consistent across all 3 seasons (2022-25)
- NCAA underdog ML/ATS: no profitable strategies found
- Backtest scripts: `scripts/analysis/nba_underdog_ml_backtest.py`, `ncaa_underdog_ml_backtest.py`

### 4. NBA UNDERDOG Tier Implemented (v12.30.0)
- Premium (ME5+ DE>0): 60.8% ATS, +16.2% ROI, p=0.002
- Ultra (ME7+ DE>0): 67.0% ATS, +28.0% ROI, p=0.004
- Lime green badge, callout with conviction level
- Files: `nba-generate-picks.js`, `nba-cron-generate.js`, `NbaPickCard.jsx`, `NbaPicksContent.jsx`, `nba-bets.js`
- Grading: Added to TRACKED_TIERS in `nba-cron-grade.js`, `nba-grade-picks.js`, `nba-live-results.js`

### 5. Backend Audit — 3 Critical Bugs Fixed
- **grade-results.js**: Missing fuzzy team name matching (ROOT CAUSE of missing NCAA results)
- **grade-results.js**: Never wrote to `graded_results` collection (results invisible to site)
- **grade-picks.js**: Rebuild only counted APEX, missed AGREE/MADNESS
- **nba-grade-picks.js**: TRACKED_TIERS missing FORTRESS/TALENT/UNDERDOG
- **nba-live-results.js**: Removed dead `yesterdayCT()`/`twoDaysAgoCT()`
- **nba-generate-picks.js/nba-cron-generate.js**: Removed unused `fetchBettingSplits` calls

## What's Left To Do
- **NCAA 0 picks issue**: The ML pipeline (`predict_and_upload.py`) hasn't been generating picks during March Madness. Need to verify the crontab is running and the pipeline produces picks with valid tiers
- **Admin Command Center dropdowns**: The "View Analysis" dropdown was added to the Picks page but NOT to the Admin Command Center tab in `AdminPage.jsx`
- **CLAUDE.md update**: Needs UNDERDOG tier documentation added to the NBA Tiers section
- **4th season backtest**: User mentioned wanting to add a 4th season for more statistical power — not yet implemented
- **Grading backfill**: Now that grading bugs are fixed, may need to manually trigger a rebuild to re-grade dates that were silently skipped

## Key Decisions Made
- **Dropped Core conviction for UNDERDOG** — user chose Premium (ME5+) and Ultra (ME7+) only
- **No NCAA underdog system** — backtest showed no profitable strategies
- **No NBA underdog ML system** — ATS is profitable but ML is not
- **UNDERDOG bets the DOG side** — opposite of all other NBA tiers which bet favorites

## Bugs Found & Fixed
| Bug | File | Root Cause | Fix |
|-----|------|-----------|-----|
| NCAA results silently skipped | grade-results.js | Exact-only team name matching | Added fuzzy prefix matcher |
| Graded results invisible to site | grade-results.js | Never wrote to `graded_results` collection | Added setDoc call |
| Season rebuild undercounts | grade-picks.js | Only counted APEX tier | Fixed to include AGREE/MADNESS |
| NBA tiers not tracked | nba-grade-picks.js | TRACKED_TIERS had only 2 of 7 tiers | Expanded to all 7 |

## Gotchas for Next Agent
- **Deploy clone pattern**: Git operations use `/tmp/courtside-ai-deploy`, not iCloud. Always clone fresh or pull latest.
- **iCloud != GitHub**: The iCloud working directory may be behind GitHub. Always check both.
- **rsync overwrites edits**: If you rsync from iCloud to deploy clone, you'll overwrite deploy clone edits. Re-apply after rsync.
- **UNDERDOG bets dogs**: All other NBA tiers bet the favorite. UNDERDOG bets the underdog side.
- **model_spread convention**: In NBA, positive model_spread = model thinks home wins. Negative = away wins. Trace carefully for dog side.

## Current State
- Branch: `main`
- Last commit: `c51a00f` — fix: Backend audit — 3 critical grading bugs + tier consistency
- Build status: passing
- Deploy status: deployed to Cloudflare Pages
- Version: 12.30.0

## NBA Tier Hierarchy (Current)
AGREE > DEFENSE > FORTRESS > TALENT > UNDERDOG > PLAYOFF_AGREE > PLAYOFF_DEFENSE

## NCAA Tier Hierarchy (Current)
MONEYLINE > AGREE > APEX > MADNESS
