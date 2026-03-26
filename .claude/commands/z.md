Switch models mid-session via the anyclaude proxy. Supports Z AI GLM-5, Claude Opus, and Claude Sonnet.

## Phase 1: Status Check
```bash
# Check proxy status
if [ -f ~/.claude/anyclaude-proxy.pid ] && kill -0 $(cat ~/.claude/anyclaude-proxy.pid) 2>/dev/null; then
  echo "PROXY: RUNNING"
  echo "URL: $(cat ~/.claude/anyclaude-proxy.url 2>/dev/null)"
  echo "PID: $(cat ~/.claude/anyclaude-proxy.pid)"
else
  echo "PROXY: NOT RUNNING"
fi
```

Display current status:
```
Model Router Status
===================
Proxy: [RUNNING / NOT RUNNING]
Current model: [detect from session — Opus shows 🟠, Haiku/GLM-5 shows 🟢, Sonnet shows 🔵]

Available models:
  /model opus              → Claude Opus 4.6 (Anthropic direct)
  /model sonnet            → Claude Sonnet 4.6 (Anthropic direct)
  /model openai/glm-5      → Z AI GLM-5 (via proxy — Haiku slot)

Routing: Haiku in model picker = GLM-5 via Z AI proxy
```

## Phase 2: Action

### If proxy is RUNNING
Tell the user they can switch immediately:
- `/model openai/glm-5` → Z AI GLM-5
- `/model opus` → Claude Opus
- `/model sonnet` → Claude Sonnet

Switches are instant, same session. No restart needed.

### If proxy is NOT RUNNING
```bash
# Check if start script exists
if [ -f ~/.claude/scripts/start-anyclaude-proxy.sh ]; then
  bash ~/.claude/scripts/start-anyclaude-proxy.sh
  sleep 2
  # Verify it started
  if [ -f ~/.claude/anyclaude-proxy.pid ] && kill -0 $(cat ~/.claude/anyclaude-proxy.pid) 2>/dev/null; then
    echo "Proxy started successfully"
    echo "URL: $(cat ~/.claude/anyclaude-proxy.url 2>/dev/null)"
  else
    echo "ERROR: Proxy failed to start. Check logs:"
    echo "  cat ~/.claude/logs/anyclaude-proxy.log"
    echo "  Possible causes: port conflict, missing dependencies, auth issue"
  fi
else
  echo "ERROR: start-anyclaude-proxy.sh not found at ~/.claude/scripts/"
  echo "The proxy scripts may need to be reinstalled."
fi
```

After starting: "Proxy started. Quit and reopen Claude Code to connect through it. After reopening, `/model openai/glm-5` will switch to Z AI."

### Stop the proxy
```bash
if [ -f ~/.claude/scripts/stop-proxy.sh ]; then
  bash ~/.claude/scripts/stop-proxy.sh
  echo "Proxy stopped. Using direct Anthropic connection."
else
  # Manual stop
  kill $(cat ~/.claude/anyclaude-proxy.pid 2>/dev/null) 2>/dev/null
  rm -f ~/.claude/anyclaude-proxy.pid ~/.claude/anyclaude-proxy.url
  echo "Proxy stopped manually."
fi
```

## Error Recovery
If the proxy is unresponsive or models aren't switching:
1. Kill stale process: `kill -9 $(cat ~/.claude/anyclaude-proxy.pid) 2>/dev/null`
2. Clean up PID file: `rm -f ~/.claude/anyclaude-proxy.pid`
3. Restart: `bash ~/.claude/scripts/start-anyclaude-proxy.sh`
4. If port conflict: `lsof -i :17532` to find what's using the port
5. If still broken: "Proxy needs manual troubleshooting. Check `~/.claude/logs/anyclaude-proxy.log`"
