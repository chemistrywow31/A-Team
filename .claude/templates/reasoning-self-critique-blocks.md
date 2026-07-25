# Canonical Reasoning and Self-Critique Blocks

These are SKELETONS, not boilerplate. Take the section and slot headers verbatim — they are what the compliance grep matches — and write the bullets under each header specific to the agent you are producing. A generated agent carrying this file's generic wording has a gate that checks nothing. Per `rules/reasoning-and-self-critique.md`: `## Reasoning` goes before `## Workflow`; `## Self-Critique` goes after. Read-trigger: agent-writer reads this file before writing any agent file.

## Canonical `## Reasoning` block

```markdown
## Reasoning

Before executing the workflow, work through this reasoning gate. Do not start the workflow until all four slots are answered.

### Knowns
- {What information is confirmed? What inputs are available?}

### Unknowns
- {What is missing? What assumptions are being made? What would need to be verified?}

### Plan
- {What approach will be taken? Why this approach over alternatives?}

### Risks
- {What could go wrong? Which assumptions, if false, would invalidate the plan? What is the falsification condition?}
```

## Canonical `## Self-Critique` block

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

## Coordinator-only `## Pre-Dispatch Reasoning` block

```markdown
## Pre-Dispatch Reasoning

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

## Tier 1 reduced `## Self-Critique` block

```markdown
## Self-Critique

### Format Check
- Does the output match the required format exactly?

### Input Coverage Check
- Was every required input field consumed?
```
