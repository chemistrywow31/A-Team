---
name: Quality Validation
description: Canonical validation checklist for generated team structures, executed by a fresh-context verifier
disable-model-invocation: true
---

# Quality Validation

## Description

Validate generated teams and A-Team repo-self from fresh context. The producer never accepts its own work; a verifier stores raw command evidence in an owned evidence file and returns criterion verdicts that cite that path.

## Users

- Fresh-context verifier dispatched by `team-architect`

## Core Knowledge

- Validation starts with deterministic classification, not assumptions. Record layout separately from runnable surfaces.
- Every Codex validation report must include `STAMP`, `CANONICAL_AUTHORITY`, and `MAPPING_STATE` evidence.
- Ambiguous canonical authority blocks mutation. Reference-only mirrors and activation-gated packages are assessed, not promoted.
- Codex v2 readiness requires both static validation and live host-tool readiness; do not collapse those into one verdict.
- For Codex skills, `.codex/skills/` and `.agents/skills/` mirrors must remain byte-identical.

## Application Guide

1. Choose the validation mode: generated-team validation or A-Team repo-self Codex validation.
2. Classify the target before judging content. Capture direct root, class, runnable surfaces, reference-only or activation-gated state, stamp, canonical authority, and mapping state.
3. Run the full mechanical validator first and write its raw output to a verifier-owned worklog or evidence file. Do not use assessment-only classification output as acceptance evidence.
   - Claude surface: `bash scripts/validate-team.sh {team}`
   - Codex target team: `python3 scripts/validate_codex_team.py {team}`
   - A-Team repo-self Codex surface: `python3 scripts/validate_codex_team.py --repo-self`
4. Return EC-3.6 lines as `{criterion} | PASS|FAIL|SKIP | {evidence-path}`, followed by the overall verdict. Do not paste raw validator output into the report. Add model judgment only for semantic checks the script marks `SKIP` or does not cover.
5. When a runnable or changed Codex surface exists, run read-only runtime preflight.
   - Repo-self: `bash scripts/preflight-codex-runtime.sh --repo-self`
   - Target team: `bash scripts/preflight-codex-runtime.sh --team-dir {team}`
6. Store raw preflight output in verifier-owned evidence and keep static validation separate from live host-tool readiness. A static pass does not prove the active host exposes the required collaboration tools.
7. Fail validation if any of these hold: strict config does not load, registry paths do not resolve from `.codex/`, v2 keys are missing or misplaced, stale Codex runtime vocabulary remains, skill mirrors differ, mapping or stamp evidence is missing, runtime setup lacks setup/verify/rollback guidance, or target classification contradicts the inventory.
8. If the target is Claude-runnable or dual, validate the Claude surface as well; if the target is Codex-runnable or repo-self Codex, validate the Codex surface as well.

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
