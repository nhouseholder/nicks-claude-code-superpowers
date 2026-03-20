---
name: reflexion:reflect
description: Reflect on previous response and output, based on Self-refinement framework for iterative improvement with complexity triage and verification
argument-hint: Optional focus area or confidence threshold to use, for example "security" or "deep reflect if less than 90% confidence"
---

# Self-Refinement Framework

Reflect on previous response and output.

You are a **thorough quality reviewer** — catch real issues before they ship. Acknowledge good work, flag genuine problems, provide actionable feedback.

## WHEN TO FIRE

**This skill is opt-in by default.** Do NOT auto-fire on every response.

Fire ONLY when:
- User explicitly asks for review/reflection ("review this", "check my work", "is this right?")
- Verification-before-completion triggers on a high-risk change (deploy, data migration, auth changes)
- A bug fix failed 2+ times (escalation from qa-gate)

Do NOT fire when:
- Simple task completed successfully (single file edit, config change, etc.)
- The work is clearly correct from the implementation itself
- Another heavy skill (qa-gate, deep-research) already validated the work

**If in doubt, don't fire.** The user will ask if they want reflection.

## TASK COMPLEXITY TRIAGE

Two paths only:

### Quick Path (default)
For all standard work — verify output is correct, complete, and matches the request. Skip to "Final Verification" section.

### Deep Path (opt-in)
For high-risk changes (auth, payments, data migrations), explicit user request, or after 2+ failed bug fixes. Follow complete framework below.

## DEEP PATH: REFLECTION PROTOCOL

### Step 1: Initial Assessment

Evaluate your most recent output:

- [ ] **Completeness**: Fully addresses request? All explicit and implicit requirements covered?
- [ ] **Quality**: Appropriate complexity? Could be simplified? Obvious improvements?
- [ ] **Correctness**: Logically sound? Edge cases considered? Unintended side effects?
- [ ] **Dependencies**: Checked for dependencies on changed items? Searched for superseding decisions? Verified nothing depends on removed items?
- [ ] **Facts**: Performance claims, technical facts, and security assertions verified before stating them?
- [ ] **Generated Artifacts**: Cross-references validated? Scanned for sensitive info (paths, credentials)? Documentation referencing changed values updated? State claims verified with actual commands?

**HARD RULE:** If any check reveals active dependencies, evaluations, or pending decisions — FLAG IT. Do not approve work that skips dependency verification.

### Step 2: Decision Point

**REFINEMENT NEEDED?** [YES/NO]

If YES, proceed to Step 3. If NO, skip to Final Verification.

### Step 3: Refinement Plan

1. **List specific issues found** with descriptions
2. **Propose solutions** for each issue
3. **Prioritize**: Critical fixes > Performance > Style/readability

## REFINEMENT TRIGGERS

Auto-trigger refinement when:
- **Complexity**: Cyclomatic complexity >10, nesting >3 levels, function >50 lines
- **Code smells**: Duplicate code, long parameter lists (>4), god classes, magic numbers
- **Missing elements**: No error handling, no input validation, no tests for critical paths
- **Dependency gaps**: Deletion without dependency check, config changes without checking authoritative docs, generated cross-references not validated, files containing absolute paths/usernames
- **Unverified claims**: Declared complete without running verification commands

## FINAL VERIFICATION

Before finalizing any output:

- [ ] Verified assumptions and considered at least one alternative approach?
- [ ] This is the simplest correct solution another developer would understand?
- [ ] All factual/performance/security claims verified or sourced?
- [ ] Tool/API/file references verified against actual inventory (not assumed)?
- [ ] Generated files scanned for sensitive info (paths, usernames, credentials)?
- [ ] All docs referencing changed values updated?
- [ ] Claims verified with actual commands, not memory?
- [ ] For additions/deletions/modifications, verified no active dependencies or superseding decisions?

## CONFIDENCE & REPORTING

Report should contain: summary of what was reviewed, issues found (with severity), specific fixes applied or recommended, final confidence level, and remaining risks.

Score objectively based on evidence. Most competent work is 3-4 out of 5. Be honest — flag problems clearly regardless of tone or effort invested.

If confidence is below threshold for the task's complexity tier, iterate again.
