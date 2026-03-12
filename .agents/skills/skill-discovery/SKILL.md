---
name: Skill Discovery
description: Search external sources for reusable skills before designing a new one
---

# Skill Discovery

## Description

Use this skill during planning to find reusable external skills, score them, and decide whether to install, adapt, or only reference them.

## Users

- `.codex/agents/planning/skill-planner.md`

## Configuration

Read `config.json` beside this skill if it exists. Otherwise use the bundled defaults.

## Search Workflow

1. derive 2-3 search queries per capability
2. search every enabled source
3. fetch promising detail pages
4. deduplicate overlapping results
5. score each candidate
6. classify as reuse, reference, or discard

## Scoring Dimensions

- relevance: 40%
- quality: 25%
- freshness: 15%
- adoption: 20%

## Decision Thresholds

- `>= 3.5`: reuse with Pattern A or B
- `2.5 - 3.4`: reference only
- `< 2.5`: discard and create custom skill

## Installation Rules

When installing or adapting a skill, place it in both:

- `.codex/skills/{skill-name}/SKILL.md`
- `.agents/skills/{skill-name}/SKILL.md`

External installs must append Source Attribution.

## Output Format

Always include:

- `External Skills Discovery`
- `Search Summary`
- recommended external skills
- reference materials

## Example

### Input

`capability: structured blog writing`

### Output

`找到 4 個候選；1 個建議直接重用，1 個作為參考素材，2 個淘汰。`
