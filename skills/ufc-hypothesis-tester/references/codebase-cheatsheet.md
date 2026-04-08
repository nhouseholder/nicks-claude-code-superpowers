# UFC Algorithm Codebase Cheatsheet
# UFC_Alg_v4_fast_2026.py — v11.24.0

Exact line numbers shift after edits. Verify with grep before using.

---

## File Paths (project root: ~/Projects/mmalogic or ~/ProjectsHQ/mmalogic)

```
UFC_Alg_v4_fast_2026.py             ← production algorithm (NEVER modify directly)
UFC_Alg_v4_fast_2026_HYPOTHESIS.py  ← hypothesis copy (create fresh for each test)
ufc_backtest_registry.json          ← fighter data (fight_history, career_stats)
ufc_profit_registry.json            ← P/L results (overwritten by each backtest)
ufc_odds_cache.json                 ← ML odds for 76 events (June 2024–April 2026)
ufc_prop_odds_cache.json            ← Method/round/combo odds
ufc_ou_odds_cache.json              ← Over/under odds
ufc_temporal_stats_cache.json       ← Time-slice career stats (1,859 fighters)
backtest_baseline_v{VERSION}.json   ← Saved baseline from fresh clean run
backtest_runs/EXPERIMENT_LOG.md     ← Experiment history (never delete)
backtest_runs/{version}_{date}.json ← Archived backtest results
algorithm_stats.json                ← Website data (overwritten by each backtest)
fight_breakdowns.json               ← Per-fight pick data (overwritten by each backtest)
```

---

## Imports (line 24)

```python
from datetime import datetime, timedelta  # datetime = CLASS not module
```

**CRITICAL consequences:**
- `datetime.date` → does NOT exist (AttributeError)
- `datetime.fromisoformat(s)` → parses datetime (Python 3.7+)
- `datetime.strptime(s, "%Y-%m-%d").date()` → parses to date ✓ USE THIS
- `datetime.now()` → works ✓
- `datetime.strptime(s, "%Y-%m-%d")` → works ✓

---

## fight_history Data Format (ufc_backtest_registry.json)

```python
# Fighter struct
{
  "name": "Alex Pereira",
  "ufc_fight_count": 12,          # ← direct field, use this for veteran check
  "fight_history": [
    {
      "date": "2024-11-16",         # YYYY-MM-DD string
      "opponent_name": "Khalil Rountree",
      "opponent_url": "http://www.ufcstats.com/fighter-details/...",
      "result": "WIN",              # ← "WIN" or "LOSS" (NOT 'W' or 'L')
      "method": "KO/TKO",
      "round": 3,
      "time": "2:58",
      "is_top_position": True,      # True = red corner (usually favorite)
      "kd_top": 2, "kd_bot": 0,
      "ss_top": 45, "ss_bot": 12,
      "bout_url": "http://www.ufcstats.com/fight-details/...",
      "fight_minutes": 12.97
      # NOTE: NO historical odds, NO event name, NO fight_number
    }
  ]
}
```

**How to access in a new function:**
```python
def _my_function(fighter_url, fighter_name, cutoff_date):
    reg = _load_backtest_registry()          # cached global — call freely
    fd = reg.get("fighters", {}).get(fighter_url, {})
    fh = fd.get("fight_history", [])
    ufc_count = fd.get("ufc_fight_count", 0) or 0   # always use 'or 0' guard
    
    for fight in fh:
        result = fight.get("result", "")
        if result not in ("WIN", "LOSS"):    # NOT ('W', 'L')
            continue
        try:
            fh_date = datetime.strptime(fight.get("date", "1900-01-01"), "%Y-%m-%d").date()
            if cutoff_date and fh_date >= cutoff_date:
                continue
        except (ValueError, TypeError):
            continue
        # ... your logic
```

---

## Key Constants (v11.24.0)

