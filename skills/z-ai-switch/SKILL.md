---
name: z-ai-switch
description: Mid-session model switching via anyclaude proxy. Switch between Claude Opus/Sonnet and Z AI GLM-5 with /model command — no restart needed. Proxy runs as background daemon, auto-starts on login.
user_invocable: true
---

# Multi-Model Switching (Built Into Desktop App)

## How It Works

An anyclaude proxy runs as a background daemon on localhost. Claude Code connects through it via `ANTHROPIC_BASE_URL`. The proxy translates between Anthropic format and other providers (Z AI, OpenAI, Google, xAI).

## Mid-Session Commands

Type these in the chat — they switch INSTANTLY, same session:
- `/model opus` → Claude Opus 4.6
- `/model sonnet` → Claude Sonnet 4.6
- `/model openai/glm-5` → Z AI GLM-5

## Proxy Management

- **Start proxy:** `bash ~/.claude/scripts/start-anyclaude-proxy.sh`
- **Stop proxy:** `bash ~/.claude/scripts/stop-proxy.sh`
- **Auto-start:** LaunchAgent at `~/Library/LaunchAgents/com.nick.anyclaude-proxy.plist`
- **Status check:** `cat ~/.claude/anyclaude-proxy.pid && kill -0 $(cat ~/.claude/anyclaude-proxy.pid) 2>/dev/null`

## Session Start

Check proxy status and announce:
```bash
kill -0 $(cat ~/.claude/anyclaude-proxy.pid 2>/dev/null) 2>/dev/null && echo "Proxy: ACTIVE" || echo "Proxy: INACTIVE"
```
- ACTIVE → "Multi-model switching available. Use `/model openai/glm-5` for Z AI."
- INACTIVE → normal Claude session
