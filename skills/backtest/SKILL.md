---
name: backtest
description: Run backtests for prediction models (UFC, sports betting). Ensures visible output via tee, compares against baseline accuracy, and commits improvements with structured messages. Enforces walk-forward integrity, overfitting awareness, and future predictive accuracy as the #1 goal. Use when the user mentions backtesting, model evaluation, coefficient testing, or accuracy comparison.
weight: heavy
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

## Mandatory Rules (defined in CLAUDE.md — not repeated here)

These are enforced globally via CLAUDE.md. See those sections for full details:
- **Backtest Window Limits** — UFC: 70 events growing, NHL/MLB/NBA/CBB: 3 seasons
- **Walk-Forward Integrity** — point-in-time stats only, no post-event data leakage
- **Data Caching** — cache all scraped data locally, commit to GitHub, never re-scrape

## Rules
- Never suppress backtest output
- Always show the comparison to baseline
- Commit only improvements (or explicitly ask before committing regressions)
- Break long sweeps into chunks that can be committed incrementally
- **Overfitting check** — validate on holdout data before committing sports model changes
- **Future-first** — every change must have a hypothesis for why it improves future accuracy
