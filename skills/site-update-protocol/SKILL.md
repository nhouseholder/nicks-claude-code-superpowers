---
name: site-update-protocol
description: UFC MMA Logic website frontend update and maintenance protocol. Fires after ANY algorithm update, backtest re-run, new event scoring, or website deploy. Ensures all 5 bet types display correctly, charts render properly, tables are complete, and data is consistent across all pages. Prevents the recurring bugs of missing bet types, broken charts, and incomplete tables.
weight: light
triggers:
  - "update the website"
  - "deploy to cloudflare"
  - "update mmalogic"
  - "sync data to webapp"
  - after any backtest re-run
  - after any algorithm change that affects P/L
  - after scoring a new event
---

# Site Update Protocol — mmalogic.com / OctagonAI

## When This Fires

After ANY of these:
- Algorithm update that changes scoring/P/L
- Backtest re-run that regenerates the registry
- New event scored and added to registry
- Frontend code change
- User says "update the website"

## The 5 Display Requirements (Non-Negotiable)

Every page on mmalogic.com MUST display all 5 bet types. If any page shows fewer than 5, it's broken.

### 1. Hero Stats Cards — MUST show 5 cards

```
[ML +60.07u]  [Method +34.99u]  [Round +3.58u]  [Combo +35.25u]  [Parlay +28.65u]
 183W-61L       86W-110L          17W-38L          14W-37L          18W-17L
```

Colors: ML=green, Method=blue, Round=purple, Combo=amber, Parlay=yellow

**Bug this prevents:** Screenshots showed 3 cards (ML/Method/Round only). All 5 must always render.

### 2. Event Tables — MUST have all columns + parlay row + totals row

```
FIGHT              | ML      | METHOD  | ROUND  | COMBO  | COMBINED
Murphy v Evloev    | X -1.00 | X -1.00 | —      | —      | -2.00
Page v Patterson   | ✓ +0.56 | ✓ +1.90 | —      | —      | +2.46
Duncan v Dolidze   | ✓ +0.22 | ✓ +1.30 | —      | —      | +1.52
PARLAY (Page+Duncan)                                      | +1.80
EVENT TOTAL        | -0.22   | +0.20   | —      | —      | +3.78
```

Rules:
- Fighter LOSS → show "X -1.00u" in EVERY bet type column where a bet was placed (not "X —")
- Fighter WIN but no odds → show "✓ —" (checkmark, no P/L amount)
- No bet placed → show "—" (em dash)
- NEVER show "0.00u" for a bet type with wins — that means the P/L isn't being computed
- Parlay row is ALWAYS present (even if no parlay was placed, show "— no parlay")
- EVENT TOTAL row sums ALL bet P/Ls including parlay

**Bugs this prevents:**
- Method showing "0.00u" with "2W-0L" (impossible — wins must have positive P/L)
- Method showing "✓ ✓" with no dollar amounts
- Murphy method showing "X —" instead of "X -1.00u"
- Missing parlay row
- Missing totals row

### 3. Profit Curve Chart — ALL 5 lines starting from event 1

Requirements:
- 5 colored lines: Combined (red), ML (green), Method (blue), Round (purple), Combo (amber), Parlay (yellow)
- ALL lines start at (0, 0) from event 1 — no flat zero line for the first 35 events
- X-axis labels: show every 8-10 events, angled at -45°, with enough height (100px minimum) so text isn't cut off
- Legend at bottom with all 6 items visible (no overlap, no truncation)
- Y-axis starts at the minimum value (allow negative), not hardcoded at 0

**Bugs this prevents:**
- Graph starting in the middle with first 35 events showing flat zero
- X-axis labels overlapping or cut off at bottom
- Legend items overlapping ("Round" being cut off)
- Only showing 3 lines instead of 6

### 4. Event History Cards — ALL 5 bet type summaries

