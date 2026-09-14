# Codex Runtime Setup — A-Team repo-self

> Preflight stamp: `2026-09-14T16:22:48+0800`; target: `/Users/wow/wrk/sp/A-Team`; mode: `repo-self`.
> Evidence: [raw current preflight output](../../.worklog/202609/codex-platform-boundaries/phase-3.5-preflight/preflight-output.md). The probe was read-only and exited `0`.

## Result

`V2-READY` for the current read-only Codex repo-self lane: static validation passed, the validator-owned single strict-config execution returned `CONFIG_OK`, and the current host exposes all six required collaboration tools. This is not a Claude-host readiness result, a whole generated-package PASS, or authorization for protected-path or user-scope configuration writes.

Static/strict failure overrides live-tool readiness; live readiness does not prove a session has reloaded persisted project settings.

## Evidence Lanes

| Lane | Result | Current evidence |
|---|---|---|
| Codex static runtime surface | PASS | `R0`, `STAMP`, `CANONICAL_AUTHORITY`, `MAPPING_STATE`, and `R1`, `R3`–`R12` passed. The validator resolved 13 registry paths from `.codex/`, checked 13 TOMLs, found 12 byte-identical runtime skill mirrors, and found no stale active vocabulary. |
| Strict project config | PASS | The one validator-owned `R2` execution returned `CONFIG_OK`; the preflight reused it as `P1`. No second strict-config execution was run. |
| Live collaboration tools | `v2-ready` | Current host supplied `spawn_agent`, `send_message`, `followup_task`, `wait_agent`, `interrupt_agent`, and `list_agents`. This task's coordinator family used spawn/send/followup/list/wait; `interrupt_agent` was catalog-confirmed and intentionally not invoked because no work was invalidated or unsafe. |
| Live host posture | OBSERVED | `codex-cli 0.154.0`; `multi_agent` and `multi_agent_v2` are stable/true. `codex doctor` reported restricted filesystem/network and `OnRequest`, loading `~/.codex/config.toml`. |
| Protected metadata | NOT PROBED | `R7` confirms static scope includes `.codex/` and `.agents/`; no live write probe was performed. |

The static source is Claude-canonical (`CANONICAL_AUTHORITY=claude`) with complete mapping. No Claude host was probed; no Claude readiness is claimed. Native affected-file verification is separately owned by the [phase-5 artifact review](../../.worklog/202609/codex-platform-boundaries/phase-5-review/artifact-review.md); the [phase-3 mixed provider-free regression record](../../.worklog/202609/codex-platform-boundaries/phase-3-generation/runtime-verification.txt) is separate evidence. Neither is a Codex preflight lane or a whole generated-package PASS. The retained full-root generated-package result remains diagnostic (`36 PASS`, `4 FAIL`, `2 SKIP`), not this repo-self acceptance route.

## Persisted Configuration vs. Running Session

`.codex/config.toml` persistently declares the approved repo-self profile: `gpt-6-astra`/`xhigh` root, `gpt-5.6-terra`/`high` subagent defaults, explicit per-role pins, `approval_policy = "on-request"`, `sandbox_mode = "workspace-write"`, and enabled multi-agent v2. The strict command checked the project surface with `-C /Users/wow/wrk/sp/A-Team`; the doctor output separately identifies the user-scoped base config it loaded.

Neither declaration proves that an already-running session reloaded its registry/model, nor does the read-only strict subprocess prove this session's effective write policy. The current execution environment is distinct from persisted settings. Project configuration cannot authorize rewriting its own protected metadata or any user-scope configuration.

## Setup

For a new or reloaded Codex session rooted at this repository, retain the project-local configuration and confirm the host supplies the declared v2 collaboration surface. Do not edit `~/.codex/config.toml` for baseline setup. Any future runtime change needs its own authorized scope and effective host permission; canonical/projection changes remain sequential and mapped.

## Verify

After a Codex upgrade or frozen runtime-surface change, run:

```sh
scripts/preflight-codex-runtime.sh --repo-self --live-tools 'spawn_agent,send_message,followup_task,wait_agent,interrupt_agent,list_agents'
```

This command runs the validator and reuses its one strict result. Do not add a second strict/model smoke probe. Native affected-file verification and mixed provider-free regressions remain separately owned evidence, not results established by this Codex probe.

## Scoped Rollback and Limits

- This probe changed no runtime configuration, user configuration, permissions, or protected metadata, so there is no configuration rollback.
- To reverse this label-only correction, restore `.worklog/202609/codex-platform-boundaries/phase-3.5-preflight/preimages/advisory-label-correction/.codex/docs/RUNTIME-SETUP.md`. To revert the entire preflight advisory, restore the prior `.worklog/202609/codex-platform-boundaries/phase-3.5-preflight/preimages/preflight/.codex/docs/RUNTIME-SETUP.md`; hash evidence is in this phase's `freeze-hashes.md`. Preserve concurrent and pre-existing dirty work.
- A future protected-path mutation remains subject to its authorized scope and live host permission. This advisory supplies no added write authorization.
