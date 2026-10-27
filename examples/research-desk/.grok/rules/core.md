---
name: Research Desk Core
description: Always-loaded bootstrap that routes the research-desk policies
---

# Research Desk Core

## Applicability

This is the only always-loaded rule. Read `AGENTS.md` and the assigned role before acting.

## Required Policy Routing

- Every role reads `.grok/policies/execution.md` at startup.
- The lead reads `.grok/policies/supervision.md` and `.grok/policies/worklog.md` when dispatching, updating the task board, or writing the owner report.

## Boundaries

One lead coordinates. Specialists do not spawn helpers. Native Grok sessions use `.grok/agents/`. Helper sessions use the matching file in `briefs/` plus the lead's task envelope.

## Violation Determination

- A triggered policy is unread, or a specialist spawns another helper -> Violation.

## Exceptions

Read each applicable policy once while its content remains current.
