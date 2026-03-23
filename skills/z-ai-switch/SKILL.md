---
name: z-ai-switch
description: Mid-session switching between Claude (Anthropic) and Z AI (GLM-5). When started via anyclaude, switch anytime with /model openai/glm-5 (no restart). Type /z for instructions.
user_invocable: true
---

# Z AI Mid-Session Switching

## How It Works

**anyclaude** is a local proxy that translates between Anthropic's API format and other providers. When Claude Code runs through anyclaude, you can switch models mid-session:

- `/model openai/glm-5` → switches to Z AI (GLM-5)
- `/model opus` → switches back to Claude Opus
- `/model sonnet` → switches to Claude Sonnet

No restart. No handoff. Same session, same context, same skills.

## Starting anyclaude

From terminal: `zai` (alias) or `anyclaude`

## Session Start Check

At session start, check if running through anyclaude:
```bash
echo $ANTHROPIC_BASE_URL
```
- `http://localhost:*` → anyclaude active, mid-session switching available
- Empty or anthropic.com → native Claude, no mid-session switching

Announce: "API: [Claude/anyclaude]. Mid-session switching: [available/not available]."

## Z AI Config

- OpenAI-compatible endpoint: `https://api.z.ai/api/paas/v4/`
- API key: stored in settings.json as `OPENAI_API_KEY`
- Model ID: `openai/glm-5` (for anyclaude's `/model` command)
