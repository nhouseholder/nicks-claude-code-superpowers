Dedicated MMALogic/OctagonAI website agent. This command carries ALL domain knowledge for mmalogic.com — betting rules, canonical paths, anti-patterns, verification checklists, ground truth validation, and learned errors. Use this for ANY task involving the UFC website.

Triggers: "mmalogic", "octagonai", "ufc website", "ufc site", "update the site", "deploy the site", "fix the site", any mention of mmalogic.com

---

## Step 0: Load Knowledge Base (MANDATORY — read before doing ANYTHING)

Read ALL of these files. Do NOT skip any. Do NOT "apply mentally" — actually read them:

```
1. ~/.claude/memory/topics/ufc_website_maintenance_rules.md    — 15-item verification checklist + 29 display rules
2. ~/.claude/memory/topics/ufc_canonical_paths.md              — canonical directory paths
3. ~/.claude/memory/topics/ufc_betting_model_spec.md           — 4-bet model specification + 12 scoring rules
4. ~/.claude/memory/topics/ufc_ground_truth_spec.md            — ground truth registry + validator spec
5. ~/.claude/skills/site-update-protocol/SKILL.md              — full update protocol
6. ~/.claude/anti-patterns.md                                  — search for "UFC" entries
7. ~/.claude/recurring-bugs.md                                 — search for "UFC" entries
```

After reading, summarize in one line what you loaded: "Loaded: 15-item checklist, canonical paths (ufc-predict/webapp/frontend/), 4-bet model, 12 scoring rules, ground truth spec, N anti-patterns, N recurring bugs."

## Step 1: Freshness Check (MANDATORY — prevents stale file disasters)

```bash
# Where am I?
echo "Working directory: $(pwd)"

# Branch check — NEVER deploy from feature branches
BRANCH=$(git branch --show-current 2>/dev/null)
echo "Branch: $BRANCH"
if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
  echo "⚠️ NOT ON MAIN — you are on branch: $BRANCH. Switch to main before deploying."
fi

# Is this iCloud? (iCloud folders diverge from GitHub)
[[ "$(pwd)" == *"Mobile Documents"* ]] && echo "⚠️ iCLOUD DIRECTORY — must verify freshness against GitHub"

# Clone fresh from GitHub for comparison
cd /tmp && rm -rf mmalogic-fresh
git clone https://github.com/nhouseholder/ufc-predict.git mmalogic-fresh --depth 1 2>&1 | tail -1

# Compare version
LOCAL_VER=$(cat ufc-predict/webapp/frontend/src/version.js 2>/dev/null || echo "NOT FOUND")
REMOTE_VER=$(cat /tmp/mmalogic-fresh/webapp/frontend/src/version.js 2>/dev/null || echo "NOT FOUND")
echo "Local version: $LOCAL_VER"
echo "GitHub version: $REMOTE_VER"

# If versions differ, ALWAYS use GitHub version
if [ "$LOCAL_VER" != "$REMOTE_VER" ]; then
  echo "⚠️ VERSION MISMATCH — local is stale. Work from /tmp/mmalogic-fresh/ or pull latest."
fi
```

**RULE: If local is stale, work from the fresh GitHub clone in /tmp/. Never edit stale files.**
**RULE: If branch is not main, switch before deploying. Feature branch deploys overwrite production.**

## Step 1.5: Baseline Snapshot (MANDATORY for Update/Deploy/Feature/Debug tasks)

Before making ANY changes, record what currently works. This prevents regressions.

1. **Record current version:** `cat webapp/frontend/src/config/version.js`
2. **Record current state of affected pages** — specific values, not "looks fine":
   - Hero cards: 5 cards with exact P/L values
   - Latest event table: row count, parlay row present, combined total
   - Chart: how many lines, starting point
   - Any other pages affected by this task
3. **Record credential counts in config files you'll touch:**
   ```bash
   grep -c "FIREBASE\|SUPABASE\|API_KEY\|SECRET" <files-you-will-edit> 2>/dev/null
   ```
4. **Write baseline to `_update/baseline.md`** (will be cleaned up before commit)

**RULE: If you can't state specific values for what currently works, you can't detect regressions. Record the baseline.**

## Step 2: Determine Task Type

Based on what the user asked, route to the appropriate workflow:

| User says | Task type | Workflow |
|-----------|-----------|---------|
| "update the site" / "push changes" / "deploy" | **Update & Deploy** | → Step 3A |
| "fix [bug]" / "something's broken" / screenshot | **Debug** | → Step 3B |
| "audit the site" / "check everything" | **Audit** | → Step 3C |
| "redesign" / "rebuild the look" | **Redesign** | → Step 3D |
| "add [feature]" / "change [component]" | **Feature Work** | → Step 3E |
| "check the site" / "how does it look" | **Visual Verification** | → Step 3F |
| "clean rebuild" / "start fresh" / "nuke and rebuild" | **Clean Rebuild** | → Step 3G |
| "review" / "--review" / "is this ready" / "pre-merge review" | **Domain-Safe Review** | → Step 3H |

