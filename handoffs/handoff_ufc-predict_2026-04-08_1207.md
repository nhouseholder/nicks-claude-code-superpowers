# Handoff — UFC Predict (mmalogic) — 2026-04-08 12:07
## Model: Claude Sonnet 4.6 (via Opus 4.6 planning, Sonnet execution)
## Previous handoff: handoff_ufc-predict_2026-04-08_0240.md
## GitHub repo: nhouseholder/ufc-predict
## Local path: ~/ProjectsHQ/mmalogic/
## Last commit date: 2026-04-08 11:41:57 -0700

---

## 1. Session Summary
This session was entirely devoted to hypothesis testing on the UFC algorithm (v11.24.0). Three theories were tested and rejected: SL Defiance Score, Opponent Confidence Discount, and Role-Based Performance Modifier. After all three rejections, a root cause analysis of every error encountered was performed, and a new unified `ufc-hypothesis-tester` skill was created to prevent those errors from recurring in future sessions.

## 2. What Was Done

- **Hypothesis 1 — SL Defiance Score**: Tested boosting fighters who consistently win despite lower adjusted SL ratios (penalizing those who lose despite higher ratios). Variants at COEFF=0.25 and COEFF=0.10+gap both rejected: -33.36u and -2.80u vs baseline.
- **Hypothesis 2 — Opponent Confidence Discount**: Analyzed whether fighters with thin opponent chains have inflated stats. Tested blending low-coverage opponent ratios toward neutral (1.0). Rejected: -60.09u. Over-corrects and removes valid signal.
- **Hypothesis 3 — Role-Based Performance**: Tested boosting veterans (8+ UFC fights) with strong W/L records in their current role (favorite/underdog). Rejected: zero effect at COEFF=0.12-0.20 (modifier never fired — data format bugs); -17.61u at COEFF=0.40.
- **Root cause analysis**: Catalogued all 5 errors from hypothesis 3 testing — wrong result enum, wrong datetime API, stale baseline, no git restore between sweeps, missing activation verification.
- **Anti-patterns updated**: Added HYPOTHESIS_DATA_TRAPS to `~/.claude/anti-patterns.md`.
- **Memory updated**: Added Rules 8, 9, 10 to `feedback_hypothesis_testing_protocol.md` (activation check, fresh baseline requirement, clean state between sweeps).
- **New skill created**: `~/.claude/skills/ufc-hypothesis-tester/SKILL.md` — 10-step workflow with all codebase knowledge embedded. Plus `references/codebase-cheatsheet.md` with exact line numbers, data formats, fight_history field names, git restore commands.
- **Baseline corrected**: `backtest_baseline_v11.24.0.json` updated from stale 745.78u to true fresh-run 770.51u.
- **EXPERIMENT_LOG updated**: Three new entries (Hypotheses 1, 2, 3) with full per-stream breakdowns, root cause analysis, and learnings.
- **GitHub superpowers synced**: commit `ab14a52` to nhouseholder/nicks-claude-code-superpowers.

## 3. What Failed (And Why)

- **`result not in ('W', 'L')` — zero activations, no error**: fight_history in `ufc_backtest_registry.json` uses `'WIN'`/`'LOSS'`, not `'W'`/`'L'`. Every fight was silently excluded. Logged as HYPOTHESIS_DATA_TRAPS in anti-patterns.md.
- **`datetime.date.fromisoformat()` — AttributeError**: File imports `from datetime import datetime` so `datetime` = CLASS not module. `datetime.date` doesn't exist. Fix: `datetime.strptime(d, "%Y-%m-%d").date()`. Logged in HYPOTHESIS_DATA_TRAPS.
- **False +24.73u baseline delta**: Baseline was 745.78u from registry totals (stale incremental state) vs actual 770.51u from fresh run. Three runs compared against wrong number. Rule 9 added to memory.
- **Confounded coefficient sweeps**: First run overwrote data files; subsequent COEFF=0.20 and COEFF=0.0 runs all returned 770.51u from contaminated state. Rule 10 added: `git restore` all 12 data files before each sweep.
- **3 wasted sweeps before diagnosing activation bug**: No activation verification step existed. Rule 8 and skill Step 4 now make this mandatory.
- **All 3 hypotheses rejected**: Pattern: the v11.24.0 optimizer already found near-optimal weights for current features. Simple score modifiers either have no effect or cause regression. Combo is the most sensitive stream — regresses on almost every pick flip.

