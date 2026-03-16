# Skills Reference — Nick's Claude Code Superpowers

> Complete documentation for all 36 skills, 4 hooks, 4 commands, and the continuous learning system.
> Last updated: 2026-03-16

---

## Table of Contents

- [How Skills Work](#how-skills-work)
- [Skill Trigger Types](#skill-trigger-types)
- [Workflow Map](#workflow-map)
- [Skills by Category](#skills-by-category)
  - [Foundation (Always Active)](#foundation-always-active)
  - [Autonomy & Completeness](#autonomy--completeness)
  - [Thinking & Reasoning](#thinking--reasoning)
  - [Memory & Learning](#memory--learning)
  - [Code Quality & Testing](#code-quality--testing)
  - [Planning & Execution](#planning--execution)
  - [Research & Context](#research--context)
  - [Review & Collaboration](#review--collaboration)
  - [OpenViking Context DB](#openviking-context-db)
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
    ├─ Vague? ──→ prompt-improver (auto-enriches)
    │
    ├─ Creative? ──→ brainstorming ──→ writing-plans ──→ executing-plans
    │                                                        │
    │                                                        ├─ using-git-worktrees
    │                                                        ├─ subagent-driven-development
    │                                                        └─ finishing-a-development-branch
    │
    ├─ Bug/Error? ──→ pre-debug-check ──→ systematic-debugging
    │                  (check known fixes)    (root cause first)
    │                                              │
    │                                              └─ error-memory (save fix)
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

#### `using-superpowers`
**What it does:** Meta-skill that establishes skill invocation protocol. Ensures relevant skills fire BEFORE any response — even clarifying questions.

**How to use:** Always active at conversation start. Checks if any skill matches (even 1% probability), invokes it, then responds. Instruction priority: User > Skills > System prompt.

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

### Memory & Learning

#### `continuous-learning` (v1)
**Trigger:** Automatic — Stop hook at session end

**What it does:** Extracts reusable patterns from completed sessions: error resolutions, user corrections, workarounds, debugging techniques, project-specific knowledge. Saves to `~/.claude/skills/learned/`.

**Limitation:** ~50-80% pattern detection reliability. v2 is recommended.

---

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
**Trigger:** Automatic — BEFORE any fix attempt when errors are encountered

**What it does:** Consults `~/.claude/anti-patterns.md` and project memory for known solutions before debugging. Prevents retrying failed approaches.

**How to use:** Fires automatically before `systematic-debugging`. Reports matches with confidence:
- **HIGH** (exact match) → Apply fix directly, skip debugging
- **MEDIUM** (similar) → Suggest fix, note it's similar-not-identical
- **LOW** (vague) → Mention it, proceed with normal debugging

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

#### `verification-loop`
**Trigger:** Manual — after implementing features or before PRs

**What it does:** 6-phase comprehensive verification: Build → Type Check → Lint → Tests → Security → Diff Review. Produces detailed report with PASS/FAIL status.

**How to use:** Run after completing implementation:
1. Build check
2. Type checking (tsc, mypy, etc.)
3. Lint (eslint, ruff, etc.)
4. Test suite
5. Security scan
6. Diff review (unintended changes?)

**Output:** Verification report with pass/fail per phase, issue counts, coverage percentage.

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

### Research & Context

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

#### `prompt-improver`
**Trigger:** Automatic (hook) — fires on every user message

**What it does:** Detects vague prompts and enriches them with targeted research and clarifying questions. Silent when prompts are already clear.

**4 phases:**
1. **Research** — Check conversation history → codebase → docs → web
2. **Generate** — 1-6 targeted questions grounded in research findings
3. **Clarify** — Ask user
4. **Execute** — Proceed with enriched understanding

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

### OpenViking Context DB

#### `ov-add-data`
**Trigger:** Manual — when adding resources, files, URLs, or memories to persistent storage

**What it does:** Wrapper for OpenViking CLI commands to import content into the context database.

**Commands:**
```bash
ov add-resource ./docs/api-spec.md           # Local file
ov add-resource https://github.com/user/repo  # Git repo
ov add-resource https://example.com/doc.pdf   # URL
ov add-memory "User prefers Tailwind CSS"     # Plain text memory
ov add-skill ./skills/my-skill/               # Skill file
```

**Prerequisites:** OpenViking server running, CLI configured at `~/.openviking/ovcli.conf`

---

#### `ov-search-context`
**Trigger:** Manual — when searching stored memories, skills, or resources

**What it does:** Semantic and pattern-based search across all OpenViking content.

**Commands:**
```bash
ov find "authentication flow"                # Semantic search
ov ls viking://resources/                     # List directory
ov tree viking://resources/ --level-limit 2   # Tree view
ov grep "viking://resources" "TODO:"          # Pattern match
ov glob "**/*.md"                             # File path match
ov read viking://resources/docs/api.md        # Full content
```

---

#### `ov-server-operate`
**Trigger:** Manual — for server setup, management, and maintenance

**What it does:** Complete operational procedures: install, configure, start, stop, cleanup, and troubleshoot the OpenViking server.

**Quick reference:**
```bash
# Start
source ~/.openviking/ov-venv/bin/activate
nohup openviking-server > ~/.openviking/log/openviking-server.log 2>&1 &

# Health check
curl http://localhost:1933/health

# Stop
pkill -f openviking-server
```

---

#### `memory-recall`
**Trigger:** Automatic — when user asks about past decisions, fixes, or historical context

**What it does:** Sub-agent that searches OpenViking memory bridge for relevant historical memories. Returns actionable facts with source URIs.

**How to use:** Fires automatically when historical context is needed. Can also invoke:
```
What did we decide about the auth flow last week?
```

---

### Meta Skills

#### `writing-skills`
**Trigger:** Manual — when creating or editing skills

**What it does:** TDD approach to skill creation. RED: baseline test of skill failure → GREEN: write minimal skill → REFACTOR: close loopholes. Covers technique, pattern, and reference skill types.

**How to use:** When creating a new skill:
1. **RED:** Create pressure scenario without the skill, document baseline failures
2. **GREEN:** Write minimal SKILL.md that addresses those failures
3. **REFACTOR:** Identify new loopholes, add explicit counters

---

## Hooks

Hooks are shell scripts that fire automatically on specific Claude Code events.

| Hook | File | Event | What It Does |
|------|------|-------|-------------|
| **Prompt Improver** | `hooks/improve-prompt.py` | UserPromptSubmit | Evaluates every user message. If vague, enriches with research and clarifying questions. Silent when prompt is clear. |
| **Observer** | `hooks/observe.py` | PostToolUse | Captures all tool calls (except Glob/Grep/Read/ToolSearch) with timestamps. Stores to `observations.jsonl` per project. Powers continuous-learning-v2. |
| **Memory Save** | `hooks/stop-memory-save.py` | Stop | At session end (if >4 messages), reminds Claude to save learnings to project or global memory. |

---

## Commands

Slash commands users can invoke directly.

| Command | File | What It Does |
|---------|------|-------------|
| `/mem show` | `commands/mem.md` | Display memory structure and contents |
| `/mem save <text>` | `commands/mem.md` | Save observation to appropriate topic in `~/.claude/memory/` |
| `/mem recall <query>` | `commands/mem.md` | Search and retrieve relevant memories |
| `/mem forget <topic>` | `commands/mem.md` | Remove a topic from memory |
| `/brainstorm` | `commands/brainstorm.md` | Shortcut to invoke brainstorming skill |
| `/write-plan` | `commands/write-plan.md` | Shortcut to invoke writing-plans skill |
| `/execute-plan` | `commands/execute-plan.md` | Shortcut to invoke executing-plans skill |

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
    │                          └─ No match ──→ systematic-debugging
    │                                              │
    │                                              └─ Fix found ──→ error-memory
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
| Fix a bug | `pre-debug-check` → `systematic-debugging` → `error-memory` |
| Remember something | `/mem save <text>` |
| Recall past work | `/mem recall <query>` or `memory-recall` |
| Review my code | `requesting-code-review` |
| Reflect on output | `/reflexion:reflect` → `/reflexion:memorize` |
| Deep analysis | `/reflexion:critique` (3-judge panel) |
| Critical decision | `/fpf:propose-hypotheses` |
| Check skill status | `/instinct-status` |
| Search before coding | `search-first` |
| Add to context DB | `ov add-resource <path>` |
| Search context DB | `ov find <query>` |

---

**38 skills. 3 hooks. 4 commands. One intelligence stack.**
