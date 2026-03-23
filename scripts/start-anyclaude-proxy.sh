#!/bin/bash
# Start anyclaude as a background proxy daemon
# The Claude Desktop app connects through this proxy
# Enables mid-session model switching with /model openai/glm-5

PIDFILE="$HOME/.claude/anyclaude-proxy.pid"
URLFILE="$HOME/.claude/anyclaude-proxy.url"
LOGFILE="$HOME/.claude/anyclaude-proxy.log"

# Check if already running
if [ -f "$PIDFILE" ] && kill -0 "$(cat $PIDFILE)" 2>/dev/null; then
    PROXY_URL=$(cat "$URLFILE" 2>/dev/null)
    echo "anyclaude proxy already running (PID $(cat $PIDFILE))"
    echo "Proxy URL: $PROXY_URL"
    exit 0
fi

# Set provider API keys
export OPENAI_API_KEY="${OPENAI_API_KEY:-d8047c5f5b4246fd9a94b672adfe4882.t2Sn4v37ISjM4IaE}"
export OPENAI_API_URL="${OPENAI_API_URL:-https://api.z.ai/api/paas/v4/}"
export PROXY_ONLY="true"

# Start proxy in background, capture the URL from stdout
anyclaude > "$LOGFILE" 2>&1 &
PROXY_PID=$!
echo $PROXY_PID > "$PIDFILE"

# Wait for proxy to start and capture URL
sleep 2
PROXY_URL=$(grep -o 'http://localhost:[0-9]*' "$LOGFILE" | head -1)

if [ -z "$PROXY_URL" ]; then
    echo "ERROR: Failed to start anyclaude proxy. Check $LOGFILE"
    kill $PROXY_PID 2>/dev/null
    rm -f "$PIDFILE"
    exit 1
fi

echo "$PROXY_URL" > "$URLFILE"

# Update settings.json to point at the proxy
if command -v jq &> /dev/null; then
    jq --arg url "$PROXY_URL" '.env.ANTHROPIC_BASE_URL = $url | .env.ANTHROPIC_DEFAULT_HAIKU_MODEL = "openai/glm-5"' ~/.claude/settings.json > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json
    echo "Updated settings.json: ANTHROPIC_BASE_URL = $PROXY_URL, Haiku → GLM-5"
fi

echo ""
echo "╔═══════════════════════════════════════════════╗"
echo "║  anyclaude proxy running (PID $PROXY_PID)"
echo "║  Proxy URL: $PROXY_URL"
echo "║                                               ║"
echo "║  Claude Desktop app will now route through    ║"
echo "║  the proxy. Restart the app to connect.       ║"
echo "║                                               ║"
echo "║  Mid-session switching available:              ║"
echo "║    /model opus          → Claude Opus          ║"
echo "║    /model sonnet        → Claude Sonnet        ║"
echo "║    /model openai/glm-5  → Z AI GLM-5           ║"
echo "║                                               ║"
echo "║  To stop: ~/.claude/scripts/stop-proxy.sh     ║"
echo "╚═══════════════════════════════════════════════╝"
