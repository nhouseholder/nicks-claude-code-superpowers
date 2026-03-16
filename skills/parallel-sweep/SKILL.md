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

### 3. Create the Sweep Script

```bash
#!/bin/bash
# parallel_sweep.sh — Launch N parallel Claude Code agents

set -e

NUM_AGENTS=${1:-4}
DB_PATH="sweep_results.db"
CONFIG="config.json"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="sweep_logs_${TIMESTAMP}"

mkdir -p "$LOG_DIR"

# Create results table if it doesn't exist
sqlite3 "$DB_PATH" "CREATE TABLE IF NOT EXISTS sweep_results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  agent_id INTEGER,
  coefficients_json TEXT,
  accuracy REAL,
  roi REAL,
  timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);"

# Launch agents in parallel
for i in $(seq 1 $NUM_AGENTS); do
  echo "Launching agent $i of $NUM_AGENTS..."
  claude -p "You are sweep agent $i of $NUM_AGENTS.
Read $CONFIG for coefficient ranges.
Your partition: take the range and split into $NUM_AGENTS equal parts, you handle part $i.
For each configuration in your partition:
1. Run the backtest
2. Record results to SQLite: INSERT INTO sweep_results (agent_id, coefficients_json, accuracy, roi) VALUES ($i, '<json>', <accuracy>, <roi>)
DB path: $DB_PATH
Use | tee for all output. Never suppress stdout." \
    --allowedTools "Read,Edit,Bash,Grep" \
    > "$LOG_DIR/agent_${i}.log" 2>&1 &

  PIDS+=($!)
done

echo "All $NUM_AGENTS agents launched. PIDs: ${PIDS[*]}"
echo "Logs: $LOG_DIR/"

# Wait for all agents
FAILED=0
for pid in "${PIDS[@]}"; do
  if ! wait "$pid"; then
    echo "Agent (PID $pid) failed"
    ((FAILED++))
  fi
done

echo ""
echo "=== SWEEP COMPLETE ==="
echo "Agents: $NUM_AGENTS total, $((NUM_AGENTS - FAILED)) succeeded, $FAILED failed"
echo ""

# Generate summary
echo "=== TOP 5 CONFIGURATIONS ==="
sqlite3 -header -column "$DB_PATH" \
  "SELECT agent_id, coefficients_json, accuracy, roi, timestamp
   FROM sweep_results
   ORDER BY accuracy DESC
   LIMIT 5;"
```

### 4. Run and Monitor
```bash
chmod +x parallel_sweep.sh
./parallel_sweep.sh 4 | tee sweep_summary.log
```

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

## Rules
- Each agent writes to the SAME SQLite database (SQLite handles concurrent writes)
- If one agent fails, others continue
- Always log each agent's output separately
- Generate a summary report after all agents complete
- Never suppress output — use `| tee` for everything
