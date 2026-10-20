---
name: Grok Agent Configuration
description: Author supported native agent profiles with explicit tool, loading, and runtime-evidence boundaries
---

# Grok Agent Configuration

## Applicability

- Applies to agent/skill writers, coordinators, validators, and preflight reviewers.

## Rule Content

### Native Definitions And Typed Fields

Store one definition at `.grok/agents/{unique-name}.md`; use matching lowercase kebab-case `name`, nonempty `description`, and a role body. The native loader scans direct files, not nested directories. Validate YAML with a real parser and an explicit supported-key/type allowlist: unknown fields may be silently ignored by the runtime.

Use supported camelCase keys. `promptMode` accepts `extend` or `full`; prefer `extend`. `agentsMd`, `discoverSkills`, `inheritSkills`, and `injectDefaultTools` are booleans; retain initial instruction discovery. `maxTurns` must be a positive integer. Add fields only for a documented use case and validated native support. Do not emit permission-bypass metadata.

Omit `model` and `effort` for the native designer roles. Omitted/`inherit` model follows the parent according to source; effort omission leaves installed session/default behavior without claiming inheritance. A future override uses a supported actual model and measured rationale. `low`, `medium`, `high`, `xhigh`, `max` parse as effort values; parser acceptance alone does not prove model support.

### Tool Identifiers And Enforcement

Metadata uses canonical short IDs; model calls use the live advertised aliases:

| Metadata ID | Model-facing tool |
| --- | --- |
| `task` | `spawn_subagent` |
| `get_task_output` | `get_command_or_subagent_output` |
| `wait_tasks` | `wait_commands_or_subagents` |
| `kill_task` | `kill_command_or_subagent` |
| `run_terminal_cmd` | `run_terminal_command` |
| `read_file`, `grep`, `list_dir`, `search_replace`, `write` | Same name |
| `todo_write`, `web_search`, `web_fetch`, `search_tool`, `use_tool` | Same name |

The special directive `disallowedTools: [Task]` is source-backed for denying specialist delegation. Validate that directive separately from literal canonical IDs. Do not guess other aliases: an unknown allowlist item can retain the entire toolset, while literal deny matching can silently miss a display name. `tools: []` also retains the inherited toolset; it does not mean no tools.

Omit root's `tools` allowlist and enforce its accepted child roster as prompt policy. Typed task allowlists would filter root's broader native capabilities; do not trade away questions, skills, research, or writes merely to claim a roster boundary. Never report prompt policy as runtime enforcement.

`capabilityMode: all` retains execution for writers, validators, auditors, and preflight. `read-write` excludes Execute and fits only a report-only role with no execution checks. Capability modes do not generally confine unknown/MCP tools or write paths. Ownership is the exact dispatch contract; live host permissions remain authoritative.

### Supported Role Patterns

Use these minimal patterns with the actual unique role name and description:

```yaml
---
name: contract-reviewer
description: Verify assigned artifacts and persist criterion evidence
capabilityMode: all
disallowedTools: [Task]
agentsMd: true
discoverSkills: true
---
```

An execution writer uses the same tool posture with its actual responsibilities; it needs read/write and shell checks. A research role keeps needed native web access, persists evidence only in assigned paths, and never mutates the reviewed source. A report-only investigator may select `read-write` only when no execution criterion depends on it.

A planner may add `skills: [prompt-patterns]` for a reference needed on every run; otherwise read exact skill paths on demand. Validate the named skill exists. `discoverSkills` and child `inheritSkills` are distinct from preload, and effective loading requires session evidence.

```yaml
---
name: coordinator
description: Coordinate the accepted workflow in the main session
capabilityMode: all
agentsMd: true
discoverSkills: true
---
```

The coordinator entry skill adopts that role in the current session. No skill field is a substitute for tool permissions. Long research work is explicitly dispatched by root as a standalone child task under `.grok/policies/context-isolation.md`.

### Verify Discovery And Effective Behavior Separately

Validate exact frontmatter keys/types and expected names before `grok inspect --json`. Inspect must list every required definition from its exact project source; a zero exit with a missing profile fails discovery. Inspect does not expose effective per-role tools, model, effort, or prompt isolation. Those claims need bounded installed-session traces, including Task denial and shell capability where required.

### Rejection Example

Reject an auditor profile that sets `tools: [run_terminal_command]` and claims an enforced shell-only role. The display alias is not the canonical metadata ID and an unknown entry can broaden the toolset. Use the validated canonical contract and verify effective behavior before making an enforcement claim.

## Violation Determination

- Nested or duplicate role definitions, filename/name mismatch, unknown fields, or unsupported types -> Violation.
- A tool display alias is used as an unverified metadata filter, or an empty/unknown allowlist is called restrictive -> Violation.
- A specialist lacks Task denial, a shell-check role uses an execution-excluding profile, or root tools are narrowed without approved need -> Violation.
- Effective routing/tool/path isolation is inferred from parser or inspect success -> Violation.

## Exceptions

A target with a measured, explicitly authorized profile may retain its supported overrides and bounded tool filters. Document the evidence and exact capability need; no exception permits a false effective-runtime claim.

Tradeoff: A preload spends startup context; on-demand reads spend calls. Tool filters reduce available actions but do not replace exact path ownership or host authorization.
