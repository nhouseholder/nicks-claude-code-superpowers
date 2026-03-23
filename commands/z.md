Switch this Claude Code session to use Z AI (GLM-5) as the API backend.

## Steps to execute:

1. First, write a handoff document capturing the current session state:
   - What was being worked on
   - What's done, what's in progress, what's next
   - Any important context or decisions made
   Save it to `~/.claude/handoff.md`

2. Run this command to update settings.json with Z AI routing:
```bash
jq '.env.ANTHROPIC_AUTH_TOKEN = .env.Z_AI_API_KEY | .env.ANTHROPIC_BASE_URL = "https://api.z.ai/api/anthropic"' ~/.claude/settings.json > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json
```

3. Tell the user:
   "Settings updated to Z AI (GLM-5). To activate:
   - **Cmd+Shift+P → 'Reload Window'** or **quit and reopen Claude Code**
   - Your handoff is saved at `~/.claude/handoff.md` — paste 'load handoff' in the new session
   - All skills and memory will load automatically
   - To switch back later, type `/zback`"
