---
name: continuous-learning-v2
version: 2.1.0
---

# Continuous Learning v2.1 — Setup & Reference

An advanced learning system that turns your Claude Code sessions into reusable knowledge through atomic "instincts" - small learned behaviors with confidence scoring.

**v2.1** adds **project-scoped instincts** — React patterns stay in your React project, Python conventions stay in your Python project, and universal patterns (like "always validate input") are shared globally.

## What's New in v2.1

| Feature | v2.0 | v2.1 |
|---------|------|------|
| Storage | Global (~/.claude/homunculus/) | Project-scoped (projects/<hash>/) |
| Scope | All instincts apply everywhere | Project-scoped + global |
| Detection | None | git remote URL / repo path |
| Promotion | N/A | Project → global when seen in 2+ projects |
| Commands | 4 (status/evolve/export/import) | 6 (+promote/projects) |
| Cross-project | Contamination risk | Isolated by default |

## What's New in v2 (vs v1)

| Feature | v1 | v2 |
|---------|----|----|
| Observation | Stop hook (session end) | PreToolUse/PostToolUse (100% reliable) |
| Analysis | Main context | Background agent (Haiku) |
| Granularity | Full skills | Atomic "instincts" |
| Confidence | None | 0.3-0.9 weighted |
| Evolution | Direct to skill | Instincts -> cluster -> skill/command/agent |
| Sharing | None | Export/import instincts |

## Quick Start

### 1. Enable Observation Hooks

Add to your `~/.claude/settings.json`.

**Important:** Use the `Stop` hook (fires once at session end) instead of PreToolUse/PostToolUse (which fire on EVERY tool call and add significant overhead). The Stop hook batches all observations from the session into a single analysis pass.

**If installed as a plugin** (recommended):

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/hooks/observe.sh"
      }]
    }]
  }
}
```

**If installed manually** to `~/.claude/skills`:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh"
      }]
    }]
  }
}
```

> **Migration note:** Previous versions used PreToolUse/PostToolUse hooks for 100% tool call capture. While more comprehensive, this added latency to every single tool call. The Stop hook captures the same patterns with a single batch analysis at session end — dramatically reducing overhead with minimal learning loss.

### 2. Initialize Directory Structure

The system creates directories automatically on first use, but you can also create them manually:

```bash
# Global directories
mkdir -p ~/.claude/homunculus/{instincts/{personal,inherited},evolved/{agents,skills,commands},projects}

# Project directories are auto-created when the hook first runs in a git repo
```

### 3. Use the Instinct Commands

```bash
/instinct-status     # Show learned instincts (project + global)
/evolve              # Cluster related instincts into skills/commands
/instinct-export     # Export instincts to file
/instinct-import     # Import instincts from others
/promote             # Promote project instincts to global scope
/projects            # List all known projects and their instinct counts
```

## Commands

| Command | Description |
|---------|-------------|
| `/instinct-status` | Show all instincts (project-scoped + global) with confidence |
| `/evolve` | Cluster related instincts into skills/commands, suggest promotions |
| `/instinct-export` | Export instincts (filterable by scope/domain) |
| `/instinct-import <file>` | Import instincts with scope control |
| `/promote [id]` | Promote project instincts to global scope |
| `/projects` | List all known projects and their instinct counts |

## Configuration

Edit `config.json` to control the background observer:

```json
{
  "version": "2.1",
  "observer": {
    "enabled": true,
    "run_interval_minutes": 5,
    "min_observations_to_analyze": 20
  }
}
```

Observer is enabled by default. Disable with `enabled: false` in config if token overhead is a concern.

| Key | Default | Description |
|-----|---------|-------------|
| `observer.enabled` | `true` | Enable the background observer agent (disable if token overhead is a concern) |
| `observer.run_interval_minutes` | `5` | How often the observer analyzes observations |
| `observer.min_observations_to_analyze` | `20` | Minimum observations before analysis runs |

Other behavior (observation capture, instinct thresholds, project scoping, promotion criteria) is configured via code defaults in `instinct-cli.py` and `observe.sh`.

## File Structure

All files under `~/.claude/homunculus/`:
- `identity.json` — your profile/technical level
- `projects.json` — registry: project hash -> name/path/remote
- `observations.jsonl` — global observations (fallback)
- `instincts/personal/` — global auto-learned instincts
- `instincts/inherited/` — global imported instincts
- `evolved/{agents,skills,commands}/` — global generated artifacts
- `projects/<hash>/project.json` — per-project metadata
- `projects/<hash>/observations.jsonl` — per-project observations
- `projects/<hash>/instincts/{personal,inherited}/` — project-scoped instincts
- `projects/<hash>/evolved/{skills,commands,agents}/` — project-scoped evolved artifacts

## Backward Compatibility

v2.1 is fully compatible with v2.0 and v1:
- Existing global instincts in `~/.claude/homunculus/instincts/` still work as global instincts
- Existing `~/.claude/skills/learned/` skills from v1 still work
- Stop hook still runs (but now also feeds into v2)
- Gradual migration: run both in parallel

## Related

- [Skill Creator](https://skill-creator.app) - Generate instincts from repo history
- Homunculus - Community project that inspired the v2 instinct-based architecture (atomic observations, confidence scoring, instinct evolution pipeline)
- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - Continuous learning section