Each event card in the scrollable history must show:
```
UFC Fight Night: Emmett vs. Vallejos        -4.17u
Mar 13, 2026 · 9 picks
[ML -0.07u 6W-3L] [Method -2.09u 3W-3L] [Round -1.00u 0W-1L] [Combo ... ] [Parlay ... ]
```

**Bugs this prevents:**
- Only showing ML/Method/Round, missing Combo/Parlay
- Event name truncated to "UFC ..." — show full name or truncate with "..." only after 40+ chars

### 5. History Page Event Tables — Same rules as #2

The History page has its own inline table (NOT EventBetsDropdown). It must follow the exact same 5-column format with parlay row and totals row.

## Data Consistency Checks (Run Before EVERY Deploy)

Before deploying, verify these invariants:

```python
# Run mentally or with validate_event_table.py
for event in registry:
    # 1. Profit > 0 requires Wins > 0
    assert not (event.ml.pnl > 0 and event.ml.wins == 0)

    # 2. Wins with 0.00u P/L is impossible (unless all wins had missing odds)
    if event.method.wins > 0 and event.method.pnl == 0:
        # WARNING: method wins exist but P/L is zero — odds are missing

    # 3. Combined = ML + Method + Round + Combo + Parlay
    assert combined == ml + method + round + combo + parlay

    # 4. Fighter loss = ALL placed bets lose (each -1u)
    for bout in event.bouts:
        if not bout.correct:  # fighter lost
            assert bout.ml_pnl == -1.0
            if bout.method_odds: assert bout.method_pnl == -1.0

    # 5. W + L counts match displayed totals
    assert ml.wins + ml.losses == total_ml_bets
```

## Update Procedure

### Step 0: Sync from Canonical Source (MANDATORY)
```bash
# Sync ALL data files from ufc-predict → root webapp
SRC="ufc-predict/webapp/frontend/public/data"
DST="webapp/frontend/public/data"
for f in algorithm_stats.json ufc_profit_registry.json ufc_systems_registry.json current_picks.json fight_breakdowns.json constants.json optimizer_results.json; do
  cp "$SRC/$f" "$DST/$f"
done
# Also check for source file divergence
diff -rq ufc-predict/webapp/frontend/src/ webapp/frontend/src/ | head -20
```
**Why:** This step was missing and caused 25 events showing instead of 71 on the live site.

### Step 0.5: Verify Registry Totals (MANDATORY)
Check that `ufc_profit_registry.json` totals include ALL 5 bet types:
- `ml_wins`, `ml_losses`, `ml_pnl`
- `method_wins`, `method_losses`, `method_pnl`
- `round_wins`, `round_losses`, `round_pnl`
- `combo_wins`, `combo_losses`, `combo_pnl`
- `parlay_wins`, `parlay_losses`, `parlay_pnl`

If parlay fields are missing, recompute totals from event-level data.

### Step 1: Copy Data Files
```bash
cp /path/to/ufc_profit_registry.json webapp/public/data/
cp /path/to/algorithm_stats.json webapp/public/data/
cp /path/to/upcoming_predictions.json webapp/public/data/  # if new picks
```

### Step 2: Verify Data Before Build
- Check registry has 71+ events
- Check algorithm_stats.json has correct version (currently v11.11)
- Check combined P/L matches expected baseline
- Run data consistency checks (above)

### Step 3: Build and Deploy
```bash
cd webapp && npm run build && npx wrangler pages deploy dist --project-name=octagonai
```

### Step 4: Visual Verification (MANDATORY)
After deploy, check EVERY page:

| Page | What to verify |
|------|---------------|
| Landing (/) | 5 hero cards, profit curve with 5 lines from event 1, latest event with all columns |
| Dashboard (/dashboard) | 8 summary stats, event tables with 5 columns + parlay + totals |
| History (/history) | All events listed, 5 columns per event, event names not truncated |
| Upcoming (/upcoming) | Latest picks displayed |

