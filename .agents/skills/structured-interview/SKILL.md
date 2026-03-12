---
name: Structured Interview
description: Extract precise team requirements through staged, single-direction questioning
---

# Structured Interview

## Description

Use this skill to turn vague user wishes into a confirmed requirements summary with explicit scope, workflow, role coverage, and constraints.

## Users

- `.codex/agents/discovery/requirements-analyst.md`
- `.codex/agents/team-architect.md`

## Core Methods

### Funnel Method

1. requested format question
2. open goal question
3. scope boundary question
4. concretization follow-up
5. playback and confirmation

### Follow-Up Triggers

Ask a follow-up when the user:

- asks for Claude or another non-Codex format without clarifying whether Codex-native canonical output is acceptable
- uses vague filler words
- skips workflow details
- implies a missing stage
- asks for conflicting outcomes

### Reverse Validation

Use counterfactuals:

- what work breaks if role X disappears
- what risk appears if roles Y and Z merge
- what failure mode is most likely

## Rhythm

- one direction per response
- interim summary every 3-4 rounds
- stop when the user starts repeating already-confirmed information

## Example

### Input

`我想做一個內容團隊。`

### Output

`先確認你要的團隊格式：要以 Codex-native 交付、Claude 相容格式，還是先以 Codex 為 canonical 並保留 mapping 供之後雙向轉換？`
