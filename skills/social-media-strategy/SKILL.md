---
name: social-media-strategy
description: Build a complete social media strategy OR audit an existing one. Covers brand positioning, content direction, audience targeting, platform strategy, monetization path, and 90-day roadmap. Two modes — BUILD (new presence) and AUDIT (diagnose + fix existing). Triggers on "social media strategy", "social strategy", "strategy audit", "audit my social", "build my brand strategy", "how should I position on social".
weight: heavy
---

# Full Social Media Strategy

Build a complete, actionable social media strategy from a brand context file. Not generic advice — specific, executable strategy tied to the user's business, audience, and goals.

## When This Fires

- "Build my social media strategy"
- "Create a social strategy for [project]"
- "How should I position myself on social media"
- "Audit my social media strategy"
- "Strategy audit"
- Starting a new social media presence from scratch
- Overhauling a stale or unfocused social presence

## Mode Detection

**BUILD mode** — no existing strategy files, or user says "build", "create", "new"
**AUDIT mode** — existing presence, or user says "audit", "review", "diagnose", "what's wrong"

In AUDIT mode, the Strategy Audit phase runs FIRST before any build phases.

## Prerequisites

1. **Read `brand-context.md`** in the current project root. If it doesn't exist, tell the user to copy and fill out `brand-context.template.md` from `~/ProjectsHQ/Ads/`. Do NOT proceed without brand context.
2. **Read project memory** — check for prior strategy decisions, audience insights, or content history.

## Workflow

### Phase 0: Strategy Audit (AUDIT mode only)

When running in AUDIT mode, produce a strategic brief formatted as **diagnosis first, then prescription**:

**Gather context from user** (or brand-context.md):
- Niche, offer, current follower counts per platform
- Monthly revenue, hours/week available for content
- Current posting frequency

**Deliver:**

| Section | What to Provide |
|---------|----------------|
| **Brand positioning** | What makes you distinctly different from 10 competitors |
| **Platform pick** | Which 1-2 platforms fit your offer, audience, and time budget |
| **Content direction** | The 3 angles that resonate most with your audience |
| **90-day roadmap** | Follower milestones, content volume, engagement benchmarks |
| **Monetization path** | How content converts to leads or sales at your current stage |

Format the output as a strategic brief: diagnosis section (what's wrong/missing), then prescription section (what to do).

Save to `strategy-audit.md` in the project root. Then continue to build phases if the user wants a full strategy.

---

### Phase 1: Audit Current State

If the brand has existing social presence:
- What platforms are active?
- What's working (engagement, growth, conversions)?
- What's not working (low reach, wrong audience, no conversions)?
- What's the posting frequency and consistency?

If starting fresh, skip to Phase 2.

### Phase 2: Brand Positioning

Define the brand's social media identity:

1. **Category ownership** — What ONE thing should people associate with this brand?
2. **Positioning statement** — "[Brand] helps [audience] achieve [outcome] by [method], unlike [competitors] who [what they do differently]."
3. **Authority pillars** — 3-5 topics where the brand has genuine expertise or unique perspective
4. **Voice calibration** — Take the brand voice from context and translate it to platform-specific guidelines:
   - Twitter: [tone + constraints]
   - Instagram: [visual style + caption tone]
   - YouTube: [presentation style]
   - TikTok: [format + energy]
   - LinkedIn: [professional angle]

### Phase 3: Audience Targeting

For each platform, define:

| Element | Detail |
|---------|--------|
| **Who** | Specific demographic + psychographic profile |
| **Where** | Which platform features (feed, stories, shorts, spaces) |
| **When** | Best posting times based on audience behavior |
| **Why them** | What problem you solve for THIS specific audience |
| **Trigger** | What event/emotion makes them need you |

### Phase 4: Content Direction

Map content types to the funnel:

| Funnel Stage | Content Type | Goal | Example |
|-------------|-------------|------|---------|
| **Awareness** | Educational, entertaining, controversial takes | Reach new people | "Most [industry] advice is wrong. Here's why..." |
| **Interest** | Behind-the-scenes, process, results | Build curiosity | "I built [X] in 3 days. Here's the full breakdown." |
| **Trust** | Case studies, proof, testimonials, deep dives | Establish authority | "Real results: [specific numbers]" |
| **Conversion** | CTA posts, offers, limited access | Drive action | "Join [X] — here's what you get" |

Ratio recommendation: 40% awareness, 30% trust, 20% interest, 10% conversion.

### Phase 5: Platform Strategy

For each active platform, deliver:

```
PLATFORM: [Name]
POSTING FREQUENCY: [X per week]
CONTENT MIX: [Types and ratios]
KEY FORMATS: [Carousel, thread, reel, etc.]
GROWTH TACTIC: [Platform-specific growth lever]
MONETIZATION ROLE: [How this platform feeds the funnel]
METRICS TO TRACK: [3-5 KPIs]
```

### Phase 6: Monetization Integration

Connect social to revenue:
1. **Primary funnel path** — Platform → [intermediate step] → Revenue
2. **Lead magnets** — What free value captures emails/follows
3. **Conversion events** — What posts/content types drive purchases
4. **Retention loop** — How existing customers become content amplifiers

## Output Format

Deliver as a structured document saved to `social-strategy.md` in the project root. Include:
- Executive summary (3 sentences)
- Positioning statement
- Platform-by-platform playbook
- Content direction matrix
- Monetization funnel map
- 30-day quick-start actions (5 things to do THIS week)

## Rules

1. **No generic advice** — every recommendation must reference something specific from brand-context.md
2. **Platform-specific** — don't give the same advice for every platform
3. **Actionable** — every section ends with "do this" not "consider this"
4. **Anti-slop** — no "in today's digital landscape" filler. Direct, specific, useful.
5. **Realistic** — match posting frequency to what ONE person can actually sustain
6. **Funnel-aware** — every piece of content should have a clear role in the monetization funnel
