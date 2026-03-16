---
name: deep-research
description: Self-directed literature review and expert-level research before implementation. When Claude encounters an unfamiliar concept, statistic, algorithm, technique, or domain — it STOPS, researches extensively from authoritative sources (academic papers, official docs, expert blogs), becomes an expert, identifies alternatives, and makes informed suggestions BEFORE writing any code. Triggers when asked to implement something Claude isn't deeply knowledgeable about, add a new statistical method, integrate an unfamiliar API, or when the user says "research this" or "learn about this first".
---

# Deep Research — Become an Expert Before You Build

When you encounter something you don't deeply understand, STOP. Research it thoroughly from the best sources available. Become the expert. THEN implement.

## Core Principle

**Know what you don't know.** Claude's training data has breadth but not always depth. When asked to implement a specific statistical method, algorithm, technique, or domain concept — assume your knowledge is surface-level until proven otherwise. Research first.

## When to Trigger

### Automatic Triggers (always fire)
- User asks to "add [specific stat/algorithm/technique] to our model"
- User mentions a method/library/approach Claude hasn't used extensively
- User asks about domain-specific concepts (pharmacology, sports analytics, ML techniques)
- The implementation requires understanding mathematical properties, edge cases, or best practices that aren't obvious
- User says "research this", "learn about this", "what's the best way to..."

### Self-Assessment Check
Before implementing ANYTHING technical, ask yourself:
1. Can I explain WHY this method works, not just HOW to code it?
2. Do I know the assumptions and limitations?
3. Do I know when this method is inappropriate?
4. Can I name 2-3 alternatives and explain the tradeoffs?
5. Do I know the common pitfalls and gotchas?

If ANY answer is "no" → trigger deep research before proceeding.

## The Research Protocol

### Phase 1: Scope the Knowledge Gap (2 min)

Identify exactly what you need to learn:
```
TOPIC: [what the user asked about]
WHAT I KNOW: [honest assessment — what do I actually know vs. vaguely recall?]
WHAT I DON'T KNOW: [specific gaps]
KEY QUESTIONS:
1. [most important question to answer]
2. [second most important]
3. [third]
```

### Phase 2: Source Hierarchy Search (5-10 min)

Search in this priority order — always go to the MOST authoritative source first:

#### Tier 1: Primary Sources (gold standard)
- **Academic papers** — search Google Scholar, arXiv, PubMed
- **Official documentation** — the library/framework's own docs
- **Textbooks/references** — authoritative books in the field
- **Standards bodies** — IEEE, W3C, NIST, etc.

Search queries:
```
WebSearch: "[topic] academic paper methodology"
WebSearch: "[topic] official documentation"
WebSearch: "[topic] survey paper comparison"
```

#### Tier 2: Expert Analysis
- **Technical blogs by known experts** — not random Medium posts
- **Conference talks/proceedings** — NeurIPS, ICML, KDD, etc.
- **Stack Overflow accepted answers with 100+ votes**
- **GitHub repos with 1K+ stars** that implement the technique

Search queries:
```
WebSearch: "[topic] best practices 2025 2026"
WebSearch: "[topic] comparison alternatives benchmark"
WebSearch: "[topic] common mistakes pitfalls"
```

#### Tier 3: Community Knowledge (verify against Tier 1-2)
- Blog posts with code examples
- Tutorial sites
- Forum discussions

**NEVER use as sole source.** Always cross-reference with Tier 1-2.

### Phase 3: Deep Read (5-10 min)

For the top 3-5 most relevant sources:
```
WebFetch: [URL] — "Extract the key methodology, assumptions, limitations,
  mathematical formulation, implementation details, and common pitfalls"
```

Take notes on:
- **Core concept** — what is this, precisely?
- **Mathematical foundation** — the actual formula/algorithm
- **Assumptions** — what must be true for this to work?
- **Limitations** — when does this break down?
- **Parameters** — what needs tuning and what are sensible defaults?
- **Alternatives** — what else could solve this problem?
- **Implementation gotchas** — what do people get wrong?

### Phase 4: Synthesize & Present (2 min)

Present findings to the user BEFORE implementing:

