---
name: A-Team
description: Start the A-Team Codex coordinator workflow for designing or restructuring teams
---

# A-Team

## Description

Use this skill when the user asks A-Team to design, generate, review, optimize, or restructure an agent team in the Codex runtime.

## Users

- `.codex/agents/team-architect.md`
- Users invoking A-Team with `$a-team`, `A-Team`, or equivalent wording

## Core Knowledge

- `AGENTS.md` is the Codex runtime contract and `.codex/agents/team-architect.md` is the coordinator playbook.
- A-Team repo-self keeps `.claude/` as its canonical source, but generated teams can declare Claude, Codex, dual, or another explicit canonical policy.
- Existing-team work starts with deterministic classification: target root, layout, runnable surfaces, activation or reference-only state, generation stamp, canonical authority, and mapping state.
- `prompt-optimizer` owns text-only Codex improvements that leave roles, rules, runtime, ownership, mapping, canonical authority, and parity unchanged.
- `team-restructuring-master` owns every structural, runtime, ownership, mapping, canonical-authority, or parity change and classifies `Codex-only runtime gap` versus `cross-platform design gap`.

## Application Guide

1. Read `AGENTS.md`.
2. Read `.codex/agents/team-architect.md`.
3. For a new team, stay in Discovery until objective, scope, workflow, role coverage, requested format, execution mode, canonical authority, and requirements summary are explicitly confirmed.
4. For an existing team, classify the target before mutating it. If canonical authority is ambiguous, limit work to assessment until it is confirmed.
5. Route text-only Codex prompt improvements to `prompt-optimizer`; route every structural/runtime/parity change to `team-restructuring-master`, then require recommendation audit and user approval before implementation.
6. Give every dispatch a stable phase-purpose task path plus owned paths, forbidden paths, acceptance criteria, and the shared-filesystem non-reversion rule.
7. Use `spawn_agent` for a new bounded task, `send_message` for a non-triggering update, `followup_task` for a new or corrective turn on an existing idle agent, `interrupt_agent` only when work is invalidated or unsafe, `list_agents` before routing or join decisions, and `wait_agent` only at a real join boundary.
8. Respect the target team's own canonical declaration, mapping artifacts, and reference-only surfaces. If a generator defect is discovered, fix A-Team's canonical `.claude/` source and then regenerate the affected Codex projection.

## Quality Checkpoints

- [ ] Discovery stayed open for new teams until requirements were explicitly confirmed.
- [ ] Existing-team work recorded classification, stamp, canonical authority, and mapping state before mutation.
- [ ] Reference-only or activation-gated surfaces were not promoted implicitly.
- [ ] Optimization stayed text-only; restructuring handled every runtime or parity change.
- [ ] Task paths, lifecycle tools, and shared-filesystem ownership rules were applied consistently.

## Example

### Input

`$a-team optimize teams/content-studio handoff wording without changing roles or runtime`

### Output

Classify `teams/content-studio`, confirm its canonical authority and mapping state, then route the request through the text-only optimization lane instead of restructuring.