---

## Step 3A: Update & Deploy

1. **Run validator first** — `python3 validate_registry.py` (see Ground Truth Validation below)
2. **If validator fails** — fix data issues BEFORE any display work
3. **Data sync** — copy data files from `ufc-predict/webapp/frontend/public/data/`
4. **Source sync** — check for divergence: `diff -rq ufc-predict/webapp/frontend/src/ webapp/frontend/src/`
5. **Credential protection** — before AND after edits, verify credential env vars are intact:
   ```bash
   grep -c "FIREBASE\|SUPABASE\|API_KEY\|SECRET\|VITE_" webapp/frontend/.env* wrangler.toml 2>/dev/null
   ```
   Counts must match before and after. If count drops, you removed a credential — UNDO immediately.
6. **Build** — `cd ufc-predict/webapp/frontend && npm run build` (NEVER from root webapp/)
7. **Version bump** — patch for fixes, minor for features. Update `version.js` and any "last updated" display.
8. **Clean up temp files** — `rm -rf _update/ 2>/dev/null` before committing
9. **Commit with specific files** — NEVER `git add -A`. Stage only files you intentionally changed:
   ```bash
   git add webapp/frontend/src/config/version.js webapp/frontend/public/data/*.json [other specific files]
   git commit -m "v[X.Y.Z]: [description]"
   git push origin main
   ```
10. **Post-deploy verification (MANDATORY)** — open mmalogic.com in Claude in Chrome or Preview:
    - Confirm new version number is displayed
    - Confirm updated date is displayed
    - Run FULL 15-item checklist with specific values for each item
    - Spot-check 1 event table end-to-end (fight-level P/L matches registry)
11. **If deploy fails or live site has regressions:**
    ```bash
    git revert HEAD    # revert the bad commit
    git push origin main  # CI redeploys the reverted state
    ```
    Log failure to `~/.claude/anti-patterns.md` with root cause.

## Step 3B: Debug

1. Read anti-patterns for matching bugs FIRST
2. **Run validator** — most "display bugs" are actually data bugs. Validator catches them.
3. If validator passes, the data is correct — bug is in frontend rendering
4. If validator fails, fix data first (re-run backtester or patch registry)
5. Baseline snapshot (specific values, not "looks fine")
6. Isolate → diagnose → fix
7. Verify against 15-item checklist
8. Log to anti-patterns with root cause
9. Commit and push to trigger CI redeploy

## Step 3C: Audit

1. **Run validator** — automated check of all 12 scoring rules across all events
2. Run `/site-audit` from `ufc-predict/webapp/frontend/`
3. Run the UFC-specific 15-item checklist
4. Spot-check 2 events end-to-end (compare validator output to what the site shows)

## Step 3D: Redesign

1. Run `/site-redesign` from `ufc-predict/webapp/frontend/`
2. **Preserve ALL betting display logic** — redesign is VISUAL only
3. **Validator must pass before AND after** — redesign cannot change data
4. After redesign, re-verify all display rules still pass

## Step 3E: Feature Work

1. Plan the feature
2. Implement in `ufc-predict/webapp/frontend/`
3. **Run validator before committing** — features often break scoring display
4. Verify 15-item checklist
5. Build and test before committing

## Step 3F: Visual Verification

Run the full 15-item checklist from ufc_website_maintenance_rules.md:
- Use Claude in Chrome or Claude Preview to view the live site
- Check EACH item with specific values
- Report pass/fail per item

## Step 3G: Clean Rebuild (NUCLEAR OPTION — guaranteed correct)

Use this when the data pipeline is too corrupted to patch. Starts from scratch:

### Phase 1: Clean Backtest
```bash
cd /path/to/ufc-predict

# 1. Backup current registry
cp ufc_profit_registry.json ufc_profit_registry_backup_$(date +%Y%m%d_%H%M%S).json

# 2. Run clean backtest (all events, walk-forward, cache-only for speed)
UFC_BACKTEST_MODE=1 UFC_CACHE_ONLY=1 UFC_NUM_EVENTS=71 python3 UFC_Alg_v4_fast_2026.py 2>&1 | tee backtest_clean_$(date +%Y%m%d).log

# 3. Verify the new registry is larger than or equal to backup
python3 -c "
import json
old = json.load(open('ufc_profit_registry_backup_*.json'))
new = json.load(open('ufc_profit_registry.json'))
old_events = len(old.get('events', []))
new_events = len(new.get('events', []))
print(f'Old: {old_events} events, New: {new_events} events')
assert new_events >= old_events, f'REGRESSION: new has fewer events ({new_events} < {old_events})'
print('✓ Event count OK')
"
```

### Phase 2: Validate Clean Data
```bash
# Run the ground truth validator on the fresh registry
python3 validate_registry.py

# If ANY rule fails, the backtest has a bug — do NOT proceed to frontend
# Fix the backtester, re-run, re-validate until ALL 12 rules pass
```

