Switch back to native Claude (Anthropic) API from Z AI.

## Steps to execute:

1. Run this command to remove Z AI routing from settings.json:
```bash
jq 'del(.env.ANTHROPIC_AUTH_TOKEN) | del(.env.ANTHROPIC_BASE_URL)' ~/.claude/settings.json > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json
```

2. Tell the user:
   "Settings restored to native Claude (Anthropic). To activate:
   - **Cmd+Shift+P → 'Reload Window'** or **quit and reopen Claude Code**
   - All skills and memory will load automatically
   - Your handoff from the Z AI session is at `~/.claude/handoff.md` if you need it"
