#!/bin/bash
# Stop the anyclaude proxy and restore direct Anthropic connection

PIDFILE="$HOME/.claude/anyclaude-proxy.pid"
URLFILE="$HOME/.claude/anyclaude-proxy.url"

# Kill proxy
if [ -f "$PIDFILE" ]; then
    kill "$(cat $PIDFILE)" 2>/dev/null
    rm -f "$PIDFILE" "$URLFILE"
    echo "Proxy stopped."
else
    echo "No proxy running."
fi

# Remove ANTHROPIC_BASE_URL from settings.json (restore direct connection)
if command -v jq &> /dev/null; then
    jq 'del(.env.ANTHROPIC_BASE_URL) | del(.env.ANTHROPIC_DEFAULT_HAIKU_MODEL)' ~/.claude/settings.json > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json
    echo "Restored direct Anthropic connection. Haiku restored to native."
fi

echo "Restart Claude Code to reconnect directly to Anthropic."
