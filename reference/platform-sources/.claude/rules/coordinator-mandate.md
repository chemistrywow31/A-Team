---
name: Coordinator Mandate
description: Require one coordinator with direct specialists, stable task paths, and coordinator-only delegation in Claude subagent mode
---

# Coordinator Mandate

## Applicability

- Applies to: all agents; the coordinator carries the additional obligations below

## Rule Content

### Coordinator Must Exist And Own Coordination

- Every generated multi-agent team must contain exactly one coordinator role.
- The coordinator is the sole user-facing phase owner. It may synthesize only the artifact families explicitly assigned to it by the phase plan.
- Specialist-owned artifact families stay specialist-owned. The coordinator must not absorb them to "move faster."

### Flat Direct-Specialist Topology

- All phase specialists are direct children of the coordinator.
- Sub-coordinators are prohibited.
- In Claude subagent mode, only the coordinator delegates via the Agent tool (`Task` is the compatibility alias). Specialists must not dispatch nested helpers or other specialists.
- Claude Code supports nested subagents; this prohibition is A-Team topology policy. Enforce it with `disallowedTools: [Agent]` on each direct specialist. Keep Agent available to the main-session coordinator; do not change user/global spawn-depth settings. See [native subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-10-06.
- Keep subagent mode distinct from experimental Agent Teams. Select Agent Teams only for a target that needs independent collaborating sessions and has confirmed runtime support; do not infer teammate skill loading or nested-team support from subagent behavior.

### Stable Task Paths And Lifecycle Discipline

- Every Agent dispatch uses a stable phase-purpose task path such as `discovery_requirements`, `planning_skill_plan`, `generation_rules`, `generation_agents`, `restructure_assessment`, or `review_runtime_preflight`.
- A resumed or corrective Agent dispatch for the same logical work keeps the same task path and carries only the delta: new evidence, corrected assumptions, updated criteria, or path changes.
- Do not stop for an Agent result while independent coordinator work remains. Wait only at a real join boundary where the next coordinator step depends on that result.

### Shared Filesystem Ownership

- Assume agents share the same filesystem unless the runtime explicitly provisions isolation.
- Every dispatch must state owned write paths, forbidden paths, acceptance criteria, and the non-reversion rule: do not revert edits you did not make.
- Unexpected foreign edits in an owned path are handled by adapting the task or escalating a real conflict, never by blind overwrite.

## Violation Determination

- A generated multi-agent team has no coordinator role, or more than one role claims coordinator authority -> Violation
- The coordinator writes an artifact family owned by a specialist with no explicit phase-plan reassignment -> Violation
- A sub-coordinator exists, a specialist delegates nested work in subagent mode, or its native Agent restriction is missing -> Violation
- An Agent dispatch lacks a stable task path, or a resumed task abandons that path without invalidation rationale -> Violation
- A file-mutating dispatch omits owned paths, forbidden paths, acceptance criteria, or the non-reversion rule -> Violation
- The coordinator waits while independent coordinator work still remains -> Violation

## Exceptions

- Single-agent teams do not require a coordinator role.
- User-facing conversation in the main session remains coordination, not specialist execution.
