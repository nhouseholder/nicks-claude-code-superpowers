Switch models mid-session via the anyclaude proxy.

## Steps to execute:

1. Check if the anyclaude proxy is running:
```bash
cat ~/.claude/anyclaude-proxy.pid 2>/dev/null && kill -0 $(cat ~/.claude/anyclaude-proxy.pid) 2>/dev/null && echo "RUNNING: $(cat ~/.claude/anyclaude-proxy.url)" || echo "NOT RUNNING"
```

2. If proxy is running, tell the user they can switch models right now:
   - `/model openai/glm-5` → Z AI GLM-5
   - `/model opus` → Claude Opus
   - `/model sonnet` → Claude Sonnet
   Just type the /model command — it switches instantly, same session.

3. If proxy is NOT running, start it:
```bash
bash ~/.claude/scripts/start-anyclaude-proxy.sh
```
Then tell user: "Proxy started. Quit and reopen Claude Code to connect through it. After reopening, `/model openai/glm-5` will switch to Z AI mid-session."

4. To stop the proxy and go back to direct Anthropic:
```bash
bash ~/.claude/scripts/stop-proxy.sh
```
