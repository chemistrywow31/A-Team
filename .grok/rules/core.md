---
name: Native Core
description: Route exact native policies while preserving scoped authority, ownership, and honest runtime evidence
---

# Native Core

## Applicability

This is the only always-loaded project rule. Read root `AGENTS.md` and the assigned role's startup references before acting; load complete policies by the triggers below, not every policy body on every turn.

## Required Policy Routing

- Every role reads `.grok/policies/execution-contract.md`, `.grok/policies/source-authority.md`, and `.grok/policies/context-management.md` at task startup.
- Coordinating a phase, dispatch, or status update: `.grok/policies/coordinator-mandate.md`, `.grok/policies/conversation-protocol.md`, `.grok/policies/worklog.md`, `.grok/policies/reviewer-mandate.md`, `.grok/policies/supervision.md`.
- Authoring prompts/rules/skills: `.grok/policies/yaml-frontmatter.md`, `.grok/policies/writing-quality-standard.md`, `.grok/policies/prompt-engineering-patterns.md`, `.grok/policies/reasoning-and-self-critique.md`, `.grok/policies/output-structure.md`.
- Selecting native runtime/context: `.grok/policies/grok-agent-config.md`, `.grok/policies/grok-runtime-config.md`, `.grok/policies/context-isolation.md`, `.grok/policies/context-tier.md`.
- Proposing hooks: `.grok/policies/grok-hooks.md`. Proposing/retaining non-obvious safeguards: `.grok/policies/proportional-design.md`. Making recommendations: `.grok/policies/anti-sycophancy.md`.
- Reviewing artifacts: relevant policy criteria and `JUDGMENT.md`; independent acceptance uses a new child without `resume_from`, frozen paths, and criteria only.

## Always Applicable Boundaries

`.grok/` plus `AGENTS.md` is this branch's explicit canonical authority. Archives are reference data. Honor the selected target's own declaration; never infer authority from a filename or activate a reference surface.

Root coordinates directly; specialists do not delegate. Native definitions are flat. Preserve exact assigned ownership, same-owner canonical-first regeneration, and concurrent edits. Existing user authorization persists across phases; ask only for material missing choices or uncovered actions.

Use the advertised native tool schema. Root's 12-specialist roster is prompt policy; parsed metadata and `grok inspect --json` do not prove effective tools, model, effort, or context. Preserve trust/approvals and report missing live evidence as UNVERIFIED.

## Violation Determination

- A triggered policy is not read, ownership is exceeded, or reference data becomes active authority -> Violation.
- A specialist delegates, a fresh review resumes producer history, or discovery is called functional runtime proof -> Violation.

## Exceptions

Read each applicable policy once while its content remains current. A clarification-only turn may defer artifact-specific reads until that work begins; host instruction precedence always governs.
