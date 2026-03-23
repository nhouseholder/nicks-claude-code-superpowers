# Nick's Claude Code Superpowers

> A comprehensive intelligence stack for Claude Code — making it smarter, more efficient, better at memory, and more capable.

## ⚡ 63 Skills at a Glance

| # | Skill | What it does |
|---|-------|------|
| 1 | **adaptive-voice** | Matches the user's energy and pace — terse in flow, detailed when learning, calm when frustrated — so responses always feel natural. |
| 2 | **anti-slop** | Zero tolerance for placeholder data ("Unknown", "N/A", "TBD") in any deliverable — every field gets real data or an explicit gap explanation so the user never receives AI-generated garbage. |
| 3 | **audit** | Scans codebases for hardcoded secrets, security issues, and anti-patterns so vulnerabilities don't ship. |
| 4 | **backtest** | Runs prediction model backtests with walk-forward integrity, overfitting guards, and future-accuracy focus so model changes are data-driven. |
| 5 | **brainstorming** | Explores intent, requirements, and design before complex implementations so you build the right thing. |
| 6 | **calibrated-confidence** | Makes Claude honest about what it knows vs guesses — dynamically adjusts speed and flags uncertainty so the user knows when to trust and when to verify. |
| 7 | **codebase-cartographer** | Maps codebase architecture with fast-path for documented projects so Claude navigates instantly without redundant exploration. |
| 8 | **coding-standards** | Enforces universal best practices for TypeScript, JavaScript, React, and Node.js so code quality is consistent. |
| 9 | **cleanup-old-files** | When code advances significantly, identifies and removes stale files (old backtestors, deprecated configs, superseded scripts) that would confuse future agents into running the wrong version. |
| 10 | **confusion-prevention** | Detects when Claude is confused and forces re-orientation instead of spiraling — prevents the "wait... actually... let me check..." pattern that burns 15+ tool calls. |
| 11 | **content-research-writer** | Full research + writing assistant — searches the web, gathers sources, builds outlines, and drafts content with citations. Use for blog posts, articles, documentation, and any structured writing that needs research backing. |
| 11 | **continuous-learning-v2** | Observes sessions via hooks and creates atomic instincts with confidence scoring so Claude gets smarter over time. |
| 12 | **data-consistency-check** | Validates that displayed data is mathematically and logically consistent before claiming correctness — catches impossible stats like profit with 0 wins. |
| 13 | **deep-research** | Stops and researches unfamiliar concepts from authoritative sources before implementing so solutions are expert-level. |
| 14 | **deploy** | Handles full deployment with Cloudflare-specific checks, smoke tests, and auto-rollback so broken code never reaches production. |
| 15 | **dispatching-parallel-agents** | Launches 2+ independent tasks as concurrent subagents so wall-clock time is cut in half (or more). |
| 16 | **error-memory** | Captures failed approaches and working solutions so Claude never wastes tokens retrying known-bad fixes. |
| 17 | **executing-plans** | Executes written implementation plans with review checkpoints so multi-step work stays on track. |
| 18 | **expert-lens** | Activates domain-expert mental models so output meets professional-grade bars. |
| 19 | **finishing-a-development-branch** | Guides branch completion with structured merge/PR/cleanup options so work integrates cleanly. |
| 20 | **fix-loop** | Self-healing CI loop that runs tests, diagnoses, fixes, and re-runs until all pass so broken builds resolve autonomously. |
| 21 | **fpf-hypotheses** | Executes first-principles hypothesis cycles so complex decisions are grounded in evidence, not gut feeling. |
| 22 | **git-sorcery** | Smart commit messages, conflict resolution, bisect, and cherry-pick so git operations are expert-level. |
| 23 | **implicit-preferences** | Detects patterns in user corrections and adapts without being told — if the user corrects the same thing repeatedly, treats it as a permanent preference for the session. |
| 24 | **isolate-before-iterate** | Before debugging via full pipelines, isolate the suspect logic in a minimal standalone test — prevents 30+ minute feedback loops when a 5-line script would answer in seconds. |
| 25 | **iterative-retrieval** | Progressively refines context retrieval so subagents get exactly the information they need, no more. |
| 26 | **mid-task-triage** | Instantly classifies mid-task messages as addendum, course correction, or queue item so nothing derails active work. |
| 27 | **never-give-up** | Never abandon a proven-valuable idea because integration failed — failed execution is not a failed idea. Iterate, learn, try harder. |
| 28 | **opportunistic-improvement** | Fixes no-brainer code issues in files already being touched so the project gets cleaner with every interaction. |
| 29 | **parallel-sweep** | Runs parallel parameter sweeps with walk-forward and overfitting guards so optimization finishes in minutes, not hours. |
| 30 | **pattern-propagation** | When a pattern changes in one place, updates ALL instances across the codebase so nothing is left inconsistent. |
| 31 | **pre-debug-check** | Checks known anti-patterns and past failures BEFORE attempting fixes so tokens aren't wasted on dead-end approaches. |
| 32 | **precision-reading** | Grep-first, read-only-relevant-lines so large files don't waste thousands of tokens on irrelevant content. |
| 33 | **predictive-next** | After completing a task, offers the most likely next step in one line so workflow momentum is maintained. |
| 34 | **proactive-qa** | Walks the user journey after every implementation, catching edge cases and fixing adjacent bugs before you notice. |
| 35 | **process-monitor** | Detects hung processes, port conflicts, and zombie tasks so dev environment issues are caught before they cascade. |
| 36 | **profit-driven-development** | The north star for all sports prediction work — every change must answer "will this make the NEXT picks more correct and more profitable?" |
| 37 | **progressive-disclosure** | Leads with the answer or action, then offers details only if asked — prevents walls of text when the user just wants the result. |
| 38 | **prompt-architect** | Internally decomposes every prompt into intent, context, scope, and unstated requirements so execution is perfect first try. |
| 39 | **qa-gate** | Mandatory QA checkpoint before delivering any feature — dispatches independent testing agent to exercise the implementation end-to-end so the user never finds bugs first. |
| 40 | **receiving-code-review** | Evaluates review feedback with technical rigor before implementing so bad suggestions don't degrade code quality. |
| 41 | **reflexion** | Self-refinement and review framework. `/reflexion:reflect` for quick self-assessment, `/reflexion:critique` for deep multi-dimensional review via a reviewer agent. |
| 42 | **response-recap** | Provides plain English summary ONLY after complex multi-step work so the user understands what changed without wading through diffs. |
| 43 | **screenshot-dissector** | Methodical pixel-level screenshot analysis during debugging — catches layout bugs, state issues, console errors, and UI regressions beyond the obvious. |
| 44 | **search-first** | Searches for existing tools and libraries before writing custom code so wheels aren't reinvented. |
| 45 | **senior-dev-mindset** | Ships complete, production-ready features with inferred requirements so nothing needs hand-holding or follow-up. |
| 46 | **skill-manager** | Prevents skill overload — enforces weight classes (passive/light/heavy), skill cap, resolves conflicts, and detects overthinking. |
| 47 | **smart-clarify** | Asks structured multiple-choice questions instead of open-ended ones so ambiguity resolves in one round, not three. |
| 48 | **spec-interview** | Interviews the user about a feature before writing any code, producing a reusable SPEC.md artifact. |
| 49 | **strategic-compact** | Suggests context compaction at logical task boundaries so important context survives rather than being arbitrarily truncated. |
| 50 | **systematic-debugging** | Root-cause-first debugging methodology so bugs are actually fixed, not band-aided. |
| 51 | **take-your-time** | Matches effort to prompt complexity — a 20-bullet spec gets 20 careful implementations, not one rushed pass. Prevents AI slop by treating each requirement as its own unit of work. |
| 52 | **task-router** | Automatically routes tasks to Opus or Sonnet based on complexity — Opus for debugging/planning/strategy, Sonnet for execution/simple edits/following plans. |
| 53 | **test-driven-development** | RED-GREEN-REFACTOR cycle for business logic so code is tested from the start, not as an afterthought. |
| 54 | **think-efficiently** | Before every action, checks if it will produce new information, if there's a faster path, and if effort is proportional — prevents token-burning non-actions. |
| 55 | **total-recall** | Lazy-loads project context at session start and saves everything at session end — with crash-safe checkpointing and pre-compaction capture. |
| 56 | **user-rules** | Captures and enforces hard constraints the user sets ("max 70 events", "always use X") — persists across sessions, checked before every relevant action. |
| 57 | **using-git-worktrees** | Creates isolated git worktrees for feature work so experiments don't risk the current workspace. |
| 58 | **verification-before-completion** | Requires running verification commands and reading output before any success claim — with speed tiers and repeat-bug escalation. |
| 59 | **version-bump** | Automated semantic versioning — determines patch/minor/major from changes, bumps package.json, and formats commit messages with version prefix. |
| 60 | **writing-plans** | Creates comprehensive implementation plans with file mapping and TDD cycles so multi-step work has a roadmap before code is touched. |
| 61 | **z-ai-switch** | Dynamic model routing — maps Haiku in the model picker to GLM-5 via Z AI proxy. No restart needed. Type `/z` for help. |
| 62 | **zero-iteration** | Mentally traces code execution before writing it so bugs are caught in the mind, not in the test suite. |

