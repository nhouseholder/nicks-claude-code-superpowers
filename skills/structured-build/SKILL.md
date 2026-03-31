---
name: structured-build
description: Mandatory pipeline for new features and complex tasks. Enforces Research → Strategize → Plan → Execute → Self-Check → Verify → Deploy with gates between each phase. Prevents the #1 failure mode: jumping to code without understanding the problem.
weight: light
triggers:
  - new feature requests
  - complex multi-file tasks
  - tasks touching 3+ files or 2+ subsystems
  - "build me", "add feature", "implement", "new page", "new system"
  - routed via improve-prompt.py builder profile
---

# Structured Build — The Full Pipeline

Every new feature or complex task follows this pipeline. No skipping phases. Each phase has a gate that must pass before the next phase starts.

## When This Fires

- New feature development
- Complex tasks (3+ files, 2+ subsystems, or ambiguous requirements)
- Any task where jumping straight to code would be a mistake

**Does NOT fire for:** Quick fixes, config changes, simple edits, single-file changes with clear instructions.

## Complexity Check (5 seconds)

Before entering the pipeline, ask:

| Signal | Simple (skip pipeline) | Complex (use pipeline) |
|--------|----------------------|----------------------|
| Files touched | 1-2 | 3+ |
| Requirements clarity | Exact instructions given | Ambiguous or multi-part |
| Domain knowledge needed | Standard patterns | Domain-specific rules |
| Risk of breaking existing | Low | Medium-High |
| Subsystems involved | 1 | 2+ |

**2+ "Complex" signals → enter the pipeline.** Otherwise, just do the work.

---

## Phase 1: RESEARCH (Don't assume — investigate)

**Purpose:** Understand the problem space, existing code, constraints, and domain rules BEFORE forming an opinion on how to solve it.

### Actions
1. **Read the target area** — Every file you'll touch. Read them now, not during execution.
2. **Check anti-patterns.md** — Has this been tried before? Did it fail?
3. **Check memory** — Is there domain knowledge, user preferences, or prior decisions relevant to this task?
4. **Check specs** — Does a spec file exist for this domain? Read it.
5. **Domain research** (if needed) — Fire `know-what-you-dont-know` checklist. If domain-specific logic is involved, research from authoritative sources BEFORE proceeding.
6. **Map dependencies** — What calls what? What breaks if you change X?

### Research Output (mental, not written)
- What exists today
- What the user actually wants (not what you assumed)
- What constraints exist (technical, domain, user preference)
- What has failed before in this area

### Gate 1: Research Complete
- [ ] I have read every file I plan to touch
- [ ] I checked anti-patterns.md for relevant failures
- [ ] I understand the domain rules (not guessing)
- [ ] I know what depends on the code I'm changing

**If any checkbox fails → stay in Phase 1.**

---

## Phase 2: STRATEGIZE (Pick the right approach)

**Purpose:** Consider multiple approaches and pick the best one BEFORE committing to a plan. This is where you avoid the "first idea = only idea" trap.

### Actions
1. **Generate 2-3 approaches** — Don't go with the first thing that comes to mind.
   - Approach A: The obvious/simple way
   - Approach B: An alternative that trades off differently
   - Approach C: (if applicable) A creative or unconventional option
2. **Evaluate each against:**
   - Simplicity (fewer moving parts wins)
   - Risk (what could go wrong?)
   - Scope (does it stay within the task boundary?)
   - User's known preferences (from memory/feedback)
3. **Pick one.** State why in 1-2 sentences. If unsure, ask the user.

### Strategy Output
Brief statement to user:
> "I'll approach this by [approach]. Rationale: [why this over alternatives]."

For complex tasks, present options and let the user choose.

### Gate 2: Strategy Locked
- [ ] I considered at least 2 approaches
- [ ] I picked the simplest viable option
- [ ] The approach stays within task scope (surgical-scope check)
- [ ] I've communicated the approach to the user (or it's obvious enough to proceed)

**If any checkbox fails → stay in Phase 2.**

---

## Phase 3: PLAN (Map the work before doing it)

**Purpose:** Break the work into ordered steps so execution is mechanical, not creative.

### Actions
1. **List files to create/modify** — exact paths
2. **Order the steps** — dependencies first, UI last
3. **Identify test points** — where can you verify partial progress?
4. **Set commit boundaries** — what gets committed together?

### Plan Depth (match to rigor level from writing-plans)
| Task Type | Plan Depth |
|-----------|-----------|
| Site update | Mental plan, no doc needed |
| New feature | Brief written plan (bullet list with file paths) |
| New system/build | Full plan doc via `writing-plans` skill |
| Algorithm/model | Full plan + hypothesis + validation criteria |

