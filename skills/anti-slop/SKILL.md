---
name: anti-slop
description: Zero tolerance for placeholder data in structured output. Every field must be real data or explicitly flagged as unfound. Always-on quality gate.
weight: passive
---

# Anti-Slop — No Placeholder Garbage

## Rules for Structured Output

1. **No silent placeholders** — "Unknown", "N/A", "TBD" are never acceptable without explanation
2. **Research before defaulting** — look it up before writing "Unknown"
3. **Flag gaps explicitly** — "Not found — [reason]" beats "Unknown"
4. **Never mass-default** — same placeholder across many records = systematic failure
5. **Partial data beats no data** — "Published ~2020" beats "Unknown"
6. **Spot-check high-stakes output** — 3 random entries minimum for financial/user-facing data

## What To Do Instead

| Bad | Good |
|-----|------|
| "Author: Unknown" | "Author: Could not determine — paper via aggregator without attribution" |
| "DOI: N/A" | "DOI: Not assigned (preprint, arXiv:2024.12345)" |
| All dates "2024" | Research each actual date |
| Repeated identical values | Each record gets its own real data |
| Made-up data as real | Label clearly as example/generated |

When you can't find data: search harder → use partial data → flag specifically → ask the user → deliver with explicit gap report.
