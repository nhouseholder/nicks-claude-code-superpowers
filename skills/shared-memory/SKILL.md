---
name: shared-memory
description: Maintains a shared memory document (AGENT-MEMORY.md) in the GitHub repo that any AI agent can read and contribute to. Provides a structured protocol for cross-agent collaboration — decisions, architecture, context, and conventions are persisted so that Claude, Cursor, Copilot, Windsurf, or any AI working from the repo can stay aligned. Updates on request or when explicitly prompted. Manual skill — invoke when you want to update the shared memory.
---

# Shared Memory — Cross-Agent Collaboration via GitHub

Maintain a living memory document in the repo that ALL AI agents can read. Any agent working from this repo should understand the project's decisions, architecture, conventions, and current state — even if they've never seen it before.

## When to Use

This skill is **manual** — invoke it when:
- You want to update the shared memory after a significant session
- The user asks you to update the agent memory
- You're starting work on a repo and want to read the existing shared memory
- A major architecture decision, convention change, or gotcha was discovered

**Do not auto-update** after every session. Only update when the significance test passes.

## The Shared Memory File

**Location**: `AGENT-MEMORY.md` in the repo root.

This file is the single source of truth for cross-agent context. Every AI agent working from this repo — Claude Code, Cursor, Copilot, Windsurf, Aider, or any future tool — should read this file first and update it when they make meaningful changes.

## File Structure

```markdown
# Agent Shared Memory

> This file is maintained by AI agents working on this repo.
> **Read this before making changes. Update it after significant work.**
> Last updated: [ISO date] by [agent name]

## Project Identity
- What this project is (1-2 sentences)
- Primary language/framework
- Key URLs (prod, staging, docs)

## Architecture Decisions
| Decision | Chosen | Why | Date | Agent |
|----------|--------|-----|------|-------|
| [decision] | [choice] | [reasoning] | [date] | [who] |

## Active Conventions
- [Convention 1 — e.g., "All API routes go in /api/v1/"]
- [Convention 2 — e.g., "Use Tailwind, never inline styles"]
- [Convention 3 — e.g., "SQLite for local, KV for production"]

## Current State
- **Version**: [current version]
- **Branch strategy**: [e.g., main = production, dev = staging]
- **Deploy target**: [e.g., Cloudflare Pages]
- **Known issues**: [brief list]

## Recent Significant Changes
| Date | What Changed | Why | Files Affected | Agent |
|------|-------------|-----|----------------|-------|
| [date] | [change] | [reason] | [files] | [who] |

## Gotchas & Warnings
- [Things that will trip up a new agent — e.g., "Don't edit matching_engine.py, production uses recommend.js"]
- [Environment quirks — e.g., "Node 25 needs ROLLUP_PARSE_WORKERS=0"]
- [Data quirks — e.g., "THC-A markets lack GPS coords, use Nominatim fallback"]

## Agent Instructions
[See below — this section tells other agents how to maintain this file]
```

## When to Update

### DO update after:
- Architectural decisions (new library, changed pattern, removed feature)
- Convention changes (renamed directories, new coding standards, changed deploy target)
- Significant refactors (moved files, restructured modules, changed data flow)
- Bug discoveries with non-obvious root causes (gotchas for future agents)
- Version bumps or releases
- New integrations or API changes

### DO NOT update for:
- Minor bug fixes (the commit message is enough)
- Typo fixes, formatting changes
- Routine feature additions that follow existing patterns
- Work that doesn't change how the project operates

### The Significance Test
Before updating, ask: **"Would a new AI agent make a mistake without knowing this?"**
- YES → update AGENT-MEMORY.md
- NO → skip, the code/commits tell the story

## How to Update (Protocol for ALL Agents)

### Rule 1: Read Before Writing
Always read the full AGENT-MEMORY.md before making changes. Your update must be consistent with what's already there.

### Rule 2: Append, Don't Rewrite
- Add new rows to tables — don't delete old ones unless they're factually wrong
- Add new bullets to lists — don't reorganize unless structure is broken
- Old entries are historical context — they have value even if outdated

