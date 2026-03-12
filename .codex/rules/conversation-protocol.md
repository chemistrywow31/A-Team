---
name: Conversation Protocol
description: Regulate interview flow so discovery is complete before planning or generation
---

# Conversation Protocol

## Applicability

- Applies to: `team-architect`, `requirements-analyst`, `prompt-optimizer`

## Rule Content

### Communicate In The User's Language

Match the user's language. Technical terms may remain in English, but explain them the first time they appear if the user may not know them.

### Do Not Skip Discovery

Do not enter Planning or Generation until all of the following are true:

1. Team objectives are specific and can be summarized without vague filler words.
2. The workflow stages are identified from input to final output.
3. Each workflow stage has at least one candidate role.
4. The requested delivery format is confirmed or explicitly delegated.
5. The user has confirmed the requirements summary.

### Delivery Format Is Part Of Discovery

Before Planning, confirm which team format the user wants: `codex-native`, `claude-compatible`, `dual-format`, or `let A-Team decide`.

Also confirm:

- Codex remains the canonical authored format
- whether conversion-ready mapping must be retained for later Claude <-> Codex transformation

Ask this early in discovery. Do not bury it as a minor preference under generic output requirements.

### One Direction Per Turn

Each response must focus on one question direction. Do not ask more than three unrelated questions in the same reply.

### Interim Summaries Are Mandatory

Every 3-4 rounds, provide a short interim summary containing:

- confirmed requirements
- open questions
- the next area to explore

Do not keep digging after the summary until the user has had a chance to correct it.

### Challenge Weak Assumptions

When the user's proposal has obvious problems, point them out directly. Typical problems:

- responsibilities are too coarse or too fragmented
- two roles overlap without a deliberate review relationship
- the workflow has a gap or dead end
- the requested throughput is unrealistic
- the proposed multi-agent split adds coordination cost without parallel value

Whenever you challenge an assumption, provide a concrete alternative.

## Violation Determination

- Planning starts before the five discovery criteria are satisfied -> Violation
- One response contains four or more unrelated questions -> Violation
- Five consecutive rounds pass without an interim summary -> Violation
- A clear structural issue is noticed but not surfaced -> Violation

## Exceptions

- If the user explicitly asks for a faster pass, reduce interview depth, but still confirm the core objective, workflow, role coverage, and summary before Generation.
