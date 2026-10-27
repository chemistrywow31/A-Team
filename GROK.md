# A-Team for Grok Build

This branch runs A-Team as a Grok-native team designer. Its canonical instructions are `AGENTS.md` and `.grok/`. It designs teams under `teams/{team-name}/`; A-Team's own 13 roles are the designer, not a mandatory roster for every generated team.

The main branch retains its Claude/Codex design. This branch explicitly migrates its active authority to Grok and preserves all 201 baseline source files, byte for byte and with their executable modes, under [`reference/platform-sources/`](reference/platform-sources/SNAPSHOT.md). That snapshot is conversion and provenance data. Start Grok from this branch's root, never from the snapshot.

## Start

With Grok Build installed and authenticated through your normal setup:

```sh
cd /path/to/A-Team
grok --cwd "$PWD" --agent team-architect
```

Alternatively, start a normal Grok session in this root and ask it to use the `a-team` skill. The current main session adopts `.grok/agents/team-architect.md`; it must not spawn a second coordinator.

Grok reads root `AGENTS.md` and the flat `.grok/rules/` files. **This `GROK.md` is an operation guide, not an automatically loaded instruction file.** Roles are flat `.grok/agents/*.md`; skills live at `.grok/skills/<name>/SKILL.md`. Full policies live in `.grok/policies/` and are read by the relevant role or task.

See [runtime setup](.grok/docs/RUNTIME-SETUP.md) for dated validation and any remaining activation requirements. Folder trust belongs to the user. The tools here never grant it automatically. A Git worktree's trust can be shared with sibling worktrees of the same repository.

## Validate

Use Python 3.11 or later and the declared dependencies in a local environment:

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
.venv/bin/python scripts/validate_grok_team.py . --repo-self
PYTHON="$PWD/.venv/bin/python" bash scripts/preflight-grok-runtime.sh . --repo-self --json
```

Choose an installed Python 3.11+ executable if `python3.11` is not its name. No global package installation is required. The preflight accepts an explicit target root from any caller directory and `--grok-bin /path/to/grok`; `PYTHON` selects its interpreter.

For a generated team, omit `--repo-self`:

```sh
.venv/bin/python scripts/render_helper_briefs.py teams/example
.venv/bin/python scripts/render_helper_briefs.py teams/example --write-schema-copy
.venv/bin/python scripts/validate_grok_team.py teams/example
.venv/bin/python scripts/validate_grok_team.py teams/example --classify --json
.venv/bin/python scripts/validate_grok_team.py --board .worklog/task-board.json
```

`render_helper_briefs.py` rewrites `briefs/` from the six portable sections in each agent file. `--board` checks one task-board file. Ordinary team validation does not read gitignored `.worklog/`.

`--baseline /path/to/baseline` compares a target with an earlier copy to identify text-only versus structural changes. The comparison is routing evidence, not an independent design approval.

The checks have separate meanings:

| Check | What it establishes |
| --- | --- |
| Strict local validation | YAML/TOML, authoring fields, unique roles, references, authority, mapping and snapshot integrity |
| `grok inspect --json` | Discovered names, source paths and project trust; untrusted agent listings alone do not establish activation |
| Bounded model-session trace | Actual role selection, tool exposure, delegation and context behavior, model/effort where observable |

The default preflight only validates and inspects. It never calls a model, copies credentials, changes approval defaults, or grants trust. `model_access: NOT_PROBED` and effective-runtime `UNVERIFIED` are deliberate results, not authentication failure claims. A discovery PASS cannot be used as a model-session PASS.

## Native design

- The main coordinator retains Grok's native tools by omitting an allowlist. Its 12-role routing boundary is prompt policy.
- Specialists use `disallowedTools: [Task]`, the source-backed directive removing child delegation tools. Installed effective enforcement still needs session evidence.
- Roles omit model and effort pins. Source supports parent-model inheritance; effort omission retains the installed session/default behavior. No cross-provider quality equivalence is assumed.
- The coordinator uses only the lifecycle exposed by the running client. Default model-facing names include `spawn_subagent` and `get_command_or_subagent_output`. Use `subagent_type` only when the live schema advertises it, and `background`, not the internal `run_in_background`.
- Project `.grok/config.toml` contributes only the supported permission, MCP and plugin sections. It cannot set the project's model, effort or compatibility defaults.
- One short automatic rule points to 20 full policies. The role's explicit startup references preserve detailed contracts without automatically loading every policy for every task.
- Skills are native instructions and assets. Their `allowed-tools`, `model` and `effort` metadata are not effective permission or routing controls.

## Generate and maintain teams

New-team discovery confirms objectives, scope, workflow, roles, output format, authority and the requirements summary. Planning, generation, independent review, runtime preflight and optional optimization follow. Generated teams receive their own suitable roster and native runtime setup.

Existing-team work first records its layout, runnable surfaces, authority and mappings. Text-only work preserves topology, runtime, ownership and authority. Structural work goes through a recommendation audit, exact writer ownership, independent artifact review, and preflight when runtime changes. A foreign or reference-only team is not made Grok-runnable merely because its files are present.

This branch's runnable output is Grok-native. Conversion from another format requires explicit target authority and scope, with complete source-to-target mappings where retention is requested. The preserved source snapshot supports that analysis; it does not make this branch a simultaneous Claude/Codex runtime.

## Source and version evidence

The initial adaptation used installed `grok 1.0.62 (1474f9cbdd91)` and official source revision `2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8`, observed on 2026-10-20. These are different revisions. Source-backed semantics and installed observations are recorded separately.

Official references: [project instructions](https://docs.x.ai/build/features/project-rules), [subagents](https://docs.x.ai/build/features/subagents), [skills](https://docs.x.ai/build/features/skills-plugins-marketplaces), [settings](https://docs.x.ai/build/settings/reference), and [pinned source](https://github.com/xai-org/grok-build/tree/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8). Future upgrades require checking the actual installed schema and behavior rather than copying this version's assumptions.

The [README](readme.md) introduces A-Team and the ways you can customize your team. The [format mapping](.grok/docs/format-mapping.md) describes authority, preserved sources, deliberate adaptations and rollback. `AUDIT.md`, `VERIFICATION.md` and `CHANGELOG.md` retain historical records; their earlier PASS statements are not Grok validation. The [baseline README](reference/platform-sources/readme.md) remains in the source snapshot.
