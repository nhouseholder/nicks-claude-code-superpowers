---
name: content-calendar
description: Generate a full 30-day content calendar with daily content ideas, post formats, core message angles, and goals (reach, trust, conversion). Reads from brand context, audience profile, content pillars, and strategy files. Triggers on "content calendar", "30-day plan", "what should I post this month", "content schedule", "monthly content plan".
weight: heavy
---

# 30-Day Content Calendar

Create a full 30-day content calendar with daily content ideas, post format, core message angle, and the goal of each post.

## When This Fires

- "Create my content calendar"
- "30-day content plan"
- "What should I post this month?"
- "Monthly content schedule"
- After content pillars are defined

## Prerequisites (READ ORDER MATTERS)

1. **Read `brand-context.md`** — Required. Do not proceed without it.
2. **Read `content-pillars.md`** — Strongly recommended. If missing, define pillars first or ask user.
3. **Read `audience-profile.md`** — If exists, use messaging angles.
4. **Read `authority-positioning.md`** — If exists, align with positioning.
5. **Read `social-strategy.md`** — If exists, follow platform strategy.

## Workflow

### Phase 1: Calendar Parameters

Confirm with the user:
- **Start date:** [Default: next Monday]
- **Primary platform:** [Where most content goes]
- **Secondary platforms:** [Repurpose targets]
- **Posting frequency:** [Posts per day per platform]
- **Special dates:** [Product launches, events, holidays in the 30-day window]
- **Current focus:** [What the brand is pushing this month — new product? Growth? Community?]

### Phase 2: Content Distribution Rules

Apply pillar ratios across 30 days:

| Pillar | % of Posts | Posts/Month (at 1/day) |
|--------|-----------|----------------------|
| Expertise | 25% | 7-8 |
| Results/Proof | 20% | 6 |
| Process/BTS | 20% | 6 |
| Industry Commentary | 20% | 6 |
| Personal/Relatable | 15% | 4-5 |

Apply goal distribution:

| Goal | % of Posts | Posts/Month |
|------|-----------|------------|
| **Reach** (new eyeballs) | 40% | 12 |
| **Trust** (build credibility) | 35% | 10-11 |
| **Conversion** (drive action) | 25% | 7-8 |

### Phase 3: Generate the Calendar

For each of the 30 days, provide:

```
DAY [N] — [Date] ([Day of Week])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pillar: [Which content pillar]
Format: [Thread | Carousel | Reel | Single post | Video | Story | Poll]
Platform: [Primary platform]
Goal: [Reach | Trust | Conversion]

TOPIC: [Specific topic]
HOOK: "[Opening line that stops the scroll]"
CORE MESSAGE: [The key takeaway in 1-2 sentences]
CTA: [What the reader should do after consuming this]

REPURPOSE TO: [Secondary platform + adjusted format]
```

### Phase 4: Weekly Themes (optional overlay)

If the brand benefits from weekly structure:

| Week | Theme | Focus |
|------|-------|-------|
| Week 1 | [Theme] | Awareness push |
| Week 2 | [Theme] | Authority building |
| Week 3 | [Theme] | Social proof / results |
| Week 4 | [Theme] | Conversion push |

### Phase 5: Calendar Quality Check

Before delivering, verify:
- [ ] All 5 pillars are represented at roughly the right ratios
- [ ] Reach/Trust/Conversion goals are balanced
- [ ] No two consecutive days have the same pillar
- [ ] At least 2 conversion-focused posts per week
- [ ] Hooks are specific, not generic
- [ ] CTAs vary (not every post says "follow for more")
- [ ] Special dates/events are accounted for
- [ ] Weekend content is lighter/more personal (if appropriate)

### Phase 6: Evergreen Posts Bank

Identify 3 evergreen posts that can be reused every 90 days:

```
EVERGREEN POST 1:
Topic: [Universal topic that never goes stale]
Hook: "[Timeless hook]"
Why reusable: [Why this stays relevant]
Best repost months: [When to recycle]

EVERGREEN POST 2: [same format]
EVERGREEN POST 3: [same format]
```

### Phase 7: Week-1 Momentum Priority

Identify which single post from Week 1 to prioritize for maximum early momentum:

```
MOMENTUM POST: Day [N]
Why this one: [Algorithm/audience reasoning]
Boost strategy: [How to amplify — engage in comments, share to stories, cross-post]
Success metric: [What "working" looks like for this post]
```

### Phase 8: Optimal Posting Schedule

Based on platform algorithms and audience behavior:

| Dimension | Recommendation |
|-----------|---------------|
| **Optimal frequency** | [X posts/week for this platform + audience size] |
| **Best days** | [Specific days ranked by engagement potential] |
| **Best times** | [Time windows based on niche audience patterns] |
| **Algorithm notes** | [Platform-specific tips for this content type] |

## Output

Save to `content-calendar-[YYYY-MM].md` in the project root. Structure:
1. Month overview (theme, goals, key dates)
2. Full 30-day calendar table (Date | Format | Topic | Hook | Goal)
3. Weekly summary tables
4. Optimal posting schedule (frequency, days, times)
5. 3 evergreen posts for 90-day recycling
6. Week-1 momentum priority pick
7. Repurposing guide (how to adapt primary content for other platforms)
8. Metrics to track this month

## Rules

1. **30 days, no shortcuts** — every day gets a complete entry
2. **Specific hooks** — "Here's why..." is not a hook. "[Surprising claim] — and I can prove it" is.
3. **No repeat topics** — 30 unique content ideas. Similar themes OK, identical topics not.
4. **Platform-aware formats** — don't suggest carousels for Twitter or threads for TikTok
5. **Conversion isn't just selling** — CTA can be "save this", "DM me", "comment your experience"
6. **Anti-slop** — no filler days. Every entry should be something worth posting.
7. **Sustainable pace** — match frequency to what one person can produce without burnout
8. **Read upstream files** — if content-pillars.md exists, USE those pillars. Don't invent new ones.
