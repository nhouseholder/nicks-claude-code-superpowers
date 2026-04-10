# RTK — Rust Token Killer (thin stub)

The canonical `RTK.md` instruction file lives at `~/.claude/RTK.md` in the owner's personal config. It's not duplicated here to avoid doubling the harness's session-start context load.

For anyone browsing this repo: RTK is a Rust-based CLI proxy that rewrites common dev commands (`git status`, `wc -l`, etc.) into token-optimized forms, transparently via a hook. It saves 60-90% of tokens on routine shell operations inside Claude Code.
