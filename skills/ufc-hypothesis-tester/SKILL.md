---
name: ufc-hypothesis-tester
description: >
  UFC algorithm hypothesis tester — the ONLY agent that should run algorithm experiments for mmalogic/OctagonAI.
  Encodes all codebase-specific knowledge: correct data formats, safe baseline workflow, activation verification,
  clean state management, coefficient sweep protocol, and mandatory experiment logging.
  ALWAYS use this skill when the user says any of: "test a theory", "test this in the backtester",
  "hypothesis", "try this idea in the algorithm", "would X improve picks", "backtest experiment",
  "parameter sweep", "coefficient sweep", "test this modifier", "does X help", "add X to the algorithm
  and test it", or anything involving modifying UFC_Alg_v4_fast_2026.py and running a backtest.
weight: heavy
---

# UFC Hypothesis Tester

Single source of truth for algorithm hypothesis testing. Every step is mandatory. Every trap is documented.

> Read `references/codebase-cheatsheet.md` for exact line numbers, variable names, and data format specs.

---

## Step 0: Pre-Compute Gate (Run BEFORE Any Code)

**First:** Read `references/LEARNED_BUGS.md` for bugs from previous sessions. Pattern-match your hypothesis against known failure modes before writing code. Pay special attention to LB-001 (signature preservation zero-delta) if your hypothesis changes method/combo settlement.

Answer these 3 questions. If all can be answered without a full backtest, skip to logging.

1. **Can math answer this?** What is the typical score differential? Does the proposed modifier cross the `PICK_DIFF_THRESHOLD = 0.14`? If `proposed_coeff < min_score_diff` → zero pick flips guaranteed → reject immediately.

2. **Can a 10-line script answer this?** Load the odds cache, registry, or fight_breakdowns.json and count how many fights match the proposed condition. If N < 10 → too few activations to matter.

3. **Is the approach locked?** Write ONE sentence: "I will test X using Y with coefficient Z." If you can't state this, resolve the ambiguity before writing a line of code.

Pre-compute diagnostic template:
```bash
python3 -c "
import json
with open('ufc_backtest_registry.json') as f:
    reg = json.load(f)
fighters = reg.get('fighters', {})
# Count fighters meeting the hypothesis condition
qualifying = 0
for url, fd in fighters.items():
    fh = fd.get('fight_history', [])
    # YOUR CONDITION HERE (use 'WIN'/'LOSS' not 'W'/'L')
    qualifying += 1  # increment when condition met
print(f'Qualifying fighters: {qualifying} of {len(fighters)}')
"
```

---

## Architecture: 3 P/L Computation Paths (READ BEFORE DEBUGGING)

> This section explains why hypothesis changes can produce **zero delta** even when the code activates correctly. See `references/codebase-cheatsheet.md` for line numbers and code examples.

The algorithm has 3 separate P/L paths. A hypothesis change must flow through ALL 3 to appear in the archived output.

**Path 1: Settlement Loop** (line ~10521) — Computes in-memory `fb['_method_pnl']`, `fb['_combo_pnl']` during per-fight iteration. Your hypothesis code goes here.

**Path 2: Registry Builder** (line ~1723) — `_build_registry_event_entry()` constructs bout entries for the profit registry. **CRITICAL TRAP:** Signature preservation at line ~1787 deep-copies existing bouts when `(picked, predicted_method, predicted_round)` matches. If your hypothesis changes settlement logic WITHOUT changing the prediction signature → old P/L is silently preserved.

**Path 3: Canonicalize + Regenerate** (line ~2008) — `_canonicalize_profit_registry_after_backtest()` runs `fix_bout()` on every bout, then `recompute_event_totals()` sums P/L. **The archived output reads from THIS path**, not from the settlement loop.

### The Zero-Delta Rule
**If your hypothesis changes HOW a bet is settled (different odds, different method key, different gating) without changing the prediction signature → you MUST patch the registry builder's preserved bout with settlement P/L.** Otherwise the deep copy preserves old values and your change is invisible.

### Never Skip Preservation
Skipping signature preservation entirely causes -25.91u regression (ML/odds instability, parlay crash). Always PATCH specific fields after the deep copy — never skip the copy itself.