### Phase 3: Generate Frontend Data
```bash
# The backtester outputs the registry. Now generate the display data files:
# algorithm_stats.json, prediction_output.json, etc.
# These must be derived FROM the validated registry, not independently computed.

# Copy to webapp data directory
cp ufc_profit_registry.json webapp/frontend/public/data/
cp algorithm_stats.json webapp/frontend/public/data/
cp prediction_output.json webapp/frontend/public/data/
# ... (all data files)
```

### Phase 4: Rebuild Frontend (if needed)
If the frontend components are broken/confused:
```bash
cd ufc-predict/webapp/frontend
npm run build
# Verify build succeeds with zero warnings about missing data
```

### Phase 5: Deploy & Verify
```bash
# Stage specific files — NEVER git add -A (prevents accidental backup/temp file commits)
git add ufc_profit_registry.json algorithm_stats.json prediction_output.json
git add webapp/frontend/public/data/*.json
git add webapp/frontend/src/config/version.js
# Add any other intentionally changed files by name
git commit -m "Clean rebuild: fresh backtest + validated registry + rebuilt frontend"
git push origin main  # Triggers GitHub CI auto-deploy

# Wait for deploy, then visual verification via Claude in Chrome
# Run FULL 15-item checklist on live site
# If live site has regressions: git revert HEAD && git push origin main
```

### Phase 6: Snapshot Baseline
After deploy, record the known-good state:
```
CLEAN REBUILD BASELINE — [date]
Registry: [event count] events, [bout count] bouts
ML: [W]-[L], [pnl]u | Method: [W]-[L], [pnl]u | Round: [W]-[L], [pnl]u
Combo: [W]-[L], [pnl]u | Parlay: [W]-[L], [pnl]u
Total: [total bets] bets, [combined pnl]u, [ROI]%
Validator: ALL 12 RULES PASS
Version: v[X.Y.Z]
Commit: [SHA]
```

Save this baseline to `~/.claude/memory/topics/ufc_clean_rebuild_baseline.md` so future sessions know the last known-good state.

---

## Step 3H: Domain-Safe Review (--review)

Multi-agent site review with MMALogic guardrails. This is `/site-review` adapted to respect the betting model, scoring pipeline, and display rules. All agents are constrained to prevent the exact types of breakage we've seen 15+ times.

### Pre-Review Gate

Before dispatching agents, run the validator:
```bash
cd ufc-predict && python3 validate_registry.py
```
If validator fails, fix data FIRST — don't review broken state.

### Shared Context

Write `_review/CONTEXT.md` with standard project info PLUS:
```
DOMAIN_CONSTRAINTS:
- DO NOT suggest changes to: validate_registry.py, ufc_profit_registry.json, any scoring logic,
  algorithm files (UFC_Alg_*.py), constants.json, odds cache files
- DO NOT suggest "simplifying" P/L calculations — they implement 12 verified scoring rules
- DO NOT suggest removing bet types, columns, or parlay rows from any table
- DO NOT suggest changing odds format (MUST stay American: +150, -200)
- DO NOT suggest merging/refactoring EventBetsDropdown safePnl() — it's a safety net for 6 edge cases
- The 4+1 bet model is FINAL and user-confirmed. Do not suggest alternatives.
- confidence = raw differential (0.14–3.0+), NOT a percentage. Do not "fix" this.

PROTECTED FILES (read-only during review):
- webapp/frontend/.env*
- wrangler.toml
- validate_registry.py
- UFC_Alg_*.py
- constants.json
- ufc_odds_cache.json / ufc_prop_odds_cache.json
- ufc_profit_registry.json

SAFE TO REVIEW:
- webapp/frontend/src/components/ (visual/UX only, not scoring logic)
- webapp/frontend/src/pages/ (layout, navigation, UX)
- webapp/frontend/src/styles/ (CSS, Tailwind)
- webapp/frontend/public/ (assets, not data/*.json)
- Workers (live-tracker, API routes — security and reliability only)
```

### Agent 1: Frontend Reviewer (MMALogic-constrained)

**Dispatch prompt:**
> You are reviewing mmalogic.com's frontend. Read `_review/CONTEXT.md` — pay special attention to DOMAIN_CONSTRAINTS. Read `~/.claude/skills/senior-frontend/SKILL.md` and `~/.claude/skills/frontend-design/SKILL.md`.
>
> Review ONLY visual/UX quality in `webapp/frontend/src/`:
> - Component architecture (are components too large? good composition?)
> - User experience (loading states, empty states, error states, mobile responsiveness)
> - Visual design quality (typography, spacing, color consistency)
> - Performance (bundle size, lazy loading, image optimization)
> - Accessibility (ARIA, keyboard nav, contrast)
>
> **HARD CONSTRAINTS:**
> - DO NOT suggest changes to ANY table column content, P/L calculation, or bet type display
> - DO NOT suggest changes to safePnl(), scoring logic, or data processing
> - DO NOT suggest removing ANY existing functionality
> - If you see something in a protected file that looks odd, NOTE IT but do NOT suggest changing it
>
> Rate findings P0-P3. End with TOP 3 FRONTEND IMPROVEMENTS (visual/UX only).
> Write to `_review/frontend_review.md`.

