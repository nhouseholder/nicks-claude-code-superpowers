# Handoff — UFC Predict (mmalogic) — 2026-04-08 02:40
## Model: Claude Sonnet 4.6
## Previous handoff: handoff_ufc-predict_2026-04-07_1455_v11.23.5-ou-coverage-recovery.md
## GitHub repo: nhouseholder/ufc-predict
## Local path: /Users/nicholashouseholder/ProjectsHQ/mmalogic/
## Last commit date: 2026-04-08 02:34:35 -0700

---

## 1. Session Summary
The session expanded the backtest window from 71→75 events, ran the full optimizer (producing v11.24.0 with 63-param retune), validated and deployed it live, then researched and implemented significant optimizer improvements (v2): adaptive bounds, 75% faster runtime (37min→9.3min), and rebalanced prop weight. The v2 parameters were tested but showed holdout regression and were correctly NOT deployed — only the optimizer tooling was shipped.

## 2. What Was Done

- **Backtest window 71→75 events**: Added 4 events (Moicano vs Duncan, UFC 303, Namajunas vs Cortez, Whittaker vs Aliskerov) via two-pass expansion. Registry grew to 75 events, 580 bouts.
- **v11.24.0 optimizer run**: 63 params, 2-pass DE, 580 fights, 37 min. Validated at +755.36u combined (all streams).
- **v11.24.0 deployed**: Version bumped, picks regenerated for UFC 327 (11 picks), Cloudflare deploy, git push.
- **CLAUDE.md updated**: New baseline numbers documented (75 events, 580 bouts).
- **Optimizer v2 implemented** (commit `fcb23c0`):
  - Adaptive bounds: ±25% of current values, clamped to original safety rails — shrinks search space ~80%
  - Faster DE: Pass1 popsize 15→12, maxiter 200→150, patience 20→15; Pass2 popsize 10→8, maxiter 150→100, patience 15→12
  - PROP_PROFIT_WEIGHT: 0.5→0.75 (balanced — 1.0 tested, caused O/U overfitting on holdout)
  - Runtime: 37 min → 9.3 min (75% faster)
- **Optimizer v2 tested**: Both PROP_PROFIT_WEIGHT=1.0 and 0.75 tested. Train improved (+66u) but holdout regressed (-16.6u). New constants correctly NOT deployed — v11.24.0 params remain active.
- **Git cleanup**: Pulled remote (behind by 1), resolved merge conflicts on prediction_output.json and current_picks.json.

## 3. What Failed (And Why)

- **PROP_PROFIT_WEIGHT=1.0 overfits O/U**: Equal-weighting all bet types caused optimizer to chase O/U train gains (+43u on train) that don't generalize to holdout (-8.5u). O/U has fewer bets and higher variance → easy to overfit. O/U thresholds drifted massively (OU_UNDER_DEC: 0.45→0.55, OU_UNDER_KOSUB: 0.36→0.42).
- **PROP_PROFIT_WEIGHT=0.75 produced identical results**: Same basin found with warm-start + tight bounds. Holdout regression persisted (-16.6u). The weight change didn't fix the overfitting.
- **OPTIMIZER_ONLY env var wrong**: Must use BOTH `UFC_OPTIMIZE_MODE=1` AND `UFC_OPTIMIZER_ONLY=1`. Using `UFC_OPTIMIZER_ONLY=1` alone silently runs prediction mode instead.
- **Cache key mismatch (repeated)**: Editing the algorithm file changes SHA fingerprint, invalidating the optimizer cache. The cache uses `ufc_backtest_registry.json` (not `ufc_profit_registry.json`) for registry fingerprint. Fixed by copying cache files with correct key names each time.
- **Background task started before edits**: A background optimizer job started before code edits applied, so it ran with old settings (patience=20/15). Detected via "stale 20 gens" in log vs expected "stale 15 gens".

## 4. What Worked Well

- **Two-pass backtest expansion**: Seed pass for HTML scraping + clean pass with UFC_CACHE_ONLY=1 was the right approach for adding historical events.
- **Adaptive bounds logic**: The ±25% formula with 5% original-range floor correctly handles near-zero params without zero-width bounds.
- **Cache key manipulation**: Understanding the key format (algo_fp + bt_registry_fp + num_events) and metadata structure allowed bypassing full re-runs.
- **Holdout validation**: The decision NOT to deploy overfitting params was correct. The holdout test caught what the train metrics hid.

