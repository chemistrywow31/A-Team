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

Every agent's `## Reasoning` section must contain four labeled subsections. The agent must fill all four before starting the workflow.

```markdown
## Reasoning

Before executing the workflow, complete this reasoning gate. Do not start the workflow until all four slots are filled. Write the reasoning to the worklog or to a structured note in your task return — do not skip and produce output directly.

### Knowns
- {What information is confirmed? What inputs are available?}

### Unknowns
- {What is missing? What assumptions are being made? What would need to be verified?}

### Plan
- {What approach will be taken? Why this approach over alternatives?}

### Risks
- {What could go wrong? Which assumptions, if false, would invalidate the plan? What is the falsification condition?}
```

### Canonical `## Self-Critique` Block

Every agent's `## Self-Critique` section must contain five labeled checks. The agent must run all five against the draft output before submission. If any check fails, the agent must revise and re-run all five — not submit unrevised output.

```markdown
## Self-Critique

After producing draft output, run this critique pass before submission. If any check exposes a gap, revise the draft and re-run all five checks. Submit only when every check passes, or escalate per the Uncertainty Protocol when revision cannot close the gap.

### Evidence Check
- Does every claim trace back to a source, finding, or upstream worklog entry? Flag any claim that does not.

### Position Check
- Did I take a clear position with stated reasoning, or did I hedge with vague agreement? Restate any hedged conclusion as a position with evidence and a falsification condition.

### Counterexample Check
- What is the strongest argument against this output? Did I address it, or did I avoid it? If unaddressed, address it now.

### Completeness Check
- Does the output answer the actual task scope, or only the easy parts? Flag and fix any task scope item that received less attention than its difficulty warrants.

### Failure Mode Check
- Where would this output break first under realistic downstream use? What input or context would expose the weakest link? State the predicted failure mode in the output or fix the weak link.
```

### When the Gates Apply

Both gates apply to every output that crosses an agent boundary:

- Decisions written to `decisions.md`
- Files generated (agent .md, skill SKILL.md, rule .md, CLAUDE.md, settings.json)
- Reports returned to the coordinator
- Recommendations delivered to the user

The gates do not apply to internal scratch work that never leaves the agent (e.g., intermediate exploration that gets discarded).

### Coordinators Run a Pre-Dispatch Variant

Coordinators must additionally run a **Pre-Dispatch Reasoning** before each Task dispatch:

```markdown
## Pre-Dispatch Reasoning (Coordinator only)

Before dispatching any Task, fill this gate:

### What This Dispatch Must Achieve
- {Single concrete outcome — not "make progress on X"}

### Why This Agent
- {Why this agent over alternatives. What capability uniquely qualifies it.}

### Inputs the Agent Needs
- {Worklog paths, upstream decisions, scope summary — confirm each is ready before dispatch}

### Predicted Failure Modes
- {What the agent might get wrong. What you will check on return.}
```

This is the coordinator's equivalent of `## Reasoning`. It forces the coordinator to commit before dispatching and prevents reflexive forwarding of vague tasks.

### Self-Critique Cannot Be Outsourced

The agent that produces the output must run its own Self-Critique. Downstream review agents (decision-auditor, dialogue-reviewer, code-reviewer, process-reviewer) are additional layers, not replacements. An agent that submits without self-critique, expecting downstream review to catch errors, is in violation regardless of whether the review later catches the issue.

This is a separation of concerns: Self-Critique catches the agent's own blind spots; downstream review catches blind spots the agent could not see by definition.

### Tier 1 Agents

Tier 1 agents (deterministic formatters, single-lookup utilities — see `rules/context-tier.md`) may use a reduced 2-slot Self-Critique:

```markdown
## Self-Critique

### Format Check
- Does the output match the required format exactly?

### Input Coverage Check
- Was every required input field consumed?
```

Tier 1 agents may omit `## Reasoning` entirely if the task has zero judgment calls and the agent .md states this in the Tier 1 justification.

### Failure Recovery

If Self-Critique exposes a gap that revision cannot close after 3 attempts, the agent must escalate via the Uncertainty Protocol with `INSUFFICIENT_DATA` or `BLOCKED` rather than submit known-flawed output. State the specific gap and what would unblock it.

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

Tradeoff: Both gates add structured reasoning steps before and after every workflow. For trivial tasks the cost is real — typically 30-60 extra seconds of reasoning per dispatch. The payoff is reliability: agents catch their own evidence gaps, hedged positions, and unaddressed counterexamples before downstream agents have to. Skipping the gates produces faster output that fails more often under real use, and downstream review costs (re-dispatch, rework, audit findings) exceed the gate cost.
