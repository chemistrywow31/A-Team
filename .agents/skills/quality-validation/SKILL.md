---
name: Quality Validation
description: Validate that a generated Codex team is structurally complete and internally consistent
---

# Quality Validation

## Description

Validate generated teams and A-Team repo-self from fresh context. Capture mechanical evidence first, then add only the semantic judgment the validators cannot automate.

## Users

- `.codex/agents/team-architect.md`
- Fresh-context reviewers validating generated or existing teams

## Core Knowledge

- Validation starts with deterministic classification, not assumptions. Record layout separately from runnable surfaces.
- Every Codex validation report must include `STAMP`, `CANONICAL_AUTHORITY`, and `MAPPING_STATE` evidence.
- Ambiguous canonical authority blocks mutation. Reference-only mirrors and activation-gated packages are assessed, not promoted.
- Codex v2 readiness requires both static validation and live host-tool readiness; do not collapse those into one verdict.
- `.codex/skills/` and `.agents/skills/` mirrors must remain byte-identical.

## Application Guide

1. Choose the validation mode: generated target team or A-Team repo-self.
2. Classify the target before judging content. Capture direct root, class, runnable surfaces, reference-only or activation-gated state, stamp, canonical authority, and mapping state.
3. Run the full Codex validator first and write its raw output to a verifier-owned worklog or evidence file. Do not use assessment-only classification output as acceptance evidence.
   - Target team: `python3 scripts/validate_codex_team.py {team}`
   - Repo-self: `python3 scripts/validate_codex_team.py --repo-self`
4. If the target has a Claude-runnable surface, run `bash scripts/validate-team.sh {team}` for that surface too.
5. Return EC-3.6 lines as `{criterion} | PASS|FAIL|SKIP | {evidence-path}`, followed by the overall verdict. Do not paste raw validator output into the report. Add model judgment only for semantic checks the scripts mark `SKIP` or do not cover.
6. When a runnable or changed Codex surface exists, run read-only runtime preflight and write its raw output to verifier-owned evidence.
   - Repo-self: `bash scripts/preflight-codex-runtime.sh --repo-self`
   - Target team: `bash scripts/preflight-codex-runtime.sh --team-dir {team}`
7. Fail validation if any of these hold: strict config does not load, registry paths do not resolve from `.codex/`, v2 keys are missing or misplaced, stale runtime vocabulary remains, skill mirrors differ, mapping or stamp evidence is missing, runtime setup lacks setup/verify/rollback guidance, or target classification contradicts the inventory.
8. Keep static validation separate from live host-tool readiness. A static pass does not prove the active host exposes the required collaboration tools.

## Quality Checkpoints

- [ ] The report includes classification plus `STAMP`, `CANONICAL_AUTHORITY`, and `MAPPING_STATE`.
- [ ] Mutation was blocked when canonical authority was ambiguous.
- [ ] Codex validation checked strict config, v2 runtime keys, registry resolution, mirror parity, and stale-vocabulary absence.
- [ ] Raw validator and preflight output stayed in verifier-owned evidence files; criterion lines cited those paths.
- [ ] Runtime preflight documented setup, verify, and rollback separately from static validation.
- [ ] Surface-specific reference-only or activation-gated declarations were respected.

## Example

### Input

`Validate teams/u-team for Codex restructuring readiness.`

### Output

Classify `teams/u-team` as dual layout with Codex-only runnable status, run the full Codex validator and runtime preflight, store raw output in verifier-owned evidence files, and return criterion verdicts citing those paths.
