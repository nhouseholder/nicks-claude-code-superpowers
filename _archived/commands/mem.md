# Memory — Unified Memory System

Manage both the hierarchical memory (`~/.claude/memory/`) and the project-scoped auto-memory (`~/.claude/projects/.../memory/`).

## Two Memory Systems

### 1. Hierarchical Memory (`~/.claude/memory/`)
```
~/.claude/memory/
├── core.md              # Summaries + pointers (always loaded)
├── me.md                # About the user (always loaded)
├── topics/
│   └── <topic>.md       # Detailed entries by topic
└── projects/
    └── <project>.md     # Project-specific knowledge
```

### 2. Auto-Memory (project-scoped, per working directory)
```
~/.claude/projects/<project-path>/memory/
├── MEMORY.md            # Index file with links to memory files
├── user_*.md            # User profile memories (frontmatter: type: user)
├── feedback_*.md        # User corrections/preferences (frontmatter: type: feedback)
├── project_*.md         # Project context memories (frontmatter: type: project)
└── reference_*.md       # External system pointers (frontmatter: type: reference)
```

Auto-memory files use frontmatter format:
```markdown
---
name: memory name
description: one-line description
type: user|feedback|project|reference
---
Content here
```

## User Commands

### `/mem show`
Show current memory state across BOTH systems:
1. List all files in `~/.claude/memory/` with line counts
2. Show contents of `core.md` (hierarchical)
3. List all files in the current project's auto-memory directory
4. Show contents of `MEMORY.md` (auto-memory index)
5. Summary: total memory files, total lines, last modified dates

### `/mem search <query>`
Search across ALL memory files for a keyword or topic:
1. Grep `~/.claude/memory/` recursively for the query
2. Grep the current project's auto-memory directory
3. Show matching entries with file path and context (3 lines around match)

### `/mem save <observation>`
Save a new memory entry:
1. Determine the best location:
   - User preferences/profile → `~/.claude/memory/me.md` or auto-memory `user_*.md`
   - Project-specific → auto-memory `project_*.md`
   - Technical pattern → `~/.claude/memory/topics/<topic>.md`
   - Feedback/correction → auto-memory `feedback_*.md`
2. Check for duplicates first — update existing entries rather than creating new ones
3. Use frontmatter format for auto-memory, `## Title [date]` format for hierarchical
4. Update the relevant index file (core.md or MEMORY.md)

### `/mem forget <topic>`
Remove a memory entry:
1. Search both systems for matching entries
2. Show what will be removed and confirm with user
3. Remove from the file and update the index
4. Never delete the file itself if other entries remain — just remove the specific entry

### `/mem cleanup`
Prune stale or duplicate memories:
1. Scan both systems for:
   - Duplicate entries (same content in different files)
   - Stale entries (reference things that no longer exist in the codebase)
   - Conflicting entries (two memories that say opposite things)
2. Present findings and ask before removing anything
3. Update indexes after cleanup

## Agent-Initiated Actions (Automatic)

### Load — Session Start
Run in background at session start. Use the Agent tool:
- Read `~/.claude/memory/me.md` and `~/.claude/memory/core.md`
- Read current project's `MEMORY.md` if it exists
- Check for `projects/<project>.md` in hierarchical memory
- Return a context summary

### Save — Persist Learning
Run in background when you learn something worth keeping. Use the Agent tool:
- Categorize the observation (user/feedback/project/reference)
- Check for existing entries to update before creating new ones
- Write to the appropriate system (hierarchical for cross-project, auto-memory for project-specific)
- Update the relevant index

### Recall — Retrieve Context
Run when you need specific context (can block if needed immediately):
- Grep both memory systems for the query
- Follow pointers from core.md and MEMORY.md
- Return relevant entries with source paths

## When to Save
- User explicitly says "remember..." or similar
- You solve a non-trivial problem (save the approach)
- You discover a user preference or correction
- You learn something project-specific
- A pattern emerges across multiple interactions

## When to Recall
- Starting unfamiliar work
- Stuck on a problem (check for similar past issues)
- User asks "do you remember..."
- Context from memory would clearly help

## Principles
- **Background ops**: Load and save don't block the main conversation
- **Deduplicate**: Check before creating — update existing entries first
- **Right system**: Cross-project knowledge → hierarchical, project-specific → auto-memory
- **Atomic entries**: One concept per entry, clearly titled
- **User editable**: Plain markdown, user can edit anytime
