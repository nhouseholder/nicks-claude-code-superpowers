---
name: site-update-protocol
description: Universal checklist for updating sports prediction websites (OctagonAI, Diamond Predictions, Courtside AI) after algorithm changes. Covers all tabs, stats, data files, images, backtest results, and deployment. Fires when algorithm changes are committed or when the user mentions updating the site/website.
weight: light
category: deployment
---

# Site Update Protocol — Full Website Refresh After Algorithm Changes

## When This Activates

After ANY algorithm change that affects predictions, accuracy, P/L, stats, or backtest results — including:
- Coefficient/weight changes
- New betting systems added or removed
- Feature engineering changes
- Backtest window changes
- Optimizer runs
- Any change that alters prediction output or historical stats

**One rule: if the algorithm changed, the ENTIRE site must reflect the new state. No partial updates.**

## Site Registry

| Site | Sport | URL | Repo | Algorithm Location |
|------|-------|-----|------|--------------------|
| OctagonAI | UFC | octagonai.pages.dev | nhouseholder/ufc-predict | `UFC_Alg_v4_fast_2026.py` |
| Diamond Predictions | MLB + NHL | diamond-predict.pages.dev | nhouseholder/diamond-predictions | `mlb_predict/algorithms/` + `nhl_predict/algorithms/` |
| Courtside AI | CBB + NBA | courtside-ai.pages.dev | nhouseholder/courtside-ai | `scripts/predict_and_upload.py` |

All sites: **React + Vite + Tailwind + Cloudflare Pages**

## Universal Update Checklist

After every algorithm change, run through ALL of these. Skip none.

### Phase 1: Regenerate Data

Every site has static JSON data files that power the frontend. These MUST be regenerated after algorithm changes.

**OctagonAI (UFC):**
```bash
# Run full backtest (generates updated stats)
python UFC_Alg_v4_fast_2026.py 2>&1 | tee backtest_results.log

# Key output files to verify (all in webapp/frontend/public/data/):
# - algorithm_stats.json      ← accuracy %, component breakdown
# - ufc_profit_registry.json  ← event history, P/L per event
# - backtest_summary.json     ← backtest results
# - fight_breakdowns.json     ← detailed fighter analysis
# - constants.json            ← algorithm parameters
# - current_picks.json        ← latest event picks (if event is upcoming)
# - optimizer_results.json    ← if optimizer was run
```

**Diamond Predictions (MLB):**
```bash
# Full refresh pipeline (backtest + data gen + build + deploy)
./mlb_predict/scripts/refresh_and_deploy.sh

# Or quick mode (skip backtest, just regenerate):
./mlb_predict/scripts/refresh_and_deploy.sh --quick

# Key output files (in backtest_results/ → copied to webapp/frontend/public/data/):
# - prediction_log.json           ← all picks recomputed
# - performance_log.json          ← historical ROI/results
# - system_profit_rankings.json   ← system leaderboard
# - system_bets_log.json          ← per-system stats
```

**Diamond Predictions (NHL):**
```bash
# NHL pipeline cross-writes to diamond-predictions frontend
# Key output files (copied to webapp/frontend/public/data/nhl-*.json):
# - nhl-predictions.json
# - nhl-performance.json
# - nhl-system-rankings.json
```

**Courtside AI (CBB/NBA):**
```bash
# Regenerate static data from backtest DB
python3 scripts/generate-static-data.py

# Key output files (in public/data/):
# - predictions.json    ← today's picks with edges, tiers
# - summary.json        ← season stats (record, ATS%, ROI, units)
# - performance.json    ← daily cumulative profit curve
# - elo.json            ← team ELO rankings
# - recent-results.json ← last 15 graded games
# - diagnostic-summary.json ← model diagnostics
# NBA variants in public/data/nba/
```

### Phase 2: Verify All Data Files Updated

Before building, confirm every data file has a fresh timestamp:

```bash
# Check all data files were regenerated (should all be within last few minutes)
ls -la webapp/frontend/public/data/*.json  # or public/data/*.json
```

**Checklist — every file must reflect the new algorithm:**

| What | Where to Check | What Should Change |
|------|----------------|-------------------|
| Overall accuracy/record | `algorithm_stats.json` or `summary.json` | New win %, P/L, ROI |
| Profit curve data | `performance.json` or `ufc_profit_registry.json` | New data points, updated totals |
| System rankings | `system_profit_rankings.json` | Reranked by new performance |
| Pick history | `prediction_log.json` or registry | All historical picks recomputed |
| Current picks | `current_picks.json` or `predictions.json` | New odds, edges, tier assignments |
| Algorithm parameters | `constants.json` or config | New weights/coefficients |
| Backtest summary | `backtest_summary.json` | New baseline numbers |

### Phase 3: Update Frontend Components (If Needed)

Usually NO code changes needed — the frontend reads data files dynamically. But check if:

- [ ] **New stat added** → Add display in Dashboard/Admin component
- [ ] **New betting system category** → Add to system leaderboard/rankings
- [ ] **New tier/badge** → Add styling in Picks component
- [ ] **Accuracy milestones** → Update hero stats on Landing page (if hardcoded)
- [ ] **Version number** → Bump in `package.json` or `VERSION` file

