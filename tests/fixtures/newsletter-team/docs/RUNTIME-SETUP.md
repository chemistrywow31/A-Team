# Runtime setup

Probed: 2026-11-26, Claude Code, no live probe (test fixture).

1. Open this folder as the project in Claude Code.
2. Ask for this week's issue. The `weekly-newsletter` skill loads when the request matches it.
3. Web access goes through WebFetch and WebSearch, which the project settings allow. Nothing else needs configuring.

Rollback: delete `.claude/settings.local.json` to reset the output style choice. The team changes no user-level settings, so there is nothing else to revert.
