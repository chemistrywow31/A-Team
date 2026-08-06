---
name: Structured Interview
description: Extract precise team requirements through staged, single-direction questioning
---

# Structured Interview

## Description

Extract precise team requirements through staged, single-direction questioning that confirms requested format, canonical policy, workflow, and operating constraints before planning starts.

## Users

- `.codex/agents/discovery/requirements-analyst.md`
- `.codex/agents/team-architect.md`

## Core Knowledge

- Discovery is format-neutral. Do not assume Codex or Claude is the canonical target for a generated team.
- A-Team repo-self uses `.claude/` as its own canonical source, but generated teams can be Claude-canonical, Codex-canonical, dual, or not yet confirmed.
- Existing-team requests need two clarifications: the user-visible change type and the target team's actual classified state.
- One response should move only one discovery direction at a time.

## Application Guide

1. Start by identifying whether the request is for a new team or an existing team.
2. Confirm the requested delivery format, runnable surfaces, and whether mapping or conversion artifacts must be retained.
3. If the request targets an existing team, ask for the exact path and whether the user expects text-only optimization or structural/runtime/parity change. Do not assume canonical authority until classification confirms it.
4. Ask for the objective and how success will be judged.
5. Ask what the team must not do so scope is bounded by exclusion as well as inclusion.
6. Ask for the workflow and handoff sequence, not just the desired outcome.
7. Ask for role coverage, execution mode, shared-worktree risks, and any task-path or ownership constraints that affect coordination.
8. After several rounds, play back a concise requirements summary and ask for explicit confirmation before moving to planning.

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
