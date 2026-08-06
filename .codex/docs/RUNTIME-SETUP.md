# Codex Runtime Setup — A-Team repo-self

> Probed: `codex-cli 0.146.0` on Darwin at 2026-08-05.
> Re-run `scripts/preflight-codex-runtime.sh --repo-self` after any Codex upgrade or runtime-config change.

## What Was Probed

| Item | Value |
|---|---|
| Target | `/Users/wow/wrk/sp/A-Team` |
| Codex | `codex-cli 0.146.0` |
| Doctor sandbox line | ✓ sandbox      restricted fs + restricted network · approval OnRequest |
| Doctor config line | config.toml              ~/.codex/config.toml |
| Feature rows | multi_agent                          stable             true;multi_agent_mode                     removed            false;multi_agent_v2                       stable             true |
| Static validator | `python3 -B /Users/wow/wrk/sp/A-Team/scripts/validate_codex_team.py --repo-self` |
| Strict config command | `codex exec --strict-config --sandbox read-only --skip-git-repo-check --ephemeral 'Reply with CONFIG_OK only.'` |

## Static Validation

```text
R0 repo-self-target | PASS | .
STAMP repo-self-stamp | PASS | repo@AGENTS.md=2026-08-05
CANONICAL_AUTHORITY repo-self-canonical-authority | PASS | claude | .codex/docs/claude-to-codex-mapping.md:5, .codex/docs/claude-to-codex-mapping.md:105, AGENTS.md:9, AGENTS.md:35
MAPPING_STATE repo-self-mapping-state | PASS | complete | .codex/docs/claude-to-codex-mapping.md, .codex/docs/claude-adaptation-audit.md
R1 version-features | PASS | codex-cli 0.146.0; multi_agent                          stable             true; multi_agent_mode                     removed            false; multi_agent_v2                       stable             true
R2 strict-config | PASS | CONFIG_OK
R3 config-toml-parses | PASS | .codex/config.toml
R4 registry-resolution | PASS | 13 config_file paths resolve from .codex/
R5 agent-toml-required-keys | PASS | checked 13 agent TOMLs
R6 v2-feature-and-legacy-keys | PASS | v2 feature block present and current
R9 skill-mirror-parity | PASS | byte-identical trees; 12 files
R10 m5-manifest-audit-parity | PASS | manifest/audit agree; 12 platform-only and 8 deliberately-not-copied paths
R11 active-runtime-vocabulary | PASS | scanned 14 active TOMLs and 13 mapped playbooks; no stale fields or tool vocabulary
R7 protected-path-expectation | PASS | static scope includes .codex/ and .agents/; live writeability must be confirmed separately by runtime preflight
R8 host-tool-readiness | PASS | all required collaboration tools present
```

## Strict Config

```text
P1 strict-config | PASS | command exit 0
```
- Note: `codex doctor` reports the user-scoped base config it loaded; the strict-config command above is the project-surface check.

## Live Host Tool Readiness

- Class: `v2-ready`
- Evidence: all required collaboration tools supplied: spawn_agent,send_message,followup_task,wait_agent,interrupt_agent,list_agents
- Required v2 collaboration tools: `spawn_agent`, `send_message`, `followup_task`, `wait_agent`, `interrupt_agent`, `list_agents`

## Overall Preflight Result

- Result: `V2-READY (static=PASS; strict-config=PASS; host-tools=v2-ready)`
- Rule: host-tool readiness cannot override static target or strict-config failures.

## Protected-Path Posture

- Static scope only: this preflight records whether the target owns runtime metadata under `.codex/` or `.agents/`; it does not perform a write probe.
- Consequence: keep live host-tool readiness separate from the static validator output. Do not claim autonomous protected-metadata rewrites from config text alone.

## Setup

```sh
codex --version
codex features list | rg '^multi_agent'
codex exec --strict-config --sandbox read-only --skip-git-repo-check --ephemeral 'Reply with CONFIG_OK only.'
```

## Verify

```sh
python3 -B /Users/wow/wrk/sp/A-Team/scripts/validate_codex_team.py --repo-self
codex exec --strict-config --sandbox read-only --skip-git-repo-check --ephemeral 'Reply with CONFIG_OK only.'
```

## Rollback

- This probe is read-only, so it has no config rollback step.
- If you changed repo or team runtime files before re-running validation, restore those files from version control or an untouched generated copy.
- Never use this lane to edit `~/.codex/config.toml`.
