---
name: Codex Agent Config Patterns
description: Define current TOML patterns, model tiers, and sandbox posture for Codex agent configs
---

# Codex Agent Config Patterns

## Applicability

- Applies to: `agent-writer`, `team-architect`, and every generated Codex multi-agent runtime

## Rule Content

### Required TOML Shape

Every generated agent config must include:

```toml
name = "process_reviewer"
description = "Audit coordination quality and produce a retrospective report."
model = "gpt-5.6-sol"
model_reasoning_effort = "xhigh"
sandbox_mode = "read-only"

developer_instructions = """
Read `AGENTS.md`, then read `.codex/agents/review/process-reviewer.md` and follow it as the authoritative playbook for this role.
"""
```

Keep TOMLs thin: runtime keys plus a nonempty bootstrap to the same-relative authoritative playbook. Map `agents/{path}.toml` to `.codex/agents/{path}.md`. Do not copy the full playbook into `developer_instructions`.
Validate required role sections in the authoritative playbook; validate the TOML bootstrap only for nonempty content and a resolvable same-relative target.

### Registry And Discovery

- Runtime TOMLs live under `agents/`.
- `.codex/config.toml` registers them through `[agents.<id>]` entries whose `config_file` paths resolve relative to `.codex/`.
- Treat each `[agents.<id>]` table id as the agent's stable snake_case runtime identity, matching the role and task-path vocabulary.
- Require the referenced agent TOML's `name` to equal `<id>` exactly; do not substitute a display name.

### Current Model Guidance

- Planning, generation, optimization, restructuring, and artifact-gate roles default to `gpt-5.6-sol` at `xhigh`.
- Read-heavy research, runtime probing, and dialogue review default to `gpt-5.6-terra` at `high` unless the worklog records a stronger-risk rationale.
- Do not pin new or regenerated Codex agent configs to `gpt-5.4` unless the worklog records a compatibility exception.

### Sandbox Posture

- Roles that mutate repo artifacts use `workspace-write`.
- Reviewer, auditor, and verifier roles that only inspect artifacts use `read-only`.
- A review or probe role may use `workspace-write` only when its owned artifact set explicitly includes a report path or runtime advisory it must write.

### Coordinator Playbook Requirements

The authoritative coordinator playbook under `.codex/agents/` must include:

- direct specialist topology
- stable task-path strategy
- follow-up, interrupt, and join rules
- shared-filesystem non-reversion rule
- quality gates and completion contract

### Specialist Playbook Requirements

The authoritative specialist playbook under `.codex/agents/` must include:

- `## Identity`
- `## Responsibilities`
- `## Input and Output`
- `## Workflow`
- `## Preflight`
- `## Verification`
- `## Completion Contract`
- `## File Ownership`
- `## Boundaries`

### Fork Override Constraint

- Full-history forks inherit the parent model and reasoning effort.
- Any explicit `spawn_agent` model or reasoning override requires `fork_turns = "none"` or a positive bounded fork.
- Do not rely on omitted or `all` forks when overriding model or effort.

## Violation Determination

- An agent TOML misses `name`, `description`, `model`, `model_reasoning_effort`, `sandbox_mode`, or `developer_instructions` -> Violation
- `developer_instructions` is empty, omits the same-relative `.codex/agents/{path}.md` bootstrap target, or names a missing target -> Violation
- A registry entry points outside the intended TOML path or does not resolve from `.codex/` -> Violation
- A `[agents.<id>]` table id is not a stable snake_case runtime identity, or its referenced agent TOML's `name` does not equal `<id>` exactly -> Violation
- A new or regenerated Codex agent TOML pins `gpt-5.4` with no recorded compatibility rationale -> Violation
- A reviewer or verifier uses `workspace-write` without an owned write artifact, or a writer role uses `read-only` while owning mutable paths -> Violation
- The authoritative coordinator playbook omits topology, task-path, join, or non-reversion guidance -> Violation
- The authoritative specialist playbook omits completion contract, file ownership, or boundaries -> Violation
- A dispatch pattern claims model or effort override on a full-history fork -> Violation

## Exceptions

- If Codex runtime schema changes, update this rule and the mapping docs in the same change.
- Deterministic utility roles may inherit the project default model when the worklog records why a role-specific pin is unnecessary.
