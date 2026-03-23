---
name: cleanup-old-files
description: When code advances significantly (new architecture, replaced files, renamed scripts), identify and archive or mark stale files so future agents cannot confuse them with the current version. NEVER delete — always archive or rename with a clear marker. Prevents the anti-pattern where old backtestors, deprecated configs, or superseded scripts sit alongside new ones and get picked up by mistake.
weight: light
triggers:
  - "we replaced X with Y"
  - "we switched from X to Y"
  - "the old [script/file/version] is still there"
  - after major refactors or architecture changes
  - when agent confusion is diagnosed as picking up wrong file
---

# Cleanup Old Files

## The Problem

When code evolves, old files accumulate. Future agents (and future you) see both the old and new version and pick the wrong one — often the old one, because it has more history, more comments, or a familiar name.

**Real example:** UFC backtestor migrated from 25-event window to 71-event window. Old `backtest_25.py` still present. Next agent runs old file, reports 25-event results, user thinks the new logic is broken.

## When to Fire

Fire this skill when:
1. A file has been **replaced** by a new version (not just modified)
2. An architecture change makes old files **actively misleading**
3. A user reports agent confusion and the root cause is **stale file presence**
4. After any "we swapped X for Y" or "we migrated from X to Y" statement

Do NOT fire for:
- Normal file edits (use pattern-propagation instead)
- Files that are still used anywhere in the codebase
- Archive/history files the user explicitly wants to keep

## Protocol

### Step 1 — Inventory Suspects

Search for stale counterparts to whatever was just changed:

```
# Find files with old naming patterns
grep -r "old_name\|deprecated\|backup\|v1\|25_event\|legacy" --include="*.py" .

# Find files with similar names to the new canonical file
ls -la | grep -i <keyword>
```

Look for:
- Old numbered versions (`backtest_v1.py`, `25_events.py`)
- Backup copies (`train_old.py`, `model_backup.py`)
- Superseded configs (`config_old.json`, `weights_25.json`)
- Files whose names describe the OLD behavior

### Step 2 — Confirm Still Unused

Before removing anything, verify the file is genuinely orphaned:

```bash
# Check nothing imports or calls it
grep -r "old_filename" --include="*.py" --include="*.js" --include="*.ts" .

# Check git for recent modifications (recently touched = maybe still active)
git log --oneline -3 -- <suspect_file>
```

**If anything imports it: STOP. Flag to user instead of deleting.**

### Step 3 — Choose Disposition

**NEVER delete old files.** Always archive or mark them so the history is preserved but the confusion is eliminated.

| Situation | Action |
|-----------|--------|
| Clearly replaced, nothing imports it | Rename to `<name>.archived.py` + add `# ARCHIVED` header |
| Has unique logic not yet ported | Move to `archive/` subdirectory + add deprecation notice at top |
| Unclear if still needed | Add prominent `# DEPRECATED — replaced by <new_file>` header at top of file |
| Already in archive/ | Add `# ARCHIVED` header if missing |

**Naming conventions for archived files:**
- Rename in-place: `backtest_25.py` → `backtest_25.ARCHIVED.py`
- Or move to subdirectory: `archive/backtest_25.py`
- Always add a header comment explaining what replaced it and when

**Header template to add to every archived file:**
```python
# ============================================================
# ARCHIVED — 2026-03-23
# This file has been superseded by: <new_file.py>
# Reason: <brief explanation, e.g. "migrated from 25→71 event window">
# Do NOT run this file. Do NOT import from this file.
# Kept for historical reference only.
# ============================================================
```

### Step 4 — Document the Cleanup

After archiving files, leave a breadcrumb in the new canonical file:

```python
# In the new canonical file, add a comment:
# NOTE: Replaced backtest_25.py (25-event window). This file uses 71-event window.
# Old file archived as backtest_25.ARCHIVED.py — 2026-03-23.
```

Optionally create or update a `MIGRATION.md` in the directory noting what changed and when.

### Step 5 — Verify Clean State

After cleanup:
```bash
# Confirm old patterns are gone
grep -r "old_name" . --include="*.py"

# Confirm new canonical file is what runs
grep -r "new_name" . --include="*.py"
```

## Output Format

Report cleanups concisely:

```
Archived stale files after UFC backtestor migration (25→71 events):
- ARCHIVED: backtest_25.py → backtest_25.ARCHIVED.py (header added, replaced by backtest.py)
- ARCHIVED: weights_25.json → archive/weights_25.json (header added, replaced by weights_71.json)
- FLAGGED: old_features.py — has unique normalization logic not yet ported, added DEPRECATED header

New canonical files: backtest.py, weights_71.json
```

## Anti-Patterns to Prevent

- **Silent stale files**: Old files sitting quietly with no marker — agent treats them as valid
- **Name collision**: `backtest.py` and `backtest_25.py` both present with no indication which is current
- **Config drift**: New code, old config → model runs with wrong parameters
- **Soft archives that still confuse**: Files moved to `archive/` but without a header — agent reads them anyway
- **Deleting history**: Never delete — the original logic may contain useful reference or catch regressions
