---
name: z-ai-switch
description: Switch between Claude (Anthropic) and Z AI (GLM-5) APIs. Use /z to toggle. When rate limited on Claude, switch to Z AI as fallback. Haiku model slot maps to GLM-5.
user_invocable: true
---

# Z AI API Switch

Toggle between native Claude (Anthropic) and Z AI (GLM-5) as the backing API.

## How It Works

Z AI provides an Anthropic-compatible API endpoint. When activated:
- **Haiku 4.5 → GLM-5** (select via `/model haiku` to use GLM-5)
- **Opus/Sonnet → remain on Claude** (unless you override)
- All skills, CLAUDE.md, and memory still load (they're local files)

## Commands

### Switch TO Z AI
```bash
~/.claude/scripts/swap-to-zai.sh
```
Then restart Claude Code. Select `/model haiku` to use GLM-5.

### Switch BACK to Claude
```bash
~/.claude/scripts/swap-to-claude.sh
```
Then restart Claude Code.

## When to Use

- **Rate limited on Claude API** — switch to Z AI to keep working
- **Cost optimization** — GLM-5 for routine tasks, Claude Opus for complex reasoning
- **After switching**, remind user: "Restart Claude Code, then `/model haiku` for GLM-5"

## Important Notes

- Z AI endpoint: `https://api.z.ai/api/anthropic`
- API key stored in settings.json as `Z_AI_API_KEY`
- **Restart required** — settings.json env vars only load at startup
- GLM-5 may not handle all Claude-specific tool formats perfectly — flag issues
- Your skills and memory work normally (they're loaded from local files, not the API)