## 5. What The User Wants

- "we need to check that you used the right optimizer, ensure it has all the parameters in our most up to date algorithm, and covers all 75 events from the backtestor"
- "we should make a plan to make the optimizer run faster, make it smarter, i.e. test parameter values within a predefined range of prior values as to not waste time testing unrealistic combinations"
- "the optimizer should be not only be optimizing for ML ROI, but increased ROI across all 5 bet types. Need to implement that in a way that is smart, streamlined, and efficient."
- User preference: verify before deploy, don't blindly apply new params if holdout regresses.

## 6. In Progress (Unfinished)

The optimizer overfitting problem is partially addressed (speed/bounds improved, prop weight raised from 0.5→0.75) but the core challenge — optimizing all 5 bet types without O/U overfitting — remains open. Options for next session:
- Increase regularization coefficient (currently 0.10 → try 0.25-0.30) to constrain parameter drift
- Lock O/U thresholds (OU_UNDER_DEC, OU_UNDER_KOSUB) out of param_spec, optimize remaining 61 params, then tune O/U separately
- Wait for 76-80 events (more data = less overfit risk; current 580 fights / 63 params = 9.2 per param, ideal is 20+)

## 7. Blocked / Waiting On

- UFC 327 results (Prochazka vs Ulberg, Apr 12) — needed to grow registry to 76 events.
- User decision on overfitting approach for next optimizer iteration.

## 8. Next Steps (Prioritized)

1. **Track UFC 327 results** (Apr 12) — `python3 track_results.py`, validate registry, commit & push. Use `/mmalogic` skill.
2. **Optimizer overfitting investigation** — test regularization 0.10→0.25 with PROP_PROFIT_WEIGHT=0.75. Or lock O/U params and optimize 61. Target: train gain that also passes holdout.
3. **Grow backtest window to 76-80 events** — after UFC 327 + 2-3 more events, re-run optimizer with more data to reduce overfit risk.
4. **Consider OU_OVER_DEC_THRESH in param_spec** — currently hardcoded at 0.55 while both Under thresholds are optimized. Asymmetry worth addressing in future.

## 9. Agent Observations

### Recommendations
- The optimizer structural improvements (adaptive bounds, faster DE) are permanent wins — don't revert.
- The holdout regression pattern (train up, holdout down) with 580 fights / 63 params is expected. Wait for more data before next major param tune.
- The v11.24.0 params produced +5.10u holdout improvement. They are good. Don't change without holdout evidence.
- System mode matters: OPTIMIZER_ONLY initializes systems in PREDICTION mode, producing slightly different baselines than full backtest mode. Not a bug, but explains baseline discrepancies between runs.

### Data Contradictions Detected
- **Holdout baseline discrepancy**: v11.24.0 full backtest showed holdout COMBINED +55.49u; OPTIMIZER_ONLY mode showed +50.57u for same parameters. Root cause: system initialization mode difference (BACKTEST vs PREDICTION). Full backtest number is more reliable.
- **Background task log showed old patience values**: "stale 20 gens" / "stale 15 gens" in background task output confirmed it ran with pre-edit code (old patience=20/15, not new 15/12).

### Where I Fell Short
- Ran PROP_PROFIT_WEIGHT=0.75 without recognizing it would find the same basin as 1.0. Should have proposed regularization increase instead of burning a second 9-min run.
- Should have immediately recognized that warm-start + tight bounds = constrained search = same local optimum regardless of objective weight.

## 10. Miscommunications

- Parlays can't be scored at the fight level (event-level only), so they're correctly excluded from the optimizer. This wasn't communicated proactively to the user — worth noting next session.

## 11. Files Changed

