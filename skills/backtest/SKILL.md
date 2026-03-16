---
name: backtest
description: Run backtests for prediction models (UFC, sports betting). Ensures visible output via tee, compares against baseline accuracy, and commits improvements with structured messages. Use when the user mentions backtesting, model evaluation, coefficient testing, or accuracy comparison.
---

# Backtest Skill

Standardized workflow for running and evaluating prediction model backtests.

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

## Rules
- Never suppress backtest output
- Always show the comparison to baseline
- Commit only improvements (or explicitly ask before committing regressions)
- Break long sweeps into chunks that can be committed incrementally
