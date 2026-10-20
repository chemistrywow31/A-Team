---
name: Team Topology Analysis
description: Provide framework for analyzing team structure rationality and evaluating collaboration topology efficiency between agents
---

# Team Topology Analysis

## Description

Evaluate whether a proposed team graph supports safe handoffs, coordinator-owned delegation, useful parallelism, and clear ownership in a shared filesystem.

## Users

- `role-designer`
- `team-architect`

## Core Knowledge

- Prefer direct-specialist topologies. The coordinator stays user-facing; do not add a sub-coordinator.
- In Claude subagent mode, only the main-session coordinator delegates through `Agent` (`Task` is the compatibility alias). Native nesting exists; A-Team’s specialist prohibition is topology policy enforced with `disallowedTools: [Agent]`. Keep experimental Agent Teams a separate explicitly selected mode.
- Stable task paths use phase-purpose names so joins, follow-ups, and worklog evidence stay traceable.
- All agents share one filesystem. Parallel branches need explicit owned paths, forbidden paths, and the non-reversion rule.
- Give each new Agent dispatch explicit task identity, input paths, ownership, criteria, and required skill preload/read instructions. Do not assume parent conversation or skills are inherited; resumed work retains its stable task identity.
- A specialist that needs user input returns `NEEDS_CONTEXT`; the coordinator relays the question and re-dispatches the task with the answer.

## Application Guide

1. Establish the selected native runtime/mode, then map workflow stages, deliverables, and review relationships. Keep supported runtime capability separate from A-Team delegation policy.
2. Choose the lightest topology that preserves clear ownership: pipeline for strict sequence, hub-and-spoke for coordinator-driven parallel work, hybrid for mixed staged and parallel work.
3. Assign stable task paths and disjoint file ownership to every branch that can run in parallel.
4. Define each coordinator-to-specialist Agent handoff: input paths, owned and forbidden paths, acceptance criteria, return state, evidence-persistence owner, and downstream verification. Use EC-1’s bounded inline fallback when the live sandbox blocks the assigned report write.
5. Reject or flatten any topology that requires a specialist to dispatch another agent; all specialist work must be dispatched directly by the coordinator.
6. Flag bottlenecks, cycles, review loops without exit criteria, and shared-file hotspots before accepting the topology.

## Quality Checkpoints

- [ ] The coordinator is the only user-facing hub and does not depend on a sub-coordinator.
- [ ] Parallel branches own different files or one explicit primary owner mediates writes.
- [ ] Every Agent dispatch originates from the main-session coordinator; specialists never dispatch.
- [ ] Task paths and join boundaries are explicit enough to support worklog tracing.
- [ ] The topology can finish without circular dependency outside intentional review loops.

## Examples

### Rejection Case

For “Frontend, backend, and QA all need to edit the same API schema at the same time,” reject overlapping writes; assign one schema owner, route feedback through review or coordinator, and keep the other roles read-only on that file.

## Sources

Native modes and skill-loading semantics: [Claude subagents](https://code.claude.com/docs/en/sub-agents) and [Agent Teams](https://code.claude.com/docs/en/agent-teams), checked 2026-10-06. Direct-specialist ownership, no sub-coordinator, and review gates are A-Team policy.
