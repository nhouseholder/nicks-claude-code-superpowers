# Superpowers Repo — Session Handoff

**Date**: 2026-03-24
**GitHub Repo**: https://github.com/nhouseholder/nicks-claude-code-superpowers
**GLM Router Repo**: https://github.com/nhouseholder/claude-glm-router
**Local Copy**: `/Users/nicholashouseholder/Library/Mobile Documents/com~apple~CloudDocs/superpowers/`
**Installed To**: `~/.claude/skills/`, `~/.claude/commands/`, `~/.claude/hooks/`

---

## Current State

### GLM-5 Integration (Z AI Router) — WORKING
- **Proxy**: `~/.claude/scripts/model-router-proxy.py` (v6) on port 17532
- **LaunchAgent**: `~/Library/LaunchAgents/com.claude.model-router.plist`
- **How it works**: Haiku in model picker → proxy routes to Z AI (GLM-5). Opus/Sonnet → Anthropic direct.
- **Banner**: `api-banner.py` injects 🟠 (Opus/Sonnet) or 🟢 (GLM-5) emoji at response start
- **Session bridge**: `session-bridge.py` injects Opus's last checkpoint when GLM-5 takes over
- **Auto-checkpoint**: `auto-checkpoint.py` writes `~/.claude/last-checkpoint.json` on every Stop event (zero tokens, disk-only)
- **Focus guard**: `glm5-focus-guard.py` catches GLM-5 hallucinating during tool use
- **GLM-5 scaffolding**: Injected dynamically by `api-banner.py` (NOT a separate skill)

### Bug Fixed This Session
- **False green emoji in Opus sessions**: `detect_model.py` fell back to proxy's stale `/last-route`. Fix: removed fallback, default to "opus" when `CLAUDE_MODEL` is empty.

### Active Hooks (in settings.json)
| Event | Hook | Purpose |
|---|---|---|
| SessionStart | api-banner.py | API routing banner |
| UserPromptSubmit | api-banner.py | Emoji + GLM-5 scaffolding |
| UserPromptSubmit | session-bridge.py | Opus checkpoint for GLM-5 |
| UserPromptSubmit | improve-prompt.py | Prompt enrichment |
| PreToolUse | rtk-rewrite.sh | Token optimization |
| PreToolUse | block-dangerous-commands.py | Safety |
| Stop | auto-checkpoint.py | State save for GLM-5 handoff |
| PostToolUse | glm5-focus-guard.py | GLM-5 hallucination guard |
| PostToolUse | observe.py | Skill performance observation |

### Archived This Session
- `stop-memory-save.py` → `.ARCHIVED.py` (was #1 token burner)
- `track-skill-performance.js` → `.ARCHIVED.js` (removed from settings)

### Skills: 75 (at cap). Token savings: 381K→302K chars.

### GLM-5 Confidence
| Task Type | Confidence |
|---|---|
| Single-file edits | High |
| Following plans | High |
| Multi-file debugging | Medium-low |
| Domain math | Medium-low |
| Large refactors | Low |

### Known Issues
1. GLM-5 runaway generation on complex codebases
2. Subagent emoji overlap mid-response
3. Skill count at cap (75)
4. observe.py may add PostToolUse overhead — audit if needed