See `references/codebase-cheatsheet.md` → "3 P/L Computation Paths" and "Registry Builder Signature Preservation" for exact code.

---

## Step 1: Establish Fresh Baseline (MANDATORY — one-time per session)

**NEVER** use `ufc_profit_registry.json` totals as the baseline. Always get it from a fresh run.

```bash
# 1. Restore all data files to HEAD
git restore ufc_backtest_registry.json ufc_profit_registry.json algorithm_stats.json \
  backtest_runs/latest.json backtest_summary.json fight_breakdowns.json \
  ufc_systems_registry.json \
  webapp/frontend/public/data/algorithm_stats.json \
  webapp/frontend/public/data/backtest_summary.json \
  webapp/frontend/public/data/hero_stats.json \
  webapp/frontend/public/data/ufc_profit_registry.json \
  webapp/frontend/public/data/ufc_systems_registry.json

# 2. Run clean production algorithm
UFC_BACKTEST_MODE=1 UFC_CACHE_ONLY=1 python3 UFC_Alg_v4_fast_2026.py 2>&1 | tail -5

# 3. Read the archived result (NOT the registry totals)
python3 -c "
import json, glob
runs = sorted(glob.glob('backtest_runs/*.json'))
latest = [r for r in runs if 'EXPERIMENT' not in r][-1]
d = json.load(open(latest))
print(f'Baseline: {d[\"combined_pnl\"]:+.2f}u')
print(f'ML: {d[\"ml_pnl\"]:+.2f}u {d[\"ml_record\"]}')
print(f'Method: {d[\"method_pnl\"]:+.2f}u {d[\"method_record\"]}')
print(f'Combo: {d[\"combo_pnl\"]:+.2f}u')
print(f'OU: {d[\"ou_pnl\"]:+.2f}u')
parlay = d['combined_pnl'] - d['ml_pnl'] - d['method_pnl'] - d['combo_pnl'] - d['ou_pnl']
print(f'Parlay: {parlay:+.2f}u')
print(f'File: {latest}')
"
```

Save these numbers to `backtest_baseline_v{VERSION}.json` (overwrite if stale). This JSON is the single source of truth for all comparisons this session.

---

## Step 2: Create Hypothesis File

```bash
# Create hypothesis copy — never modify the production file
cp UFC_Alg_v4_fast_2026.py UFC_Alg_v4_fast_2026_HYPOTHESIS.py
echo "Hypothesis copy created: $(wc -l UFC_Alg_v4_fast_2026_HYPOTHESIS.py | awk '{print $1}') lines"
```

---

## Step 3: Implement the Hypothesis

### MANDATORY: Check these before writing ANY code

**1. Data format check** (run first, write code second):
```bash
python3 -c "
import json
with open('ufc_backtest_registry.json') as f:
    reg = json.load(f)
f = list(reg['fighters'].values())[0]
fh = f['fight_history']
if fh:
    print('result field:', repr(fh[0].get('result')))      # 'WIN' or 'LOSS' — NOT 'W'/'L'
    print('date field:', repr(fh[0].get('date')))           # '2024-06-01' format
    print('keys:', list(fh[0].keys()))
    print('ufc_fight_count:', f.get('ufc_fight_count'))
"
```

**2. Import pattern check** (before using any stdlib function):
```bash
grep -n "^import datetime\|^from datetime" UFC_Alg_v4_fast_2026_HYPOTHESIS.py | head -3
# Expected: "from datetime import datetime, timedelta"
# This means: datetime = CLASS (not module)
# CORRECT: datetime.strptime(date_str, "%Y-%m-%d").date()
# WRONG:   datetime.date.fromisoformat(date_str)  ← AttributeError
```

### Code template for new modifier functions

