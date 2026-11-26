---
name: Prompt Patterns
description: Apply Codex-native prompt patterns for agents, skills, rules, and project instructions
---

# Prompt Patterns

Use this skill when generating or optimizing agent prompts, skills, rules, or project instructions. Select only guidance relevant to the assigned artifact; historical Claude research assets stay under the canonical source tree.

## Effective Generation Contract

- The target's writing-quality-standard is the standard for generated files; this library is a set of optional patterns for particular problems, not a checklist. Pick a pattern when the file has the problem it solves and leave out the rest. Use supported reasoning-effort controls and clear deliverables instead of requesting private reasoning transcripts.

- No section is mandatory in a generated agent. When an agent uses `Reasoning`, `Workflow`, and `Self-Critique`, write that sequence once, in that order, and make it specific to the role. Do not duplicate it with mandatory `Preflight`/`Verification` blocks or fixed four/five-slot essays.
- Request concise decisions and verification evidence, never private reasoning transcripts. Keep input/output, ownership, boundaries, uncertainty, and completion requirements explicit.
- State the contract first and add an example only when it shows something the contract cannot. No example is mandatory. J5 size overages require independent review.
- Reuse confirmed requirements and existing authorization. Ask only for material missing decisions, unresolved authority, or actions outside that authorization. Continue independent work during supported asynchronous clarification; unanswered required questions do not supply approval.
- Give the existing independent reviewer one coherent frozen artifact batch. After fixes, rerun every criterion citing a changed file plus dependent mappings/parity. Run preflight for new delivery, changed active runtime artifacts, or missing current readiness evidence; reuse its current validator and runtime/model probe results.
- Use only EC-1 report statuses from `.codex/rules/execution-contract.md`. Missing required context uses `STATUS: NEEDS_CONTEXT` with `INSUFFICIENT_DATA: {missing}` in `CONCLUSIONS`, never as a status.

## Proportional-Design Generation

Apply this A-Team contract to rule generation and architecture, implementation, packaging, deployment, migration, recovery, and review work:

- Read `.claude/skills/prompt-patterns/assets/templates/anti-over-engineering.md`. Its proportional-safeguard extension is user-approved A-Team guidance, not Anthropic-authored content.
- Generate one `proportional-design` rule in the target's declared canonical rule family, then project it to every requested runtime. Do not create independent platform-specific rules.
- Add a `Safeguard Decision` producer slot only when the role proposes or retains a non-obvious safeguard. Require evidence/likelihood, protected impact, cheapest adequate alternative, ordinary-path/new-failure cost, and removal/override/monitoring.
- Require the existing independent reviewer to return a criterion-level verdict for those five fields and for preservation of mutable config, copy/start, intentional stop/restart, update, and recovery paths.
- Reject unsupported rare hypotheticals as code or release blockers; record them as assumptions or monitoring triggers. Preserve narrowly scoped controls justified by credible corruption, security, privacy, compatibility, data-loss, compliance, or irreversible-mutation risk.
- Use existing producer and review roles. Do not add a role, state machine, approval stage, or approval ladder for this contract.

## Codex Adaptation

- Put project guidance in `AGENTS.md`, registered runtime behavior in `.codex/config.toml` and `agents/**/*.toml`, discoverable skills in `.agents/skills/{skill}/SKILL.md`, and enforceable constraints in `.codex/rules/`.
- Apply `.codex/rules/reasoning-and-self-critique.md` and `.codex/rules/prompt-engineering-patterns.md` for prompt structure; use `.codex/rules/codex-agent-config-patterns.md` and `.codex/rules/codex-runtime-config.md` for current model/config decisions. Do not copy a generic model guide into every prompt.
- Select actual lifecycle, tool, path, and isolation behavior through `.codex/rules/context-isolation.md`; label observed-host v2 details separately from portable target capabilities. Runtime permissions belong in config/TOML; do not copy Claude-only skill frontmatter or runtime assumptions.
- Preserve exact assigned ownership, declared authority/mappings, and canonical-first order. Mirror the resulting Codex skill byte-for-byte between `.codex/skills/` and `.agents/skills/`.

## Application Guide

1. Identify the required behavior and use current official guidance for the target model/runtime. Keep the structure that makes correct execution and completion observable.
2. Write task-specific decision, execution, completion, and escalation conditions under the applicable contract.
3. Supply only applicable pattern paths with scope, exact owned/forbidden paths, criteria, and worklog paths in writer dispatches. The canonical `select.py` preserves scenario/tag selection while excluding historical `claude-4-patterns/` and `raw/`. Its outputs are candidates to adapt, not a blanket assembly recipe; do not copy source payload into the Codex skill package.
4. Check frontmatter, reference paths, runtime vocabulary, uncertainty handling, rejection behavior, and any applicable safeguard decision.

## Examples

### Rejection Case

Reject a deployment prompt that requires an unconditional whole-package checksum and residual-task gate but supplies no evidence/likelihood, protected impact, cheapest adequate alternative, ordinary-path/new-failure cost, or removal/override/monitoring. Do not let it block routine config edits, copy/start, or intentional stop/restart.

This rejection does not remove a narrowly scoped integrity or task-drain control backed by credible corruption, security, data-loss, compliance, or irreversible-mutation risk. Preserve that justified high-impact control, require the same five fields, and use the existing independent reviewer.

## Sources And Adaptation

Shared source: `.claude/skills/prompt-patterns/SKILL.md`. Inventoried native inputs: `.codex/rules/codex-agent-config-patterns.md` and `.codex/rules/context-isolation.md`. [OpenAI GPT-6 guidance](https://developers.openai.com/api/docs/guides/latest-model) and [GPT-6 Astra prompting guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), checked 2026-10-06, govern native prompting. A-Team contracts and authored examples are project policy, not vendor text or unseen system prompts. Claude adaptive-thinking/manual-worked-solution advice is applied only to a selected Claude surface using its current model/mode guidance.