### Agent 2: Backend/Worker Reviewer (MMALogic-constrained)

**Dispatch prompt:**
> You are reviewing mmalogic.com's backend infrastructure. Read `_review/CONTEXT.md`. Read `~/.claude/skills/senior-backend/SKILL.md`.
>
> Review ONLY reliability and security:
> - Live tracker Worker: error handling, timeout handling, Firestore write safety
> - API routes: input validation, auth on protected endpoints
> - CORS configuration
> - Secrets management (are any hardcoded?)
> - Firestore rules and data protection
> - GitHub Actions workflows: are they robust?
>
> **HARD CONSTRAINTS:**
> - DO NOT suggest changes to scoring logic or the algorithm
> - DO NOT suggest changes to the registry format or validator
> - DO NOT suggest removing or restructuring the live tracker's cron schedule
> - Focus on: "could this break in production?" and "is this secure?"
>
> Rate findings P0-P3. End with TOP 3 RELIABILITY IMPROVEMENTS.
> Write to `_review/backend_review.md`.

### Agent 3: Product Reviewer (MMALogic-constrained)

**Dispatch prompt:**
> You are reviewing mmalogic.com as a product. Read `_review/CONTEXT.md`. Read `~/.claude/skills/senior-dev-mindset/SKILL.md`.
>
> Review the site as a USER would experience it:
> - Does the site deliver on its promise (UFC betting predictions with transparent P/L)?
> - Is the navigation intuitive? Can users find what they need?
> - Are there dead pages, stub features, or confusing flows?
> - Is the data presentation clear to someone who bets on UFC?
> - What's the #1 thing that would make this more valuable to a bettor?
>
> **HARD CONSTRAINTS:**
> - DO NOT suggest changing the betting model, bet types, or scoring rules
> - DO NOT suggest "simplifying" the data — bettors want the detail
> - Focus on: "what would make a UFC bettor come back every week?"
>
> Rate findings P0-P3. End with TOP 3 PRODUCT IMPROVEMENTS.
> Write to `_review/fullstack_review.md`.

### Synthesis (Orchestrator)

After all agents complete:
1. Read all 3 review files
2. Deduplicate findings (same issue from multiple agents = 1 entry)
3. **FILTER OUT any suggestion that touches protected files or scoring logic** — if an agent violated constraints, drop that finding
4. Merge into ranked P0-P3 list
5. Present the standard site-review report format

### Post-Review

```
MMALOGIC REVIEW COMPLETE
=========================
Validator: [ALL 12 RULES PASS ✓]
Reviewers: Frontend + Backend + Product (all MMALogic-constrained)
Protected files: [confirmed untouched]
Findings: [N total] (P0: X, P1: Y, P2: Z, P3: W)
Constraint violations filtered: [N findings removed for touching protected areas]

[Standard site-review report follows]
```

The review is READ-ONLY. It produces recommendations. The user decides what to act on, and any implementation goes through the normal `/mmalogic` workflow with validator checks.

---

## Ground Truth Validation (THE FIX FOR RECURRING TABLE BUGS)

### Why This Exists
The UFC event table has been wrong 15+ times across multiple sessions. The root cause: no automated validation between the backtester output and what the website displays. Bugs include wrong methods (KO instead of DEC due to missing tiebreaker), missing parlays, -1u on won bets, missing bet types, and incorrect P/L calculations.

### The Validator: validate_registry.py
This script lives at `ufc-predict/validate_registry.py`. It reads `ufc_profit_registry.json` and checks ALL 12 scoring rules from the betting model spec against every bout in every event.

### What It Checks (12 Rules)

| Rule | Check | Failure = |
|------|-------|-----------|
| 1 | Fighter loss → ALL placed bets = -1u | Data corruption |
| 2 | Wins use real odds payout, not flat +1u | Payout calculation bug |
| 3 | All prop bets require ML win | Scoring logic bug |
| 4 | Combo wins require ML + method + round all correct | Combo scoring bug |
| 5 | No bet placed when odds are null | Phantom bet bug |
| 6 | No round/combo on DEC predictions | Gating bug |
| 7 | Bet count matches available odds | Bet counting bug |
| 8 | Method scoring: exact method match, KO/TKO grouped | Method matching bug |
| 9 | Method and Round scored independently | Independence violation |
| 10 | Parlay exists per event with correct legs | Parlay data bug |
| 11 | Total bets = sum of fight bets + parlays | Arithmetic bug |
| 12 | W + L = total bets per category | Balance check failure |

### Additional Checks (from learned bugs)

| Check | What It Catches |
|-------|----------------|
| R1 KO gating | Round/combo bets only on KO R1 predictions |
| SUB gating | No SUB method bets below threshold |
| DEC tiebreaker | When model is close between KO and DEC, verify tiebreaker fired |
| Parlay completeness | Both HC and ROI parlays present (or documented why not) |
| Odds reasonableness | No odds outside -2000 to +5000 range |
| P/L math | For each bout: combined_pnl = ml_pnl + method_pnl + round_pnl + combo_pnl |
| Event totals | Event-level totals match sum of bout-level P/L |
| Registry totals | Header totals match sum of all event totals |

