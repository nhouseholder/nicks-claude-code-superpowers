# Second Brain: Karpathy-Inspired Wiki Pattern
**Source:** Instagram carousel (14 slides), account unknown
**Date captured:** 2026-04-08
**Tags:** knowledge-management, wiki, claude-code

## Content
3-folder pattern: `raw/` (dump sources) → `wiki/` (AI-compiled articles) → `outputs/` (saved Q&A).

Key steps:
1. Create 3 folders — raw/, wiki/, outputs/
2. Dump everything in raw/ unorganized (articles, notes, screenshots)
3. CLAUDE.md schema: what wiki covers, 1 file per topic, link with [[topic]]
4. One prompt: "Read raw/. Compile wiki following CLAUDE.md rules. Create INDEX.md first."
5. Ask questions against wiki, save answers to outputs/
6. Compounding loop: outputs feed back, monthly health check ("flag contradictions, find gaps")

Karpathy quote: "super simple and flat. Just a nested directory of .md files."

## Relevance
Adopted as research-vault skill. raw/ + wiki/ pattern fills gap in our system — we had no frictionless capture for external research that isn't immediately actionable. Skipped outputs/ (handoffs + memory cover that). Skipped per-project wikis (our skills/memory handle domain knowledge).
