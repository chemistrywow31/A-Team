# Runtime setup — A-Team repo-self

> Historical preflight stamp: `2026-10-06T07:28:33Z`; root: this repository; scope: frozen A-Team source-maintenance batch.
> This published advisory summarizes that preflight. It does not report a new runtime probe.

## Readiness by runtime

| Runtime | Static/source status | Live host status | Model/effective-session status |
|---|---|---|---|
| Codex | PASS for the frozen project config, registry, explicit role model/effort and sandbox pins, and mirrors. The corrected mapping validator had 41 passing tests and its non-strict repo-self classification passed. | `V2-READY` on the October 6 host: it exposed `spawn_agent`, `send_message`, `followup_task`, `wait_agent`, `interrupt_agent`, and `list_agents`, and reported seven total session slots including root. | Unverified for an already-running session. Root and default-subagent model/effort are intentionally host-selected; persisted role pins do not prove loaded routing. |
| Claude Code | PASS for native project artifacts: 13 agent frontmatters, settings JSON, hooks, entry skill, and direct-specialist Agent restriction. | No authenticated A-Team project session was verified. The CLI was available and `claude doctor` reported no installation issue; hooks and restrictions were not observed executing. | Unverified. Claude Code `2.1.290` reported no usable credential/policy fetch; no paid model call was run. |

On October 6, the Codex strict-config subprocess ran once before the validator-only mapping correction and returned `CONFIG_OK`. Its result remains applicable to the unchanged config; no second strict-config or model subprocess was run. The correction was covered by focused tests and dependent non-strict classification, not a second runtime invocation.

## Dated evidence summary

- October 6: Codex CLI `0.160.1`; static records `R0`–`R12`, the reused strict result `P1`, the six live collaboration tools, and the root-inclusive seven-slot observation above were recorded.
- October 6: native Claude artifact checks covered the CLI, settings, hooks, frontmatter, and declared direct-specialist mode; an authenticated session, credential/policy fetch, paid model call, effective routing, hook execution, and loaded restrictions remained unverified.
- October 20: publication integrity checking confirmed all 100 frozen source artifacts retained their sealed hashes, so the October 6 evidence remains reusable for this unchanged source batch.

Raw probe and hash records are local maintenance evidence and are not shipped with this repository. This dated summary is sufficient to interpret the advisory; it does not turn historical evidence into a current host test.

## Setup

Start a new or reloaded Codex session at the repository root and retain the checked-in `.codex/config.toml` and role TOMLs. Before relying on collaboration, confirm that the target host exposes its supported lifecycle tools. Project configuration does not authorize protected-metadata or user-scope writes.

For Claude Code, start a normal project session at the repository root so it loads `CLAUDE.md`, `.claude/settings.json`, project agents, and hooks. A-Team uses ordinary subagent mode, not Agent Teams. The main session adopts the coordinator; direct specialists have `disallowedTools: [Agent]`. This advisory requires no user or global configuration change.

## Verify after a runtime change

Run these commands from the repository root:

```sh
scripts/preflight-codex-runtime.sh --repo-self --live-tools 'spawn_agent,send_message,followup_task,wait_agent,interrupt_agent,list_agents'
claude agents --json --cwd .
claude doctor
```

The first command includes the validator and one strict-config execution; do not add another strict/model smoke call. The Claude commands establish CLI and active-session evidence only. Observe a real authenticated Claude project session before claiming effective model routing, hook execution, or loaded Agent restrictions.

## Scoped rollback

This preflight changed no runtime config, user configuration, permissions, or account settings. First save the current advisory file separately, including any staged and unstaged local edits. Then restore only this file from known prior revision `8508acf1e36227853f7924348a02133db414b991`:

```sh
git restore --source=8508acf1e36227853f7924348a02133db414b991 -- .codex/docs/RUNTIME-SETUP.md
```

Do not reset the worktree or overwrite concurrent changes.
