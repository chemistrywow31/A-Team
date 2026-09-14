---
name: Codex Runtime Config
description: Require current project-local Codex v2 config, protected-path awareness, and no home-directory dependency
---

# Codex Runtime Config

## Applicability

- Applies to: `team-architect`, `agent-writer`, `runtime-preflight-advisor`, and every generated Codex runnable surface

## Rule Content

### Use Project-Local `.codex/config.toml`

- Generated Codex teams must boot from `teams/{team-name}/.codex/config.toml`.
- `codex exec --strict-config` must load that file without unknown-field or deprecated-field errors.
- Do not require users to edit `~/.codex/config.toml` for baseline execution.

### Use The Current V2 Multi-Agent Schema

Require this schema for Codex multi-agent surfaces. Model/effort values shown are defaults for new teams without explicit pins or explicitly authorized profile migration; they remain A-Team's approved repo-self profile. Preserve explicit user or target model AND effort pins during unrelated regeneration/restructuring without fresh compatibility approval. A model-only migration preserves existing supported effort unless the authorized scope also changes effort.

```toml
model = "gpt-6-astra"
model_reasoning_effort = "xhigh"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
project_doc_fallback_filenames = ["CLAUDE.md"]

[features]
multi_agent = true

[features.multi_agent_v2]
enabled = true
max_concurrent_threads_per_session = 7
expose_spawn_agent_model_overrides = true
wait_agent_enabled = true

[agents]
enabled = true
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "high"
interrupt_message = true

[agents.coordinator]
description = "Coordinate delegation, quality gates, and delivery."
config_file = "../agents/coordinator.toml"
```

Do not generate or keep stale v1 fields such as `disable_response_storage`, `max_threads`, or `max_depth`.

### Register Agents Relative To `.codex/`

- Resolve every `config_file` relative to the `.codex/` directory.
- For project-root runtime TOMLs, register `../agents/...`.
- Each `[agents.{id}]` entry must include `description` and `config_file`.

### Respect Approval And Protected-Path Limits

- Use `approval_policy = "on-request"` and `sandbox_mode = "workspace-write"` unless a stricter user requirement applies.
- Standard `workspace-write` protects `.codex/` and `.agents/`. Project config must not claim it can authorize rewriting its own protected metadata or bypass host approval.
- Runtime-affecting changes must document setup, verify, and rollback guidance in `docs/RUNTIME-SETUP.md`.

### Model Defaults Belong In Config

- Within the default/migration scope above, root and strong roles default to `gpt-6-astra`/`xhigh` and subagents to `gpt-5.6-terra`/`high`; explicit target model/effort pins take precedence.
- Every `agents/**/*.toml` declares explicit model/effort. For role-specific dispatch routing, pass explicit `spawn_agent` model/effort with `fork_turns = "none"` or a positive bounded fork; full-history forks inherit the parent.

## Violation Determination

- A Codex runnable surface has no project-local `.codex/config.toml`, or `codex exec --strict-config` rejects it -> Violation
- A multi-agent Codex config omits `[features.multi_agent_v2]`, omits required v2 keys, or still uses `disable_response_storage`, `max_threads`, or `max_depth` -> Violation
- A generated Codex team requires editing `~/.codex/config.toml` for baseline execution -> Violation
- Any `[agents.{id}]` entry resolves `config_file` from the wrong base path or omits `description` -> Violation
- A rule or setup document claims project config can bypass protected metadata restrictions on `.codex/` or `.agents/` -> Violation
- Approval guidance defaults to `on-failure` or `never` without explicit user approval and recorded rationale -> Violation

## Exceptions

- Claude-only or reference-only surfaces are out of scope.
- A single-agent Codex surface may omit the multi-agent v2 block and agent registry.
- A user-approved tighter runtime profile is allowed when strict-config still passes and the rationale is recorded.
