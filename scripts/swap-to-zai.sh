#!/bin/bash
# Swap Claude Code to use Z AI (GLM-5) API
# Usage: ~/.claude/scripts/swap-to-zai.sh

SETTINGS="$HOME/.claude/settings.json"

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "ERROR: jq is required. Install with: brew install jq"
    exit 1
fi

# Backup current settings
cp "$SETTINGS" "$SETTINGS.backup"

# Check if already on Z AI
if jq -e '.env.ANTHROPIC_BASE_URL' "$SETTINGS" &>/dev/null 2>&1; then
    CURRENT=$(jq -r '.env.ANTHROPIC_BASE_URL' "$SETTINGS")
    if [ "$CURRENT" = "https://api.z.ai/api/anthropic" ]; then
        echo "Already using Z AI. To switch back: ~/.claude/scripts/swap-to-claude.sh"
        exit 0
    fi
fi

# Get Z AI API key from existing env
ZAI_KEY=$(jq -r '.env.Z_AI_API_KEY // empty' "$SETTINGS")
if [ -z "$ZAI_KEY" ]; then
    echo "ERROR: Z_AI_API_KEY not found in settings.json"
    exit 1
fi

# Add Z AI routing env vars
jq '.env.ANTHROPIC_AUTH_TOKEN = .env.Z_AI_API_KEY |
    .env.ANTHROPIC_BASE_URL = "https://api.z.ai/api/anthropic" |
    .env.ANTHROPIC_DEFAULT_HAIKU_MODEL = "GLM-5"' "$SETTINGS" > "$SETTINGS.tmp" && mv "$SETTINGS.tmp" "$SETTINGS"

echo "SWITCHED TO Z AI (GLM-5)"
echo "  Haiku 4.5 → GLM-5"
echo "  Opus/Sonnet → Claude (native)"
echo ""
echo "In Claude Code, select 'Haiku 4.5' via /model to use GLM-5."
echo "To switch back: ~/.claude/scripts/swap-to-claude.sh"
echo ""
echo "⚠️  Restart Claude Code for changes to take effect."