### When to Run the Validator

**ALWAYS run before:**
- Any deploy (`Step 3A`)
- Any debug conclusion (`Step 3B` — "the data is correct" requires validator proof)
- Any audit sign-off (`Step 3C`)
- After any redesign (`Step 3D`)
- After any feature work (`Step 3E`)

**NEVER deploy if the validator fails.** Fix the data first.

---

## Domain Rules (Quick Reference — full spec in the knowledge base files)

### The 4+1 Bet Model (CORRECTED — 2026-03-25, user-confirmed)
- **ML** (moneyline): 1u bet. Fighter wins = payout at odds. Fighter loses = -1u.
- **Method** (exact method): 1u bet. **ALWAYS placed** when we have a method prediction. Fighter loses = -1u. Fighter wins + wrong method = -1u. Fighter wins + correct method = payout at method prop odds.
- **Round** (exact round): 1u bet. ONLY placed for R1 KO predictions. Fighter loses = -1u. Correct round = payout at round odds. Wrong round = -1u.
- **Combo** (method + round): 1u bet. ONLY placed for R1 KO predictions. Requires BOTH method AND round correct to win. Otherwise -1u.
- **Parlay** (per event): 1u bet. HC parlay + High ROI parlay (if no fighter overlap).
- **Fighter loss = ALL placed bets lose.** For DEC predictions: ML (-1u) + Method (-1u) = **-2.00u combined**. For KO R1 predictions: ML (-1u) + Method (-1u) + Round (-1u) + Combo (-1u) = **-4.00u combined**.
- Method and Round are scored INDEPENDENTLY.
- **Method bet does NOT require ML win to be PLACED.** It requires ML win to WIN, but it's always placed and always scored. This was the #1 most-confused rule across 5+ sessions.

### Parlay Rules (LEARNED — 2026-03-26)
- **HC Parlay** = top 2 FAVORITES by implied probability from active picks (not passes). Underdogs are NEVER HC legs.
- **ROI Parlay** = top 2 highest American odds picks (biggest underdogs), no overlap with HC legs.
- Implied probability: `abs(odds) / (abs(odds) + 100)` for favorites, `100 / (odds + 100)` for underdogs.
- Both parlays should appear per event in the registry as `parlay` (HC) and `parlay_roi` (ROI).

### Odds Format (PERMANENT RULE — 2026-03-26)
- **ALL odds on the site must be American format** (+150, -200). NEVER decimal/European (1.90x, 2.50x).
- Parlay combined odds stored as `parlay_odds_decimal` internally — convert for display: `dec >= 2.0 → +((dec-1)*100)`, `dec < 2.0 → -(100/(dec-1))`.
- This applies everywhere: event tables, admin panels, prediction output, parlay rows, all components.

### BFO Prop Odds Mapping (LEARNED — 2026-03-26)
- Prop odds cache uses `f1`/`f2` keys. f1 = first fighter in the `name1|||name2` key, f2 = second.
- f1/f2 do NOT always match red/blue corners. The BFO page order can be swapped.
- **ALWAYS validate**: favorite DEC odds should be LOWER than underdog DEC odds. If a -450 favorite shows +850 DEC, the f1/f2 mapping is WRONG.
- Cross-check: `f1_dec` vs `f2_dec` — the one closer to +100/+200 belongs to the favorite.

### Backtester vs Prediction Archive (LEARNED — 2026-03-26)
- The backtester's vectorized scoring path normalizes KO/DEC/SUB scores (divides by total), which eliminates small gaps that the DEC tiebreaker targets.
- The live prediction path does NOT normalize the same way, so tiebreaker fires for close calls.
- **After ANY backtest re-run**: cross-check the most recent 1-2 events' method predictions against `prediction_archive/`. If they diverge, the archive is ground truth.
- Manually patch the registry for recent events after re-running the backtester.

### Live Tracking Worker (DEPLOYED — 2026-03-26)
- `mmalogic-live-tracker` Cloudflare Worker at `https://mmalogic-live-tracker.nikhouseholdr.workers.dev`
- Cron: `*/5 * * * *` — fires every 5 min, only processes during Saturday 22:00-Sunday 09:00 UTC
- Scrapes UFCStats.com for completed bouts, scores ML/method/round/combo, updates Firestore `live_events/{slug}`
- Frontend picks up changes via `onSnapshot` — zero manual work on fight night
- Manual trigger: `curl -X POST https://mmalogic-live-tracker.nikhouseholdr.workers.dev/`
- Secret: `FIREBASE_SA_KEY` configured on the Worker

