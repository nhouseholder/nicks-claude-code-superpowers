# Claude Code Settings — Superpowers Public Mirror

This repo publicly mirrors **skills**, **hooks**, **commands**, and **anti-patterns.md** from Nicholas Householder's Claude Code configuration.

The full `CLAUDE.md` + `RTK.md` personal instruction files are **intentionally not duplicated here** — they would double the harness's session-start context load in this working directory.

If you're browsing this repo to adapt the setup: everything user-specific (global instructions, model preferences, workflow rules) lives in a single file at `~/.claude/CLAUDE.md` in the owner's personal config. The sharable pieces — skills, hooks, slash commands, anti-patterns — are all present here.

**Owner's own sessions:** the global `~/.claude/CLAUDE.md` auto-loads from the home config directory regardless of `cwd`, so no project context is lost by this thin stub.
