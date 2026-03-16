# Claude Code Settings

## Project Context

Primary languages: Python and JavaScript. Projects include: UFC/MMA prediction algorithm, MyStrainAI (strain recommendation app on Cloudflare), sports betting SaaS. Always commit working checkpoints before attempting optimizations.

## Development Practices

When running long-running scripts (backtests, sweeps, coefficient searches), always stream output to both stdout and a log file (e.g., `| tee output.log`). Never redirect stdout to /dev/null for scripts that need monitoring.

## Session Management

Before starting large tasks, check remaining API usage/rate limits. Break work into smaller, committable chunks so progress is saved if the session is interrupted by usage limits.

## Git Workflow

For git operations in iCloud-synced directories, always use a fresh clone to a non-iCloud path first. Never attempt git push/pull directly in iCloud Drive folders.

## Debugging

When debugging errors, identify the minimal fix first before considering large-scale refactors. For import/reference errors, check for missing imports in the specific file before replacing symbols across the codebase.

## Memory

I have two memory systems:

### 1. Hierarchical Memory (`~/.claude/memory/`)
- `me.md` — user profile (always loaded)
- `core.md` — summaries + pointers (always loaded)
- `topics/<topic>.md` — detailed entries by topic
- `projects/<project>.md` — project-specific knowledge

**Session start:** Load `me.md` and `core.md` in background.
**During session:** Save learnings to `topics/` when I discover something worth keeping.
**When stuck:** Recall relevant topics by reading `core.md` pointers.

### 2. Project Memory (`~/.claude/projects/.../memory/`)
- MEMORY.md index + individual memory files per project
- Scoped to the current working directory

## Behavioral Rules

1. **Search before coding** — Before writing custom code, check if a solution already exists (npm, PyPI, MCP, skills, GitHub).
2. **Think before acting** — On complex tasks, plan first. Use `/write-plan` for multi-step work.
3. **Verify before claiming done** — Run tests/builds and confirm output before declaring success.
4. **Save learnings** — When I learn something reusable (user preferences, patterns, gotchas), save it to memory.
5. **Compact strategically** — Suggest `/compact` at logical task boundaries, not mid-implementation.