### Step 5: Spot-Check One Event Table
Pick the latest event. Verify:
1. Every fighter loss shows -1.00u in EVERY column where a bet was placed
2. Every fighter win shows correct odds-based P/L (not flat +1.00u)
3. Combined column = sum of all bet columns for that row
4. Parlay row shows correct legs and P/L
5. Event total row sums correctly

## Common Failure Modes (With Fixes)

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Method shows 0.00u with W > 0 | Method odds missing (method_pnl: null) | Show "✓ —" not "✓ 0.00u" |
| 3 cards instead of 5 | Old component version deployed | Rebuild from source |
| Chart starts in middle | Profit curve data starts at event ~35 not event 1 | Fix computeCurveFromRegistry to iterate ALL events |
| X-axis labels cut off | Chart height too small or angle wrong | Set xAxis height={100}, angle={-45} |
| Legend overlaps | Too many items for available width | Use 2-row legend or smaller font |
| "Please fill out this field" tooltip | Browser autocomplete on a non-form element | Add autoComplete="off" to the container |
| Event name "UFC ..." | CSS truncation too aggressive | Set min-width or use text-ellipsis with wider container |
| Version shows old number | algorithm_stats.json overwritten by backtest | Never overwrite — only update specific fields |
| Combined P/L doesn't match sum | Parlay not included in combined calculation | combined = ml + method + round + combo + parlay |

## Color Scheme (Canonical)

| Bet Type | Color | Tailwind | Hex |
|----------|-------|----------|-----|
| ML | Green | text-green-400 | #4ade80 |
| Method | Blue | text-blue-400 | #60a5fa |
| Round | Purple | text-purple-400 | #c084fc |
| Combo | Amber | text-amber-400 | #fbbf24 |
| Parlay | Yellow | text-yellow-400 | #facc15 |
| Combined | Red | text-red-400 | #f87171 |

## Domain Knowledge Requirement

Before touching any UFC website code, the AI agent MUST read:
- `~/.claude/memory/topics/ufc_betting_domain_knowledge.md` — expert-level UFC betting reference
- `~/.claude/memory/topics/ufc_betting_model_spec.md` — the 4+1 bet model specification

If the agent does not understand how prop bets settle (fighter loss = ALL props lose), it WILL produce broken tables. Read the domain knowledge first.

## Screenshot-Verified Bug Checklist (Recurring Issues)

These bugs have been found on the live site via screenshots. Check for ALL of them after every deploy:

