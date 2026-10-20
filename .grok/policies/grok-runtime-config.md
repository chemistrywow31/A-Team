---
name: Grok Runtime Configuration
description: Keep project TOML minimal, permission changes scoped, and setup evidence separate from effective runtime claims
---

# Grok Runtime Configuration

## Applicability

- Applies to coordinators, runtime/agent writers, validators, and preflight reviewers.

## Rule Content

### Generate Only Supported Project Sections

Every runnable native team ships `.grok/config.toml`. For the observed target, project configuration contributes only `[mcp_servers]`, `[plugins]`, and `[permission]`. A minimal file may contain comments plus an empty permission rule list; absent optional integrations do not need placeholder services.

```toml
# Keep host permission defaults; no project permission overrides are required.
[permission]
rules = []
```

Do not emit project model, effort, compatibility, sandbox, subagent, UI, or hook settings as if they take effect. Put tested agent overrides in agent metadata and user-applied setup in `docs/RUNTIME-SETUP.md`. Project config appearing in inspect's source layers does not prove unsupported keys became effective.

### Preserve Permission And Trust Boundaries

Project permission rules activate only after folder trust. Inspect the actual target state and inherited constraints; do not automatically grant trust, disable approvals, expand permissions, or change user/global configuration to make a check pass. A real worktree trust decision can be shared with the repository's other worktrees; it is not a branch-local permission workaround.

Add an exact permission pattern only when the team's actual workflow needs it and the installed parser/evaluator supports its shape. Classify the operation's impact before choosing a rule:

- Routine project-scoped reversible reads/edits/local checks should keep ordinary operation usable; avoid repetitive new prompts without an evidenced reason.
- Externally visible or hard-to-reverse writes require existing authorization for that operation and target; preserve live approval requirements.
- Destructive cleanup, force rewrites, secret exposure, and arbitrary interpreter/shell execution must not receive broad allow rules.

Never copy another runtime's permission grammar. Validate native allow/deny patterns and actual precedence before relying on them. Do not add a guessed ask/allow/deny table or broad runner wildcard merely because the source design had one. A task's frequent safe operation can receive a narrow justified pattern; frequency alone does not authorize destructive/external work.

### Declare Actual Dependencies

Add MCP servers/plugins only for confirmed workflow needs and supported configuration. Keep credentials out of committed files and reports; preserve existing external connection and trust controls. Name local runtime/interpreter dependencies with portable setup and version requirements; do not install globally without authorization.

Settings are mutable operational inputs. Do not impose whole-tree integrity locks on routine config edits, package copy/start, intentional stop/restart, updates, or recovery without the proportional-design evidence.

### Portable Verification And Readiness

1. Resolve the supplied target root independently of caller cwd; parse TOML using a real parser and enforce allowed sections/types.
2. Record client version, configuration sources, project root/trust, and expected native source paths through read-only `grok inspect --json`.
3. Treat untrusted instructions/skills as activation-gated, missing binary as unavailable, and unknown/missing metadata as failure of the corresponding check. Do not silently drop profiles or let exit zero stand for inventory completeness.
4. Separate static validity, discovery, and effective-session checks. Record model access, role selection, tool exposure/Task denial, shell execution, context, and effort only when actually exercised.
5. Default preflight must not trigger costly model tasks, change real trust, copy credentials, or alter global settings. A bounded runtime smoke needs existing access and authorization. Missing access remains PENDING_NATIVE_AUTH/UNVERIFIED.
6. Write `docs/RUNTIME-SETUP.md` with probe date/version, setup/activation requirements, verification, current limits, and scoped rollback. Repo-self uses `.grok/docs/RUNTIME-SETUP.md`.

Disposable trusted loader fixtures may isolate state through a fresh process-local `GROK_HOME` only within their explicit authorization. Never point that temporary state at live user credentials or overwrite HOME. Such discovery evidence does not prove effective authenticated execution.

## Violation Determination

- Runnable target omits native config or emits unsupported project sections as controls -> Violation.
- Configuration parsing/listing is called effective permissions/model/tool proof -> Violation.
- Preflight depends on caller cwd, grants real trust, copies auth, changes global settings, or runs unrequested paid inference -> Violation.
- Broad destructive/arbitrary-execution grants, secret-bearing config, or invented permission grammar -> Violation.
- Setup omits activation gaps, verify/rollback steps, or effective-runtime limits -> Violation.

## Exceptions

A sub-team explicitly running inside a parent project may inherit its native configuration if its root declaration names that source and setup documents the effective boundaries. This does not authorize a new global setting or permit unsupported project fields.

Tradeoff: Explicit config can conflict with inherited settings. Keep it minimal, inspect effective sources, and prefer a documented setup requirement over speculative project overrides.
