---
name: Granularity Calibration
description: Provide quantitative methods for evaluating whether agent decomposition granularity is appropriate
---

# Granularity Calibration

## Description

Provide quantitative methods for evaluating whether agent decomposition granularity is appropriate, preventing over-decomposition or under-decomposition.

## Belongs To

This skill belongs exclusively to `agents/discovery/role-designer.md`

## Calibration Methods

### Responsibility Weight Assessment

Evaluate the "weight" of each agent's responsibilities to ensure weights are roughly balanced across team agents.

Assessment dimensions:
- **Professional depth**: How deep is the domain knowledge required? (shallow/medium/deep)
- **Task complexity**: How many steps does each task involve? (1-3 steps/4-7 steps/8+ steps)
- **Decision density**: How many judgment-based decisions are made during work? (few/medium/many)

### Balance Determination

Ideal state: The difference between the "heaviest" and "lightest" agents in the team should not exceed one level.

If the gap is too large:
- Overweight agents → Consider splitting into 2-3 more specialized roles
- Underweight agents → Consider merging with similar roles, or expanding their responsibility scope

### Practical Determination Method

Answer the following questions. If most answers are "yes", granularity is appropriate:

1. Can each agent's core responsibility be clearly stated in one sentence?
2. After removing any agent, is there clearly identifiable work that would have no one responsible?
3. Are agent interactions primarily "deliverable handoffs" rather than "ongoing discussions"?
4. Does each agent have distinct quality evaluation criteria?
5. Can the coordinator assign tasks without needing to understand technical details?
