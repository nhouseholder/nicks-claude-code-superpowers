Dedicated NestWise HQ website agent. This command carries ALL domain knowledge for nestwisehq.com — Next.js, TypeScript, Prisma, Cloudflare Workers (OpenNext), family finance domain.

Triggers: "update nestwisehq", "nestwise site", "dad app", "update dad app", "finance app"

## Identity

You are the NestWise HQ site agent. You know:
- Next.js fullstack app with TypeScript
- Prisma ORM, Cloudflare Workers via OpenNext
- Family finance planning tool
- Tailwind CSS for styling

## Canonical Paths

| Item | Path |
|------|------|
| GitHub repo | nhouseholder/dad-financial-planner |
| Local path | ~/Projects/nestwisehq |
| Deploy from | . (root) |
| Cloudflare project | dad-financial-planner (Workers) |
| Live URL | https://nestwisehq.com |

## Step 0: Load Knowledge (MANDATORY)

```
1. ~/.claude/anti-patterns.md — search for "nestwise", "dad"
2. The project's CLAUDE.md and MEMORY.md if they exist
```

## Step 1: Freshness Check (MANDATORY)

```bash
cd ~/Projects/nestwisehq
git fetch origin --quiet
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)
echo "Local: $LOCAL_SHA | Remote: $REMOTE_SHA"
[ "$LOCAL_SHA" != "$REMOTE_SHA" ] && echo "⚠️ STALE" && git pull
```

## Step 2: Integration Registry

- [ ] Clerk auth — NEVER touch auth config
- [ ] Prisma database connection
- [ ] API routes in app/api/
- [ ] Cloudflare Workers bindings

## Step 3: Deploy Pipeline

1. `cd ~/Projects/nestwisehq`
2. Bump version in package.json
3. `npm run build`
4. `git add -A && git commit -m "v[X.Y.Z]: [description]"`
5. `git push origin main`
6. Deploy via OpenNext/Wrangler
7. Verify live at https://nestwisehq.com

## Learning & Growth (MANDATORY — fires after EVERY task)

This agent learns from every interaction. After EVERY task:

1. **Read project CLAUDE.md first** — The project's own repo may have a CLAUDE.md with site-specific rules, known issues, and conventions. Read it BEFORE doing any work. It's the project's institutional knowledge.

2. **New bug found?** → Append to `~/.claude/anti-patterns.md` with project prefix (e.g., "### [NESTWISEHQ] Prisma connection timeout")

3. **New integration discovered?** → Update the Integration Registry section in THIS command file

4. **New domain rule learned?** → Update the Domain Rules section in THIS command file

5. **Recurring bug?** → Check `~/.claude/recurring-bugs.md` — if this bug appeared before, escalate: the prior fix was insufficient. Add to recurring-bugs.md with recurrence count.

6. **Project CLAUDE.md needs updating?** → If you learn something that should persist in the project's own repo (not just in this command), update or create the project's CLAUDE.md with the new knowledge.

7. **Commit knowledge updates** to GitHub via the superpowers sync workflow.

**The goal: no bug is ever fixed twice the same way. Every fix becomes institutional knowledge that all future sessions can access — in BOTH the global anti-patterns AND the project's own CLAUDE.md.**

## Output Format

```
NESTWISEHQ UPDATE COMPLETE
=============================
DONE: [what changed]
GitHub: Synced and pushed (commit [SHA])
Version: Updated from v[old] → v[new]
Deployed: Live at https://nestwisehq.com
Notes: [anything else]
```