### Concurrency
When updating AGENT-MEMORY.md, read the current file first, merge your additions, then write. Never overwrite the entire file — append to or update specific sections. If the file changed between your read and write (unlikely but possible), re-read and re-merge.

### Rule 3: Timestamp Everything
Every entry must include:
- **Date**: ISO format (YYYY-MM-DD)
- **Agent**: Which AI tool made the change (e.g., "Claude Code", "Cursor", "Copilot")

### Rule 4: Be Concise
- One line per entry in tables
- No paragraphs — bullets and table rows only
- Link to commits or files instead of explaining code inline

### Rule 5: Resolve, Don't Conflict
If you disagree with an existing entry:
- Add your perspective as a NEW entry, referencing the old one
- Never silently overwrite another agent's decision
- Mark disputed entries with `⚠️ DISPUTED` and explain why

### Rule 6: Prune Quarterly
Entries older than 90 days in "Recent Significant Changes" can be archived to a `## Historical Changes` section at the bottom. Architecture decisions and gotchas persist indefinitely.

## Auto-Update Behavior

At the end of a significant session, Claude should:

1. **Check if AGENT-MEMORY.md exists** — if not, create it from the template above
2. **Read the current contents**
3. **Determine if updates are needed** (apply the significance test)
4. **Append new entries** to the appropriate sections
5. **Update the "Last updated" line** at the top
6. **Commit with message**: `docs: update agent shared memory — [brief reason]`

## Template for New Projects

When starting a new project or adding shared memory to an existing repo, create `AGENT-MEMORY.md` with this starter:

```markdown
# Agent Shared Memory

> This file is maintained by AI agents working on this repo.
> **Read this before making changes. Update it after significant work.**
> Last updated: [today's date] by Claude Code

## Project Identity
- [Project name]: [one-line description]
- Stack: [primary technologies]
- Repo: [GitHub URL]

## Architecture Decisions
| Decision | Chosen | Why | Date | Agent |
|----------|--------|-----|------|-------|

## Active Conventions
- [Add conventions as they emerge]

## Current State
- **Version**: [version]
- **Branch strategy**: [strategy]
- **Deploy target**: [target]
- **Known issues**: None yet

## Recent Significant Changes
| Date | What Changed | Why | Files Affected | Agent |
|------|-------------|-----|----------------|-------|

## Gotchas & Warnings
- [Add gotchas as they're discovered]

## Agent Instructions
Any AI agent working from this repo should:
1. **Read this file first** before making significant changes
2. **Update this file** after architectural decisions, convention changes, or discovering gotchas
3. **Never silently overwrite** another agent's entries — append or mark as disputed
4. **Timestamp all entries** with ISO dates and your agent name
5. **Be concise** — one line per entry, link to code instead of explaining inline
```

## Integration with Other Skills

```
Session starts
    │
    ├─ Read AGENT-MEMORY.md (if exists) — understand project context
    │
    ├─ Do work...
    │
    ├─ Session ends with significant changes?
    │       │
    │       YES → Update AGENT-MEMORY.md
    │       │       ├─ Append to Architecture Decisions (if new decisions)
    │       │       ├─ Append to Recent Changes (if significant)
    │       │       ├─ Append to Gotchas (if discovered)
    │       │       └─ Update Current State (if version/status changed)
    │       │
    │       NO → Skip update
    │
    └─ Commit if updated
```

## Rules

1. **AGENT-MEMORY.md is the shared source of truth** — all agents read it, all agents contribute
2. **Read before write** — always read the full file before updating
3. **Append, don't rewrite** — respect previous agents' entries
4. **Significance test** — only update when a new agent would make mistakes without the info
5. **Timestamp and attribute** — every entry needs a date and agent name
6. **Concise entries only** — tables and bullets, never paragraphs
7. **Never delete silently** — mark disputes, don't overwrite
8. **Auto-create on first use** — if the file doesn't exist, create it from the template
