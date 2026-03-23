#!/bin/bash
# Swap Claude Code back to native Anthropic API
# Usage: ~/.claude/scripts/swap-to-claude.sh

SETTINGS="$HOME/.claude/settings.json"

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "ERROR: jq is required. Install with: brew install jq"
    exit 1
fi

# Remove Z AI routing vars (keep Z_AI_API_KEY for future use)
jq 'del(.env.ANTHROPIC_AUTH_TOKEN) |
    del(.env.ANTHROPIC_BASE_URL) |
    del(.env.ANTHROPIC_DEFAULT_HAIKU_MODEL) |
    del(.env.ANTHROPIC_DEFAULT_SONNET_MODEL) |
    del(.env.ANTHROPIC_DEFAULT_OPUS_MODEL)' "$SETTINGS" > "$SETTINGS.tmp" && mv "$SETTINGS.tmp" "$SETTINGS"

echo "SWITCHED BACK TO CLAUDE (Native Anthropic API)"
echo "  All models → Anthropic (Opus, Sonnet, Haiku)"
echo ""
echo "⚠️  Restart Claude Code for changes to take effect."
