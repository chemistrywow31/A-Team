---
name: Coordinator Mandate
description: Require one coordinator with direct specialists, stable task paths, and disciplined joins in every Codex multi-agent team
---

# Coordinator Mandate

## Applicability

- Applies to: all generated Codex multi-agent teams and all A-Team writers

## Rule Content

### Coordinator Must Exist

Every generated `multi-agent` team must include one coordinator agent registration in `teams/{team-name}/.codex/config.toml` and one matching config file under `teams/{team-name}/agents/`.

Because `.codex/config.toml` lives under `.codex/`, the coordinator registration must point to the project-root agent file with `../agents/coordinator.toml`.

Recommended shape:

```toml
[agents.coordinator]
description = "Coordinate delegation, follow-ups, and final synthesis."
config_file = "../agents/coordinator.toml"
```

### Coordinator Is Phase Owner, Not Producer

- The coordinator owns user-facing conversation, task-path routing, joins, and final synthesis.
- Specialist-owned artifact families stay specialist-owned unless the phase plan explicitly reassigns them.
- Coordinator `developer_instructions` must stay coordination-focused.

### Flat Direct-Specialist Topology

- Use one coordinator with direct specialists.
- Do not add relay coordinators or sub-coordinators.
- Where the target host and dispatch permit it, one bounded helper hop is permitted only for independent evidence or verification inside a specialist's owned artifact family; a helper cannot delegate again. Native Claude restrictions do not define Codex capability. Use `.codex/rules/context-isolation.md` for the target-supported lifecycle and fork contract.

### Shared Filesystem Dispatch Contract

- Every file-mutating dispatch states owned write paths, forbidden paths, acceptance criteria, and the non-reversion rule. Name report-persistence ownership; a live host-blocked report uses only EC-1.12's bounded coordinator handoff.
- All agents share the same filesystem unless the runtime explicitly provisions isolation.

### Join Discipline

- On A-Team's observed v2 host, inspect live agents with `list_agents` before routing or joining; use `wait_agent` only at a real join boundary when no independent coordinator work remains. For other target profiles use the supported equivalent and record unavailable readiness evidence.

## Violation Determination

- No coordinator registration exists in `.codex/config.toml` for a `multi-agent` team -> Violation
- The coordinator `config_file` path does not resolve from `.codex/config.toml` to `../agents/coordinator.toml` -> Violation
- The coordinator `developer_instructions` contain production ownership outside explicitly assigned coordinator artifacts -> Violation
- A second coordinator exists only to relay tasks between the main coordinator and workers -> Violation
- A file-mutating dispatch omits owned paths, forbidden paths, acceptance criteria, or the non-reversion rule -> Violation
- The coordinator joins without the supported state check, waits while independent work remains, or assumes unavailable v2 lifecycle tools -> Violation

## Exceptions

Single-agent teams do not require a coordinator registration.
