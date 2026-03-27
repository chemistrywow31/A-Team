---
name: Prompt Patterns
description: Reference library of Anthropic-official prompt engineering patterns, templates, and Claude 4.6 best practices for generation agents
---

# Prompt Patterns

A curated library of prompt engineering patterns distilled from Anthropic's official sources. Generation agents (agent-writer, skill-writer, rule-writer) and the prompt-optimizer read from this library during their work.

## When to Use

Use this skill when generating or optimizing agent prompts, skill prompts, rule files, or CLAUDE.md content for a target team. Do not load the entire library — select only the patterns relevant to the current generation task.

## Assets Structure

```
assets/
├── templates/               14 verbatim Anthropic prompt blocks (inject directly)
├── context-strategies/       7 agent context management patterns
├── advanced-techniques/      7 core prompt engineering techniques
├── claude-4-patterns/        6 Claude 4.6 behavioral patterns
└── raw/                      4 source files (3311 lines total)
```

## Selection Methods

### Method 1: Script (recommended for coordinators)

```bash
python .claude/skills/prompt-patterns/select.py --scenario generating-coordinator -v
python .claude/skills/prompt-patterns/select.py --tags "hallucination,escape-hatch"
python .claude/skills/prompt-patterns/select.py --list-scenarios
```

### Method 2: INDEX.md Quick Reference

Read `INDEX.md` in this folder for the scenario-to-file mapping table.

### Method 3: Direct Path

When you already know which pattern you need:
```
.claude/skills/prompt-patterns/assets/templates/parallel-tool-calls.md
```

## Coordinator Dispatch Integration

Include selected pattern paths in the writer dispatch alongside worklog paths:

```xml
<knowledge_refs>
Read these patterns before writing:
- .claude/skills/prompt-patterns/assets/templates/investigate-before-answering.md
- .claude/skills/prompt-patterns/assets/claude-4-patterns/tone-calibration.md
</knowledge_refs>
<task_scope>Write the coordinator agent for the XYZ team.</task_scope>
<worklog_path>.worklog/202603/xyz-team/phase-3-generation/</worklog_path>
```

## Available Scenarios

| Scenario | Description |
|----------|-------------|
| `generating-coordinator` | Writing coordinator agents |
| `generating-execution-agent` | Writing worker/execution agents |
| `generating-research-agent` | Writing research/analysis agents |
| `generating-review-agent` | Writing QA/review agents |
| `generating-coding-team` | Target team works with code |
| `generating-frontend-team` | Target team does frontend work |
| `generating-rules` | Writing rule files |
| `writing-skill-prompts` | Writing skill SKILL.md files |
| `writing-agent-prompts` | Writing agent .md files |
| `optimizing-prompts` | Prompt optimization pass |
| `long-running-tasks` | Agents handling extended workflows |
| `context-constrained` | Context budget is a concern |

## Example

### Input

Coordinator dispatching agent-writer to create a coding team's coordinator:

```
Scenario: generating-coordinator + generating-coding-team
```

### Output from select.py

```
assets/templates/parallel-tool-calls.md
assets/templates/commitment-over-exploration.md
assets/templates/investigate-before-answering.md
assets/templates/anti-over-engineering.md
assets/context-strategies/compaction.md
assets/context-strategies/sub-agent-dispatch.md
assets/claude-4-patterns/anti-overthinking.md
assets/claude-4-patterns/tone-calibration.md
assets/claude-4-patterns/over-engineering-prevention.md
```

### How Writer Uses the Patterns

1. Read each selected pattern file
2. For `templates/` files: inject the verbatim prompt block into the generated agent's prompt where appropriate
3. For `context-strategies/` and `advanced-techniques/` files: apply the pattern principle when structuring the agent's sections
4. For `claude-4-patterns/` files: verify the generated prompt does not contain the listed anti-patterns

## Sources

| Source | Content |
|--------|---------|
| github.com/anthropics/prompt-eng-interactive-tutorial | 10-element template, CoT, Few-shot, Tool Use, Prompt Chaining |
| github.com/anthropics/courses | Structured Refusal, Dual-zone Output, Evaluation frameworks |
| anthropic.com/engineering | Context engineering, Sub-agent architecture, Compaction |
| platform.claude.com | Claude 4.6 best practices, Ready-to-use templates, Migration guide |
