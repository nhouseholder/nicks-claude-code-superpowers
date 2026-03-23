#!/bin/bash
# Switch Claude Code between Anthropic (Claude) and Z AI (GLM-5)
# Usage:
#   source ~/.claude/scripts/switch-provider.sh zai    # Switch to Z AI / GLM-5
#   source ~/.claude/scripts/switch-provider.sh claude  # Switch back to Anthropic
#   source ~/.claude/scripts/switch-provider.sh status   # Show current provider

SETTINGS_FILE="$HOME/.claude/settings.json"
BACKUP_FILE="$HOME/.claude/settings.anthropic.json"
ZAI_SETTINGS="$HOME/.claude/settings.zai.json"

case "${1:-status}" in
  zai|glm|glm5|z)
    # Backup current Anthropic settings if not already backed up
    if [ ! -f "$BACKUP_FILE" ]; then
      cp "$SETTINGS_FILE" "$BACKUP_FILE"
    fi

    # Update settings.json to use Z AI
    python3 -c "
import json
with open('$SETTINGS_FILE', 'r') as f:
    settings = json.load(f)

settings['env']['ANTHROPIC_AUTH_TOKEN'] = settings['env'].get('Z_AI_API_KEY', '')
settings['env']['ANTHROPIC_BASE_URL'] = 'https://api.z.ai/api/anthropic'
settings['env']['API_TIMEOUT_MS'] = '3000000'
settings['env']['ANTHROPIC_DEFAULT_OPUS_MODEL'] = 'glm-5'
settings['env']['ANTHROPIC_DEFAULT_SONNET_MODEL'] = 'glm-5'
settings['env']['ANTHROPIC_DEFAULT_HAIKU_MODEL'] = 'glm-4.5-air'

with open('$SETTINGS_FILE', 'w') as f:
    json.dump(settings, f, indent=2)
"
    echo "Switched to Z AI (GLM-5). Start a NEW Claude Code session to take effect."
    echo "Run: source ~/.claude/scripts/switch-provider.sh claude  — to switch back"
    ;;

  claude|anthropic|back)
    # Restore Anthropic settings
    if [ -f "$BACKUP_FILE" ]; then
      cp "$BACKUP_FILE" "$SETTINGS_FILE"
      echo "Switched back to Anthropic (Claude). Start a NEW Claude Code session to take effect."
    else
      # Just remove Z AI env vars
      python3 -c "
import json
with open('$SETTINGS_FILE', 'r') as f:
    settings = json.load(f)

for key in ['ANTHROPIC_AUTH_TOKEN', 'ANTHROPIC_BASE_URL', 'ANTHROPIC_DEFAULT_OPUS_MODEL', 'ANTHROPIC_DEFAULT_SONNET_MODEL', 'ANTHROPIC_DEFAULT_HAIKU_MODEL']:
    settings['env'].pop(key, None)

with open('$SETTINGS_FILE', 'w') as f:
    json.dump(settings, f, indent=2)
"
      echo "Switched back to Anthropic (Claude). Start a NEW Claude Code session to take effect."
    fi
    ;;

  status)
    if python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    s = json.load(f)
if s.get('env', {}).get('ANTHROPIC_BASE_URL', '').startswith('https://api.z.ai'):
    model = s['env'].get('ANTHROPIC_DEFAULT_OPUS_MODEL', 'glm-4.7')
    print(f'Provider: Z AI ({model})')
else:
    print('Provider: Anthropic (Claude)')
"; then true; fi
    ;;

  *)
    echo "Usage: source ~/.claude/scripts/switch-provider.sh [zai|claude|status]"
    echo "  zai    — Switch to Z AI / GLM-5"
    echo "  claude — Switch back to Anthropic / Claude"
    echo "  status — Show current provider"
    ;;
esac
