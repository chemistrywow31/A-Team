---
name: Output Structure
description: Define what a generated team ships for its work shape, requested runtime surfaces, and mapping artifacts
paths:
  - "teams/**"
---

# Output Structure

## Applicability

- Applies to: `team-architect`, `agent-writer`, `skill-writer`, `rule-writer`

## Rule Content

### Generated Deliverables Live Under `teams/{team-name}/`

Before generation, Discovery confirms the work shape (`.claude/skills/work-shape/SKILL.md`) and the delivery format: `codex-native`, `claude-compatible`, `dual-format`, or `let A-Team decide`.

Every team records its shape decision in `docs/work-shape.json`, and its entry document declares the team's canonical authority and carries the generator stamp. The shape selects what else ships. `scripts/validate-team.sh` and `scripts/validate_codex_team.py` enforce the lists below, so read their output rather than a longer description here.

### Skill-Workflow Team

One agent that loads skills. For a Claude surface:

- `CLAUDE.md`: what the project is for, plus gotchas
- `.claude/skills/{skill-name}/SKILL.md`, with `references/` for detail that is loaded on demand
- `.claude/settings.json` from `.claude/templates/settings-baseline.json`, keeping its `ask` and `deny` lists; `hooks` holds only the first-run output-style hook unless a flow needs another
- `.claude/output-styles/adhd-friendly.md`, copied verbatim
- `docs/work-shape.json` and `docs/RUNTIME-SETUP.md`

It has no agent definitions, no coordinator entry skill, and no rule pack. Add a rule only for a constraint that must load by path and cannot live in a skill.

For a Codex surface: `AGENTS.md`, `.agents/skills/` with its `.codex/skills/` mirror, `docs/work-shape.json` and `docs/RUNTIME-SETUP.md`. `.codex/config.toml` is optional and no agent registry is needed.

### Agent-Group Team

A coordinator in the main session plus the roles the record's triggers justify. For a Claude surface, everything a skill-workflow team ships, and:

- `.claude/agents/{coordinator}.md` in the agents root and specialists in group subfolders
- one coordinator entry skill that makes the main session adopt the coordinator playbook
- one short handoff contract rule written for this team (`execution-contract.md` or `handoff-contract.md`): what a dispatch carries, what a return carries, who accepts
- a `CLAUDE.md` deployment section stating that the coordinator runs in the main session and is never spawned
- other rules, a worklog, and hooks beyond the first-run hook only when a flow needs them

For a Codex surface: `AGENTS.md`, `agents/coordinator.toml`, `agents/{group}/{agent-name}.toml`, `.codex/config.toml`, `.codex/rules/`, `.codex/skills/` with its `.agents/skills/` mirror, and `docs/RUNTIME-SETUP.md`.

### Apply The Selected Runtime's Specification

For Claude output, apply `.claude/rules/settings-json.md`, `.claude/rules/hooks-integration.md` and `.claude/rules/frontmatter-optional-patterns.md`. A Claude-only target does not require Codex runtime checks.

Only when the output includes a runnable Codex surface, read `.codex/rules/codex-runtime-config.md`, `.codex/rules/codex-agent-config-patterns.md` and `.codex/rules/context-isolation.md`, and validate that surface against them without copying their content into Claude guidance.

Keep explicit user or target model and effort pins during unrelated regeneration or restructuring.

### Naming And Placement

- Team, folder and rule names use kebab-case. Codex agent registry ids use snake_case.
- `CLAUDE.md`, `AGENTS.md` and `SKILL.md` are the only uppercase filenames.

### Mapping Artifacts

A multi-surface or conversion-retained team ships `.codex/docs/format-mapping.md` and `.codex/docs/format-mapping.manifest.yaml`, recording format, authority, runnable or reference-only state, platform-only files, path mappings, lossy steps and reverse strategy. A dual-format team ships both runnable surfaces or marks one reference-only.

### Runtime Setup Advisory

Every runnable team ships `docs/RUNTIME-SETUP.md` after runtime artifacts freeze, with a probe stamp, setup and verification steps, rollback, and any approval limits the user must handle before first run.

## Violation Determination

- Generation starts without a recorded work shape, delivery format and canonical authority -> Violation
- The tree contradicts the work-shape record, or the record breaks the shape rule -> Violation
- A skill-workflow team ships agent definitions, a coordinator entry, or a copied rule pack -> Violation
- An agent-group team lacks its coordinator, entry skill, handoff contract, or main-session statement -> Violation
- A Claude surface omits `.claude/settings.json`, drops the baseline `ask` or `deny` entries, or omits the output style and its first-run hook -> Violation
- A Claude-only delivery is gated on Codex checks, or a target's model or effort pins change outside authorization -> Violation
- A multi-surface or conversion-retained team omits either mapping artifact -> Violation
- `docs/RUNTIME-SETUP.md` is missing, or lacks a probe stamp, verification steps or rollback -> Violation

## Exceptions

- Single-surface teams need no mapping artifacts unless the user asks for conversion retention.
- Teams stamped before 2026-11-26 without a work-shape record are validated against the contract they were built under. Teams stamped before 2026-07-28 need no output style.
