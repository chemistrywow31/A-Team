---
name: Skill Creator
description: Create or improve a skill by using the system skill when available and the legacy local bundle as fallback
---

# Skill Creator

## Description

Use this bridge skill when A-Team needs to create or improve a skill inside the Codex layout.

## Resolution Order

1. Prefer the globally available Codex/system `skill-creator` skill.
2. If that is unavailable, use the legacy implementation at `.claude/skills/skill-creator/SKILL.md`.
3. When you need bundled scripts or references, use the legacy assets under `.claude/skills/skill-creator/`.

## Minimum Workflow

1. capture intent
2. draft or revise the skill
3. create 2-3 realistic test prompts
4. evaluate outputs
5. iterate
6. improve the skill description for triggering quality

## Output Rule

When the skill is ready, place the final version in both:

- `.codex/skills/{skill-name}/SKILL.md`
- `.agents/skills/{skill-name}/SKILL.md`

## Example

### Input

`幫 A-Team 新增一個專門做法規摘要的 skill。`

### Output

`先用 skill-creator 工作流定義 scope、測試 prompt、評估結果，再把完成版同步到 authored/runtime 兩層。`
