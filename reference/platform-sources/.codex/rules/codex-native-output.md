---
name: Codex Native Output
description: Keep A-Team root Codex surfaces as projections and require each generated team to declare its own canonical authority
---

# Codex Native Output

## Applicability

- Applies to: `team-architect`, `requirements-analyst`, `skill-planner`, `rule-writer`, `skill-writer`, `agent-writer`

## Rule Content

### Separate A-Team Root Authority From Generated-Team Authority

- A-Team root repository authority remains `.claude/`. Root Codex surfaces in this repo are regenerated projections.
- Generated teams do not inherit that authority automatically. Discovery must decide whether a generated team is Codex canonical, Claude canonical, or dual-surface with one canonical source.

### Confirm Delivery Format During Discovery

Before Planning, confirm:

- the requested delivery format: `codex-native`, `claude-compatible`, `dual-format`, or `let A-Team decide`
- the generated team's canonical authority
- whether conversion-ready mapping must be retained for later Claude <-> Codex transformation

### Author The Chosen Canonical Surface First

- If the generated team is Codex canonical, author `AGENTS.md`, `.codex/`, `agents/`, and `.agents/skills/` first.
- If the generated team is Claude canonical, author `CLAUDE.md` and `.claude/` first, then regenerate any requested Codex projection.
- A dual-surface team still has one canonical source. Never let both surfaces diverge as peers.

### Retain Mapping When More Than One Surface Exists

Every generated team with more than one surface, or with explicit future conversion retention, must include:

- `.codex/docs/format-mapping.md`
- `.codex/docs/format-mapping.manifest.yaml`

Those artifacts must record:

- requested delivery format
- canonical authority
- runnable vs reference-only or activation-gated state
- Codex <-> Claude path mapping
- platform-only files
- lossy or manual steps
- reverse strategy or canonical source
- selected Codex runtime profile, installed-client evidence, and live readiness limits under `.codex/rules/codex-runtime-config.md`; distinguish documented CLI and observed-host lifecycle/capacity

### Protect Projection Boundaries

- Non-canonical surfaces are regenerated, not hand-edited.
- A reference-only surface stays reference-only until the user approves activation and the mapping artifacts are updated.
- If a direct counterpart does not exist, record the fallback or manual step in the mapping artifacts.

## Violation Determination

- Discovery omits requested format, canonical authority, or mapping-retention need -> Violation
- A generated team surface is written first even though another surface was declared canonical -> Violation
- A multi-surface or conversion-retained team omits `.codex/docs/format-mapping.md` or `.codex/docs/format-mapping.manifest.yaml` -> Violation
- Mapping artifacts omit canonical authority, surface state, platform-only files, or the selected Codex runtime profile/evidence -> Violation
- A non-canonical surface is hand-edited as if it were canonical -> Violation

## Exceptions

- A true single-surface team may omit mapping artifacts unless the user explicitly requests future conversion support.
