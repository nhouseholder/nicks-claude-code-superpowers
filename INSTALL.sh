#!/bin/bash

# Nick's Claude Code Superpowers - One-click installer
# Run: curl -sL https://raw.githubusercontent.com/yourusername/nicks-claude-code-superpowers/main/INSTALL.sh | bash

set -e

echo "🚀 Installing Nick's Claude Code Superpowers..."

# Backup existing config
if [ -d "$HOME/.claude" ]; then
    BACKUP_DIR="$HOME/.claude.backup.$(date +%Y%m%d_%H%M%S)"
    echo "📦 Backing up existing config to: $BACKUP_DIR"
    cp -r "$HOME/.claude" "$BACKUP_DIR"
fi

# Clone repo (change this URL after pushing to GitHub)
REPO_URL="https://github.com/nhouseholder/nicks-claude-code-superpowers.git"
TEMP_DIR=$(mktemp -d)
echo "📥 Cloning from: $REPO_URL"
git clone "$REPO_URL" "$TEMP_DIR"

# Copy files
echo "📋 Installing skills, hooks, commands..."
cp -r "$TEMP_DIR/skills" "$HOME/.claude/"
cp -r "$TEMP_DIR/hooks" "$HOME/.claude/"
cp -r "$TEMP_DIR/commands" "$HOME/.claude/"
cp -r "$TEMP_DIR/homunculus" "$HOME/.claude/" 2>/dev/null || true
cp "$TEMP_DIR/CLAUDE.md" "$HOME/.claude/" 2>/dev/null || true
cp "$TEMP_DIR/settings.json" "$HOME/.claude/" 2>/dev/null || true

# Copy OpenViking integration files
echo "📋 Installing OpenViking context database integration..."
cp -r "$TEMP_DIR/openviking" "$HOME/.claude/" 2>/dev/null || true

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Active skills installed:"
ls "$HOME/.claude/skills" | head -25
echo "... and more"
echo ""
echo "Active hooks:"
ls "$HOME/.claude/hooks"
echo ""
echo "OpenViking integration:"
echo "  See openviking/README.md for setup instructions"
echo "  Run: pip install openviking (or use uv)"
echo ""
echo "Start a new Claude Code session and ask: 'What skills do you have?'"
echo "Or try: /mem show"
echo ""
