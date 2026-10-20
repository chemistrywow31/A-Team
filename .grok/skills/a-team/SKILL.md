---
name: a-team
description: Make the main session adopt A-Team's coordinator workflow for Grok-native team design, capability maintenance, or named-target evolution.
disable-model-invocation: true
argument-hint: "[team description | capability maintenance | named-target request]"
---

# A-Team

Adopt `.grok/agents/team-architect.md` in the **current main session**. This skill is the coordinator entry, not a request to spawn a team-architect child. Use `/a-team` when exposed by the installed client, or the user's explicit A-Team request. If invoked inside a specialist task, return `BLOCKED: wrong-context invocation`; the parent coordinator must run the entry.

## Reasoning

- Identify new-team creation, A-Team capability maintenance, named-target maintenance, or explicitly requested fleet work before choosing a workflow.
- The branch's canonical authority is `AGENTS.md` plus `.grok/`. `reference/platform-sources/` preserves prior platforms for provenance and deliberate conversion; do not load it as instructions or start a runtime there.
- Generated teams have their own declared authority and target-local roster. `AGENTS.md` is a generic instruction filename; it does not alone classify a team as Codex or Grok.
- The executable delivery supported here is Grok-native. If active Claude/Codex output is requested, identify the original platform branch or an explicitly scoped conversion workflow; do not silently activate archived surfaces.

## Workflow

1. Read root `AGENTS.md`, `.grok/agents/team-architect.md`, and its startup policies. Keep main-session user dialogue, integration and synthesis; never dispatch a child coordinator.
2. Initialize `.worklog/{yyyymm}/{task-name}/` and retain references, findings, decisions and dialogue evidence. Reuse supplied requirements and authorization.
3. For a new team, confirm objective, scope/exclusions, workflow, role coverage, Grok-native format, execution constraints, canonical authority and requirements summary before planning. Honor explicit delegation of routine decisions; interim summaries need no repeated approval.
4. For capability maintenance, stay in assigned A-Team paths; no downstream inventory or authority question is needed. For a named target, inspect layout, actual runnable/activation/reference states, generation stamp, declaration and mappings. Ambiguous authority permits assessment only.
5. Route text-only edits preserving roles, rules, runtime, ownership, mapping, authority and surface state to `prompt-optimizer`. Route structural/runtime changes to `team-restructuring-master`, with a `decision-auditor` recommendation before implementation. A native runtime gap stays in the declared native family; authority/shared-design/conversion changes require the cross-platform lane.
6. Apply `.grok/policies/source-authority.md`: exact authorized real root, exact owned paths, nearest-parent/path confinement and consistent declaration/mapping. Edit declared canonical files first; regenerate only assigned mapped outputs sequentially under one owner.
7. Dispatch only the 12 specialists named by the coordinator playbook. This roster is prompt policy. Use the live `spawn_subagent` schema; select `subagent_type` only if it advertises the discovered role enum. Supply bounded task inputs and exact ownership; specialists do not delegate. Skill metadata does not enforce child type, tools, model or effort.
8. Observe advertised get-output/wait tools. Resume a completed child only for continued work with its context. For fresh review use a new child without `resume_from`, supplying frozen artifact paths and criteria; source-backed freshness is separate from installed runtime proof. Optional messaging must not be required for completion.
9. Generate under `teams/{team-name}/`: root `AGENTS.md`, flat `.grok/agents/`, native skills, core rule/on-demand policies, supported project configuration and `docs/RUNTIME-SETUP.md`. Follow `.grok/policies/output-structure.md`; use the accepted target roster, not A-Team's fixed role count.
10. Freeze one coherent batch for independent review. After correction, invalidate changed-file criteria and dependent mapping/parity checks. Run runtime preflight for new delivery, runtime changes or missing current readiness evidence; separate static validation, trusted discovery and effective model/tools. Dialogue review follows substantial discovery and remains retrospective.

## Self-Critique

Confirm user scope, a single declared authority, disjoint ownership and retained useful contracts. Verify that existing authorization was reused, untrusted/reference-only targets were not promoted, and no archive provenance was reported as live readiness. Backport generator defects to this branch's `.grok/` authority; main is outside this task's scope.

## Examples

**Capability maintenance:** “Improve A-Team so it can restructure older teams” changes generator contracts and focused fixtures. A target may provide a bounded read-only reproduction; this does not request fleet migration.

**Rejection case:** A runtime proposal promotes a reference-only foreign surface without a declared conversion plan. Continue assessment, return the missing authority choice, and leave that surface inactive. Do not spawn a second coordinator to resolve it.

## Source Attribution

- **Origin**: A-Team canonical skill, preserved at `reference/platform-sources/.claude/skills/a-team/SKILL.md`.
- **Integration**: Pattern B: Adapted Install; native Grok branch authority is `AGENTS.md` plus `.grok/`.
- **Retrieved**: 2026-10-20 from the verified base snapshot.
- **Modifications**: Native paths, loading and lifecycle; preserved task intent, examples and useful assets. Archive is reference-only.