| Constant | Line | Value | Notes |
|----------|------|-------|-------|
| `ALG_VERSION` | 8 | `"11.24.0"` | Must bump for any shipped change |
| `PICK_DIFF_THRESHOLD` | 189 | `0.14` | Min score diff to place a bet |
| `FIGHT_ADJUSTED_CAP` | 192 | `2.80` | Max adjusted SL ratio |
| `WIN_STREAK_BONUS` | 360 | `0.036` | → Insert new constants HERE |
| `STRDEF_COEFF` | 361 | `0.34` | |
| `RATIO_MIN` | 517 | `0.21` | |
| `RATIO_MAX` | 518 | `4.10` | |
| `OPP_SL_FLOOR` | 521 | `0.30` | |
| `MIN_OPP_UFC_FIGHTS` | 545 | `1` | Effectively no filter |
| `SYSTEM_SCORE_WEIGHT` | ~398 | `0.05` | Systems layer weight |

**To flip the closest pick, modifier must be > `PICK_DIFF_THRESHOLD = 0.14`.**

---

## Code Insertion Points

### New Constants
```
After line 360 (WIN_STREAK_BONUS = 0.036)
```

### New Helper Functions
```
After line 8196 ("return None" at end of get_last_5_fights)
Before line 8194 ("def calculate_adjusted_sl_ratio")
```

### Modifier Block in Fight Loop
```
After line 9478: red_ml, blue_ml = lookup_fight_odds(event_odds, red["name"], blue["name"])
Before line 9481: fight_props = lookup_fight_prop_odds(...)
```
Note: Line numbers shift by ~120+ in the HYPOTHESIS copy due to added code.
Always grep for the anchor text rather than using line numbers directly.

---

## Fight Loop Variables (available at modifier insertion point)

```python
red["name"]          # str: red corner fighter name
red["url"]           # str: fighter URL (use for registry lookup)
blue["name"]         # str: blue corner fighter name  
blue["url"]          # str: fighter URL
red_score            # float: current red score (modify directly)
blue_score           # float: current blue score (modify directly)
red_ml               # int|None: red ML odds (e.g. -150, +130)
blue_ml              # int|None: blue ML odds
temporal_cutoff      # date|None: event date cutoff (None in prediction mode)
event_date           # date: current event's date
BACKTEST_MODE        # bool: True during backtest
QUIET_MODE           # bool: True suppresses print statements
```

**Favorite/underdog determination:**
```python
red_is_dog = (red_ml is not None and red_ml > 0)   # positive odds = underdog
```

---

## Odds Cache Format (ufc_odds_cache.json)

```python
{
  "UFC 325: Volkanovski vs. Lopes 2": {
    "alexander volkanovski|||diego lopes": [-154, 130],
    # key: "fighter1_lower|||fighter2_lower"
    # value: [ml1, ml2] — ml1 for fighter1, ml2 for fighter2
  }
}
```

**Loaded at runtime** via `_load_odds_cache()` → converted to tuple keys for `lookup_fight_odds()`.

**Coverage**: 76 events, June 2024–April 2026 only. Older events have no ML odds.

**To build a flat lookup across all events:**
```python
flat_lookup = {}
with open("ufc_odds_cache.json") as f:
    raw = json.load(f)
for event, matchups in raw.items():
    for key_str, odds in matchups.items():
        parts = key_str.split("|||")
        if len(parts) == 2:
            pair = frozenset([parts[0], parts[1]])
            flat_lookup.setdefault(pair, []).append((parts[0], parts[1], odds[0], odds[1]))
```

---

## Backtest Run Commands