| File | Action | Why |
|------|--------|-----|
| UFC_Alg_v4_fast_2026.py | Modified | v11.24.0 constants + optimizer v2 (adaptive bounds, faster DE, PROP_PROFIT_WEIGHT=0.75) |
| CLAUDE.md | Modified | Updated baseline numbers for v11.24.0 (75 events) |
| constants.json | Modified | v11.24.0 optimized constants (63 params) |
| ufc_profit_registry.json | Modified | Expanded to 75 events, 580 bouts |
| ufc_backtest_registry.json | Modified | Full backtest data for 75 events |
| fight_breakdowns.json | Modified | Updated fight analysis data |
| algorithm_stats.json | Modified | Updated metrics |
| backtest_summary.json | Modified | Updated summary |
| optimizer_results.json | Modified | Optimizer v2 run results (NOT applied to constants) |
| ufc_ou_odds_cache.json | Modified | Minor odds cache updates |
| ufc_systems_registry.json | Modified | Systems data updated |
| .optimizer_cache/warm_start.json | Modified | New warm-start (v2 params — overfits holdout, use with caution) |
| prediction_output.json | Modified | UFC 327 picks (11 picks) |
| webapp/frontend/public/data/current_picks.json | Modified | Auto-updated UFC 327 picks |

## 12. Current State

- **Branch**: main
- **Last commit**: `fcb23c0` — Optimizer v2: adaptive bounds, faster DE, balanced prop weight (2026-04-08 02:34:35)
- **Build**: Passing — v11.24.0 validated at +755.36u combined (75 events, 580 bouts)
- **Deploy**: Live at mmalogic.com — UFC 327 picks active (11 picks)
- **Uncommitted changes**: warm_start.json, optimizer_results.json, prediction_output.json, current_picks.json (all auto-generated, safe to ignore or commit)
- **Local SHA matches remote**: Yes — `fcb23c0` on both local and origin/main

## 13. Environment

- **Python**: 3.9.6
- **Node.js**: v25.6.1
- **Dev servers**: None running

## 14. Session Metrics

- **Duration**: ~4 hours
- **Tasks**: 6 completed / 6 attempted (75-event expansion, v11.24.0 optimizer, v11.24.0 deploy, optimizer v2 design, optimizer v2 implement, optimizer v2 test)
- **User corrections**: 0 explicit corrections
- **Commits**: 4 (bdf6987, 239b84c, c5aff3d, fcb23c0)
- **Skills used**: EnterPlanMode/ExitPlanMode, direct Bash/Read/Grep (agent limit hit — Explore agents blocked)

## 15. Memory Updates

- No new anti-pattern entries created this session
- warm_start.json updated with optimizer v2 results — NOTE: these params overfit holdout, use v11.24.0 constants instead
- CLAUDE.md updated with v11.24.0 baseline table (75 events, +755.36u)

## 16. Skills Used

| Skill | Purpose | Helpful? |
|-------|---------|----------|
| EnterPlanMode | Design optimizer v2 implementation plan | Yes — caught approach issues before coding |
| ExitPlanMode | Get user sign-off before execution | Yes |
| direct Bash/Read/Grep | Explore optimizer internals, results analysis | Yes — faster than spawning agents |

## 17. For The Next Agent

Read these files first (in order):
1. This handoff (`HANDOFF.md`)
2. `~/.claude/anti-patterns.md`
3. `/Users/nicholashouseholder/ProjectsHQ/mmalogic/CLAUDE.md` (pay special attention to baseline numbers table)
4. `/Users/nicholashouseholder/ProjectsHQ/mmalogic/AGENTS.md`
5. `/Users/nicholashouseholder/ProjectsHQ/mmalogic/docs/reference/EVENT_TABLE_SPEC.md`

**Key context for next agent:**
- Algorithm is **v11.24.0**, active at mmalogic.com with UFC 327 picks live
- Optimizer v2 code improvements committed (`fcb23c0`) — TOOLING ONLY, no constant changes
- Optimizer v2 ran, produced better train (+66u) but worse holdout (-16.6u) — constants NOT applied
- Current active constants = v11.24.0 values (all marked "v11.24: optimizer 75-event retuned")
- UFC 327 event on Apr 12 — track results with `python3 track_results.py` after event
- Optimizer overfitting issue is open — regularization increase OR O/U param lockout are viable next approaches

**Canonical local path for this project: /Users/nicholashouseholder/ProjectsHQ/mmalogic/**
**Do NOT open from iCloud or /tmp/. Use the path above.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo (ufc-predict → mmalogic)
2. GATE 2: `git fetch && git log -1 origin/main` — compare SHA to local, git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + CLAUDE.md

ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: /Users/nicholashouseholder/ProjectsHQ/mmalogic/**
**Last verified commit: fcb23c0 on 2026-04-08 02:34:35 -0700**
