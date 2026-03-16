# Nick's Claude Code Superpowers

> A comprehensive intelligence stack for Claude Code — making it smarter, more efficient, better at memory, and more capable.

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

### Skills (61 total)

| Category | Skills |
|----------|--------|
| **Thinking & Reasoning** | brainstorming, systematic-debugging, reflexion-reflect, reflexion-critique, fpf-hypotheses, zero-iteration |
| **Autonomy & Completeness** | senior-dev-mindset, proactive-qa, response-recap, intent-detection, smart-clarify, seamless-resume, adaptive-voice, predictive-next, process-monitor, expert-lens, mid-task-triage |
| **Memory & Learning** | continuous-learning, continuous-learning-v2, reflexion-memorize, mem, error-memory, pre-debug-check, shared-memory, total-recall |
| **Coding Quality** | coding-standards, test-driven-development, verification-before-completion, verification-loop, pattern-propagation |
| **Planning & Execution** | writing-plans, executing-plans, subagent-driven-development, dispatching-parallel-agents, using-git-worktrees, finishing-a-development-branch, command-center |
| **Research & Context** | search-first, deep-research, iterative-retrieval, strategic-compact, context-hydration, token-awareness, precision-reading, parallel-tool-routing, codebase-cartographer |
| **Review & Collaboration** | requesting-code-review, receiving-code-review |
| **Workflow Automation** | backtest, audit, deploy, fix-loop, parallel-sweep |
| **Git Intelligence** | git-sorcery |
| **OpenViking Context DB** | ov-add-data, ov-search-context, ov-server-operate, memory-recall |
| **Meta** | writing-skills, prompt-improver |

### Hooks (4 total)

| Hook | Trigger | Function |
|------|---------|----------|
| improve-prompt.py | UserPromptSubmit | Enriches vague prompts automatically |
| observe.py | PostToolUse | Tracks patterns for instinct-based learning |
| stop-memory-save.py | Stop | Saves learnings at session end |

### Commands (11 total)

| Command | Description |
|---------|-------------|
| /mem show | Show memory contents |
| /mem save [text] | Save to memory |
| /mem recall [topic] | Recall from memory |
| /mem forget [topic] | Forget from memory |
| /brainstorm | Start brainstorming session |
| /write-plan | Create implementation plan |
| /execute-plan | Execute plan with checkpoints |
| /backtest | Run model backtest with baseline comparison |
| /audit | Scan for hardcoded secrets and code quality issues |
| /deploy | Full deploy pipeline with rollback |
| /fix-loop | Self-healing CI: test, fix, re-run until green |

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
- `backtest`: Run model backtests with `| tee`, compare against baseline, commit improvements
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
- **Explicit**: "You are an expert NBA statistician" → activates sports analytics mental models (WAR, regression to the mean, sample size)
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

### 21. OpenViking Context Database
[OpenViking](https://github.com/volcengine/OpenViking) provides persistent, semantic memory across sessions:
- **ov-add-data**: Add resources, files, URLs, and memories to the context database
- **ov-search-context**: Semantic search across all stored memories and resources
- **ov-server-operate**: Install, configure, start/stop the OpenViking server
- **memory-recall**: Recall long-term memories from previous sessions
- **MCP Server**: RAG query/search/add tools via Model Context Protocol
- **Claude Memory Plugin**: Hooks that auto-capture session data and extract memories

---

## 📋 Skill Matrix

| Skill | Trigger | Automatic? |
|-------|---------|-----------|
| brainstorming | `/brainstorm` | Manual |
| systematic-debugging | Bugs | Automatic |
| coding-standards | Active | Always-on |
| token-awareness | Active | Always-on |
| context-hydration | Pre-edit | Automatic |
| search-first | Research tasks | Automatic |
| strategic-compact | Context growth | Automatic |
| verification-before-completion | Completion | Automatic |
| reflexion-reflect | Reflection | Manual |
| reflexion-critique | Review | Manual |
| reflexion-memorize | Learning | Manual |
| fpf-hypotheses | Complex decisions | Manual |
| continuous-learning | Session end | Automatic (hook) |
| continuous-learning-v2 | Every tool call | Automatic (hook) |
| prompt-improver | Ambiguous prompts only | Automatic (hook) |
| senior-dev-mindset | Active | Always-on |
| proactive-qa | Active | Always-on |
| error-memory | After fix found | Automatic |
| pre-debug-check | Before debugging | Automatic |
| ov-add-data | Adding resources | Manual |
| ov-search-context | Searching context | Manual |
| ov-server-operate | Server management | Manual |
| memory-recall | Past session context | Automatic |
| shared-memory | On request | Manual |
| total-recall | Session start + end | Always-on |
| response-recap | After complex multi-step work | Automatic |
| seamless-resume | On "continue" / session resume | Always-on |
| backtest | `/backtest` or backtest tasks | Manual |
| audit | `/audit` or security scan tasks | Manual |
| deploy | `/deploy` or deploy tasks | Manual |
| fix-loop | `/fix-loop` or test failures | Manual |
| parallel-sweep | Coefficient sweeps | Manual |
| zero-iteration | Code generation | Always-on |
| adaptive-voice | Every response | Always-on |
| predictive-next | After task completion | Automatic |
| codebase-cartographer | Session start | Automatic |
| pattern-propagation | Pattern changes | Automatic |
| git-sorcery | Git operations | Always-on |
| process-monitor | Background processes | Automatic |
| expert-lens | "You are an expert in..." or domain detection | Always-on |
| command-center | Complex multi-domain tasks | Automatic |
| mid-task-triage | New message arrives mid-task | Always-on |

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

5. **OpenViking** (volcengine) - Context database for AI agents
   - ov-add-data, ov-search-context, ov-server-operate
   - memory-recall, Claude memory plugin hooks
   - MCP server for RAG query capabilities

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

**61 skills. 3 hooks. 11 commands. One intelligence stack.**

**Made with ❤️ for smarter AI-assisted development**
