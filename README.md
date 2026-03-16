# Nick's Claude Code Superpowers

> A comprehensive intelligence stack for Claude Code — making it smarter, more efficient, better at memory, and more capable.

## 🚀 Quick Install

```bash
# Clone this repo
git clone https://github.com/yourusername/nicks-claude-code-superpowers.git ~/.claude-tmp

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

### Skills (30 total)

| Category | Skills |
|----------|--------|
| **Thinking & Reasoning** | brainstorming, systematic-debugging, reflexion-reflect, reflexion-critique, fpf-hypotheses |
| **Memory & Learning** | continuous-learning, continuous-learning-v2, reflexion-memorize, mem |
| **Coding Quality** | coding-standards, test-driven-development, verification-before-completion, verification-loop |
| **Planning & Execution** | writing-plans, executing-plans, subagent-driven-development, dispatching-parallel-agents, using-git-worktrees, finishing-a-development-branch |
| **Research & Context** | search-first, iterative-retrieval, strategic-compact, context-hydration, token-awareness |
| **Review & Collaboration** | requesting-code-review, receiving-code-review |
| **Meta** | using-superpowers, writing-skills, prompt-improver |

### Hooks (4 total)

| Hook | Trigger | Function |
|------|---------|----------|
| improve-prompt.py | UserPromptSubmit | Enriches vague prompts automatically |
| observe.py | PostToolUse | Tracks patterns for instinct-based learning |
| stop-memory-save.py | Stop | Saves learnings at session end |

### Commands

| Command | Description |
|---------|-------------|
| /mem show | Show memory contents |
| /mem save [text] | Save to memory |
| /mem recall [topic] | Recall from memory |
| /mem forget [topic] | Forget from memory |
| /brainstorm | Start brainstorming session |
| /write-plan | Create implementation plan |
| /execute-plan | Execute plan with checkpoints |

---

## 🧠 Key Features

### 1. Continuous Learning
The `continuous-learning-v2` skill automatically learns from your sessions via hooks:
- Tracks tool usage patterns
- Builds instincts with confidence scores
- Promotes high-confidence patterns to full skills
- Project-scoped to prevent cross-contamination

### 2. Prompt Improvement
The `prompt-improver` hook fires on every message:
- Detects vague prompts
- Enriches with research and clarification
- Silent when prompt is already clear

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
| prompt-improver | Every message | Automatic (hook) |

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

**Made with ❤️ for smarter AI-assisted development**
