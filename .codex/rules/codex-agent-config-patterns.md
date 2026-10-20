---
name: Codex Agent Config Patterns
description: Define current TOML patterns, model tiers, and sandbox posture for Codex agent configs
---

# Codex Agent Config Patterns

## Applicability

- Applies to: `agent-writer`, `team-architect`, and every generated Codex multi-agent runtime

## Rule Content

### Required TOML Shape

A-Team requires these fields in generated role configs; distinguish this authoring floor from the target client's native optional fields. Model/effort values illustrate the scoped defaults under Current Model Guidance:

```toml
name = "process_reviewer"
description = "Audit coordination quality and produce a retrospective report."
model = "gpt-6-astra"
model_reasoning_effort = "xhigh"
sandbox_mode = "read-only"

developer_instructions = """
Read `AGENTS.md`, then read `.codex/agents/review/process-reviewer.md` and follow it as the authoritative playbook for this role.
"""
```

Keep TOMLs thin: runtime keys plus a nonempty bootstrap to the same-relative authoritative playbook. Map `agents/{path}.toml` to `.codex/agents/{path}.md`. Do not copy the full playbook into `developer_instructions`.
Validate required role sections in the authoritative playbook; validate the TOML bootstrap only for nonempty content and a resolvable same-relative target.

### Standalone MCP Shape

- Treat every agent TOML as a standalone config: each `[mcp_servers.<id>]`, even when `enabled = false`, must define exactly one transport using nonempty stdio `command` plus applicable `args`, or nonempty streamable-HTTP `url`.
- Include explicit `enabled` state and the role's complete approved tool/posture fields: tool allow/deny lists, default or per-tool approval modes, and any required startup, timeout, environment, or authentication settings. A partial `enabled` override is invalid.
- Treat child MCP configuration as a config layer, not a hard isolation boundary. Parent live runtime tools can be reapplied after the layer, so child-side disable/deny settings and child-only enabled servers do not prove the effective namespace.
- When a role must never see a parent tool, remove it from the parent surface or launch the role in an independent process/session that disables the server and nested agents at startup. Accept only actual live tool enumeration as isolation evidence.
- Strict-config acceptance requires process success plus zero diagnostics that any role or agent config was malformed, had an invalid transport, failed to load, or was ignored. Do not treat a notice caused solely by intentional `--ignore-user-config` as an agent-config failure.

### Registry And Discovery

- Runtime TOMLs live under `agents/`.
- `.codex/config.toml` registers them through `[agents.<id>]` entries whose `config_file` paths resolve relative to `.codex/`.
- Treat each `[agents.<id>]` table id as the agent's stable snake_case runtime identity, matching the role and task-path vocabulary.
- Require the referenced agent TOML's `name` to equal `<id>` exactly; do not substitute a display name.

### Current Model Guidance

- Preserve the host-selected root and unpinned defaults; A-Team has no project root/default-subagent model or effort pins. Its explicit strong-role `gpt-6-astra`/`xhigh` and read-heavy-role `gpt-5.6-terra`/`high` pins remain. Use those role defaults for new unpinned teams, not as a mandate to add root/default pins; validate against the target-supported runtime profile.
- Preserve explicit user or target model AND effort pins during unrelated regeneration/restructuring; retaining a pin, including `gpt-5.4`, requires no fresh compatibility approval. A model-only migration preserves existing supported effort unless the authorized scope also changes effort.

### Sandbox Posture

- Roles that mutate repo artifacts use `workspace-write`; reviewer, auditor, and verifier roles that only inspect artifacts use `read-only`.
- A review or probe role may use `workspace-write` only when its owned artifact set explicitly includes a report path or runtime advisory it must write and the approved runtime policy permits it. Preserve existing sandbox pins. If its live sandbox blocks persistence, use execution-contract EC-1.12 `INLINE-FALLBACK` with a dispatch cap and coordinator persistence; do not bypass or broaden permissions.

### Coordinator Playbook Requirements

- The authoritative coordinator playbook under `.codex/agents/` must include direct specialist topology, stable task-path strategy, follow-up/interrupt/join rules, the shared-filesystem non-reversion rule, quality gates, and a completion contract.

### Specialist Playbook Requirements

- The authoritative specialist playbook under `.codex/agents/` includes Identity, Responsibilities, Input and Output, the adjacent H2 Reasoning/Workflow/Self-Critique sequence, Uncertainty Protocol, Examples with at least one meaningful boundary case and any useful positive/contrast cases, Completion Contract, File Ownership, and Boundaries. Keep the J5.1 floors and role-specific checks; omit duplicate Preflight/Verification forms and mandatory four/five slots.

### Fork Override Constraint

The following describes A-Team's observed v2 host. For other targets, select and verify their lifecycle/profile under `context-isolation.md`; do not claim these fork parameters are a universal CLI API.

- Full-history forks inherit the parent model and reasoning effort; any explicit `spawn_agent` model or reasoning override requires `fork_turns = "none"` or a positive bounded fork.
- Do not rely on omitted or `all` forks when overriding model or effort.
- Use explicit model/effort and bounded/no-history forks for effective role-specific routing; selecting a pinned role does not prove that its pin overrides full-history inheritance.

### Verification

- Parse every registered agent TOML in isolation, resolve its playbook bootstrap, and run the target through strict-config when available.
- For every claimed role-specific tool restriction, probe a fresh live role context and compare the actual namespace with the declared allowlist; do not infer visibility from TOML text.
- Fail verification on a malformed/invalid-transport/failed-load/ignored-role diagnostic even when the command exits zero and prints `CONFIG_OK`; retain only bounded, redacted diagnostic evidence.

## Violation Determination

- An agent TOML misses `name`, `description`, `model`, `model_reasoning_effort`, `sandbox_mode`, or `developer_instructions` -> Violation
- An agent TOML contains an MCP entry with no transport, both transports, only an `enabled` override, or incomplete role-approved tool/posture fields -> Violation
- A role-isolation claim relies on child `enabled = false`, `disabled_tools`, a narrower child `enabled_tools`, or a child-only enabled server while the parent live namespace differs, without independent-process isolation and a live namespace probe -> Violation
- `developer_instructions` is empty, omits the same-relative `.codex/agents/{path}.md` bootstrap target, or names a missing target -> Violation
- A registry entry points outside the intended TOML path or does not resolve from `.codex/` -> Violation
- A `[agents.<id>]` table id is not a stable snake_case runtime identity, or its referenced agent TOML's `name` does not equal `<id>` exactly -> Violation
- A default overrides explicit user/target model or effort pins outside authorized migration, or retaining a pin triggers fresh compatibility approval -> Violation
- A reviewer or verifier uses `workspace-write` without an owned write artifact, or a writer role claims mutable outputs under `read-only` without an approved persistence handoff -> Violation
- The authoritative coordinator playbook omits topology, task-path, join, or non-reversion guidance -> Violation
- The authoritative specialist playbook omits completion contract, file ownership, or boundaries -> Violation
- A dispatch pattern claims model or effort override on a full-history fork -> Violation
- Strict config exits successfully or prints `CONFIG_OK` while reporting a malformed, invalid-transport, failed-load, or ignored role/agent config -> Violation

## Exceptions

- If Codex runtime schema changes, update this rule and the mapping docs in the same change.
- Deterministic utility roles may use an approved lower model/effort with a recorded rationale, but retain explicit TOML runtime fields.