```python
# ── Hypothesis N: [Name] ──
# Constants (add near line 360, after WIN_STREAK_BONUS)
HYPO_COEFF       = 0.12   # modifier weight — start here, sweep up
HYPO_MIN_FIGHTS  = 8      # veteran threshold

def _get_hypo_modifier(fighter_url, fighter_name, cutoff_date):
    """Returns modifier float or 0.0 if insufficient data."""
    reg = _load_backtest_registry()  # cached global — safe to call repeatedly
    fd = reg.get("fighters", {}).get(fighter_url, {})
    fh = fd.get("fight_history", [])
    if not fh:
        return 0.0

    qualifying = 0
    for fight in fh:
        result = fight.get("result", "")
        if result not in ("WIN", "LOSS"):  # ← 'WIN'/'LOSS' not 'W'/'L'
            continue
        try:
            # ← datetime.strptime not datetime.date.fromisoformat
            fh_date = datetime.strptime(fight.get("date", "1900-01-01"), "%Y-%m-%d").date()
            if cutoff_date and fh_date >= cutoff_date:
                continue
        except (ValueError, TypeError):
            continue
        qualifying += 1

    if qualifying < HYPO_MIN_FIGHTS:
        return 0.0

    # YOUR LOGIC HERE
    return 0.0
```

### Where to insert code

See `references/codebase-cheatsheet.md` for exact current line numbers. Key insertion points:
- **Constants**: after `WIN_STREAK_BONUS` (~line 360)
- **Helper functions**: after `get_last_5_fights()` ends (~line 8197), before `calculate_adjusted_sl_ratio()`
- **Modifier block**: after `red_ml, blue_ml = lookup_fight_odds(event_odds, ...)` (~line 9607 in hypothesis copy)
- `temporal_cutoff` is available in scope throughout the fight loop (set at event start, line ~9033)
- `red["url"]`, `blue["url"]`, `red["name"]`, `blue["name"]` are the correct field names

---

## Step 4: Activation Diagnostic (MANDATORY — run BEFORE full backtest)

Count how many fighters actually qualify BEFORE burning 5+ minutes on a full run:

```bash
python3 -c "
import json, datetime

# Adjust this to match your hypothesis condition
COEFF_NAME = 'HYPO_COEFF'   # change to your constant name
MIN_FIGHTS = 8

with open('ufc_backtest_registry.json') as f:
    reg = json.load(f)

qualifying = 0
total_vets = 0
for url, fd in reg.get('fighters', {}).items():
    count = fd.get('ufc_fight_count', 0) or 0
    if count < MIN_FIGHTS:
        continue
    total_vets += 1
    fh = fd.get('fight_history', [])
    valid = [f for f in fh if f.get('result') in ('WIN', 'LOSS')]
    if len(valid) >= MIN_FIGHTS:
        qualifying += 1

print(f'Veterans ({MIN_FIGHTS}+ fights): {total_vets}')
print(f'Qualifying for modifier: {qualifying}')
print(f'Rate: {qualifying/total_vets*100:.1f}%' if total_vets else 'n/a')
" 2>&1
```

**Decision gate:**
- `qualifying = 0` → bug in your code. Check data format, date parsing, import pattern. Do NOT proceed.
- `qualifying < 10` → too sparse. The modifier cannot generalize. Reject or redesign.
- `qualifying >= 20` → proceed to full backtest.

---

## Step 5: First Full Backtest + Immediate Verification

```bash
# Restore clean state first
git restore ufc_backtest_registry.json ufc_profit_registry.json algorithm_stats.json \
  backtest_runs/latest.json backtest_summary.json fight_breakdowns.json \
  ufc_systems_registry.json \
  webapp/frontend/public/data/algorithm_stats.json \
  webapp/frontend/public/data/backtest_summary.json \
  webapp/frontend/public/data/hero_stats.json \
  webapp/frontend/public/data/ufc_profit_registry.json \
  webapp/frontend/public/data/ufc_systems_registry.json

# Run hypothesis
UFC_BACKTEST_MODE=1 UFC_CACHE_ONLY=1 python3 UFC_Alg_v4_fast_2026_HYPOTHESIS.py 2>&1 | tee backtest_hypothesis.log | tail -5
```

**Immediately after the run**, verify activations fired before interpreting results:

