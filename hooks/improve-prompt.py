#!/usr/bin/env python3
"""
Claude Code Agent Router Hook
Routes prompts to COMPOSITE AGENT PROFILES — bundled skill sets
that work together. When the user says "call in the frontend agent,"
Claude spawns an agent briefed with ALL frontend skills' protocols.
"""
import json
import sys
import re

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    sys.exit(1)

prompt = input_data.get("prompt", "")
prompt_lower = prompt.lower().strip()

def output_json(text):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": text
        }
    }
    print(json.dumps(output))

# === COMPOSITE AGENT PROFILES ===
# Named agent bundles with weighted skill priorities
# Priority: which skills to read FIRST (1=highest)

AGENT_PROFILES = {
    "frontend": {
        "name": "Website Design Agent",
        "skills": [
            (1, "website-design-agent", "Unified design agent — 5-phase workflow: Understand → Research (58 brand refs + search.py DB) → Build → Audit (7-pillar + slop detection) → Critique (Nielsen /40 + personas). READ SKILL.md FIRST."),
            (2, "react-best-practices", "40+ performance rules — read relevant rules/ files for the task"),
            (2, "coding-standards", "TypeScript/React patterns and conventions"),
        ],
        "after": "Run Phase 4 (7-pillar audit + slop detection). If slop score 3+ → redesign. Then Phase 5 (Nielsen critique) for quantitative scoring.",
    },
    "backend": {
        "name": "Backend Agent",
        "skills": [
            (1, "senior-backend", "6-step audit: security scan, performance scan, architecture scan + architecture review"),
            (1, "audit", "Invoke /audit for secrets/credential scanning"),
            (2, "coding-standards", "Code quality patterns"),
        ],
        "after": "Follow website-guardian verify protocol after fixes",
    },
    "debugger": {
        "name": "Debugger Agent",
        "skills": [
            (1, "pre-debug-check", "Check anti-patterns.md and recurring-bugs.md FIRST"),
            (1, "systematic-debugging", "Hypothesis → test → fix protocol"),
            (2, "error-memory", "Log bug permanently after fix — root cause + flawed assumption"),
            (2, "website-guardian", "Baseline snapshot before fix, verify after"),
            (2, "fix-loop", "Self-healing CI loop — run tests, fix, re-run until green"),
            (3, "isolate-before-iterate", "Isolate in minimal test before full pipeline"),
            (3, "data-consistency-check", "Validate any numbers/stats before presenting"),
            (3, "screenshot-dissector", "Pixel-level visual bug analysis from screenshots"),
        ],
        "after": "Log to anti-patterns.md via error-memory",
    },
    "reviewer": {
        "name": "Code Review Agent",
        "skills": [
            (1, "code-reviewer", "Automated analysis, security scan, checklist generation"),
            (2, "qa-gate", "Dispatch testing agent for end-to-end verification"),
            (3, "coding-standards", "TypeScript/React/Python patterns and conventions"),
        ],
        "after": "Run qa-gate before declaring review complete",
    },
    "planner": {
        "name": "Planning Agent",
        "skills": [
            (1, "brainstorming", "Lite vs Full brainstorm, complexity gate"),
            (1, "spec-interview", "Gather requirements, produce SPEC.md"),
            (2, "writing-plans", "Write implementation plan before code"),
            (2, "senior-backend", "System design, service boundaries, tech decisions (architecture review protocol)"),
            (3, "executing-plans", "Execute plan with review checkpoints"),
            (3, "deep-research", "Research unfamiliar concepts before planning"),
        ],
        "after": "Output: SPEC.md or PLAN.md artifact",
    },
    "tester": {
        "name": "Testing Agent",
        "skills": [
            (1, "webapp-testing", "Playwright toolkit — with_server.py, decision tree, examples"),
            (1, "test-driven-development", "TDD protocol — test first, implement second"),
            (2, "qa-gate", "Dispatch independent testing agent"),
        ],
        "after": "Take screenshots at all breakpoints for visual regression baseline",
    },
    "designer": {
        "name": "Visual Designer Agent",
        "skills": [
            (1, "canvas-design", "Design philosophy creation → visual expression"),
            (1, "website-design-agent", "Unified design agent — brand refs, expert references, search DB, slop detection, critique framework"),
        ],
        "after": "Output: design philosophy doc + visual artifact (.png/.pdf)",
    },
    "deployer": {
        "name": "Deploy Agent",
        "skills": [
            (1, "deploy", "Invoke /deploy — build, lint, deploy, verify"),
            (2, "website-guardian", "Post-deploy verification checklist"),
            (3, "git-sorcery", "Smart commits, branch management"),
            (3, "version-bump", "Semantic versioning for deploy commits"),
        ],
        "after": "Visual verification of every page after deploy",
    },
    "builder": {
        "name": "Structured Build Agent",
        "skills": [
            (1, "structured-build", "Full pipeline: Research → Strategize → Plan → Execute → Self-Check → Verify → Deploy"),
            (1, "know-what-you-dont-know", "Domain ignorance detector — fires during Research phase"),
            (2, "writing-plans", "Write implementation plan (Phase 3)"),
            (2, "zero-iteration", "Mental execution before writing code (Phase 4-5)"),
            (3, "calibrated-confidence", "Honest confidence calibration throughout"),
        ],
        "after": "Deliver post-change report. If deployed, follow tiered verification from website-guardian.",
    },
}