### Scoring Data Rules (MANDATORY — prevents the #1 recurring bug class)
- **NEVER accept missing odds.** If prop odds are null/missing, RUN THE SCRAPER before doing anything else. "—" in a payout cell is NEVER acceptable. Only after the scraper confirms the source is genuinely unavailable can you note "odds unavailable."
- **NEVER manually patch the registry.** Always re-run the backtester (`UFC_BACKTEST_MODE=1 UFC_CACHE_ONLY=1`) to fix scoring. Manual patches diverge from the backtester's logic and cause inconsistencies. The ONE exception: patching the most recent event's method prediction when the backtester's walk-forward diverges from prediction_archive (see Backtester vs Prediction Archive above).
- **R1 KO gating in registry**: If prediction is NOT R1 KO, then `round_correct` and `combo_correct` MUST be `null` (not `false`). `false` = bet placed and lost. `null` = no bet placed.
- **KO R1 losses need BOTH round AND combo at -1u**: If prediction was KO R1 but actual was DEC/SUB or wrong round, `round_pnl = -1` AND `combo_pnl = -1`. Not null.
- **Fighter loss = ALL placed bets lose -1u.** Method loses -1u (regardless of odds availability). Round/Combo lose -1u only if KO R1 was predicted.
- **Event totals must match sum of bout P/L.** After ANY registry change, verify: `event.ml.pnl == sum(bout.ml_pnl)` for each bet type.
- **Parlay totals aggregated separately.** Backtester doesn't aggregate parlays in registry totals — must be computed from event-level parlay data after each backtest.

### Odds Scraping Operational Knowledge (LEARNED — 2026-03-25)
- **BFO event name mismatch:** BFO uses short names ("UFC Seattle") while the algorithm uses full names ("UFC Fight Night: Adesanya vs. Pyfer"). The scraper's event-name matching needs fuzzy/token matching — if scraping returns 0 odds, check BFO's actual event name manually.
- **`__NO_PROPS__: true` blocks re-scraping:** The prop odds cache marks fights with no props found. On subsequent runs, the scraper skips these. To force re-scraping, delete the `__NO_PROPS__` entries from `ufc_prop_odds_cache.json` before running.
- **Prelim odds timing:** Prelim fight odds typically appear on BFO 1-2 days before the event, not a week before. Don't panic if prelim odds are missing early fight week — they'll appear Wed-Sat. The scheduled odds refresh workflow (Wed/Thu/Fri 3pm ET, Sat 9am ET) catches these automatically.
- **Registry totals vs algorithm_stats.json:** These come from different pipelines and CAN disagree. The registry (from `track_results.py`) is the source of truth for actual results. `algorithm_stats.json` (from the backtester) may have different ML/Method numbers due to different scoring interpretations. When they disagree, update `algorithm_stats.json` to match registry-computed values.

### Data Analysis Integrity (LEARNED — 2026-03-25/26)
- **Cross-query consistency.** If you run the same analysis twice and get different numbers, your query has a bug. NEVER present shifting numbers — use standalone scripts with assertions.
- **Extreme results = bug in your analysis.** 0% or 100% win rates, results that seem too good — suspect your code first, not the data.
- **Validate on known data.** Before presenting analysis as a "verdict", trace 1-2 specific events manually to confirm your query is correct.

### Apply & Regenerate Pipeline (VERIFIED — 2026-03-26)
- "Apply & Regenerate Picks" on admin optimizer page: saves constants to Firestore → dispatches GitHub Actions `run-predictions` workflow → GH Actions syncs constants from Firestore (`UFC_SYNC_CONSTANTS=1`) → runs algorithm → ingests predictions to site + commits to GitHub.
- Requires: `GITHUB_TOKEN` + `INGEST_SECRET` in Cloudflare Pages env vars, `GOOGLE_APPLICATION_CREDENTIALS_JSON` + `INGEST_SECRET` in GitHub repo secrets. All verified configured.
- Async: takes ~1-2 minutes. UI shows "Prediction run started."

### KO R2 Routing (ANALYZED — 2026-03-26, script: analysis_ko_r2_routing.py)
- KO R2 predictions: 19.4% end R1 KO, 12.5% exact R2 KO, 29.2% DEC, 26.4% fighter loses.
- Routing R2→R1: -40.4% ROI. Routing R2→DEC: -1.1% ROI. Current gating (no bet): 0% ROI.
- **Gating is correct.** Neither alternative routing is profitable.

### Display Rules (Most Violated)
- Confidence = raw differential (0.14–3.0+), NOT a percentage
- Losses show -1u (not blank, not "—"). Losses NEVER need odds — a loss is always -1u regardless.
- Wins show payout at real Vegas odds (not +1u flat, not blank). No odds for a WIN → show ✓ with "—" (no dollar amount).
- All 5 bet types on every page and every table component
- Both parlays per event
- Event count = 71+ (current backtest window)
- ALL table components must show the same bet types: EventBetsDropdown, AdminBacktest, EventSlideshow, LastWeekPicks, HistoryPage
- **Event breakdown tables must include parlay rows** (HC + ROI) below fight rows, showing legs, W/L, American odds, and P/L
- **Parlay P/L must be included in the Combined total** in both summary chips and TOTALS row
- **AdminBacktest must match EventBetsDropdown format**: Combo column, Parlay row, safePnl for losses, all 5 types in chart/totals