```bash
# Check 1: Did the modifier print anything? (only works if QUIET_MODE was off)
grep -c "\[YOUR_TAG\]" backtest_hypothesis.log 2>/dev/null || echo "0 prints (QUIET_MODE on — use diagnostic script)"

# Check 2: Did ML record change? (key signal — if same as baseline, modifier had zero effect)
python3 -c "
import json, glob
runs = sorted(glob.glob('backtest_runs/*.json'))
latest = [r for r in runs if 'EXPERIMENT' not in r][-1]
d = json.load(open(latest))
print(f'Hypothesis: {d[\"combined_pnl\"]:+.2f}u  ML: {d[\"ml_record\"]}')
print(f'Baseline ML record was: [paste from Step 1]')
print(f'Same ML record = modifier had zero pick-flip effect')
"
```

**If ML record is identical to baseline → modifier is not changing picks.**
Diagnose before sweeping. Do NOT run more coefficient values until you know why.

---

## Step 5.5: Zero-Delta Diagnostic (if first run shows zero delta despite activations)

If Step 5 shows identical P/L to baseline despite confirmed activations, **do NOT run more sweeps**. Debug in this order:

### 1. Check archived file integrity
```bash
python3 -c "
import json, glob
runs = sorted(glob.glob('backtest_runs/*.json'))
latest = [r for r in runs if 'EXPERIMENT' not in r][-1]
d = json.load(open(latest))
ml_parts = d['ml_record'].replace('W','').replace('L','').split('-')
total_bouts = int(ml_parts[0]) + int(ml_parts[1])
print(f'File: {latest}')
print(f'Bouts: {total_bouts} (expect ~580)')
print(f'Events: {d.get(\"event_count\", \"?\")} (expect 75)')
assert total_bouts >= 550, f'WRONG FILE — only {total_bouts} bouts'
"
```

### 2. Check registry builder signature preservation
Does your hypothesis change method/combo settlement WITHOUT changing `predicted_method` or `predicted_round`?
- YES → Signature preservation is deep-copying old P/L. You need to patch `preserved_bout["method_pnl"]` from `fb["_method_pnl"]` after the deep copy. See "Architecture" section above.
- NO → Proceed to check 3.

### 3. Check canonicalize path
Does `fix_bout()` in `fix_registry_placed_flags.py` re-apply default logic (e.g., SUB→DEC fallback at line 432) that overwrites your hypothesis P/L?
- YES → Store a flag in the bout entry so `fix_bout()` respects it, OR ensure your settlement P/L is non-None so `determine_placed_flags()` preserves it.
- NO → Proceed to check 4.

### 4. Debug with targeted prints
Place debug prints **AFTER** the variable assignment (not before — stale values from previous loop iteration will mislead). Use unique tags:
```python
if not QUIET_MODE and _hypo_active:
    print(f"[HYPO_ACTIVE] {picked_name} bet_method={_bet_method} method_odds={method_odds} pnl={fb.get('_method_pnl')}")
```
Then grep for `[HYPO_ACTIVE]` specifically — not generic strings like the function name.

### DO NOT: Skip signature preservation entirely
First instinct will be to skip the deep copy when your gate is active. This causes -25.91u regression from ML/odds instability and parlay crashes. Always PATCH, never SKIP.

---

## Step 6: Coefficient Sweep

Only if Step 5 showed the modifier IS changing results. Restore before each variant.

```bash
# Template — repeat for each COEFF value (e.g. 0.05, 0.12, 0.20, 0.40)
git restore ufc_backtest_registry.json ufc_profit_registry.json algorithm_stats.json \
  backtest_runs/latest.json backtest_summary.json fight_breakdowns.json \
  ufc_systems_registry.json \
  webapp/frontend/public/data/algorithm_stats.json \
  webapp/frontend/public/data/backtest_summary.json \
  webapp/frontend/public/data/hero_stats.json \
  webapp/frontend/public/data/ufc_profit_registry.json \
  webapp/frontend/public/data/ufc_systems_registry.json
# Then edit COEFF in HYPOTHESIS.py and re-run
```