---

## 🚀 Quick Install

```bash
# Clone this repo
git clone https://github.com/nhouseholder/nicks-claude-code-superpowers.git ~/.claude-tmp

# Install to your Claude Code config
cp -r ~/.claude-tmp/skills ~/.claude/
cp -r ~/.claude-tmp/hooks ~/.claude/
cp -r ~/.claude-tmp/commands ~/.claude/
cp -r ~/.claude-tmp/homunculus ~/.claude/
cp ~/.claude-tmp/CLAUDE.md ~/.claude/
cp ~/.claude-tmp/settings.json ~/.claude/

# Cleanup
rm -rf ~/.claude-tmp
```

---

## 📦 What's Included

### Skills (63 total)

| Category | Skills |
|----------|--------|
| **Thinking & Reasoning** | brainstorming, systematic-debugging, reflexion, fpf-hypotheses, zero-iteration |
| **Autonomy & Completeness** | senior-dev-mindset, proactive-qa, response-recap, smart-clarify, adaptive-voice, predictive-next, process-monitor, expert-lens, mid-task-triage, never-give-up, screenshot-dissector, take-your-time, calibrated-confidence, implicit-preferences, progressive-disclosure, data-consistency-check |
| **Memory & Learning** | continuous-learning-v2, error-memory, pre-debug-check, total-recall, user-rules |
| **Debugging** | systematic-debugging, confusion-prevention, fix-loop, isolate-before-iterate |
| **Coding Quality** | coding-standards, test-driven-development, verification-before-completion, pattern-propagation, opportunistic-improvement, qa-gate, anti-slop |
| **Planning & Execution** | writing-plans, executing-plans, dispatching-parallel-agents, using-git-worktrees, finishing-a-development-branch, spec-interview |
| **Research & Context** | search-first, deep-research, iterative-retrieval, strategic-compact, think-efficiently, precision-reading, codebase-cartographer, content-research-writer |
| **Review & Collaboration** | receiving-code-review |
| **Workflow Automation** | audit, backtest, deploy, fix-loop, parallel-sweep, version-bump, profit-driven-development |
| **Git Intelligence** | git-sorcery |
| **Model Routing** | task-router, z-ai-switch |
| **Meta** | prompt-architect, skill-manager |

