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

---

## Step 3A: Update & Deploy

1. **Run validator first** — `python3 validate_registry.py` (see Ground Truth Validation below)
2. **If validator fails** — fix data issues BEFORE any display work
3. **Data sync** — copy data files from `ufc-predict/webapp/frontend/public/data/`
4. **Source sync** — check for divergence: `diff -rq ufc-predict/webapp/frontend/src/ webapp/frontend/src/`
5. **Build** — `cd ufc-predict/webapp/frontend && npm run build` (NEVER from root webapp/)
6. **Deploy** — commit + push to `ufc-predict` main branch to trigger GitHub CI auto-deploy
7. **Post-deploy verification** — run 15-item checklist on the live site via Claude in Chrome

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
# Commit everything
git add -A
git commit -m "Clean rebuild: fresh backtest + validated registry + rebuilt frontend"
git push origin main  # Triggers GitHub CI auto-deploy

# Wait for deploy, then visual verification via Claude in Chrome
# Run FULL 15-item checklist on live site
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

### The 4+1 Bet Model
- **ML** (moneyline): fighter wins = payout at odds, fighter loses = -1u
- **Method** (ML + exact method): requires ML win + correct method. KO/TKO grouped.
- **Round** (ML + exact round): requires ML win + correct round. ONLY for R1 KO predictions.
- **Combo** (ML + method + round): requires ALL three correct. ONLY for R1 KO predictions.
- **Parlay** (per event): HC parlay + High ROI parlay (if no fighter overlap)
- Fighter loss = ALL bets on that fighter lose (-1u each, up to -4u)
- Method and Round are scored INDEPENDENTLY

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

### Display Rules (Most Violated)
- Confidence = raw differential (0.14–3.0+), NOT a percentage
- Losses show -1u (not blank, not "—")
- Wins show payout at odds (not +1u flat, not blank)
- All 5 bet types on every page and every table component
- Both parlays per event
- Event count = 71+ (current backtest window)
- ALL table components must show the same bet types: EventBetsDropdown, AdminBacktest, EventSlideshow, LastWeekPicks, HistoryPage
- **Event breakdown tables must include parlay rows** (HC + ROI) below fight rows, showing legs, W/L, American odds, and P/L
- **Parlay P/L must be included in the Combined total** in both summary chips and TOTALS row

### Canonical Paths
- Webapp: `ufc-predict/webapp/frontend/` (NEVER root `webapp/`)
- Data: `ufc-predict/webapp/frontend/public/data/`
- Algorithm: `ufc-predict/`
- Validator: `ufc-predict/validate_registry.py`
- GitHub repo: `nhouseholder/ufc-predict`
- GitHub CI deploys on push to main

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
Version: [version.js value]
Freshness: [verified against GitHub ✓]
Validator: [ALL 12 RULES PASS / N failures — list them]
15-item checklist: [N/15 passed]
Knowledge updated: [list of files updated — or "none (no new learnings)" with justification]
Knowledge synced to GitHub: [yes/no — commit SHA]
Deployed: [yes/no — if yes, via GitHub CI]
```
