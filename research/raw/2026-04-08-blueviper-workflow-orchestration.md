# Workflow Orchestration Rules (blueviper.ai)
**Source:** blueviper.ai Instagram post
**Date captured:** 2026-04-08
**Tags:** workflow, claude-code, productivity

## Content
6 rules for Claude Code workflow:
1. Plan mode for 3+ step tasks (write detailed specs)
2. Subagent strategy — offload to subagents, 1 task each
3. Self-improvement loop — update tasks/lessons.md after corrections
4. Verification before done — diff behavior, run tests, "would a staff engineer approve?"
5. Demand elegance — "is there a more elegant way?" for non-trivial changes
6. Autonomous bug fixing — point at logs/errors, don't ask for hand-holding

Task management: Plan first → verify → track → explain → document → capture lessons.

## Relevance
Evaluated 2026-04-08 — all 6 rules already covered by our hooks and skills (plan-mode-enforcer, agent-limit, correction-detector, verification-before-completion, simplify, systematic-debugging). Our implementations are stricter (hooks enforce mechanically vs. CLAUDE.md rules). No changes adopted.
