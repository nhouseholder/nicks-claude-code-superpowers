# ============================================================
# ARCHIVED — 2026-03-24
# Reason: Removed from settings.json during token audit (saved ~8K tokens/session)
# Do NOT run this file. Do NOT import from this file.
# Kept for historical reference only.
# ============================================================

#!/usr/bin/env node

/**
 * Skill Performance Tracker — runs on Stop AND NotificationReceived hooks
 *
 * Collects data at:
 * 1. Session end (Stop hook)
 * 2. Compaction events (NotificationReceived — system notifications include compaction)
 * 3. Any point Claude can detect context pressure
 *
 * Appends entries to ~/.claude/skill-tracker.md
 * Analysis happens via /skill-insights command.
 *
 * Hook config (add to settings.json):
 * {
 *   "hooks": {
 *     "Stop": [
 *       { "type": "command", "command": "node ~/.claude/hooks/track-skill-performance.js stop" }
 *     ],
 *     "PostToolUse": [
 *       { "type": "command", "command": "node ~/.claude/hooks/track-skill-performance.js checkpoint" }
 *     ]
 *   }
 * }
 */

const fs = require('fs');
const path = require('path');

const TRACKER_PATH = path.join(process.env.HOME, '.claude', 'skill-tracker.md');
const COUNTER_PATH = path.join(process.env.HOME, '.claude', '.skill-tracker-counter');
const MAX_ENTRIES = 100;
const CHECKPOINT_INTERVAL = 30; // Analyze every 30 tool calls (roughly matches compaction timing)

const triggerType = process.argv[2] || 'stop'; // 'stop' or 'checkpoint'

// Read stdin
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => { input += chunk; });
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);

    // For checkpoint mode: only run every N tool calls
    if (triggerType === 'checkpoint') {
      let count = 0;
      try { count = parseInt(fs.readFileSync(COUNTER_PATH, 'utf8')) || 0; } catch {}
      count++;
      fs.writeFileSync(COUNTER_PATH, String(count));

      if (count % CHECKPOINT_INTERVAL !== 0) {
        process.exit(0); // Not time yet
      }
    }

    // Get transcript from whatever field is available
    const transcript = data.transcript_summary
      || data.stop_hook_active_transcript
      || data.tool_input
      || (data.output ? JSON.stringify(data.output) : '')
      || '';

    const signals = analyzeSession(transcript);

    if (signals.length === 0 && triggerType !== 'stop') {
      process.exit(0);
    }

    // Build entry
    const date = new Date().toISOString().split('T')[0];
    const time = new Date().toTimeString().split(' ')[0].slice(0, 5);
    const label = triggerType === 'stop' ? 'SESSION END' : 'CHECKPOINT';
    let entry = `\n### ${date} ${time} [${label}]\n`;

    if (signals.length === 0) {
      entry += `- No notable signals this period\n`;
    } else {
      for (const signal of signals) {
        entry += `- **${signal.type}**: ${signal.skill} — ${signal.detail}\n`;
      }
    }

    // Read or create tracker
    let existing = '';
    try {
      existing = fs.readFileSync(TRACKER_PATH, 'utf8');
    } catch {
      existing = '# Skill Performance Tracker\n\n> Auto-maintained by track-skill-performance hook.\n> Run /skill-insights to analyze.\n';
    }

    // Trim old entries
    const entries = existing.split('\n### ');
    if (entries.length > MAX_ENTRIES) {
      const header = entries[0];
      const recent = entries.slice(entries.length - MAX_ENTRIES + 1);
      existing = header + '\n### ' + recent.join('\n### ');
    }

    fs.writeFileSync(TRACKER_PATH, existing + entry);

    // Reset counter on session end
    if (triggerType === 'stop') {
      try { fs.unlinkSync(COUNTER_PATH); } catch {}
    }

  } catch (e) {
    process.exit(0); // Silent fail — non-critical
  }
});

function analyzeSession(transcript) {
  const signals = [];
  const t = (typeof transcript === 'string' ? transcript : '').toLowerCase();

  if (!t || t.length < 50) return signals; // Not enough data

  // === HURT signals ===

  // Confusion spirals
  if ((t.match(/let me check/g) || []).length >= 3) {
    signals.push({ type: 'HURT', skill: 'confusion-prevention', detail: '3+ "let me check" — confusion spiral' });
  }
  if ((t.match(/wait —|wait,|actually,/g) || []).length >= 3) {
    signals.push({ type: 'HURT', skill: 'think-efficiently', detail: 'Multiple "wait/actually" — overthinking' });
  }

  // User corrections (most important signal)
  if (t.includes('i already told you') || t.includes('i already said') || t.includes('i told you')) {
    signals.push({ type: 'HURT', skill: 'user-rules', detail: 'User repeated a rule — forgotten or not enforced' });
  }
  if (t.includes('don\'t do that') || t.includes('stop doing') || t.includes('that\'s not what i')) {
    signals.push({ type: 'HURT', skill: 'prompt-architect', detail: 'User corrected approach — intent misread' });
  }
  if (t.includes('why are you') || t.includes('i didn\'t ask')) {
    signals.push({ type: 'HURT', skill: 'prompt-anchoring', detail: 'User questioned relevance — possible drift' });
  }

  // Unverified fixes
  if (t.includes('try now') && (t.includes('still broken') || t.includes('still doesn\'t') || t.includes('still not'))) {
    signals.push({ type: 'HURT', skill: 'qa-gate', detail: '"Try now" + still broken — unverified fix' });
  }

  // Scope creep
  if (t.includes('i just wanted') || t.includes('that\'s too much') || t.includes('keep it simple')) {
    signals.push({ type: 'HURT', skill: 'senior-dev-mindset', detail: 'User felt scope was too large — over-engineering' });
  }

  // Token waste
  if (t.includes('that took too long') || t.includes('too many tokens') || t.includes('why so slow')) {
    signals.push({ type: 'HURT', skill: 'think-efficiently', detail: 'User noted slowness — token waste' });
  }

  // === HELP signals ===

  if (t.includes('perfect') || t.includes('exactly what i wanted') || t.includes('that\'s great') || t.includes('nice work')) {
    signals.push({ type: 'HELP', skill: 'prompt-architect', detail: 'User satisfied with result' });
  }
  if (t.includes('good catch') || t.includes('glad you caught') || t.includes('nice catch')) {
    signals.push({ type: 'HELP', skill: 'proactive-qa', detail: 'Proactive issue detection appreciated' });
  }
  if (t.includes('saved me') || t.includes('that was fast') || t.includes('impressive')) {
    signals.push({ type: 'HELP', skill: 'think-efficiently', detail: 'Speed/efficiency noted' });
  }
  if (t.includes('good question') || t.includes('glad you asked')) {
    signals.push({ type: 'HELP', skill: 'smart-clarify', detail: 'Clarification question was useful' });
  }
  if (t.includes('you remembered') || t.includes('thanks for remembering')) {
    signals.push({ type: 'HELP', skill: 'total-recall', detail: 'Memory persistence noticed and appreciated' });
  }

  // === WARN signals ===

  if ((t.match(/reading file|read file|read tool/g) || []).length >= 10) {
    signals.push({ type: 'WARN', skill: 'precision-reading', detail: '10+ file reads this period' });
  }
  if ((t.match(/agent|subagent|spawn/g) || []).length >= 5) {
    signals.push({ type: 'WARN', skill: 'dispatching-parallel-agents', detail: '5+ agent spawns — check if necessary' });
  }

  return signals;
}
