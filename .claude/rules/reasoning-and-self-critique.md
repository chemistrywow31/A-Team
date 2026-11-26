---
name: Reasoning and Self-Critique
description: A producer checks its own output before handoff; the Reasoning, Workflow and Self-Critique sections are optional structure
paths:
  - "teams/**"
  - ".claude/agents/**"
---

# Reasoning and Self-Critique

## Applicability

- Applies to: anyone writing or editing an agent definition, and every producer before a handoff

## Rule Content

### Check Before You Hand Off

Before returning an artifact or a decision, compare the actual output with its acceptance criteria and with the ways this kind of work usually goes wrong. Fix what you find. If a gap cannot be closed, return `NEEDS_CONTEXT` or `BLOCKED` and name it; do not report `DONE` over a known flaw. This check does not replace independent acceptance under `rules/execution-contract.md` EC-3.

### The Three Sections Are Optional

`## Reasoning`, `## Workflow` and `## Self-Critique` are a useful way to organize an agent whose work has real decisions and real failure modes. A-Team's own agents use them. A generated agent uses them only when each section would say something specific to that role. When they are used, keep them adjacent and in that order, write them once, and do not add Preflight or Verification sections that repeat them. `.claude/templates/reasoning-self-critique-blocks.md` is a starting skeleton, not a form.

The sections instruct the agent. They are not a report format, and no prompt asks for a private reasoning transcript.

## Violation Determination

- A producer returns `DONE` without checking its output against the acceptance criteria -> Violation
- An agent definition carries the three sections with generic text that is not specific to the role -> Violation
- The sections are present but reordered, split by unrelated sections, or duplicated by Preflight or Verification forms -> Violation
- A prompt asks for a private reasoning transcript -> Violation

## Exceptions

- A clarification-only conversation turn needs no artifact check.
- Teams generated before 2026-11-26 without a work-shape record keep the section floor the validator applies to them.
