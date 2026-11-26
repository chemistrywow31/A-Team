---
name: Coordinator Mandate
description: An agent group has one coordinator in the main session, direct specialists, and explicit path ownership
paths:
  - "teams/**"
  - ".claude/agents/**"
---

# Coordinator Mandate

## Applicability

- Applies to: A-Team itself and every generated team whose work-shape record includes an `agent-group` flow
- A skill-workflow team is one agent and has no coordinator.

## Rule Content

### One Coordinator, Direct Specialists

- A group has exactly one coordinator. It runs in the main session, owns the conversation with the user, and is never spawned as a subagent.
- Specialists are direct children of the coordinator. There is no sub-coordinator and no relay role.
- Only the coordinator dispatches. Claude Code supports nested subagents; this is team policy, enforced with `disallowedTools: [Agent]` on each specialist. Do not change user or global spawn-depth settings. See [native subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-10-06.
- The coordinator does not take over a specialist's artifact family to move faster.
- Subagent mode and experimental Agent Teams are different runtimes. Choose Agent Teams only when a target needs independently collaborating sessions and the runtime supports it.

### Stable Task Paths

Each dispatch has a stable name for its purpose, such as `generation_rules` or `review_runtime_preflight`. A corrective or resumed dispatch keeps the name and carries only what changed. The coordinator waits for a result only when its next step depends on it.

### Shared Filesystem

Agents share one filesystem unless the runtime isolates them. A dispatch that writes names its owned paths, its forbidden paths, and its acceptance criteria. Nobody reverts an edit they did not make; an unexpected foreign edit is adapted to or escalated, not overwritten.

## Violation Determination

- A group has no coordinator, more than one, a sub-coordinator, or a coordinator that is spawned -> Violation
- A specialist dispatches, or its `disallowedTools: [Agent]` restriction is missing -> Violation
- The coordinator writes a specialist's artifact family without an explicit reassignment -> Violation
- A writing dispatch omits owned paths, forbidden paths or acceptance criteria -> Violation
- An agent reverts or overwrites an edit it did not make -> Violation

## Exceptions

- A skill-workflow team is out of scope.
- Conversation with the user in the main session is coordination, not specialist work.