### Hooks (4 total)

| Hook | Trigger | Function |
|------|---------|----------|
| improve-prompt.py | UserPromptSubmit | Enriches vague prompts automatically |
| observe.py | PostToolUse | Tracks patterns for instinct-based learning |
| stop-memory-save.py | Stop | Saves learnings at session end |
| track-skill-performance.js | Stop + PostToolUse | Collects skill effectiveness data for `/skill-insights` |

### Commands (9 total)

| Command | Description |
|---------|-------------|
| /audit | Scan for hardcoded secrets and code quality issues |
| /brainstorm | Start brainstorming session |
| /deploy | Full deploy pipeline with rollback |
| /execute-plan | Execute plan with checkpoints |
| /fix-loop | Self-healing CI: test, fix, re-run until green |
| /mem | Memory management (show, save, recall, forget) |
| /skill-insights | Report on which skills help vs hurt |
| /write-plan | Create implementation plan |

---

## 🧠 Key Features

### 1. Continuous Learning
The `continuous-learning-v2` skill automatically learns from your sessions via hooks:
- Tracks tool usage patterns
- Builds instincts with confidence scores
- Promotes high-confidence patterns to full skills
- Project-scoped to prevent cross-contamination

### 2. Prompt Improvement
The `prompt-improver` hook evaluates prompts for clarity:
- Fast-paths clear prompts (short answers, specific commands, detailed requests)
- Only evaluates mid-length ambiguous prompts
- Enriches genuinely vague prompts with research and clarification

