# Research Desk runtime setup

Recorded: 2026-10-27. This file describes the tracked example at `examples/research-desk/`. The example was written to the generator contract in this repository. It is not the output of an authenticated model session.

## Prerequisites and startup

1. Use the A-Team repository's Python 3.11+ environment and `requirements.txt`.
2. From the repository root, validate this example:

```sh
python3 scripts/validate_grok_team.py examples/research-desk
python3 scripts/render_helper_briefs.py examples/research-desk --check
```

3. To run it in Grok Build, start a session with this directory as the project root and adopt `.grok/agents/research-lead.md`, or use the `research-desk` skill. This setup guide does not claim that command was executed here.
4. To run it as a lead plus helpers, pass `briefs/<role>.md` and a task envelope to one direct specialist. The specialist returns one EC-1 result to the lead.

## Static proof and limits

Static validation on 2026-10-27, run as `python3 scripts/validate_grok_team.py examples/research-desk`, returned `STATIC_VALID`. The same command reported `effective_runtime=UNVERIFIED` and `model_access=NOT_PROBED`. It did not call a model. Re-run it after any edit. This guide does not copy that result forward as proof of a later tree.

`docs/task-board.example.json` and `docs/owner-report.example.md` are sample rows. They are not measurements. `cost` and `tokens` are null because no host reported them.

Installed discovery for this example: NOT_PROBED.
Effective tool exposure, Task denial, fresh context, role selection, and model or effort: UNVERIFIED.
Model access: NOT_PROBED. No model was called to produce or exercise this example.

## Verification and maintenance

A Grok client that supports `grok inspect --json` can list discovered project agents, skills, `AGENTS.md`, and `.grok/rules/core.md`. Inspect shows discovery only. It does not prove tools, permissions, or model behavior. Briefs under `briefs/` are assignments, not agent files, so an inspect listing of agents is not a listing of briefs.

Text that leaves roles, authority, and ownership unchanged can be reviewed as text. A change to roster, frontmatter, the brief sections, or the task-board schema is structural and needs the schema copy and the briefs regenerated together.

## Rollback

Restore the example files you changed. Do not reset the rest of the repository. Removing this directory removes the sample only. It does not change A-Team's generator.