| # | Bug | Where | How to Detect | Fix |
|---|-----|-------|--------------|-----|
| 1 | Method shows "✓ ✓" with no P/L amount | Event table method column | Page/Duncan show green checkmarks but "—" instead of dollar amounts | Display method_pnl if available, "✓ —" only if method_correct=true AND method_pnl=null |
| 2 | Method header shows "0.00u 0W-0L" when bouts have method wins | Event card summary | Evloev vs Murphy card shows Method 0.00u when 2 bouts have method_correct=true | Recompute event-level method stats from bout data, not from potentially zeroed aggregates |
| 3 | Murphy method shows "X —" instead of "X -1.00u" | Event table | Murphy lost AND method bet was placed (method_odds exist) → should show -1.00u loss | If fighter lost AND bet was placed (odds exist), show "X -1.00u" |
| 4 | Profit curve starts flat at 0 for first ~35 events | Chart | Left third of chart shows flat red line at 0 | Ensure profit curve data array has entries for ALL events starting from event 1 |
| 5 | X-axis event labels cut off at bottom | Chart | Event names truncated, only top portions visible | Set chart bottom margin to 120px+, angle labels -45°, ensure container has overflow visible |
| 6 | Legend items overlap or get cut off ("Round" partially visible) | Chart legend | Legend text runs together or clips | Use flexWrap, or 2-row legend, or reduce font size |
| 7 | "Please fill out this field" browser tooltip | Landing page, near search/filter area | Native browser validation tooltip appearing on non-form elements | Add `autoComplete="off"` and `noValidate` to container elements |
| 8 | Event cards show only "ML/Method/Round" — missing Combo and Parlay | Event history cards | Cards show 3 summary badges instead of 5 | Update EventCard component to include combo + parlay badges |
| 9 | Event table in history shows "ML ODDS / ML / METHOD ODDS" — missing Round/Combo/Parlay columns | History page inline table | Table only has 3 data columns | Update HistoryPage table to use same 5-column format as EventBetsDropdown |
| 10 | Two different profit curves on same site — one shows ML+Method+Round (3 lines), other shows all 5 | Multiple pages | Inconsistent chart data | Ensure ALL charts use the same registryData.js computeCurveFromRegistry with all 5 bet types |
| 11 | Registry totals missing parlay fields — Combo/Parlay show 0W-0L +0.00u on hero | Landing page hero cards | Parlay card shows +0.00u, combined P/L is wrong | Verify registry totals include ALL 5 bet types with wins/losses/pnl. Recompute from events if missing. |
| 12 | Confidence shows >100% (e.g., "260% conf") | Picks page FightCard | pick.diff * 100 displayed as percentage | Display raw diff value (e.g., "2.60 diff") — diff is NOT a percentage |
| 13 | Data files not synced between ufc-predict/webapp/ and root webapp/ | All pages | Stale P/L numbers, wrong event count, old version | After EVERY backtest/optimizer/prediction run, sync 7 data files + modified source files from ufc-predict/webapp/ → root webapp/ |
| 14 | algorithm_stats.json missing parlay_pnl | Admin page, any component reading stats | Combined P/L doesn't include parlay | Always include parlay_pnl, parlay_wins, parlay_losses in algorithm_stats.json |

## Rules

1. **All 5 bet types on every page** — if any page shows fewer than 5, the deploy is broken
2. **No 0.00u with wins** — display "✓ —" for wins without odds, never "✓ 0.00u"
3. **Fighter loss = -1.00u in every column** — not "X —", show the actual -1.00u
4. **Chart starts at event 1** — no flat zero lines, no lines starting midway
5. **Visual verification is mandatory** — check every page after every deploy using Claude in Chrome or screenshots
6. **Never deploy without building** — `npm run build` first, always
7. **Spot-check one event** — trace one fight's numbers from registry → table
8. **Read domain knowledge first** — `ufc_betting_domain_knowledge.md` before any UFC website work
9. **Never overwrite algorithm_stats.json version** — only update P/L fields, never touch version fields
10. **Consistent charts everywhere** — if one chart shows 5 bet types, ALL charts must show 5
11. **NEVER say "looks correct" without checking each item** — read ~/.claude/memory/topics/ufc_website_maintenance_rules.md BEFORE reviewing any screenshot. Check each of the 15 items individually with specific values.
12. **Both parlays must appear** — High Confidence parlay AND High ROI parlay. If only one shows, the second is broken.
13. **Combo bets must appear on picks cards** — every fight with method AND round prediction shows a combo bet. If NONE show combos, rendering is broken.
14. **Gating must be enforced visually** — if SUB gating is on, NO "by SUB" in recommended bets. If round gating applies, NO round bet displayed.
15. **Event detail pages show full P/L** — every LOST prop bet = -1u (not blank), every WON prop bet = units at odds (not blank), parlay results shown.

## MANDATORY PRE-REVIEW STEP (Added 2026-03-25)

**Before reviewing ANY UFC website screenshot or claiming ANY page "looks correct":**
1. Read `~/.claude/memory/topics/ufc_website_maintenance_rules.md`
2. Check EACH item on the 15-item checklist
3. State specific values for each check, not "looks fine"
4. If you can't verify something, say "UNABLE TO VERIFY" — do NOT assume correct

**This step exists because on 2026-03-24, the AI said "no obvious bugs" while 260% confidence values, SUB-gated bets, missing combos, missing parlay, empty optimizer values, and broken event detail P/L were ALL visible on screen.**
