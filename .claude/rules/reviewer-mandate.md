---
name: Reviewer Mandate
description: Add a reviewer role only where the work-shape record names an isolated check; process review is a skill by default
paths:
  - "teams/**"
---

# Reviewer Mandate

## Applicability

- Applies to: `team-architect`, `role-designer`, `agent-writer`

## Rule Content

### A Reviewer Role Needs An Isolated Check

A reviewer is a separate agent only when the flow's entry in `docs/work-shape.json` names an `isolated_check`: something that must be judged by a reader who has not seen the author's reasoning. That reviewer gets the acceptance criteria and the artifact paths and nothing about how the work was done. When the deliverable is executable, the check runs it. When a person approves the output, they are the isolated check, and an agent reviewer is added only if the user asks for one.

Without an isolated check, the author checks its own work against the team's standards using a review skill. Do not add a reviewer because teams usually have one.

### Process Review Is A Skill By Default

A retrospective on how the team worked (handoffs that lost information, loops, scope drift) is a skill the coordinator runs after a cycle. Make it a dedicated role only when the user wants a standing process reviewer or the retrospective must be independent of the coordinator. Keep it apart from deliverable review: one asks whether the output is right, the other asks how the team got there.

### Placement

A reviewer role sits in its own group folder, not beside the agents whose work it reviews.

## Violation Determination

- A reviewer role exists and no flow in the record names an isolated check or a user request for it -> Violation
- A flow names an isolated check and the check is made by the author or by an agent that received the author's reasoning -> Violation
- A reviewer role is placed in the same group folder as the agents it reviews -> Violation

## Exceptions

- Teams generated before 2026-11-26 keep the reviewers they were built with until they are restructured.
