---
name: Codex Runtime Config
description: Select target-supported project-local Codex profiles with explicit runtime evidence and protected-path limits
---

# Codex Runtime Config

## Applicability

- Applies to: `team-architect`, `agent-writer`, `runtime-preflight-advisor`, and every generated Codex runnable surface

## Rule Content

### Use Project-Local Configuration

- Generate `.codex/config.toml` at the authorized team root; do not require home-config edits for baseline execution.
- Select the schema from the target's installed client and available capabilities. Use `codex exec --strict-config` when that client supports it; otherwise run the supported config check and record the unavailable check explicitly.
- Record client/version, config-validation result, actual lifecycle tools, capacity accounting, and model-access evidence separately in `docs/RUNTIME-SETUP.md`. A parsed config does not prove live tools or model access, and a persisted change does not reconfigure an already-running session.

### Select One Supported Multi-Agent Profile

The [published configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), checked 2026-10-06, documents the portable CLI profile below. Its capacity counts spawned threads, excluding the primary thread. This illustrative cap is not a universal default:

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"
project_doc_fallback_filenames = ["CLAUDE.md"]

[features]
multi_agent = true

[agents]
enabled = true
max_concurrent_threads_per_session = 6
interrupt_message = true

[agents.coordinator]
description = "Coordinate delegation, quality gates, and delivery."
config_file = "../agents/coordinator.toml"
```

A-Team's installed Codex 0.160.1 and active host support a distinct v2 profile. Preserve the working repo-self config; published omission of v2 is not evidence that this installed profile is invalid. Its observed block is:

```toml
[features.multi_agent_v2]
enabled = true
max_concurrent_threads_per_session = 7
expose_spawn_agent_model_overrides = true
wait_agent_enabled = true
```

The current host reports seven total session slots including root. Do not copy that number into the portable spawned-thread field as if accounting were identical. For a future target, use v2 only when its client and live tools support it; otherwise use its supported documented profile. Do not combine profile snippets blindly, create a mandatory overlay, or invent profile-marker keys in config; record the selection in mapping/setup metadata. Validate legacy fields against that client: published `agents.max_threads` is an alias, not universally invalid. Prefer current supported keys for new output; unsupported keys fail validation.

### Preserve Model And Effort Choices

- A-Team deliberately omits root `model`/`model_reasoning_effort` and `agents.default_subagent_*` pins. The host selects the root and unpinned defaults. Do not restore removed defaults during maintenance.
- Preserve explicit target model AND effort pins. A model-only migration preserves supported effort unless changing effort is authorized. Retaining a pin needs no fresh compatibility approval; schema validity and actual access are separate checks.
- Keep each A-Team role TOML's explicit model/effort. New unpinned strong roles use the approved `gpt-6-astra`/`xhigh` profile and bounded read-heavy roles `gpt-5.6-terra`/`high`; these are team design choices, not universal vendor defaults or root pins. A future authorized tier migration should compare quality, latency, and cost on representative tasks before replacing them.
- Use the target's actual fork/override semantics under `context-isolation.md`; public CLI defaults do not prove this host's effective role routing.

### Register Agents Relative To The Declaring Config

- Resolve project role `config_file` paths from `.codex/`; project-root TOMLs use `../agents/...`.
- Every `[agents.<id>]` registration includes `description` and `config_file`; validate its standalone config and authoritative playbook under `codex-agent-config-patterns.md`.

### Respect Approval And Protected Paths

- For new interactive teams, default to `on-request` and `workspace-write`; preserve existing target permission policies unless change is authorized. Do not broaden a live role's permissions to persist a report; use execution-contract EC-1.12.
- Standard `workspace-write` protects `.codex/` and `.agents/`. Project config cannot authorize its own protected-metadata rewrite or bypass host approval.
- Runtime-affecting changes require setup, verification, and scoped rollback in `docs/RUNTIME-SETUP.md`.

## Violation Determination

- A runnable Codex surface lacks project config, or its target-supported check reports invalid/ignored settings -> Violation
- A target is forced to use unverified v2 keys, profile fields are mixed without support, or capacity counts conflate root-inclusive and spawned-only limits -> Violation
- A profile marker is invented as a config key, or static parsing is presented as live tool/model readiness -> Violation
- Removed root/default pins are restored or target model/effort/permissions change outside authorized scope -> Violation
- A role registration omits required fields or resolves from the wrong base directory -> Violation
- Setup requires home-config edits for baseline execution, claims project config bypasses protected paths, or broadens permissions for report persistence -> Violation

## Exceptions

- Claude-only and reference-only surfaces do not require Codex runtime checks.
- Single-agent Codex surfaces may omit multi-agent features and registration.
- Explicit user requirements may choose a supported different permission profile; record its scope and verification without changing the active host by implication.
