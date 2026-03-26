# Skills Reference — Nick's Claude Code Superpowers

> Complete documentation for all 69 skills, 4 hooks, 9 commands, and the continuous learning system.
> Last updated: 2026-03-19

---

## Table of Contents

- [How Skills Work](#how-skills-work)
- [Skill Trigger Types](#skill-trigger-types)
- [Workflow Map](#workflow-map)
- [Skills by Category](#skills-by-category)
  - [Foundation (Always Active)](#foundation-always-active)
  - [Autonomy & Completeness](#autonomy--completeness)
  - [Thinking & Reasoning](#thinking--reasoning)
  - [Code Intelligence](#code-intelligence)
  - [Communication & UX](#communication--ux)
  - [Git Intelligence](#git-intelligence)
  - [Infrastructure Awareness](#infrastructure-awareness)
  - [Domain Expertise](#domain-expertise)
  - [Memory & Learning](#memory--learning)
  - [Code Quality & Testing](#code-quality--testing)
  - [Planning & Execution](#planning--execution)
  - [Agent Orchestration](#agent-orchestration)
  - [Research & Context](#research--context)
  - [Review & Collaboration](#review--collaboration)
  - [Meta Skills](#meta-skills)
- [Hooks](#hooks)
- [Commands](#commands)
- [Continuous Learning System](#continuous-learning-system)

---

## How Skills Work

Skills are markdown files in `~/.claude/skills/` that Claude Code loads into context when relevant. Each skill has:

- **SKILL.md** — Instructions that guide Claude's behavior
- **Frontmatter** — Name, description, trigger conditions, allowed tools
- **Context mode** — `fork` (runs as subagent) or inline (runs in main conversation)

Skills fire based on description matching against the current task. Some are always-on, some are manual (`/skill-name`), and some auto-trigger on specific conditions.

## Skill Trigger Types

| Type | When It Fires | Examples |
|------|--------------|---------|
| **Always-on** | Every conversation, every response | coding-standards, token-awareness, context-hydration |
| **Automatic** | When conditions match (errors, completion, etc.) | pre-debug-check, verification-before-completion, strategic-compact |
| **Hook-driven** | Via shell hooks on specific events | continuous-learning-v2, prompt-improver |
| **Manual** | User invokes with `/skill-name` or task matches description | brainstorming, writing-plans, reflexion-reflect |

## Workflow Map

```
User Request
    │
    ├─ prompt-architect (always-on: decompose intent → optimize execution)
    │
    ├─ Vague? ──→ prompt-improver (auto-enriches)
    │
    ├─ Creative? ──→ brainstorming ──→ writing-plans ──→ executing-plans
    │                                                        │
    │                                                        ├─ using-git-worktrees
    │                                                        ├─ subagent-driven-development
    │                                                        └─ finishing-a-development-branch
    │
    ├─ Bug/Error? ──→ barrier-recognition ──→ pre-debug-check ──→ systematic-debugging
    │                  (known pattern?)         (check anti-patterns)   (root cause first)
    │                                                                        │
    │                                                                        └─ error-memory (save fix)
    │
    ├─ Implementation? ──→ search-first ──→ test-driven-development
    │                      (existing solution?)   (RED → GREEN → REFACTOR)
    │
    └─ Done? ──→ verification-before-completion ──→ requesting-code-review
                  (evidence before claims)           (subagent review)
```

---

## Skills by Category

---

### Foundation (Always Active)

These skills shape every interaction. They don't need to be invoked.

#### `coding-standards`
**What it does:** Establishes universal coding conventions — KISS, DRY, YAGNI, naming rules, immutability patterns, error handling, async/await, React best practices, API design, and testing standards.

**How to use:** Always active. Reference it when:
- Starting a new project (establishes conventions)
- Reviewing code quality
- Naming variables/functions (verb-noun for functions, descriptive for variables)

**Key rules:**
- Functions: `calculateTotal()`, `fetchUserData()` (verb + noun)
- Variables: descriptive, no abbreviations
- Prefer immutability (spread operator, `.map()` over mutation)
- Always handle errors explicitly
- Never ignore Promise rejections

---

#### `token-awareness`
**What it does:** Promotes efficient, concise communication. Code over explanation. Lazy-load files. Parallelize tool calls. Compact output.

**How to use:** Always active. Shapes response style:
- Short answers by default
- Code snippets instead of paragraphs
- Only read files when needed (lazy loading)
- Run independent tool calls in parallel
- Expand only when user is learning or explicitly asks

---

#### `context-hydration`
**What it does:** Enforces "read before edit" — never modify a file without reading it first. Checks related files, understands current implementation, and preserves dependencies.

**How to use:** Always active. Before any Edit/Write:
1. Read the target file
2. Read related/imported files
3. Understand current state
4. Then make changes

---

### Autonomy & Completeness

These skills make Claude operate like a senior developer who ships complete, production-ready code without hand-holding.

#### `senior-dev-mindset`
**What it does:** Bridges the gap between what the user *says* and what they *mean*. When told "add a login page," this skill ensures Claude builds the complete feature — form validation, error states, loading states, auth integration, redirect logic, mobile responsive, accessible — not just a bare form with a TODO comment.

**How to use:** Always active. Shapes every implementation by:
- **Inferring unstated requirements** from real-world app patterns (e-commerce, SaaS, social, etc.)
- **Enforcing completeness** — all states handled (empty, loading, error, success)
- **Banning placeholders** — no `// TODO`, no `console.log`, no stub functions, no lorem ipsum
- **Making independent decisions** — follows codebase patterns for styling, state management, file organization without asking permission
- **Connecting everything** — wired to real data, routes, and services

**Key rules:**
- When told "add X" → also connect, protect, style, test, and add navigation
- When told "fix X" → also find sibling bugs, fix root cause, prevent regression
- When told "update X" → also update consumers, types, tests, docs
- Never say "you'll need to add..." — just add it

**Completeness checklist (automatic):**
- Frontend: all states, validation, loading, error handling, responsive, accessible, edge cases
- Backend: validation, error codes, auth checks, efficient queries
- Integration: real data flowing, auth handled, routes working, data persisting

---

#### `proactive-qa`
**What it does:** After every implementation, mentally walks through the feature as different users (new, returning, error-prone, mobile, impatient) and fixes what it finds. Detects architectural smells, anticipates scaling issues, and fixes adjacent bugs.

**How to use:** Always active. After writing any code, runs this loop:
1. **Walk the user journey** — Would a real user get stuck anywhere?
2. **Check blast radius** — What else did this change affect?
3. **Hunt edge cases** — Empty strings, null values, timeout, offline, concurrent access
4. **Anticipate next problems** — "This list will grow. Does it paginate?"

**Proactive fixes (do without asking):**
- Missing loading/error/empty states
- Unhandled promise rejections
- Memory leaks (uncleared intervals, unsubscribed listeners)
- Race conditions (stale closures, request ordering)
- Broken navigation (dead links, orphaned pages)
- Accessibility issues noticed in passing
- Inconsistent styling that's clearly a bug

**Architecture smell detection:**
- God components (300+ lines) → extract sub-components
- Prop drilling (3+ levels) → use context
- Duplicated logic (3+ places) → extract utility
- Mixed concerns (API in render) → separate into service

**The "Ship It" test:** Before declaring done, imagine screen-sharing with the user. Would you feel confident clicking through? If not — fix it first.

**Independence protocol:**
- Established codebase pattern exists → Follow it (don't ask)
- Common software pattern → Apply it (don't ask)
- Choice is reversible → Make judgment, mention it
- Choice is irreversible → Ask the user

---

#### `sanity-check`
**Trigger:** Automatic — fires when a request could break things, waste significant effort, or introduce problems

**What it does:** Before blindly executing a risky or wasteful request, pauses to respectfully flag the concern and recommend a better approach. Saves tokens and prevents regressions by catching bad ideas before work begins.

**Format:** Always three parts:
1. Specific concern (one sentence)
2. Better alternative (if one exists)
3. The choice — user always decides

**Severity levels:**
- **Green** — Mild concern: do it anyway, mention alternative in one line
- **Yellow** — Moderate risk: flag before proceeding, ask which approach
- **Red** — High risk: clear warning, recommend against, still let them decide
- **Hard stop** — Destructive/irreversible: explicit warning, won't proceed without confirmation

**Key rules:** 95/5 ratio (vast majority of requests execute immediately). Flag once, then respect the decision. Always offer an alternative, not just criticism. Be specific, not vague. Consider you might be wrong.

**Boundary with `proactive-qa`:** QA catches issues in implementation. Sanity-check catches issues in the REQUEST before work begins.

---

#### `brainstorming`
**Trigger:** Manual — must invoke before any creative work (features, components, UI changes)

**What it does:** Guides collaborative design dialogue before implementation. Explores user intent through natural questioning, proposes approaches, creates design document, then hands off to `writing-plans`.

**How to use:**
```
/brainstorm I want to add a dark mode toggle
```

**Workflow:**
1. Explore context and constraints
2. Ask clarifying questions (not a quiz — natural conversation)
3. Propose 2-3 approaches with tradeoffs
4. Present design for approval
5. Write design doc
6. Hand off to `/write-plan`

**Rule:** Design must be approved before any code is written.

---

#### `systematic-debugging`
**Trigger:** Manual — when encountering any bug, test failure, or unexpected behavior

**What it does:** Enforces 4-phase debugging methodology. NEVER proposes fixes without completing root cause investigation first.

**How to use:** Triggered automatically when errors are encountered, but comes AFTER `pre-debug-check`.

**Phases:**
1. **Root Cause Investigation** — Read errors, reproduce, check recent changes, gather evidence, trace data flow
2. **Pattern Analysis** — Find patterns, compare to known issues
3. **Hypothesis Testing** — Form hypothesis + minimal test
4. **Implementation** — Create test, write minimal fix, verify

**Iron Law:** If 3+ fixes fail → question the architecture, not just the hypothesis.

**Anti-patterns to avoid:**
- "Quick fix for now, investigate later"
- "Just try changing X and see"
- Proposing fixes before reading error messages

---

#### `fpf-hypotheses`
**Trigger:** Manual — for complex decisions requiring rigorous reasoning

**What it does:** First Principles Framework — generates competing hypotheses, validates with evidence, and produces a documented Decision Rationale Record (DRR).

**How to use:**
```
/fpf:propose-hypotheses Why is the app crashing on iOS Safari?
```

**Workflow:** Create FPF directory → Initialize context → Generate hypotheses → Verify logic → Validate evidence → Audit trust scores → Make decision → Output DRR

**Knowledge states:** L0 (accepted) → L1 (supported) → L2 (speculative)

---

---

### Code Intelligence

#### `zero-iteration`
**Trigger:** Always-on — fires during any code generation or modification

**What it does:** Mentally executes code before writing it. Traces inputs through logic with concrete values, predicts outputs, catches bugs before they exist. The fastest debugging is the debugging you never have to do.

**The mental execution protocol:**
1. **INPUTS** — What types/shapes come in? Edge cases?
2. **TRACE** — Step through line by line with concrete values
3. **OUTPUT** — Does the result match the caller's expectation?
4. **FAIL** — What makes this break? Null? Empty? Off-by-one?

**The three-value test (every function):**
1. Happy path — normal expected input
2. Empty/zero case — empty string, empty array, 0, null
3. Boundary case — max length, negative, special chars

**Common pre-bugs caught:** Data shape mismatches, off-by-one errors, async timing (missing await), type coercion traps, reference vs value, import/export mismatches.

**Token economics:** Zero cost when code is correct (mental execution). Only costs tokens when it catches a pre-bug — far cheaper than a debug cycle.

---

#### `pattern-propagation`
**Trigger:** Automatic — fires when modifying anything with multiple instances

**What it does:** When a pattern changes in one place, finds and updates ALL instances across the codebase. Covers renames, API shape changes, component prop changes, config/env changes, and file moves.

**The propagation protocol:**
1. **Detect scope** — Grep for the pattern, check exports, check conventions
2. **Collect all instances** — Exact matches, variations, indirect references, tests, docs
3. **Update systematically** — Source → consumers → indirect consumers → tests → docs → config
4. **Verify consistency** — Grep for OLD pattern should return zero results

**Rules:** Never leave partial updates. Ask before propagating across 10+ files. Include tests. Skip cosmetic propagation.

---

#### `opportunistic-improvement`
**Trigger:** Always-on — passive while working on any task, zero overhead when code is clean

**What it does:** While working on the primary task, notices code smells, inefficiencies, and obvious improvements in files already being read or edited. Fixes no-brainers silently, flags bigger opportunities, and reports all improvements at the end of the response.

**No-brainer test (all 4 must pass):**
1. Is the fix obviously correct?
2. Can it break anything?
3. Is it in a file I'm already touching?
4. Would ANY developer agree this is better?

**Fix silently:** Dead imports, unused variables, obvious bugs, naming clarity, consistency issues, security basics.

**Flag for permission:** Refactoring patterns, API changes, architecture shifts, logic changes.

**Report format:** End of response — "Improvements made: [list]. Also noticed: [flagged items]."

**Compounding effect:** Each session leaves the project cleaner. Session 5 has almost nothing to flag because sessions 1-4 already cleaned up what they touched.

**Token economics:** ~0 when code is clean. ~5-15 tokens average. Net negative over time — clean code means fewer bugs and debugging sessions.

---

#### `codebase-cartographer`
**Trigger:** Automatic — fires at session start

**What it does:** Builds a mental architecture map of the codebase. Knows directory purposes, data flows, conventions, and entry points. Enables instant navigation without redundant exploration.

**Three-tier mapping:**
- **Tier 1** (memory + git): ~100 tokens — check project memory, git status, package files, directory structure
- **Tier 2** (targeted reads): ~500-1000 tokens — config files, entry points, routes, schemas (on-demand for current task)
- **Tier 3** (deep exploration): ~3000-5000 tokens — full subsystem analysis (rare, only for complex multi-file tasks)

**What to map:** Directory purposes, data flow (user input → API → DB → response → UI), auth flow, state management, file naming conventions, testing patterns.

---

### Communication & UX

#### `adaptive-voice`
**Trigger:** Always-on — reads user energy every response

**What it does:** Matches the user's communication style. Terse when they're in flow, detailed when learning, calm when frustrated.

**Signal detection:**
| User State | Signals | Your Response |
|------------|---------|---------------|
| **Flow** | Short rapid messages, no pleasantries | Max brevity, code only, execute immediately |
| **Learning** | "why", "how does", "what's the difference" | Brief explanations WITH code |
| **Frustrated** | ALL CAPS, "!!!", "this still doesn't work" | Acknowledge briefly, try different approach, skip explanations |
| **Collaborative** | "what do you think?", sharing trade-offs | Engage with ideas, share reasoning |
| **Directive** | Specific instructions, bullet points | Execute exactly as specified, zero improvisation |

**Rules:** Never announce adaptation. Never be sycophantic. Mirror energy level, not exact style. Default to concise.

---

#### `predictive-next`
**Trigger:** Automatic — fires after completing any substantive task

**What it does:** Anticipates the most likely next request and offers it in one line. If right, saves a prompt. If wrong, easily ignored.

**Format:** Always a single line: `Next: want me to add tests for this component?`

**Common predictions:**
- After new code → "Want me to add tests?" / "Wire into router?"
- After bug fix → "Check for same pattern elsewhere?"
- After refactor → "Update all references?"
- After config change → "Run build to verify?"

**Rules:** One prediction, one line. Never list options. Never predict destructive actions. Suppress in flow state.

---

#### `always-improving`
**Trigger:** Automatic — fires when all tasks are complete and no urgent work remains

**What it does:** When the to-do list is empty and there are no glaring holes, proactively scans the project across 8 dimensions (performance, UX, code quality, architecture, security, testing, DX, features) and suggests the top 1-3 highest-impact improvements.

**How it suggests:**
- Brief, specific, actionable suggestions with effort estimates
- Prioritizes high-impact + low-effort quick wins first
- Adapts to user preferences (feature-focused? quality-focused? performance-focused?)
- Always asks before implementing — never takes action without approval

**Key rules:** Only at idle points — never interrupts active work. Suggestions must be grounded in actual code, not hypothetical. Respects declined suggestions (backs off). Top 1-3 only, never a laundry list.

**Boundary with `predictive-next`:** Predictive-next suggests the logical NEXT step after completing a task. Always-improving suggests ENHANCEMENTS when there IS no next step.

---

### Git Intelligence

#### `git-sorcery`
**Trigger:** Always-on — enhances all git operations

**What it does:** Advanced git intelligence: smart commit messages from diffs, conflict resolution strategies, bisect for bug hunting, cherry-pick workflows, branch management, stash operations.

**Smart commit formula:** `[Action] [What] — [Why/Impact]`
- Action: Fix, Add, Remove, Refactor, Optimize, Update, Migrate
- What: The specific thing that changed
- Why: The reason or impact

**Conflict resolution:** UNDERSTAND (read both sides) → INTENT (which is more important?) → RESOLVE (integrate both if possible) → VERIFY (does it make sense?)

**Bug hunting:** When "this used to work" → suggest bisect to binary-search for the introducing commit.

**Rules:** Intent over diff in messages. Atomic commits. Never force-push without asking. Descriptive stashes always.

---

### Infrastructure Awareness

#### `process-monitor`
**Trigger:** Automatic — fires when starting/encountering background processes, when something seems stuck, before session end

**What it does:** Maintains awareness of background processes (dev servers, builds, test runners). Detects port conflicts, hung processes, zombies, and resource issues. Reports problems, not status.

**Key behaviors:**
- **Before starting a server** → Check if port is already in use
- **When something fails** → Check if it's a process issue before checking code
- **When something hangs** → Detect no-output timeout (30s builds, 5s servers)
- **Before session end** → Mention running processes (don't auto-kill)

**Token economics:** Event-driven checks only. Zero overhead when everything is normal. Port check = ~50 tokens. Health check = ~100 tokens. No polling.

**Safe to kill:** Duplicate instances, completed builds, watchers no longer needed.
**Ask before killing:** Processes you didn't start, databases, servers serving other terminals.

---

### Domain Expertise

#### `expert-lens`
**Trigger:** Always-on — detects domain from explicit persona assignment ("you are an expert in X") or implicitly from task context

**What it does:** Activates professional-grade thinking for any domain. Not just "roleplay" — loads four concrete layers that produce expert-quality output.

**Four layers of expertise:**
1. **Mental Models** — Domain-specific frameworks (sports: WAR/regression to mean, design: visual hierarchy/Fitts's law, medicine: differential diagnosis, finance: DCF/risk-adjusted returns)
2. **Vocabulary Calibration** — Use precise domain terms that add clarity, define when needed
3. **Quality Standards** — Apply the domain's professional bar (statistician: never present a number without context; designer: never propose UI without considering full flow)
4. **Amateur-Mistake Avoidance** — Know what non-experts get wrong and proactively avoid it

**Activation modes:**
- **Explicit**: "You are an expert NBA statistician" → activates immediately
- **Implicit**: Task involves statistical analysis → auto-applies stats lens quietly

**Token economics:** ~30-50 tokens per activation. Expert framing often makes output SHORTER (experts are more direct). Net token impact is near-zero or negative.

**Key rules:** Frameworks over roleplay. Never fabricate credentials. Silent activation. Honest about knowledge limits.

---

### Memory & Learning

#### `continuous-learning-v2`
**Trigger:** Automatic — PreToolUse/PostToolUse hooks (100% reliability)

**What it does:** Advanced instinct-based learning system. Observes every tool call, creates atomic "instincts" with confidence scoring (0.3–0.9), and scopes them by project to prevent cross-contamination.

**How to use:** Runs automatically via hooks. Manage with commands:
- `/instinct-status` — Show current learned instincts
- `/evolve` — Cluster instincts into skills/commands
- `/instinct-export` / `/instinct-import` — Share instincts
- `/promote` — Move project-scoped instinct to global
- `/projects` — List all tracked projects

**Instinct lifecycle:** Observation → Instinct (confidence scored) → Cluster → Evolved skill/command/agent

**Storage:** `~/.claude/homunculus/` (global) and `~/.claude/homunculus/projects/<hash>/` (per-project)

---

#### `reflexion-reflect`
**Trigger:** Manual — invoke when you want structured self-critique of recent work

**What it does:** Self-refinement framework for iterative improvement. Evaluates the most recent output against completeness, quality, correctness, dependency/impact verification, fact-checking, and generated artifact verification. Uses complexity triage to apply the right depth of reflection (quick path for simple tasks, standard path for multi-file work, deep reflection for critical/security changes).

**How to use:**
```
/reflexion:reflect
/reflexion:reflect security
/reflexion:reflect deep reflect if less than 90% confidence
```

**Workflow:**
1. **Complexity triage** — Categorize task as Quick / Standard / Deep
2. **Initial assessment** — Completeness, quality, correctness, dependency checks, fact-checking, artifact verification
3. **Decision point** — Refinement needed? If yes, plan and prioritize fixes
4. **Code-specific checks** — Library-first approach, architecture/DDD alignment, code smells, test coverage
5. **Final verification** — Self-refine checklist + reflexion questions
6. **Confidence scoring** — Weighted rubric (Instruction Following 0.30, Output Completeness 0.25, Solution Quality 0.25, Reasoning 0.10, Coherence 0.10). Must meet threshold based on complexity tier.

**Key rules:** Default score is 2 — must justify any upward deviation. Fight sycophancy and leniency bias. Verify all claims with evidence, not memory.

---

#### `reflexion-critique`
**Trigger:** Manual — invoke for comprehensive multi-perspective review of completed work

**What it does:** Multi-Agent Debate + LLM-as-a-Judge pattern. Spawns three specialized judge agents in parallel (Requirements Validator, Solution Architect, Code Quality Reviewer), each using Chain-of-Verification (CoVe). Judges review independently, then debate disagreements before reaching consensus.

**How to use:**
```
/reflexion:critique
/reflexion:critique src/feature.ts src/feature.test.ts
/reflexion:critique HEAD~1..HEAD
```

**Workflow:**
1. **Context gathering** — Identify scope (files, commits, conversation), capture requirements and decisions
2. **Independent judge reviews** (parallel via Task tool) — Each judge scores X/10 with structured analysis
3. **Cross-review & debate** — Synthesize findings, identify contradictions, resolve disagreements
4. **Consensus report** — Executive summary, judge scores, strengths, prioritized issues, refactoring recommendations, action items

**Three judges:**
- **Requirements Validator** — Checks every requirement is met, identifies gaps and scope creep
- **Solution Architect** — Evaluates design decisions, considers alternatives, assesses scalability
- **Code Quality Reviewer** — Finds code smells, suggests refactorings with before/after examples

**Key rules:** Report-only (no automatic fixes). Be objective and cite specific evidence. Consider project constraints. Disagreements between judges are valuable insights.

---

#### `reflexion-memorize`
**Trigger:** Manual — after completing `/reflexion:reflect` or `/reflexion:critique`

**What it does:** Transforms reflection/critique outputs into durable guidance. Uses Agentic Context Engineering (ACE) to harvest insights, extract patterns/anti-patterns, categorize by impact, and update CLAUDE.md.

**How to use:**
```
/reflexion:memorize
```

**Categories:** Domain Knowledge, Solution Patterns, Anti-Patterns, Context Clues, Quality Gates

**Output:** Updates appropriate section of CLAUDE.md with structured entries (pattern, validation criteria, avoid section).

---

#### `error-memory`
**Trigger:** Automatic — after debugging sessions resolve, or when user corrects approach

**What it does:** Captures failed approaches and working solutions. Persists to `~/.claude/anti-patterns.md` so future sessions never repeat known-bad approaches.

**How to use:** Fires automatically after troubleshooting. Can also invoke manually:
```
Save this fix to error memory
```

**Format persisted:**
```markdown
### [Title] — [Date]
- **Context**: project/language/framework
- **Failed approach**: what was tried
- **Why it failed**: root cause
- **Working fix**: what actually works
- **Applies when**: trigger conditions
```

**Rules:** Never delete patterns. Always include date and scope. Capture user's exact words when they correct you.

---

#### `pre-debug-check`
**Trigger:** Automatic — BEFORE any fix attempt when errors are encountered, plus continuous mid-execution barrier detection

**What it does:** Consults `~/.claude/anti-patterns.md` and project memory for known solutions before debugging. Also includes **barrier recognition** — detecting familiar patterns mid-execution (error deja vu, approach repetition, escalating cascades, environment friction, framework quirks). Prevents retrying failed approaches.

**How to use:** Fires automatically before `systematic-debugging` and stays alert during execution. Reports matches with confidence:
- **HIGH** (exact match) → Apply fix directly, skip debugging
- **MEDIUM** (similar) → Suggest fix, note it's similar-not-identical
- **LOW** (vague) → Mention it, proceed with normal debugging

**Barrier signals:** Error deja vu, approach repetition (tried before), escalating cascade (fix A breaks B breaks C), environment friction (iCloud+git, Node versions), framework quirks. When recognized: STOP → ANNOUNCE → CITE → REDIRECT → VERIFY.

---

#### `isolate-before-iterate`
**Trigger:** Passive — activates during debugging sessions when about to re-run a full pipeline

**What it does:** Prevents the anti-pattern of running 30+ minute full pipelines (backtests, builds, deploys) to debug a single function. Forces Claude to write a minimal standalone test (5-15 lines) that exercises only the suspect logic.

**Escalation ladder:**
- < 30 seconds → fine, run the full thing
- 30s - 5 min → acceptable first time; isolate on second attempt
- 5 - 15 min → must isolate, no exceptions
- 15+ min → stop everything, write isolation script first

**Key rules:**
1. Second run = must isolate. If running the same pipeline a second time to debug, write an isolation script first.
2. One print, one run. If you must debug via the full pipeline, add ONE targeted print that definitively answers your hypothesis.
3. Compare inputs, not outputs. When isolated tests pass but pipeline fails, the bug is in the inputs.

**Coordinates with:** `systematic-debugging` (root cause methodology), `pre-debug-check` (known patterns), `fix-loop` (test cycles), `think-efficiently` (general efficiency).

---

#### `total-recall`
**Trigger:** Always-on — session start (hydrate) + session end (persist) + continuous during session

**What it does:** Infinite cross-session memory. Orchestrates all memory systems into a seamless experience where Claude remembers everything important about the project between sessions — automatically, without `/mem save`.

**Three phases:**
1. **Session start** — silently loads MEMORY.md + all memory files + anti-patterns + AGENT-MEMORY.md + recent git log. Builds a mental model of the project without announcing it.
2. **During session** — watches for capture signals: architecture decisions, gotchas, user corrections, preference statements, project state changes. Saves them to memory files as they happen.
3. **Session end** — runs the "Would I Forget?" test: if starting a new session tomorrow, what would you wish you knew? Persists anything that passes.

**Memory organization:** By topic, not chronology. Files like `architecture.md`, `gotchas.md`, `user_preferences.md`, `current_work.md`. Aim for 5-15 files per project, not 50. Merge into existing files rather than creating duplicates.

**Coordinates with:** `error-memory` (debugging failures), `shared-memory` (AGENT-MEMORY.md), `stop-memory-save.py` (session end hook), `mem` (manual commands).

**Key rule:** Save WHY decisions were made, not just WHAT was decided. "We use Tailwind" is okay. "We use Tailwind because the user prefers utility-first CSS and the project already had it set up" is much better.

---

#### `mem` (command)
**Trigger:** Manual — user-invoked commands

**What it does:** Manages hierarchical memory system at `~/.claude/memory/`. Supports show, save, recall, and forget operations.

**Commands:**
```
/mem show              — Display memory structure and contents
/mem save <text>       — Save observation to appropriate topic
/mem recall <query>    — Search and retrieve relevant memories
/mem forget <topic>    — Remove a topic from memory
```

**Automatic operations:**
- **load** — Runs in background at session start (reads me.md + core.md)
- **save** — Runs in background when something worth keeping is learned
- **recall** — Runs when past context would help current task

---

### Code Quality & Testing

#### `test-driven-development`
**Trigger:** Manual — before ALL implementation work (no exceptions)

**What it does:** Enforces RED-GREEN-REFACTOR cycle. Write failing test → verify it fails → write minimal code to pass → verify it passes → refactor while green.

**How to use:** Start any implementation with:
1. **RED:** Write one minimal failing test
2. Verify it fails (for the right reason)
3. **GREEN:** Write minimal code to make it pass
4. Verify it passes
5. **REFACTOR:** Clean up while tests stay green
6. Repeat for next feature

**Rule:** NEVER skip or reverse the order. Always watch the test fail first.

---

#### `verification-before-completion`
**Trigger:** Automatic — before any claim of "done", "fixed", or "passing"

**What it does:** Gate function requiring evidence before completion claims. IDENTIFY the verification command → RUN it fresh → READ the output → VERIFY it matches the claim.

**How to use:** Before saying "tests pass" or "build succeeds":
1. Run the actual command
2. Check exit code AND output
3. Only then make the claim

**Forbidden phrases:** "should work", "probably passes", "seems fixed" — without evidence.

---

---

### Planning & Execution

#### `writing-plans`
**Trigger:** Manual — after brainstorming/spec approval, before touching code

**What it does:** Creates comprehensive implementation plans with file structure mapping, bite-sized tasks, exact commands with expected output, and TDD cycle per task.

**How to use:**
```
/write-plan Add user authentication with Firebase
```

**Output:** Plan document with:
- File structure map (which files touch per task)
- Ordered tasks with: test → verify fail → implement → verify pass → commit
- Exact commands with expected output
- Skill references with `@skill-name` syntax
- Review loop with spec-document-reviewer subagent

---

#### `executing-plans`
**Trigger:** Manual — when you have a written plan to execute

**What it does:** Executes implementation plans step-by-step with verification checkpoints. Supports subagent-driven (recommended) and manual execution modes.

**How to use:**
```
/execute-plan
```

**Workflow:** Load plan → Review critically → Execute tasks (marking progress) → Run verifications → Stop if blocked → Transition to `finishing-a-development-branch`

---

#### `subagent-driven-development`
**Trigger:** Manual — when executing plans with independent tasks in the current session

**What it does:** Executes plans via fresh subagent per task with two-stage review (spec compliance, then code quality). Subagents have isolated context — no inheritance from main session. Preserves controller context window.

**How to use:** Best for plans with 3+ independent tasks. Each task gets its own agent with focused context, runs independently, gets reviewed before marking complete.

---

#### `using-git-worktrees`
**Trigger:** Manual — before feature work or plan execution

**What it does:** Creates isolated git worktree for implementation. Smart directory selection (existing → CLAUDE.md → ask user). Verifies git-ignored. Runs setup commands (npm install, etc.). Verifies clean baseline.

**Required before:** brainstorming execution, subagent-driven-development, executing-plans

---

#### `finishing-a-development-branch`
**Trigger:** Manual — when implementation is complete and tests pass

**What it does:** Presents 4 integration options: merge locally, create PR, keep branch, or discard. Executes chosen workflow and cleans up worktree.

**Options:**
1. Merge to base branch locally
2. Create GitHub PR
3. Keep branch for later
4. Discard changes

**Rule:** STOP if tests fail — don't proceed to integration.

---

#### `dispatching-parallel-agents`
**Trigger:** Manual — when facing 2+ independent tasks

**What it does:** Coordinates multiple specialized agents working on independent problems concurrently. Each agent gets isolated context, focused scope, and clear success criteria.

**How to use:** When you have multiple unrelated tasks:
1. Identify independent domains
2. Create focused agent tasks with specific context
3. Dispatch in parallel
4. Review and integrate results

---

### Task Flow & Interruption Handling

#### `mid-task-triage`
**Trigger:** Always-on — fires when a new user message arrives while Claude is mid-execution

**What it does:** Instantly classifies mid-task messages into one of three categories and handles them without stopping work. No "should I continue?" — just seamless absorption and momentum.

**The three classifications:**

| Type | Signal | Action |
|------|--------|--------|
| **A) Addendum** | Adds detail/context to current task | Absorb silently, keep working |
| **B) Course Correction** | Changes direction/approach | Pivot with one-line ack, keep working |
| **C) Queue** | Different topic entirely | Note it ("I'll do X after this"), keep working |

**Decision tree:** About current task + adds info → Addendum. About current task + changes direction → Correction. Different topic → Queue. Ambiguous → default to Addendum.

**Urgent interrupts override all:** "STOP", "wait", production bugs → halt immediately.

**Token economics:** Near zero. Classification is instant pattern matching. Saves massive tokens by preventing stop-start cycles and re-orientation.

---

### Agent Orchestration

#### `command-center`
**Trigger:** Automatic — activates on complex multi-domain tasks that are decomposable into parallel workstreams

**What it does:** Master AI agent orchestrator. Analyzes a task, decomposes it into independent workstreams, assigns specialist subagents with expert lenses, launches them in parallel, monitors results, resolves conflicts, and delivers a unified output. You talk to the boss — the boss runs the army.

**The 5-phase protocol:**
1. **Mission Analysis** (~100 tokens) — Decompose into workstreams, identify parallel vs sequential
2. **Agent Briefing** — Self-contained brief per agent: role, mission, context, expert lens, quality bar
3. **Parallel Dispatch** — Launch all independent agents simultaneously
4. **Result Integration** — Review, check for conflicts, resolve, merge
5. **Quality Gate** — Build/test, verify consistency, deliver polished result

**Resource management:**
- **Sizing**: Minimum agents needed (2 focused > 5 fragmented)
- **Strategy**: Research-first (uncertain tasks) vs Execute-first (clear path) vs Hybrid
- **Priority**: Critical (blocks everything) → High (user-facing) → Medium (tests/docs) → Low (nice-to-have)
- **Context budgeting**: Each agent gets ONLY the files/context it needs, not the whole codebase
- **Monitoring**: Check results as they return, resolve conflicts, never duplicate agents

**Budget guard:** <3 agents always fine. 3-5 for substantial features. >5 asks permission first.

**Token economics:** ~200 tokens overhead + ~2000-8000 per agent + ~500 integration. Parallel agents finish in wall-clock time of the slowest (not sum of all). Focused context per agent reduces per-agent cost.

---

### Research & Context

#### `deep-research`
**Trigger:** Automatic — when asked to implement an unfamiliar concept, statistic, algorithm, or technique

**What it does:** Self-directed literature review that makes Claude an expert before writing any code. Searches authoritative sources (academic papers, official docs, expert analysis), identifies alternatives, and presents a research summary with recommendation — all before implementation.

**The flow:**
1. **Self-assess** — honestly identify knowledge gaps
2. **Search** — Tier 1 (academic/official) → Tier 2 (expert blogs) → Tier 3 (community), max 5 searches
3. **Deep read** — WebFetch top 3 sources with targeted extraction prompts
4. **Synthesize** — present compact summary: what it is, how it works, alternatives table, recommendation
5. **Get approval** — user confirms approach before any code is written

**Token budget:** Max 5 WebSearch + 3 WebFetch calls per topic. Skips deep research if self-assessment shows 80%+ confidence. Summary is 200-400 words max with source links.

**Key difference from search-first:** search-first looks for existing *code/libraries*. deep-research learns the *domain knowledge* needed to implement correctly.

---

#### `search-first`
**Trigger:** Manual — before writing any custom code

**What it does:** 5-phase research workflow: Need Analysis → Parallel Search (npm, PyPI, MCP, GitHub, existing code) → Evaluate → Decide (Adopt/Extend/Compose/Build) → Implement.

**How to use:** Before implementing something new, check if it already exists:
1. Search your codebase first
2. Then npm/PyPI
3. Then MCP registry
4. Then GitHub
5. Only build custom if nothing fits

**Decision matrix:** Score candidates on functionality, maintainability, community, docs, license.

---

#### `iterative-retrieval`
**Trigger:** Manual — when spawning subagents that need codebase context

**What it does:** 4-phase loop (DISPATCH → EVALUATE → REFINE → LOOP) that progressively refines what files a subagent needs. Starts broad, identifies gaps, narrows search. Max 3 cycles.

**How to use:** When you need to give a subagent the right files:
1. Broad initial query
2. Score relevance of results (0.0–1.0)
3. Refine based on gaps
4. Loop until high-relevance (0.8+) results

---

#### `strategic-compact`
**Trigger:** Automatic — suggests `/compact` at logical task boundaries

**What it does:** Monitors tool call count, suggests compaction at threshold (50 calls), reminds every 25 after. Compacts at logical boundaries (after planning, after debugging) rather than arbitrary points.

**What survives compaction:** CLAUDE.md, TodoWrite, memory files, git state
**What's lost:** Intermediate reasoning, file contents, tool history

---

#### `precision-reading`
**Trigger:** Always-on — shapes every file read

**What it does:** Grep first, read second. Instead of loading entire 2000-line files, finds the relevant section with Grep (getting line numbers), then reads only those lines with offset+limit. Small files (<100 lines) are read fully — the overhead isn't worth it.

**Size thresholds:**
- < 100 lines → read whole file
- 100-500 lines → grep+target if you need a specific section
- 500+ lines → ALWAYS grep first, then targeted read

**Token savings:** A 1500-line file read costs ~1500 lines of tokens. Targeted read of 30 lines costs ~30 lines. That's a 98% reduction per file access.

---

#### `prompt-improver`
**Trigger:** Automatic (hook) — fires on every user message

**What it does:** Detects vague prompts and enriches them with targeted research and clarifying questions. Silent when prompts are already clear.

**4 phases:**
1. **Research** — Check conversation history → codebase → docs → web
2. **Generate** — 1-6 targeted questions grounded in research findings
3. **Clarify** — Ask user
4. **Execute** — Proceed with enriched understanding

---

#### `prompt-architect`
**Trigger:** Always-on — every user message, zero overhead

**What it does:** Internally restructures every prompt into the optimal execution format before acting. Extracts intent, identifies implicit requirements, infers constraints, resolves ambiguity, and executes as if the user gave the perfect prompt. The user types naturally; Claude executes perfectly on the first try.

**6-component mental decomposition:**
1. **TASK** — What exactly am I being asked to do?
2. **CONTEXT** — What do I already know that's relevant?
3. **SCOPE** — What's in bounds vs out of bounds?
4. **QUALITY** — What does "done right" look like?
5. **FORMAT** — How should the output be structured?
6. **UNSTATED** — What did they NOT say but clearly expect?

**Key features:**
- Intent extraction (hear the complete intent, not just literal words)
- Implicit requirement detection (professional defaults a senior dev would handle)
- Quality calibration (pragmatic → professional → bulletproof based on context)
- Ambiguity resolution (conversation > codebase > common interpretation > most impactful)
- Stream-of-consciousness organization (reorders chaotic requests into logical execution)

**Boundary with `prompt-improver`:** Improver catches vague prompts and asks questions. Architect optimizes ALL prompts during execution. They complement — improver is the safety net, architect is the optimizer.

**Token economics:** ~0 tokens (mental checklist). Net NEGATIVE token cost — eliminates "that's not what I meant" redo cycles.

---

### Review & Collaboration

#### `requesting-code-review`
**Trigger:** Manual — after completing tasks or major features

**What it does:** Dispatches a code-reviewer subagent with precisely crafted context (never session history). Reviewer evaluates work independently and reports assessment.

**How to use:** After completing implementation:
1. Get git SHAs (base and HEAD)
2. Dispatch reviewer with: what was implemented, requirements, SHAs, description
3. Act on feedback: Critical issues immediately, Important before proceeding

---

#### `receiving-code-review`
**Trigger:** Manual — when receiving review feedback

**What it does:** Technical evaluation process for review feedback. Prevents performative agreement. Requires verification before implementing suggestions.

**Rules:**
- NEVER respond with "You're right!" or "Thanks for catching that!"
- Verify each suggestion against the codebase
- Push back with technical reasoning if the suggestion is wrong
- Implement one item at a time
- Actions speak louder than acknowledgments

---

### Workflow Automation

#### `backtest`
**Trigger:** Manual — `/backtest` or when mentioning backtesting, model evaluation, accuracy comparison

**What it does:** Standardized workflow for running and evaluating prediction model backtests. Ensures visible output via `| tee`, compares against baseline accuracy, and commits only when metrics improve.

**How to use:**
```
/backtest
```

**Workflow:** Verify DB → Run with `| tee` → Parse metrics → Compare to baseline → Commit if improved (or report regression)

---

#### `audit`
**Trigger:** Manual — `/audit` or when asked to scan for secrets, check security

**What it does:** Scans Python and JavaScript files for hardcoded API keys, tokens, credentials. Fixes by moving to env vars. Also checks for code quality anti-patterns (debug statements, unused imports, stale TODOs).

**How to use:**
```
/audit
```

**Workflow:** Scan for secrets → Fix (move to env vars) → Scan for quality issues → Commit → Output report

---

#### `deploy`
**Trigger:** Manual — `/deploy` or when asked to ship, release, push to production

**What it does:** Full Cloudflare Pages/Workers deployment pipeline with pre-flight checks (lint, test, build), deployment snapshot for rollback, post-deploy verification, automatic rollback on failure, and release tagging.

**How to use:**
```
/deploy
```

**Workflow:** Pre-flight → Snapshot → Deploy → Verify (HTTP 200 + key pages) → Rollback if failed → Tag release if passed

**Rule:** NEVER deploy without passing tests. ALWAYS verify live site. ALWAYS rollback on failure.

---

#### `site-update-protocol`
**Trigger:** Light — fires when algorithm changes are committed or user mentions updating the website

**What it does:** Universal checklist for fully updating sports prediction websites after any algorithm change. Covers data regeneration, frontend verification, deployment, and post-deploy validation across all tabs (Home, Picks, Dashboard, History, Admin).

**Sites covered:**
- **OctagonAI** (UFC) — octagonai.pages.dev
- **Diamond Predictions** (MLB + NHL) — diamond-predict.pages.dev
- **Courtside AI** (CBB + NBA) — courtside-ai.pages.dev

**6-Phase Protocol:**
1. **Regenerate Data** — Re-run algorithm/backtest, regenerate all static JSON files
2. **Verify Data Files** — Confirm every JSON file has fresh timestamps and correct stats
3. **Update Frontend** — Check for hardcoded stats (landing page hero, system counts)
4. **Build & Deploy** — Clone to `/tmp/`, build, deploy to Cloudflare Pages
5. **Post-Deploy Verification** — Open every tab, verify all stats/charts/tables reflect new data
6. **Update Firestore** — Sync real-time data stores (OctagonAI, Courtside AI)

**Key rule:** If the algorithm changed, the ENTIRE site must reflect the new state. No partial updates.

**Coordinates with:** `deploy` (Cloudflare deployment mechanics), `backtest` (algorithm validation), `version-bump` (version incrementing)

---

#### `fix-loop`
**Trigger:** Manual — `/fix-loop` or when asked to fix all tests, make tests pass

**What it does:** Self-healing CI loop. Runs full test suite, diagnoses each failure, fixes source code (NEVER test files), re-runs until all pass, then commits.

**How to use:**
```
/fix-loop
```

**Workflow:** Run tests → For each failure: read test → read source → diagnose → fix source → verify → Final regression check → Commit

**Rules:** Never modify tests. Max 3 full-suite iterations. Skip network-dependent tests.

---

#### `parallel-sweep`
**Trigger:** Manual — when doing coefficient searches, hyperparameter tuning, or parallelizable parameter optimization

**What it does:** Spawns N headless Claude Code agents (`claude -p`) to search parameter spaces in parallel. Each agent handles a partition and writes results to a shared SQLite database.

**How to use:** Describe the parameter space and evaluation metric. The skill partitions the space across agents and generates a sweep script.

**Workflow:** Define search space → Partition into N subspaces → Launch headless agents → Wait → Query top results from SQLite

---

### Session Continuity

#### `seamless-resume`
**Trigger:** Always-on — fires when user sends "continue", "go", "keep going", or returns to a paused session

**What it does:** When a session is interrupted (tab switch, timeout, compaction), resumes execution instantly with zero ceremony. No re-reading files, no re-explaining context, no "where were we?" — just picks up the exact next step.

**The protocol:**
1. Identify where execution stopped (mid-edit, mid-plan, pending tool call)
2. Resume immediately — no greetings, no recaps, no confirmation
3. If context was compacted, give a ONE-LINE status then proceed

**Rules:**
- "Continue" means GO, not "tell me what you were doing"
- Don't re-read files already in context
- Don't re-ask questions already answered
- Don't summarize previous work (they can scroll up)
- Match the previous pace — if you were moving fast, keep moving fast

---

### Communication

#### `response-recap`
**Trigger:** Automatic — fires ONLY after complex, multi-step work (not every response)

**What it does:** Provides a plain English summary after complex work — multi-file changes, debugging sessions with non-obvious root causes, architecture decisions, multi-step implementations. Skips for single-file edits, quick fixes, Q&A, and routine tasks.

**The decision rule:** If the user would need to scroll up to remember what just happened → add a recap. If the response fits on one screen → skip it.

**Format:**
```
---
**What happened:** [1-2 sentences — plain English]
**What changed:** [file list with one-line descriptions]
**Current state:** [where things stand]
```

**Rules:**
- Lead with "what" not "how" — say what the change *means*, not line numbers
- Max 5 bullets in "What changed"
- Skip entirely for quick fixes and simple answers
- Add root cause insight for debugging sessions

---

### Smart Clarification

#### `smart-clarify`
**Trigger:** Always-on — fires when ambiguity is detected in user's request

**What it does:** Instead of guessing or asking open-ended "what do you mean?" questions, presents a structured multiple-choice question with 2-4 options. User picks a letter, Claude proceeds instantly.

**Format:**
```
Quick question — [one sentence framing the ambiguity]:

A) [Most likely interpretation — ~60% of the time this is right]
B) [Second most likely — ~30%]
C) [Third if genuinely plausible]
D) Something else — tell me what you had in mind

→ Just reply with the letter!
```

**The 80/20 rule:**
- 80%+ confident → just do it, mention assumption
- 50-80% → do it, flag the assumption clearly
- <50% → ask multiple choice

**Key rules:** A/B should cover ~90% of cases. One question at a time. After they answer, execute immediately — no follow-ups.

---

### Natural Language Interface

#### `intent-detection`
**Trigger:** Always-on — evaluates every user message

**What it does:** Automatically maps plain language to the right slash command or workflow. Instead of memorizing `/deploy`, `/backtest`, `/audit`, etc., just say what you want in natural language and the right workflow triggers.

**Examples:**
| You say | Claude triggers |
|---------|----------------|
| "ship it" | `/deploy` |
| "the tests are all broken" | `/fix-loop` |
| "any leaked API keys?" | `/audit` |
| "how's the model doing?" | `/backtest` |
| "I want to add dark mode" | `/brainstorm` |
| "break this into steps" | `/write-plan` |
| "remember we use Tailwind" | `/mem save` |
| "try a bunch of different weights" | `parallel-sweep` |
| "fix tests then deploy" | `/fix-loop` → `/deploy` (chained) |

**Confidence levels:**
- **High** → executes immediately with a brief announcement
- **Medium** → confirms briefly, then executes
- **Low** → asks one clarifying question

**Won't trigger on:** Questions *about* workflows, hypotheticals, past tense, or explicit overrides ("don't deploy yet")

---

### Meta Skills

#### `skill-manager`
**Trigger:** Always-on (meta) — fires on every message

**What it does:** Prevents skill overload by enforcing weight classes and budgets. Skills are classified as Passive (behavioral guidance, unlimited), Light (quick checks, max 5/message), or Heavy (spawn agents/run commands, max 2/message). Enforces the 67-skill hard cap with a one-in-one-out rule. Includes overthinking detector.

**Key rules:**
- Passive skills: zero token cost, always allowed
- Light skills: max 5 per message
- Heavy skills: max 2 per message
- 67-skill cap: adding a new skill requires removing or merging an existing one

### Execution Discipline

#### `think-efficiently`
**Trigger:** Always-on — before every action

**What it does:** Before executing anything, checks three questions: (1) Will this produce new information? (2) Is there a faster path? (3) Is the effort proportional to the value? Includes overthinking test and three rules: bias toward action, one obvious path = take it, execution over explanation.

#### `prompt-anchoring`
**Trigger:** Always-on — during long sessions

**What it does:** Keeps Claude anchored to the original prompt objective. Periodic drift checks prevent "Claude ADHD" — going off on tangents or expanding scope beyond what was asked — without reducing proactivity on the actual task.

#### `calibrated-confidence`
**Trigger:** Always-on — every response

**What it does:** Makes Claude honest about what it knows vs what it's guessing. Dynamically adjusts speed and depth based on confidence level. Flags uncertainty explicitly so the user knows when to trust and when to verify.

#### `take-your-time`
**Trigger:** Always-on — complex multi-item prompts

**What it does:** Matches effort to prompt complexity. A 20-bullet detailed prompt gets 20 individual implementations, not one rushed pass. Prevents AI slop on complex work while staying fast on simple tasks. Each requirement is treated as its own unit of work.

### Quality & Output

#### `anti-slop`
**Trigger:** Always-on — structured output generation

**What it does:** Zero tolerance for placeholder data ("Unknown", "N/A", "TBD") in any deliverable. Every field gets real data or an explicit gap explanation. Prevents AI-generated garbage from reaching the user.

#### `qa-gate`
**Trigger:** Automatic — before feature delivery

**What it does:** Tiered QA checkpoint scaled to change complexity. Tier 1 (config changes): mental trace. Tier 2 (single function): quick check. Tier 3 (multi-file): full subagent testing. Includes bug-fix verification protocol and repeat-bug escalation.

#### `version-bump`
**Trigger:** Automatic — commits with version changes

**What it does:** Automated semantic versioning. Determines patch/minor/major from the nature of changes, bumps package.json version, and formats commit messages with version prefix.

### Debugging (Additional)

#### `confusion-prevention`
**Trigger:** Always-on — confusion signals detected

**What it does:** Detects when Claude is confused about its own state — what version of a file is active, what config values are set, what results came from which run. Instead of spiraling ("wait... actually... let me check..."), forces a STOP-ORIENT-ACT protocol. Snapshots critical state before destructive actions, recognizes ground-shift signals (config changed, file reverted), prevents comparing incompatible results.

**Confusion signals:** Comparing numbers from different runs, re-reading files already read, contradicting own recent output, "wait, actually..." language patterns.

### Domain (Additional)

#### `profit-driven-development`
**Trigger:** Always-on — sports prediction work

**What it does:** The north star for all sports prediction work. Every change must answer: "will this make the NEXT picks more correct and more profitable?" Prevents overfitting to historical data and endless backtest spinning. Forces forward-looking accuracy focus.

#### `screenshot-dissector`
**Trigger:** Automatic — screenshot provided during debugging

**What it does:** Methodical pixel-level screenshot analysis during debugging. Catches layout bugs, state issues, console errors, and UI regressions beyond the obvious. Systematic visual inspection rather than just looking at the most prominent element.

### Persistence (Additional)

#### `never-give-up`
**Trigger:** Automatic — integration failure of validated idea

**What it does:** Never abandon a proven-valuable idea because integration failed. Uses an evidence gate + think-efficiently integration to persist smartly, not stubbornly. Failed execution is not a failed idea — iterate, learn, try harder. But also never burn tokens on endless retries without new information.

#### `user-rules`
**Trigger:** Always-on — hard constraint detected

**What it does:** Captures and enforces user-defined hard constraints across sessions. When the user sets a rule ("max 70 events", "always use approach X", "never do Y"), it's saved to `~/.claude/projects/<project>/memory/user_rules.md` and checked before every relevant action. Rules survive compaction, crashes, and session boundaries. These are NOT preferences — they are hard constraints that must never be violated.

**Detection signals:** "always", "never", "must", "max/min", "from now on", "don't ever"

---

## Hooks

Hooks are shell scripts that fire automatically on specific Claude Code events.

| Hook | File | Event | What It Does |
|------|------|-------|-------------|
| **Prompt Improver** | `hooks/improve-prompt.py` | UserPromptSubmit | Fast-paths clear prompts (short, specific, detailed). Only evaluates mid-length ambiguous prompts. Enriches genuinely vague ones with research and clarification. |
| **Observer** | `hooks/observe.py` | PostToolUse | Captures all tool calls (except Glob/Grep/Read/ToolSearch) with timestamps. Stores to `observations.jsonl` per project. Powers continuous-learning-v2. |
| **Memory Save** | `hooks/stop-memory-save.py` | Stop | At session end (if >4 messages), reminds Claude to save learnings to project or global memory. |
| **Skill Tracker** | `hooks/track-skill-performance.js` | Stop + PostToolUse (every 30 calls) | Collects skill effectiveness data during sessions. Generates reports for `/skill-insights` on which skills help vs hurt. |

---

## Commands

Slash commands users can invoke directly.

| Command | File | What It Does |
|---------|------|-------------|
| `/audit` | `commands/audit.md` | Scan for hardcoded secrets and quality issues |
| `/backtest` | `commands/backtest.md` | Run model backtest with baseline comparison |
| `/brainstorm` | `commands/brainstorm.md` | Shortcut to invoke brainstorming skill |
| `/deploy` | `commands/deploy.md` | Full deploy pipeline with rollback |
| `/execute-plan` | `commands/execute-plan.md` | Shortcut to invoke executing-plans skill |
| `/fix-loop` | `commands/fix-loop.md` | Self-healing CI: test, fix, re-run until green |
| `/mem` | `commands/mem.md` | Memory management (show, save, recall, forget) |
| `/skill-insights` | `commands/skill-insights.md` | Report on which skills help vs hurt effectiveness |
| `/write-plan` | `commands/write-plan.md` | Shortcut to invoke writing-plans skill |

---

## Continuous Learning System

The learning infrastructure has three layers:

### Layer 1: Observation (100% capture)
- `observe.py` hook fires on every PostToolUse
- Stores timestamped tool call data to `observations.jsonl`
- Scoped by project (via git remote URL hash)

### Layer 2: Instinct Generation
- Continuous-learning-v2 analyzes observations
- Creates atomic instincts with confidence scores (0.3–0.9)
- Domains: code-style, testing, git, debugging, workflow
- Evidence-tracked: which observations created each instinct

### Layer 3: Evolution
- High-confidence instincts cluster into full skills/commands/agents
- Project-scoped instincts promote to global when seen in 2+ projects (conf >= 0.8)
- Commands: `/instinct-status`, `/evolve`, `/promote`

### Error Learning Loop
```
Error occurs
    │
    ├─ pre-debug-check ──→ Known fix? ──→ Apply directly (0 wasted tokens)
    │                          │
    │                          └─ No match ──→ isolate-before-iterate ──→ systematic-debugging
    │                                          (fast feedback loop)           │
    │                                                                        └─ Fix found ──→ error-memory
    │                                                                   │
    │                                                                   └─ Saved to anti-patterns.md
    │                                                                        │
    └────────────────────────── Next time ──────────────────────────────────┘
```

### Memory Hierarchy
```
~/.claude/
├── anti-patterns.md           ← Error memory (known failures + fixes)
├── memory/
│   ├── me.md                  ← User profile
│   ├── core.md                ← Key learnings + pointers
│   ├── topics/<topic>.md      ← Detailed topic entries
│   └── projects/<project>.md  ← Project-specific knowledge
├── homunculus/
│   ├── instincts/personal/    ← Learned instincts (global)
│   ├── instincts/inherited/   ← Shared instincts
│   ├── evolved/               ← Promoted skills/commands
│   └── projects/<hash>/       ← Per-project instincts
└── projects/*/memory/         ← Claude Code project memory (MEMORY.md + files)
```

---

## Quick Reference Card

| I want to... | Use this |
|--------------|----------|
| Design a feature | `/brainstorm` → `/write-plan` → `/execute-plan` |
| Fix a bug | `pre-debug-check` → `isolate-before-iterate` → `systematic-debugging` → `error-memory` |
| Remember something | `/mem save <text>` |
| Recall past work | `/mem recall <query>` |
| Review my code | `requesting-code-review` |
| Reflect on output | `/reflexion:reflect` → `/reflexion:memorize` |
| Deep analysis | `/reflexion:critique` (3-judge panel) |
| Critical decision | `/fpf:propose-hypotheses` |
| Check skill effectiveness | `/skill-insights` |
| Search before coding | `search-first` |
| Run a backtest | `/backtest` |
| Scan for secrets | `/audit` |
| Deploy to production | `/deploy` |
| Fix all failing tests | `/fix-loop` |
| Sweep parameters | `parallel-sweep` |
| Prevent bugs before writing | `zero-iteration` (always-on) |
| Update all instances of a pattern | `pattern-propagation` (automatic) |
| Map the codebase | `codebase-cartographer` (session start) |
| Smart commit messages | `git-sorcery` (always-on) |
| Find bug-introducing commit | `git-sorcery` bisect |
| Check background processes | `process-monitor` (automatic) |
| Think like a domain expert | `expert-lens` (always-on) |
| Orchestrate parallel agent army | `command-center` (automatic) |
| Handle mid-task interruptions | `mid-task-triage` (always-on) |

---

**69 skills. 4 hooks. 9 commands. One intelligence stack.**
