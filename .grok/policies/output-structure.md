---
name: Output Structure
description: Generate complete native Grok teams with target-local rosters, declared authority, and verified setup
---

# Output Structure

## Applicability

- Applies to coordinators, planners, all writers, and delivery reviewers.

## Rule Content

### Confirm Delivery Before Generation

Generate deliverables under `teams/{team-name}/` unless the external-root gate in `.grok/policies/source-authority.md` passes. Confirm objectives, scope, workflow, role coverage, requested format, one canonical authority, activation state, conversion-retention need, and the requirements summary before planning a new team. Reuse prior answers and delegated routine choices.

This branch's executable delivery format is `grok-native`. If another runtime is requested, record an explicit conversion or maintained-branch handoff; do not claim this branch implements or verifies that runtime. Never copy archived surfaces into an active root merely to satisfy a format name.

### Required Native Layout

A runnable Grok team contains:

- Root `AGENTS.md`: objectives, scope, unique authority and canonical roots, deployment mode, target-local role map, precedence, worklog/context contract, and generator stamp.
- Flat `.grok/agents/{role-name}.md`: the confirmed coordinator and specialists; one role per unique kebab-case stem/name. No nested role folders.
- `.grok/skills/{skill-name}/SKILL.md`: required skills and their referenced scripts/assets; exactly one coordinator-entry skill for a multi-agent workflow, adopting the current session's coordinator playbook.
- `.grok/rules/core.md`: a short always-loaded bootstrap naming the governing policy paths and read triggers. Keep complete task policies under `.grok/policies/`, with startup reads named in role bodies.
- `.grok/config.toml`: minimal supported project configuration under `.grok/policies/grok-runtime-config.md`; do not invent project settings for model, effort, trust, or hooks.
- `docs/RUNTIME-SETUP.md`: actual version/probe stamp, prerequisites, startup, validation, activation gaps, effective-runtime evidence, verification and rollback.
- `briefs/{role-name}.md` for every role, produced by `scripts/render_helper_briefs.py` and left byte-identical to that renderer. Identity, Responsibilities, Input and Output, Workflow, Boundaries, and Completion Contract must be sufficient for a specialist with no other conversation. Do not hand-edit briefs.
- `docs/task-board.schema.json`: a copy of `schemas/task-board.schema.json`. The coordinator keeps `.worklog/task-board.json` and the owner report from `.grok/policies/supervision.md` current. `.worklog/` remains runtime state.
- `.grok/docs/format-mapping.md` and `.grok/docs/format-mapping.json` when multi-surface/conversion retention requires them.

A procedural helper such as `GROK.md` is ordinary documentation; it is not an auto-loaded entry. Keep generated paths portable and resolve project-relative inputs from the actual target root.

### Preserve The Full Workflow

Use the target's accepted roles, not A-Team's fixed 13-role designer inventory. Preserve role ownership, input/output handoffs, adjacent Reasoning → Workflow → Self-Critique, actionable uncertainty, boundaries, completion contract, and meaningful rejection examples.

Include complete execution-contract, worklog, context-management, reasoning/self-critique, and conditional proportional-design rules or documented equivalents in every multi-agent/multi-phase delivery. Include other applicable authority, metadata, quality, and review policies needed to make that target execute correctly. A bootstrap with unresolved links is not a policy implementation.

Generated teams have one coordinator, direct specialists only, source-backed Task denial for specialists, and a roster declared as prompt policy. Preserve independent EC-3 artifact acceptance and the process-review requirements/three-or-fewer-role exception. Small teams must not inherit every designer specialist merely to satisfy a count.

### Native Metadata And Existing Choices

Apply `.grok/policies/yaml-frontmatter.md`, `.grok/policies/grok-agent-config.md`, and `.grok/policies/context-isolation.md`. Omit new untested model/effort overrides; preserve existing explicit target pins during unrelated maintenance. Native skill metadata does not grant permissions or establish effective model routing.

Follow project permissions and actual trust without broadening them to make generation or tests pass. Optional hooks require the source-backed and installed evidence in `.grok/policies/grok-hooks.md`; complete worklog bookkeeping in the coordinator workflow even when no hooks are configured.

### Mapping And Activation

For retained mappings, record source and target paths, requested format, canonical authority, runnable/reference-only states, lossy decisions, platform-only assets, and reverse strategy. Use `kind: generated-team` with its accepted inventory. Single native surface delivery need not carry A-Team's 201-file source archive.

After producers freeze, execute appropriate static validation and installed discovery; separately probe effective tools, role selection, context, and model/effort only with authorized access and bounded cost. Keep missing evidence UNVERIFIED or activation-gated. A discovered file is not functional readiness.

## Violation Determination

- New-team generation starts without confirmed requirements, format, or authority -> Violation.
- A requested native entry, role, required skill/policy/config, brief, task-board schema copy, or setup advisory is absent, stale, or a reference is broken -> Violation.
- The coordinator contract does not update `.worklog/task-board.json` and the owner report -> Violation.
- Native roles/rules are nested, an entry skill spawns the coordinator, or a generated roster is forced to A-Team counts -> Violation.
- Existing model/effort changes without scope, unsupported project settings, or assumed effective metadata -> Violation.
- Required mappings omit authority, activation state, or assigned path coverage -> Violation.
- Setup lacks a probe stamp, verify/rollback steps, or separates neither discovery nor effective execution -> Violation.

## Exceptions

An explicitly single-agent target may omit child definitions and a separate entry skill; document single-session execution and retain applicable quality, authority, and setup requirements. An unmapped single native surface may omit conversion artifacts.