### 3. Reflexion Framework
Two reflexion skills for deeper thinking:
- `reflexion-reflect`: Self-critique with complexity triage
- `reflexion-critique`: Multi-perspective review with debate
- `reflexion-memorize`: Curates insights into CLAUDE.md

### 4. First Principles Framework
`fpf-hypotheses` executes complete Abduction-Deduction-Induction cycles:
- Generates competing hypotheses
- Validates with evidence-based trust scores
- Produces documented decisions

### 5. Strategic Compact
Smart context management:
- Suggests compaction at logical boundaries
- Preserves critical context through phase transitions
- Avoids arbitrary auto-compaction

### 6. Context Hydration
Ensures proper context before action:
- Requires reading files before editing
- Checks related dependencies
- Prevents context-blind changes

### 7. Token Awareness
Encourages efficiency:
- Be concise and direct
- Lazy-load context
- Parallelize independent operations
- Avoid unnecessary explanations

### 8. Senior Dev Mindset & Proactive QA
Two always-active skills with scope-matching guardrails:
- `senior-dev-mindset`: Infers unstated requirements, builds complete features, makes independent decisions. Now with **scope discipline** — small request = small response, big request = comprehensive response. Won't turn a 5-minute fix into a 30-minute refactor.
- `proactive-qa`: Walks the user journey, catches edge cases, fixes adjacent issues. Now with **scope matching** — only applies full QA loop to code proportional to the request size.

### 9. Error Memory — Never Repeat Mistakes
Two skills that form a feedback loop:
- `pre-debug-check`: Consults `~/.claude/anti-patterns.md` BEFORE attempting any fix
- `error-memory`: Captures failed approaches and working solutions AFTER debugging
- Persists structured anti-patterns: what failed, why, and what actually works
- Prevents wasting tokens retrying known-bad approaches across sessions

### 10. Barrier Recognition (merged into pre-debug-check)
The `pre-debug-check` skill now includes barrier recognition — detecting familiar patterns mid-execution:
- **Error deja vu**, **approach repetition**, **escalating cascades**, **environment friction**, **framework quirks**
- Stops immediately, announces the pattern, redirects to the documented fix
- Previously a separate always-on skill; now consolidated for cleaner pipeline

### 11. Workflow Automation
Five purpose-built skills for common development workflows:
- `audit`: Scan for hardcoded secrets/API keys, fix by moving to env vars, commit
- `deploy`: Full Cloudflare Pages/Workers pipeline — lint, test, build, deploy, verify, rollback on failure
- `fix-loop`: Self-healing CI — run tests, diagnose, fix source (never tests), re-run until green
- `parallel-sweep`: Launch N headless Claude agents to search parameter spaces in parallel

### 12. Zero Iteration — Bug Prevention
`zero-iteration` mentally executes code before writing it:
- Traces inputs through logic with concrete values
- Catches off-by-one, async timing, type coercion, and shape mismatches
- Three-value test: happy path, empty/zero case, boundary case
- Zero token cost when code is correct — only speaks up when catching a pre-bug

### 13. Adaptive Voice
`adaptive-voice` matches the user's communication energy:
- **Flow state** (short rapid messages) → maximum brevity, code only
- **Learning mode** (why/how questions) → brief explanations with code
- **Frustrated** (caps, "!!!", "this still doesn't work") → calm competence, different approach
- **Collaborative** ("what do you think?") → engage with ideas, share reasoning

### 14. Predictive Next
`predictive-next` anticipates what you need after completing a task:
- One-line suggestion at the end of responses: "Next: want me to add tests?"
- Based on codebase patterns, session history, common workflows
- Never predicts destructive actions or deployments
- Suppresses in flow state — fast-moving users don't need suggestions

### 15. Codebase Cartographer
`codebase-cartographer` builds a mental architecture map at session start:
- Tier 1: From memory + git (near-zero cost, ~80% coverage)
- Tier 2: Targeted reads for current task
- Tier 3: Deep exploration only for complex multi-file tasks
- Knows directory purposes, data flows, conventions, entry points