### Deploy Rules (CRITICAL — caused catastrophic v11.9.3 → v10.68 reversion)
- **NEVER run `wrangler deploy` manually.** Push to `ufc-predict` main branch → GitHub CI auto-deploys. Manual deploys risk deploying from the wrong directory.
- **Before ANY deploy: check version.js.** `cat webapp/frontend/src/config/version.js` — if it shows an OLD version, you're in the WRONG directory. ABORT.
- **Root `webapp/` is ARCHIVED** (`archive/webapp_ROOT_STALE_v10.68/`). It froze at v10.68 and deploying from it destroyed months of work. NEVER build or deploy from it.
- **The correct deploy chain:** edit files in `ufc-predict/webapp/frontend/` → commit → push → CI builds and deploys automatically.

### Data Sync After Backtest (MANDATORY)
- After every backtest or optimizer run, copy output files to webapp data dir:
  ```
  cp ufc_profit_registry.json webapp/frontend/public/data/
  cp algorithm_stats.json webapp/frontend/public/data/
  cp prediction_output.json webapp/frontend/public/data/
  ```
- Then commit and push to trigger CI redeploy with fresh data.
- **Parlay totals must be computed separately** — backtester doesn't aggregate them. Run parlay aggregation after every backtest.

### Frontend Safety Net: safePnl (LEARNED — 2026-03-25)
- `EventBetsDropdown.jsx` has a `safePnl(correct, pnl, odds)` function that computes P/L when registry data is incomplete:
  - `correct === false` → return `-1` (loss is always -1u regardless of odds)
  - `correct === true && odds != null` → return payout at odds
  - `pnl != null` → return pnl (registry value takes priority)
  - Otherwise → return null (no bet placed)
- **safePnl must NEVER assume +1.0 for wins.** If pnl is null and correct is true but no odds, show ✓ with "—" (correct prediction but no bet placed).
- This is a safety net, NOT a replacement for correct backtester output. The backtester should write complete data.

### Firestore Data Protection (LEARNED — 2026-03-25, caused catastrophic data regression)
- **track_results.py upload can OVERWRITE the full Firestore registry.** If it uploads 25 events, it destroys the 71-event registry.
- **Before any Firestore upload:** check existing event count. If new data has FEWER events, ABORT.
- **The Firestore `loadRegistry()` prefers Firestore over static JSON** when Firestore has bout-level data. If Firestore has stale 25-event data, the website shows 25 events even though the static JSON has 71.
- **After any backtest re-run:** verify Firestore was updated with the full registry, not just the static JSON.

### BFO Scraping Stability (LEARNED — 2026-03-25)
- **BFO scraping crashes the process on macOS** — silently killed around event 28-34 due to memory/resource limits.
- **Always use `UFC_CACHE_ONLY=1` for backtests.** Cache-only mode processes 71 events in ~5 minutes. Full scraping takes 30+ minutes and crashes.
- **If you MUST scrape:** run in smaller batches or use standalone scraper scripts, not the full algorithm import.

