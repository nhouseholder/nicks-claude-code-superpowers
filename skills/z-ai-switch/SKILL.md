---
name: z-ai-switch
description: Mid-session model switching via anyclaude proxy. Haiku 4.5 in picker = GLM-5 via Z AI. Always confirm which API is active with a banner message on every switch and session start. Type /z for help.
user_invocable: true
---

# Multi-Model Switching

## Model Picker Mapping

| Dropdown Label | Actual Model | API Provider |
|---|---|---|
| Opus 4.6 | Claude Opus 4.6 | Anthropic |
| Sonnet 4.6 | Claude Sonnet 4.6 | Anthropic |
| **Haiku 4.5** | **GLM-5** | **Z AI** (rate limits bypassed) |

"Haiku 4.5" in the picker is remapped to GLM-5 via the anyclaude proxy.

## Switching

Click the model dropdown (bottom right) and select. Or type:
- `/model opus` → Claude Opus
- `/model sonnet` → Claude Sonnet
- `/model openai/glm-5` → Z AI GLM-5 (same as selecting Haiku)

## Proxy Management

- **Start:** `bash ~/.claude/scripts/start-anyclaude-proxy.sh`
- **Stop:** `bash ~/.claude/scripts/stop-proxy.sh`
- **Auto-starts on login** via LaunchAgent
