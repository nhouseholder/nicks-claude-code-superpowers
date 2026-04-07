---
name: skill-awareness
description: "MANDATORY first-thought on every prompt: 'Is there a skill, hook, command, or agent that handles this?' Before doing ANY work, Claude must scan the available skills list in the system prompt and identify which skills apply. If a matching skill exists and wasn't used, that's a failure. This skill exists because Claude repeatedly ignores installed skills and does tasks manually when specialized skills would produce better results. Always-on, fires on every message."
weight: passive
---

# Skill Awareness — Use Your Tools

## The Problem

Claude has 70+ specialized skills installed but doesn't use them. Real example:
- User asks to redesign a frontend
- `frontend-design` and `ui-ux-pro-max` skills exist — designed exactly for this
- Claude ignores both and writes components from scratch
- User has to ASK "did you use the frontend skills I installed?"
- Claude admits it didn't

This happens because Claude treats skills as passive background context instead of **active tools to invoke**. This skill fixes that.

## The Rule (Non-Negotiable)

**On EVERY prompt, before doing ANY work, ask yourself:**

> "Is there a skill, hook, command, or agent designed for this task?"

Then:
1. **Scan the skills list** in the system prompt (the `Available skills` section)
2. **Identify matching skills** by name, description, and trigger conditions
3. **Use them** — invoke the Skill tool, follow the skill's protocol, or activate the skill's checklist
4. **If no skill matches**, proceed normally

## How to Check

The system prompt contains a list like:
```
- frontend-design: Create distinctive, production-grade frontend interfaces...
- ui-ux-pro-max: UI/UX design intelligence. 50 styles, 21 palettes...
- fix-loop: Self-healing CI loop...
```

**Read this list.** Match against the current task. If a skill's description or triggers match what the user asked for, USE IT.

## Matching Rules

| User Request Contains | Check These Skills |
|----------------------|-------------------|
| frontend, UI, design, component, page, layout, style | `frontend-design`, `ui-ux-pro-max` |
| fix, bug, broken, error, failing | `fix-loop`, `systematic-debugging`, `pre-debug-check`, `website-guardian` |
| deploy, ship, push, release, go live | `deploy` |
| plan, design, architect, break down | `writing-plans`, `brainstorming`, `spec-interview` |
| test, TDD, coverage | `test-driven-development`, `qa-gate` |
| commit, git, branch, merge, push | `git-sorcery`, `version-bump` |
| research, learn, understand, how does | `deep-research`, `know-what-you-dont-know` |
| backtest, model, accuracy, prediction | `backtest`, `profit-driven-development` |
| website, webapp, site, page broke | `website-guardian`, `site-update-protocol` |
| review, check, audit, scan | `audit`, `reflexion`, `receiving-code-review` |
| parallel, multiple, concurrent | `dispatching-parallel-agents`, `parallel-sweep` |
| API, Claude API, Anthropic, SDK | `claude-api` |
| article, blog, write content | `content-research-writer` |
| schedule, recurring, every X minutes | `loop` (skill), scheduled tasks |
| PowerPoint, slides, deck, presentation | `anthropic-skills:pptx` |
| PDF, fill form, merge PDF | `anthropic-skills:pdf` |
| Word, docx, document | `anthropic-skills:docx` |
| spreadsheet, xlsx, csv, Excel | `anthropic-skills:xlsx` |

## What "Using a Skill" Means

Different skills are used differently:

1. **User-invocable skills** (like `fix-loop`, `deploy`, `backtest`): Call with the Skill tool
2. **Always-on passive skills** (like `zero-iteration`, `anti-slop`): Follow their checklist mentally
3. **Triggered skills** (like `website-guardian`, `error-memory`): Activate when their trigger conditions match
4. **Heavy skills with agents** (like `frontend-design`, `qa-gate`): Spawn subagents as the skill directs

**The key insight:** User-invocable skills MUST be actively called. They don't fire automatically. If `frontend-design` matches the task, you must either:
- Invoke it via the Skill tool if it's a slash command
- Follow its protocol manually if it's a behavioral skill
- Spawn an agent briefed with its instructions

## Failure Modes This Prevents

| Failure | What Happens Without This Skill |
|---------|-------------------------------|
| **Skill blindness** | Claude has `frontend-design` but designs frontends from scratch |
| **Reinventing the wheel** | Claude writes custom deploy scripts when `deploy` skill exists |
| **Missing quality gates** | Claude skips verification when `website-guardian` should fire |
| **Manual research** | Claude guesses domain logic when `know-what-you-dont-know` would force research |
| **No memory** | Claude doesn't log bugs when `error-memory` should capture them |
| **Brute force debugging** | Claude retries randomly when `systematic-debugging` has a protocol |

## When Multiple Skills Match

If 2+ skills match the task:
1. Use ALL of them — they're designed to complement each other
2. Start with the most specific one (e.g., `site-update-protocol` before generic `website-guardian`)
3. Let the skill-manager handle weight limits if too many are heavy

## Blocked Excuses (You May NOT Use These to Skip Skills)

Claude has a pattern of acknowledging skills then rationalizing why it didn't use them. These rationalizations are explicitly BLOCKED:

| Excuse | Why It's Wrong | What To Do Instead |
|--------|---------------|-------------------|
| "I applied its principles without formally invoking it" | Mentally applying ≠ using. The skill has specific checklists, scripts, and protocols that mental application skips. | Read the SKILL.md, follow each step. |
| "The fixes were minor CSS/JSX changes" | Minor changes still benefit from `frontend-design` anti-slop guidelines and `ui-ux-pro-max` accessibility checks. | Run the skill's checklist even for small changes. |
| "No test suite exists in the project" | `webapp-testing` uses Playwright — it creates its own tests. `qa-gate` can verify via curl, browser, or preview. | Use the skill's tools, don't require project tests. |
| "The Explore agent handled the research" | Explore reads files. Skills provide expert judgment, checklists, and quality gates that Explore doesn't have. | Use Explore for reading, THEN apply skill protocols to the findings. |
| "Those skills are more relevant for interactive debugging" | If the hook matched them, they're relevant NOW. | Use them now. |
| "I verified manually via curl/build" | Manual verification is not a substitute for skill-driven verification with checklists. | Use the skill's verification protocol, then ALSO do manual checks. |
| "It would add overhead for a simple task" | The user installed these skills specifically to avoid the bugs that "simple" tasks keep causing. Overhead is the point. | Use the skill. The overhead prevents regressions. |

**The rule:** If a skill was matched by the hook, you must either USE it or explain BEFORE starting work why it genuinely doesn't apply (not after you've already done the work without it).

## Self-Check (Run Mentally on Every Response)

Before submitting your response:
```
[ ] Did I check the skills list for this task?
[ ] If a skill matched, did I use it?
[ ] If I wrote code manually that a skill covers, why didn't I use the skill?
[ ] Am I about to claim "done" without running verification skills?
[ ] Am I about to rationalize not using a skill? (Check the blocked excuses table)
```

If you catch yourself NOT using a matching skill, stop and use it. The user installed these skills for a reason.
