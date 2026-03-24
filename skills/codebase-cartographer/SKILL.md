---
name: codebase-cartographer
description: Build a mental architecture map of the codebase at session start. Know every directory's purpose, key files, data flow patterns, and entry points. Enables instant navigation and informed decisions without redundant file exploration. Automatic skill that fires at session start.
weight: passive
---

# Codebase Cartographer — Know the Terrain Before You Build

At the start of every session, build a mental map of the codebase. Know the architecture, the patterns, the entry points, the data flow. When the user asks you to change something, you should already know where to look — not waste tokens exploring.

## When This Activates

- **Session start** — Automatically build the map from available context
- **New directory encountered** — Extend the map on-demand
- **"What does X do?"** — Leverage the map for instant answers

## The Mapping Protocol

### Fast Path: Architecture Already Documented

**Before doing ANY mapping work**, check if MEMORY.md or CLAUDE.md already contains an architecture section with key paths, tech stack, and directory purposes. If it does:
- Skip Tier 1 mapping entirely — the map already exists
- Go straight to Tier 2 targeted reads for the current task
- This saves ~500+ tokens per session on well-documented projects

### Tier 1: Instant Map (From Memory + Git Status)

Only if the fast path didn't find existing architecture docs:

```
1. Check project memory (MEMORY.md, CLAUDE.md) — architecture may already be documented
2. Check git status — what's changed, what branch, what's in progress
3. Check package.json / pyproject.toml / Cargo.toml — stack and dependencies
4. Check directory structure (top 2 levels) — project layout
```

This gives you ~80% of the map at near-zero token cost.

### Tier 2: Targeted Reads (On-Demand)

Only read files when you need specifics for the current task:

```
- Config files (vite.config, tsconfig, wrangler.toml) — build/deploy setup
- Entry points (main.jsx, app.py, index.ts) — application bootstrap
- Route definitions — page/endpoint structure
- Schema/model files — data shapes
```

### Tier 3: Deep Exploration (Rare)

Full exploration of a subsystem. Only when the task requires understanding interconnected code across multiple files. Use the Explore agent for this.

## What to Map

### Directory Purpose Map
For each top-level directory, know:
- **What it contains** — Components? Services? Scripts? Config?
- **What depends on it** — Who imports from here?
- **Entry points** — Which files are "roots" vs "leaves"?

### Data Flow Map
Trace the critical paths:
- **User input → API → Database → Response → UI** — The main data pipeline
- **Auth flow** — Login → Token → Protected routes → Refresh
- **State management** — Where state lives, how it flows, what triggers updates

### Pattern Map
Identify the project's conventions:
- **File naming** — kebab-case? PascalCase? index.ts barrels?
- **Component structure** — Collocated styles? Separate test files? Hooks alongside components?
- **API pattern** — REST? GraphQL? RPC? How are endpoints organized?
- **Error handling** — Try/catch? Error boundaries? Global handler?
- **Testing** — What framework? What's the coverage pattern? Where do tests live?

## Map Storage

The map lives in your working memory — don't write it to a file. It's derived from code state and would go stale. Rebuild it each session from:

1. Project memory (persistent knowledge)
2. Quick directory scan (current state)
3. Targeted file reads (as needed)

Tier 1 is always worth it. Tier 2 is worth it for the task at hand. Tier 3 only for complex multi-file tasks.

## Rules

1. **Memory first** — Check what you already know before reading files
2. **Top-down** — Start with directory structure, then drill into files as needed
3. **Task-driven** — Map what's relevant to the current work, not the entire codebase
4. **Don't output the map** — It's your internal knowledge. Don't dump a file tree at the user.
5. **Update incrementally** — When you discover something new about the codebase, extend the map
6. **Convention over exploration** — If you see one component follows a pattern, assume others do too until proven otherwise