**Sweep strategy:**
1. Start at the minimum effective coefficient (>0.14 to flip the closest pick)
2. If zero effect at first value → check activations (Step 4) before trying more values
3. If improvement → go up 50% increments until regression appears
4. If first value regresses → try 50% lower, but if still regressing → reject
5. **Identical results at 3+ values = dead feature. STOP. Do not continue sweeping.**

---

## Step 7: Compare Results

```bash
python3 -c "
import json, glob

baseline = {'ml': 0.0, 'method': 0.0, 'combo': 0.0, 'ou': 0.0, 'combined': 0.0}
# Fill in baseline numbers from backtest_baseline_v*.json

# Read all hypothesis runs
runs = sorted(glob.glob('backtest_runs/*.json'))
for path in [r for r in runs if 'EXPERIMENT' not in r][-5:]:
    d = json.load(open(path))
    print(f'{path.split(\"/\")[-1]}:')
    print(f'  Combined: {d[\"combined_pnl\"]:+.2f}u  (delta: {d[\"combined_pnl\"]-baseline[\"combined\"]:+.2f}u)')
    print(f'  ML: {d[\"ml_pnl\"]:+.2f}u  Method: {d[\"method_pnl\"]:+.2f}u  Combo: {d[\"combo_pnl\"]:+.2f}u')
"
```

Decision criteria:
- **SHIP if:** `combined_delta >= +5u` AND `ml_delta >= 0` AND no single stream regresses more than 10u
- **INVESTIGATE if:** `+1u <= combined_delta < +5u` — try one more coefficient value
- **REJECT if:** `combined_delta < 0` OR `combined_delta = 0` (no effect)

---

## Step 8: Decision + Cleanup

### If SHIPPING:
```bash
# 1. Copy hypothesis changes into production file (manual merge or diff)
diff UFC_Alg_v4_fast_2026.py UFC_Alg_v4_fast_2026_HYPOTHESIS.py
# 2. Bump version: ALG_VERSION = "11.25.0" in production file
# 3. Bump APP_VERSION in webapp/frontend/src/config/version.js
# 4. Delete hypothesis file
rm UFC_Alg_v4_fast_2026_HYPOTHESIS.py
```

### If REJECTING:
```bash
git restore ufc_backtest_registry.json ufc_profit_registry.json algorithm_stats.json \
  backtest_runs/latest.json backtest_summary.json fight_breakdowns.json \
  ufc_systems_registry.json \
  webapp/frontend/public/data/algorithm_stats.json \
  webapp/frontend/public/data/backtest_summary.json \
  webapp/frontend/public/data/hero_stats.json \
  webapp/frontend/public/data/ufc_profit_registry.json \
  webapp/frontend/public/data/ufc_systems_registry.json
rm UFC_Alg_v4_fast_2026_HYPOTHESIS.py
```

---

## Step 9: Log to EXPERIMENT_LOG.md (MANDATORY — no exceptions)

```bash
cat >> backtest_runs/EXPERIMENT_LOG.md << 'EOF'

---

## Session: [DATE] — Hypothesis [N]: [Name]

### Theory
[What was tested and why]

### Implementation
- Constants added: [list]
- Functions added: [list]  
- Insertion point: [line number and context]
- Data accessed: [fight_history / odds_cache / etc.]

### Baseline
Fresh run baseline: v[VERSION], [N] events, combined [+XXX.XXu]

### Per-Variant Results

| COEFF | Combined | Delta | ML | Method | Combo | O/U | Pick Flips |
|-------|----------|-------|----|--------|-------|-----|------------|
| X.XX  | +XXX.XXu | +X.Xu | ...| ...    | ...   | ... | N          |

### Why It Failed / Succeeded
[Root cause analysis — not just "it didn't work"]

### Interesting Findings
[Anything notable even from a rejection]

### Decision
**[SHIPPED / REJECTED]**

### Files
- `UFC_Alg_v4_fast_2026_HYPOTHESIS.py` — created and deleted
- Archived runs: [filenames]
EOF

git add backtest_runs/EXPERIMENT_LOG.md backtest_baseline_v*.json
git commit -m "Experiment log: [Hypothesis name] — [SHIPPED/REJECTED]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push origin main
```

---

## Known Traps (DO NOT REPEAT)

