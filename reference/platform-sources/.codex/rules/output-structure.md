---
name: Output Structure
description: Define requested Claude and Codex team surfaces with target-supported runtime profiles
---

# Output Structure

## Applicability

- Applies to: `team-architect`, `agent-writer`, `skill-writer`, `rule-writer`

## Rule Content

### Confirm Format Before Layout

Keep every generated team under `teams/{team-name}/`. Record the requested format, canonical authority, and whether each surface is runnable, activation-gated, or reference-only before generation.

### Required Codex Runnable Layout

For a runnable Codex surface, generate:

- `AGENTS.md` and `docs/RUNTIME-SETUP.md`
- `agents/coordinator.toml` and `agents/{group}/{agent-name}.toml`
- `.codex/config.toml`, `.codex/rules/`, and `.codex/skills/{skill-name}/SKILL.md`
- `.agents/skills/{skill-name}/SKILL.md`
- `.codex/docs/format-mapping.md` and `.codex/docs/format-mapping.manifest.yaml` when mapping is required

Single-agent Codex teams may omit `agents/` and agent registration.

### Required Claude Runnable Layout

For a runnable Claude or dual surface, generate:

- `CLAUDE.md`, `.claude/agents/**/*.md`, `.claude/skills/{skill-name}/SKILL.md`, and `.claude/rules/**/*.md`
- `.claude/settings.json` with top-level `hooks`, `permissions`, and `env`, including the baseline hooks from `.claude/templates/hooks-baseline.json`
- `.claude/output-styles/adhd-friendly.md`, copied verbatim from A-Team, for teams stamped 2026-07-28 or later
- the first-run `outputStyle` ask hook in `.claude/settings.json` for teams stamped 2026-07-28 or later

Declare canonical authority and the generator stamp in `CLAUDE.md`. Apply the output style only to the main-session coordinator. Do not generate these Claude-only runtime artifacts for a Codex-only surface.

### Naming And Entry Documents

- Use kebab-case for team, folder, markdown, TOML, rule, and skill folder names; use stable snake_case runtime identities for agent registry ids.
- Treat `CLAUDE.md`, `AGENTS.md`, and `SKILL.md` as the only uppercase filenames.
- Place coordinator TOML at `agents/coordinator.toml` and specialist TOMLs under `agents/{group}/`.
- Put universal Codex runtime guidance in root `AGENTS.md`; keep role and file constraints in authoritative playbooks or `.codex/rules/`.

### Codex Runtime Config

Every runnable Codex surface includes `.codex/config.toml`. Use `.codex/rules/codex-runtime-config.md` to select the target-supported profile; do not impose A-Team's observed v2 schema on a different client. Preserve the working repo-self v2 config.

- Multi-agent surfaces enable the target-supported collaboration feature and role registration. Record the exact client/schema check and actual lifecycle tools separately.
- Published `agents.max_concurrent_threads_per_session` counts spawned threads excluding root; this host's v2 capacity counts total session slots. Keep each profile's count semantics explicit.
- Preserve host-selected root/unpinned defaults and explicit role model/effort/sandbox pins. Do not restore A-Team's absent root/default-subagent pins.
- Record profile selection in setup/mapping metadata, not invented config keys. Retain protected-path, approval, verification, and rollback guidance.

Treat each `[agents.<id>]` table id as the agent's stable snake_case runtime identity. Require each entry to include `description` and `config_file`. Resolve `config_file` relative to `.codex/`; use `../agents/...` for project-root configs. Require the referenced agent TOML's `name` to equal `<id>` exactly and to also include `description`, `model`, `model_reasoning_effort`, `sandbox_mode`, and nonempty `developer_instructions`.

Default strong roles to `gpt-6-astra`/`xhigh` and read-heavy roles to `gpt-5.6-terra`/`high` only within that scope. Preserve explicit user or target model AND effort pins during unrelated regeneration/restructuring without fresh compatibility approval. A model-only migration preserves existing supported effort unless the authorized scope also changes effort. On A-Team's observed v2 host, full-history forks inherit parent model/effort; use bounded/no-history forks and explicit parameters for role-specific routing. Other targets use their supported lifecycle under `.codex/rules/context-isolation.md`.

### Shared Deliverables

Mirror every Codex skill between `.codex/skills/{skill}/SKILL.md` and `.agents/skills/{skill}/SKILL.md`. Include worklog, context-management, execution-contract, and reasoning/self-critique rules or documented equivalents for multi-agent or multi-phase teams. Keep one adjacent Reasoning/Workflow/Self-Critique contract in each authoritative role; do not add duplicate forms.

Every runnable team must ship `docs/RUNTIME-SETUP.md` after runtime artifacts freeze, with a probe stamp and setup, verify, and rollback steps. Retain both mapping artifacts for multi-surface or conversion-retained teams; record requested format, canonical authority, surface state, platform-only files, lossy conversions, and round-trip notes.

## Violation Determination

- Generation starts without requested format, canonical authority, and surface-state decisions -> Violation
- A requested runnable surface is missing its entry document or artifact tree -> Violation
- `docs/RUNTIME-SETUP.md` is missing, or lacks the probe stamp or the rollback command -> Violation
- `.codex/config.toml` is missing, or the target-supported config check rejects or ignores required fields -> Violation
- a multi-agent team omits its supported collaboration/registration surface, mixes unverified profiles, or conflates capacity accounting -> Violation
- coordinator or specialist TOML placement breaks the rules above -> Violation
- an agent registry entry is incomplete or its `config_file` does not resolve from `.codex/` -> Violation
- an `[agents.<id>]` table id is not a stable snake_case runtime identity, or its referenced agent TOML's `name` does not equal `<id>` exactly -> Violation
- an agent TOML misses a required runtime key -> Violation
- a skill exists only in `.codex/skills/` or only in `.agents/skills/` -> Violation
- a Claude runnable surface omits `.claude/settings.json`, any required top-level key, or baseline hooks -> Violation
- a Claude runnable team stamped 2026-07-28 or later omits `.claude/output-styles/adhd-friendly.md` or the first-run `outputStyle` hook -> Violation
- a Codex-only surface includes Claude-only runtime artifacts -> Violation
- mapping artifacts are required but missing, or omit canonical authority, surface state, or platform-only files -> Violation
- required process rules are missing without documented equivalents -> Violation
- file or folder names break naming conventions -> Violation

## Exceptions

Single-agent teams may omit `agents/`, `[agents]` registration, and coordinator TOML.
