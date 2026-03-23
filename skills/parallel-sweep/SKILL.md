---
name: parallel-sweep
description: Run parallel parameter sweeps using multiple Claude Code headless agents. Each agent explores a different parameter subspace, writes results to shared SQLite database, and a summary report is generated. Use for coefficient searches, hyperparameter tuning, or any parallelizable parameter optimization.
---

# Parallel Sweep — Multi-Agent Parameter Search

Spawn multiple Claude Code headless agents to search parameter spaces in parallel, converging results into a shared database.

## When to Use
- Coefficient sweeps for prediction models
- Hyperparameter tuning
- Any parameter search that can be divided into independent subspaces
- Tasks that would take hours single-threaded but minutes in parallel

While designed for coefficient sweeps in sports prediction, this skill works for any parameter optimization task. Adapt the parameter space and evaluation metrics to the domain.

## Sports Model Integration
When sweeping sports prediction model parameters:
- **Walk-forward only**: Each backtest in the sweep must use only pre-game data
- **Holdout validation**: Reserve most recent data window — sweep on training data, validate winner on holdout
- **Overfitting guard**: If the top configuration has dramatically better results than neighbors, it's likely overfit — prefer the cluster of good results over the single best
- **Log the full sweep**: Store ALL configurations tested, not just the winner — the distribution matters
- Follow the full [Sports Backtesting Protocol] for the winning configuration before committing

## Workflow

### 1. Define the Search Space
Read the current configuration to understand:
- Which parameters are being swept
- Their current ranges and step sizes
- The evaluation metric (accuracy, ROI, F1, etc.)

### 2. Partition into Subspaces
Divide the parameter space into N equal partitions (default: 4 agents):
- Agent 1: parameter range [0%, 25%)
- Agent 2: parameter range [25%, 50%)
- Agent 3: parameter range [50%, 75%)
- Agent 4: parameter range [75%, 100%)

### 3. Set Up Results Database

```bash
DB_PATH="sweep_results.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create results table if it doesn't exist
sqlite3 "$DB_PATH" "CREATE TABLE IF NOT EXISTS sweep_results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  agent_id INTEGER,
  coefficients_json TEXT,
  accuracy REAL,
  roi REAL,
  timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);"
```

### 4. Dispatch Sweep Agents

Use the Agent tool to dispatch a subagent for each parameter set. Each subagent receives:
- Its agent number and total agent count
- The parameter partition it is responsible for
- The path to the shared SQLite database
- Instructions to run backtests and record results

**Subagent prompt template:**
```
You are sweep agent {i} of {N}.
Read config.json for coefficient ranges.
Your partition: take the full range and split into {N} equal parts, you handle part {i}.
For each configuration in your partition:
1. Run the backtest
2. Record results to SQLite: INSERT INTO sweep_results (agent_id, coefficients_json, accuracy, roi) VALUES ({i}, '<json>', <accuracy>, <roi>)
DB path: {DB_PATH}
Use | tee for all output. Never suppress stdout.
```

Dispatch all N subagents (default: 4) in parallel using the Agent tool. Wait for all to complete before proceeding to analysis.

**Fallback:** If subagents are unavailable, run sweeps sequentially. Iterate through each partition one at a time in the current session, recording results to the same SQLite database after each partition completes.

### 5. Analyze Results
After completion:
```bash
# Top configurations by accuracy
sqlite3 -header sweep_results.db "SELECT * FROM sweep_results ORDER BY accuracy DESC LIMIT 10;"

# Best ROI
sqlite3 -header sweep_results.db "SELECT * FROM sweep_results ORDER BY roi DESC LIMIT 10;"

# Distribution
sqlite3 sweep_results.db "SELECT agent_id, COUNT(*), AVG(accuracy), MAX(accuracy) FROM sweep_results GROUP BY agent_id;"
```

## Resumability (MANDATORY for sweeps > 50 combinations)

Long sweeps get interrupted by rate limits, timeouts, and session crashes. Every sweep must be resumable:

1. **Batch processing.** Break the sweep into batches of 50-100 combinations. After each batch, save results and print top 5 so far.
2. **Check for existing results before starting.** Query the SQLite database for already-completed configurations. Skip any that already have results.
3. **Resume detection.** At sweep start, check: `SELECT COUNT(*) FROM sweep_results` — if results exist, announce "Resuming sweep — X configurations already completed, Y remaining."
4. **Intermediate reporting.** After each batch, print: current batch number, total completed, top 5 results so far, estimated remaining time.
5. **Checkpoint commits.** Every 100 combinations, commit the SQLite database to git so results survive session crashes.

```python
# Resume-aware sweep loop
completed = db.execute("SELECT coefficients_json FROM sweep_results").fetchall()
completed_set = {row[0] for row in completed}
remaining = [c for c in all_configs if json.dumps(c) not in completed_set]
print(f"Resuming: {len(completed_set)} done, {len(remaining)} remaining")

for batch in chunks(remaining, batch_size=100):
    for config in batch:
        result = run_backtest(config)
        db.execute("INSERT INTO sweep_results ...")
    db.commit()
    print_top_5(db)
```

## Rules
- Each agent writes to the SAME SQLite database (SQLite handles concurrent writes)
- If one agent fails, others continue
- Always log each agent's output separately
- Generate a summary report after all agents complete
- Never suppress output — use `| tee` for everything
- For sports models: validate the winning config on holdout data before committing
- Prefer robust configurations (good neighborhood) over isolated peaks
- **Never re-run configurations that already have results** — always check the database first
