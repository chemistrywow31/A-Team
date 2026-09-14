---
name: Prompt Patterns
description: Apply Codex-native prompt patterns for agents, skills, rules, and project instructions
---

# Prompt Patterns

Use this skill when generating or optimizing agent prompts, skills, rules, or project instructions. Select only guidance relevant to the assigned artifact; historical Claude research assets stay under the canonical source tree.

## Compact Generation Contract

- Give each agent exactly one adjacent `Reasoning`, `Workflow`, and `Self-Critique` sequence in that order: role-specific decision criteria, execution steps, then checks of likely failures. Do not duplicate this contract with mandatory `Preflight`/`Verification` blocks or fixed four/five-slot essays.
- Request concise decisions and verification evidence, never private reasoning transcripts. Keep input/output, ownership, boundaries, uncertainty, and completion requirements explicit.
- Include exactly one rejection example in each agent or skill. Choose the boundary that changes behavior; do not mandate normal or edge examples.
- Reuse confirmed requirements and existing authorization. Ask only for material missing decisions, unresolved authority, or actions outside that authorization. Continue independent work during supported asynchronous clarification; unanswered required questions do not supply approval.
- Give the existing independent reviewer one coherent frozen artifact batch. After fixes, rerun every criterion citing a changed file plus dependent mappings/parity. Run preflight for new delivery, changed active runtime artifacts, or missing current readiness evidence; reuse its current validator and strict-model results.
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
- Translate lifecycle, tool, path, and isolation intent to Codex-native constructs. Runtime permissions belong in config/TOML; do not copy Claude-only skill frontmatter or runtime assumptions.
- Preserve exact assigned ownership, declared authority/mappings, and canonical-first order. Mirror the resulting Codex skill byte-for-byte between `.codex/skills/` and `.agents/skills/`.

## Application Guide

1. Identify the required behavior and choose the smallest structural instruction that makes it observable.
2. Write task-specific decision, execution, completion, and escalation conditions under the applicable contract.
3. Supply selected pattern paths with scope, exact owned/forbidden paths, criteria, and worklog paths in writer dispatches.
4. Check frontmatter, reference paths, runtime vocabulary, uncertainty handling, rejection behavior, and any applicable safeguard decision.

## Examples

### Rejection Case

Reject a deployment prompt that requires an unconditional whole-package checksum and residual-task gate but supplies no evidence/likelihood, protected impact, cheapest adequate alternative, ordinary-path/new-failure cost, or removal/override/monitoring. Do not let it block routine config edits, copy/start, or intentional stop/restart.

This rejection does not remove a narrowly scoped integrity or task-drain control backed by credible corruption, security, data-loss, compliance, or irreversible-mutation risk. Preserve that justified high-impact control, require the same five fields, and use the existing independent reviewer.