## 4. What Worked Well

- Pre-compute diagnostic script (Step 4 in the skill) correctly identified the activation bug.
- EXPERIMENT_LOG format (per-stream tables + root cause + interesting findings) produced high-quality scientific records.
- `_build_role_odds_lookup()` frozenset pattern for fast pair lookups is a reusable building block.

## 5. What The User Wants

- Future hypothesis tests should be "efficiently, economically, swiftly, and without error every time."
- Wants a permanent agent/skill that "always follows the rules and has the right memory and skills for the job."
- Prefers brutal honesty on why hypotheses fail: "DO root cause analysis."

## 6. In Progress (Unfinished)

No hypothesis is currently in progress. All three tested hypotheses were rejected. Backtester is in clean state (data files restored to HEAD). There are 32 untracked log files and backtest run archives that could be committed or gitignore'd.

## 7. Blocked / Waiting On

Nothing blocked. Next hypothesis theory will come from the user. The skill is ready.

## 8. Next Steps (Prioritized)

1. **Test the next hypothesis theory** — use `/ufc-hypothesis-tester` which now handles the full workflow without the errors from this session.
2. **Clean up untracked files** — `git add backtest_runs/*.json && git commit` to capture archived runs; add `*.log` to `.gitignore`.
3. **Track UFC 327 (Apr 12)** — Run `python3 track_results.py` after the event to grow registry to 76 events.
4. **Explore new hypothesis directions** — Ideas not yet tested: (a) fighter age trajectory over last 3 fights, (b) significant strike accuracy trend, (c) weight-class move penalty.

## 9. Agent Observations

### Recommendations
- Algorithm v11.24.0 appears near-optimal for current feature set. Simple score modifiers are increasingly unlikely to improve results — the 2-pass DE optimizer found near-optimal weights. Future gains likely require new data sources, not coefficient tuning.
- The `ufc-hypothesis-tester` skill's Step 4 (activation diagnostic before full backtest) is the highest-value guard. Would have saved 3 full backtest runs this session alone (~15 minutes).
- The `_build_role_odds_lookup()` frozenset dict pattern is worth extracting into the algorithm as a utility for future hypotheses needing historical matchup-level data.

### Data Contradictions Detected
- **Baseline discrepancy**: baseline JSON showed 745.78u (registry totals) vs 770.51u from fresh run. Root cause: registry totals reflect last incremental state, not a clean full rebuild. 770.51u confirmed correct. Baseline JSON updated.

### Where I Fell Short
- Did not run activation diagnostic before first hypothesis 3 backtest — violated Rule 2 of hypothesis protocol. Caused 3 wasted sweeps.
- Did not check `result` field format before writing `_get_role_performance()`. A 5-second `python3 -c` check would have caught the WIN/LOSS vs W/L mismatch.
- Did not verify baseline was from a fresh run — compared against stale totals for first 3 runs.

## 10. Miscommunications

- Initial hypothesis 3 appeared to show +24.73u improvement — false positive from stale baseline. Diagnosed and corrected.
- Plan mode enforcer correctly blocked Opus from executing the plan — required `/model sonnet` before proceeding. Not a miscommunication — hook working as intended.

## 11. Files Changed

**Git diff --stat (HEAD~5):**
```
HANDOFF.md                                         | 241 +++++++++++++--------
backtest_baseline_v11.24.0.json                    |  16 ++
backtest_runs/11.24.0_20260408_104054.json         |  18 ++
backtest_runs/EXPERIMENT_LOG.md                    | 211 ++++++++++++++++++
[+ 12 more backtest run archives and data files]
```

