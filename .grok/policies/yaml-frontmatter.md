---
name: YAML Frontmatter
description: Validate native frontmatter with exact supported fields while separating metadata from runtime guarantees
---

# YAML Frontmatter

## Applicability

- Applies to authors and validators of native agents, skills, policies, and bootstrap rules.

## Rule Content

### Start Authored Runtime Documents With YAML

The first line is `---`; no blank line, comment, or content precedes the opening delimiter. Parse the full mapping with a real YAML parser and reject duplicate keys, unknown native keys, wrong types, and missing required values. A runtime that ignores an unknown key does not make that key valid.

Require nonempty string `name` and `description` for agents, skills, and rules/policies. Keep descriptions precise and short; the preferred one-sentence/under-120-character style is an authoring convention, not a vendor parser limit.

### Agent Fields

Use `.grok/agents/{name}.md`, flat, with filename stem equal to unique lowercase kebab-case `name`. Native keys and supported behavior are governed by `.grok/policies/grok-agent-config.md`:

| Field | Type / authoring boundary |
| --- | --- |
| `name`, `description` | Required nonempty strings |
| `model` | Omit for untested profiles; `inherit` is source-supported; actual pins require declared availability evidence |
| `effort` | Omit by default; supported parser values are low/medium/high/xhigh/max, effective support separately tested |
| `promptMode` | `extend` or `full`; prefer extend |
| `tools`, `disallowedTools` | Prefer lists of validated canonical IDs or supported special directives; specialists use `[Task]` denial |
| `capabilityMode` | Explicitly justified native capability profile; `all` for roles executing checks |
| `agentsMd`, `discoverSkills`, `inheritSkills`, `injectDefaultTools` | Booleans; do not silently disable bootstrap instructions |
| `skills` | List of exact available native skill names for preload |
| `maxTurns` | Positive integer; zero and snake_case misspellings fail local validation |
| `mcpInheritance` | Source-supported all/none or named/except shape; add only for a confirmed need |

Other native fields require a documented use case plus schema and effective validation before adding them to the local allowlist. Do not emit permission bypass or speculative hook fields merely because a source struct accepts them. Do not duplicate a model/effort choice in body prose as a second runtime declaration.

### Skill Fields And Entry Semantics

Store `.grok/skills/{name}/SKILL.md` with native name/description. Preserve a chosen invocation identifier rather than forcing display-title conversion. Optional `disable-model-invocation`, `user-invocable`, `argument-hint`, and tooling `metadata` must match the installed skill schema and actual intended behavior.

For an A-Team-authored coordinator-entry skill, declare explicit-user invocation intent with `disable-model-invocation: true` and a useful `argument-hint`; the body must adopt the resolved coordinator playbook in the current session. Identify entry candidates from their workflow purpose even if required metadata is missing. Exactly one entry serves a multi-agent team. A manual-only utility is not automatically an entry.

Skill `model` and `effort` are accepted but not applied in the observed native contract, and `allowed-tools` does not grant/restrict tools. Omit these as execution controls. Do not use foreign skill-fork metadata to create context isolation; root performs explicit child dispatch. Agent preload/discovery/inheritance controls are separate and need their own evidence.

### Rules And Supporting Documents

Rules and policies require `name` and `description`; their applicability belongs in the body. This branch auto-loads only direct `.grok/rules/core.md`; complete `.grok/policies/` are exact on-demand reads. Do not rely on unsupported `paths` metadata to load a policy.

Root `AGENTS.md`, `JUDGMENT.md`, dispatch templates, mapping/setup reports, worklogs, and vendored reference assets may use their established document format without YAML. This exception does not apply to authored runtime agent/skill/rule files.

### Validate Before Handoff

Check source YAML, names/paths, allowed keys/types, required role/skill body contracts, referenced files, and meaningful boundary examples. Then run installed discovery and match exact expected source identities; a missing profile fails even if inspect exits zero. Record effective tool/model/context behavior separately from metadata loading.

### Rejection Example

A writer adds `max_turns: 0` and marks the agent safely bounded because inspect lists it. Reject the ignored key; use a supported positive `maxTurns` only when a turn budget is justified, then verify the relevant behavior.

## Violation Determination

- Authored runtime document lacks line-1 YAML, required strings, or unique/matching native identifiers -> Violation.
- Unknown/duplicate fields, wrong types, or ignored metadata are treated as valid controls -> Violation.
- Entry identification depends on already-valid metadata, or its body spawns the coordinator -> Violation.
- Skill metadata claims effective tool/model/context controls or policy loading relies on unsupported globs -> Violation.
- A profile is accepted without exact inventory checks or effective behavior is inferred from parsing -> Violation.

## Exceptions

Supporting documents and retained reference assets use the formats named above. Existing explicitly supported target pins may be preserved during unrelated work; omission defaults do not authorize migration.