def format_profile(profile):
    """Format a composite agent profile as an instruction."""
    p = AGENT_PROFILES[profile]
    lines = [f"COMPOSITE AGENT: {p['name']}"]
    lines.append(f"Read these skills' SKILL.md files and follow their protocols (priority order):\n")

    current_pri = 0
    for pri, skill, desc in p["skills"]:
        if pri != current_pri:
            current_pri = pri
            lines.append(f"  Priority {pri}:")
        lines.append(f"    - {skill}: {desc}")

    lines.append(f"\n  After: {p['after']}")
    return "\n".join(lines)

# === ROUTE TABLE ===
# Pattern → (priority, profile_or_instruction)

ROUTES = [
    # --- COMPOSITE AGENT TRIGGERS (user asks for "an agent") ---
    (r"build.?agent|call.?in.*build|structured.?build|full.?pipeline",
     130, "builder"),
    (r"front.?end.?agent|call.?in.*front|bring.?in.*front|front.?end.?team|ui.?agent|design.?agent",
     130, "frontend"),
    (r"back.?end.?agent|call.?in.*back|bring.?in.*back|server.?agent|api.?agent",
     130, "backend"),
    (r"debug.?agent|call.?in.*debug|bring.?in.*debug|fix.?agent",
     130, "debugger"),
    (r"review.?agent|call.?in.*review|bring.?in.*review|code.?review.?agent",
     130, "reviewer"),
    (r"plan.?agent|call.?in.*plan|bring.?in.*architect|architect.?agent",
     130, "planner"),
    (r"test.?agent|call.?in.*test|bring.?in.*test|qa.?agent",
     130, "tester"),
    (r"design.?agent|call.?in.*design|visual.?agent|art.?agent",
     130, "designer"),
    (r"deploy.?agent|call.?in.*deploy|ship.?agent",
     130, "deployer"),

    # --- TASK-BASED TRIGGERS (infer the right agent from the task) ---
    # Complex builds / new features (structured pipeline)
    (r"build.*new|new.*feature|implement.*new|add.*system|create.*system|new.*module|build.*from.*scratch",
     95, "builder"),
    (r"build.*me|implement.*feature|add.*functionality|new.*integration|new.*pipeline",
     90, "builder"),
    (r"add.*to.*algorithm|new.*gate|new.*penalty|new.*factor|algorithm.*change|modify.*algorithm",
     90, "builder"),

    # Audits
    (r"audit.*front|front.*audit|ui.*audit|ux.*audit", 100, "frontend"),
    (r"audit.*back|back.*audit|api.*audit|security.*audit|server.*audit", 100, "backend"),
    (r"full.*audit|site.*audit|audit.*site|audit.*app|comprehensive.*audit",
     110, "_cmd:/site-audit"),

    # Review handoff (READ-ONLY — orient from previous session, NOT write a new one)
    (r"review.*handoff|read.*handoff|pick.*up.*where|orient.*yourself|continue.*from.*last|what.*was.*last.*session",
     130, "_cmd:/review-handoff"),

    # Full handoff (WRITE — generate new handoff at session end)
    (r"full.*handoff|prepare.*handoff|session.*handoff|get.*handoff.*ready|end.*session|wrap.*up.*session|write.*handoff",
     120, "_cmd:/full-handoff"),

    # Redesign
    (r"redesign|rebuild|overhaul|full.*redesign|site.*redesign|makeover",
     110, "_cmd:/site-redesign"),

    # Frontend work
    (r"build.*page|build.*component|create.*page|create.*component|new.*page|add.*page|landing.*page|dashboard",
     90, "frontend"),
    (r"frontend|front.?end|component|ui\b|ux\b|interface|layout|styl|beautif|html|css|react|vue|svelte|next\.?js|tailwind",
     70, "frontend"),

    # Backend work
    (r"backend|back.?end|api|endpoint|server|database|query|migration|graphql|rest|express|postgres|supabase|prisma",
     70, "backend"),

    # Debugging
    (r"site.*broke|page.*broke|display.*wrong|render.*wrong|chart.*broke|table.*broke",
     85, "debugger"),
    (r"\bfix\b|bug|broken|error|crash|failing|not.?working|broke|debug|regress",
     80, "debugger"),

    # Website commands (specific → command, generic → agent)
    (r"update.*site|update.*website|site.*update",
     90, "_cmd:/site-update"),
    (r"debug.*site|site.*debug|debug.*website|website.*debug",
     90, "_cmd:/site-debug"),
    (r"deploy.*site|website|webapp|web.?app|mmalogic|octagonai",
     75, "deployer"),

    # Testing
    (r"test.*app|test.*site|playwright|e2e|end.?to.?end|smoke.?test",
     80, "tester"),

    # Code review
    (r"review|code.?review|pr.?review|check.*code",
     75, "reviewer"),

    # Deploy
    (r"deploy|(?<!\w)ship(?!\w)|release|go.?live|push.?to.?prod|cloudflare|wrangler",
     80, "deployer"),

    # Planning
    (r"\bplan\b|break.*down|roadmap|requirements",
     60, "planner"),

    # Design
    (r"poster|visual|\bart\b|canvas|infographic|banner",
     80, "designer"),
    (r"design.?system|design.?token|theme|color.?palette|typography",
     75, "designer"),

    # Testing
    (r"\btest\b|tdd|coverage|\bspec\b|unit.?test|integration.?test",
     60, "tester"),

    # What's next — strategic advisor
    (r"what.?s.*next|what.*should.*work.*on|out.*of.*ideas|what.*to.*improve|recommendations|what.*needs.*attention",
     90, "_cmd:/whats-next"),

    # Simple commands
    (r"backtest|model.?accuracy|prediction|coefficient|sweep|betting|odds",
     80, "_backtest"),
    (r"\bcommit|git\b|branch|merge|push|pull.?request|\bpr\b",
     50, "_raw:Follow git-sorcery skill protocol"),
    (r"research|learn.?about|how.?does",
     50, "_raw:Use deep-research skill protocol"),
    (r"prompt|llm|ai.?product|\bagent\b|\brag\b",
     60, "_raw:Use deep-research skill for AI/LLM topics"),
    (r"create.*skill|new.*skill|eval.*skill",
     70, "_raw:Use skill-creator SKILL.md protocol"),
    (r"article|blog|write.*content|draft|newsletter",
     60, "_raw:Use content-research-writer skill"),
    (r"powerpoint|slides|deck|\.pptx", 80, "_raw:Use anthropic-skills:pptx"),
    (r"\.pdf|fill.*form|merge.*pdf", 80, "_raw:Use anthropic-skills:pdf"),
    (r"word.?doc|\.docx|memo|letter", 80, "_raw:Use anthropic-skills:docx"),
    (r"spreadsheet|\.xlsx|\.csv|excel", 80, "_raw:Use anthropic-skills:xlsx"),
]

