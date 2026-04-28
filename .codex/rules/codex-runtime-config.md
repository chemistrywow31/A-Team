---
name: Codex Runtime Config
description: Map Claude settings and hook concepts to Codex project-local runtime configuration
---

# Codex Runtime Config

## Applicability

- Applies to: `team-architect`, `agent-writer`, and generated multi-agent teams

## Rule Content

### Use Project-Local Codex Configuration

Generated Codex teams must use `teams/{team-name}/.codex/config.toml` as the runtime switch. Do not require users to edit `~/.codex/config.toml` for a generated team to work.

### Register Agents From `.codex/config.toml`

For `multi-agent` teams:

```toml
[features]
multi_agent = true

[agents]
max_threads = 6
max_depth = 1

[agents.coordinator]
description = "Coordinate delegation, quality gates, and delivery."
config_file = "../agents/coordinator.toml"
```

Resolve `config_file` relative to the `.codex/` directory.

### Treat Claude Settings As Non-Portable

Do not generate `.claude/settings.json`, Claude permission allowlists, Claude Agent Teams flags, or Claude hook events for Codex-native output. Convert portable intent as follows:

- settings defaults -> `.codex/config.toml`
- skill discovery -> `.agents/skills/`
- lifecycle bookkeeping -> worklog and optional Codex hooks
- Agent Teams flags -> `[features] multi_agent = true`

### Hooks Are Optional

Codex supports hooks, but generated teams must not depend on hooks for correctness. If hooks are generated, keep them advisory and document the non-hook fallback in `AGENTS.md`.

## Violation Determination

- generated Codex team requires editing `~/.codex/config.toml` -> Violation
- generated Codex package contains `.claude/settings.json` as a runtime requirement -> Violation
- `config_file` paths are written as if they resolve from project root -> Violation
- hooks are required for correctness with no fallback -> Violation
- `multi-agent` team omits `[features] multi_agent = true` -> Violation

## Exceptions

If the user explicitly requests a Claude-compatible or dual-format export, write Claude settings only as compatibility artifacts and keep Codex runtime canonical.
