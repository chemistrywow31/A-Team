# A-Team Grok Runtime

## Purpose and authority

A-Team designs multi-agent teams; it is not the target team itself. Generate deliverables under `teams/{team-name}/`, with the team's own accepted role set and format.

**This branch explicitly declares root `AGENTS.md` plus `.grok/` as its sole active canonical design and Grok as its runnable platform.** Shared role intent, workflow, ownership and quality changes start here. The original Claude/Codex baseline at `reference/platform-sources/` is reference-only conversion/provenance data, never an active instruction source. Main retains its original authority. Read `.grok/docs/format-mapping.json` and `.grok/policies/source-authority.md` for the exact boundary. Do not start Grok inside the archive.

## Design principles

- Optimize prompt effectiveness using current official guidance for the selected platform and model. Preserve useful examples, XML boundaries, task steps and checks; concision is secondary.
- Complete the full requested result when the extra cost materially improves reliability. Stop broadening checks after applicable criteria pass unless new evidence warrants more.
- Inspect unfamiliar context and verify current tools or external facts before decisions that depend on them. Make evidence-backed recommendations with a clear position.
- Prefer explicit sections, output slots, completion contracts and uncertainty protocols over vague reminders. Use one compact task-specific Reasoning → Workflow → Self-Critique contract; do not request private reasoning transcripts or duplicate generic forms.
- Default to the cheapest adequate design. Apply `.grok/policies/proportional-design.md` only to non-obvious safeguards; unsupported rare hypotheticals become assumptions or monitoring rather than blockers.

## Main-session coordinator

The current main session adopts `.grok/agents/team-architect.md` when A-Team is requested, including through `.grok/skills/a-team/SKILL.md`. Never spawn the coordinator as a child or create a relay coordinator. Communicate in the user's language. Specialists return questions through the coordinator under the conversation protocol.

Read the main playbook's startup policies before dispatching. `.grok/rules/core.md` is the short automatic bootstrap; full policies are in `.grok/policies/` and are loaded by role/task. Keep exact paths in dispatches rather than assuming parent skills or policy content is inherited.

The coordinator's approved child roster is requirements-analyst, role-designer, domain-researcher, decision-auditor, skill-planner, rule-writer, skill-writer, agent-writer, prompt-optimizer, runtime-preflight-advisor, dialogue-reviewer and team-restructuring-master. This roster is prompt policy. The coordinator omits a tools allowlist to preserve Grok's native tools. Specialists declare `disallowedTools: [Task]`; effective enforcement must be observed independently of metadata parsing.

Use only the lifecycle actually advertised by the installed client. Source-backed default model-facing names are `spawn_subagent`, `get_command_or_subagent_output`, `wait_commands_or_subagents` and `kill_command_or_subagent`. Spawn uses `background`; select an exact `subagent_type` only if the live schema offers it. Never claim named-role controls were applied to an untyped general-purpose fallback. Optional active messaging must not be a required workflow primitive.

Assign stable phase-purpose task names, exact owned/forbidden paths, ready inputs, acceptance criteria, report destination and persistence owner. All agents share the filesystem: preserve concurrent changes, keep writers disjoint, and serialize canonical changes plus any same-family projection. Specialists do not delegate. Cancel only when a task is invalidated or unsafe; wait at real join points while independent work continues.

## Workflow and authorization

1. Classify the request as new-team design, A-Team capability maintenance, named-target maintenance or explicitly requested fleet work. Capability improvement alone does not authorize downstream inventories or target writes; bounded read-only examples may reproduce a designer defect.
2. For a new team, confirm objectives, scope, workflow, role coverage, requested format, authority and a requirements summary. Reuse answers and delegated routine choices. Scoped maintenance starts with classification rather than repeating discovery.
3. Plan roles, skills, rules, ownership and runtime evidence; obtain the decision-auditor recommendation gate for structural changes. Existing user authorization covers its scoped reversible work; ask only about material missing choices, unresolved authority, uncovered scope or irreversible/external actions.
4. Generate complete native artifacts through the assigned writers. Preserve target model/effort choices unless their migration is authorized. Runtime features must come from target-specific evidence, not another platform's schema.
5. Freeze one coherent batch. Obtain an independent fresh-context artifact review and runtime preflight when runtime files changed. A new Grok child without `resume_from` is source-backed fresh context; give the reviewer only acceptance criteria and frozen artifact paths. Installed behavior remains a separate observation.
6. Apply optional text optimization and rerun every criterion citing changed files plus dependent mapping/runtime criteria. Carry forward unrelated current evidence. Deliver the result, setup and honest limitations.
7. Run dialogue review after substantial discovery or when requested; it is a retrospective, not a repeated permission gate.

Follow host instruction precedence: explicit user instructions outrank repository guidance and skills. An action request authorizes its scoped reversible work. Interim summaries do not require renewed approval; continue independent work while questions are pending, without treating silence as a required answer.

## Execution and quality

`.grok/policies/execution-contract.md` defines EC-1 reports, EC-2 evidence-based retries, EC-3 independent acceptance, EC-4 precedence and EC-5 context economy. `JUDGMENT.md` and `templates/` supply judgment and dispatch structures. Producers do not accept their own artifacts, and the coordinator is not the sole acceptor.

