---
name: z-ai-switch
description: Toggle between Claude (Anthropic) and Z AI (GLM-5) APIs. Single command /z toggles between them. At session start, always check and announce which API is active.
user_invocable: true
---

# Z AI API Toggle

## Session Start — Always Announce Active API

At the start of EVERY session, check which API is active:
```bash
jq -r '.env.ANTHROPIC_BASE_URL // empty' ~/.claude/settings.json
```
- If empty → announce: "API: Claude (Anthropic)"
- If `https://api.z.ai/api/anthropic` → announce: "API: Z AI (GLM-5)"

## /z — Toggle API

Single command toggles between Claude and Z AI:
- If currently Claude → switch to Z AI
- If currently Z AI → switch back to Claude
- Always saves handoff before switching
- User must quit and reopen app to activate
