---
name: Continuous Learning V2
description: Capture repeated A-Team design patterns as reusable instincts for later sessions
---

# Continuous Learning V2

## Description

Use this skill to record repeated design decisions and user corrections as small reusable instincts. The Codex port is manual-first: capture the pattern after the session, then promote it when it keeps recurring.

## Users

- `.codex/agents/team-architect.md`
- maintainers reviewing repeated A-Team outputs

## Instinct Format

```yaml
---
id: always-propose-reviewer
trigger: "when the team produces external deliverables"
confidence: 0.8
domain: "role-design"
---
```

## What To Capture

- roles users repeatedly add
- recurring workflow stages
- common validation failures
- repeated execution-mode preferences
- naming or grouping patterns that keep winning

## Operating Loop

1. after delivery, log the repeated pattern
2. add evidence from the session
3. assign a confidence score
4. promote high-confidence instincts into shared skills or coordinator guidance

## Example

### Input

`最近 5 次技術團隊設計裡，有 4 次使用者都要求補上 feasibility reviewer。`

### Output

`記錄 instinct：when designing a technology-heavy team, ask whether feasibility review needs a dedicated role.`
