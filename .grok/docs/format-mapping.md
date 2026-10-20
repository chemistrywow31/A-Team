# Grok-native authority and source mapping

## Declaration

This branch explicitly migrates A-Team's active canonical authority to **root `AGENTS.md` plus `.grok/`**. Its sole runnable platform is Grok. The original Claude/Codex source is preserved at `reference/platform-sources/` as reference and conversion data. The main branch's authority is unchanged.

[`format-mapping.json`](format-mapping.json) is the machine-readable v1 inventory. It identifies role, skill, policy and supporting-file mappings; each target occurs once. Mapped sources plus explicitly source-only items account for every snapshot entry. The manifest's digest binds the mapping to the exact archive. File presence alone never grants runtime or canonical status.

## Provenance

- Baseline commit: `1bec32fb6c120aaa22d79af7d466363331cefa34`.
- Snapshot: [`snapshot.manifest.json`](../../reference/platform-sources/snapshot.manifest.json), with all 201 original paths, archive paths, SHA-256 hashes and Git executable modes.
- Shared design input: archived `.claude/` and `CLAUDE.md`.
- Bounded runtime comparison input: archived Codex projections and their mapping/audit.
- Native input: installed Grok 1.0.62, official source revision `2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8`; effective-runtime evidence is distinct from source and discovery evidence.

Archive paths in JSON are relative to the delivery root. In this document, `reference/platform-sources/` also denotes that root-relative directory. The snapshot is immutable provenance, not an active dependency to be loaded as instructions. Do not start Grok with its working directory inside it.

## Families

| Original source family | Native target | Treatment |
| --- | --- | --- |
| 13 nested `.claude/agents/` roles | 13 flat `.grok/agents/*.md` | Preserve responsibilities, task contracts, authority and review duties; use native metadata and lifecycle |
| 11 canonical skills | `.grok/skills/*/SKILL.md` and maintained assets | Native loading and instructions; self-contained skill helpers |
| 19 shared rules | `.grok/policies/*.md` | Full contracts, role-specific on-demand loading |
| Automatically loaded shared bootstrap | `.grok/rules/core.md` | Small native entry pointing to complete policies |
| Root entries | `AGENTS.md` | Explicit Grok authority and main-session coordinator |
| Shared judgment and dispatch templates | `JUDGMENT.md`, `templates/`, `.grok/templates/` | Preserve decision quality with native dispatch semantics |
| Validation and preflight | `scripts/`, `tests/`, `requirements.txt` | Real parsers and Grok-specific checks; discovery/effective behavior separated |
| Historical audit records | `AUDIT.md`, `VERIFICATION.md` with branch pointers | Preserve original bodies; do not reuse historical PASS as Grok evidence |
| README | `readme.md` | Current introduction to customizing an AI team; the original README remains in the immutable source snapshot |

The exact role/skill inventories and every policy rename are in the JSON; `.grok/agents/team-architect.md` supplies the 12-specialist routing roster. A generated team's `kind: generated-team` mapping uses its own accepted roster, not A-Team's 13/11/19 counts.

## Deliberate native differences

The coordinator keeps Grok's full default toolset. Role routing is prompt policy; specialist `disallowedTools: [Task]` is a source-backed native directive with effective execution checked separately. Model and effort pins are omitted rather than translated between providers. Model inheritance is source-backed; exact effort behavior remains an installed-session observation.

The old platform registries, configuration, hooks and output-style activation remain source-only. Their engine-specific behavior is not copied into Grok schema. The original output-style file, license-bearing assets and historical prompt references remain in the exact snapshot. Maintained skill assets and their licenses remain available natively where applicable.

The original skill-creator's Claude command/event assumptions are adapted to the documented Grok headless interface; fixture tests and an actual model evaluation are separate evidence levels. Native helper limitations belong in runtime setup and the helper's own instructions.

Root `CLAUDE.md`, `.claude/`, `.codex/`, `.agents/` and `agents/` are removed from the active project after snapshot verification. Grok can load foreign compatibility surfaces, and project compatibility settings cannot be used to suppress all root instruction filenames. User/global extensions are outside this branch's authority and are inventoried separately during preflight.

## Validation and future maintenance

Run the commands in [`GROK.md`](../../GROK.md). The validator checks path confinement, uniqueness, complete source coverage, snapshot hashes/modes and active inventories. It does not infer effective models, permissions or tool exposure from mappings.

Edit the native canonical family for later Grok changes, then update only its affected mappings and evidence. A main-branch sync is an explicit comparison against the pinned snapshot, not a blind directory copy. Retained foreign source does not authorize foreign runtime activation or a second canonical authority.

For a generated target, first read its own declaration and mappings. A Grok-native target declares authority in `AGENTS.md`; conversion-retained targets record native/reference-only status in `.grok/docs/format-mapping.json`. Single-platform targets without retained conversion sources do not need this repository's 201-file snapshot.

## Rollback

Before changing a family, record its current bytes and exact owned paths. To undo this migration, restore only that family's archived original paths and remove only its known task-created native files. Preserve later unrelated edits and compare conflicts before restoration. Do not reset or clean an entire repository, and do not change main as part of branch rollback.

Restoring archived platform trees restores the baseline files, not a claim that an already-running host has reloaded its registry. Start the appropriate client after choosing one consistent restored authority.
