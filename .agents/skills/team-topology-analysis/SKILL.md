---
name: Team Topology Analysis
description: Evaluate whether a proposed agent graph supports safe handoffs and useful parallel work
---

# Team Topology Analysis

## Description

Evaluate whether a proposed team graph supports safe handoffs, bounded delegation, useful parallelism, and clear ownership in a shared filesystem.

## Users

- `.codex/agents/discovery/role-designer.md`
- `.codex/agents/team-architect.md`

## Core Knowledge

- Prefer direct-specialist topologies. The coordinator stays user-facing; do not add a sub-coordinator.
- A specialist may create one nested helper only for bounded, independent evidence or verification inside that specialist's owned artifact family.
- Stable task paths use phase-purpose names so joins, follow-ups, and worklog evidence stay traceable.
- All agents share one filesystem. Parallel branches need explicit owned paths, forbidden paths, and the non-reversion rule.
- Full-history forks are the default. Use `fork_turns = "none"` or a bounded positive fork only when isolation or a model or effort override requires it.
- Join points are explicit. Do not stop the coordinator at `wait_agent` while independent work still exists.

## Application Guide

1. Map workflow stages, deliverables, and review relationships before drawing the graph.
2. Choose the lightest topology that preserves clear ownership: pipeline for strict sequence, hub-and-spoke for coordinator-driven parallel work, hybrid for mixed staged and parallel work.
3. Assign stable task paths and disjoint file ownership to every branch that can run in parallel.
4. Define the lifecycle for each edge: `spawn_agent` for new bounded work, `send_message` for non-triggering updates, `followup_task` for a corrective or new idle-agent turn, `interrupt_agent` only for invalid or unsafe work, `list_agents` before joins or reroutes, and `wait_agent` only at a real synchronization boundary.
5. Check whether any specialist would need more than one helper hop. If yes, the design is too deep for the runtime contract.
6. Flag bottlenecks, cycles, review loops without exit criteria, and shared-file hotspots before accepting the topology.

## Quality Checkpoints

- [ ] The coordinator is the only user-facing hub and does not depend on a sub-coordinator.
- [ ] Parallel branches own different files or one explicit primary owner mediates writes.
- [ ] Nested delegation is bounded to one helper hop inside the owner's artifact family.
- [ ] Task paths and join boundaries are explicit enough to support worklog tracing.
- [ ] The topology can finish without circular dependency outside intentional review loops.

## Example

### Input

`Frontend, backend, and QA all need to edit the same API schema at the same time.`

### Output

Reject the topology as unsafe for a shared filesystem; assign one schema owner, route feedback through review or coordinator, and keep the other roles read-only on that file.
