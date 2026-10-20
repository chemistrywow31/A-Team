---
name: structured-interview
description: Provide in-depth interview methodology for extracting clear actionable requirements from vague descriptions
---

# Structured Interview

## Description

Extract precise team requirements through staged, single-direction questioning that confirms requested format, canonical policy, workflow, and operating constraints before planning starts.

## Users

- `requirements-analyst`
- `team-architect`

## Core Knowledge

- Discovery is format-neutral. The supported runnable delivery on this branch is Grok-native; confirm it explicitly rather than treating AGENTS.md alone as proof of platform.
- A-Team repo-self uses `AGENTS.md` plus `.grok/`. Generated teams retain their declared authority; foreign and multi-surface inputs require explicit conversion scope before native activation. The archive is not a runnable delivery.
- Existing-team requests need two clarifications: the user-visible change type and the target team's actual classified state.
- One response should move only one discovery direction at a time.

## Application Guide

1. Start by identifying whether the request is for a new team or an existing team.
2. Confirm the requested delivery format, runnable surfaces, and whether mapping or conversion artifacts must be retained.
3. If the request targets an existing team, reuse its supplied exact path and requested change; ask only for what is materially missing. Classify text-only optimization versus structural/runtime/parity change. Do not assume canonical authority until classification confirms it.
4. Ask for the objective and how success will be judged.
5. Ask what the team must not do so scope is bounded by exclusion as well as inclusion.
6. Ask for the workflow and handoff sequence, not just the desired outcome.
7. Ask for role coverage, execution mode, shared-worktree risks, and any task-path or ownership constraints that affect coordination.
8. Play back a concise requirements summary before planning. Reuse confirmation and delegated routine decisions already supplied; ask only when a material choice remains unresolved. Existing scoped maintenance uses classification instead of repeating new-team discovery.

## Quality Checkpoints

- [ ] Requested format and runnable surfaces were confirmed explicitly.
- [ ] Canonical authority was confirmed or marked ambiguous instead of assumed.
- [ ] Workflow, scope exclusions, and role coverage were captured separately.
- [ ] Existing-team requests distinguished text-only optimization from structural/runtime/parity change.
- [ ] The final requirements summary is specific enough for planning without further interpretation.

## Example

### Input

`I want A-Team to improve an existing research team.`

### Output

Ask for the exact team path, then ask whether the user wants text-only prompt optimization or a structural/runtime/parity change, and only after that confirm the desired format and canonical authority.

## Rejection Case

For “improve the A-Team skill planner,” reject a demand to inventory or migrate every generated team. This is capability maintenance; use a bounded read-only example only when needed to reproduce the defect.

## Source Attribution

- **Origin**: A-Team canonical skill, preserved at `reference/platform-sources/.claude/skills/structured-interview/SKILL.md`.
- **Integration**: Pattern B: Adapted Install; native Grok branch authority is `AGENTS.md` plus `.grok/`.
- **Retrieved**: 2026-10-20 from the verified base snapshot.
- **Modifications**: Native paths, loading and lifecycle; preserved task intent, examples and useful assets. Archive is reference-only.
