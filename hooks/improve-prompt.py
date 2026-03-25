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
        "name": "Frontend Agent",
        "skills": [
            (1, "frontend-design", "Anti-slop design, bold aesthetics, UNFORGETTABLE differentiation"),
            (1, "ui-ux-pro-max", "50 styles, accessibility checklist, search scripts for recommendations"),
            (2, "react-best-practices", "40+ performance rules — read relevant rules/ files for the task"),
            (2, "senior-frontend", "Component patterns, state management, bundle optimization"),
            (3, "ui-design-system", "Design token generator — run scripts/design_token_generator.py for tokens"),
            (3, "coding-standards", "TypeScript/React patterns and conventions"),
            (4, "senior-dev-mindset", "Frontend checklist: all states, responsive, accessible, no stubs"),
        ],
        "after": "Verify with webapp-testing Playwright if possible",
    },
    "backend": {
        "name": "Backend Agent",
        "skills": [
            (1, "senior-backend", "6-step audit: security scan, performance scan, architecture scan"),
            (1, "audit", "Invoke /audit for secrets/credential scanning"),
            (2, "senior-architect", "System design, service boundaries, dependency analysis"),
            (3, "senior-dev-mindset", "Backend checklist: validation, auth, error codes, N+1"),
            (3, "coding-standards", "Code quality patterns"),
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
            (1, "reflexion", "Self-assessment + comprehensive review modes"),
            (2, "requesting-code-review", "How to give feedback — spawn review subagent"),
            (2, "receiving-code-review", "How to handle feedback — no performative agreement"),
            (3, "qa-gate", "Dispatch testing agent for end-to-end verification"),
            (3, "verification-before-completion", "Evidence before assertions"),
        ],
        "after": "Run qa-gate before declaring review complete",
    },
    "planner": {
        "name": "Planning Agent",
        "skills": [
            (1, "brainstorming", "Lite vs Full brainstorm, complexity gate"),
            (1, "spec-interview", "Gather requirements, produce SPEC.md"),
            (2, "writing-plans", "Write implementation plan before code"),
            (2, "senior-architect", "System design, service boundaries, tech decisions"),
            (3, "executing-plans", "Execute plan with review checkpoints"),
            (3, "deep-research", "Research unfamiliar concepts before planning"),
            (3, "search-first", "Find existing solutions before building custom"),
            (4, "dispatching-parallel-agents", "Orchestrate parallel work streams"),
            (4, "subagent-driven-development", "Execute plans via subagents"),
            (4, "senior-prompt-engineer", "AI/prompt system design decisions"),
        ],
        "after": "Output: SPEC.md or PLAN.md artifact",
    },
    "tester": {
        "name": "Testing Agent",
        "skills": [
            (1, "webapp-testing", "Playwright toolkit — with_server.py, decision tree, examples"),
            (1, "test-driven-development", "TDD protocol — test first, implement second"),
            (2, "qa-gate", "Dispatch independent testing agent"),
            (3, "verification-before-completion", "Evidence before claiming done"),
        ],
        "after": "Take screenshots at all breakpoints for visual regression baseline",
    },
    "designer": {
        "name": "Visual Designer Agent",
        "skills": [
            (1, "canvas-design", "Design philosophy creation → visual expression"),
            (1, "frontend-design", "Bold aesthetic direction, anti-generic rules"),
            (2, "ui-design-system", "Design token generator for colors/typography/spacing"),
            (2, "ui-ux-pro-max", "Style/palette/font search, accessibility rules"),
        ],
        "after": "Output: design philosophy doc + visual artifact (.png/.pdf)",
    },
    "deployer": {
        "name": "Deploy Agent",
        "skills": [
            (1, "deploy", "Invoke /deploy — build, lint, deploy, verify"),
            (2, "website-guardian", "Post-deploy verification checklist"),
            (2, "site-update-protocol", "UFC/mmalogic-specific deploy checks"),
            (3, "git-sorcery", "Smart commits, branch management"),
            (3, "version-bump", "Semantic versioning for deploy commits"),
            (3, "finishing-a-development-branch", "Branch completion workflow"),
        ],
        "after": "Visual verification of every page after deploy",
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
    # Audits
    (r"audit.*front|front.*audit|ui.*audit|ux.*audit", 100, "frontend"),
    (r"audit.*back|back.*audit|api.*audit|security.*audit|server.*audit", 100, "backend"),
    (r"full.*audit|site.*audit|audit.*site|audit.*app|comprehensive.*audit",
     110, "_cmd:/site-audit"),

    # Handoff (highest priority)
    (r"handoff|hand.?off|prepare.*handoff|session.*handoff|get.*handoff.*ready|end.*session|wrap.*up.*session",
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
    (r"deploy|ship|release|go.?live|push.?to.?prod|cloudflare|wrangler",
     80, "deployer"),

    # Planning
    (r"\bplan\b|break.*down|roadmap|requirements",
     60, "planner"),

    # Design
    (r"poster|visual|art|canvas|infographic|banner",
     80, "designer"),
    (r"design.?system|design.?token|theme|color.?palette|typography",
     75, "designer"),

    # Testing
    (r"\btest|tdd|coverage|spec|unit.?test|integration.?test",
     60, "tester"),

    # Simple commands
    (r"backtest|model.?accuracy|prediction|coefficient|sweep|betting|odds",
     80, "_cmd:/backtest"),
    (r"\bcommit|git\b|branch|merge|push|pull.?request|\bpr\b",
     50, "_raw:Follow git-sorcery skill protocol"),
    (r"research|learn.?about|how.?does",
     50, "_raw:Use deep-research skill protocol"),
    (r"prompt|llm|ai.?product|agent|rag",
     60, "_raw:Read senior-prompt-engineer SKILL.md"),
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
    output_json(f"{prompt}\n\nIMPORTANT: If you cannot determine what to continue, or if context feels limited, run /compact first to free space, then resume.")
    sys.exit(0)

# === ROUTING ===
word_count = len(prompt.split())
agent_route = route(prompt_lower)

directive = ""
if agent_route:
    directive = (
        f"\n\n{agent_route}\n\n"
        f"ENFORCEMENT: Follow the agent profile above. Spawn a general-purpose agent briefed with "
        f"the Priority 1 skills' SKILL.md content. Read Priority 2-3 skills yourself for context. "
        f"Do NOT skip skills or 'apply principles mentally.'"
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
