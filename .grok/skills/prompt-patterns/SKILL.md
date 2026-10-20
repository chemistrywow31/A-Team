---
name: prompt-patterns
description: Select task-relevant prompt patterns using current native model guidance and A-Team generation contracts
---

# Prompt Patterns

A maintained selection library adapted for Grok from attributed Anthropic-origin techniques, with separately attributed A-Team contracts and authored examples. Historical snapshots are retained only for provenance. Generation agents (agent-writer, skill-writer, rule-writer) and the prompt-optimizer read from this library during their work.

## When to Use

Use this skill when generating or optimizing agent prompts, skill prompts, rule files, or AGENTS.md content for a target team. Do not load the entire library — select only the patterns relevant to the current generation task.

## A-Team Return Contract

This repository-specific contract is not attributed to the Anthropic sources below. For A-Team task returns, use only the statuses in `.grok/policies/execution-contract.md` EC-1. Missing required evidence or context uses `STATUS: NEEDS_CONTEXT` with `INSUFFICIENT_DATA: {missing}` in `CONCLUSIONS`; never use `INSUFFICIENT_DATA` as a report status.

## Effective Generation Contract

- Prioritize effectiveness for the selected platform, model, and thinking mode. Retain useful XML, examples, steps, and verification; concision is secondary. For Grok, use only target-supported model/effort controls with measured behavior; omitted effort does not prove thinking is disabled. Skill model/effort metadata is ignored. Public derivations and evidence are distinct from private reasoning.

- For each agent, write exactly one adjacent `Reasoning`, `Workflow`, and `Self-Critique` sequence in that order. Make it task-specific: decision criteria, execution steps, then checks of the likely failure modes. Do not duplicate this contract with mandatory `Preflight`/`Verification` blocks or fixed four/five-slot essays.
- Request concise decisions and verification evidence, never private reasoning transcripts. Keep input/output, ownership, uncertainty, boundaries, and completion requirements explicit.
- Include at least one meaningful rejection/defer/escalation example in each authored agent or skill. Add positive or contrast examples when they clarify behavior. Do not impose a universal example count; size overages follow J5 independent usefulness review.
- Reuse confirmed requirements and existing authorization. Ask only for material missing decisions, unresolved authority, or actions outside that authorization. Continue independent work during supported asynchronous clarification; do not assume an unanswered required question is approval.
- Send one coherent frozen artifact batch to the existing independent reviewer. After fixes, rerun every criterion citing a changed file plus dependent mappings/parity. Run preflight only for new delivery, changed active runtime artifacts, or missing current readiness evidence, and reuse its current validation results for each selected runtime.
- Follow `.grok/policies/reasoning-and-self-critique.md`, `.grok/policies/prompt-engineering-patterns.md`, `.grok/policies/context-tier.md` and `.grok/policies/grok-agent-config.md`. Preserve tested target model choices outside an authorized migration. No Anthropic model-tier equivalence is implied. Grok lifecycle follows `.grok/policies/context-isolation.md`.


## Assets Structure

```
assets/
├── templates/               14 prompt blocks (Anthropic-derived; one has an attributed A-Team extension)
├── context-strategies/       7 agent context management patterns
└── advanced-techniques/      7 core prompt engineering techniques
```

**Selection boundary (native adaptation 2026-10-20).** `select.py` scans only `templates/`, `context-strategies/`, and `advanced-techniques/`. It never returns `claude-4-patterns/` or `raw/`, including through tag queries. Historical files remain intact only under `reference/platform-sources/.claude/skills/prompt-patterns/assets/` and can be inspected explicitly for provenance; they do not override current native guidance. `source` and `historical-source` metadata are attribution, not read triggers.

Selection returns candidates, not instructions to inject every block. Check each candidate against the actual task, model/mode, native tools, existing authorization, and higher-priority contracts. Preserve useful structure; adapt model-specific advice rather than generalizing it across providers. Do not add irrelevant candidates merely because they share a scenario tag.

## Selection Methods

### Method 1: Script (recommended for coordinators)

```bash
python .grok/skills/prompt-patterns/select.py --scenario generating-coordinator -v
python .grok/skills/prompt-patterns/select.py --tags "hallucination,escape-hatch"
python .grok/skills/prompt-patterns/select.py --list-scenarios
```

### Method 2: INDEX.md Quick Reference

Read `INDEX.md` in this folder for the scenario-to-file mapping table.

### Method 3: Direct Path

When you already know which pattern you need:
```
.grok/skills/prompt-patterns/assets/templates/parallel-tool-calls.md
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

Historical technique sources checked in the original adaptation on 2026-10-06 (not Grok runtime authority): [Claude prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), [effort](https://platform.claude.com/docs/en/build-with-claude/effort), and [Claude Code subagents](https://code.claude.com/docs/en/sub-agents). Active rewrites label A-Team-authored examples separately; the sources below record the library’s origins, not a claim that every current pattern is verbatim vendor text.

| Source | Content |
|--------|---------|
| github.com/anthropics/prompt-eng-interactive-tutorial | 10-element template, CoT, Few-shot, Tool Use, Prompt Chaining |
| github.com/anthropics/courses | Structured Refusal, Dual-zone Output, Evaluation frameworks |
| anthropic.com/engineering | Context engineering, Sub-agent architecture, Compaction |
| platform.claude.com | Dated prompting guidance and historical templates; re-check the selected model |

The proportional-design contract and the extension in `anti-over-engineering.md` retain the canonical source attribution to user-approved decisions D6-D9, recorded in the archived original skill. The active contract is `.grok/policies/proportional-design.md`. Do not attribute that extension to Anthropic.

## Source Attribution

- **Origin**: A-Team canonical skill, preserved at `reference/platform-sources/.claude/skills/prompt-patterns/SKILL.md`.
- **Integration**: Pattern B: Adapted Install; native Grok branch authority is `AGENTS.md` plus `.grok/`.
- **Retrieved**: 2026-10-20 from the verified base snapshot.
- **Modifications**: Native paths, loading and lifecycle; preserved task intent, examples and useful assets. Archive is reference-only.