Each specialist returns STATUS, CONCLUSIONS, EVIDENCE, ARTIFACTS, RISKS/UNKNOWNS and NEXT. Persist reports at the assigned path. If the host blocks persistence, use only a preassigned bounded INLINE-FALLBACK, with the coordinator persisting the evidence; do not broaden permissions.

Maintain `.worklog/{yyyymm}/{task-name}/phase-{n}-{label}/` with traceable references, findings and decisions, and the conversation record required by `.grok/policies/conversation-protocol.md`. Record concise evidence and decisions, not private reasoning transcripts.

Generated teams must include a main-session coordinator, explicit ownership and completion contracts, independent artifact/code review when appropriate, process review duties under `.grok/policies/reviewer-mandate.md`, the required worklog/context/execution/reasoning/proportional policies, and `docs/RUNTIME-SETUP.md`. Apply the documented small-team review exception when adequate; do not copy A-Team's entire designer roster into every target.

## Supervision surfaces

Generated teams keep the Grok Build layout above and also ship one portable brief per role at `briefs/{role}.md`, rendered by `scripts/render_helper_briefs.py`. A lead that runs the team as short-lived specialists hands the brief plus a task envelope to a specialist that starts with no conversation. The specialist returns one result to the lead and does not spawn or message peers or the user. Native Grok sessions still load `.grok/agents/` and `.grok/rules/`. Briefs are assignments, not agent definitions.

The lead maintains `.worklog/task-board.json` against `schemas/task-board.schema.json` and writes the owner report defined in `.grok/policies/supervision.md`. Cost and token fields stay empty until the host reports them. `.worklog/` remains runtime state and is gitignored. `disallowedTools: [Task]` is the source-backed specialist limit when a Grok client loads the agent file. The brief repeats that limit. This repository does not treat either one as proof that a live session enforced it.

`examples/research-desk/` is a tracked three-role sample that passes the validator in the native layout and ships the briefs, schema copy, sample board, and sample owner report. Its setup notes keep model access NOT_PROBED.

## Existing-team evolution

Record layout and runnable surfaces separately: Grok-only, foreign-only, multiple surfaces, reference-only, non-team or incomplete/activation-gated. Read generation stamps, declarations and required mappings before mutation. This repository's authority never overrides a target's own declaration, and a reference-only surface is never promoted implicitly.

Use prompt-optimizer only for text-only improvements preserving roles, rules, runtime, ownership, mapping, authority and parity. Structural/runtime changes use team-restructuring-master for the smallest justified plan, recommendation audit, exact writer ownership, fresh artifact acceptance and relevant preflight. Distinguish a Grok-only runtime gap from a cross-platform design gap. A generator defect is corrected in this branch's canonical `.grok/` family first.

External target writes require user authorization for one exact real root, exact owned paths and one consistent authority. A Grok target declares its native authority in `AGENTS.md`; foreign sources retain their declared authority until conversion is explicitly scoped. Multi-surface or conversion-retained targets require complete source/target and runnable/reference-only mappings. Missing/conflicting authority, multiple canonical claims, incomplete mappings, `..`, outside absolute paths or root/parent symlink escape blocks the affected mutation. Continue unaffected read-only analysis. Edit the declared canonical family first and regenerate mapped projections sequentially under one owner with scoped verification and rollback.

## Native runtime boundary

- Use flat `.grok/agents/*.md` and `.grok/skills/<name>/SKILL.md`. Nested role/rule discovery is not supported by the observed client.
- Project `.grok/config.toml` is limited to its supported permission, MCP and plugin sections. Project model, effort, compatibility or global approval defaults are not configurable here.
- This branch omits role model/effort pins. Source supports parent-model inheritance; effort omission retains installed session/default behavior. Do not invent provider-equivalent model tiers.
- Skill metadata `allowed-tools`, `model` and `effort` does not enforce tool restrictions or model routing.
- Preserve native trust, permission and sandbox controls. No project file can grant itself trust. Do not change global settings or copy credentials as a readiness workaround.
- `grok inspect --json` proves discovery and trust state only. It does not prove effective tools, role selection, model/effort, fresh context or model quality. Static validation, installed discovery and effective runtime each need their own evidence.
- The initial source input and installed build differ; current behavior must be probed after upgrades. See `.grok/docs/RUNTIME-SETUP.md` for dated results and `GROK.md` for operation commands. `GROK.md` itself is not auto-loaded.

## Role and policy lookup

All role playbooks are `.grok/agents/<role-name>.md`. The main playbook lists their responsibilities and startup requirements. Full policy names and preserved source mappings are in `.grok/docs/format-mapping.json`; use `.grok/policies/output-structure.md`, `.grok/policies/grok-agent-config.md`, `.grok/policies/grok-runtime-config.md`, `.grok/policies/source-authority.md` and `.grok/policies/context-isolation.md` for generation and maintenance contracts.

---

Generated by A-Team on 2026-10-20

Adapted by A-Team for Grok on 2026-10-20; baseline source preserved in `reference/platform-sources/`.
