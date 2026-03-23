Switch to Z AI (GLM-5) mid-session using anyclaude.

## If anyclaude is running (this session was started with anyclaude):

Just tell the user to type:
```
/model openai/glm-5
```
That's it. Mid-session switch. No restart needed.

To switch back to Claude:
```
/model opus
```
or
```
/model sonnet
```

## If this is a regular Claude session (not started with anyclaude):

Tell the user:
"This session was started with native Claude, which doesn't support mid-session provider switching. To get mid-session switching:
1. Quit Claude Code
2. Open a terminal and type: `zai`
3. This starts Claude Code through anyclaude with Z AI support
4. You can then switch between Claude and GLM-5 anytime with `/model openai/glm-5` and `/model opus`

Or start anyclaude normally with: `anyclaude` (starts on Claude, switch anytime)"

## Verify current API:
```bash
echo $ANTHROPIC_BASE_URL
```
- If empty or anthropic.com → native Claude
- If localhost:* → anyclaude (supports mid-session switching)