def route(text):
    """Find the best agent route."""
    matches = []
    for pattern, priority, target in ROUTES:
        if re.search(pattern, text, re.IGNORECASE):
            matches.append((priority, target))

    if not matches:
        return None

    matches.sort(key=lambda x: x[0], reverse=True)
    best = matches[0][1]

    # Format based on target type
    if best in AGENT_PROFILES:
        return format_profile(best)
    elif best == "_backtest":
        return (
            "AGENT ROUTE: Invoke /backtest command via Skill tool.\n\n"
            "PRE-COMPUTE GATE (MANDATORY — answer before running ANY backtest):\n"
            "1. CAN MATH ANSWER THIS? Read the threshold/parameter values. Calculate: "
            "does the proposed change cross the decision boundary? If not, report the math — no run needed.\n"
            "2. CAN A 10-LINE SCRIPT ANSWER THIS? Read registry JSON directly, apply change, report result in <5s.\n"
            "3. IS YOUR APPROACH LOCKED? State ONE approach. If you pivot mid-run, STOP — go back to gate.\n\n"
            "ANTI-PATTERN: TRIPLE_PIVOT_NO_PRECOMPUTE — Running full backtests to test hypotheses "
            "that arithmetic could answer in seconds, then pivoting 3+ times. Do the math FIRST."
        )
    elif best.startswith("_cmd:"):
        cmd = best[5:]
        return f"AGENT ROUTE: Invoke {cmd} command via Skill tool."
    elif best.startswith("_raw:"):
        return f"AGENT ROUTE: {best[5:]}"
    return None

# === BYPASS ===
if prompt.startswith("*"):
    output_json(prompt[1:].strip())
    sys.exit(0)
if prompt.startswith("/"):
    output_json(prompt)
    sys.exit(0)
if prompt.startswith("#"):
    output_json(prompt)
    sys.exit(0)