| File | Action | Why |
|------|--------|-----|
| HANDOFF.md | Updated | Session handoff |
| backtest_baseline_v11.24.0.json | Updated | Corrected stale 745.78→770.51u |
| backtest_runs/EXPERIMENT_LOG.md | +3 entries | Hypotheses 1, 2, 3 logged |
| backtest_runs/*.json (hyp3 runs) | Untracked | 6 archived hypothesis 3 runs |
| ~/.claude/anti-patterns.md | +HYPOTHESIS_DATA_TRAPS | New data format traps documented |
| feedback_hypothesis_testing_protocol.md | +Rules 8-10 | Activation, fresh baseline, clean state |
| ufc-hypothesis-tester/SKILL.md | Created | New hypothesis testing skill |
| ufc-hypothesis-tester/references/codebase-cheatsheet.md | Created | Line numbers, data formats |

## 12. Current State

- **Branch**: main
- **Last commit**: `ef69e2d` — "Experiment log: Role-Based Performance hypothesis — rejected" (2026-04-08 11:41:57 -0700)
- **Build**: N/A — Python algorithm, no build step
- **Deploy**: No changes deployed — hypothesis testing only. mmalogic.com is live at v11.24.0.
- **Uncommitted changes**: 32 untracked files (.log files + 6 backtest_runs/*.json hypothesis archives). No tracked file changes.
- **Local SHA matches remote**: YES — ef69e2d on both

## 13. Environment

- **Node.js**: v25.6.1
- **Python**: 3.9.6
- **Dev servers**: None running

## 14. Session Metrics

- **Duration**: ~90 minutes
- **Tasks**: 3 hypotheses tested (all rejected) + 1 skill created + memory/anti-patterns updated
- **User corrections**: 2 (model switch for plan execution, continuation after context break)
- **Commits**: 3 (Hyp 1 log, Hyp 2+baseline log, Hyp 3 log)
- **Skills used**: backtest, backtestor-quality-control, ufc-hypothesis-tester (created this session)

## 15. Memory Updates

- **anti-patterns.md**: Added `HYPOTHESIS_DATA_TRAPS` — WIN/LOSS vs W/L, datetime class vs module, stale baseline from file reads, registry contamination between sweeps.
- **feedback_hypothesis_testing_protocol.md**: Added Rule 8 (verify activations after first run), Rule 9 (fresh baseline from production run, not file reads), Rule 10 (git restore all 12 data files before each sweep — exact command included).
- **backtest_baseline_v11.24.0.json**: Updated from 745.78u (stale) to 770.51u (fresh run). Note explains discrepancy.
- **EXPERIMENT_LOG.md**: Three new entries — SL Defiance Score (rejected), Opponent Confidence Discount (rejected), Role-Based Performance (rejected). All include per-stream tables, bugs encountered, root cause, learnings.
- **~/.claude/skills/ufc-hypothesis-tester/**: New skill + cheatsheet reference synced to GitHub superpowers (commit ab14a52).

## 16. Skills Used

| Skill | Purpose | Helpful? |
|-------|---------|----------|
| backtest | Standard backtest workflow | Yes |
| backtestor-quality-control | Registry protection | Yes |
| ufc-hypothesis-tester | Created this session | Yes — encodes all learnings |

## 17. For The Next Agent

Read these files first (in order):
1. This handoff
2. `~/.claude/projects/-Users-nicholashouseholder-ProjectsHQ-mmalogic/memory/handoff_ufc-predict_2026-04-08_0240.md` — previous session context
3. `~/.claude/anti-patterns.md` — search `HYPOTHESIS_DATA_TRAPS` before ANY hypothesis work
4. `~/ProjectsHQ/mmalogic/CLAUDE.md` — algorithm spec, baseline numbers, 5 bet types
5. `~/.claude/skills/ufc-hypothesis-tester/SKILL.md` — use this for ALL future hypothesis testing
6. `~/ProjectsHQ/mmalogic/backtest_runs/EXPERIMENT_LOG.md` — 3 rejected hypotheses and why

**When testing ANY new hypothesis: invoke `/ufc-hypothesis-tester` — do NOT implement manually.**
**True baseline: v11.24.0, 75 events, +770.51u combined (fresh run 2026-04-08).**
**Canonical local path: ~/ProjectsHQ/mmalogic/**
**Do NOT open this project from iCloud or /tmp/.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify repo is nhouseholder/ufc-predict
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md (HYPOTHESIS_DATA_TRAPS) + CLAUDE.md

ALL 3 GATES MUST PASS before touching any code.

**Canonical path: ~/ProjectsHQ/mmalogic/**
**Last verified commit: ef69e2d on 2026-04-08 11:41:57 -0700**
