---
name: Hooks Integration
description: Define the first-run hook every Claude team ships and the worklog hooks a team adds when it keeps a worklog
paths:
  - "teams/**"
---

# Hooks Integration

## Applicability

- Applies to: `agent-writer`, `team-architect`

## Rule Content

### Hooks Follow What The Team Does

Every generated Claude team ships `.claude/settings.json` with the first-run output-mode hook (the `SessionStart` entry with matcher `startup` below). The other four hooks automate worklog bookkeeping. Add them only when the team keeps a worklog; a skill-workflow team normally ships the first-run hook alone.

### Hook Set

| Event | Purpose | Hook type | Blocking? |
|-------|---------|-----------|-----------|
| `SessionStart` | Ensure `.worklog/{yyyymm}/` exists for the current month | `command` | No |
| `SessionStart` (matcher `startup`) | First-run output-mode ask: inject the ask-once instruction when `.claude/settings.local.json` names no `outputStyle`; silent on every later session (`rules/output-structure.md`, Output Mode Component) | `command` | No |
| `UserPromptSubmit` | Log the user's initial request to a session ledger | `command` | No |
| `PreCompact` | Write a compaction checkpoint snapshotting current phase state | `command` | No |
| `Stop` | Warn when the month's worklog directory is missing (advisory; a real triad check is a team-specific addition) | `command` | No (advisory) |

### Template

Copy the entries the team needs verbatim from the `hooks` object in `.claude/templates/hooks-baseline.json` (A-Team repo): the `startup` entry always, the worklog entries when the team keeps a worklog. Read-trigger: agent-writer must Read that file before producing any settings.json. The baseline anchors every path to `"${CLAUDE_PROJECT_DIR:-.}"`, uses `cat` (not `jq`) to capture hook stdin, and suffixes non-blocking commands with `2>/dev/null || true`. Compliance check: the generated settings.json parses with `jq .` and its hook commands contain no bare relative `.worklog/` paths and no `jq` dependency. (Two different execution contexts: hook COMMANDS run in the user's plain shell, so they must not depend on jq. This compliance CHECK runs in the agent's Bash context, where jq is allowlisted and normally present. If jq is unavailable there too, use `python3 -m json.tool` instead.)

### Team-Specific Additions

Beyond the baseline, teams may add hooks for team-specific concerns:

- Teams with external write operations (SiYuan, Notion, HTTP APIs) should add a `PreToolUse` hook with matcher on `Bash(curl *)` or `mcp__*__write.*` to log write attempts
- Teams in Agent Teams mode may add `SubagentStop` or `TeammateIdle` hooks for cross-teammate coordination (experimental — verify event names against your Claude Code version)
- Teams with deadlines (e.g., chemistry-times daily publish) may add `SessionStart` hooks that check deadline status

### What Hooks Must NOT Do

- Hooks must not block the main flow unless the operation is truly dangerous (e.g., a production API write without authorization). Default: non-blocking.
- Hooks must not exceed 10 second timeout — long hooks cripple session startup.
- Hooks must not depend on tools not preinstalled in the user's shell. Guaranteed set: `mkdir`, `cat`, `echo`, `printf`, `test`, `date`, `ls`, plus shell syntax (`case`). `jq` is NOT preinstalled on stock macOS — capture hook stdin with `cat` instead of parsing it (avoid `python`, `node` entirely).
- Anchor every hook path to `"${CLAUDE_PROJECT_DIR:-.}"` — hooks can run with a cwd outside the project root; bare relative `.worklog/` paths created nested worklog trees in ground truth (toeic, 2026-06).
- The `UserPromptSubmit` capture file accumulates full prompt text. Name its consumer in the team's CLAUDE.md (dialogue review, worklog audit). Teams handling secrets or PII must drop this hook or add redaction before append.

### Hook File Location

Hooks live in the generated team's `.claude/settings.json` under the top-level `hooks` key. Do not create a separate `hooks.json` unless the team has so many hooks that settings.json becomes unreadable (> 200 lines).

## Violation Determination

- Generated team `.claude/settings.json` missing the first-run output-mode hook, or a team that keeps a worklog missing its worklog hooks → Violation
- Worklog hooks shipped in a team that keeps no worklog → Violation
- Hook command exceeds 10 second timeout without `async: true` → Violation
- Blocking hook on non-dangerous operation (not an API write, not a destructive Bash command) → Violation
- Hook depends on a tool not guaranteed in the user's shell → Violation

## Exceptions

- Teams stamped before 2026-11-26 keep the full baseline they were built with.

Tradeoff: Hooks add startup latency (typically < 100ms total) and can fail silently if their commands break. Test every hook in a fresh shell before shipping the team.
