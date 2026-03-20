---
name: backtest
description: Run backtests for prediction models (UFC, sports betting). Ensures visible output via tee, compares against baseline accuracy, and commits improvements with structured messages. Enforces walk-forward integrity, overfitting awareness, and future predictive accuracy as the #1 goal. Use when the user mentions backtesting, model evaluation, coefficient testing, or accuracy comparison.
---

# Backtest Skill

Standardized workflow for running and evaluating prediction model backtests.

## The #1 Rule: Future Predictive Accuracy

Every backtest exists to answer ONE question: **Will this algorithm make money on FUTURE bets?**

Historical performance is a tool, not the goal. Before running any backtest, ask:
- What is the hypothesis? Why should this change improve future predictions?
- Is this generalizable across time periods, or fitting noise?
- Would a domain expert agree this factor matters?

Check project memory for a Sports Backtesting Protocol. If one exists, follow it. If not, use these defaults: walk-forward validation, no future data leakage, compare against baseline accuracy, output results with `| tee` to both stdout and log file.

## Overfitting Guard

After every backtest, run this quick check:
- **Suspiciously good?** If accuracy jumped 5%+ from a minor tweak → likely overfit
- **Stable across windows?** Test on 2+ non-overlapping time periods
- **Robust to perturbation?** Slightly different coefficients should give similar results
- **Explainable?** If you can't explain WHY it works in domain terms → don't trust it

## Workflow

### 1. Verify Database
- Check that BacktestDB (or equivalent SQLite database) exists and is populated
- Verify the backtest script exists and is runnable
- Check for a baseline accuracy to compare against (previous results, config, or git history)

### 2. Run Backtest with Visible Output
```bash
python backtest.py | tee backtest_results.log
```

**CRITICAL:** Always use `| tee <logfile>` for visible output. NEVER redirect stdout to /dev/null or suppress output for scripts that need monitoring.

If the backtest script is in a different location or has arguments:
```bash
python <script_path> [args] 2>&1 | tee backtest_results_$(date +%Y%m%d_%H%M%S).log
```

### 3. Compare Against Baseline
- Parse results for key metrics: accuracy, ROI, precision, recall
- Compare against the previous best (from git log, config, or results file)
- Show delta clearly:
  ```
  Accuracy: 67.3% → 69.1% (+1.8%)
  ROI: +4.2% → +5.7% (+1.5%)
  ```

### 4. Commit if Improved
If metrics improved:
```bash
git add <changed_files>
git commit -m "backtest: vX.XX +Y.Y% accuracy (+Z.Z% delta)"
```

If metrics declined:
- Do NOT commit automatically
- Report the regression and suggest reverting or investigating

### 5. Log Management
- Keep backtest logs in a `logs/` directory or project root
- Never delete previous logs — they're the audit trail
- Name logs with timestamps for traceability

### 6. Overfitting Validation (Sports Models)
Before committing, validate the improvement is real:
```bash
# Run on a holdout time window the algorithm hasn't seen
python backtest.py --start-date HOLDOUT_START --end-date HOLDOUT_END | tee holdout_results.log
```
- If holdout performance is significantly worse than training window → likely overfit
- If holdout performance is comparable → improvement is likely genuine
- Log both training and holdout results in commit message

## Backtest Window Limits

Hard rules — never backtest on less data than specified:

| Sport | Minimum Window |
|-------|---------------|
| UFC | 70 events (growing — starts at 70, auto-increments via track_results.py, never shrinks) |
| NHL | 3 seasons |
| MLB | 3 seasons |
| NBA | 3 seasons |
| CBB | 3 seasons |

## Walk-Forward Integrity (MANDATORY — #1 RULE)

Every backtest MUST be temporally legitimate. For each game/event being evaluated, the model may ONLY use data available BEFORE that game occurred.

**What this means in practice:**
- Stats must be computed using only games played BEFORE the prediction date
- Season-long averages that include the game being predicted are INVALID (this is the most common violation)
- Point-in-time only: predicting Game 50 = model sees Games 1-49, never Game 50+
- Odds, injuries, lineups must reflect pre-game state only

**Why this is non-negotiable:**
Using full-season averages (which include the game being predicted and future games) inflates accuracy by 10-20% and produces completely misleading results. This is called **winner bias** — the backtest looks amazing but the model will fail on live bets because it was secretly using information it won't have in production.

**How to verify:**
1. Stat functions must accept `cutoff_date` or `before_event` parameter
2. Rolling/expanding windows must exclude the current game
3. Any `.mean()`, `.avg()`, or aggregate must filter by date
4. If accuracy is 80%+ on sports, suspect data leakage FIRST

**If walk-forward integrity cannot be confirmed, the backtest result is WORTHLESS. Do not commit, do not celebrate, do not report it as real.**

## Rules
- Never suppress backtest output
- Always show the comparison to baseline
- Commit only improvements (or explicitly ask before committing regressions)
- Break long sweeps into chunks that can be committed incrementally
- **Overfitting check** — validate on holdout data before committing sports model changes
- **Future-first** — every change must have a hypothesis for why it improves future accuracy
