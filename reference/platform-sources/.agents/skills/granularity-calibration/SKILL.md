---
name: Granularity Calibration
description: Check whether a proposed role split is too coarse, too fine, or balanced
---

# Granularity Calibration

## Description

Use this skill to judge whether a team split is balanced enough to be useful without creating unnecessary coordination load.

## Users

- `.codex/agents/discovery/role-designer.md`

## Calibration Method

Score each role on:

- professional depth
- task complexity
- decision density

If the heaviest and lightest roles differ by more than one band, revisit the split.

## Fast Checks

Ask:

1. can each role be described in one sentence
2. does removing the role create an obvious ownership gap
3. are interactions mainly handoffs instead of continuous negotiation
4. does the role have distinct quality criteria
5. can the coordinator assign work without doing the work itself

## Example

### Input

`把前端、後端、資料庫、DevOps 都塞給 lead programmer。`

### Output

`顆粒度過粗；至少拆成 implementation 與 platform/ops，否則專業深度與決策密度失衡。`
