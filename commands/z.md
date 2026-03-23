Toggle between Claude (Anthropic) and Z AI (GLM-5) APIs.

## Steps to execute:

1. Check which API is currently active:
```bash
jq -r '.env.ANTHROPIC_BASE_URL // "anthropic (native)"' ~/.claude/settings.json
```

2. If currently on Anthropic (no ANTHROPIC_BASE_URL), switch TO Z AI:
```bash
jq '.env.ANTHROPIC_AUTH_TOKEN = .env.Z_AI_API_KEY | .env.ANTHROPIC_BASE_URL = "https://api.z.ai/api/anthropic"' ~/.claude/settings.json > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json
```
Then tell the user: "Switched to **Z AI (GLM-5)**. Quit and reopen Claude Code to activate."

3. If currently on Z AI (ANTHROPIC_BASE_URL exists), switch BACK to Claude:
```bash
jq 'del(.env.ANTHROPIC_AUTH_TOKEN) | del(.env.ANTHROPIC_BASE_URL)' ~/.claude/settings.json > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json
```
Then tell the user: "Switched back to **Claude (Anthropic)**. Quit and reopen Claude Code to activate."

4. Save a handoff document before the user restarts:
   - What was being worked on
   - What's done, what's next
   Save to `~/.claude/handoff.md`

5. Tell the user: "Your handoff is saved. After reopening, type 'load my handoff' to resume."
