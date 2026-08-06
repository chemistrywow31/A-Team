---
name: Output Structure
description: Define required generated-team surfaces, Codex v2 runtime layout, and per-format mapping artifacts
paths:
  - "teams/**"
---

# Output Structure

## Applicability

- Applies to: `team-architect`, `agent-writer`, `skill-writer`, `rule-writer`

## Rule Content

### Generated Deliverables Live Under `teams/{team-name}/`

Discovery must confirm the requested delivery format before generation: `codex-native`, `claude-compatible`, `dual-format`, or `let A-Team decide`.

Every generated team must record its requested delivery format, canonical authority, runnable or activation state, and mapping artifacts needed for regeneration or future conversion.

### Required Surface Layouts

#### Claude Runnable Surface

If the requested format includes a runnable Claude surface, generate:

- `CLAUDE.md` at team root
- `.claude/agents/**/*.md`
- `.claude/skills/{skill-name}/SKILL.md`
- `.claude/rules/**/*.md`
- `.claude/settings.json` with the required `hooks`, `permissions`, and `env` keys and the baseline hook set from `.claude/templates/hooks-baseline.json`
- `.claude/output-styles/adhd-friendly.md`, copied verbatim from A-Team's canonical output style
- the first-run `outputStyle` ask hook from `.claude/templates/hooks-baseline.json` inside `.claude/settings.json`

The Claude surface entry document must declare the team's canonical authority and carry the generator stamp.
The output style and first-run hook are mandatory for teams stamped 2026-07-28 or later. They shape the main-session coordinator output only; do not apply them to specialist EC reports or add them to a Codex-only surface.

#### Codex Runnable Surface

If the requested format includes a runnable Codex surface, generate:

- `AGENTS.md` and `docs/RUNTIME-SETUP.md`
- `agents/coordinator.toml` and `agents/{group}/{agent-name}.toml`
- `.codex/config.toml`, `.codex/rules/`, and `.codex/skills/{skill-name}/SKILL.md`
- `.agents/skills/{skill-name}/SKILL.md`
- `.codex/docs/format-mapping.md` and `.codex/docs/format-mapping.manifest.yaml` when mapping artifacts are required

The Codex surface entry document must declare the team's canonical authority and carry the generator stamp.

#### Dual-Format Teams

Dual-format teams must ship both runnable surfaces or explicitly mark one as reference-only. They must also ship the mapping artifacts in `.codex/docs/`.

### Current Codex V2 Runtime Requirements

Every generated Codex multi-agent surface must use the current strict-valid v2 config schema: project-local `.codex/config.toml`; root `gpt-5.6-sol` at `xhigh`; project-local approval and sandbox posture; `features.multi_agent = true`; seven total slots including root; model-override exposure; bounded wait support; and default subagents on `gpt-5.6-terra` at `high`. Do not use stale v1 keys such as `disable_response_storage`, `max_threads`, or `max_depth`.

Treat each `[agents.<id>]` table id as that agent's stable snake_case runtime identity. Each registration must resolve `config_file` relative to `.codex/`, and the referenced agent TOML's `name` must equal `<id>` exactly. Project-root agent configs therefore register as `../agents/...`.

### Naming And Placement

- Team, folder, and rule names use kebab-case.
- Agent registry ids use snake_case.
- `CLAUDE.md`, `AGENTS.md`, and `SKILL.md` are the only uppercase filenames.
- The Codex coordinator TOML lives at `agents/coordinator.toml`.
- Non-coordinator Codex agent TOMLs live under `agents/{group}/`.

### Mapping Artifacts

For a multi-surface or conversion-retained team, generate `.codex/docs/format-mapping.md` and `.codex/docs/format-mapping.manifest.yaml`. Record requested format, canonical authority, runnable vs reference-only state, platform-only files, path mappings, lossy steps, and reverse strategy.

### Runtime Setup Advisory

Every runnable team must ship `docs/RUNTIME-SETUP.md` after runtime artifacts freeze. Include a probe stamp, setup, verification, rollback, and any protected-path or approval-policy limits required before first run.

## Violation Determination

- Generation starts without a recorded requested format and canonical-authority decision -> Violation
- A requested runnable surface is missing its required entry document or artifact tree -> Violation
- A Claude runnable surface omits `.claude/settings.json`, any required top-level key, or the baseline hook set -> Violation
- A Claude runnable team stamped 2026-07-28 or later omits `.claude/output-styles/adhd-friendly.md` or the first-run `outputStyle` hook -> Violation
- A Codex runnable surface omits the v2 config block above, uses deprecated v1 keys, or resolves `config_file` from the wrong base path -> Violation
- A `[agents.<id>]` table id is not a stable snake_case runtime identity, or its referenced agent TOML's `name` does not equal `<id>` exactly -> Violation
- A multi-surface or conversion-retained team omits either mapping artifact, or the artifacts omit canonical authority, activation state, or platform-only files -> Violation
- `docs/RUNTIME-SETUP.md` is missing, or lacks a probe stamp, verify steps, or rollback steps -> Violation
- File or folder names break the naming and placement rules above -> Violation

## Exceptions

- Single-surface teams do not need mapping artifacts unless the user explicitly requests future conversion retention.
- Single-agent Codex teams may omit `agents/` and the multi-agent v2 block.
