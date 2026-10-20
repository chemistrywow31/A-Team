---
name: role-decomposition
description: Provide methodology and decision framework for decomposing team responsibilities into agent roles with appropriate granularity
---

# Role Decomposition

## Description

Provide methodology and decision framework for decomposing team responsibilities into agent roles with appropriate granularity.

## Users

- `role-designer`: For responsibility decomposition during role design phase
- `team-architect`: For structural rationality assessment during review phase

## Core Framework: MECE Responsibility Decomposition

Each agent's responsibilities must follow the MECE principle:
- **Mutually Exclusive**: Any specific work should belong to only one agent
- **Collectively Exhaustive**: All work combined should have no omissions

## Granularity Guidance

For detailed quantitative granularity assessment, use `.grok/skills/granularity-calibration/SKILL.md`. Quick reference:

- **Too coarse** → Split: Agent has 5+ core work items, spans 2+ professional domains, or cannot be described in one sentence
- **Too fine** → Merge: Two agents always communicate on every task, or one agent has only 1-2 simple tasks
- **Appropriate**: Each agent has one clear sentence describing their core responsibility, 3-5 work items, and interactions are primarily "deliverable handoffs"

## Grouping Strategy

Choose grouping criteria by priority:

1. **Workflow stages** (Most recommended)
   - Applicable scenario: Team work has clear sequential order
   - Example: discovery → planning → execution → review

2. **Professional domains**
   - Applicable scenario: Team spans multiple specialties, but processes within each are similar
   - Example: content → technical → quality

3. **Deliverable-oriented**
   - Applicable scenario: Team's deliverable types are significantly different
   - Example: code → documentation → visual-assets

## Application and Output

Map each confirmed requirement to an owner, its input/output, handoff and quality criterion. Treat numeric guidance above as a heuristic; validate actual workload with granularity-calibration. Choose a target-local roster: generated teams do not inherit A-Team’s 13-role inventory. Only the main coordinator dispatches native specialists; each writer owns exact paths.

## Rejection Case

Reject a proposed role split in which both the researcher and writer own the same facts file. Assign one owner and a read-only review handoff, then check that all confirmed requirements still have coverage.

## Source Attribution

- **Origin**: A-Team canonical skill, preserved at `reference/platform-sources/.claude/skills/role-decomposition/SKILL.md`.
- **Integration**: Pattern B: Adapted Install; native Grok branch authority is `AGENTS.md` plus `.grok/`.
- **Retrieved**: 2026-10-20 from the verified base snapshot.
- **Modifications**: Native paths, loading and lifecycle; preserved task intent, examples and useful assets. Archive is reference-only.
