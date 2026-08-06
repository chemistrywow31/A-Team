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

For current A-Team and generated Codex multi-agent surfaces, use:

```toml
model = "gpt-5.6-sol"
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

- Root or project default guidance is `gpt-5.6-sol` at `xhigh`.
- Default subagent guidance is `gpt-5.6-terra` at `high`.
- Role-specific overrides belong in `agents/**/*.toml` or explicit `spawn_agent` parameters, not only in prose.

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
