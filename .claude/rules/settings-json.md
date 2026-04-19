---
name: Settings JSON
description: Define the settings.json template every generated team must include
---

# Settings JSON

## Applicability

- Applies to: `agent-writer`, `team-architect`

## Rule Content

### Every Generated Team Must Include settings.json

Every generated team must include `.claude/settings.json` at the team root. This file captures project-scope configuration: hooks, permissions, env vars, and plugin declarations. Without it, Claude Code falls back to user-level settings, which the team designer cannot control.

### Required Sections

Every generated `settings.json` must contain:

1. `hooks` — baseline hook set per `rules/hooks-integration.md`
2. `permissions` — allow/ask/deny lists scoped to the team's expected operations
3. `env` — environment variables required by the team (e.g., Agent Teams flag)

### Template

```json
{
  "env": {},
  "permissions": {
    "allow": [
      "Bash(mkdir *)",
      "Bash(jq *)",
      "Read",
      "Grep",
      "Glob"
    ],
    "ask": [
      "Bash(curl *)",
      "Bash(rm *)",
      "Write",
      "Edit"
    ],
    "deny": []
  },
  "hooks": {
    "SessionStart": [ /* per hooks-integration.md */ ],
    "UserPromptSubmit": [ /* per hooks-integration.md */ ],
    "PreCompact": [ /* per hooks-integration.md */ ],
    "Stop": [ /* per hooks-integration.md */ ]
  }
}
```

### Agent Teams Mode Configuration

When the team uses Agent Teams mode (per CLAUDE.md deployment section), settings.json must additionally set:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "teammateMode": "in-process"
}
```

Use `"in-process"` as default. Teams may switch to `"tmux"` only when split-pane visibility is critical and the user confirms their terminal supports it.

### Team-Specific Permissions

Beyond the baseline `permissions`, teams must add:

- API write operations the team performs (e.g., `"Bash(curl -X POST *)"` for teams that push to HTTP APIs)
- MCP tool calls the team depends on (e.g., `"mcp__memory__write"`)
- Agent tool itself (teams that dispatch via Agent must allow `"Agent"` or scope it via skills' `allowed-tools`)

Default to `"ask"` for write operations unless the team has explicit user authorization for automation.

### File Locations

- Committed to git: `.claude/settings.json` (project-scope, team defaults)
- Not committed: `.claude/settings.local.json` (user-local overrides, gitignored)

Generated teams only produce `settings.json`. Users create `settings.local.json` at their discretion.

### Precedence

Precedence: Managed (org-wide) > User (`~/.claude/settings.json`) > Project (`.claude/settings.json`) > Local (`.claude/settings.local.json`). Generated team settings operate at project scope — users may override but organizations may force back.

## Violation Determination

- Generated team missing `.claude/settings.json` → Violation
- `settings.json` missing required sections (`hooks`, `permissions`, `env`) → Violation
- Team declares Agent Teams mode in CLAUDE.md but settings.json lacks `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` → Violation
- `permissions.allow` grants destructive operations (`"Bash(rm -rf *)"`, `"Bash(git push --force *)"`) without explicit user instruction → Violation
- `settings.local.json` committed to git (project template should gitignore it) → Violation

## Exceptions

- Teams that run only as subagents of another project (e.g., a sub-team inside A-Team itself) may inherit settings from the parent and omit their own `settings.json`. State the inheritance in CLAUDE.md.

Tradeoff: Explicit settings.json means every generated team ships configuration that may conflict with the user's existing project. Keep the template minimal — add team-specific entries only when the team cannot function without them.
