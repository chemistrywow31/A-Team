---
name: Prompt Patterns
description: Select task-relevant prompt patterns using current native model guidance and A-Team generation contracts
---

# Prompt Patterns

A maintained selection library informed by official Anthropic sources, with separately attributed A-Team contracts and authored examples. Historical snapshots are retained only for provenance. Generation agents (agent-writer, skill-writer, rule-writer) and the prompt-optimizer read from this library during their work.

## When to Use

Use this skill when generating or optimizing agent prompts, skill prompts, rule files, or CLAUDE.md content for a target team. Do not load the entire library — select only the patterns relevant to the current generation task.

## A-Team Return Contract

This repository-specific contract is not attributed to the Anthropic sources below. For A-Team task returns, use only the statuses in `.claude/rules/execution-contract.md` EC-1. Missing required evidence or context uses `STATUS: NEEDS_CONTEXT` with `INSUFFICIENT_DATA: {missing}` in `CONCLUSIONS`; never use `INSUFFICIENT_DATA` as a report status.

## How To Use The Library

The writing standard for generated files is `.claude/rules/writing-quality-standard.md`; read that first. This library is a set of optional patterns for particular problems, not a checklist. Most files need none of them. Pick a pattern when the file has the problem the pattern solves, adapt it to the target model, and leave out the rest. A block copied in because its scenario tag matched is the kind of text the standard asks you to cut.

Check the selected model's current official guidance before using a model-specific technique, and keep the target's explicit model and effort choices. Only when the output is Codex or dual, read `.codex/rules/codex-agent-config-patterns.md` and `.codex/rules/codex-runtime-config.md` for that projection.

## Assets Structure

```
assets/
├── templates/               14 prompt blocks (Anthropic-derived; one has an attributed A-Team extension)
├── context-strategies/       7 agent context management patterns
├── advanced-techniques/      7 core prompt engineering techniques
├── claude-4-patterns/        6 historical Claude 4.6 patterns (excluded)
└── raw/                      4 historical source snapshots — provenance only
```

**Selection boundary (checked 2026-10-06).** `select.py` scans only `templates/`, `context-strategies/`, and `advanced-techniques/`. It never returns `claude-4-patterns/` or `raw/`, including through tag queries. Historical files remain intact and can be inspected explicitly for provenance; they do not override current native guidance. `source` and `historical-source` metadata are attribution, not read triggers.

Selection returns candidates, not instructions to inject every block. Check each candidate against the actual task, model/mode, native tools, existing authorization, and higher-priority contracts. Preserve useful structure; adapt model-specific advice rather than generalizing it across providers. Do not add irrelevant candidates merely because they share a scenario tag.

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

Include only selected pattern paths in the writer dispatch alongside the task scope, exact owned/forbidden paths, acceptance criteria, and worklog paths. Historical patterns do not override the current generation contract.

## Proportional-Design Pattern

A-Team policy from user-approved decisions D6-D9, not from the Anthropic sources below.

Use `assets/templates/anti-over-engineering.md` for a team whose work can propose safeguards: architecture, implementation, packaging, deployment, migration, recovery, review. Such a team gets one short proportional-design rule in its canonical rule family, a `Safeguard Decision` slot only in roles that can propose or keep a non-obvious safeguard, and a verdict from its existing reviewer. Other teams get none of it. Unsupported rare hypotheticals are assumptions or monitoring triggers, not blockers; narrowly scoped controls backed by a credible corruption, security, privacy, data-loss, compliance or irreversible-mutation risk stay.

## Available Scenarios

| Scenario | Description |
|----------|-------------|
| `generating-coordinator` | Writing coordinator agents |
| `generating-execution-agent` | Writing worker/execution agents |
| `generating-research-agent` | Writing research/analysis agents |
| `generating-review-agent` | Writing QA/review agents |
| `generating-coding-team` | Target team works with code |
| `generating-architecture-agent` | Writing system or architecture agents |
| `generating-packaging-agent` | Writing packaging or release agents |
| `generating-deployment-agent` | Writing deployment agents |
| `generating-migration-agent` | Writing migration agents |
| `generating-recovery-agent` | Writing recovery agents |
| `generating-frontend-team` | Target team does frontend work |
| `generating-rules` | Writing rule files |
| `writing-skill-prompts` | Writing skill SKILL.md files |
| `writing-agent-prompts` | Writing agent .md files |
| `optimizing-prompts` | Prompt optimization pass |
| `long-running-tasks` | Agents handling extended workflows |
| `context-constrained` | Context budget is a concern |

## Sources

Current native guidance checked 2026-10-06: [Claude prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), [effort](https://platform.claude.com/docs/en/build-with-claude/effort), and [Claude Code subagents](https://code.claude.com/docs/en/sub-agents). Active rewrites label A-Team-authored examples separately; the sources below record the library’s origins, not a claim that every current pattern is verbatim vendor text.

| Source | Content |
|--------|---------|
| github.com/anthropics/prompt-eng-interactive-tutorial | 10-element template, CoT, Few-shot, Tool Use, Prompt Chaining |
| github.com/anthropics/courses | Structured Refusal, Dual-zone Output, Evaluation frameworks |
| anthropic.com/engineering | Context engineering, Sub-agent architecture, Compaction |
| platform.claude.com | Dated prompting guidance and historical templates; re-check the selected model |

The proportional-design contract and the extension in `anti-over-engineering.md` trace to `.worklog/202609/prevent-overengineering-three-teams/phase-2-a-team-generator-assessment/decisions.md` D6-D9. Do not attribute that extension to Anthropic.
