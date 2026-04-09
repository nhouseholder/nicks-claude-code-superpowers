# RTK Token Filtering (bestapps.ai)
**Source:** bestapps.ai Instagram post
**Date captured:** 2026-04-08
**Tags:** tokens, rtk, claude-code

## Content
RTK (Rust Token Killer) — CLI proxy that filters command output before Claude sees it. Claims 89% fewer tokens, 3x longer sessions. Examples: cargo test 155 lines → 3 needed, git push 15 lines → 1 needed, npm install hundreds of lines → 0 needed.

## Relevance
Already installed in our system. RTK is hook-integrated via bash-guard.py rewriting. Documented in RTK.md. No changes needed.
