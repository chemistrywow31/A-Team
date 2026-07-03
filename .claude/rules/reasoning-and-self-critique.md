---
name: Reasoning and Self-Critique
description: Every agent must think before acting and challenge its own output before submitting
---

# Reasoning and Self-Critique

## Applicability

- Applies to: All agents (every agent .md must contain a `## Reasoning` section and a `## Self-Critique` section)
- Generated teams: Every generated team must include this rule (or an equivalent) in `rules/` and apply it to all generated agents

## Rule Content

### Two Structural Gates Around Every Workflow

Every agent must enforce two structural gates around its workflow:

1. **`## Reasoning` gate** — runs before the workflow. Forces the agent to think before acting.
2. **`## Self-Critique` gate** — runs after the workflow produces a draft, before submission. Forces the agent to challenge its own output.

Both gates are structural sections in the agent .md file, not instructional sentences. Claude reliably follows structural boundaries; the gates work because the template forces the agent to fill them in.

### Section Ordering in Agent Template

Every agent .md file must place these two sections relative to `## Workflow` as follows:

```
## Identity
## Responsibilities
## Input and Output
## Reasoning            ← Gate 1: think before acting
## Workflow             ← Execute
## Self-Critique        ← Gate 2: challenge before submitting
## Available Skills
## Applicable Rules
... rest
```

This ordering creates a tight think → act → verify triad. Do not separate the three sections; do not place skills/rules between them.

### Canonical `## Reasoning` Block

Every agent's `## Reasoning` section must contain four labeled subsections — `### Knowns`, `### Unknowns`, `### Plan`, `### Risks` — filled before the workflow starts, written to the worklog or the task return. The canonical block text lives in `.claude/templates/reasoning-self-critique-blocks.md`; writers copy it verbatim from there. Compliance check: grep the agent file for all four slot headers under `## Reasoning`.

### Canonical `## Self-Critique` Block

Every agent's `## Self-Critique` section must contain five labeled checks — `### Evidence Check`, `### Position Check`, `### Counterexample Check`, `### Completeness Check`, `### Failure Mode Check` — run against the draft before submission. If any check fails, revise and re-run all five; do not submit unrevised output. Canonical block text: `.claude/templates/reasoning-self-critique-blocks.md` (writers copy verbatim). Compliance check: grep the agent file for all five check headers under `## Self-Critique`.

### When the Gates Apply

Both gates apply to every output that crosses an agent boundary:

- Decisions written to `decisions.md`
- Files generated (agent .md, skill SKILL.md, rule .md, CLAUDE.md, settings.json)
- Reports returned to the coordinator
- Recommendations delivered to the user

The gates do not apply to internal scratch work that never leaves the agent (e.g., intermediate exploration that gets discarded).

### Coordinators Run a Pre-Dispatch Variant

Coordinators must additionally run a **Pre-Dispatch Reasoning** gate before each Task dispatch, with four slots: `### What This Dispatch Must Achieve`, `### Why This Agent`, `### Inputs the Agent Needs`, `### Predicted Failure Modes`. Canonical block text: `.claude/templates/reasoning-self-critique-blocks.md`. It forces the coordinator to commit before dispatching and prevents reflexive forwarding of vague tasks.

### Self-Critique Cannot Be Outsourced

The agent that produces the output must run its own Self-Critique. Downstream review agents (decision-auditor, dialogue-reviewer, code-reviewer, process-reviewer) are additional layers, not replacements. An agent that submits without self-critique, expecting downstream review to catch errors, is in violation regardless of whether the review later catches the issue.

This is a separation of concerns: Self-Critique catches the agent's own blind spots; downstream review catches blind spots the agent could not see by definition.

### Tier 1 Agents

Tier 1 agents (deterministic formatters, single-lookup utilities — see `rules/context-tier.md`) may use the reduced 2-slot Self-Critique (`### Format Check`, `### Input Coverage Check`) — canonical text in `.claude/templates/reasoning-self-critique-blocks.md`. Tier 1 agents may omit `## Reasoning` entirely if the task has zero judgment calls and the agent .md states this in the Tier 1 justification.

### Failure Recovery

If Self-Critique exposes a gap that revision cannot close after 3 attempts, the agent must escalate rather than submit known-flawed output: return `STATUS: NEEDS_CONTEXT` (naming the missing information, e.g. `INSUFFICIENT_DATA: {items}` in CONCLUSIONS) when the gap is informational, or `STATUS: BLOCKED` otherwise — the four EC-1.1 statuses are the only valid report statuses. State the specific gap and what would unblock it.

## Violation Determination

- Agent .md missing `## Reasoning` section → Violation
- Agent .md missing `## Self-Critique` section → Violation
- `## Reasoning` placed after `## Workflow` instead of before → Violation
- `## Self-Critique` placed before `## Workflow` instead of after → Violation
- `## Reasoning` block missing any of the four canonical slots (Knowns / Unknowns / Plan / Risks) → Violation
- `## Self-Critique` block missing any of the five canonical checks (Evidence / Position / Counterexample / Completeness / Failure Mode) → Violation
- Coordinator agent missing `## Pre-Dispatch Reasoning` section in addition to `## Reasoning` → Violation
- Agent submits output without filling `## Reasoning` slots — detected when worklog or task return contains no Knowns/Unknowns/Plan/Risks record → Violation
- Agent declares Tier 1 reduction without Tier 1 justification matching `rules/context-tier.md` → Violation
- Generated team's `rules/` does not contain a Reasoning and Self-Critique rule (this rule or an equivalent) → Violation
- Generated team's agents do not include `## Reasoning` and `## Self-Critique` sections → Violation

## Exceptions

- Tier 1 agents may use the reduced Self-Critique format and may omit `## Reasoning` per the Tier 1 carve-out above.
- During interactive conversation phases (Phase 1 Discovery), agents that ask the user a single clarification question may complete the question without running the full Self-Critique — but must run both gates before producing any artifact (summary document, requirements doc, role design).

Tradeoff: both gates add 30-60 seconds of structured reasoning per dispatch; skipping them produces faster output whose downstream failure costs (re-dispatch, rework, audit findings) exceed the gate cost.
