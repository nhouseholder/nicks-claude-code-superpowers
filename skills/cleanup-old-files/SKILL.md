---
name: cleanup-old-files
description: Autonomous registry cleanup — detects and archives stale, outdated, or duplicate files across local, iCloud, and GitHub repos so no AI agent picks up the wrong version. NEVER deletes — always archives with clear markers. Fires automatically at session start in project repos, or on-demand when agent confusion is diagnosed.
weight: light
triggers:
  - at session start in any project repo (scan for staleness signals)
  - "we replaced X with Y"
  - "we switched from X to Y"
  - "the old [script/file/version] is still there"
  - after major refactors or architecture changes
  - when agent confusion is diagnosed as picking up wrong file
  - when duplicate/outdated files are found during any operation
---

# Cleanup Old Files — Autonomous Registry Cleanup

## The Problem

When code evolves, old files accumulate. Future agents see both old and new versions and pick the wrong one — often the old one, because it has more history, more comments, or a familiar name.

**Real catastrophic example:** UFC project had 6+ copies of the algorithm scattered across directories:
- `UFC Algs/` root: 20+ old algorithm versions (v2_19 through v3.5)
- `ufc-predict/ufc-predict/` — nested duplicate
- `ufc-predict/ufc-predict-1/` — another nested duplicate
- `ufc-predict-2/` — yet another old copy
- iCloud duplicates with " 2" suffix
- Stale worktrees in `.worktrees/`

Result: agents ran the 25-event backtester instead of the 71-event one, reported wrong numbers, wasted hours.

## CRITICAL: What "Stale" Actually Means

**Stale = EXPLICITLY REPLACED by a newer version.** Nothing else qualifies.

A file is stale ONLY when:
- A newer file exists that does the SAME JOB (e.g., backtester_v2 replaced by backtester_v3)
- A commit message says "replaced X with Y"
- The user explicitly says the file is outdated

