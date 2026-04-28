---
name: Prompt Optimization
description: Rewrite generated prompts to be sharper, shorter, and more executable without changing meaning
---

# Prompt Optimization

## Description

Use this skill to improve prompt wording while preserving the original role, scope, and collaboration model.

## Users

- `.codex/agents/optimization/prompt-optimizer.md`

## Principles

1. fidelity first
2. abstract -> concrete
3. remove redundancy
4. prefer imperative language
5. offload deterministic bulk content when it meaningfully reduces tokens

## Fast Checklist

- frontmatter still valid for markdown assets
- TOML keys still valid for agent configs
- paths still resolve
- vague verbs are replaced with actions
- redundant modifiers are removed
- implied assumptions are made explicit
- terminology is consistent

## Typical Rewrite Pattern

`broad statement -> explicit action + expected result`

## Example

### Input

`負責處理使用者回饋。`

### Output

`蒐集使用者回饋，分類為 bug / feature / question，將 bug 轉交開發者，將 feature 記入 backlog，將 question 回傳對應角色。`
