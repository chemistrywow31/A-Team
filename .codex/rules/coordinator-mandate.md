---
name: Coordinator Mandate
description: Require one non-executing coordinator in every generated team
---

# Coordinator Mandate

## Applicability

- Applies to: all generated teams and all A-Team writers

## Rule Content

### Coordinator Must Exist

Every generated team must include one coordinator prompt at `.codex/agents/{coordinator}.md`. The coordinator is the only role allowed at the root of `.codex/agents/`.

### Coordinator Does Not Execute

The coordinator may plan, assign, track, follow up, resolve dependencies, and enforce quality gates. The coordinator must not absorb delivery work that belongs to specialist agents.

### Flat Architecture Only

Use one coordinator with direct specialists. Do not add sub-coordinators. In Codex, extra relay layers around `spawn_agent` and `send_input` create unnecessary information loss and slower joins.

## Violation Determination

- No coordinator file exists at `.codex/agents/` root -> Violation
- The coordinator prompt contains production work in its Responsibilities section -> Violation
- A second coordinator exists only to relay tasks between the main coordinator and workers -> Violation

## Exceptions

This rule has no exceptions.