# === CONTINUE ===
continue_signals = ["continue", "go", "keep going", "go on", "proceed", "carry on", "next"]
if prompt_lower in continue_signals:
    output_json(f"""{prompt}

IMPORTANT: If you cannot determine what to continue, or if context feels limited, read the todo list and any plan files to recover state. Do NOT run /compact again if compaction just happened — that creates a loop. If you truly have no context, tell the user: 'Context was lost during compaction. What would you like me to work on?'

ANTI-PIVOT RULES (always active):
- If you're about to change your approach, STOP. Ask: why did the last approach fail? Fix THAT, don't start over.
- If you've already changed approach once this task, you MUST write a 1-sentence plan before trying a third.
- Running the same pipeline twice to debug = WRONG. Isolate the problem in a 10-line script first.
- If arithmetic can answer your question, don't run code. Calculate first.""")
    sys.exit(0)

# === KERNEL quality scoring ===
def kernel_check(text):
    """Score prompt on KERNEL dimensions. Returns list of issues."""
    issues = []
    tl = text.lower()
    words = tl.split()
    wc = len(words)

    # K: Keep simple — overloaded wall of text
    if wc > 60 and "\n" not in text and ":" not in text:
        issues.append("simplify to one clear goal")

    # E: Easy to verify — vague success criteria
    vague_terms = ["better", "improve", "good", "nice", "clean up", "make it look",
                   "engaging", "professional", "more modern", "enhance"]
    if any(v in tl for v in vague_terms):
        issues.append("add success criteria (how to verify?)")

    # R: Reproducible — temporal references
    temporal = ["current trends", "latest", "best practices", "up to date",
                "modern approach", "trending"]
    if any(t in tl for t in temporal):
        issues.append("use specific versions, not temporal refs")

    # N: Narrow scope — multiple unrelated goals
    if tl.count(" and ") + tl.count(" also ") >= 3:
        issues.append("narrow scope — split into separate prompts")

    # E: Explicit constraints — no boundaries on longer prompts
    constraints = ["don't", "not ", "only ", "must ", "no ", "without ",
                   "avoid ", "max ", "limit", "under ", "less than"]
    if not any(c in tl for c in constraints) and wc > 20:
        issues.append("add constraints (what NOT to do)")

    # L: Logical structure — wall of text
    if wc > 30 and not any(m in text for m in [":", "\n", "1.", "2.", "- "]):
        issues.append("add structure: Task / Context / Constraints / Output")

    return issues

# === ROUTING ===
word_count = len(prompt.split())
agent_route = route(prompt_lower)

directive = ""
if agent_route:
    directive = (
        f"\n\n{agent_route}\n\n"
        f"ENFORCEMENT: Follow the agent profile above. "
        f"Read Priority 1 skills' SKILL.md content yourself for context. "
        f"Do NOT skip skills or 'apply principles mentally.' "
        f"Do NOT spawn subagents unless the task genuinely requires parallel independent work.\n\n"
        f"ANTI-PIVOT: If you change approach, diagnose WHY the first failed before trying another. "
        f"2+ pivots without a written reason = you're thrashing. Stop, write a 1-sentence plan, then execute ONE approach."
    )

# KERNEL check — append to directive when prompt fails 3+ criteria
kernel_issues = kernel_check(prompt)
if len(kernel_issues) >= 3:
    issue_list = "; ".join(kernel_issues)
    directive += (
        f"\n\nKERNEL CHECK: Prompt has structural issues that risk wrong-path execution. "
        f"Issues: {issue_list}. "
        "Before executing, mentally restructure: Task (what) → Context (where) → "
        "Constraints (boundaries) → Verify (success check)."
    )

# === FAST-PATH ===
if word_count <= 3 and not agent_route:
    output_json(prompt)
    sys.exit(0)

clear_signals = [
    "fix ", "add ", "update ", "change ", "remove ", "delete ", "create ",
    "implement ", "refactor ", "move ", "rename ", "install ", "deploy ",
    "run ", "test ", "build ", "push ", "commit ", "merge ",
    "show me", "read ", "open ", "check ", "look at", "what is",
    "how do", "why does", "can you", "please ",
]
if any(prompt_lower.startswith(s) for s in clear_signals) or word_count >= 20:
    output_json(prompt + directive)
    sys.exit(0)

if word_count <= 5 and agent_route:
    output_json(prompt + directive)
    sys.exit(0)

# === EVALUATION for ambiguous ===
escaped = prompt.replace("\\", "\\\\").replace('"', '\\"')
wrapped = f"""PROMPT EVALUATION

Original user request: "{escaped}"

PROCEED IMMEDIATELY if clear. If genuinely vague, use prompt-improver skill."""

output_json(wrapped + directive)
sys.exit(0)
