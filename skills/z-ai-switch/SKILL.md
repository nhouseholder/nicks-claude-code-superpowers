---
name: z-ai-switch
description: Z AI GLM-5 fallback when Anthropic rate limits hit. Uses environment variables only (NEVER settings.json). Type /z for setup help.
user_invocable: true
---

# Z AI GLM-5 — Rate Limit Escape Hatch

## CRITICAL SAFETY RULE

**NEVER put `ANTHROPIC_BASE_URL` in `~/.claude/settings.json`.** Settings.json is shared across ALL sessions. If the endpoint fails, EVERY session breaks. Use environment variables via the launch script only.

## Session Start Banner

At the start of EVERY session, check and announce:

If `ZAI_ACTIVE` env var is set OR `ANTHROPIC_BASE_URL` contains "z.ai":
```
🟢 Z AI MODE — GLM-5 Active | Anthropic rate limits bypassed
```

If NOT set (normal Anthropic):
```
🔵 Anthropic API — Claude Opus/Sonnet Active
```

## How to Switch (Desktop App)

**To Z AI (when rate limited):**
1. Quit Claude Code (Cmd+Q)
2. Open Terminal.app
3. Type: `zai`
4. Claude Code opens with GLM-5 — green banner confirms

**Back to Anthropic:**
1. Quit the Z AI session (Cmd+Q)
2. Open Claude Code normally (from Dock/Spotlight)
3. Blue banner confirms Anthropic API

## How It Works

The `zai` command runs `~/.claude/scripts/zai-launch.sh` which:
1. **Failsafe:** checks settings.json is clean (auto-removes any stale ANTHROPIC_BASE_URL)
2. **Connectivity test:** pings Z AI endpoint (2s timeout)
3. **Auto-fallback:** if Z AI unreachable, falls back to normal Anthropic Claude
4. **Launches Claude Code** with Z AI env vars (affects ONLY this session)
5. All skills, memory, CLAUDE.md, and anti-patterns load normally

## Verifying Which API Is Active

Ask Claude: "which API am I using?" — it should check:
```bash
echo $ANTHROPIC_BASE_URL
echo $ZAI_ACTIVE
```
- Empty / not set = Anthropic (normal)
- Contains "z.ai" = Z AI GLM-5

## Rate Limits

Z AI has its own rate limits (separate from Anthropic). They're per-account and dynamic. Check yours at: z.ai/manage-apikey/rate-limits

Tool calls (Read, Edit, Bash, Agent) go through Z AI's Anthropic-compatible endpoint which translates them to Z AI's native format.
