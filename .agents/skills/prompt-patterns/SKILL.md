---
name: Prompt Patterns
description: Apply Codex-native prompt patterns for agents, skills, rules, and project instructions
---

# Prompt Patterns

## Description

Use this skill when writing or reviewing prompts for Codex teams. It converts broad behavioral wishes into structured, testable prompt sections.

## Users

- `.codex/agents/generation/agent-writer.md`
- `.codex/agents/generation/skill-writer.md`
- `.codex/agents/generation/rule-writer.md`
- `.codex/agents/optimization/prompt-optimizer.md`

## Core Knowledge

### Structural Patterns

- Use `## Boundaries` for exclusions instead of relying on "do not" sentences.
- Use `## Input and Output` for handoff contracts.
- Use `## Completion Contract` for status, artifacts, changed files, worklog paths, and blockers.
- Use `## Preflight` and `## Verification` for concise decision notes and quality checks.
- Use `## Uncertainty Protocol` for `INSUFFICIENT_DATA`, `NEEDS_CONTEXT`, and `BLOCKED`.

### Codex Adaptation Rules

- Use `AGENTS.md` for project-wide runtime guidance.
- Use `.codex/config.toml` and `agents/**/*.toml` for subagent registration and runtime behavior.
- Use `.agents/skills/{skill-name}/SKILL.md` for runtime-discoverable skills.
- Use `.codex/rules/{rule-name}.md` for enforceable constraints.
- Avoid Claude-only assumptions such as `.claude/settings.json`, `Task tool`, `Agent tool`, `context: fork`, and Claude model names.

### Example Coverage

When examples are included, cover:

- normal case
- edge case
- rejection or escalation case

## Application Guide

1. Identify the behavior the prompt must enforce.
2. Choose a structural slot that makes the behavior observable.
3. Write the slot as an imperative instruction.
4. Add a concrete completion or escalation condition.
5. Verify paths and runtime terms are Codex-native.

## Quality Checkpoints

- frontmatter stays valid
- no Claude-only runtime term appears in Codex-native output
- every non-trivial agent has an uncertainty protocol
- examples include failure behavior when examples exist
- instructions are concrete enough to test

## Example

### Input

`Make the reviewer careful and evidence-based.`

### Output

Add `## Evidence Requirements`, `## Verification`, and `## Completion Contract` sections. Require each finding to cite a file path or worklog entry, and require `INSUFFICIENT_DATA` when evidence is missing.
