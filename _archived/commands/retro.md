Weekly engineering retrospective scoped to the current project. Analyzes commit history, work patterns, and code quality metrics. Identifies what shipped, what's working, and what to improve.

## Arguments
- `$ARGUMENTS` = time window (default: 7d)
  - `24h` = last 24 hours
  - `7d` = last 7 days (default)
  - `14d` = last 14 days
  - `30d` = last 30 days

---

## Phase 1: Identify Project

1. Get project from `pwd` + `git remote get-url origin`
2. Read project CLAUDE.md if it exists
3. Read project handoff if one exists
4. Read project memory if it exists

---

## Phase 2: Gather Raw Data

Parse the time window argument. Default to 7 days. For day units, compute an absolute start date at local midnight (e.g., 7d from 2026-03-27 = `--since="2026-03-20T00:00:00"`).

Run ALL of these git commands in parallel:

```bash
# 1. All commits in window
git log --since="<window>" --format="%H|%aN|%ai|%s" --shortstat

# 2. Per-commit LOC breakdown
git log --since="<window>" --format="COMMIT:%H|%aN" --numstat

# 3. Commit timestamps for session detection
git log --since="<window>" --format="%at|%aN|%ai|%s" | sort -n

# 4. Hotspot analysis — most changed files
git log --since="<window>" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn | head -15

# 5. Test files changed vs production files
git log --since="<window>" --format="" --name-only | grep -E '\.(test|spec)\.' | sort -u | wc -l

# 6. Any reverts in window
git log --since="<window>" --oneline --grep="revert" --grep="Revert" -i
```

---

## Phase 3: Compute Metrics

| Metric | Value |
|--------|-------|
| Commits | N |
| Total insertions | +N |
| Total deletions | -N |
| Net LOC | +/-N |
| Active days | N (days with at least 1 commit) |
| Sessions | N (gap > 2h = new session) |
| Avg LOC/session | N |
| Test files touched | N |
| Hotspot file | [most changed file] (N changes) |
| Reverts | N |

**Session detection:** Sort commits by timestamp. Any gap > 2 hours between consecutive commits = new session boundary.

---

## Phase 4: Analyze Patterns

### What Shipped
Group commits by theme (feature, fix, refactor, docs, test) from commit message prefixes. List the major items that shipped.

### Hotspot Analysis
The most-changed files often indicate:
- Active development area (good)
- Churn / instability (investigate)
- File that's too large and needs splitting

### Revert Analysis
If reverts exist, flag them:
- What was reverted and why?
- Pattern: same area being reverted repeatedly = deeper issue

### Largest Commits
Find the single largest commit by LOC. If > 500 LOC in one commit, flag as potential scope creep or missing incremental commits.

### Test Coverage Direction
Compare test files touched vs production files. Are tests keeping up with code changes?

---

## Phase 5: Check Against Plans

Read the project handoff (if exists) and compare:
- What was planned vs what actually shipped
- Any blocked items still blocked?
- Did work match priorities or drift to other areas?

Read `~/.claude/anti-patterns.md` for any recurring bugs in this project.

---

## Phase 6: Output Report

```
RETRO — [Project Name] — [start date] to [end date]
═════════════════════════════════════════════════════

METRICS
───────
| Metric          | Value              |
|-----------------|--------------------|
| Commits         | N                  |
| Insertions      | +N                 |
| Deletions       | -N                 |
| Active days     | N / [window days]  |
| Sessions        | N                  |
| Avg LOC/session | N                  |
| Hotspot         | [file] (N changes) |
| Reverts         | N                  |

WHAT SHIPPED
────────────
- [feature/fix 1 — from commit messages]
- [feature/fix 2]
- ...

HOTSPOTS (most changed files)
─────────────────────────────
  Changes  File
  12       src/components/Hero.tsx
  8        src/lib/api.ts
  6        src/pages/index.tsx
  ...

PATTERNS
────────
- [observation about work patterns]
- [churn analysis if applicable]
- [test coverage trend]

WHAT'S WORKING
──────────────
- [positive patterns to continue]

WHAT TO IMPROVE
───────────────
- [areas of concern — reverts, churn, missing tests]

PLAN vs ACTUAL
──────────────
- Planned: [from handoff]
- Shipped: [from commits]
- Gap: [what didn't get done and why]

NEXT PRIORITIES
───────────────
Based on momentum and remaining work:
1. [highest priority next task]
2. [second priority]
3. [third priority]
```

---

## Phase 7: Save & Learn

1. Save report to `_retro/{date}-retro.md`
2. If any notable patterns emerged (recurring bugs, consistent hotspots, workflow issues), offer to save them to project memory for future sessions.

---

## Rules

1. **Current project only.** Don't sweep other projects.
2. **Data-driven.** Every claim backed by git data. No speculation.
3. **Constructive.** "What to improve" should be actionable, not judgmental.
4. **READ-ONLY.** This is a report. Don't modify code.
5. **Compare to plans.** The most valuable insight is plan-vs-actual drift.
