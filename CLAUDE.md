# Claude Code Settings

## Project Context

Primary languages: Python and JavaScript. Always commit working checkpoints before attempting optimizations.

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

## Background Task Notifications

When background tasks complete (especially stale ones from prior sessions):
- **Batch them.** If multiple stale tasks drain, acknowledge ALL of them in ONE message: "X background tasks from the prior session completed. Already incorporated." Do NOT respond to each one individually.
- **Don't repeat results.** If results were already reported, don't restate them. Just say "Already reported" or nothing at all.
- **Keep it short.** Stale task = 1 line max. Never write paragraphs explaining why a stale task is irrelevant.
- **Final summary only.** After all tasks drain, give ONE clean summary of what actually matters — results, next steps. Skip the play-by-play.

## Bug Recording (MANDATORY)

**Every bug fix must be recorded. No exceptions.**

When ANY bug is fixed — in the algorithm, the app, the website, or any project — immediately:

1. **Record it** in `~/.claude/anti-patterns.md` using the error-memory format:
   ```
   ### [SHORT_TITLE] — [DATE]
   - **Context**: [project/file/component]
   - **Bug**: [what was broken]
   - **Root cause**: [why it was broken]
   - **Fix**: [what actually fixed it]
   - **Applies when**: [when to check this before acting]
   ```

2. **Check it first** — Before attempting ANY fix, search `~/.claude/anti-patterns.md` and `~/.claude/recurring-bugs.md` for prior occurrences. If this bug was fixed before, the previous fix was insufficient — escalate, don't re-apply.

3. **Commit to GitHub** — Anti-patterns and recurring-bugs files must be committed to the relevant project repo so all agents (across sessions, machines, and collaborators) share the same knowledge.

4. **Read on session start** — At the beginning of every session that involves debugging, read `anti-patterns.md` to preload known failure patterns.

The goal: **no bug is ever fixed twice the same way.** Every fix becomes institutional knowledge that all future sessions can access.

## Behavioral Rules

1. **Search before coding** — Before writing custom code, check if a solution already exists (npm, PyPI, MCP, skills, GitHub).
2. **Think before acting** — On complex tasks, plan first. Use `/write-plan` for multi-step work.
3. **Verify before claiming done** — Run tests/builds and confirm output before declaring success.
4. **Save learnings** — When I learn something reusable (user preferences, patterns, gotchas), save it to memory.
5. **Compact strategically** — Suggest `/compact` at logical task boundaries, not mid-implementation.
