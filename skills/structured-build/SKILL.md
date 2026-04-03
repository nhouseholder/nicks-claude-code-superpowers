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

## Triage (5 seconds — before anything else)

Classify the task. This determines which phases you enter and how deep research goes.

### Step 1: Do I need to research at all?

| Ask yourself | YES → Research | NO → Skip research |
|---|---|---|
| Am I touching code I haven't read this session? | Read it first | Already read it |
| Does this involve domain-specific rules (betting, finance, medicine, legal)? | Fire `know-what-you-dont-know` | Standard programming patterns |
| Has this area failed before? (anti-patterns.md) | Check what failed and why | No prior failures logged |
| Are the requirements ambiguous or multi-part? | Clarify before building | User gave exact instructions |
| Am I about to change something with downstream dependents I don't fully understand? | Map the dependencies | I know the call graph |

**Any YES → enter Research phase.** All NO → skip to Strategize or Plan.

### Step 2: How deep does research need to go?

| Research Depth | When | What to do |
|---|---|---|
| **None** | Clear instructions, familiar code, standard patterns, single-file change | Skip to Phase 3 (Plan) or Phase 4 (Execute) |
| **Quick scan** (30 sec) | Touching 2-3 files, known codebase, minor uncertainty | Read target files + quick anti-patterns check. That's it. |
| **Targeted research** (2-3 min) | New area of codebase, unfamiliar API, user preference unknown | Read files + check memory + check specs + map dependencies |
| **Deep research** (5+ min) | Domain logic, unfamiliar technology, system design, high-risk change | Full Phase 1 protocol + `know-what-you-dont-know` + external sources |

**Match research depth to actual uncertainty.** Over-researching a CSS tweak wastes tokens. Under-researching a payment integration causes production bugs. The skill is knowing which is which.

### Step 3: Which phases do I need?

| Task Type | Phases | Why |
|---|---|---|
| **Exact instructions, familiar code** (e.g., "change button color to blue") | Execute → Self-Check | Nothing to research or plan — just do it and verify |
| **Clear feature, known codebase** (e.g., "add a loading spinner to the dashboard") | Plan → Execute → Self-Check → Verify | Know what to build, just need to map the steps |
| **Ambiguous feature or multi-step** (e.g., "add user notifications") | Strategize → Plan → Execute → Self-Check → Verify | Need to pick an approach before planning |
| **Unfamiliar code or area** (e.g., "add feature to a repo you just opened") | Research → Plan → Execute → Self-Check → Verify | Need to understand what exists before deciding anything |
| **Domain-specific or high-risk** (e.g., "new betting settlement logic") | Research → Strategize → Plan → Execute → Self-Check → Verify → Deploy | Full pipeline — can't afford to get this wrong |
| **New system from scratch** | Research → Strategize → Plan → Execute → Self-Check → Verify → Deploy | Full pipeline |
| **Experiment / A-B test** (e.g., "test if feature X improves results") | Research → Experiment Plan → Execute → Validate Results | Scientific method — NOT a build. See Experiment Protocol below. |

**The default is NOT "full pipeline." The default is "whatever this task actually needs."**

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

## Experiment Protocol (for A/B tests, coefficient sweeps, feature evaluation)

**When this fires:** Any task where you're testing whether a change improves measurable results. This is NOT a build — it's a scientific experiment. Different mental model, different gates.

### Step 1: Write the Experiment Card (BEFORE any code or commands)

State these 4 things in plain text to the user before touching anything:

```
EXPERIMENT: [what you're testing]
HYPOTHESIS: [why you expect it to work, in domain terms]
BASELINE: [exact command + expected output to establish the control]
VARIANT: [exact command — must differ from baseline by ONE variable only]
```

**Gate: If you can't fill all 4 fields, you don't understand the experiment yet. Research more.**

### Step 2: Establish the Baseline (run it, record the numbers)

Run the baseline command. Record:
- Event count (e.g., 70+ events, 354W-133L)
- Pipeline steps executed (every script that ran)
- Key metrics (units, W/L, accuracy)

**Gate: If event count is suspiciously low (<50 events for UFC), STOP. Check for FAST_MODE, limited date range, or missing data.**

### Step 3: Run the Variant (IDENTICAL pipeline, ONE variable changed)

The variant must use:
- Same scripts in same order as baseline
- Same data, same date range, same mode flags
- ONE thing different: the feature under test

**Gate: Before comparing results, verify event counts match. If they don't, the comparison is invalid — find the pipeline difference first.**

### Step 4: Validate the Delta

Before claiming any improvement:
1. **Do the numbers add up?** W/L counts should be close. Large divergences = pipeline mismatch.
2. **Is the effect real?** Test 2-3 coefficient values. If all produce identical results, the feature has no effect — report null immediately, don't keep testing.
3. **Is the attribution correct?** Could the delta come from a different change (e.g., a script that ran in one pipeline but not the other)?

**Gate: Only claim an improvement if you can point to specific picks that flipped AND explain WHY the feature caused those flips.**

### Experiment Anti-Patterns (stop immediately if you catch yourself doing these)

- Running a "quick test" with FAST_MODE or limited events, then scaling up — just run full from the start
- Comparing numbers from runs with different pipeline steps
- Celebrating a delta without checking if coefficient variations produce different results
- Running 4+ sweeps without a written hypothesis for each one

---

## Rules

1. **Triage first** — the Triage section determines which phases you enter. Don't run full pipeline on simple tasks. Don't skip research on complex ones.
2. **Research depth matches uncertainty** — over-researching wastes tokens, under-researching causes bugs. Match depth to actual unknowns.
3. **Strategize is where bad approaches die** — kill them here, not in code review
4. **Self-Check is ALWAYS mandatory** — even for simple tasks, re-read your diff before declaring done
5. **Gates are real** — if a gate fails, stay in that phase
6. **Don't announce phases** — the user doesn't need "Entering Phase 3: Plan." Just do the work. Only surface phase transitions when asking the user to make a decision (strategy choice, plan approval).
7. **The pipeline is a safety net, not a cage** — it exists to prevent jumping to code without thinking. If thinking takes 5 seconds because the task is obvious, that's fine.
