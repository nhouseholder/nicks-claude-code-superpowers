---
name: seamless-resume
description: When the user sends "continue", "go", "keep going", or returns to a paused session, resume execution instantly without re-reading files, re-explaining context, or asking clarifying questions. Pick up exactly where you left off as if the break never happened. Always-on awareness skill.
---

# Seamless Resume — Pick Up Exactly Where You Left Off

When the user returns to a session after a pause (tab switch, timeout, or interruption), resume instantly. No re-reading, no re-explaining, no "where were we?"

## Always Active

This skill fires whenever:
- The user sends "continue", "go", "keep going", "yes", "proceed", or similar
- The conversation resumes after a compaction/summary
- The user returns to a session that was interrupted mid-task

## The Resume Protocol

### Step 1: Identify Where You Stopped
Check what was happening when execution paused:
- Were you mid-edit? → Complete the edit
- Were you mid-plan execution? → Pick up the next uncompleted step
- Were you about to run a command? → Run it
- Were you waiting for a tool result? → Re-run the tool call
- Were you mid-response? → Continue writing from where you left off

### Step 2: Resume Without Ceremony
**DO:**
- Continue the exact task that was in progress
- Pick up at the exact step/file/function you were working on
- Maintain the same approach and plan
- If you had pending tool calls, make them immediately

**DO NOT:**
- Say "Welcome back!" or "Let me catch you up" or "Where were we?"
- Re-read files you already read before the pause
- Re-explain decisions already made
- Ask "Should I continue?" — the user already said to continue
- Restart the task from the beginning
- Summarize what was done before the pause (they can scroll up)

### Step 3: Brief Status Only If Needed
If the pause was long enough that context was compacted, give a ONE-LINE status:
```
Continuing — [current step of N] — [what's being done right now]
```

Then immediately proceed. No elaboration.

## Handling Crash Recovery (New Session After Disconnect/Crash)

When a NEW session starts and the user says "continue" or "pick up where I left off" or references work from a previous session:

1. **Read `current_work.md`** from project memory — this is the crash-safe checkpoint
   ```
   Read ~/.claude/projects/<project>/memory/current_work.md
   ```
2. If it exists and has active work:
   - Read the "Resume Instructions" section
   - Read the "Files Modified This Session" to know what was being touched
   - Pick up at the first incomplete step
   - Tell the user in ONE line: "Resuming — [task], picking up at [step]"
3. If it says "No active work" or doesn't exist:
   - Check git log for recent commits to understand what was last done
   - Ask the user what they'd like to work on

**This is the key difference from in-session resume**: after a crash, you DON'T have conversation context. `current_work.md` IS your context. Trust it.

## Handling "continue" After Compaction

When a conversation is compacted (context compressed), the summary includes task state. Use it:

1. Read the compaction summary (it's already in context)
2. Identify the last completed step
3. Start the next step immediately
4. Do NOT re-read files that were already processed (unless you need specific content)

## Handling Multi-Step Plans

If executing a plan when interrupted:
- Check TodoWrite/task state for progress markers
- Resume at the first incomplete task
- Don't re-verify completed tasks unless something seems wrong

## Rules

1. **"Continue" means GO** — not "tell me what you were doing"
2. **Zero ceremony** — no greetings, no recaps, no "let me pick up where I left off"
3. **One-line status max** — if context was lost, one line. Then execute.
4. **Don't re-read** — trust your context. Only re-read if you genuinely need the content
5. **Don't re-ask** — if the user already approved an approach, don't re-confirm
6. **Match the previous pace** — if you were moving fast, keep moving fast
