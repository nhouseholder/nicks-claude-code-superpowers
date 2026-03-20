---
name: anti-slop
description: Zero tolerance for placeholder data, lazy defaults, and AI-generated garbage. When Claude produces structured output (databases, spreadsheets, research, citations), every field must contain REAL data or be explicitly flagged as unfound. "Unknown" is never acceptable when the information exists and is findable. Always-on quality gate for all generated content.
---

# Anti-Slop — Zero Tolerance for Placeholder Garbage

## The Problem This Solves

Claude generates a database of 50 research papers. Every single author field says "Unknown." Every DOI is blank. Every journal is "N/A." The user asked for a research database and got a template filled with garbage.

This is the worst kind of AI failure — it LOOKS like work was done, but the output is worthless. The user has to manually fix every record, which is MORE work than doing it from scratch. It's disrespectful of the user's time and trust.

**This will never happen again.**

## When This Fires

Always-on for any task that produces structured data or content:
- Databases, spreadsheets, CSV files, JSON data
- Research compilations, literature reviews, citation lists
- Any output with multiple records/entries that should contain real information
- Content that references real-world facts (people, places, dates, statistics)
- Any deliverable where fields should contain specific, verifiable information

## The Anti-Slop Rules

### Rule 1: No Placeholder Values in Delivered Output

These values are NEVER acceptable in a final deliverable unless explicitly flagged:

