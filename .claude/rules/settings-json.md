---
name: Settings JSON
description: Define the settings.json template every generated team must include
paths:
  - "teams/**"
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

Copy `.claude/templates/settings-baseline.json` (A-Team repo) as the starting file, then apply the team-specific additions below. Read-trigger: agent-writer must Read that template file before producing any settings.json. The baseline's `hooks` is an EMPTY stub `{}` — replace it entirely with the `hooks` object from `.claude/templates/hooks-baseline.json` per `rules/hooks-integration.md`; shipping the empty stub is a violation. Compliance check: the generated file parses with `jq .`, contains `hooks`, `permissions`, and `env` keys, and `hooks` contains at least the four baseline events.

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

### Permission Bands

The baseline sorts every permission into three bands by blast radius. Keep entries in the matching band:

1. **allow — routine, project-scoped, reversible**: Read/Grep/Glob, Write/Edit on project files, Agent dispatch, WebFetch/WebSearch, safe file ops (ls/mkdir/jq/date/test/tree), local-only git (status/diff/log/add/commit/checkout/worktree). Prompting for routine work trains users to approve reflexively, which destroys the signal of the prompts that matter; local git is reversible via reflog.
2. **ask — externally visible or hard to reverse**: curl/wget transfers, rm, git push, npm/npx installs, API write operations (e.g., `"Bash(curl -X POST *)"`).
3. **deny — irreversible or secret-exposing**: rm -rf variants, force push, reset --hard, clean -fd, pipe-to-shell, chmod -R 777, reads of `.env` / `secrets/**` / `*.pem`.

Scoped overrides beat bare grants: `ask`/`deny` rules match before `allow`, so a team that must gate one directory keeps bare `Write` in allow and adds the scoped gate to ask (e.g., `"Write(profiles/**)"` for fixed-by-design profiles). Never demote bare `Write`/`Edit`/`Agent` to ask — that reintroduces a prompt on every deliverable and every dispatch.

Never allowlist arbitrary execution: interpreter and runner wildcards (`Bash(python3 *)`, `Bash(node *)`, `Bash(bash *)`, `Bash(npm run *)`) are unrestricted code execution. Grant exact-form entries per vetted script instead (e.g., `"Bash(python scripts/cnn_scraper.py *)"`, `"Bash(npm run lint*)"`).

### Team-Specific Permissions

Beyond the baseline `permissions`, teams add allow entries for tools their pipeline actually invokes (e.g., `"Bash(pandoc *)"`, `"Bash(ffprobe *)"`) and MCP tool calls they depend on (e.g., `"mcp__memory__write"`). Default to `"ask"` only for operations with external effect, per the bands above.

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
- `permissions.allow` contains an interpreter, shell, or runner wildcard (`Bash(python3 *)`, `Bash(node *)`, `Bash(bash *)`, `Bash(npm run *)`) → Violation
- Bare `Write`, `Edit`, or `Agent` placed in `ask`/`deny` instead of allow, without a decisions.md entry justifying the gate → Violation
- `settings.local.json` committed to git (project template should gitignore it) → Violation

## Exceptions

- Teams that run only as subagents of another project (e.g., a sub-team inside A-Team itself) may inherit settings from the parent and omit their own `settings.json`. State the inheritance in CLAUDE.md.

Tradeoff: Explicit settings.json means every generated team ships configuration that may conflict with the user's existing project. Keep the template minimal — add team-specific entries only when the team cannot function without them.
