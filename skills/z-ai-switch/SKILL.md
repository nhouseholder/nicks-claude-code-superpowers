---
name: z-ai-switch
description: Dynamic model routing — Haiku 4.5 in picker = GLM-5 via Z AI. Opus/Sonnet = Anthropic. No restart needed. Type /z for help.
user_invocable: true
---

# Dynamic Model Router — Z AI Integration

## How It Works

A local proxy runs permanently (started at login via LaunchAgent):
- **Opus/Sonnet** in model picker → routed to **Anthropic** (native Claude)
- **Haiku 4.5** in model picker → routed to **Z AI (GLM-5)**
- If Z AI fails → **auto-fallback to Anthropic** (never breaks)

Switch models mid-session by clicking the model dropdown. No restart needed.

## Setup (one-time)

```bash
bash ~/.claude/scripts/setup-model-router.sh
```
Then restart Claude Code. The proxy runs forever via LaunchAgent.

## Emergency Uninstall

If anything breaks:
```bash
bash ~/.claude/scripts/uninstall-model-router.sh
```
Then restart Claude Code. Direct Anthropic connection restored.

## Verifying Active API

The `api-banner.py` hook automatically:
- Prefixes every response with 🟢 (GLM-5) or 🟠 (Anthropic)
- Injects reasoning scaffolding when GLM-5 is active (zero cost on Opus)
- Shows session banner on start

You can also check: `curl http://127.0.0.1:17532/health`

## Files

| File | Purpose |
|---|---|
| `~/.claude/scripts/model-router-proxy.py` | The proxy (routes by model ID) |
| `~/Library/LaunchAgents/com.claude.model-router.plist` | Keeps proxy alive (auto-restart) |
| `~/.claude/scripts/setup-model-router.sh` | One-time setup |
| `~/.claude/scripts/uninstall-model-router.sh` | Emergency teardown |

## Safety Rules

1. Proxy uses LaunchAgent with KeepAlive — auto-restarts if it crashes
2. If Z AI is unreachable, proxy forwards to Anthropic (never fails)
3. Health check at `http://127.0.0.1:17532/health`
4. All state is in the proxy process — settings.json only has the localhost URL
5. Uninstall script restores everything in one command
