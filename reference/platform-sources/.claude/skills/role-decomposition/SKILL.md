---
name: Role Decomposition
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

For detailed quantitative granularity assessment, use `skills/granularity-calibration/SKILL.md`. Quick reference:

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
