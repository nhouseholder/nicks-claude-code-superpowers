Run a backtest for the current sports prediction project. Ensures walk-forward integrity, visible output, comparison against baseline, and commits improvements.

## Arguments
- `$ARGUMENTS` = sport name, event count, or specific flags (e.g., `ufc 70`, `nhl 3`, `--skip-scrape`)

## Phase 1: Pre-checks
```bash
# Identify the sport and project
PROJECT_NAME=$(basename "$(pwd)")
echo "Project: $PROJECT_NAME"

# Check for cached data
ls *cache*.json *_cache.* data/*.json 2>/dev/null | head -10 || echo "WARNING: No cache files found"

# Check for existing baseline metrics
ls *stats*.json *baseline* *results* 2>/dev/null | head -5

# Check for speed flags in the backtest script
grep -i 'skip\|cache\|fast\|mode\|mock\|dry.run\|offline' *.py 2>/dev/null | head -10
```

Before running:
1. **Verify minimum window**: UFC = 70 events, NHL/MLB/NBA/CBB = 3 seasons (from `~/.claude/CLAUDE.md`)
2. **Use fastest mode first**: cache-only, skip-scrape, dry-run — only run full slow version if fast mode output is insufficient
3. **Backup profit registry**: `cp registry.json registry_backup_$(date +%Y%m%d).json` (if exists)
4. **Record existing baseline**: Note current accuracy/profit numbers BEFORE running

## Phase 2: Execute Backtest
Follow the backtest SKILL.md protocol (`~/.claude/skills/backtest/SKILL.md`):

1. Run with **visible output**: Always pipe through `| tee backtest_output.log`
2. Use **cache-only mode first** if available
3. Monitor output within 30 seconds — if silent, something is wrong
4. **Walk-forward integrity**: Verify no future data leakage (see `~/.claude/CLAUDE.md` rules)

## Phase 3: Verify & Compare
1. **Compare against baseline**: Did accuracy/profit improve, regress, or stay flat?
2. **Registry protection**: If registry updated, compare field-by-field against backup — if ANY event lost data, RESTORE backup immediately
3. **Sanity check**: If accuracy >80% on sports, suspect data leakage
4. **Data invariants**: Verify all invariants from `~/.claude/CLAUDE.md` (profit>0 requires wins>0, etc.)

## Phase 4: Report & Commit
```
BACKTEST COMPLETE
=================
Sport: [name] | Window: [N events/seasons]
Walk-forward: ✓ verified
Cache used: [yes/no — if no, new data cached]

Results vs Baseline:
| Metric | Baseline | New | Delta |
|--------|----------|-----|-------|
| Accuracy | X% | Y% | +/-Z% |
| Profit | Xu | Yu | +/-Zu |
| ROI | X% | Y% | +/-Z% |

Registry: [protected ✓ / updated ✓ / restored from backup ⚠]
```

If improved: commit with structured message.
If regressed: DO NOT commit. Report and ask user how to proceed.
