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
- Where the target runtime and dispatch permit delegation, a specialist may create one nested helper only for bounded, independent evidence or verification inside its owned artifact family. That helper may not delegate again. This is A-Team policy, not a universal vendor depth limit.
- Stable task paths use phase-purpose names so joins, follow-ups, and worklog evidence stay traceable.
- All agents share one filesystem. Parallel branches need explicit owned paths, forbidden paths, and the non-reversion rule.
- Select the target-supported lifecycle/profile from `.codex/rules/context-isolation.md`. On A-Team’s observed v2 host, full-history forks inherit the parent model/effort; use bounded/no-history forks when isolation or role overrides require them. Do not assume those parameters exist on another host.
- Join points are explicit. Do not stop the coordinator at `wait_agent` while independent work still exists.

## Application Guide

1. Establish the selected native runtime/profile, then map workflow stages, deliverables, and review relationships. Record installed support and live tools separately; use the native capacity counting unit without mixing root-inclusive and spawned-only counts.
2. Choose the lightest topology that preserves clear ownership: pipeline for strict sequence, hub-and-spoke for coordinator-driven parallel work, hybrid for mixed staged and parallel work.
3. Assign stable task paths and disjoint file ownership to every branch that can run in parallel.
4. Define each handoff’s input paths, exact ownership, acceptance criteria, return state, evidence-persistence owner, and verification. Use EC-1’s bounded inline fallback when the live sandbox blocks report writes. For the observed v2 profile, define each edge with `spawn_agent` for new bounded work, `send_message` for non-triggering updates, `followup_task` for a corrective or new idle-agent turn, `interrupt_agent` only for invalid or unsafe work, `list_agents` before joins or reroutes, and `wait_agent` only at a real synchronization boundary.
5. Check whether any specialist would need more than one helper hop or an unavailable native capability. Flatten unsupported edges; when the host disallows delegation, execute locally and record that limitation.
6. Flag bottlenecks, cycles, review loops without exit criteria, and shared-file hotspots before accepting the topology.

## Quality Checkpoints

- [ ] The coordinator is the only user-facing hub and does not depend on a sub-coordinator.
- [ ] Parallel branches own different files or one explicit primary owner mediates writes.
- [ ] Nested delegation is bounded to one helper hop inside the owner's artifact family.
- [ ] Task paths and join boundaries are explicit enough to support worklog tracing.
- [ ] The topology can finish without circular dependency outside intentional review loops.

## Examples

### Rejection Case

For “Frontend, backend, and QA all need to edit the same API schema at the same time,” reject overlapping writes; assign one schema owner, route feedback through review or coordinator, and keep the other roles read-only on that file.

## Sources And Adaptation

Shared topology and ownership intent: `.claude/skills/team-topology-analysis/SKILL.md`. Codex-specific fork/helper/lifecycle behavior: `.codex/rules/context-isolation.md`, within its inventoried scope. Keep the target’s declared profile and live evidence current; static config alone cannot prove collaboration readiness.
