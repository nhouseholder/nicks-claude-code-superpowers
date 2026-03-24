---
name: process-monitor
description: Monitor background processes (dev servers, builds, tests, watchers) during a session. Detect hung processes, runaway resource usage, port conflicts, and zombie processes. Provide status updates only when relevant. Kill unnecessary tasks when safe. Low-overhead self-awareness skill.
weight: passive
---

# Process Monitor — Self-Aware Background Process Management

Stay aware of what's running in the background. Dev servers, build watchers, test runners, database processes — know their status, detect problems, and clean up when done. Be the developer who never leaves orphaned processes behind.

## When This Activates

- **After starting any background process** — Track it
- **Before starting a new server/process** — Check for port conflicts
- **When something seems stuck** — Check if a process is hanging
- **Before session end** — Report on running processes
- **When the user reports something slow/broken** — Check process health

## Process Tracking

### Common Processes to Monitor

Watch for: Vite, React, FastAPI, Wrangler, database servers, test watchers, build processes, npm install. Check for: startup completion, crash loops, memory growth, compilation errors, hung/frozen state.

## Problem Detection

### Port Conflicts
Before starting a server:
```
Check: Is the target port already in use?
If yes: Report which process holds it
Suggest: Kill the old process, or use an alternate port
```

### Hung Processes
Signs a process is stuck:
- Build with no output for >60 seconds
- Dev server that started but isn't responding
- Test suite with no progress
- npm install frozen mid-download
- 0% CPU for >30 seconds on a compute-heavy task

Action: Report to the user with the specific symptom. Suggest kill + restart.

**NEVER poll a hung process.** If you check once and see no progress, DIAGNOSE (check CPU%, I/O state, network connections via `lsof -p`) — don't check again in 30 seconds hoping it changed. One diagnostic check replaces 8 status checks.

### Zombie Processes
Processes that should have stopped but didn't:
- Previous dev server still running after session ended
- Build watcher from a different branch
- Multiple instances of the same server

Action: Identify and suggest cleanup.

### Resource Issues
Signs of trouble:
- Process consuming excessive CPU (build loop, infinite re-render)
- Memory growing unbounded (memory leak in dev server)
- Disk filling up (build artifacts, logs)

Action: Report the specific issue and suggest resolution.

## Status Updates

### When to Report (Low Token Overhead)
- **Port conflict detected** — Before the user hits the error
- **Process crashed** — Immediately, with the error
- **Process seems hung** — After reasonable timeout (30s for builds, 5s for servers)
- **Cleanup opportunity** — When you notice orphaned processes

### When NOT to Report
- Process is running normally — don't say "dev server is still running" every response
- Process completed successfully — the output speaks for itself
- User is focused on something else — don't interrupt with process status

### Status Format
When reporting, keep it to one line:

```
⚠ Port 5173 already in use (PID 12345, vite from previous session) — kill it?
```

```
⚠ Build process appears hung (no output for 45s) — restart?
```

## Escalation Rule — Diagnose, Don't Poll

After 2 consecutive status checks with no new output, STOP polling and DIAGNOSE:
1. Check CPU: `ps aux | grep <process>` — is it consuming CPU or idle?
2. Check I/O: `lsof -p <pid>` — is it waiting on network, disk, or stdin?
3. Check logs: read the log file for errors or stuck messages
4. Never poll more than 3 times without diagnosing. Polling without diagnosing is token waste.

## Cleanup Protocol

### Safe to Kill (Do it, mention it)
- Duplicate server instances (same port, same project)
- Build processes that completed
- Test watchers no longer needed
- Processes you started in this session that are done

### Ask Before Killing
- Processes you didn't start
- Servers that might be serving other terminals
- Database processes (could have unsaved state)
- Anything the user might want running

### Session End Awareness
Before a session ends or the user switches context:
```
IF running processes exist that you started:
  → Mention them: "Note: vite dev server still running on :5173"
  → Don't kill them automatically — the user might want them
```

## Pre-Command Checks

Before running commands that depend on services:

```
BEFORE running tests    → Is the test DB running?
BEFORE API calls        → Is the dev server up?
BEFORE deploy           → Are there running dev processes to stop?
BEFORE build            → Kill any dev servers that might conflict
BEFORE long-running scripts → Do required inputs exist? (cache files, data files, configs)
BEFORE iCloud-path scripts  → Will I/O hang? Copy to /tmp first.
```

## Background Task Anti-Patterns

### The Polling Trap
When you start a process with `run_in_background`:
- **DO**: Trust the notification system. Do other work while waiting.
- **DON'T**: Manually check status every 30 seconds. Each check is a wasted tool call.
- **If you must check**: Check ONCE. If no progress, diagnose the root cause immediately (CPU%, I/O, network). Don't check a second time with the same command.

### Pre-Flight for Long-Running Tasks
Before starting any task that takes >60 seconds:
1. **Verify inputs exist** — cache files, data files, API keys
2. **Verify environment** — correct directory, not on iCloud, dependencies installed
3. **Estimate runtime** — tell the user "this will take ~X minutes"
4. **Choose the right path** — if a cache is missing, acknowledge the scraping cost upfront rather than discovering it mid-run

## Rules

1. **Check before starting** — Always check for port conflicts before launching servers
2. **Track what you start** — Know what processes you've spawned this session
3. **Report problems, not status** — Don't announce that everything is fine
4. **Ask before killing others' processes** — Only auto-kill processes you started or obvious zombies
5. **One-line updates** — Process status is infrastructure, not the main event
6. **No polling** — Event-driven checks only. If you check once and see no progress, diagnose — don't check again.
7. **Clean up on exit** — Mention running processes before session end, don't auto-kill
