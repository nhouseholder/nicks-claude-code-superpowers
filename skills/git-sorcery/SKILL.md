---
name: git-sorcery
description: Advanced git intelligence beyond basic add/commit/push. Smart commit messages from diffs, conflict resolution strategies, interactive history analysis, bisect for bug hunting, cherry-pick workflows, branch management, and stash operations. Automatic skill that enhances all git operations.
weight: passive
---

# Git Sorcery — Master-Level Git Operations

Elevate every git interaction from basic commands to strategic version control. Write commit messages that tell a story, resolve conflicts intelligently, find the exact commit that introduced a bug, and manage branches like a pro.

## Always Active

This skill enhances all git operations automatically. No manual trigger needed.

## Smart Commits

### Commit Message Craft

Analyze the actual diff to write messages that capture intent, not just changes.

**Formula**: `[Action] [What] — [Why/Impact]`
Example: `"Fix race condition in auth token refresh — stale tokens caused 401 cascade"`

- Action: Fix, Add, Remove, Refactor, Optimize, Update, Migrate
- What: The specific thing that changed
- Why: The reason or impact (after the em dash)

### Version-Aware Commits

When the project uses semantic versioning:
```
Breaking change → suggest major bump
New feature → suggest minor bump
Bug fix → suggest patch bump
```

Mention the version in the commit when bumping: `v5.64.0: Add dispensary search radius filter`

### Atomic Commits

When multiple logical changes are staged:
- Suggest splitting into separate commits
- Group related files together
- Each commit should be independently revertable

## Conflict Resolution

### Smart Merge Strategy

When conflicts arise:

```
1. UNDERSTAND — Read both sides. What was each change trying to do?
2. INTENT — Which change is more recent/important? Do they overlap or complement?
3. RESOLVE:
   - Both changes needed → Integrate both (most common)
   - Changes contradict → Keep the one that matches current direction
   - Changes are in different sections → Accept both (clean merge)
4. VERIFY — After resolving, does the file still make sense as a whole?
```

### Common Conflict Patterns

| Pattern | Resolution |
|---------|-----------|
| Both added imports | Keep both, dedupe |
| Both modified same function | Usually integrate both changes |
| One deleted, one modified | Check if the modification is still needed |
| Package lock conflicts | Regenerate from package.json |
| Both added to a list | Keep both entries, check for order dependencies |

## Bug Hunting with Bisect

When a bug's origin is unknown:

```
1. Find a known good commit (when did it last work?)
2. The current commit is bad
3. Use git log to identify the range
4. Binary search: test the midpoint commit
5. Narrow down until you find the exact introducing commit
6. Read that commit's diff to understand what caused the bug
```

Suggest bisect when:
- User says "this used to work" or "when did this break?"
- Bug seems unrelated to recent changes
- Multiple people commit to the repo

## Cherry-Pick Workflows

When to suggest cherry-picking:
- A fix on one branch is needed on another
- A feature needs to be backported
- Specific commits need to be extracted from a messy branch

```
1. Identify the exact commit(s) needed
2. Check for dependencies between commits
3. Cherry-pick in chronological order
4. Resolve conflicts if the target branch diverged
5. Verify the cherry-picked code works in the new context
```

## Branch Management

### Branch Naming
Follow the project's convention, or suggest:
```
feature/short-description
fix/issue-description
refactor/what-changed
```

### Branch Cleanup
After merging, suggest cleaning up:
- Delete the merged branch locally and remotely
- Prune stale remote-tracking branches
- Check for other branches that might be stale

### Branch Strategy
- Small fix → commit directly to the working branch
- Feature work → suggest a feature branch if not already on one
- Risky change → suggest a branch before making changes

## Stash Operations

Smart stash usage:
- User wants to switch context → suggest stash with descriptive message
- Returning to stashed work → remind them about the stash
- Multiple stashes → help identify which one to pop

```
git stash push -m "WIP: dispensary filter — radius selector done, need to add URL params"
```

Always use descriptive stash messages — `git stash` with no message is a recipe for confusion.

## History Analysis

### Reading the Story
```
git log --oneline -20          → Quick overview of recent work
git log --stat -5              → What files changed in recent commits
git log --author="name" -10   → What a specific person did
git log -- path/to/file       → History of a specific file
git blame path/to/file        → Who last touched each line
```

### Finding Patterns
- Frequently changed files → potential hotspots that need refactoring
- Large commits → might need to be split in the future
- Commit message patterns → follow the project's established style

## Rules

1. **Intent over diff** — Commit messages explain WHY, not WHAT (the diff shows what)
2. **Atomic commits** — One logical change per commit. Suggest splitting when appropriate.
3. **Never force-push without asking** — Even to feature branches. Always confirm.
4. **Preserve history** — Prefer merge over rebase for shared branches
5. **Descriptive stashes** — Always include a message with stash operations
6. **Verify after resolve** — After conflict resolution, always check the result makes sense
7. **Follow existing conventions** — Match the project's commit style, branch naming, and workflow