### Data Format & API Traps
| Trap | Symptom | Fix |
|------|---------|-----|
| `'W'`/`'L'` instead of `'WIN'`/`'LOSS'` | Zero activations, no error | Use `result not in ("WIN", "LOSS")` |
| `datetime.date.fromisoformat()` | AttributeError on fromisoformat | Use `datetime.strptime(d, "%Y-%m-%d").date()` |
| `ufc_fight_count` field | Wrong veteran count | Use `fd.get('ufc_fight_count', 0) or 0` — field exists directly on fighter dict |

### Comparison & Baseline Traps
| Trap | Symptom | Fix |
|------|---------|-----|
| Baseline from registry totals | Confounded comparison | Run fresh production baseline, use archived run file |
| No `git restore` between sweeps | All sweeps return same result | Restore all 12 data files before each run |
| Modifier fires but doesn't flip picks | All coefficients produce same P/L | Check: is `HYPO_COEFF` above the pick threshold (~0.14)? Count pick flips from ML record |
| Running sweeps before verifying activations | 3+ wasted runs | Always run activation diagnostic (Step 4) before first full backtest |
| Comparing hypothesis to wrong baseline | False +24u "improvement" | Verify baseline = fresh production run, not stale totals |
| Wrong archived file read | 484 bouts instead of 580 | Verify `events` count (>=75) + bout count (>=575) immediately after reading any archived file |

### P/L Pipeline Traps (learned 2026-04-08, Hypothesis 6)
| Trap | Symptom | Fix |
|------|---------|-----|
| Registry signature preservation | Zero delta despite activations (settlement computes new P/L, archived shows old) | Hypothesis changes settlement without changing prediction signature → deep copy preserves old P/L. Patch `method_pnl`/`combo_pnl` on preserved bout from `fb['_method_pnl']` after deep copy. See Step 5.5. |
| Skip preservation entirely | -25.91u regression, ML losses, parlay tanked (-27u) | NEVER skip signature preservation. Patch specific fields only. Deep copy keeps ML/odds stable. |
| `_canonicalize` overwrites P/L | `fix_bout()` re-applies SUB→DEC fallback, overwriting hypothesis settlement | Store a flag (e.g., `sub_grapple_gate: True`) in bout so `fix_bout()` respects it, OR ensure settlement P/L is non-None so `determine_placed_flags()` preserves it |
| Debug print before assignment | Stale variable value from previous loop iteration (e.g., `_bet_method=DEC` when gate is True) | In settlement loop, place debug prints AFTER the variable is assigned. Loop reuses variables across iterations. |
| `fight_breakdowns.json` != in-memory | URLs "missing" but actually present | JSON is simplified export. Read code at line ~10213 for in-memory structure, not the file. |
| Generic grep for activations | 623 false matches vs 21 real | Use specific tags: `[GATE_NAME_ACTIVE]` and grep for those exact strings |

---

## Step 10: Self-Learning Protocol (MANDATORY — after Step 9)

After every hypothesis test session, check for new bugs to record:

1. **Review**: Did any unexpected bugs occur during this session? (zero-delta, wrong file, debug confusion, etc.)
2. **If yes**, append a structured entry to `references/LEARNED_BUGS.md`:
   ```markdown
   ### LB-NNN: [Bug Name]
   - **Symptom**: [What you observed]
   - **Root Cause**: [Why it happened]
   - **Time Wasted**: [Approximate debugging time]
   - **Prevention**: [Rule to prevent recurrence]
   ```
3. **Number sequentially** — check the last LB-NNN in the file and increment
4. **Commit** the updated LEARNED_BUGS.md alongside EXPERIMENT_LOG.md:
   ```bash
   git add references/LEARNED_BUGS.md backtest_runs/EXPERIMENT_LOG.md
   # (or include in the experiment commit)
   ```

The goal: every debugging session that wastes >5 minutes teaches the next session to avoid the same trap. The LEARNED_BUGS.md file is read at Step 0 before any code is written.

---

> Full reference: `references/codebase-cheatsheet.md`
> Bug history: `references/LEARNED_BUGS.md`
