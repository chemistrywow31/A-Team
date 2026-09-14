---
name: Prompt Patterns
description: Reference library of Anthropic-official prompt engineering patterns, templates, and Claude 4.6 best practices for generation agents
---

# Prompt Patterns

A curated library of prompt engineering patterns distilled from Anthropic's official sources, plus an explicitly attributed A-Team proportional-design contract. Generation agents (agent-writer, skill-writer, rule-writer) and the prompt-optimizer read from this library during their work.

## When to Use

Use this skill when generating or optimizing agent prompts, skill prompts, rule files, or CLAUDE.md content for a target team. Do not load the entire library — select only the patterns relevant to the current generation task.

## A-Team Return Contract

This repository-specific contract is not attributed to the Anthropic sources below. For A-Team task returns, use only the statuses in `.claude/rules/execution-contract.md` EC-1. Missing required evidence or context uses `STATUS: NEEDS_CONTEXT` with `INSUFFICIENT_DATA: {missing}` in `CONCLUSIONS`; never use `INSUFFICIENT_DATA` as a report status.

## Compact Generation Contract

- For each agent, write exactly one adjacent `Reasoning`, `Workflow`, and `Self-Critique` sequence in that order. Make it task-specific: decision criteria, execution steps, then checks of the likely failure modes. Do not duplicate this contract with mandatory `Preflight`/`Verification` blocks or fixed four/five-slot essays.
- Request concise decisions and verification evidence, never private reasoning transcripts. Keep input/output, ownership, uncertainty, boundaries, and completion requirements explicit.
- Include exactly one rejection example in each agent or skill. Use the case that clarifies the boundary; do not mandate normal or edge examples.
- Reuse confirmed requirements and existing authorization. Ask only for material missing decisions, unresolved authority, or actions outside that authorization. Continue independent work during supported asynchronous clarification; do not assume an unanswered required question is approval.
- Send one coherent frozen artifact batch to the existing independent reviewer. After fixes, rerun every criterion citing a changed file plus dependent mappings/parity. Run preflight only for new delivery, changed active runtime artifacts, or missing current readiness evidence, and reuse its current validation results for each selected runtime.
- Follow `.claude/rules/reasoning-and-self-critique.md` and `.claude/rules/prompt-engineering-patterns.md` for the contract, and `.claude/rules/context-tier.md` for Claude model routing. Only when the selected output is Codex or dual, read `.codex/rules/codex-agent-config-patterns.md` and `.codex/rules/codex-runtime-config.md` for that projection's specifications. Preserve the target's explicit model and effort choices outside an authorized migration; do not copy a generic model guide into every generated prompt.

## Assets Structure

```
assets/
├── templates/               14 prompt blocks (Anthropic-derived; one has an attributed A-Team extension)
├── context-strategies/       7 agent context management patterns
├── advanced-techniques/      7 core prompt engineering techniques
├── claude-4-patterns/        6 Claude 4.6 behavioral patterns
└── raw/                      4 source snapshots (3311 lines) — provenance only, do not read
```

**Version note (checked 2026-07-25).** `raw/` and `claude-4-patterns/` are anchored to Claude 4.x:
`raw/` contains 52 occurrences of "Opus 4.", 37 of "Sonnet 4.", and zero references to Claude 5.
Nothing reads `raw/` — `select.py` never emits a `raw/` path, and the `source:` fields in the
distilled files are citations, not read-triggers. Treat both directories as historical provenance.
Where they conflict with Anthropic's Claude 5 context-engineering guidance, the newer guidance
wins: prefer judgment over enumerated prohibitions, interface design over usage examples,
progressive disclosure over upfront loading, and one statement of each fact over repetition.

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

## Proportional-Design Generation Contract

This contract is specific to A-Team and comes from the user-approved decisions D6-D9, not from the Anthropic sources below.

Route `assets/templates/anti-over-engineering.md` to rule generation and to prompts for architecture, implementation, packaging, deployment, migration, recovery, and review work. Then:

- Generate one `proportional-design` rule in the target's declared canonical rule family and project it to every requested runtime. Do not create independent platform-specific versions.
- Add a `Safeguard Decision` producer slot only when a role proposes or retains a non-obvious safeguard. Require the five template fields; do not burden ordinary decisions with the slot.
- Make the existing independent reviewer return a criterion-level verdict for all five fields and the ordinary-path check. Use the team's existing review stage; do not add a role, state machine, or approval ladder.
- Reject unsupported rare hypotheticals as implementation or release blockers. Record them as assumptions or monitoring triggers instead.
- Preserve narrowly scoped controls justified by credible corruption, security, privacy, compatibility, data-loss, compliance, or irreversible-mutation risk.

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

## Examples

### Rejection Case

Reject a deployment prompt that requires an unconditional whole-package checksum and residual-task gate but supplies no evidence/likelihood, protected impact, cheapest adequate alternative, ordinary-path/new-failure cost, or removal/override/monitoring. Do not let it block routine config edits, copy/start, or intentional stop/restart.

This rejection does not remove a narrowly scoped integrity or task-drain control backed by credible corruption, security, data-loss, compliance, or irreversible-mutation risk. Preserve that justified high-impact control, require the same five fields, and use the existing independent reviewer.

## Sources

| Source | Content |
|--------|---------|
| github.com/anthropics/prompt-eng-interactive-tutorial | 10-element template, CoT, Few-shot, Tool Use, Prompt Chaining |
| github.com/anthropics/courses | Structured Refusal, Dual-zone Output, Evaluation frameworks |
| anthropic.com/engineering | Context engineering, Sub-agent architecture, Compaction |
| platform.claude.com | Claude 4.6 best practices, Ready-to-use templates, Migration guide |

The proportional-design contract and the extension in `anti-over-engineering.md` trace to `.worklog/202609/prevent-overengineering-three-teams/phase-2-a-team-generator-assessment/decisions.md` D6-D9. Do not attribute that extension to Anthropic.
