# Claude And Codex Format Mapping

## Goal

This repository keeps the original `.claude/` implementation as the legacy/source design and adds a Codex-native execution layer. Codex is the canonical authored format. Mapping is retained so future conversion can run in either direction without reverse-engineering the team layout.

## Mapping Principles

- Canonical authored format: Codex
- Legacy and compatibility format: Claude
- Discovery must confirm the user's requested delivery format before planning or generation
- Normal generation writes the Codex package first, then preserves mapping for later export or import work
- Do not rewrite `.claude/` during normal Codex generation unless the user explicitly requests a conversion task

## Mapping Table

| Canonical Codex Asset | Claude Counterpart | Direction | Notes |
| --- | --- | --- | --- |
| `AGENTS.md` | `CLAUDE.md` | Bidirectional | Root runtime contract; content must stay semantically aligned |
| `.codex/agents/` | `.claude/agents/` | Bidirectional | Authored playbooks for coordinator and specialists |
| `.codex/rules/` | `.claude/rules/` | Bidirectional | Hard constraints and process rules |
| `.codex/skills/` | `.claude/skills/` | Codex -> Claude | Authored skill definitions map to legacy skill bundles |
| `.agents/skills/` | `.claude/skills/` | Claude -> Codex runtime | Runtime-discoverable Codex skill copy mirrors authored or adapted skills |
| `.codex/docs/format-mapping.md` | N/A | Codex anchor | Per-team retained mapping artifact for round-trip conversion |
| Codex `spawn_agent`, `send_input`, `wait` | Claude `Task` / Agent Teams phrasing | Bidirectional concept mapping | Coordinator workflow terminology differs, intent stays aligned |

## Runtime Split

- `AGENTS.md`: the active project contract for Codex.
- `.codex/`: source-of-truth for prompts, rules, config, and skill definitions.
- `.agents/skills/`: runtime skill packages that Codex can discover automatically.
- `.claude/`: retained as legacy/source material and migration reference.

## Per-Team Mapping Artifact

Each generated team should retain `teams/{team-name}/.codex/docs/format-mapping.md`.
Each generated team should also retain `teams/{team-name}/.codex/docs/format-mapping.manifest.yaml`.

Required sections:

1. requested delivery format
2. canonical authored format
3. Codex -> Claude asset mapping
4. Claude -> Codex asset mapping
5. lossy conversions and exceptions
6. round-trip preservation notes

Required manifest fields:

- `spec_version`
- `supported_directions`
- `canonical_roots`
- `default_policies`
- `artifacts`

Each artifact entry should define:

- `id`
- `kind`
- `source`
- `targets`
- `relation`
- `transform_mode`
- `reverse_from` or `canonical`
- `field_map` and `section_map` when structure changes
- `validation`
- `lossy`
- `sidecar` when lossy or bundle-based

Recommended table shape:

| Canonical path | Claude path | Direction | Status | Notes |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | `CLAUDE.md` | bidirectional | direct | root contract |
| `.codex/agents/coordinator.md` | `.claude/agents/coordinator.md` | bidirectional | adapted | terminology changes only |
| `.agents/skills/research/SKILL.md` | `.claude/skills/research/SKILL.md` | codex-to-claude | adapted | runtime copy maps to legacy bundle |

Status values:

- `direct`: one-to-one conversion is expected
- `adapted`: semantic mapping exists but structure differs
- `lossy`: some structure or metadata cannot round-trip cleanly
- `manual`: human review is required

Recommended manifest shape:

```yaml
spec_version: 1
supported_directions:
  - claude_to_codex
  - codex_to_claude
canonical_roots:
  codex_authored:
    - ".codex"
  codex_runtime:
    - ".agents"
  claude:
    - ".claude"
default_policies:
  ambiguity: fail
  lossy_transform: require_sidecar
artifacts:
  - id: root-project-doc
    kind: project_doc
    source:
      runtime: codex
      path: "AGENTS.md"
    targets:
      - runtime: claude
        path: "CLAUDE.md"
        canonical: false
    relation: "1:1"
    transform_mode: rewrite
    reverse_from: "AGENTS.md"
    lossy: false
```

Use sidecars only for lossy or bundle-style transforms such as frontmatter remapping or bridge skills.

## Generated Team Structure

```text
teams/{team-name}/
├── AGENTS.md
├── .codex/
│   ├── config.toml
│   ├── docs/
│   │   ├── format-mapping.md
│   │   └── format-mapping.manifest.yaml
│   ├── agents/
│   ├── rules/
│   └── skills/
└── .agents/
    └── skills/
```

## Special Cases

- `skill-creator` is bridged into Codex as a lightweight wrapper. Prefer the globally available Codex/system skill when present. The original large implementation remains under `.claude/skills/skill-creator/`.
- `.codex/skills/` is the maintenance copy. `.agents/skills/` is the runtime copy. Keep them in sync.

## Conversion Use Cases

- Claude -> Codex: import legacy team assets into the canonical Codex layout, then regenerate `.agents/skills/` as the runtime mirror.
- Codex -> Claude: export from the canonical Codex layout using the retained mapping artifact instead of inferring structure from prompts.
- Dual-format delivery: treat Codex as the source package and produce Claude-compatible output as a follow-up conversion step.
