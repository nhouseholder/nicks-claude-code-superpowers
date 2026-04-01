Design variant generation. Creates multiple design directions for a page or component, builds a side-by-side comparison, and applies the chosen variant. Uses parallel agents for variant generation.

## Arguments
- `$ARGUMENTS` = component or page to explore (e.g., "hero section", "pricing page", "/dashboard")
- `--count N` = Number of variants (default: 3, max: 5)

---

## Phase 1: Context Gathering

1. Identify the project and tech stack from `package.json` / project structure
2. Read the target component/page code
3. Read existing design system if one exists (Tailwind config, CSS variables, theme files)
4. If a live URL exists (from `~/Projects/site-to-repo-map.json`), take a screenshot of the current state using Claude in Chrome for reference

Create `_designs/CONTEXT.md`:
```
TARGET: [component/page name]
FILE: [source file path]
TECH_STACK: [React/Next.js/Vue/etc.]
CSS_FRAMEWORK: [Tailwind/CSS modules/etc.]
CURRENT_STATE: [screenshot path or "no live URL"]
DESIGN_TOKENS: [key colors, fonts, spacing from existing config]
```

---

## Phase 2: Variant Generation

Dispatch **3 parallel agents** (or N per --count), each generating a different design direction. Each agent reads `_designs/CONTEXT.md` first.

### Variant A: Minimal / Clean
**Agent prompt:**
> Read `_designs/CONTEXT.md`. You are redesigning this component with a MINIMAL approach. Strip to essentials. More whitespace. Fewer colors. Let the content breathe. Think Apple, Linear, Notion. Write the modified component to `_designs/variant-a/[filename]`. Also create `_designs/variant-a/preview.html` — a standalone HTML file that renders this component with mock data and the project's CSS framework loaded from CDN. Include a brief `_designs/variant-a/RATIONALE.md` explaining your design choices.

### Variant B: Rich / Premium
**Agent prompt:**
> Read `_designs/CONTEXT.md`. You are redesigning this component with a RICH/PREMIUM approach. Add depth, texture, subtle gradients, micro-interactions. Think Stripe, Vercel, premium SaaS. Write the modified component to `_designs/variant-b/[filename]`. Also create `_designs/variant-b/preview.html` and `_designs/variant-b/RATIONALE.md`.

### Variant C: Bold / Creative
**Agent prompt:**
> Read `_designs/CONTEXT.md`. You are redesigning this component with a BOLD/CREATIVE approach. Unexpected layout, strong typography, distinctive color usage, asymmetry. Break conventions tastefully. Think award-winning agency sites. Write the modified component to `_designs/variant-c/[filename]`. Also create `_designs/variant-c/preview.html` and `_designs/variant-c/RATIONALE.md`.

---

## Phase 3: Comparison Board

After all agents complete, build `_designs/comparison.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Design Options — [component name]</title>
  <style>
    body { margin: 0; font-family: system-ui; background: #111; color: #fff; }
    .header { padding: 20px 40px; border-bottom: 1px solid #333; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; padding: 20px; }
    .card { background: #1a1a1a; border-radius: 12px; overflow: hidden; }
    .card h3 { padding: 12px 16px; margin: 0; font-size: 14px; color: #888; text-transform: uppercase; }
    .card iframe { width: 100%; height: 600px; border: none; background: #fff; }
    .actions { padding: 12px 16px; display: flex; gap: 8px; }
    .btn { padding: 8px 16px; border-radius: 6px; border: none; cursor: pointer; font-size: 13px; }
    .btn-pick { background: #22c55e; color: #fff; }
    .btn-iterate { background: #333; color: #fff; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Design Options</h1>
    <p>[component name] — pick a direction or iterate</p>
  </div>
  <div class="grid">
    <!-- One card per variant with iframe loading preview.html -->
  </div>
</body>
</html>
```

Open in browser using `mcp__Claude_in_Chrome__navigate` with `file://` path.

---

## Phase 4: User Choice

Present the variants with their rationales:

```
DESIGN OPTIONS — [component name]
══════════════════════════════════

Variant A: Minimal / Clean
  [2-3 sentence summary from RATIONALE.md]

Variant B: Rich / Premium
  [2-3 sentence summary from RATIONALE.md]

Variant C: Bold / Creative
  [2-3 sentence summary from RATIONALE.md]

Comparison board open in browser.
```

Ask user:
- A) Pick Variant A — apply to codebase
- B) Pick Variant B — apply to codebase
- C) Pick Variant C — apply to codebase
- D) Mix — take elements from multiple variants (describe what you want)
- E) Iterate — refine one variant with feedback

---

## Phase 5: Apply

When user picks a variant:
1. Copy the chosen variant's component code to the actual source file location
2. Verify it builds/renders correctly
3. If live URL exists, verify in browser with Claude in Chrome
4. Commit the change

If user picks "Mix" or "Iterate":
1. Take their feedback
2. Generate a new variant incorporating their notes
3. Show comparison again
4. Repeat until they approve

---

## Phase 6: Clean Up

Keep `_designs/` for reference. The comparison board and rationale files are useful context for future design decisions.

---

## Rules

1. **READ-ONLY until user picks.** Don't modify the real codebase until a variant is chosen.
2. **Preserve the design system.** All variants must use the project's existing CSS framework, color tokens, and typography.
3. **Preview must be self-contained.** Each preview.html loads independently — no project build required.
4. **Rationale matters.** Each variant needs a clear explanation of WHY, not just WHAT changed.
5. **Respect surgical scope.** Only modify the target component/page. Don't touch unrelated files.
