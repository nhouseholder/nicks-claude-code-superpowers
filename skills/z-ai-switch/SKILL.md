---
name: z-ai-switch
description: Switch to Z AI (GLM-5) when rate limited on Claude. Two-instance approach — no restart needed. Just open a new terminal and type 'zai', or double-click 'Claude (Z AI).command' on Desktop.
user_invocable: true
---

# Z AI Fallback — When Rate Limited

When you hit Anthropic API rate limits, switch to a Z AI-backed Claude Code instance.

## How to Switch (no restart needed)

**Option A — Terminal:** Open a new terminal tab/window and type:
```bash
zai
```

**Option B — Desktop:** Double-click `Claude (Z AI).command` on your Desktop.

Both launch a fresh Claude Code session backed by GLM-5 via Z AI's Anthropic-compatible API. Your skills, CLAUDE.md, memory, and project context all load normally — they're local files.

## What Happens

- A NEW Claude Code session starts on Z AI (separate from your rate-limited one)
- Z AI has its own rate limits (independent of Anthropic)
- All 67 skills work (they're loaded from `~/.claude/skills/`)
- Tool use (Read, Edit, Bash, Agent) works through Z AI's Anthropic-compatible endpoint

## When to Use

- "API Error: Rate limit reached" on Claude
- "You've hit your limit" message
- Want to keep working while Anthropic limits reset

## Limitations

- GLM-5 may not match Opus 4.6 on complex reasoning tasks
- It's a new session — doesn't carry over conversation from the rate-limited session
- Use auto-handoff to transfer context: write a handoff doc in the old session, load it in the new one
