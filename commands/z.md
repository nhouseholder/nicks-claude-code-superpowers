Switch to Z AI (GLM-5) API as a fallback when rate limited on Claude.

Run the swap script:
```bash
~/.claude/scripts/swap-to-zai.sh
```

After running, tell the user:
1. **Restart Claude Code** (quit and reopen) for the API change to take effect
2. Once restarted, select `/model haiku` — this now routes to GLM-5
3. To switch back later: run `~/.claude/scripts/swap-to-claude.sh` and restart

If the user says "switch back" or "go back to claude", run:
```bash
~/.claude/scripts/swap-to-claude.sh
```
