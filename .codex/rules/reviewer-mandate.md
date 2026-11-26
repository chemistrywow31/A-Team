---
name: Reviewer Mandate
description: Add a reviewer role only where the work-shape record names an isolated check; process review is a skill by default
---

# Reviewer Mandate

## Applicability

- Applies to: `team-architect`, `role-designer`, `agent-writer`

## Rule Content

### A Reviewer Role Needs An Isolated Check

A reviewer is a separate agent only when the flow's entry in `docs/work-shape.json` names an `isolated_check`: something that must be judged by a reader who has not seen the author's reasoning. Give that reviewer the acceptance criteria and artifact paths and nothing about how the work was done. When a person approves the output, they are the isolated check; add an agent reviewer only when the user asks for one.

Without an isolated check, the author checks its own work against the team's standards using a review skill. Do not add a reviewer because teams usually have one.

### Process Review Is A Skill By Default

A retrospective on how the team coordinated (handoff quality, workflow adherence, missed opportunities) is a skill the coordinator runs after a cycle. Make it a dedicated role only when the user wants a standing process reviewer or the retrospective must be independent of the coordinator. Keep it apart from deliverable review.

### Placement

Give a reviewer role its own agent id and config file under `agents/`. Do not merge it into a worker config or reuse a worker `developer_instructions` block for review duties.

## Violation Determination

- A reviewer role exists and no flow in the record names an isolated check or a user request for it -> Violation
- A flow names an isolated check and the check is made by the author or by an agent that received the author's reasoning -> Violation
- The reviewer shares one config file or one agent registration with a worker it reviews -> Violation

## Exceptions

- Teams generated before 2026-11-26 keep the reviewers they were built with until they are restructured.
