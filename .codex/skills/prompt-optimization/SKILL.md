---
name: Prompt Optimization
description: Rewrite generated prompts to be sharper, shorter, and more executable without changing meaning
---

# Prompt Optimization

## Description

Improve prompt wording while preserving the original role, workflow, runtime intent, ownership model, and canonical policy.

## Users

- `.codex/agents/optimization/prompt-optimizer.md`
- `.codex/agents/team-architect.md`

## Core Knowledge

- The optimization lane is text-only. It can tighten wording, make triggers explicit, normalize terminology, and remove redundancy.
- It cannot change roles, rules, topology, runtime or config, ownership, mapping, canonical authority, parity, stamps, validation/preflight requirements, or any surface's runnable, reference-only, or activation state.
- Existing-team optimization still starts with target classification so the optimizer knows the target surface, stamp, canonical authority, and mapping state.
- Plain prompt copy-editing on an already-runnable surface remains text-only when it preserves every structural item and the surface's state.
- If a requested change alters any structural item or changes surface state, it belongs to restructuring instead.
- Preserve current runtime vocabulary. Do not reintroduce retired follow-up wording or generic join instructions into Codex-facing text.

## Application Guide

1. Confirm that the request is in the optimization lane and classify the target if an existing team is involved.
2. Stop and hand the task to `team-restructuring-master` when the requested change affects roles, rules, topology, runtime or config, ownership, mapping, canonical authority, parity, stamps, validation/preflight requirements, or a surface's runnable, reference-only, or activation state.
3. Rewrite only owned text to make responsibilities, triggers, completion criteria, and uncertainty handling more explicit.
4. Replace vague verbs with concrete actions, remove repeated explanations, and keep imperative structure where it improves execution.
5. Preserve valid paths, stable task-path terminology, and mirror parity for any Codex skill text that is touched.
6. Hand optimized artifacts to fresh-context verification instead of self-accepting the result.

## Quality Checkpoints

- [ ] The edit changed wording, not runtime or topology.
- [ ] No role, rule, config, stamp, validation/preflight, or surface-state change entered the optimization lane.
- [ ] No ownership, mapping, or canonical-policy drift was introduced.
- [ ] Path references and runtime vocabulary stayed valid.
- [ ] Retired follow-up wording or generic join instructions were not added back to Codex-facing text.
- [ ] A fresh-context verifier, not the optimizer, closes the acceptance gate.

## Examples

### Rejection Case

For `Tighten the reviewer prompt, and also move config ownership to another role`, stop the optimization lane after classification and route the request to restructuring: ownership transfer changes runtime intent, so it exceeds a wording-only edit.