A file is NOT stale just because:
- It's absent from git (it may be deployed but uncommitted — the NEWEST version)
- It's different from another copy (difference ≠ staleness — investigate first)
- It's compiled/built assets on a live server (those ARE the current production)
- It has uncommitted local changes (that's work in progress)

**CATASTROPHIC EXAMPLE (2026-03-25):** An agent treated production assets as "stale" because they didn't match git. Cloudflare purged them during a deploy. An entire frontend redesign was permanently destroyed with no recovery possible. The "stale" assets were the CURRENT version.

**Rule: When in doubt, a file is NOT stale.** Ask the user before archiving anything that doesn't have clear replacement evidence.

## When to Fire

### Automatic (Session Start)
At the beginning of any session in a project repo, do a quick staleness scan:
1. Check for files with names like `*_old.*`, `*_backup.*`, `*_v1.*`, `* 2.*`, `*_copy.*`
2. Check for nested duplicate directories (repo-inside-repo)
3. Check for stale worktrees in `.worktrees/` or `.claude/worktrees/`
4. Check for multiple files that do the same job (e.g., two backtesters)

If found: flag to user with a one-line summary. **NEVER auto-archive without permission.** NEVER classify production-deployed files as stale.

### On-Demand (Explicit Trigger)
When user says "clean up", "archive old files", "there's confusion about which file to use", or when an agent picks the wrong file version.

## Three-Location Sync Protocol

Stale files can hide in THREE places. Check all three:

| Location | Path Pattern | Git-Managed |
|----------|-------------|-------------|
| **Local project** | `~/Projects/<project>/` or iCloud path | Yes |
| **iCloud sync** | `~/Library/Mobile Documents/com~apple~CloudDocs/` | Sometimes |
| **GitHub** | Remote via `/tmp/` clone | Yes |

### iCloud-Specific Gotchas
- iCloud creates " 2" duplicates when sync conflicts occur
- Files may have `.icloud` placeholder extensions
- Never `git push` from iCloud directories — clone to `/tmp/` first
- Archive iCloud duplicates in-place (don't try to move across volumes)

## Protocol

### Step 1 — Inventory Suspects

```bash
# Find duplicates and old versions
find . -maxdepth 3 -name "*_old.*" -o -name "*_backup.*" -o -name "* 2.*" -o -name "*_copy.*" 2>/dev/null

# Find files with ARCHIVED marker already (verify they have headers)
grep -rl "ARCHIVED" --include="*.py" . 2>/dev/null

# Find nested repo duplicates
find . -maxdepth 3 -type d -name ".git" 2>/dev/null

# Find stale worktrees
ls -la .worktrees/ .claude/worktrees/ 2>/dev/null

# Count files that match the canonical file's purpose
# Example: how many backtesters exist?
find . -name "*backtest*" -o -name "*UFC_Alg*" 2>/dev/null | grep -v archive | grep -v ARCHIVED
```

### Step 2 — Confirm Unused

Before archiving, verify genuinely orphaned:

```bash
# Check nothing imports or calls it
grep -r "old_filename" --include="*.py" --include="*.js" --include="*.ts" .

# Check git for recent modifications
git log --oneline -3 -- <suspect_file>
```

**If anything imports it: STOP. Flag to user.**

### Step 3 — Archive (NEVER Delete)

| Situation | Action |
|-----------|--------|
| Clearly replaced | Rename to `<name>.ARCHIVED.py` + add header |
| Has unique logic not ported | Move to `archive/` + deprecation header |
| Entire directory is stale | Rename dir to `<name>.ARCHIVED/` |
| Unclear | Add `# DEPRECATED` header, ask user |

**Archive header template:**
```python
# ============================================================
# ARCHIVED — <date>
# Superseded by: <new_file>
# Reason: <brief explanation>
# Do NOT run this file. Do NOT import from this file.
# Kept for historical reference only.
# ============================================================
```

### Step 4 — Sync to GitHub

After local cleanup:
```bash
cd /tmp && git clone <repo_url> cleanup-push
# Copy archived files and deletions
cd cleanup-push && git add -A
git commit -m "Archive stale files: <list>"
git push origin main
```

### Step 5 — Document

Update the project's canonical file list in CLAUDE.md or BACKTESTER_README.md:
```
Canonical files (ONLY use these):
- UFC_Alg_v4_fast_2026.py — THE backtester
- track_results.py — live event scorer
- verify_registry.py — registry validator
Everything else is archived or utility.
```

### Step 6 — Verify Clean State

```bash
# Confirm no unarchived duplicates
find . -name "*UFC_Alg*" -not -name "*.ARCHIVED*" -not -path "*/archive/*"

# Confirm canonical files are present
ls -la UFC_Alg_v4_fast_2026.py track_results.py verify_registry.py
```

## Canonical File Registry (UFC Predict)

These 8 Python files are THE canonical set. Everything else should be archived:

| File | Role |
|------|------|
| `UFC_Alg_v4_fast_2026.py` | THE backtester — walk-forward, 71+ events, all 5 bet types |
| `track_results.py` | Live event scorer — updates registry after real events |
| `ufc_betting_systems.py` | Value betting overlay systems |
| `prediction_cache.py` | Prediction caching utility |
| `backtest_cache.py` | Backtest data caching utility |
| `firestore_upload.py` | Firestore data uploader |
| `verify_registry.py` | Registry validator — checks all 12 scoring rules |
| `rescore_registry.py` | Re-applies scoring rules to existing registry |

## Anti-Patterns

- **Silent stale files**: Old files with no marker — agents treat them as valid
- **Name collision**: Two files doing the same job with no indication which is current
- **Nested duplicates**: `repo/repo/` directories from botched clones
- **iCloud " 2" files**: Sync conflicts creating phantom duplicates
- **Stale worktrees**: Old worktrees from prior sessions confusing the working directory
- **Config drift**: New code referencing old configs with wrong parameters
- **Deleting history**: NEVER delete — archive preserves reference while eliminating confusion

## Output Format

```
Registry cleanup complete:
- ARCHIVED: 7 old algorithm files → archive/ (v2_19 through v3.5)
- ARCHIVED: 2 nested duplicate directories → .ARCHIVED/
- REMOVED: 3 iCloud " 2" duplicates (empty/identical to originals)
- FLAGGED: old_features.py — has unique logic, added DEPRECATED header
Canonical files verified: 8 Python, 17 JSON. No duplicates remain.
```
