---
name: Hooks Integration
description: Define the hook events and templates every generated team must configure
---

# Hooks Integration

## Applicability

- Applies to: `agent-writer`, `team-architect`

## Rule Content

### Every Generated Team Must Configure Hooks

Every generated team must include `.claude/settings.json` (or `.claude/hooks.json` referenced from settings) with the baseline hook set defined below. Hooks automate worklog bookkeeping and phase lifecycle — tasks that would otherwise burden the coordinator.

### Baseline Hook Set

| Event | Purpose | Hook type | Blocking? |
|-------|---------|-----------|-----------|
| `SessionStart` | Ensure `.worklog/{yyyymm}/` exists for the current month | `command` | No |
| `UserPromptSubmit` | Log the user's initial request to a session ledger | `command` | No |
| `PreCompact` | Write a compaction checkpoint snapshotting current phase state | `command` | No |
| `Stop` | Verify worklog three-file completeness at turn end | `command` | No (advisory) |

### Template

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "mkdir -p .worklog/$(date +%Y%m)",
            "timeout": 5
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "mkdir -p .worklog/$(date +%Y%m) && jq -r '.prompt' >> .worklog/$(date +%Y%m)/session-ledger.md",
            "timeout": 10
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "jq '{ts:now, reason:.reason}' > .worklog/$(date +%Y%m)/compact-checkpoint.json",
            "timeout": 5
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "test -d .worklog/$(date +%Y%m) || echo 'WARN: no worklog dir' >&2",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Team-Specific Additions

Beyond the baseline, teams may add hooks for team-specific concerns:

- Teams with external write operations (SiYuan, Notion, HTTP APIs) should add a `PreToolUse` hook with matcher on `Bash(curl *)` or `mcp__*__write.*` to log write attempts
- Teams in Agent Teams mode may add `SubagentStop` or `TeammateIdle` hooks for cross-teammate coordination (experimental — verify event names against your Claude Code version)
- Teams with deadlines (e.g., chemistry-times daily publish) may add `SessionStart` hooks that check deadline status

### What Hooks Must NOT Do

- Hooks must not block the main flow unless the operation is truly dangerous (e.g., a production API write without authorization). Default: non-blocking.
- Hooks must not exceed 10 second timeout — long hooks cripple session startup.
- Hooks must not depend on tools not available in the user's shell (default to `mkdir`, `jq`, `echo`, `test`; avoid `python`, `node` unless strictly needed).

### Hook File Location

Hooks live in the generated team's `.claude/settings.json` under the top-level `hooks` key. Do not create a separate `hooks.json` unless the team has so many hooks that settings.json becomes unreadable (> 200 lines).

## Violation Determination

- Generated team `.claude/settings.json` missing the baseline hook set → Violation
- Hook command exceeds 10 second timeout without `async: true` → Violation
- Blocking hook on non-dangerous operation (not an API write, not a destructive Bash command) → Violation
- Hook depends on a tool not guaranteed in the user's shell → Violation

## Exceptions

- Teams explicitly designed for non-interactive batch execution (no worklog required) may omit the `SessionStart` and `PreCompact` hooks. State the reason in the team's CLAUDE.md.

Tradeoff: Hooks add startup latency (typically < 100ms total) and can fail silently if their commands break. Test every hook in a fresh shell before shipping the team.
