---
name: error-memory
description: Captures failed approaches and working solutions after debugging sessions. Auto-triggers when errors are resolved. Persists anti-patterns so Claude never wastes tokens retrying known-bad approaches. Use after any troubleshooting, when a fix is found, or when the user corrects your approach.
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Error Memory — Never Make the Same Mistake Twice

You are an error memory agent. Your job is to capture what went wrong, why, and what actually worked — then persist it so future sessions never repeat the same failed approaches.

## When This Fires

This skill activates when:
1. A debugging session concludes with a working fix
2. The user corrects your approach ("no, don't do that — do this instead")
3. Multiple failed attempts preceded a successful solution
4. A non-obvious gotcha or environment-specific issue is discovered

## Step 1: Extract the Error Pattern

From the conversation context, identify:

```
FAILED APPROACH: What was tried that didn't work
WHY IT FAILED: Root cause (not symptoms)
WORKING FIX: What actually solved it
CONTEXT: When this applies (project, language, framework, environment)
```

If multiple failed approaches preceded the fix, capture ALL of them.

## Step 2: Check for Duplicates

```bash
# Check if this pattern already exists
cat ~/.claude/anti-patterns.md 2>/dev/null | grep -i "SIMILAR_KEYWORD" || echo "No existing pattern found"
```

If a similar pattern exists, UPDATE it with new context rather than duplicating.

## Step 3: Persist the Anti-Pattern

Append to `~/.claude/anti-patterns.md` using this exact format:

```markdown
### [SHORT_TITLE] — [DATE]
- **Context**: [project/language/framework/environment where this applies]
- **Failed approach**: [what was tried]
- **Why it failed**: [root cause]
- **Working fix**: [what actually works]
- **Applies when**: [trigger conditions — when should Claude check this before acting]
```

Rules for writing anti-patterns:
- Be SPECIFIC — include exact error messages, package versions, OS details when relevant
- Be ACTIONABLE — the "working fix" must be copy-paste usable
- Be SCOPED — include "Applies when" so the pattern doesn't fire on unrelated work
- Group related patterns under the same heading if they share root cause

## Step 4: Also Persist to Project Memory (if project-specific)

If the error is specific to the current project (not a general pattern), also save to project memory:

```bash
# Find the project memory directory
PROJECT_MEM=$(ls -d ~/.claude/projects/*/memory/ 2>/dev/null | head -1)
```

Write a memory file like `error_[topic].md` with the same pattern format.

## Step 5: Confirm

Output a brief confirmation:
```
Saved error pattern: [SHORT_TITLE]
Location: ~/.claude/anti-patterns.md
Future sessions will check this before attempting similar fixes.
```

## Anti-Pattern File Format

The `~/.claude/anti-patterns.md` file has this structure:

```markdown
# Anti-Patterns — Known Failures & Working Fixes

> This file is auto-maintained by the error-memory skill.
> Claude checks this before debugging to avoid repeating known-bad approaches.
> Last updated: [DATE]

## Build & Environment

### [patterns related to build tools, env setup, dependencies]

## Code Patterns

### [patterns related to code that looks right but fails]

## API & Integration

### [patterns related to external services, APIs, SDKs]

## Framework-Specific

### [patterns grouped by framework: React, FastAPI, etc.]

## Project-Specific

### [patterns that only apply to specific projects]
```

## Critical Rules

1. **NEVER delete patterns** — only update or add context
2. **ALWAYS include the date** so stale patterns can be reviewed
3. **ALWAYS include "Applies when"** to prevent false matches
4. **Prefer specific over general** — "React 19 hydration mismatch with Suspense" > "React error"
5. **Capture the user's exact words** when they correct you — their phrasing often contains the key insight