### Gate 3: Plan Ready
- [ ] I know every file I'll touch and in what order
- [ ] Each step is small enough to verify independently
- [ ] Commit boundaries are defined

**If any checkbox fails → stay in Phase 3.**

---

## Phase 4: EXECUTE (Build it)

**Purpose:** Write the code. Follow the plan. Don't improvise.

### Rules During Execution
- **Follow the plan order.** If you need to deviate, pause and update the plan first.
- **One step at a time.** Don't batch 3 changes then test — change, verify, move on.
- **Commit at boundaries.** Don't accumulate uncommitted work across multiple steps.
- **Stay in scope.** If you notice something else that "should" be fixed — note it, don't fix it now.
- **Use zero-iteration.** Trace code mentally before writing. Catch bugs before they exist.

### Gate 4: Execution Complete
- [ ] All planned steps are done
- [ ] No unplanned changes were made (or deviations were justified and noted)
- [ ] Code is committed

**If any checkbox fails → finish execution before proceeding.**

---

## Phase 5: SELF-CHECK (Challenge your own work)

**Purpose:** Before asking anyone else to verify, verify yourself. Catch your own mistakes.

### The Self-Check Protocol
1. **Re-read every file you changed.** Not a skim — actually read the diff.
2. **Trace the happy path** — Does the main flow work end-to-end?
3. **Trace the error path** — What happens when input is bad, API fails, data is empty?
4. **Run the anti-rationalization check** (from zero-iteration):
   - "Did I actually verify, or am I rationalizing?"
   - "Am I claiming completion because it SHOULD work, or because I CHECKED?"
   - "Would I bet money on this?"
5. **Check for scope creep** — Did you change anything outside the task?
6. **Check for regressions** — Does existing functionality still work?

### Gate 5: Self-Check Passed
- [ ] I re-read every changed file
- [ ] Happy path traces correctly
- [ ] Error path is handled (or explicitly out of scope)
- [ ] No scope creep
- [ ] No regressions introduced

**If any checkbox fails → fix it, then re-check.**

---

## Phase 6: VERIFY (Prove it works)

**Purpose:** External verification — tests, browser, build, whatever proves correctness beyond your own review.

### Verification Actions (pick what applies)
- **Run tests** — If tests exist, run them. All of them, not just the new ones.
- **Build check** — Does the project build without errors/warnings?
- **Browser check** — If it's a UI change, look at it in a real browser (Claude Preview or Claude in Chrome).
- **Data check** — If it produces data, verify the output against known-good values.
- **Manual trace** — If no automated tests, walk through the feature manually.

### Gate 6: Verified
- [ ] Appropriate verification method was used (not just "looks right")
- [ ] All tests pass
- [ ] Build succeeds (if applicable)
- [ ] Visual verification done (if UI change)

**If any checkbox fails → fix and re-verify.**

---

## Phase 7: DEPLOY (Ship it)

**Purpose:** Get the verified work live and confirm it's working in production.

### Actions
1. **Final commit + push** — Everything committed, everything pushed to GitHub
2. **Deploy** — Follow the project's deploy process (Cloudflare Pages, etc.)
3. **Post-deploy verify** — Follow tiered verification from website-guardian:
   - LOW (data-only): Spot-check one data point
   - MEDIUM (feature): Check the new feature works
   - HIGH (redesign/critical): Full page verification
4. **Post-change report** — Mandatory DONE/Git/Deploy/Version status

### Gate 7: Shipped
- [ ] Committed and pushed
- [ ] Deployed (or N/A if not a website)
- [ ] Post-deploy verification passed
- [ ] Post-change report delivered

---

## Phase Shortcuts

Not every task needs all 7 phases. Use judgment:

| Task | Start At | Skip |
|------|----------|------|
| Simple feature, clear spec | Phase 3 (Plan) | Research + Strategize (already clear) |
| Bug fix in known area | Phase 1 (Research) | Strategize (fix is the fix) |
| New system, unfamiliar domain | Phase 1 (Research) | Nothing — full pipeline |
| UI tweak, user showed screenshot | Phase 4 (Execute) | Research/Strategize/Plan (obvious) |

**When in doubt, start at Phase 1.** The cost of 2 minutes of research is always less than the cost of 20 minutes of rework.

## Rules

1. **Never skip Research for complex tasks** — the #1 source of rework
2. **Strategize is where bad approaches die** — kill them here, not in code review
3. **Self-Check is mandatory** — you are your own first reviewer
4. **Gates are real** — if a gate fails, stay in that phase
5. **Communicate phase transitions** — the user should know where you are in the pipeline
6. **The pipeline is a safety net, not a cage** — use Phase Shortcuts when appropriate