### 16. Pattern Propagation
`pattern-propagation` ensures consistency when patterns change:
- Rename a function → all call sites, imports, tests, and comments updated
- Change an API shape → all consumers updated
- Grep for the OLD pattern after updating — should return zero results
- Asks before propagating across 10+ files

### 17. Git Sorcery
`git-sorcery` elevates every git interaction:
- Smart commit messages from diffs: `[Action] [What] — [Why/Impact]`
- Intelligent conflict resolution (understand both sides, integrate)
- Bug hunting with bisect
- Branch management and cleanup
- Descriptive stash operations

### 18. Expert Lens — Domain Expert Perspectives
`expert-lens` activates professional-grade thinking for any domain:
- **Explicit**: "You are an expert in X" → activates domain-specific mental models
- **Implicit**: Detects domain from task context and auto-applies the right expert framework
- Loads 4 layers: mental models, domain vocabulary, quality standards, and amateur-mistake avoidance
- ~30-50 tokens per activation — expert framing often makes output SHORTER and more precise

### 19. Mid-Task Triage — Handle Interruptions Without Stopping
`mid-task-triage` classifies new messages that arrive while Claude is working:
- **A) Addendum** — More info for current task → absorb silently, keep working
- **B) Course Correction** — Change direction → pivot with one-line ack, keep working
- **C) Queue** — Different topic → note it, finish current task, then address it
- Never stops to ask "should I continue?" — classification is instant and invisible
- Near-zero token overhead — saves tokens by preventing stop-start cycles

### 20. Command Center — Master Agent Orchestrator
`command-center` turns Claude into the CEO of an AI agent army:
- Automatically decomposes complex tasks into parallel workstreams
- Each agent gets a self-contained brief with its own expert lens
- Agents run in parallel — 3 agents finish in 1/3 the wall-clock time
- Results are integrated, conflicts resolved, and quality-gated before delivery
- Only activates for genuinely decomposable multi-domain tasks (not small fixes)

### 21. Process Monitor
`process-monitor` maintains awareness of background processes:
- Detects port conflicts before starting servers
- Identifies hung processes and zombies
- Reports problems (not status) — zero overhead when everything is normal
- Checks process health when debugging before checking code
- Mentions running processes before session end

---

## 📋 Skill Matrix

