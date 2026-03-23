---
name: z-ai-switch
description: Z AI GLM-5 fallback when Anthropic rate limits hit. Uses anyclaude proxy via environment variables (NEVER settings.json). Type /z for setup help.
user_invocable: true
---

# Z AI Fallback — Rate Limit Escape Hatch

## CRITICAL SAFETY RULE

**NEVER modify `ANTHROPIC_BASE_URL` in `~/.claude/settings.json`.** That file is shared across ALL sessions. If the proxy dies, every session breaks.

Use environment variables or launch scripts instead — they only affect the specific session.

## How to Use (Desktop App)

When you hit Anthropic rate limits:

1. **Quit Claude Code** (Cmd+Q)
2. **Open Terminal**, run: `zai`
3. Claude Code opens with Z AI backend — all skills and memory work normally
4. When done, quit and reopen normally for Anthropic

## Setup

Add to `~/.zshrc`:
```bash
alias zai='ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/paas/v4 ANTHROPIC_API_KEY=your_zai_key claude'
```

Or for anyclaude proxy (if installed):
```bash
alias zai='anyclaude --provider zai --key your_key -- claude'
```

## Confirming Active API

At session start, check:
- `echo $ANTHROPIC_BASE_URL` — if empty or `https://api.anthropic.com`, you're on Anthropic
- If set to Z AI URL, you're on GLM-5

## Limitations

- Requires restarting Claude Code (no mid-session hot-swap)
- GLM-5 may handle complex tool use differently than Claude
- Use `glm5-boost` skill (auto-activates) to compensate for reasoning gaps
