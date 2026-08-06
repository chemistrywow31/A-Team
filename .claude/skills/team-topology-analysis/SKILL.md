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
- Only the main-session coordinator delegates through the Claude Task/Agent tool. Specialists cannot dispatch other agents.
- Stable task paths use phase-purpose names so joins, follow-ups, and worklog evidence stay traceable.
- All agents share one filesystem. Parallel branches need explicit owned paths, forbidden paths, and the non-reversion rule.
- Treat each Task/Agent dispatch as fresh specialist context. Pass the task identity, artifact paths, ownership boundaries, and acceptance criteria; do not assume access to the coordinator's conversation.
- A specialist that needs user input returns `NEEDS_CONTEXT`; the coordinator relays the question and re-dispatches the task with the answer.

## Application Guide

1. Map the workflow stages, deliverables, and review relationships before drawing the graph.
2. Choose the lightest topology that preserves clear ownership: pipeline for strict sequence, hub-and-spoke for coordinator-driven parallel work, hybrid for mixed staged and parallel work.
3. Assign stable task paths and disjoint file ownership to every branch that can run in parallel.
4. Define each coordinator-to-specialist Task/Agent handoff: input paths, owned and forbidden paths, acceptance criteria, return state, and downstream verification.
5. Reject or flatten any topology that requires a specialist to dispatch another agent; all specialist work must be dispatched directly by the coordinator.
6. Flag bottlenecks, cycles, review loops without exit criteria, and shared-file hotspots before accepting the topology.

## Quality Checkpoints

- [ ] The coordinator is the only user-facing hub and does not depend on a sub-coordinator.
- [ ] Parallel branches own different files or one explicit primary owner mediates writes.
- [ ] Every Task/Agent dispatch originates from the main-session coordinator; specialists never dispatch.
- [ ] Task paths and join boundaries are explicit enough to support worklog tracing.
- [ ] The topology can finish without circular dependency outside intentional review loops.

## Example

### Input

`Frontend, backend, and QA all need to edit the same API schema at the same time.`

### Output

Reject the topology as unsafe for a shared filesystem; assign one schema owner, route feedback through review or coordinator, and keep the other roles read-only on that file.
