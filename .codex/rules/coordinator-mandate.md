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
- One bounded helper hop is permitted only inside a specialist's owned artifact family.

### Shared Filesystem Dispatch Contract

- Every file-mutating dispatch states owned write paths, forbidden paths, acceptance criteria, and the non-reversion rule.
- All agents share the same filesystem unless the runtime explicitly provisions isolation.

### Join Discipline

- Inspect live agents before routing a follow-up or deciding to join.
- `wait_agent` is reserved for a real join boundary when no independent coordinator work remains.

## Violation Determination

- No coordinator registration exists in `.codex/config.toml` for a `multi-agent` team -> Violation
- The coordinator `config_file` path does not resolve from `.codex/config.toml` to `../agents/coordinator.toml` -> Violation
- The coordinator `developer_instructions` contain production ownership outside explicitly assigned coordinator artifacts -> Violation
- A second coordinator exists only to relay tasks between the main coordinator and workers -> Violation
- A file-mutating dispatch omits owned paths, forbidden paths, acceptance criteria, or the non-reversion rule -> Violation
- The coordinator joins or waits without first inspecting live agent state -> Violation

## Exceptions

Single-agent teams do not require a coordinator registration.