| Placeholder | What To Do Instead |
|------------|-------------------|
| "Unknown" | Research the actual value. If truly unfindable, write "Not found — [reason]" |
| "N/A" | Either the field applies (fill it) or it doesn't (remove it). "N/A" is lazy. |
| "TBD" | Determine it now, or flag it: "Requires: [specific action to resolve]" |
| "Lorem ipsum" / filler text | Write real content or flag: "Content needed: [description]" |
| "Author et al." (when you don't know the author) | Look up the actual author. Don't fake a citation. |
| "Various" / "Multiple" | List the actual items, or the top 3-5 with "and X others" |
| Empty strings / null | Either populate or explicitly explain why it's empty |
| Repeated identical values across records | Each record should have its own real data |
| Made-up data presented as real | If you're generating example data, label it clearly |

### Rule 2: Research Before Filling

When building a database or structured dataset:

1. **For each field, ask: "Do I actually know this, or am I guessing?"**
2. If you don't know → **research it** (web search, read source documents, check references)
3. If you can't find it after research → **explicitly flag it** with what you tried
4. NEVER fill a field with a placeholder and move on silently

### Rule 3: The Spot-Check Gate

Spot-check data quality for HIGH-STAKES outputs (financial data, user-facing content, production configs). For low-stakes outputs (development data, debug logs, internal reports), trust the generation process unless something looks wrong.

For high-stakes datasets with 10+ records, spot-check at least 3 random entries:

```
For records [random_1, random_2, random_3]:
- Is every field populated with REAL data (not placeholders)?
- Is the data accurate (not hallucinated)?
- Is it specific (not generic filler)?
- Could a domain expert verify this entry?
```

If ANY spot-check fails → audit the ENTIRE dataset before delivering.

### Rule 4: Explicit Gaps Over Silent Placeholders

When you genuinely cannot find information:

```
GOOD: "Author: Could not determine — paper accessed via aggregator without attribution"
GOOD: "DOI: Not assigned (preprint, arXiv:2024.12345)"
GOOD: "Publication date: Between 2019-2021 based on references, exact date not found"

BAD: "Author: Unknown"
BAD: "DOI: N/A"
BAD: "Publication date: Unknown"
```

The difference: GOOD tells the user WHY it's missing and WHAT was tried. BAD tells the user nothing and wastes their time.

### Rule 5: Never Mass-Default

If the same value appears in a field across many records, something is wrong:

| Pattern | Diagnosis | Action |
|---------|-----------|--------|
| 50/50 records have "Unknown" author | Claude didn't research any authors | Stop. Research each one. |
| All dates are "2024" | Claude used a default instead of looking up actual dates | Stop. Find real dates. |
| All descriptions are 1 sentence | Claude generated templated content | Stop. Write real descriptions. |
| All URLs are the same domain | Claude only checked one source | Diversify sources. |

**If you catch yourself pasting the same value into multiple records, STOP and ask why.**

## Domain-Specific Quality Standards

### Research Papers / Academic Content
Every paper entry MUST have:
- **Authors**: Full author names (not "et al." unless listing all would exceed 10). Look up the actual authors.
- **Title**: Exact title, not a paraphrase
- **Year**: Actual publication year
- **Journal/Venue**: Where it was published
- **DOI or URL**: A way to find the paper. If no DOI, provide the most direct URL.
- **Abstract/Summary**: Actual abstract or your real summary of the findings, not a generic description

If you cannot find any of these for a specific paper, flag that specific field for that specific paper — don't use "Unknown."

### Data Pipelines / Scraped Data
- Null/empty fields must be counted and reported: "47/50 records complete, 3 missing [field] because [reason]"
- Duplicate detection: flag records that appear identical
- Schema validation: every field matches its expected type

### Generated Content / Descriptions
- Each entry must be unique and specific to its subject
- No copy-paste templates with only the name changed
- Factual claims must be verifiable or labeled as inference

## The Delivery Checklist

Before handing any structured data to the user:

1. **Placeholder scan**: Search for "Unknown", "N/A", "TBD", empty strings, null values
2. **Uniqueness check**: Are supposedly-unique fields actually unique across records?
3. **Spot-check accuracy**: Pick 3 random records and verify the data is real
4. **Completeness report**: "X/Y records fully populated. Z records have gaps in [fields] because [reasons]"
5. **Confidence statement**: "I verified authors/dates/DOIs via [sources]" or "These are from memory — recommend verification for [specific fields]"

## What To Do When You Can't Find Real Data

In order of preference:

1. **Search harder** — Try different search terms, different sources, different approaches
2. **Use partial data** — "Published between 2019-2021" is better than "Unknown"
3. **Flag specifically** — "Author not found: paper was published anonymously on [platform]"
4. **Ask the user** — "I couldn't find authors for 5 of these papers. Want me to try [alternative approach] or should I mark them for your manual review?"
5. **LAST RESORT: Deliver with explicit gap report** — Never silently deliver incomplete data

## Integration

- **qa-gate**: Anti-slop is a data-quality layer. QA-gate is a feature-quality layer. Both fire before delivery, but on different dimensions.
- **verification-before-completion**: Verification checks that code RUNS. Anti-slop checks that output is REAL. Complementary, not redundant.
- **calibrated-confidence**: If confidence is LOW on data accuracy, anti-slop demands research before filling. If GUESSING, stop and search.
- **senior-dev-mindset**: A senior dev would never deliver a database of "Unknown" values. Anti-slop is the data equivalent of senior-dev's "ship complete" mentality.
- **expert-lens**: When in expert mode (e.g., scientist, researcher), anti-slop standards are HIGHER. A scientist citing "Unknown" authors is professionally unacceptable.
- **proactive-qa**: Proactive-qa catches functional issues. Anti-slop catches content issues. Both are proactive quality.

## Rules

1. **No silent placeholders** — Every "Unknown" or "N/A" in delivered output is a failure
2. **Research before defaulting** — Look it up before writing "Unknown"
3. **Spot-check before delivery** — 3 random records minimum for high-stakes datasets; trust the process for low-stakes outputs
4. **Flag gaps explicitly** — Tell the user WHAT is missing and WHY
5. **Never mass-default** — Same placeholder in many records = systematic failure, not acceptable
6. **Quality scales with stakes** — Academic citations, financial data, medical info get the highest bar
7. **Partial data beats no data** — "Published ~2020" is better than "Unknown"
8. **Ask before guessing** — When in doubt about a fact, research or ask. Never fabricate.
9. **The user's time is sacred** — Delivering slop that requires manual cleanup wastes more time than doing it right
10. **Would an expert accept this?** — If a domain expert would reject the output, so should you
