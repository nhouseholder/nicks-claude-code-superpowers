# Skills Quick Reference — 67 Skills in One Line Each

| # | Skill | What it does & why it matters |
|---|-------|-------------------------------|
| 1 | **adaptive-voice** | Matches the user's energy and pace — terse in flow, detailed when learning, calm when frustrated — so responses always feel natural. |
| 2 | **always-improving** | When the to-do list is empty, suggests the top 1-3 highest-impact project improvements so nothing stagnates. |
| 3 | **anti-slop** | Zero tolerance for placeholder data ("Unknown", "N/A", "TBD") in any deliverable — every field gets real data or an explicit gap explanation so the user never receives AI-generated garbage. |
| 4 | **audit** | Scans codebases for hardcoded secrets, security issues, and anti-patterns so vulnerabilities don't ship. |
| 5 | **brainstorming** | Explores intent, requirements, and design before complex implementations — triggers only when BOTH scope is large AND approach is ambiguous. |
| 7 | **calibrated-confidence** | Makes Claude honest about what it knows vs guesses — dynamically adjusts speed and flags uncertainty so the user knows when to trust and when to verify. |
| 8 | **codebase-cartographer** | Maps codebase architecture with fast-path for documented projects so Claude navigates instantly without redundant exploration. |
| 9 | **coding-standards** | Enforces universal best practices for TypeScript, JavaScript, React, and Node.js so code quality is consistent. |
| 10 | **command-center** | Decomposes complex tasks into parallel subagent workstreams so multi-domain work executes at maximum speed. |
| 11 | **confusion-prevention** | Detects when Claude is confused and forces re-orientation instead of spiraling — prevents the "wait... actually... let me check..." pattern that burns 15+ tool calls. |
| 12 | **context-hydration** | Ensures all relevant files are loaded before edits so Claude never modifies code it hasn't read. |
| 13 | **continuous-learning-v2** | Observes sessions via hooks and creates atomic instincts with confidence scoring so Claude gets smarter over time. |
| 14 | **deep-research** | Stops and researches unfamiliar concepts from authoritative sources before implementing so solutions are expert-level. |
| 15 | **deploy** | Handles full deployment with Cloudflare-specific checks, smoke tests, and auto-rollback so broken code never reaches production. |
| 16 | **dispatching-parallel-agents** | Launches 2+ independent tasks as concurrent subagents so wall-clock time is cut in half (or more). |
| 17 | **error-memory** | Captures failed approaches and working solutions — tracks in-session patterns and token waste, not just cross-session bugs. |
| 18 | **executing-plans** | Executes written implementation plans with review checkpoints so multi-step work stays on track. |
| 19 | **expert-lens** | Activates domain-expert mental models so output meets professional-grade bars. |
| 20 | **finishing-a-development-branch** | Guides branch completion with structured merge/PR/cleanup options so work integrates cleanly. |
| 21 | **fix-loop** | Self-healing CI loop that runs tests, diagnoses, fixes, and re-runs until all pass so broken builds resolve autonomously. |
| 22 | **fpf-hypotheses** | Executes first-principles hypothesis cycles so complex decisions are grounded in evidence, not gut feeling. |
| 23 | **git-sorcery** | Smart commit messages, conflict resolution, bisect, and cherry-pick so git operations are expert-level. |
| 24 | **intent-detection** | Maps natural language to the right skill/command automatically so the user never needs to memorize slash commands. |
| 25 | **isolate-before-iterate** | Before debugging via full pipelines, isolate the suspect logic in a minimal standalone test — prevents 30+ minute feedback loops when a 5-line script would answer in seconds. |
| 26 | **iterative-retrieval** | Progressively refines context retrieval so subagents get exactly the information they need, no more. |
| 27 | **mid-task-triage** | Instantly classifies mid-task messages as addendum, course correction, or queue item — triage runs BEFORE prompt-architect so nothing derails active work. |
| 28 | **never-give-up** | Never abandon a proven-valuable idea because integration failed — uses evidence gate + think-efficiently integration to persist smartly, not stubbornly. |
| 29 | **opportunistic-improvement** | Fixes no-brainer code issues in files already being touched so the project gets cleaner with every interaction. |
| 30 | **parallel-sweep** | Runs parallel parameter sweeps with walk-forward and overfitting guards so optimization finishes in minutes, not hours. |
| 31 | **pattern-propagation** | When a pattern changes in one place, updates ALL instances across the codebase so nothing is left inconsistent. |
| 32 | **pre-debug-check** | Checks known anti-patterns and past failures BEFORE attempting fixes so tokens aren't wasted on dead-end approaches. |
| 33 | **precision-reading** | Grep-first, read-only-relevant-lines so large files don't waste thousands of tokens on irrelevant content. |
| 34 | **predictive-next** | After completing a task, offers the most likely NEXT step in the current workflow — suppresses when always-improving should fire instead. |
| 35 | **proactive-qa** | Walks the user journey after every implementation, catching edge cases and fixing adjacent bugs before you notice. |
| 37 | **process-monitor** | Detects hung processes, port conflicts, and zombie tasks so dev environment issues are caught before they cascade. |
| 38 | **prompt-anchoring** | Keeps Claude anchored to the original prompt objective during long sessions — periodic drift checks prevent "Claude ADHD" without reducing proactivity. |
| 39 | **prompt-architect** | Internally decomposes every prompt into intent, context, scope, and unstated requirements — with anti-inflation rule: never upgrade a simple request into a complex one. |
| 40 | **prompt-improver** | Catches genuinely vague prompts and enriches them with research-based clarifying questions so ambiguity is resolved before work begins. |
| 41 | **qa-gate** | Tiered QA checkpoint before delivering features — from mental trace (Tier 1) to full subagent testing (Tier 3), scaled to change complexity. With bug-fix verification and repeat-bug escalation. |
| 42 | **receiving-code-review** | Evaluates review feedback with technical rigor before implementing so bad suggestions don't degrade code quality. |
| 43 | **reflexion-critique** | Comprehensive single-reviewer code review with Chain-of-Verification so blind spots are caught efficiently. |
| 44 | **reflexion-memorize** | Curates insights from reflections into CLAUDE.md so learnings persist across sessions as permanent guidance. |
| 45 | **reflexion-reflect** | Self-refinement framework — now opt-in by default. Only fires on explicit request, high-risk verification, or 2+ failed bug fixes. |
| 46 | **requesting-code-review** | Dispatches a code-reviewer subagent with precise context so work is independently verified before shipping. |
| 47 | **response-recap** | Provides plain English summary ONLY after complex multi-step work so the user understands what changed without wading through diffs. |
| 48 | **sanity-check** | Flags requests that could break things or waste effort — also evaluates whether proposed new skills are necessary or redundant with existing ones. |
| 49 | **screenshot-dissector** | Methodical pixel-level screenshot analysis during debugging — catches layout bugs, state issues, console errors, and UI regressions beyond the obvious. |
| 50 | **seamless-resume** | On "continue", picks up exactly where it left off — with crash recovery that reads `current_work.md` after disconnects. |
| 51 | **search-first** | Searches for existing tools and libraries before writing custom code so wheels aren't reinvented. |
| 52 | **senior-dev-mindset** | Ships complete, production-ready features with inferred requirements so nothing needs hand-holding or follow-up. |
| 53 | **skill-manager** | Prevents skill overload — enforces weight classes (passive/light/heavy), skill cap, resolves conflicts, and detects overthinking. |
| 55 | **smart-clarify** | Asks structured multiple-choice questions instead of open-ended ones so ambiguity resolves in one round, not three. |
| 56 | **strategic-compact** | Suggests context compaction at logical task boundaries so important context survives rather than being arbitrarily truncated. |
| 57 | **subagent-driven-development** | Executes implementation plans by dispatching independent tasks to subagents so parallel work happens within a single session. |
| 58 | **systematic-debugging** | Root-cause-first debugging methodology so bugs are actually fixed, not band-aided. |
| 59 | **take-your-time** | Matches effort to prompt complexity — a 20-bullet spec gets 20 careful implementations, not one rushed pass. Prevents AI slop on complex work while staying fast on simple tasks. |
| 60 | **test-driven-development** | RED-GREEN-REFACTOR cycle for business logic so code is tested from the start, not as an afterthought. |
| 61 | **think-efficiently** | Before every action, checks if it will produce new information, if there's a faster path, and if effort is proportional — with overthinking test and bias toward action. |
| 62 | **token-awareness** | Makes Claude conscious of token costs so responses and tool usage stay concise and efficient. |
| 63 | **total-recall** | Lazy-loads project context at session start and saves everything at session end — with crash-safe checkpointing and pre-compaction capture. |
| 64 | **user-rules** | Captures and enforces hard constraints the user sets ("max 70 events", "always use X") — persists across sessions, checked before every relevant action. |
| 65 | **using-git-worktrees** | Creates isolated git worktrees for feature work so experiments don't risk the current workspace. |
| 66 | **verification-before-completion** | Requires running verification commands before any success claim — with speed tiers (config=mental trace, single function=quick check, multi-file=full gate) and repeat-bug escalation. |
| 67 | **version-bump** | Automated semantic versioning — determines patch/minor/major from changes, bumps package.json, and formats commit messages with version prefix. |
| 68 | **writing-plans** | Creates comprehensive implementation plans with file mapping and TDD cycles so multi-step work has a roadmap before code is touched. |
| 69 | **zero-iteration** | Mentally traces code execution before writing it so bugs are caught in the mind, not in the test suite. |
