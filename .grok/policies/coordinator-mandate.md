---
name: Coordinator Mandate
description: Keep one main-session coordinator with direct native specialists and exact shared-filesystem ownership
---

# Coordinator Mandate

## Applicability

- Applies to all agents; root owns user communication, phase coordination, and delegation.

## Rule Content

### One Main-Session Coordinator

Every generated multi-agent team has exactly one coordinator. The entry skill makes the current session adopt its playbook; never spawn the coordinator as a child. Root is the sole user-facing phase owner and synthesizes only artifact families explicitly assigned to it. Do not absorb specialist-owned work to save dispatch time.

### Flat Direct-Specialist Topology

All specialists are direct children of root. Do not create a sub-coordinator or nested helper. Grok's pinned source defaults to one child depth and strips/rejects further task dispatch there; retain the role-level source-backed `disallowedTools: [Task]` directive as well. Effective denial still needs installed-session evidence. A prompt prohibition alone is not a tool-enforcement proof.

A-Team's coordinator may select exactly these 12 project specialists:

- `requirements-analyst`, `role-designer`, `domain-researcher`, `decision-auditor`
- `skill-planner`, `rule-writer`, `skill-writer`, `agent-writer`
- `prompt-optimizer`, `runtime-preflight-advisor`, `dialogue-reviewer`, `team-restructuring-master`

Keep `team-architect` in the main session. Omit root's `tools` allowlist to retain its native tools for editing, research, skills, questions, and coordination. This 12-name roster is prompt policy, not native child-type enforcement. Do not claim an empty `tools` list removes tools.

Generated teams use their confirmed target-local roster, not A-Team's 13-role inventory. The one-root topology and ownership contract remain; role count follows workflow coverage and the process-review exception in `.grok/policies/reviewer-mandate.md`.

### Stable Tasks And Native Lifecycle

Give every dispatch a stable phase-purpose ID such as `generation_rules` or `review_runtime_preflight`. Keep it for corrective work and carry only changed evidence or criteria. Use the advertised native lifecycle in `.grok/policies/context-management.md`; do not invent role-selection fields or require feature-gated active messaging.

Delegate independent work while root advances its own assigned work. Join only when the next step depends on child output. Freeze producers before independent artifact review and runtime preflight. Cancellation is for invalidated or unsafe work, not normal synchronization.

### Shared Filesystem Ownership

Assume a shared filesystem unless an actually provisioned isolation mode proves otherwise. Every dispatch names exact owned and forbidden write paths, criteria, report destination/owner, and the rule: preserve concurrent edits; never revert edits you did not make.

Keep canonical edits and their mapped same-family projections sequential under one owner. If an unexpected edit touches the same file, inspect and accommodate it or report the concrete conflict. Never restore a stale whole-file preimage over another writer's changes.

### Lead And Direct Specialists

The same one-level topology runs in two ways. In Grok Build, the client discovers flat `.grok/agents/*.md`. In a lead-and-helpers deployment, the coordinator passes `briefs/<role>.md` and a task envelope to a new direct specialist that starts with no conversation history. That specialist returns one result to the coordinator. It does not spawn, message other specialists, or message the user. This is the existing direct-specialist limit, not a second tier of coordinator.

`disallowedTools: [Task]` remains the source-backed directive when the client loads the agent file. The brief states the same limit because a specialist started from the brief is not selected through that file. Do not treat the brief as proof the host enforced the limit.

The coordinator updates `.worklog/task-board.json` and the owner report in `.grok/policies/supervision.md` when a task starts, changes status, or finishes. Record cost and tokens only when the host reports them.

## Violation Determination

- A multi-agent team has no coordinator, competing coordinators, or a coordinator spawned as child -> Violation.
- A specialist delegates, lacks its Task denial, or root claims its roster is tool-enforced without evidence -> Violation.
- A generated roster is copied from A-Team solely to satisfy repo-self counts -> Violation.
- A dispatch lacks stable ID, exact ownership, criteria, report owner, or non-reversion -> Violation.
- Root takes another owner's family without reassignment or waits despite useful independent work -> Violation.

## Exceptions

A single-agent target may omit a separate coordinator role when its root entry declares single-session execution. User-facing discussion remains root coordination, not specialist work.
