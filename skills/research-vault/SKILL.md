---
name: research-vault
description: Capture raw research (screenshots, articles, tips) and compile into a searchable wiki. Activates when user shares external content for evaluation or asks to review accumulated research.
---

Two modes: **capture** (save raw input) and **compile** (build wiki from raw). Zero cost when not triggered.

## When To Activate

**Capture mode** — trigger when:
- User shares screenshots/articles/tips that contain reusable knowledge (not project-specific code changes)
- User says "save this", "capture this", "add to research", "remember this technique"
- After evaluating external tips (e.g., social media screenshots): if any content was useful, capture it

**Compile mode** — trigger when:
- User says "compile research", "build wiki", "organize research", "what do we know about [topic]"
- Context-saver suggests it (when raw/ has 10+ unprocessed files)

**Do NOT activate when:**
- User shares screenshots that ARE directly actionable (code bugs, UI issues, deploy errors)
- User is working on a specific project task — don't interrupt to suggest capturing
- Raw/ has fewer than 3 files and user didn't explicitly ask to compile

---

## Capture Mode

Extract key content from the user's input (screenshots, text, links) and save to research/raw/:

```bash
VAULT="$HOME/ProjectsHQ/superpowers/research"
DATE=$(date +%Y-%m-%d)
# Filename: YYYY-MM-DD-topic-slug.md
```

**File format (minimal):**
```markdown
# [Topic]
**Source:** [where it came from — account name, URL, or "user-provided"]
**Date captured:** [YYYY-MM-DD]
**Tags:** [2-3 keywords]

## Content
[Extracted key points — not a full transcript, just the actionable knowledge]

## Relevance
[1 sentence: how this could apply to our system]
```

**After saving:** One-line confirmation: "Saved to research/raw/[filename]. [N] items in vault."

Do NOT commit/push on every capture. Batch with the next project commit.

---

## Compile Mode

Read all files in `research/raw/`, generate wiki articles in `research/wiki/`.

### Step 1: Scan raw/
```bash
ls -la "$HOME/ProjectsHQ/superpowers/research/raw/"
```

### Step 2: Read all raw files
Group by tags/topic. Identify clusters.

### Step 3: Generate wiki articles
One .md file per topic in `research/wiki/`:

```markdown
# [Topic Name]
**Last compiled:** [date]
**Sources:** [list of raw/ files that contributed]

## Summary
[Synthesized knowledge from all sources on this topic]

## Key Takeaways
- [Actionable point 1]
- [Actionable point 2]

## See Also
- [[related-topic]]
```

### Step 4: Generate INDEX.md
```markdown
# Research Wiki Index
**Last compiled:** [date] | **Articles:** [N] | **Raw sources:** [N]

## Topics
- [topic-name](topic-name.md) — 1-line summary
```

### Step 5: Commit
```bash
cd "$HOME/ProjectsHQ/superpowers"
git add research/
git commit -m "research: compile wiki — [N] articles from [N] sources"
git push origin main
```

---

## Rules
1. Capture is lightweight — extract, save, move on. Don't over-process raw input.
2. Compile is thorough — cross-reference sources, find contradictions, note gaps.
3. Never duplicate content that belongs in anti-patterns.md, CLAUDE.md, or project skills.
4. If captured content is directly actionable (e.g., a hook improvement), implement it AND capture it.
5. Tags must be consistent across captures for clean compilation.
