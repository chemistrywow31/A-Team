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
- `.codex/config.toml` exists
- `.codex/docs/format-mapping.md` exists
- `.codex/docs/format-mapping.manifest.yaml` exists
- `.codex/agents/`, `.codex/skills/`, `.codex/rules/`, and `.agents/skills/` exist

### 2. Content Completeness

- `AGENTS.md` explains the chosen delivery format when needed
- every agent file has required sections
- coordinator file has coordinator-only sections
- every skill has description, users, core knowledge, and example
- every rule has applicability, rule content, and violation determination
- mapping docs record requested format, canonical format, and round-trip notes

### 3. Reference Consistency

- every referenced skill path resolves
- every referenced rule path resolves
- skill users map to real agents
- coordinator subordinate list covers all specialists
- mapping manifest paths resolve against generated artifacts

### 4. Logical Consistency

- responsibilities do not overlap unintentionally
- role coverage matches the scope
- file ownership does not conflict in parallel paths
- requested format, Codex-native strategy, and mapping artifacts do not contradict each other
- lossy or bridge conversions are called out explicitly

## Result Format

Produce a four-part pass/fail report with concrete issues and corrections.

## Example

### Input

`請驗證 teams/content-studio/`

### Output

`Structural Completeness: pass; Reference Consistency: fail because .agents/skills/editorial-review/SKILL.md is missing.`
