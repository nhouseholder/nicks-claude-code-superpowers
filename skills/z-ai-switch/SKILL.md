---
name: z-ai-switch
description: Switch between Claude (Anthropic) and Z AI (GLM-5) APIs from within Claude Code desktop app. Type /z to switch to Z AI when rate limited. Type /zback to return to Claude. Saves handoff doc automatically.
user_invocable: true
---

# Z AI API Switch (Desktop App)

When rate limited on Claude, type `/z` to switch to Z AI (GLM-5). Type `/zback` to return.

## How It Works

1. `/z` saves a handoff doc, updates settings.json to route through Z AI, then tells you to reload
2. After reload, Claude Code talks to Z AI's Anthropic-compatible endpoint (GLM-5)
3. All skills, CLAUDE.md, and memory load normally — they're local files
4. `/zback` reverses it — removes Z AI routing, tells you to reload

## Desktop App Reload

After `/z` or `/zback`, reload the app:
- **Cmd+Shift+P → type "reload"** or
- **Quit (Cmd+Q) and reopen**

## Important

- Z AI endpoint: `https://api.z.ai/api/anthropic`
- API key stored in settings.json as `Z_AI_API_KEY`
- Handoff saved to `~/.claude/handoff.md` — paste "load my handoff" in the new session
- GLM-5 may differ from Opus on complex reasoning — use for routine work when rate limited
