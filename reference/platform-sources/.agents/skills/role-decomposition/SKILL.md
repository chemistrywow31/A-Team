---
name: Role Decomposition
description: Decompose workflow responsibilities into a clean, non-overlapping role set
---

# Role Decomposition

## Description

Use this skill to convert workflow stages into roles with clear ownership and limited coordination overhead.

## Users

- `.codex/agents/discovery/role-designer.md`
- `.codex/agents/team-architect.md`

## Core Framework

Apply MECE:

- mutually exclusive ownership
- collectively exhaustive coverage

## Granularity Guidance

Use `.agents/skills/granularity-calibration/SKILL.md` for quantitative checks. Quick rules:

- too coarse: the role spans multiple expert domains or cannot be summarized in one sentence
- too fine: the split creates constant back-and-forth on every task
- good: the role owns one type of decision and one deliverable family

## Grouping Priority

1. workflow stages
2. professional domains
3. deliverable type

## Example

### Input

`內容團隊需要研究題目、寫稿、審稿、上架。`

### Output

`拆成 research、writing、review、delivery 四個角色；若量體小，可把 research 與 writing 合併，但 review 不應併入 delivery。`
