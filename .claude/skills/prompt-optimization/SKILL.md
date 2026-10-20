---
name: Prompt Optimization
description: Provide systematic prompt optimization methodology to improve instruction quality while preserving original characteristics
---

# Prompt Optimization

## Description

Improve prompt wording while preserving the original role, workflow, runtime intent, ownership model, and canonical policy.

## Users

- `prompt-optimizer`
- `team-architect`

## Core Knowledge

- Prompt effectiveness for the selected platform/model is the goal; word count is not a success metric. Preserve useful XML boundaries, examples, task steps, and verification. Use current official native guidance and label A-Team conventions separately.
- The optimization lane is text-only. It can tighten wording, make triggers explicit, normalize terminology, and remove redundancy.
- It cannot change roles, rules, topology, runtime or config, ownership, mapping, canonical authority, parity, stamps, validation/preflight requirements, or any surface's runnable, reference-only, or activation state.
- Choose capability-only A-Team maintenance versus named-target work before classification. A capability request alone does not authorize target inventory or edits. Named-target optimization starts with target classification so the optimizer knows the target surface, stamp, canonical authority, and mapping state.
- Plain prompt copy-editing on an already-runnable surface remains text-only when it preserves every structural item and the surface's state.
- If a requested change alters any structural item or changes surface state, it belongs to restructuring instead.
- Preserve the selected runtime's native vocabulary.

## Application Guide

1. Confirm task intent and the text-only lane. For a named existing team, classify that target; for capability-only maintenance, remain within assigned A-Team source paths.
2. Stop and hand the task to `team-restructuring-master` when the requested change affects roles, rules, topology, runtime or config, ownership, mapping, canonical authority, parity, stamps, validation/preflight requirements, or a surface's runnable, reference-only, or activation state.
3. Rewrite only owned text to make responsibilities, triggers, completion criteria, and uncertainty handling more explicit.
4. Clarify vague instructions and remove conflicting, obsolete, or redundant controls. Keep examples and concrete steps that improve execution; do not categorically remove XML or useful public derivations. Use supported native thinking/effort controls rather than private-reasoning transcript requests, preserving existing settings outside authorized migration.
5. Preserve valid paths and stable task-path terminology for the selected runtime.
6. Compare the result with the same task and acceptance criteria, then hand frozen artifacts to fresh-context verification. Record J5 size overages as `REVIEW_REQUIRED` with usefulness rationale; independent review resolves them. A shorter prompt is not evidence of better behavior.

## Quality Checkpoints

- [ ] The edit changed wording, not runtime or topology.
- [ ] No role, rule, config, stamp, validation/preflight, or surface-state change entered the optimization lane.
- [ ] No ownership, mapping, or canonical-policy drift was introduced.
- [ ] Path references and runtime vocabulary stayed valid.
- [ ] A fresh-context verifier, not the optimizer, closes the acceptance gate.

## Examples

### Useful Structure

Keep a document-processing skill’s XML source labels and worked missing-evidence example when they make source attribution testable. Remove a duplicate paragraph only when its requirement remains executable.

### Rejection Case

For `Tighten the reviewer prompt, and also move config ownership to another role`, stop the optimization lane after classification and route the request to restructuring: ownership transfer changes runtime intent, so it exceeds a wording-only edit.

## Sources

Use [current Claude prompting guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) for the selected native model/mode (checked 2026-10-06). A-Team lane boundaries and J5 review are project policy. Codex adaptations use their inventoried native inputs.
