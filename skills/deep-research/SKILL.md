---
name: deep-research
description: Self-directed literature review and expert-level research before implementation. When Claude encounters an unfamiliar concept, statistic, algorithm, technique, or domain — it STOPS, researches extensively from authoritative sources (academic papers, official docs, expert blogs), becomes an expert, identifies alternatives, and makes informed suggestions BEFORE writing any code. Triggers when asked to implement something Claude isn't deeply knowledgeable about, add a new statistical method, integrate an unfamiliar API, or when the user says "research this" or "learn about this first".
weight: heavy
---

# Deep Research — Become an Expert Before You Build

When you encounter something you don't deeply understand, STOP. Research it thoroughly from the best sources available. Become the expert. THEN implement.

**Core Principle:** Assume your knowledge is surface-level until proven otherwise. Research first.

## Research Triage

| Level | Action | Time | Examples |
|-------|--------|------|----------|
| **Routine** | Minimal research — 1 quick validation check | 0 min | Standard patterns with zero domain logic | CRUD, pure UI, config |
| **Familiar** | Quick check (1-2 searches) | 2 min | Pagination, JWT auth, caching |
| **Technical** | Targeted research (3 searches + 1-2 reads) | 5 min | Elo rating, cosine similarity, token bucket |
| **Complex** | Full literature review (5 searches + 3 reads) | 10 min | Bayesian scoring, binding models, recommendation engines |

Signals requiring research: mathematical formulas, domain-specific constants, tradeoff-heavy decisions, safety/accuracy implications, or user explicitly asks.

## The Research Protocol

### Phase 1: Scope the Knowledge Gap (2 min)
Identify: TOPIC, WHAT I KNOW (honest), WHAT I DON'T KNOW (specific gaps), 3 KEY QUESTIONS to answer.

### Phase 2: Source Hierarchy Search (5-10 min)
Search in priority order:
- **Tier 1 (gold):** Academic papers (Scholar, arXiv, PubMed), official docs, textbooks, standards bodies
- **Tier 2 (expert):** Known expert blogs, conference proceedings, SO answers (100+ votes), GitHub repos (1K+ stars)
- **Tier 3 (community):** Blog posts, tutorials, forums — NEVER use as sole source

Sample queries: `"[topic] academic paper methodology"`, `"[topic] best practices 2025"`, `"[topic] comparison alternatives benchmark"`, `"[topic] common pitfalls"`

### Phase 3: Deep Read (5-10 min)
WebFetch top 3-5 sources. Extract: core concept, mathematical foundation, assumptions, limitations, sensible defaults, alternatives, implementation gotchas.

### Phase 4: Synthesize & Present
Present findings BEFORE implementing. Format: **What It Is** (1-2 sentences) → **How It Works** (mechanism + math) → **When to Use / Not Use** (bullets) → **Alternatives Table** (method × pros/cons/best-for) → **Recommendation** (with rationale) → **Implementation Plan** → **Sources** (with URLs).

Keep summary to 200-400 words, scannable bullets/tables.

### Phase 5: Get Approval, Then Build
NEVER implement before presenting research. Wait for user to confirm approach, choose alternatives, or redirect.

## Token Economy

1. **Max 5 WebSearch + 3 WebFetch per topic.** Be specific with queries. Ask WebFetch for targeted info, not "summarize everything."
2. **Validate what you think you know.** 1-2 quick checks even at high confidence. Overconfidence has cost hours.
3. **Reuse within session.** Don't re-search or re-fetch topics/URLs already covered.

## Quality: Cross-reference claims across 2+ sources. Prefer recent (2023+), cited, peer-reviewed sources. Always include source URLs.

## Domain-Specific Guides

| Domain | Search | Always Include |
|--------|--------|----------------|
| **Stats/ML** | arXiv, Google Scholar | Assumptions, sample size reqs, parametric vs non-parametric alternatives |
| **Pharmacology** | PubMed, NCBI | Receptor binding data, clinical trials, cross-referenced effects |
| **Sports Analytics** | Academic journals, analytics sites | Sample sizes, era adjustments, traditional vs advanced vs ML |
| **Web Dev** | Official docs, MDN | Browser compat, perf benchmarks, built-in solutions first |

## Search-First Mode (absorbed from search-first skill)

Before writing ANY utility, helper, or new functionality, quick-check for existing solutions:

1. **Does it already exist in the repo?** → grep through modules/tests
2. **Is it a common problem?** → Search npm/PyPI for maintained packages
3. **Is there an MCP for this?** → Check settings.json and MCP registry
4. **Is there a skill for this?** → Check `~/.claude/skills/`
5. **Is there a GitHub implementation?** → Search for maintained OSS

**Decision matrix:**
| Signal | Action |
|--------|--------|
| Exact match, well-maintained, MIT/Apache | **Adopt** — install and use directly |
| Partial match, good foundation | **Extend** — install + thin wrapper |
| Multiple weak matches | **Compose** — combine 2-3 small packages |
| Nothing suitable found | **Build** — write custom, informed by research |

**Anti-patterns:** Jumping straight to custom code without checking. Installing massive packages for one small feature. Ignoring MCP servers that already provide the capability.

## Rules

1. **Research before code** — summary comes BEFORE any implementation; user approves before you build
2. **Search-first for tools** — check npm/PyPI/MCP/GitHub before writing custom utilities
3. **Authoritative sources** — Tier 1 > Tier 2 > Tier 3; every claim needs a URL
4. **Alternatives are mandatory** — never present only one option
5. **Be specific** — "Smith et al. (2024), N=500" not "studies show"
