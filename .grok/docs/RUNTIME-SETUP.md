# Grok runtime setup

Probe date: 2026-10-20. This advisory applies to the Grok-native A-Team
repository itself, whose active authority is root `AGENTS.md` plus `.grok/`.

## Current readiness

Static validation is **PASS**: the repo-self contract found 13 flat roles, 11
native skills, the core rule, configuration, mapping, and source snapshot.
Installed discovery is **PASS in two controlled fixtures** after fixture-only
trust: one plain Git root with a `.git` directory and one linked worktree with
a `.git` file. The installed client was `grok 1.0.62 (1474f9cbdd91)` and
resolved the expected project role/skill paths, root instructions, and core
rule in both forms. The archived platform sources were not loaded as project
instructions.

The research source revision was `2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8`;
it differs from the installed build. Static parsing and `inspect` are not a
model-session test. The real project’s normal-profile trust was not assessed.

`model_access` is **NOT_PROBED**. Effective tools, specialist Task denial,
role selection, fresh reviewer context, model routing, and effective effort are
**UNVERIFIED / PENDING_NATIVE_AUTH**. No model was invoked. Authentication was
not read, copied, or inferred from a normal browser login; an isolated home
cannot assume that normal-login state is available.

The client also reported ambient user/plugin sources, hooks, and permission
sources. They are separate from the verified project inventory and need local
operator review before relying on an ordinary user profile.

## Setup and verification

1. Use a local Python 3.11+ environment with the repository requirements; do
   not install dependencies globally.
2. From the repository root, run combined validation and discovery with an
   explicit Python 3.11+ interpreter, for example:
   `PYTHON=.venv/bin/python bash scripts/preflight-grok-runtime.sh . --repo-self --json`.
   It must report `STATIC_VALID`, `UNTRUSTED_PROJECT`, or `DISCOVERY_READY` as
   appropriate; only the last is trusted discovery readiness.
3. Inspect the actual project with `grok inspect --json`. Confirm the project
   root, the 13 expected flat `.grok/agents` paths, 11 skill paths, root
   `AGENTS.md`, and `.grok/rules/core.md`. Treat ambient entries separately.
4. If the operator elects to trust the real project, perform that host-side
   action through the installed client after reviewing its trust scope. Project
   files cannot grant their own trust. Re-run the plain inspect and preflight.
5. Use an already-authorized authenticated session and the agreed model/budget
   for any bounded smoke. Resolve a material missing access or choice first.
   Do not copy credentials or bridge a normal-home browser login into a
   disposable runtime home.

## Rollback and evidence

No repository setting can revoke host trust. For a fixture, remove its
disposable worktree and process-local Grok home. For a real project, use the
installed client’s documented trust-removal procedure or the applicable managed
setting, then re-run the untrusted inspection. Do not change global settings or
credentials as a workaround.

Full command output and both fixture inventories are retained under
`.worklog/202610/grok-native-branch/phase-3-validation/runtime_preflight/`.
