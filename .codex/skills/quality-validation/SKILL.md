---
name: Quality Validation
description: Validate generated Codex teams and A-Team repo-self through independent artifact review and current runtime evidence
---

# Quality Validation

## Description

Review one coherent frozen artifact batch from fresh context. The producer never accepts its own work; the verifier stores raw command evidence in owned files and returns criterion verdicts citing those paths.

## Users

- Fresh-context verifier dispatched by `team-architect`

## Core Knowledge

- Classify layout separately from runnable surfaces. Record the target's stamp, canonical authority, and mapping state.
- Ambiguous authority permits assessment only. Never promote reference-only or activation-gated surfaces implicitly.
- Read repo-root `JUDGMENT.md` J5 for the canonical quality floors. A green validator cannot override them; a false PASS blocks acceptance until the validator defect and the underlying failure are resolved.
- Verify native schema from current platform evidence; preserve supported Claude model forms, skill names and `paths`, and distinguish tooling metadata from runtime skill preload. Select Codex checks from the target-supported profile rather than universally requiring observed-host v2 keys.
- Keep static validation and live host-tool readiness as separate verdicts. Static config cannot prove that the active host exposes collaboration tools.

## Application Guide

1. Confirm the batch is frozen and choose generated-team or A-Team repo-self validation. Capability-only source maintenance does not require downstream team inventory or mutation. Repo-self means the repository root. Capture target class, runnable surfaces, activation/reference state, stamp, authority, and mappings before judging content; classification-only output is not acceptance evidence.
2. Run `python3 scripts/check_work_shape.py {team}` (add `--surface codex` for a Codex surface) and read the record. Judge each trigger's evidence against the flow: sequential stages are not parallel work, and a human approver already is an isolated check. A record that passes the script on evidence that is not true of the flow fails J5.8. The profile it prints selects the floors:
   - `skill-workflow`: the short entry document (J5.7), the skills (J5.2), assigned settings (J5.4), and `docs/RUNTIME-SETUP.md`. Agent definitions, a coordinator entry or a rule pack in such a team are a failure, not a bonus.
   - `agent-group`: also the agents (J5.1), exactly one Claude coordinator entry where a Claude surface is runnable (J5.2), one handoff contract rule (J5.3), and the main-session statement (J5.7). Every role traces to a trigger in the record.
   - `legacy`: the validator applies the contract the team was built under; report its result and do not hold new work to it.
   Then read every authored file against the target's writing-quality-standard and report, per file, anything repeated, conflicting, copied from A-Team's own pack without a flow that needs it, or always loaded but rarely needed. A file over its 300/200/100-line mark is `REVIEW_REQUIRED` until you accept or reject it with a reason. Reports and A-Team worklogs keep their own floors (J5.5, J5.6).
3. When the batch proposes or retains a non-obvious safeguard, apply `.codex/rules/proportional-design.md` and return verdicts for its five decision fields and ordinary-path preservation. Use this existing review stage.
4. Select evidence-producing commands for each runnable surface after runtime artifacts freeze. For a generated Claude team, run `bash scripts/validate-team.sh {team}`. For A-Team repo-self native review, check affected authored files against J5 and run focused native regressions; report that scope without claiming whole generated-package validation or ignoring failures within the selected scope. Reuse current validator evidence already supplied by applicable runtime preflight; store raw output in verifier-owned files. Missing, malformed, or failing evidence remains a failed criterion.
5. Apply the Codex Surface Checks below only when reviewing a Codex-runnable target or the repo-self Codex surface. For a dual team, cover both runnable surfaces. Add focused tests only for changed behavior or unresolved failures.
6. Inspect artifacts against the compiled checklist, adding independent semantic judgment and checking mechanical floors omitted or mis-evaluated by the scripts. Check current authority/mappings/stamps, required platform metadata, native vocabulary, and runtime setup/verify/rollback guidance for applicable surfaces.
7. After a correction, invalidate and rerun every criterion citing a changed file plus dependent mapping/parity checks. Retain only unaffected current evidence; repeat preflight when its runtime/readiness evidence was invalidated. Keep one batch review rather than separate reviewer invocations per file.
8. Return one EC-3.6 verdict line per acceptance criterion with its evidence path and an overall verdict. Keep raw command output in the evidence files. Any relevant J5 failure, validator false PASS, contradictory classification, or failed runtime criterion prevents overall PASS.

## Codex Surface Checks

Only for a selected Codex runnable surface, read `.codex/rules/codex-agent-config-patterns.md` and `.codex/rules/codex-runtime-config.md`, then apply these checks:

- Record `STAMP`, `CANONICAL_AUTHORITY`, and `MAPPING_STATE`. Require `agent_type` in each Codex playbook and `model` in its directly paired TOML.
- Check the target-supported config schema/validation command, registry resolution from `.codex/`, the declared runtime profile, and byte identity between `.codex/skills/` and `.agents/skills/` mirrors.
- Run preflight for new delivery, changed active runtime artifacts, or missing current readiness evidence: `bash scripts/preflight-codex-runtime.sh --repo-self` for A-Team, or `bash scripts/preflight-codex-runtime.sh --team-dir {team}` for a target team.
- Retain raw preflight output and reuse its current full validator records and runtime/model probe result; do not rerun the same validator or model check separately.
- Where current preflight evidence does not cover a required Codex check, run `python3 scripts/validate_codex_team.py --repo-self` or `python3 scripts/validate_codex_team.py {team}` for the corresponding root and retain its raw output.

## Examples

### Size Review

A 220-line authored skill retains a useful worked conversion example. Record `REVIEW_REQUIRED`; inspect whether that example changes correct execution, and resolve the size criterion independently. Keep missing metadata or boundary examples as separate failures.

### Rejection Case

Reject an overall PASS when validators are green but the entry document lists the directory tree and repeats a skill's steps. Cite the repeated lines against the writing standard, then recheck the corrected file.

## Sources And Adaptation

Shared source: `.claude/skills/quality-validation/SKILL.md`. Codex schema/registry/profile checks come from the inventoried `.codex/rules/codex-runtime-config.md` and `.codex/rules/codex-agent-config-patterns.md`. Preserve the runtime’s supported validation command and distinguish published schema from A-Team’s observed host.

J5 and the execution contract define A-Team acceptance. Native claims follow [Claude subagents](https://code.claude.com/docs/en/sub-agents), [Claude skills](https://code.claude.com/docs/en/skills), and the inventoried Codex runtime rules, checked 2026-10-06. Runtime evidence must name the client/profile and distinguish static validity, live tools, and model access.
