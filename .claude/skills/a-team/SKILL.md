---
name: A-Team
description: Entry point that makes this session adopt the Team Architect workflow to run the full team design process
disable-model-invocation: true
allowed-tools: ["Agent"]
argument-hint: "[team description | existing-team request]"
---

# A-Team

## Description

Adopt the Team Architect workflow in the current session and run the full A-Team process: Phases 1-6 for a new team, or the correct existing-team lane for optimization or restructuring.

## Users

- Main-session invocation of `/A-Team`

## Core Knowledge

- A-Team repo-self keeps `.claude/` as its canonical source; its Codex surfaces are regenerated projections.
- Generated teams do not inherit A-Team's canonical authority automatically. Discovery must confirm each generated team's requested format, and existing-team work must respect the target team's own canonical declaration.
- Existing-team work starts with deterministic classification: direct `teams/*` root, layout, runnable surfaces, activation or reference-only state, generation stamp, canonical authority, and mapping state.
- The optimization lane is text-only. Any structural, runtime, ownership, mapping, canonical-authority, or parity change belongs to restructuring.
- A `Codex-only runtime gap` stays inside already-allowed platform-only surfaces. A `cross-platform design gap` starts at the target team's canonical source and regenerates only affected projections.

## Application Guide

1. If `/A-Team` is invoked inside a dispatched task instead of the main user session, stop and return `BLOCKED: wrong-context invocation - /A-Team must run in the main session.`
2. Read `CLAUDE.md` and `.claude/agents/team-architect.md`, then adopt that workflow for the rest of the task.
3. Initialize the worklog and keep the dialogue log current.
4. For a new team, stay in Discovery until objective, scope, workflow, role coverage, requested format, execution mode, and requirements summary are explicitly confirmed.
5. For an existing team, classify the target before proposing changes. If canonical authority is ambiguous, limit work to assessment until it is confirmed.
6. Route text-only Codex prompt improvements that leave roles, rules, runtime, ownership, mapping, canonical authority, and parity unchanged to `prompt-optimizer`.
7. Route every structural, runtime, ownership, mapping, canonical-authority, or parity change to `team-restructuring-master`, then require recommendation audit and user approval before implementation.
8. When a generator defect is discovered while working on an existing team, backport the fix to A-Team's canonical `.claude/` design and regenerate the affected Codex projections in the same maintenance task.

## Quality Checkpoints

- [ ] New-team work did not bypass Discovery.
- [ ] Existing-team work recorded classification, stamp, canonical authority, and mapping state before mutation.
- [ ] Reference-only or activation-gated surfaces were not promoted implicitly.
- [ ] Optimization stayed text-only; restructuring handled every runtime or parity change.
- [ ] A-Team repo-self canonical policy was not confused with the generated team's canonical policy.

## Example

### Input

`/A-Team optimize teams/content-studio handoff wording without changing roles or runtime`

### Output

Classify `teams/content-studio`, confirm its canonical authority and mapping state, then route the request through the text-only optimization lane instead of restructuring.
