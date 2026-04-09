# Learned Bugs — UFC Hypothesis Tester

> Auto-appended after each hypothesis session. Read at start of every new session (Step 0).
> Pattern-match your hypothesis against known failure modes before writing code.
> If your hypothesis touches method/combo settlement, scoring gates, or odds lookups — check LB-001 and LB-007 first.

## Format

Each entry: Date | Bug Name | Symptom | Root Cause | Time Wasted | Prevention Rule

---

## 2026-04-08 — Hypothesis 6: Grappling-Gate SUB Method Betting

### LB-001: Zero-Delta from Signature Preservation (CRITICAL — 45 min)
- **Symptom**: 21 gate activations, settlement loop computes new method/combo P/L, but archived output shows zero delta across all streams
- **Root Cause**: `_build_registry_event_entry()` (line ~1787) deep-copies existing bouts via signature match `(picked, predicted_method, predicted_round)`. Hypothesis changed method settlement (SUB vs DEC odds lookup) WITHOUT changing prediction signature → old P/L from template registry was preserved in the deep copy, overwriting settlement loop's new values.
- **Time Wasted**: ~45 minutes (3 full backtest runs + extensive debugging across 3 P/L paths)
- **Prevention**: Any hypothesis that changes method/combo settlement logic (different odds, different method key, different gating) without changing the prediction signature MUST patch the preserved bout's P/L fields from the settlement path:
  ```python
  # After: preserved_bout = json.loads(json.dumps(existing_bout))
  if fb.get("_method_pnl") is not None:
      preserved_bout["method_placed"] = fb.get("_method_placed", preserved_bout.get("method_placed"))
      preserved_bout["method_correct"] = fb.get("_method_result") if fb.get("_method_placed") else preserved_bout.get("method_correct")
      preserved_bout["method_pnl"] = fb.get("_method_pnl")
  if fb.get("_combo_pnl") is not None:
      preserved_bout["combo_placed"] = fb.get("_combo_placed", preserved_bout.get("combo_placed"))
      preserved_bout["combo_correct"] = fb.get("_combo_result") if fb.get("_combo_placed") else preserved_bout.get("combo_correct")
      preserved_bout["combo_pnl"] = fb.get("_combo_pnl")
  ```
- **Trigger Pattern**: Hypothesis modifies settlement WITHOUT changing `predicted_method` or `predicted_round` in the bout entry.

### LB-002: Skipping Preservation Causes Regression (-25.91u)
- **Symptom**: First attempted fix for LB-001 — skip signature preservation entirely when gate is active → -25.91u regression (spurious ML loss, -27u parlay crash)
- **Root Cause**: Fresh bout construction uses different ML odds than the preserved bout. Signature preservation keeps ML and odds fields stable. Skipping it introduces ML divergence which cascades into parlay calculations.
- **Time Wasted**: ~15 minutes (1 extra backtest run + rollback)
- **Prevention**: NEVER skip signature preservation entirely. Always deep-copy the existing bout, then PATCH only the specific fields your hypothesis changes (method_pnl, combo_pnl, etc.).

