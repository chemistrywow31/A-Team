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

Every generated runnable Claude surface must include `.claude/settings.json` at the team root. This captures project-scope hooks, permissions, env vars, and plugin declarations alongside other active settings sources. Do not generate it for Codex-only or reference-only surfaces.

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
  }
}
```

Agent Teams is experimental and distinct from ordinary subagents. Confirm target availability in preflight. The native display default is `in-process`; do not emit a project display override without a team need. A selected `tmux` setup requires a compatible terminal. Preserve existing display preferences. See [Agent Teams](https://code.claude.com/docs/en/agent-teams), checked 2026-10-06.

### Permission Mode And Scope

Probe the selected permission mode; do not infer auto mode from a version number. Deterministic permission rules evaluate deny, then ask, then allow. When auto mode is selected, narrow allow rules remain effective while broad arbitrary-execution grants are suspended; do not claim that every allow rule is ignored or that every config write is necessarily blocked. See [permissions](https://code.claude.com/docs/en/permissions) and [auto-mode configuration](https://code.claude.com/docs/en/auto-mode-config), checked 2026-10-06.

`autoMode` is honored from managed, user, and per-invocation settings, not project or project-local files. Never emit it in a generated project. Describe any actual host restriction and user-applied setup in `docs/RUNTIME-SETUP.md`; do not alter the running session's auto-mode rules, expand permissions, or bypass the host to persist evidence. EC-1.12 provides the bounded coordinator report handoff.

### Permission Bands

These bands govern the deterministic rule set — authoritative when auto mode is off, and still the `deny`/`ask` gate when it is on. The baseline sorts every permission into three bands by blast radius. Keep entries in the matching band:

1. **allow — routine, project-scoped, reversible**: Read/Grep/Glob, Write/Edit on project files, Agent dispatch, WebFetch/WebSearch, safe file ops (ls/mkdir/jq/date/test/tree), local-only git (status/diff/log/add/commit/checkout/worktree). Prompting for routine work trains users to approve reflexively, which destroys the signal of the prompts that matter; local git is reversible via reflog.
2. **ask — externally visible or hard to reverse**: curl/wget transfers, rm, git push, npm/npx installs, API write operations (e.g., `"Bash(curl -X POST *)"`).
3. **deny — irreversible or secret-exposing**: rm -rf variants, force push, reset --hard, clean -fd, pipe-to-shell, chmod -R 777, reads of `.env` / `secrets/**` / `*.pem`.

Scoped overrides beat bare grants: `ask`/`deny` rules match before `allow`, so a team that must gate one directory keeps bare `Write` in allow and adds the scoped gate to ask (e.g., `"Write(profiles/**)"` for fixed-by-design profiles). Never demote bare `Write`/`Edit`/`Agent` to ask — with auto mode off that reintroduces a prompt on every deliverable and every dispatch, and with auto mode on the `ask` entry still fires unconditionally while broad arbitrary-execution `allow` grants may be suspended, so the demotion costs a prompt either way.

Keep the `ask` list to operations a human should decide **every single time**. An entry the team's own pipeline hits on every run does not gate risk — it trains the user to approve reflexively, which is the failure the bands exist to prevent. If the team fetches with `curl` on every run, `curl` belongs in allow with a scoped pattern, not in ask.

Never allowlist arbitrary execution: interpreter and runner wildcards (`Bash(python3 *)`, `Bash(node *)`, `Bash(bash *)`, `Bash(npm run *)`) are unrestricted code execution. Grant exact-form entries per vetted script instead (e.g., `"Bash(python scripts/cnn_scraper.py *)"`, `"Bash(npm run lint*)"`).

### Team-Specific Permissions

Beyond the baseline `permissions`, teams add allow entries for tools their pipeline actually invokes (e.g., `"Bash(pandoc *)"`, `"Bash(ffprobe *)"`) and MCP tool calls they depend on (e.g., `"mcp__memory__write"`). Default to `"ask"` only for operations with external effect, per the bands above.

### File Locations

- Committed to git: `.claude/settings.json` (project-scope, team defaults)
- Not committed: `.claude/settings.local.json` (user-local overrides, gitignored)

Generated teams only produce `settings.json`. Users create `settings.local.json` at their discretion.

One designed exception: the output-mode first-run hook (baseline, `rules/hooks-integration.md`) has the session merge the user's chosen `outputStyle` into `.claude/settings.local.json` — written only as the user's explicit answer to the first-run question. That is a user-preference record, not team configuration, and is legitimate: unlike `autoMode` (above), `outputStyle` IS honored from project-local settings.

### Precedence

For ordinary scalar settings, current precedence is managed > command line/per-invocation > project-local > shared project > user. Permission lists merge across scopes and evaluate deny before ask before allow; do not treat scalar precedence as replacement of all lower-scope lists. Some security-sensitive keys honor a stricter lower-scope value, and environment-variable precedence is key-specific. Verify the effective sources in preflight and preserve user/managed constraints. See [settings precedence](https://code.claude.com/docs/en/settings#settings-precedence), checked 2026-10-06.

## Violation Determination

- Generated runnable Claude surface missing `.claude/settings.json` → Violation
- `settings.json` missing required sections (`hooks`, `permissions`, `env`) → Violation
- Team declares Agent Teams mode in CLAUDE.md but settings.json lacks `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` → Violation
- `permissions.allow` grants destructive operations (`"Bash(rm -rf *)"`, `"Bash(git push --force *)"`) without explicit user instruction → Violation
- `permissions.allow` contains an interpreter, shell, or runner wildcard (`Bash(python3 *)`, `Bash(node *)`, `Bash(bash *)`, `Bash(npm run *)`) → Violation
- Bare `Write`, `Edit`, or `Agent` placed in `ask`/`deny` instead of allow, without a decisions.md entry justifying the gate → Violation
- Generated `settings.json` contains an `autoMode` key → Violation (unsupported project scope; surface applicable user/per-invocation setup via `docs/RUNTIME-SETUP.md`)
- `permissions.ask` contains an operation the team's own documented pipeline invokes on every run, without a decisions.md entry justifying the per-run prompt → Violation
- Any agent writes an `autoMode` block into `~/.claude/settings.json` or any settings file the running session loads → Violation (advise via `docs/RUNTIME-SETUP.md`; the user applies it)
- `settings.local.json` committed to git (project template should gitignore it) → Violation

## Exceptions

- Teams that run only as subagents of another project (e.g., a sub-team inside A-Team itself) may inherit settings from the parent and omit their own `settings.json`. State the inheritance in CLAUDE.md.

Tradeoff: Explicit settings.json means every generated team ships configuration that may conflict with the user's existing project. Keep the template minimal — add team-specific entries only when the team cannot function without them.