```markdown
## Research Summary: [Topic]

### What It Is
[1-2 sentence plain English explanation]

### How It Works
[Core mechanism — enough math to be precise, enough English to be clear]

### When to Use It
- [ideal use case 1]
- [ideal use case 2]

### When NOT to Use It
- [limitation/assumption violation 1]
- [limitation/assumption violation 2]

### Alternatives Considered
| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| [requested method] | ... | ... | ... |
| [alternative 1] | ... | ... | ... |
| [alternative 2] | ... | ... | ... |

### My Recommendation
[Which approach to use and WHY, based on the user's specific context]

### Implementation Plan
[How to add this — what files, what changes, what to test]

### Sources
- [Source 1](url)
- [Source 2](url)
- [Source 3](url)
```

### Phase 5: Get Approval, Then Build

**NEVER implement before presenting the research summary.** Wait for the user to:
- Confirm the approach
- Choose between alternatives
- Add constraints you didn't know about
- Redirect if the research revealed a better path

## Token Economy

Research is valuable but expensive. Stay efficient:

### Budget Your Searches
- **Max 5 WebSearch calls** per research topic — be specific with queries, not broad
- **Max 3 WebFetch calls** — only fetch the most promising sources, not everything
- **Use Grep-style prompts in WebFetch** — ask for specific info, not "summarize everything"
  - BAD: `"Tell me everything about this page"`
  - GOOD: `"Extract: definition, formula, assumptions, limitations, and implementation notes for [topic]"`

### Skip What You Already Know
- If your self-assessment (Phase 1) shows you know 80%+ → do a quick validation search (2 searches max), not a full literature review
- Only go deep on the specific gaps you identified

### Reuse Across the Session
- If you already researched a related topic earlier in the session, reference it — don't re-search
- Save key findings mentally — don't re-fetch the same URL

### Progressive Depth
- Start with 1-2 searches to gauge complexity
- If the topic is straightforward → stop early, present findings
- If the topic is complex/contested → go deeper with remaining budget
- Never use all 5 searches on Phase 2 Tier 3 sources — spend tokens on Tier 1 first

### Research Summary is Compact
- The summary you present should be scannable (bullets, tables, not paragraphs)
- 200-400 words max for the summary — link to sources for depth
- The alternatives table does the heavy lifting — keep everything else tight

## Research Quality Standards

### DO:
- Cross-reference claims across 2+ sources
- Prefer sources with citations, peer review, or strong community validation
- Include the mathematical formulation when relevant
- Note disagreements between sources (science isn't always settled)
- Date-check sources — prefer recent (2023+) for rapidly evolving fields
- Include source URLs so the user can verify

### DON'T:
- Trust a single blog post as gospel
- Skip the alternatives analysis — there's almost always more than one way
- Present training-data knowledge as if you just researched it — be honest about what's from research vs. prior knowledge
- Rush to implementation — the research phase IS the value
- Use sources behind paywalls you can't access — note them and move on

## Domain-Specific Research Guides

### Statistics / ML
- Search: arXiv, Google Scholar, Towards Data Science (verified authors only)
- Always include: assumptions, sample size requirements, distribution requirements
- Always compare: parametric vs non-parametric alternatives

### Pharmacology / Cannabis Science
- Search: PubMed, NCBI, published terpene/cannabinoid research
- Verify: receptor binding data, clinical trial results, peer-reviewed studies
- Cross-reference: multiple studies for any claimed effect

### Sports Analytics
- Search: academic sports science journals, established analytics sites
- Verify: sample sizes, league/era adjustments, backtesting results
- Compare: traditional stats vs advanced metrics vs ML approaches

### Web Development
- Search: official framework docs, MDN, framework maintainer blogs
- Verify: browser compatibility, performance benchmarks, security implications
- Check: is there a built-in solution before building custom?

## Integration with Other Skills

```
User asks to implement something
    │
    ├─ deep-research (research first, become expert)
    │       │
    │       ├─ Present findings + alternatives + recommendation
    │       │
    │       └─ User approves approach
    │               │
    │               ├─ brainstorming (design the feature)
    │               ├─ writing-plans (plan the implementation)
    │               └─ executing-plans (build it — now with expert knowledge)
    │
    └─ search-first (checks if code/library already exists)
```

## Rules

1. **Honesty about knowledge gaps** — never pretend to be an expert when you're not
2. **Research before code** — the research summary comes BEFORE any implementation
3. **Authoritative sources only** — Tier 1 > Tier 2 > Tier 3, always
4. **Alternatives are mandatory** — never present only one option
5. **Sources are mandatory** — every claim must have a URL
6. **User approves before implementation** — research is a recommendation, not a decision
7. **Depth over speed** — spending 5 minutes researching saves hours of wrong implementation
8. **Be specific** — "studies show" is useless; "Smith et al. (2024) found X in a sample of N=500" is valuable
