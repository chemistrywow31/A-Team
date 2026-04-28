---
name: Quality Validation
description: Validate that a generated Codex team is structurally complete and internally consistent
---

# Quality Validation

## Description

Use this skill to verify that a generated team is ready for delivery.

## Users

- `.codex/agents/team-architect.md`

## Validation Levels

### 1. Structural Completeness

- `teams/{team-name}/` exists
- `AGENTS.md` exists
- `agents/` exists when the execution mode is `multi-agent`
- `.codex/config.toml` exists
- `.codex/docs/format-mapping.md` exists
- `.codex/docs/format-mapping.manifest.yaml` exists
- `.codex/skills/`, `.codex/rules/`, and `.agents/skills/` exist
- `.codex/rules/worklog.md`, `.codex/rules/context-management.md`, and `.codex/rules/reasoning-and-self-critique.md` exist

### 2. Content Completeness

- `AGENTS.md` explains the chosen delivery format when needed
- every agent config has required runtime keys and `developer_instructions`
- coordinator config includes coordinator-only sections inside `developer_instructions`
- every non-trivial agent config includes Preflight, Verification, Completion Contract, File Ownership, and Boundaries
- every skill has description, users, core knowledge, and example
- every rule has applicability, rule content, and violation determination
- mapping docs record requested format, canonical format, and round-trip notes

### 3. Reference Consistency

- every referenced skill path resolves
- every referenced rule path resolves
- every agent registry entry resolves from the directory containing `.codex/config.toml` to a real `../agents/**/*.toml` file
- every registered agent config has non-empty `name`, `description`, `model`, `model_reasoning_effort`, `sandbox_mode`, and `developer_instructions`
- the coordinator stays at `agents/` root and workers stay in subfolders
- skill users map to real agents or team-level roles
- coordinator subordinate list covers all specialists
- mapping manifest paths resolve against generated artifacts

### 4. Logical Consistency

- responsibilities do not overlap unintentionally
- role coverage matches the scope
- file ownership does not conflict in parallel paths
- worklog, context-management, and decision-audit requirements are not contradicted by agent instructions
- requested format, Codex-native strategy, and mapping artifacts do not contradict each other
- lossy or bridge conversions are called out explicitly

## Result Format

Produce a four-part pass/fail report with concrete issues and corrections.

## Example

### Input

`請驗證 teams/content-studio/`

### Output

`Structural Completeness: pass; Reference Consistency: fail because .codex/config.toml registers ../agents/review/process-reviewer.toml but the file is missing.`
