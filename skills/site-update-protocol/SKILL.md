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

## Rules

1. **All 5 bet types on every page** — if any page shows fewer than 5, the deploy is broken
2. **No 0.00u with wins** — display "✓ —" for wins without odds, never "✓ 0.00u"
3. **Fighter loss = -1.00u in every column** — not "X —", show the actual -1.00u
4. **Chart starts at event 1** — no flat zero lines
5. **Visual verification is mandatory** — check every page after every deploy
6. **Never deploy without building** — `npm run build` first, always
7. **Spot-check one event** — trace one fight's numbers from registry → table
