---
name: team-topology-analysis
description: Evaluate whether a team graph supports safe handoffs, coordinator-owned delegation, useful parallelism and clear shared-file ownership.
---

# Team Topology Analysis

Use during role design or structural review with the confirmed workflow, deliverable map and selected native runtime.

## Core Knowledge

- Prefer direct specialists. The main-session coordinator remains user-facing; never add a child coordinator. A-Team's 12-specialist roster is prompt policy, not native child-type enforcement; generated teams have their own accepted roster.
- Native model-facing lifecycle uses advertised `spawn_subagent`, `get_command_or_subagent_output`, and `kill_command_or_subagent`; waiting-tool availability is version-dependent. Optional messaging is not required. See `.grok/policies/context-isolation.md` for exact parameters and evidence boundaries.
- Use `subagent_type` only when the live schema advertises the custom-role enum. Source-backed native depth defaults and `disallowedTools: [Task]` support the specialist no-delegation policy; installed enforcement still needs execution evidence.
- New dispatches carry task identity, input paths, exact owned/forbidden paths, criteria, explicit skill reads/preloads and evidence-persistence responsibility. Do not assume parent skills or conversation are available. Completed-child resume retains context and is unsuitable for fresh independent acceptance.
- Shared filesystem means parallel branches need disjoint ownership and a non-reversion rule. A blocked specialist returns NEEDS_CONTEXT; the coordinator relays required questions and redispatches with answers.

## Workflow

1. Map stages, deliverables and review relationships against actual host tools; distinguish native capability from team policy.
2. Choose the lightest graph: pipeline for strict sequence, hub-and-spoke for independent work, hybrid for mixed stages. Avoid delegation when its overhead exceeds the independent value.
3. Assign stable phase-purpose task paths and disjoint file ownership. Keep canonical edits and same-family regeneration sequential under one owner.
4. Define input/output, criteria, return state, report-persistence owner, join point and downstream verification for every handoff. Apply EC-1's bounded inline fallback only when assigned and needed.
5. Flatten any graph requiring a specialist to spawn another agent. Route bounded follow-up work through the main coordinator using live native completion/resume/redispatch semantics.
6. Flag bottlenecks, cycles, shared-file hotspots and review loops without exit criteria. Freeze a coherent batch before independent review, then invalidate only affected evidence after correction.

## Quality Checkpoints

- One user-facing coordinator, no child coordinator and no specialist delegation.
- Parallel owners do not write the same paths; dependencies and joins are explicit.
- Every role has measurable completion criteria and actual required tools, including execution for validators.
- Model/effort/tool constraints are not inferred from skill metadata or parser acceptance.
- Completion does not rely on an optional messaging feature or a circular dependency.

## Rejection Case

Frontend, backend and QA all propose editing one API schema concurrently. Assign a single schema owner and read-only review handoffs; keep unrelated implementation work parallel. Do not solve the collision by adding another coordinator.

## Source Attribution

- **Origin**: A-Team canonical skill, preserved at `reference/platform-sources/.claude/skills/team-topology-analysis/SKILL.md`.
- **Integration**: Pattern B: Adapted Install; native Grok branch authority is `AGENTS.md` plus `.grok/`.
- **Retrieved**: 2026-10-20 from the verified base snapshot.
- **Modifications**: Native paths, loading and lifecycle; preserved task intent, examples and useful assets. Archive is reference-only.
