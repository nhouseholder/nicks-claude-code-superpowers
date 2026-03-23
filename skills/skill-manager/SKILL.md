---
name: skill-manager
description: Prevents skill overload. Weight class limits, conflict resolution, stack cap at 75. Always-on meta-skill.
---

# Skill Manager — Traffic Control

## Weight Limits (Hard)

| Weight | Max/Message | Skills |
|--------|-------------|--------|
| Passive (~0 tokens) | Unlimited | Behavioral shaping only |
| Light (50-500 tokens) | 5 | Quick checks, small reads |
| Heavy (1K-50K+ tokens) | 2 | Agent spawns, multi-file ops |

**Stack cap: 75 skills maximum.** Adding past 75 requires merge or removal.

## Conflict Resolution Priority

1. User's explicit instruction
2. Feedback memories (prior corrections)
3. Domain-specific skills (in their domain)
4. Safety/verification skills
5. Process skills (workflow)
6. Enhancement skills (lowest — suppress if busy)

**Key tiebreaker:** Safety beats speed. Specific beats general. Current task beats improvement. Action beats analysis.

## Skill Overload Test

Before executing: is this response shaped by understanding of the task, or by a stack of checklists? If it feels robotic/checklist-y, fewer skills should be active.

| Message Type | Max Active Skills |
|-------------|-------------------|
| Simple (<20 words) | 0-2 |
| Moderate (single task) | 3-5 |
| Complex (multi-part) | 5-8 |

**Golden rule:** Skills enhance Claude's natural intelligence, not replace it. If ignoring a skill produces a better answer, ignore it.
