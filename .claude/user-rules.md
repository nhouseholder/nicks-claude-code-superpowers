# Global User Rules
> HARD CONSTRAINTS that apply to ALL projects. Violating a rule is a bug.

## Project Structure
- **Canonical project path**: New project directories are ONLY created at `~/Projects/<name>/` (resolves to `~/Library/Mobile Documents/com~apple~CloudDocs/ProjectsHQ/<name>/`). Never create project directories at `~/iCloud/`, `~/Desktop/`, `/tmp/`, or anywhere else. (set 2026-03-26)

## Deployment
- **Never deploy uncommitted code**: `git status` must show clean working tree before any deploy command. (set 2026-03-25)
- **Never accept missing odds**: If odds are null/"—" for a placed bet, run the scraper. Never display dashes. (set 2026-03-25)

## Communication
- **Permanent response format**: BLUF first line always. Then use the tightest readable structure: compact flat bullets, compact tables, or tiny charts when they improve scan speed. Prose is fallback only. Before every user-facing message, tighten aggressively; drift from BLUF/table-first formatting is a correctness failure. (set 2026-04-12)
- **Use the GitHub Copilot communication rule set as source of truth**: Lead with the answer, strip process narration unless it prevents a mistake, use one short paragraph by default, use lists only when the content is inherently list-shaped, keep progress updates to one sentence when possible, cut repetition/filler/tool-by-tool storytelling/low-value recap, and do a final compression pass. (set 2026-04-11)
- **Apply the same rules during agent work**: User-facing progress updates and working messages must follow the same brevity and scan-speed rules as final answers. (set 2026-04-11)

## Agent Routing (CODE REVIEW ONLY)
- **Discovery before evaluation**: When reviewing a codebase, @explorer MUST run first to map file tree, entry points, dependencies, and tech stack. @auditor receives explorer's output and focuses on evaluation. NEVER ask @auditor to "read key files" or "explore the codebase" — that's @explorer's job. (set 2026-04-21)

## Git & Sync
- **Always sync GitHub after every change**: After any modification to a project (code, config, docs, agents, skills), commit and push to GitHub. No exceptions. GitHub = source of truth. (set 2026-04-19)

## Website Updates (EVERY fix, EVERY time — no exceptions)
After ANY website fix, feature, or change — do ALL of these automatically without the user asking:
1. **Bump version number** in version.js / package.json / wherever the site stores it (patch bump for fixes, minor for features)
2. **Update date tag** on the website (footer, version display, "last updated" — wherever dates appear)
3. **Commit to git** with a clear message describing the change
4. **Push to GitHub** (`git push origin main`)
5. **Deploy live** via the project's deploy method (wrangler, CF Pages, etc.)
6. **Verify deployment** — check the live site to confirm the new version and date are showing
This is NOT optional. Every website change ends with a deployed, verified, version-bumped site. (set 2026-03-26)
