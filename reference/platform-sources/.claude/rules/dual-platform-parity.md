---
name: Dual-Platform Parity
description: Declare one canonical authority per team, classify existing surfaces before mutation, and regenerate every projection from that authority
paths:
  - "teams/**"
  - ".codex/**"
  - ".agents/**"
  - "agents/**"
  - "AGENTS.md"
---

# Dual-Platform Parity

## Applicability

- Applies to: `team-architect`, `team-restructuring-master`, `rule-writer`, `skill-writer`, `agent-writer`
- Trigger condition: any team with more than one documented surface, or any existing-team assessment that could change canonical or runtime files

## Rule Content

### M1 — Canonical Authority Is Explicit And Scoped

- A-Team root shared design authority is fixed: `.claude/` plus `CLAUDE.md` is canonical for role intent, workflow, ownership, authority, and quality contracts. Root Codex surfaces (`AGENTS.md`, `.codex/`, `.agents/skills/`, `agents/`) project that design with the bounded platform adaptation inputs below; those inputs do not create another shared authority.
- Every generated team must declare its own canonical authority in its team declaration and every runnable root entry. Required mapping artifacts must agree. Valid states are: Claude canonical, Codex canonical, or platform-neutral `shared/` canonical with Claude and/or Codex projections.
- A reference-only or activation-gated surface must be labeled as such. It is never promoted to canonical or runnable by implication.

An external target root is mutable only after this authority and confinement gate passes:

1. The user explicitly authorizes one exact real target root.
2. The declaration quorum names exactly one authority and its canonical roots: Claude authority uses `CLAUDE.md` as both team declaration and runnable entry; Codex authority uses `AGENTS.md`; platform-neutral authority uses `shared/team.yaml` with `canonical_authority.root: shared/`, a platform-neutral policy, and declared role, rule, and skill families. Every other runnable root entry must agree.
3. A multi-surface or conversion-retained team has `.codex/docs/format-mapping.manifest.yaml`; its authority, roots, surface states, and source/target mappings agree with the declaration and map every assigned canonical source to each assigned projection. Any human mapping must agree. An unmapped single-surface team does not require a manifest.
4. The dispatch names every exact owned path. Resolve the authorized root and each existing owned path to real paths; for a new path, resolve its nearest existing parent. Reject `..`, an absolute path outside the root, or any root, owned-path, or parent symlink escape.

Missing or conflicting declarations, dual-canonical claims, reference-only promotion, or incomplete required mappings require `NEEDS_CONTEXT` with no write. Directory presence is not authority evidence; any path escape fails closed.

### M2 — Existing Teams Are Classified Before Mutation

Before proposing or applying restructuring, record:

- runnable surfaces and activation state
- canonical authority and whether it is explicit, ambiguous, or drifted
- stamp state across entry docs
- mapping completeness
- whether the observed problem is a `Codex-only runtime gap` or a `cross-platform design gap`

Ambiguous canonical authority permits assessment only. Mutation waits until authority is confirmed.

### M3 — Changes Start At The Canonical Source

- `cross-platform design gap` changes must start at the target team's canonical source and regenerate only the affected projections.
- `Codex-only runtime gap` changes may touch Codex-only runtime artifacts directly only when the mapping inventory already classifies them as platform-only.
- For A-Team projections, the existing platform-only inputs `.codex/rules/codex-runtime-config.md`, `.codex/rules/codex-agent-config-patterns.md`, and `.codex/rules/context-isolation.md` may supply Codex runtime defaults, schema/metadata, and lifecycle details. Record each exact input, bounded scope, and exact mapped projection targets in `.codex/docs/claude-adaptation-manifest.toml` and the human adaptation audit before using it; retain canonical shared semantics and regenerate sequentially under the assigned family owner.
- An adaptation input is not a whole-tree exemption or permission to edit unrelated projections. Shared role, workflow, ownership, authority, or quality changes still start in `.claude/`; platform-specific payload need not be duplicated in active Claude instructions. Load Codex specifications only when the selected target includes Codex.
- Start at `.claude/**` or `CLAUDE.md` for Claude authority, `.codex/**` or `AGENTS.md` for Codex authority, and exact `shared/**` sources for platform-neutral authority. Regenerate only required manifest-mapped projections, sequentially under the same artifact-family owner.
- Rule Writer owns assigned canonical rules and mapped rule projections; Skill Writer owns assigned canonical skills and mapped skill projections or mirrors; Agent Writer owns assigned canonical team, role, root, mapping, and runtime-agent files plus their mapped projections.
- Family names define the maximum eligible surface, not blanket ownership. Every dispatch must enumerate exact mutable paths.
- Capture a scoped preimage and rollback plan before writing. Accept the family only after semantic parity, applicable skill-mirror identity, current mappings and stamps, validator results, and runtime preflight when active runtime artifacts changed are verified.
- Editing a non-canonical projection to carry a design change upstream is a violation.

### M4 — Stamps And Inventories Must Stay In Sync

- Every runnable surface entry document carries `Generated by A-Team on {yyyy-mm-dd}`.
- Dual-surface teams must keep the same stamp date across each regenerated runnable surface.
- Platform-only files in a non-canonical surface must appear in both the human mapping or adaptation audit and the machine-readable manifest for that team.
- A missing stamp, mismatched stamp, or un-inventoried projection file is drift.

### M5 — Generator Defects Backport To A-Team Canonical

When existing-team work uncovers a shared generator defect in A-Team itself, fix A-Team's canonical `.claude/` source and regenerate A-Team's Codex projection in the same maintenance task before closing the downstream change. A defect confined to an inventoried platform-only input follows M3 and regenerates only its declared affected projections.

## Violation Determination

- A generated team with multiple surfaces lacks a single explicit canonical declaration, or two surfaces both claim canonical authority -> Violation
- An external-root mutation lacks exact user authorization, a single consistent declaration quorum, required mappings, exact owned paths, resolved-path confinement, same-owner canonical-first order, verification, or rollback evidence -> Violation
- A restructuring recommendation or mutation is recorded without the pre-mutation classification fields from M2 -> Violation
- A shared design change touches only a non-canonical projection, or a Codex-only change bypasses its inventoried input/scope, exact mapped targets, or same-owner regeneration -> Violation
- An adaptation row exempts a mapped tree, adds a shared canonical authority, or carries shared role/workflow/ownership/authority/quality changes without their canonical source -> Violation
- Entry-doc stamps differ across runnable surfaces, or a platform-only file exists outside the team's mapping inventory -> Violation
- A known shared generator defect is patched only in a downstream projection while A-Team root `.claude/` remains stale -> Violation

## Exceptions

- Single-surface teams are out of scope for cross-surface stamp parity and platform-only inventories, but they still must declare their canonical authority.
- A team may intentionally ship a non-runnable reference surface. That surface may omit runtime artifacts when the mapping record marks it reference-only and no rule or README claims it is runnable.