```bash
# Standard hypothesis backtest (from project root)
UFC_BACKTEST_MODE=1 UFC_CACHE_ONLY=1 python3 UFC_Alg_v4_fast_2026_HYPOTHESIS.py 2>&1 | tee backtest_hypothesis.log | tail -5

# Production baseline (restore first)
UFC_BACKTEST_MODE=1 UFC_CACHE_ONLY=1 python3 UFC_Alg_v4_fast_2026.py 2>&1 | tail -5

# Read archived result (use THIS not registry totals)
python3 -c "
import json, glob
runs = sorted(glob.glob('backtest_runs/*.json'))
latest = [r for r in runs if 'EXPERIMENT' not in r][-1]
d = json.load(open(latest))
print(f'Combined: {d[\"combined_pnl\"]:+.2f}u  ML: {d[\"ml_record\"]}')
parlay = d['combined_pnl'] - d['ml_pnl'] - d['method_pnl'] - d['combo_pnl'] - d['ou_pnl']
print(f'ML: {d[\"ml_pnl\"]:+.2f}  Method: {d[\"method_pnl\"]:+.2f}  Combo: {d[\"combo_pnl\"]:+.2f}  OU: {d[\"ou_pnl\"]:+.2f}  Parlay: {parlay:+.2f}')
"
```

---

## Git Restore Command (restore ALL data files before each run)

```bash
git restore ufc_backtest_registry.json ufc_profit_registry.json algorithm_stats.json \
  backtest_runs/latest.json backtest_summary.json fight_breakdowns.json \
  ufc_systems_registry.json \
  webapp/frontend/public/data/algorithm_stats.json \
  webapp/frontend/public/data/backtest_summary.json \
  webapp/frontend/public/data/hero_stats.json \
  webapp/frontend/public/data/ufc_profit_registry.json \
  webapp/frontend/public/data/ufc_systems_registry.json
```

Verify after restore:
```bash
python3 -c "import json; print('Combined:', json.load(open('ufc_profit_registry.json'))['totals']['combined'])"
```

---

## True Current Baseline (v11.24.0, 75 events, fresh run 2026-04-08)

| Stream | P/L | Record |
|--------|-----|--------|
| ML | +131.38u | 401W-153L |
| Method | +171.68u | 162W-201L |
| Round | 0.00u | DISABLED |
| Combo | +132.39u | ~42W-62L |
| O/U | +88.10u | ~163W-73L |
| Parlay | +246.96u | — |
| **Combined** | **+770.51u** | |

Note: 745.78u was a stale incremental baseline. 770.51u is the true fresh-run value.

---

## Known Errors & Fixes (from this codebase)

| Error | Cause | Fix |
|-------|-------|-----|
| `AttributeError: 'method_descriptor' has no 'fromisoformat'` | Used `datetime.date.fromisoformat()` when `datetime` = CLASS | `datetime.strptime(s, "%Y-%m-%d").date()` |
| Zero activations, no error | `result not in ('W', 'L')` filters everything | `result not in ("WIN", "LOSS")` |
| False baseline delta | Reading totals from `ufc_profit_registry.json` instead of archived run | Read from `backtest_runs/*.json` archived file |
| All sweep values identical | Not restoring data files between runs | `git restore` all 12 files before each run |
| `ufc_fight_count` = 0 for all fighters | `fd.get('ufc_fight_count', 0)` returns `None` not `0` | `fd.get('ufc_fight_count', 0) or 0` |

---

## Useful Validation Commands

```bash
# After any registry modification
python3 validate_registry_cells.py --strict
python3 verify_registry.py

# Check event count in registry
python3 -c "import json; d=json.load(open('ufc_profit_registry.json')); print(len(d['events']), 'events')"

# Check fighter count in backtest registry
python3 -c "import json; d=json.load(open('ufc_backtest_registry.json')); print(len(d.get('fighters',{})), 'fighters')"

# Quick data format sanity check (run before writing new code)
python3 -c "
import json
d = json.load(open('ufc_backtest_registry.json'))
f = list(d['fighters'].values())[0]
fh = f.get('fight_history', [])
print('result values:', set(fight.get('result') for fight in fh[:20]))
print('ufc_fight_count:', f.get('ufc_fight_count'))
print('date format:', fh[0].get('date') if fh else 'no fights')
"
```
