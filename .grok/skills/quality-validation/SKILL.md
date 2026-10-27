---
name: quality-validation
description: Review frozen Grok-native team artifacts independently against J5, mapping and measured runtime evidence.
disable-model-invocation: true
---

# Quality Validation

Review one coherent frozen batch from fresh context. The producer never accepts its own output; the verifier stores command evidence in owned files and returns verdicts tied to the current artifact state.

## Reasoning

- Classify layout separately from runnable surfaces; record stamp, authority, mapping and activation/reference state. Missing authority permits assessment only.
- Read `JUDGMENT.md` J5 and `.grok/policies/reviewer-mandate.md`. A green parser cannot override a semantic quality failure or promote a reference-only surface.
- Grok source at a pinned revision, installed CLI parsing/discovery, and effective model/tool execution are different evidence. Skills cannot enforce model/effort/tool restrictions; unknown metadata may be ignored.
- Repo-self requires the documented 13 roles/11 skills/20 policies. Generated teams use their accepted roster and actual requirements; do not force designer counts onto them.

## Workflow

1. Confirm producer freeze and exact root, owned report paths, scope and acceptance criteria. New reviewer dispatch omits `resume_from`; reuse of a completed child is not fresh-context review. Observe installed behavior separately from source-backed lifecycle expectations.
2. Compile relevant J5 floors once:
   - Agents: line-1 nonempty name/description, flat `.grok/agents/{name}.md`, valid native fields, exactly one adjacent Reasoning/Workflow/Self-Critique sequence, Boundaries, Uncertainty Protocol, Examples with a meaningful rejection case, ownership and completion.
   - Skills: native folder and nonempty metadata, meaningful rejection/defer/escalation example, usable instructions and source attribution. Identify coordinator-entry purpose independently of folder name: exactly one entry adopts a resolvable coordinator playbook in the main session; never spawn that coordinator. Manual-only review skills are not coordinator entries.
   - Policies: metadata, actionable contract, Violation Determination and Exceptions. Keep the always-loaded core small and resolve all role startup policy paths.
   - Size: agent/skill/policy above 300/200/100 lines is REVIEW_REQUIRED. Inspect the usefulness rationale and independently accept or reject the current file. Parser success alone does not resolve it.
   - Reports: six EC-1 fields in order, conclusions at most ten lines, evidence for DONE, substantive references/findings/decisions and current source links.
   - Root: actual objectives/scope, main coordinator, precedence, worklog, declared `.grok/` authority and generation stamp. Configuration must use supported project sections and preserve approval/trust boundaries.
3. Check `.grok/policies/source-authority.md` against declarations, mapping roots, exact coverage and snapshot states. Inspect native bodies for semantic fidelity, not just renamed paths. Treat the archive as provenance, never active runtime evidence.
4. When a non-obvious safeguard is proposed or retained, apply `.grok/policies/proportional-design.md` and return verdicts for its five fields and ordinary-path preservation. Use this review stage, not an added approval ladder.
5. Run current native validation for the scoped root: `python scripts/validate_grok_team.py --repo-self` for the designer, or `python scripts/validate_grok_team.py {team-root}` for a target. Use the configured Python environment (Python >=3.11 plus PyYAML). Retain output; missing or failed evidence is a failed criterion.
6. Run/reuse focused tests and `bash scripts/preflight-grok-runtime.sh --repo-self` or `bash scripts/preflight-grok-runtime.sh {team-root}` for new delivery, runtime changes or missing readiness evidence. Reuse current preflight validation rather than rerunning identical checks. Never run a global/real-team inventory for capability-only maintenance.
7. Inspect installed `grok inspect --json` exact project source paths and projectTrusted state. Exclude competing project loaders; report inherited user/global sources separately. `inspect` does not prove effective tools, Task denial, fresh context, model or effort. Keep missing live evidence NOT_PROBED/UNVERIFIED; do not guess authentication status.
8. After fixes, invalidate every changed-file criterion plus dependent mapping/runtime criteria; retain unrelated current evidence. Return `{criterion} | PASS or FAIL | evidence` and an overall verdict under EC-1. Report static/discovery acceptance separately if effective runtime criteria remain unverified; do not claim full readiness.

## Self-Critique

Read actual files, trace each verdict to current evidence, and check that no omitted requirement or silent schema field creates a false PASS. Preserve useful examples and full contracts. Confirm the verifier is independent and that no trust, credentials or global settings were changed to obtain a pass.

## Examples

**Size review:** A 220-line skill retains a worked conversion example. Record REVIEW_REQUIRED, inspect whether it changes correct execution, and decide the size criterion independently; missing metadata remains a separate failure.

**Rejection case:** Validators exit zero but an agent places Self-Critique before Workflow. Fail the J5 ordering criterion and the false-PASS behavior, then recheck both corrected artifacts and dependent mappings. A listed agent in an untrusted inspect is likewise insufficient proof of skill activation.

## Source Attribution

- **Origin**: A-Team canonical skill, preserved at `reference/platform-sources/.claude/skills/quality-validation/SKILL.md`.
- **Integration**: Pattern B: Adapted Install; native Grok branch authority is `AGENTS.md` plus `.grok/`.
- **Retrieved**: 2026-10-20 from the verified base snapshot.
- **Modifications**: Native paths, loading and lifecycle; preserved task intent, examples and useful assets. Archive is reference-only.
