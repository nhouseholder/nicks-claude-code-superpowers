---
name: reflexion
description: Self-refinement and comprehensive review framework. Two modes — /reflexion:reflect for quick self-assessment of output quality (checklist + confidence score), and /reflexion:critique for deep multi-dimensional review (requirements + design + code quality via reviewer agent). Opt-in only — fires on explicit user request, high-risk changes, or after 2+ failed bug fixes.
weight: heavy
argument-hint: "reflect" for self-assessment, "critique" for deep review, or specific files/commits
---

# Reflexion — Self-Refinement & Comprehensive Review

Two modes for two needs:
- **Reflect** — Quick self-assessment: "Is my output correct and complete?"
- **Critique** — Deep review: "Does this meet requirements, is the design sound, is the code quality good?"

## When to Fire

**Opt-in only.** Do NOT auto-fire on every response.

Fire when:
- User explicitly asks ("review this", "check my work", "reflect", "critique")
- High-risk change (deploy, data migration, auth) via verification-before-completion
- Bug fix failed 2+ times (escalation)

Skip only when: the task is a single config/text change with no logic, OR another heavy skill just verified the exact same output. 'Simple' is not a valid skip reason — simple tasks are where bugs hide.

## Mode 1: Reflect (Self-Assessment)

### Quick Path (default)
Verify output is correct, complete, matches request. Run Final Verification checklist below.

### Deep Path (explicit request or high-risk)

**Initial Assessment:**
- [ ] **Completeness**: All explicit and implicit requirements covered?
- [ ] **Quality**: Appropriate complexity? Could be simplified?
- [ ] **Correctness**: Edge cases? Unintended side effects?
- [ ] **Dependencies**: Checked for dependencies on changed items?
- [ ] **Facts**: Performance/security claims verified?
- [ ] **Artifacts**: Cross-references valid? No leaked credentials/paths?

If issues found → list them, propose fixes, prioritize (critical > performance > style).

**Refinement triggers** (auto-escalate to deep path):
- Cyclomatic complexity >10, nesting >3, function >50 lines
- Duplicate code, >4 parameters, magic numbers
- No error handling or input validation on critical paths
- Deletion without dependency check

### Final Verification (both paths)

- [ ] Verified assumptions and considered alternatives?
- [ ] Simplest correct solution another dev would understand?
- [ ] All claims verified with commands, not memory?
- [ ] Generated files scanned for sensitive info?
- [ ] Docs referencing changed values updated?
- [ ] No active dependencies or superseding decisions?

**Report**: Summary, issues found (with severity), fixes applied/recommended, confidence score (1-5), remaining risks.

## Mode 2: Critique (Comprehensive Review)

### Phase 1: Context Gathering

1. Identify scope (arguments, recent changes, or ask user)
2. Capture: original requirements, files modified, decisions made, constraints
3. Summarize scope before proceeding

### Phase 2: Comprehensive Review Agent

Spawn ONE reviewer agent (via Agent tool) covering three dimensions:

**Requirements Check:**
- List all requirements, check each against implementation
- Identify gaps, over-delivery, misalignments

**Design Assessment:**
- Evaluate approach and trade-offs
- Note if significantly better alternative exists
- Check architectural consistency

**Code Quality Scan:**
- Readability, naming, structure
- Code smells, duplication, complexity
- Error handling and edge cases

**Self-Verification:**
- Generate 3-5 verification questions, answer honestly, adjust findings

### Phase 3: Report

```
### Overall Score: X/10

### Requirements: ✅ Met | ⚠️ Partial | ❌ Missed

### Design: Strengths, concerns, better alternatives (if any)

### Code Quality: Issues by severity with file:line locations

### Action Items:
- Must Do: [critical]
- Should Do: [high priority]
- Could Do: [nice to have]

### Verdict: ✅ Ship | ⚠️ Improve | ❌ Rework
```

## Rules

1. **Opt-in only** — never auto-fire on routine work
2. **Be objective** — base on evidence, not preferences
3. **Be specific** — cite file locations and code examples
4. **Score honestly** — most competent work is 3-4/5; don't inflate
5. **Critique is report-only** — presents findings, doesn't make changes
