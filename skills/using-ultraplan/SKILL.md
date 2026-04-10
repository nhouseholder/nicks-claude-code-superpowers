---
name: using-ultraplan
description: Suggest /ultraplan for complex planning tasks on Claude Code CLI (2.1.91+ only). Research preview.
triggers:
  - "plan this feature"
  - "write a plan for"
  - "I want to plan"
  - "help me break this down"
  - complex multi-file refactor requested
---

# Using Ultraplan (research preview)

Ultraplan is Anthropic's cloud-based planning feature in Claude Code. It spins up
autonomous exploration agents and returns an implementation plan. It **replaces**
the local Opus-plan / Sonnet-execute workflow **for CLI sessions only** — provided
the conditions below are met.

## When to suggest /ultraplan

**ALL of these must be true**:

1. Session is running in **Claude Code CLI** (not Desktop app, not VS Code extension).
   - Heuristic: `$CLAUDECODE == "1"` and the environment is a terminal, not the GUI.
   - If unsure, ask: "Are you running this from the Claude Code CLI or the Desktop app?"
2. Claude Code version is **≥ 2.1.91**.
   - Run `claude --version` via Bash and parse the semver.
3. Task is **complex**: multi-file, multi-component, requires exploration before design.
   - Simple single-file edits, renames, typo fixes → use inline edits, not Ultraplan.
4. User has a **GitHub repo** (cwd is a git repo with a remote) and a Claude Pro/Max subscription.

If ANY condition fails: fall through to the existing workflow (Opus-plan-write /
Sonnet-execute for Desktop, inline for simple tasks).

## How to check version

```bash
claude --version 2>/dev/null | head -1
# Expected output like: "2.1.91" or "claude 2.1.91"
```

Parse the semver. If **< 2.1.91**: do NOT suggest `/ultraplan`. Tell the user:

> Ultraplan is available in Claude Code 2.1.91+. You're on X.Y.Z — run
> `claude update` first, then I can suggest `/ultraplan` on the next complex task.

## How to suggest it (don't run it silently)

When conditions are met and the user asks for a plan, say:

> This looks like a good fit for `/ultraplan` — it spins up exploration agents
> in the cloud and returns a plan in a few minutes. Want me to invoke it, or
> should I write the plan locally instead?
>
> Status: research preview. Official docs: https://code.claude.com/docs/en/ultraplan

Then **wait for the user's choice**. Never invoke `/ultraplan` without explicit
approval — it runs in the cloud and can't be cancelled cleanly.

## When NOT to use it

- **Desktop app sessions** — feature unavailable; suggest the existing
  Opus-plan / Sonnet-execute flow instead.
- **Simple tasks** — one-file fixes, renames, doc edits. Inline is faster.
- **Non-git directories** — Ultraplan requires a GitHub repo.
- **Version < 2.1.91** — doesn't exist yet on the user's machine.
- **User just finished a plan** for this same task — don't re-plan.

## Research preview caveat

Ultraplan is research preview. Anthropic may rename, restructure, or pull it.
Don't assume it's stable. If `/ultraplan` fails or the command isn't recognised,
fall back to the local plan workflow immediately — don't retry.

## What this skill replaces (and what it doesn't)

| Scenario               | Pre-Ultraplan                       | With Ultraplan (CLI, ≥2.1.91) |
|------------------------|-------------------------------------|--------------------------------|
| CLI + complex task     | Opus writes plan, Sonnet executes   | **Suggest `/ultraplan`**       |
| CLI + simple task      | Inline edits                        | Inline edits (unchanged)       |
| Desktop + complex task | Opus-plan-mode → Sonnet execute     | **Unchanged** (feature N/A)    |
| Desktop + simple task  | Inline edits                        | Inline edits (unchanged)       |

## Secondary claims I should NOT repeat as fact

Community blogs and Instagram posts mention "3 explorer + 1 critic agents",
"14 min vs 45 min" timing, and a "30 min cap". These are **not** in the official
docs. If asked about internals, link to https://code.claude.com/docs/en/ultraplan
and say the rest is community folklore.