### LB-003: Debug Print Before Variable Assignment
- **Symptom**: Debug output shows `_bet_method=DEC` even when `_sub_grapple_active=True`
- **Root Cause**: Debug print was placed at line ~10570 (after gate check) but BEFORE `_bet_method = "SUB"` assignment at line ~10582. The printed value was from the previous loop iteration.
- **Time Wasted**: ~10 minutes (false conclusion that gate wasn't working)
- **Prevention**: In the settlement loop, ALWAYS place debug prints AFTER the variable being debugged is assigned. The settlement loop reuses variables across iterations — stale values from previous fights will mislead.

### LB-004: fight_breakdowns.json != In-Memory Dict
- **Symptom**: Checked `fight_breakdowns.json` for `red_url`/`blue_url` → "MISSING". Concluded settlement path couldn't access fighter URLs.
- **Root Cause**: `fight_breakdowns.json` is a simplified export written at a different point. The in-memory `fight_breakdowns` list (constructed at line ~10213) includes `'red_url': red["url"]`, `'blue_url': blue["url"]`, and all scoring fields. The settlement loop iterates the in-memory list, not the JSON file.
- **Time Wasted**: ~10 minutes (false investigation into URL availability)
- **Prevention**: To understand what's available in the settlement loop, read the dict construction at line ~10213 in the code, NOT the `fight_breakdowns.json` file. They are different structures.

### LB-005: Generic Grep Overcounting Activations
- **Symptom**: `grep -c "grapple" backtest_hypothesis.log` returned 623 matches. Interpreted as 623 gate activations.
- **Root Cause**: Generic string "grapple" matches function names, variable names, code references, log headers — not just actual activation events. Real activations were 21.
- **Time Wasted**: ~5 minutes (false confidence that gate was firing massively)
- **Prevention**: Always instrument hypothesis activations with a UNIQUE tag string that only appears when the gate actually fires:
  ```python
  if not QUIET_MODE:
      print(f"[GRAPPLE_GATE_ACTIVE] {picked_name} SubAvg={sub_avg:.2f} OppTDDef={opp_tdd:.1f}%")
  ```
  Then grep for `[GRAPPLE_GATE_ACTIVE]` specifically.

### LB-006: Wrong Archived Backtest File
- **Symptom**: Read archived file showing 484 bouts (354+130) instead of expected ~580 (401+153 based on v11.25.0 baseline)
- **Root Cause**: Multiple `backtest_runs/*.json` files from different runs exist. Glob pattern `sorted(glob.glob(...))[-1]` picked the most recent file, which was from an intermediate/partial run.
- **Time Wasted**: ~5 minutes (comparing wrong numbers to baseline)
- **Prevention**: After reading ANY archived file, immediately verify:
  ```python
  d = json.load(open(path))
  ml_parts = d['ml_record'].split('-')
  total_bouts = int(ml_parts[0].replace('W','')) + int(ml_parts[1].replace('L',''))
  assert total_bouts >= 550, f"WRONG FILE: only {total_bouts} bouts (expected ~580)"
  assert d.get('event_count', 0) >= 75, f"WRONG FILE: only {d.get('event_count')} events"
  ```

### LB-008: Fight Tuple Element Dropped by valid_fights Reconstruction (2026-04-09)
- **Symptom**: Added 13th tuple element (`opp_fight_count`) to `get_last_5_fights()` return value, diagnostic prints show all `opp_ufc_fights: ['?', '?', '?', '?', '?']`, modifier never fires, zero delta across all runs including extreme stress test (1.50x bonus + 0.50x penalty simultaneously)
- **Root Cause**: `calculate_adjusted_sl_ratio()` (line ~8307-8320) reconstructs fight tuples from the raw `fights` list into a `valid_fights` list. The `valid_fights.append()` call hardcodes exactly 12 elements extracted from `fight[0]` through `fight[11]`. Any element added beyond index 11 in `get_last_5_fights()` is silently dropped. The modifier code then does `_wf[12] if len(_wf) > 12 else 0` — always falls back to 0 since the tuple is always exactly 12 elements.
- **Time Wasted**: ~3 full backtest runs (stress test 1.50/0.50, threshold sweep, re-implementation attempts)
- **Prevention**: When adding a new field to the fight tuple in `get_last_5_fights()`, you MUST also:
  1. Add `new_field_f = fight[N] if len(fight) > N else default` at line ~8318
  2. Include `new_field_f` in the `valid_fights.append(...)` tuple
  3. Add a new `len(fight_data) == N+1` case to the unpacking block at line ~8368
  Diagnostic check: after first run, print tuple length inside modifier loop — `len(_wf)` must equal the expected count. If it equals 12 when you added a 13th element, the reconstruction is dropping it.

### LB-009: Zero Mixed Windows = Zero Effect (Uniform Multiplier Cancels After Normalization) (2026-04-09)
- **Symptom**: Running 3 full backtests at threshold 3 (all reasonable multiplier values) shows exactly +0.00u delta. No pick flips. Diagnostic confirms modifier fires (5776 activations) but result is identical to baseline.
- **Root Cause**: The recency weight modifier only changes picks when the 5-fight window has a MIX of fights above and below threshold. At threshold 3, EVERY fighter in the backtest dataset has all 5 opponents with 3+ UFC fights (0 mixed windows out of 556 windows). All 5 weights get the same multiplier (e.g., 1.10x). After normalization `w / sum(w)`, a uniform multiplier cancels out: `1.10 * w_i / (1.10 * sum(w))` = `w_i / sum(w)`. The weights are mathematically unchanged.
- **Time Wasted**: ~3 backtest runs burned before diagnosing
- **Prevention**: Before sweeping any weight-modifier hypothesis, run the mixed-window diagnostic FIRST:
  ```python
  # For each threshold, count windows with mixed above/below
  for thresh in [3, 4, 5, 6, 8, 10]:
      mixed = sum(1 for name, counts in fighters.items()
                  if 0 < sum(c >= thresh for c in counts) < len(counts))
      print(f'Threshold {thresh}: {mixed} mixed windows')
  ```
  If `mixed == 0` for your threshold → skip it entirely. The minimum useful threshold is the one where mixed > 0. At threshold 3, mixed = 0. At threshold 5, mixed = 173 (31%). Use this diagnostic before ANY threshold sweep.

### LB-007: Canonicalize Overwrites Hypothesis P/L
- **Symptom**: Registry P/L for hypothesis bouts showed `method_placed=False, method_pnl=None` even though settlement path set `fb['_method_placed']=True, fb['_method_pnl']=+3.0`
- **Root Cause**: `_canonicalize_profit_registry_after_backtest()` (line ~2008) runs `fix_bout()` on every bout after the registry is built. `fix_bout()` in `fix_registry_placed_flags.py` applies the standard SUB→DEC fallback (line 432-434) without grappling gate awareness, overwriting the hypothesis's SUB method P/L.
- **Time Wasted**: ~15 minutes (tracing through determine_placed_flags → fix_bout → recompute pipeline)
- **Prevention**: Two options:
  1. Store a flag (`sub_grapple_gate: True`) in the bout entry so `fix_bout()` can respect it and skip the SUB→DEC fallback
  2. Ensure the settlement path sets `method_pnl` to a non-None value AND the registry builder transfers it, so `fix_bout()` sees existing P/L and doesn't recalculate
  Option 2 was used for Hypothesis 6: the registry builder patches P/L from `fb['_method_pnl']`, and `determine_placed_flags()` preserves bouts where `method_pnl is not None`.