**Landing Page Stats** — These are often partially hardcoded. Check:
- Hero section accuracy/ROI numbers
- "X events tracked" or "X picks analyzed" counts
- Profit curve preview
- System count ("powered by X systems")

### Phase 4: Build & Deploy

**CRITICAL: Never build from iCloud directory. Clone to `/tmp/` first.**

**OctagonAI:**
```bash
cd /tmp/ && git clone <repo> octagonai-deploy && cd octagonai-deploy
# Copy updated data files if not committed
npm ci && npm run build
npx wrangler pages deploy dist --project-name=octagonai
```

**Diamond Predictions:**
```bash
# refresh_and_deploy.sh handles this automatically
# Or manual:
cd webapp/frontend && npm ci && npm run build
npx wrangler pages deploy dist --project-name=diamond-predict
```

**Courtside AI:**
```bash
cd /tmp/ && git clone <repo> courtside-deploy && cd courtside-deploy
npm ci && npm run build
npx wrangler pages deploy dist --project-name=courtside-ai
```

### Phase 5: Post-Deploy Verification

After deploy, verify EVERY tab shows updated data:

| Tab/Page | What to Verify |
|----------|---------------|
| **Home/Landing** | Hero stats match new accuracy/ROI. Profit curve shows latest data. Pick count is current. |
| **Picks** | Current event picks render. Odds are fresh. Tier badges correct. System signals display. |
| **Dashboard** | Profit curve has all events. ROI/win rate matches backtest. Component accuracy table updated. |
| **History** | All historical events listed. Results (W/L/P) correct. P/L per event matches registry. |
| **Admin → Overview** | System status shows latest run timestamp. Stats match other pages. |
| **Admin → Backtest** | Backtest results show new baseline. Summary matches algorithm_stats. |
| **Admin → Systems** | All systems listed with correct trigger counts and P/L. New systems appear. Removed systems gone. |
| **Admin → Algorithm** | Parameters/constants reflect current values. |
| **Admin → Performance** | Profit timeline matches dashboard. Event breakdown is complete. |

### Phase 6: Update Firestore (If Applicable)

**OctagonAI + Courtside AI** use Firestore for real-time data:

```python
# OctagonAI: Upload to Firestore after data generation
python firestore_upload.py  # or triggered via admin panel

# Courtside AI: Cron worker auto-generates, but verify:
# - Firestore collection has fresh predictions
# - graded_results collection is current
```

**Diamond Predictions** uses FastAPI backend — verify the backend can read the new JSON files.

## What Gets Missed Most Often

These are the items that get forgotten and cause stale data on the site:

1. **Landing page hero stats** — Often hardcoded, not dynamic. Must manually update after accuracy changes.
2. **System count** — "Powered by X systems" on landing page when systems are added/removed.
3. **Firestore upload** — Data files regenerated but Firestore not synced (OctagonAI).
4. **VERSION bump** — Site shows old version number.
5. **NHL cross-write** — MLB changes deployed but NHL data not regenerated into Diamond Predictions.
6. **Pick history pagination** — New events not appearing because registry wasn't regenerated.
7. **Admin backtest tab** — Shows old backtest summary because `backtest_summary.json` wasn't regenerated.

## Automation Status

| Site | Auto-Deploy on Push | Auto-Picks Generation | Auto-Grading | Auto-Backtest |
|------|--------------------|-----------------------|--------------|---------------|
| OctagonAI | Yes (GitHub Actions) | Yes (Sunday 7am UTC) | Yes (Sunday 2pm UTC) | Manual |
| Diamond Predictions | Yes (GitHub Actions) | Via refresh script | Via admin API | Via refresh script |
| Courtside AI | Yes (GitHub Actions) | Yes (Cloudflare Cron) | Yes (Cloudflare Cron) | Manual |

## Quick Command: Full Site Refresh

For each site, this single sequence covers everything:

```bash
# 1. Clone to safe location (NEVER iCloud)
cd /tmp && git clone <repo-url> site-deploy && cd site-deploy

# 2. Run algorithm/backtest (sport-specific command)
python <algorithm_script> 2>&1 | tee backtest.log

# 3. Regenerate all data files (sport-specific)
# UFC: data generated by algorithm script
# MLB: ./mlb_predict/scripts/refresh_and_deploy.sh
# CBB: python3 scripts/generate-static-data.py

# 4. Verify data files are fresh
ls -la public/data/*.json  # or webapp/frontend/public/data/*.json

# 5. Build frontend
cd webapp/frontend  # or project root for Courtside
npm ci && npm run build

# 6. Deploy
npx wrangler pages deploy dist --project-name=<project-name>

# 7. Verify all tabs in browser
# 8. Commit and push
git add -A && git commit -m "update: vX.X — [description of algorithm change]"
git push

# 9. Sync back to iCloud (for backup)
```

## Rules

1. **No partial updates.** If the algorithm changed, regenerate ALL data files and verify ALL tabs.
2. **Always backtest first.** Never deploy algorithm changes without confirming the new baseline.
3. **Version bump every deploy.** Even minor data refreshes get a version increment.
4. **Never deploy from iCloud.** Clone to `/tmp/` first.
5. **Verify after deploy.** Open every tab in the browser and confirm fresh data.
6. **Commit data files.** The regenerated JSON files are the audit trail — commit them.