| Skill | Trigger | Automatic? |
|-------|---------|-----------|
| adaptive-voice | Every response | Always-on |
| anti-slop | Structured output | Always-on |
| audit | `/audit` or security scan tasks | Manual |
| backtest | `/backtest` or backtest tasks | Manual |
| brainstorming | `/brainstorm` or large+ambiguous scope | Manual |
| calibrated-confidence | Every response | Always-on |
| cleanup-old-files | After major refactors or architecture changes | Automatic |
| codebase-cartographer | Session start | Automatic |
| coding-standards | Active | Always-on |
| confusion-prevention | Confusion signals detected | Always-on |
| content-research-writer | Writing tasks requiring research | Manual |
| continuous-learning-v2 | Every tool call | Automatic (hook) |
| data-consistency-check | Any data display or stats output | Always-on |
| deep-research | Unfamiliar concepts | Automatic |
| deploy | `/deploy` or deploy tasks | Manual |
| dispatching-parallel-agents | 2+ independent tasks | Automatic |
| error-memory | After fix found | Automatic |
| executing-plans | `/execute-plan` | Manual |
| expert-lens | Domain detection or "you are an expert in..." | Always-on |
| finishing-a-development-branch | Branch completion | Automatic |
| fix-loop | `/fix-loop` or test failures | Manual |
| fpf-hypotheses | Complex decisions | Manual |
| git-sorcery | Git operations | Always-on |
| implicit-preferences | Repeated user corrections | Always-on |
| isolate-before-iterate | Before running full pipeline to debug | Automatic |
| iterative-retrieval | Subagent context loading | Automatic |
| mid-task-triage | New message arrives mid-task | Always-on |
| never-give-up | Integration failure of validated idea | Automatic |
| opportunistic-improvement | Files already being touched | Automatic |
| parallel-sweep | Parameter sweeps | Manual |
| pattern-propagation | Pattern changes | Automatic |
| pre-debug-check | Before debugging | Automatic |
| precision-reading | Large file reads | Automatic |
| predictive-next | After task completion | Automatic |
| proactive-qa | After implementation | Always-on |
| process-monitor | Background processes | Automatic |
| profit-driven-development | Sports prediction directories | Always-on (scoped) |
| progressive-disclosure | Every response | Always-on |
| prompt-architect | Every prompt | Always-on |
| qa-gate | Before feature delivery | Automatic |
| receiving-code-review | Review feedback received | Automatic |
| reflexion | `/reflexion:reflect` or `/reflexion:critique` | Manual |
| response-recap | After complex multi-step work | Automatic |
| screenshot-dissector | Screenshot provided during debugging | Automatic |
| search-first | Before writing custom code | Automatic |
| senior-dev-mindset | Active | Always-on |
| skill-manager | Every message (meta) | Always-on |
| smart-clarify | Ambiguous requests | Automatic |
| spec-interview | Non-trivial new feature request | Automatic |
| strategic-compact | Context growth | Automatic |
| systematic-debugging | Bugs | Automatic |
| take-your-time | Complex multi-item prompts | Always-on |
| task-router | Every message | Always-on |
| test-driven-development | Feature/bugfix implementation | Automatic |
| think-efficiently | Before every action | Always-on |
| total-recall | Session start + end | Always-on |
| user-rules | Hard constraint detected | Always-on |
| using-git-worktrees | Feature work needing isolation | Manual |
| verification-before-completion | Before claiming done | Automatic |
| version-bump | Commits with version changes | Automatic |
| writing-plans | `/write-plan` | Manual |
| z-ai-switch | `/z` or model picker Haiku selection | Manual |
| zero-iteration | Code generation | Always-on |

---

## 🎯 Usage Examples

### Brainstorming
```
/brainstorm I want to add a dark mode toggle
```

### Planning
```
/write-plan Add user authentication with Firebase
```

### Executing Plans
```
/execute-plan
```

### Memory
```
/mem save I prefer Tailwind CSS over CSS-in-JS
/mem recall What's my CSS preference?
/mem show
```

### Deep Thinking
```
/reflexion:reflect That approach seems risky
/fpf:propose-hypotheses Why is the app crashing on iOS?
```

---

## 🔧 Configuration

All configuration in `settings.json`:
- Hook bindings
- Skill directories
- Command mappings

---

## 📚 Sources

This stack aggregates best-in-class skills from:

1. **everything-claude-code** (75.5K stars) - Affaan Mangru
   - strategic-compact, iterative-retrieval, search-first
   - verification-loop, coding-standards
   - continuous-learning, continuous-learning-v2

2. **Context Engineering Kit** (637 stars) - NeoLabHQ
   - reflexion (reflect, critique, memorize)
   - fpf (propose-hypotheses)

3. **Claude Code Superpowers** - Various contributors
   - brainstorming, systematic-debugging
   - writing-plans, executing-plans
   - test-driven-development, verification-before-completion

4. **Custom Skills**
   - context-hydration - Read before edit enforcement
   - token-awareness - Efficiency and conciseness
   - mem - Memory management commands

---

## 🚦 Getting Started

1. Install the skills as shown above
2. Start a new Claude Code session
3. Ask: "What skills do you have?"
4. Try `/mem show` to see memory
5. Try `/brainstorm` for creative work

---

## 📈 What This Improves

| Area | Improvement |
|------|-------------|
| **Prompt following** | Better understanding, fewer misunderstandings |
| **Memory** | Learns your patterns, remembers preferences |
| **Context** | Smart hydration, strategic compaction |
| **Tokens** | Efficient usage, concise responses |
| **Thinking** | Deeper reasoning, self-critique |
| **Code quality** | Standards, testing, verification |
| **Planning** | Structured plans with checkpoints |
| **Debugging** | Systematic methodology |

---

## 🤝 Contributing

This is a personal config but feel free to fork and adapt for your needs!

---

## 📄 License

MIT - Skills are from various sources with their own licenses.

---

**63 skills. 4 hooks. 8 commands. One intelligence stack.**

**Made with ❤️ for smarter AI-assisted development**
