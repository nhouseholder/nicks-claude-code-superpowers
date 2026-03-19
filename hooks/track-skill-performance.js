#!/usr/bin/env node

/**
 * Skill Performance Tracker — runs on Stop hook
 *
 * Appends a session summary to ~/.claude/skill-tracker.md
 * The actual analysis happens in the /skill-insights command.
 * This hook just records what happened.
 *
 * Hook config (settings.json):
 * {
 *   "hooks": {
 *     "Stop": [
 *       { "type": "command", "command": "node ~/.claude/skills/track-skill-performance.js" }
 *     ]
 *   }
 * }
 */

const fs = require('fs');
const path = require('path');

const TRACKER_PATH = path.join(process.env.HOME, '.claude', 'skill-tracker.md');
const MAX_ENTRIES = 100; // Keep last 100 session entries

// Read stdin for stop hook context
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => { input += chunk; });
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    const transcript = data.transcript_summary || data.stop_hook_active_transcript || '';

    // Extract signals from the session
    const signals = analyzeSession(transcript);

    if (signals.length === 0) {
      process.exit(0); // Nothing interesting to track
    }

    // Build entry
    const date = new Date().toISOString().split('T')[0];
    const time = new Date().toTimeString().split(' ')[0].slice(0, 5);
    let entry = `\n### ${date} ${time}\n`;

    for (const signal of signals) {
      entry += `- **${signal.type}**: ${signal.skill} — ${signal.detail}\n`;
    }

    // Append to tracker
    let existing = '';
    try {
      existing = fs.readFileSync(TRACKER_PATH, 'utf8');
    } catch {
      existing = '# Skill Performance Tracker\n\n> Auto-maintained by track-skill-performance hook.\n> Run /skill-insights to analyze.\n';
    }

    // Trim old entries if over limit
    const entries = existing.split('\n### ');
    if (entries.length > MAX_ENTRIES) {
      const header = entries[0];
      const recent = entries.slice(entries.length - MAX_ENTRIES + 1);
      existing = header + '\n### ' + recent.join('\n### ');
    }

    fs.writeFileSync(TRACKER_PATH, existing + entry);

  } catch (e) {
    // Silent fail — tracker is non-critical
    process.exit(0);
  }
});

function analyzeSession(transcript) {
  const signals = [];
  const t = transcript.toLowerCase();

  // Overthinking signals
  if ((t.match(/let me check/g) || []).length >= 3) {
    signals.push({ type: 'HURT', skill: 'confusion-prevention', detail: '3+ "let me check" — confusion spiral detected' });
  }
  if ((t.match(/wait —|wait,|actually/g) || []).length >= 3) {
    signals.push({ type: 'HURT', skill: 'think-efficiently', detail: 'Multiple "wait/actually" — overthinking' });
  }

  // User correction signals
  if (t.includes('i already told you') || t.includes('i already said')) {
    signals.push({ type: 'HURT', skill: 'user-rules', detail: 'User had to repeat a rule — rule was forgotten or not enforced' });
  }
  if (t.includes('don\'t do that') || t.includes('stop doing') || t.includes('that\'s not what i')) {
    signals.push({ type: 'HURT', skill: 'prompt-architect', detail: 'User corrected approach — intent was misread' });
  }
  if (t.includes('try now') && (t.includes('still broken') || t.includes('still doesn\'t'))) {
    signals.push({ type: 'HURT', skill: 'qa-gate', detail: '"Try now" + "still broken" — fix delivered without verification' });
  }

  // Positive signals
  if (t.includes('perfect') || t.includes('exactly what i wanted') || t.includes('that\'s great')) {
    signals.push({ type: 'HELP', skill: 'prompt-architect', detail: 'User expressed satisfaction with result' });
  }
  if (t.includes('good catch') || t.includes('glad you caught')) {
    signals.push({ type: 'HELP', skill: 'proactive-qa', detail: 'User appreciated proactive issue detection' });
  }
  if (t.includes('saved me') || t.includes('that was fast')) {
    signals.push({ type: 'HELP', skill: 'think-efficiently', detail: 'User noted speed/efficiency' });
  }

  // Token waste signals
  if ((t.match(/reading file|read file/g) || []).length >= 10) {
    signals.push({ type: 'WARN', skill: 'precision-reading', detail: '10+ file reads — possible over-reading' });
  }

  return signals;
}
