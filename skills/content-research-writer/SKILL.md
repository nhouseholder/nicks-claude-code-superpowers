---
name: content-research-writer
description: Full research + writing assistant. Searches the web, gathers sources, builds outlines, drafts content with citations, and iterates section-by-section. Use for blog posts, articles, documentation, case studies, newsletters, or any structured writing that needs research backing. Triggers on "write an article", "draft a blog post", "research and write", "create content about", or any writing task that requires source material.
---

# Content Research Writer

Research-backed writing from blank page to polished draft. One prompt → researched, cited, structured content.

## When This Fires

- "Write a blog post about X"
- "Draft an article on X"
- "Research and write about X"
- "Create a case study for X"
- "Write documentation for X"
- Any writing task that benefits from web research and citations

## Workflow

### Phase 1: Research (use deep-research patterns)

1. **Clarify scope** — topic, audience, length, tone, format (blog/article/doc/newsletter)
2. **Web search** — 5-10 queries across different angles of the topic
3. **Source collection** — gather key facts, statistics, quotes, expert opinions
4. **Source evaluation** — prioritize: official docs > peer-reviewed > expert blogs > news > forums
5. **Organize findings** — group by subtopic, note source URLs for citations

### Phase 2: Outline

Build a structured outline BEFORE drafting:

```
Title: [working title]
Audience: [who reads this]
Goal: [what the reader should know/do after reading]

1. Hook / Introduction
   - Opening angle: [specific hook]
2. Section: [subtopic]
   - Key points: [from research]
   - Source: [citation]
3. Section: [subtopic]
   ...
N. Conclusion / Call to Action
```

Present outline to user for approval before drafting. Adjust structure based on feedback.

### Phase 3: Draft

- Write section-by-section, not all at once
- After each section, briefly note: sources used, confidence level, areas that need user input
- Use inline citations: `[Source Name](url)` for web sources
- Match the requested tone (technical, conversational, persuasive, educational)
- Hook must grab attention in the first 2 sentences — no throat-clearing

### Phase 4: Review & Polish

Run these checks on the completed draft:

| Check | What to Look For |
|-------|-----------------|
| **Flow** | Does each section lead naturally to the next? |
| **Claims** | Is every factual claim backed by a cited source? |
| **Audience** | Would the target reader understand and care? |
| **Hook** | Would you keep reading after the first paragraph? |
| **Length** | Does it match the requested length? Trim or expand. |
| **Originality** | Is this substantially original, not just paraphrased sources? |

### Phase 5: Deliver

Present the final draft with:
- Sources list at the bottom (numbered, with URLs)
- Word count
- Suggested title alternatives (3 options)
- "Anything you'd like me to revise?" prompt

## Rules

1. **Research before writing** — never draft without sources unless explicitly told to
2. **Cite everything** — every factual claim gets a source; opinions are labeled as such
3. **Outline first** — get structural approval before committing to a full draft
4. **No AI slop** — no generic filler, no "in today's fast-paced world", no placeholder paragraphs
5. **Section-by-section** — write iteratively, not in one monolithic block
6. **User voice** — if the user has a writing style or brand voice, match it
