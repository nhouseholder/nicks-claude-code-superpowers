# Push to GitHub

The repository syncs to: `https://github.com/nhouseholder/nicks-claude-code-superpowers`

## Standard Sync Workflow

```bash
# Clone to /tmp (never push from iCloud)
cd /tmp && rm -rf superpowers-sync
git clone https://github.com/nhouseholder/nicks-claude-code-superpowers.git superpowers-sync

# Copy updated files from live
cp -r ~/.claude/skills/* /tmp/superpowers-sync/skills/
cp -r ~/.claude/hooks/* /tmp/superpowers-sync/hooks/
cp ~/.claude/settings.json /tmp/superpowers-sync/settings.json

# Commit and push
cd /tmp/superpowers-sync
git add -A
git commit -m "Sync superpowers from live"
git push origin main

# Clean up
rm -rf /tmp/superpowers-sync
```

## Platform Notes

This repo contains skills shared across multiple AI coding platforms:
- **Claude Code** (`~/.claude/`) — Primary platform. Uses `CLAUDE.md`, `settings.json`
- **OpenAI Codex CLI** (`~/.codex/`) — Uses `AGENTS.md`
- **GitHub Copilot** — `copilot-learning-log.py` hook

## First-Time Setup

If the repo doesn't exist yet:
```bash
gh repo create nicks-claude-code-superpowers --public --source=. --push
```
