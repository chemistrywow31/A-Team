---
name: Team Topology Analysis
description: Evaluate whether a proposed agent graph supports safe handoffs and useful parallel work
---

# Team Topology Analysis

## Description

Use this skill to judge whether a proposed team graph is clean, bottlenecked, or over-coordinated.

## Users

- `.codex/agents/discovery/role-designer.md`

## Topology Patterns

### Pipeline

`A -> B -> C`

Good for strict stage-by-stage work. Risk: one blocked node stalls the chain.

### Hub And Spoke

`Coordinator -> specialists`

Good for coordinator-driven parallel work. Risk: the coordinator becomes a bottleneck.

### Hybrid

`Coordinator -> stage group -> review -> stage group`

Usually the best default for non-trivial teams.

## Codex Multi-Agent Considerations

- parallel agents must own different files
- the coordinator must define when to `spawn_agent`
- follow-up work must be explicit enough for `send_input`
- join points must be documented so `wait` happens only at real synchronization boundaries

## Quality Checkpoints

- every agent has at least one upstream or downstream connection
- the coordinator is central but not overloaded
- no meaningless circular dependency exists
- parallel work is backed by non-overlapping file ownership

## Example

### Input

`前端、後端、QA 三個角色都要直接改同一份 API schema。`

### Output

`拓撲有衝突；應指定單一 schema owner，其他角色只讀或透過 reviewer/coordinator 提出變更。`
