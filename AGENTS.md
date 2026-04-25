# Superpowers — OpenAI Codex CLI Instructions

> **Platform:** This file is for [OpenAI Codex CLI](https://github.com/openai/codex). Codex uses `AGENTS.md` the same way Claude Code uses `CLAUDE.md`.
> **Claude Code users:** See `CLAUDE.md` instead.

## Auto-Codebase Diagram Protocol — RUN BEFORE FIRST REPLY

**CORE PRINCIPLE: GENERATE ONCE, REUSE FOREVER.**

Before typing a single word to the user, execute this protocol:

```
STEP 1: Check Engram: mem_search(query="codebase diagram", topic_key="codebase/diagram/{PROJECT_NAME}")
    ├─ FOUND → mem_get_observation → check staleness (>7 days OR major refactor?) → FRESH = use it
    └─ NOT FOUND → Generate via CGC CLI:
         cgc index . --force
         cgc stats
         cgc analyze complexity --limit 10
         cgc analyze dead-code
         Synthesize → mem_save(topic_key="codebase/diagram/{PROJECT_NAME}", type="architecture")
         If mem_save times out → write to CODEBASE_DIAGRAM.md in project root
```

**STALE CRITERIA**: >7 days old, new top-level dirs, framework changed, >20% file churn, auth/deployment changed.

**Local fallback**: If Engram is empty, read `CODEBASE_DIAGRAM.md` from project root.

---

All universal rules (backtesting, walk-forward, caching, debugging, memory, behavioral rules) are in `~/.codex/AGENTS.md`. Do NOT duplicate them here.

## This Project

This repo contains the custom skills system. Skills are shared across platforms:
- **Claude Code:** Installed at `~/.claude/skills/`
- **OpenAI Codex CLI:** Installed at `~/.codex/skills/`

Syncs to GitHub at `nhouseholder/nicks-claude-code-superpowers`.

## Skill Management Rules

- **No stack cap.** Add skills freely. Merge duplicates when noticed, but don't block new skills.
- **Three-location sync:** Edit in live directory → clone to `/tmp/` → push to GitHub. Never git push from iCloud.
- **Weight classes:** Passive (unlimited), Light (max 5/msg), Heavy (max 2/msg). See skill-manager for classifications.
- **No skill is sacred.** If a skill consistently makes output worse, remove it.
- **Merge before adding.** Before creating a new skill, check if an existing skill can absorb the behavior.