### Systems Layer (CRITICAL — NOT separate bets)
- **Systems are scoring pipeline MODIFIERS, not parallel bets.** They adjust the algorithm's confidence (diff score), NOT place independent wagers. The "Systems P/L" on the website is hypothetical tracking — NOT included in combined P/L.
- When systems agree with a pick → diff is boosted (more likely to bet). When they disagree → diff is penalized (might skip).
- System params: `SYSTEM_BET_BOOST` (+diff per agreeing system), `SYSTEM_FADE_PENALTY` (-diff per disagreeing system), `SYS_THRESH_ADJ` (lower pick threshold per net signal), `SYS_METHOD_BOOST` (method score amplification), `SYS_SCORE_WEIGHT` (base weight for score modification).
- `SYSTEM_SCORE_WEIGHT = 0.0` means systems are independent (don't modify fighter scores). Non-zero means they actively modify the scoring pipeline.

### Constants & Parameters
- `constants.json` = single source of truth for all algorithm parameters
- Optimizer saves optimized values to Firestore `algorithm_data/constants`
- Algorithm reads from `constants.json` at startup (or syncs from Firestore via `UFC_SYNC_CONSTANTS=1`)
- 61+ optimized parameters covering scoring weights, gating thresholds, system boosts
- **Optimizer zero-param problem:** If a parameter is at 0.0, the optimizer can't explore it (0 × anything = 0). To test a new param group (e.g., activating systems), seed non-zero starting values in both the .py file AND constants.json before running the optimizer.

### Odds Cache Rules (MANDATORY)
- **All Vegas odds must be cached and committed to GitHub.** `ufc_odds_cache.json` and `ufc_prop_odds_cache.json` are IRREPLACEABLE historical data. Once an event passes, BFO pages disappear.
- **Backtests default to cache-only.** `UFC_CACHE_ONLY=1` is the default in backtest mode. All 71+ events have complete ML + prop odds cached. Never re-scrape during backtest — it wastes 20+ minutes and risks overwriting good data with stale or unavailable data.
- **After any scrape, commit the updated cache files.** `git add ufc_odds_cache.json ufc_prop_odds_cache.json && git commit`.

### Canonical Paths
- Webapp: `ufc-predict/webapp/frontend/` (NEVER root `webapp/` — it's archived)
- Data: `ufc-predict/webapp/frontend/public/data/`
- Algorithm: `ufc-predict/`
- Validator: `ufc-predict/validate_registry.py`
- GitHub repo: `nhouseholder/ufc-predict`
- GitHub CI deploys on push to main — this is the ONLY correct deploy method

---

## Learning & Growth (MANDATORY — NOT OPTIONAL)

**Every /mmalogic session MUST update knowledge before ending.** This is not a suggestion — it's a hard requirement. The output format below has a "Knowledge updated" field. If it says "none" AND you fixed a bug or learned something, you failed this step.

### What to record (check ALL, record any that apply)

| Trigger | Where to write | Format |
|---------|---------------|--------|
| Fixed a bug | `~/.claude/anti-patterns.md` | `### [SHORT_TITLE] — [DATE]` with Context, Bug, Root cause, Fix, Applies when |
| Bug occurred before | `~/.claude/recurring-bugs.md` | Add recurrence count + link to anti-pattern |
| New display rule | `ufc_website_maintenance_rules.md` | Add numbered rule to the appropriate section |
| New validator check needed | `ufc_ground_truth_spec.md` + `validate_registry.py` | Add check function + table entry |
| Scoring rule clarification | `ufc_betting_model_spec.md` | Add to appropriate rule section (ONLY with user approval) |
| Path or structure changed | `ufc_canonical_paths.md` | Update the affected path |
| Frontend component behavior | `ufc_website_maintenance_rules.md` | Add to Bug History table |
| Parlay logic learned | `ufc_betting_model_spec.md` Parlay Rules section | Document the edge case |
| Tiebreaker behavior | `ufc_betting_model_spec.md` | Document the tiebreaker rule |
| Odds scraper behavior | `ufc_website_maintenance_rules.md` rule 22/28 | Update scraper instructions |

### How to record

1. **Be specific.** "Fixed table bug" is useless. "EventBetsDropdown showed method_pnl=null for fighter losses because safePnl() returned early on null odds before checking ml_correct" is useful.
2. **Include the root cause.** Not just what was wrong — WHY it was wrong. What assumption was flawed?
3. **Include "Applies when".** When should a future agent check this? "Any time you modify safePnl() or add a new bet type column."
4. **Date everything.** Use ISO format (2026-03-26).
5. **Cross-reference.** If a bug relates to an existing anti-pattern, link them.

### How to sync knowledge to GitHub

After writing to any memory/anti-pattern file:

```bash
# Clone superpowers repo fresh (NEVER push from iCloud)
cd /tmp && rm -rf superpowers-sync
git clone https://github.com/nhouseholder/nicks-claude-code-superpowers.git superpowers-sync 2>&1 | tail -1

# Copy updated files
cp ~/.claude/anti-patterns.md /tmp/superpowers-sync/
cp ~/.claude/recurring-bugs.md /tmp/superpowers-sync/
cp ~/.claude/memory/topics/ufc_*.md /tmp/superpowers-sync/memory/topics/
cp ~/.claude/commands/mmalogic.md /tmp/superpowers-sync/commands/

# Commit and push
cd /tmp/superpowers-sync
git add -A
git commit -m "MMALogic session learning: [brief description of what was learned]"
git push origin main

# Cleanup
rm -rf /tmp/superpowers-sync
```

**This sync MUST happen before the session ends.** Knowledge that only lives in one session's memory is worthless — it dies when the session closes.

### Verification

At session end, ask yourself:
- Did I fix any bugs? → Did I record them in anti-patterns?
- Did I learn any display rules? → Did I add them to maintenance rules?
- Did I discover any data edge cases? → Did I add validator checks?
- Did I push all knowledge to GitHub? → Is the sync done?

If ANY answer is "no" when it should be "yes", **do it now before writing the output format.**

---

## Output Format

Every task ends with:
```
MMALOGIC TASK COMPLETE
======================
Task: [what was done]
Directory: [confirmed canonical path]
Branch: [main ✓ / other — explain why]
Version: [before] → [after] (bumped ✓ / N/A — no deploy)
Freshness: [verified against GitHub ✓]
Baseline: [N items recorded] — [all preserved ✓ / N regressions fixed]
Validator: [ALL 12 RULES PASS / N failures — list them]
15-item checklist: [N/15 passed]
Credentials: [verified intact ✓ — counts match before/after]
Changed files: [list of specific files staged]
Knowledge updated: [list of files updated — or "none (no new learnings)" with justification]
Knowledge synced to GitHub: [yes/no — commit SHA]
Deployed: [yes/no — if yes, via GitHub CI]
Live verification: [version + date + changes confirmed on mmalogic.com ✓]
```
