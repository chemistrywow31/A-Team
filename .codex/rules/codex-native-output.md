---
name: Codex Native Output
description: Keep generated teams authored in canonical Codex format and retain mapping for future format conversion
---

# Codex Native Output

## Applicability

- Applies to: `team-architect`, `requirements-analyst`, `skill-planner`, `rule-writer`, `skill-writer`, `agent-writer`

## Rule Content

### Confirm Delivery Format During Discovery

Before Planning, confirm:

- the requested delivery format: `codex-native`, `claude-compatible`, `dual-format`, or `let A-Team decide`
- the canonical authored format: always `codex-native`
- whether conversion-ready mapping must be retained for later Claude <-> Codex transformation

### Author The Canonical Package First

The source of truth for generated teams is the Codex package:

- `AGENTS.md`
- `.codex/`
- `.agents/skills/`

Write this package first even when the user signals future Claude compatibility needs. Do not treat `.claude/` as the authored output surface during normal generation.

### Retain Round-Trip Mapping

Every generated team must include `.codex/docs/format-mapping.md`.
Every generated team must include `.codex/docs/format-mapping.manifest.yaml`.

The human-readable mapping file must record:

- requested delivery format
- canonical authored format
- Codex -> Claude path mapping
- Claude -> Codex path mapping
- lossy or unsupported conversions
- round-trip preservation notes

The manifest must record:

- artifact ids
- source and target paths
- relation shape
- transform mode
- reverse strategy or canonical source
- validation and sidecar requirements for lossy conversions

### Protect Conversion Boundaries

- Keep stable file and directory names in the canonical Codex package whenever possible
- If a direct Claude equivalent does not exist, note the fallback or manual step in the mapping artifact
- Do not modify `.claude/` unless the user explicitly requests a conversion task

## Violation Determination

- Discovery output omits the requested delivery format or canonical authored format -> Violation
- Generation writes only Claude-format artifacts without the canonical Codex package -> Violation
- `.codex/docs/format-mapping.md` is missing or incomplete -> Violation
- `.codex/docs/format-mapping.manifest.yaml` is missing or incomplete -> Violation
- `.claude/` is modified during normal generation without explicit user approval -> Violation

## Exceptions

If the user explicitly asks for a format conversion task in the current run, generate or update the canonical Codex package first unless the user explicitly waives future round-trip support.
