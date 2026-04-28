# Claude And Codex Format Mapping

## Goal

This repository keeps the original `.claude/` implementation as the legacy/source design and adds a Codex-native execution layer. Codex is the canonical authored format. Mapping is retained so future conversion can run in either direction without reverse-engineering the team layout.

## Mapping Principles

- Canonical authored format: Codex
- Legacy and compatibility format: Claude
- Discovery must confirm the user's requested delivery format before planning or generation
- Normal generation writes the Codex package first, then preserves mapping for later export or import work
- Do not rewrite `.claude/` during normal Codex generation unless the user explicitly requests a conversion task
- Generated Codex agents use project-level registration in `.codex/config.toml` plus per-agent TOML files under `agents/`
- Inside `.codex/config.toml`, every `config_file` is resolved relative to `.codex/`. For team-local runtime agent configs stored under project-root `agents/`, generated entries therefore use `../agents/...`.

## Mapping Table

| Canonical Codex Asset | Claude Counterpart | Direction | Notes |
| --- | --- | --- | --- |
| `AGENTS.md` | `CLAUDE.md` | Bidirectional | Root runtime contract; content must stay semantically aligned |
| `agents/` | `.claude/agents/` | Bidirectional | Codex stores per-agent TOML configs; Claude stores per-agent Markdown prompts |
| `.codex/config.toml` | N/A | Codex anchor | Project-level runtime registration, feature flags, and agent registry metadata |
| `.codex/rules/` | `.claude/rules/` | Bidirectional | Hard constraints and process rules |
| `.codex/skills/` | `.claude/skills/` | Codex -> Claude | Authored skill definitions map to legacy skill bundles |
| `.agents/skills/` | `.claude/skills/` | Claude -> Codex runtime | Runtime-discoverable Codex skill copy mirrors authored or adapted skills |
| `.codex/docs/format-mapping.md` | N/A | Codex anchor | Per-team retained mapping artifact for round-trip conversion |
| Codex `spawn_agent`, `send_input`, `wait` | Claude `Task` / Agent Teams phrasing | Bidirectional concept mapping | Coordinator workflow terminology differs, intent stays aligned |

## Agent Transform Rules

### Codex -> Claude

Convert each Codex agent from two inputs:

1. the registry entry in `.codex/config.toml`
2. the referenced agent TOML file after resolving `config_file` relative to `.codex/config.toml` (normally `../agents/**/*.toml`)

Deterministic path rule:

- `agents/{path}.toml` -> `.claude/agents/{path}.md`

Deterministic field mapping:

| Codex source | Claude target | Mode | Notes |
| --- | --- | --- | --- |
| `[agents.<id>]` table name | output file identity | adapted | use the id for stable conversion bookkeeping |
| `[agents.<id>].description` | summary line or frontmatter description | adapted | keep wording stable when possible |
| `config_file` | target file path | adapted | resolve it relative to `.codex/config.toml`, then convert the resulting `.toml` path to `.md` |
| `developer_instructions` | markdown body | direct | preserve headings and lists verbatim when possible |
| `model` | sidecar metadata | sidecar | Claude agent markdown has no direct equivalent |
| `model_reasoning_effort` | sidecar metadata | sidecar | retain only when round-trip preservation matters |
| `sandbox_mode` | sidecar metadata | sidecar | retain only when round-trip preservation matters |

Section handling:

- `developer_instructions` already contains the role contract, so it becomes the main body of the Claude agent file
- runtime-only TOML keys that Claude cannot express must be retained in a sidecar when round-trip fidelity is required
- Codex-native research agents such as `agents/research/domain-researcher.toml` and `agents/research/decision-auditor.toml` map to `.claude/agents/research/*.md` when exporting to Claude
- `name` and `description` in TOML are runtime metadata in Codex and map to Claude frontmatter or heading metadata during export

### Claude -> Codex

Convert each Claude agent markdown file into:

1. one `agents/**/*.toml` file
2. one `[agents.<id>]` registration in `.codex/config.toml`

Deterministic path rule:

- `.claude/agents/{path}.md` -> `agents/{path}.toml`
- register that file in `.codex/config.toml` as `../agents/{path}.toml` because the registry file lives under `.codex/`

Deterministic field mapping:

| Claude source | Codex target | Mode | Notes |
| --- | --- | --- | --- |
| file path | `config_file` | adapted | swap `.md` for `.toml`, then store it relative to `.codex/config.toml` as `../agents/{path}.toml` |
| frontmatter `description` or first summary line | `[agents.<id>].description` | adapted | prefer explicit frontmatter when present |
| markdown body | `developer_instructions` | direct | preserve structure and wording |
| unsupported Claude-specific metadata | sidecar or dropped | lossy/manual | call out in mapping artifact if present |

Default injection policy:

- if Claude provides no explicit runtime model metadata, inject Codex defaults during conversion
- record injected defaults in the manifest so reverse conversion does not pretend they came from Claude
- convert Claude `settings.json` and hook intent to `.codex/config.toml`, optional Codex hooks, worklog rules, or mapping notes; do not require `.claude/settings.json` in Codex-native output
- convert Claude skill `context: fork` intent to registered Codex subagents plus structured summary handoffs; do not add Claude-only skill frontmatter to Codex-native skills

## Runtime Split

- `AGENTS.md`: the active project contract for Codex.
- `agents/`: project-level Codex agent configs referenced by `.codex/config.toml`.
- `.codex/`: source-of-truth for project config, rules, authored skills, and mapping docs.
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
| `agents/coordinator.toml` | `.claude/agents/coordinator.md` | bidirectional | adapted | `developer_instructions` maps to Markdown body; runtime keys use sidecar if needed |
| `.codex/config.toml` | N/A | codex-only | direct | project-level registry and runtime flags |
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
    - "agents"
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
    canonical: true
    lossy: false
  - id: agent-registry
    kind: runtime_config
    source:
      runtime: codex
      path: ".codex/config.toml"
    targets: []
    relation: "1:partial"
    transform_mode: sidecar
    canonical: true
    lossy: false
  - id: coordinator-agent
    kind: agent_config
    source:
      runtime: codex
      path: "agents/coordinator.toml"
    targets:
      - runtime: claude
        path: ".claude/agents/coordinator.md"
        canonical: false
    relation: "1:1"
    transform_mode: adapted
    canonical: true
    field_map:
      description: "[agents.coordinator].description"
      body: "developer_instructions"
    section_map:
      markdown_body: "developer_instructions"
    validation:
      - "config_file must resolve from .codex/config.toml to the agent file path"
      - "developer_instructions must be non-empty"
    lossy: false
    sidecar:
      path: ".codex/docs/mapping-sidecars/agents/coordinator.runtime.yaml"
      carries:
        - model
        - model_reasoning_effort
        - sandbox_mode
```

Use sidecars only for lossy or bundle-style transforms such as registry metadata, frontmatter remapping, or bridge skills.

## Conversion Readiness Checklist

The mapping artifact is conversion-ready only if all of the following are true:

- every `[agents.<id>]` entry has a `config_file` that resolves from `.codex/config.toml`
- every `agents/**/*.toml` file has non-empty `developer_instructions`
- the manifest explicitly states which runtime-only fields require sidecars
- generated paths preserve group structure in both directions
- any injected defaults are recorded as injected, not source-authored

## Generated Team Structure

```text
teams/{team-name}/
├── AGENTS.md
├── agents/
├── .codex/
│   ├── config.toml
│   ├── docs/
│   │   ├── format-mapping.md
│   │   └── format-mapping.manifest.yaml
│   ├── rules/
│   └── skills/
└── .agents/
    └── skills/
```

## Special Cases

- `skill-creator` is bridged into Codex as a lightweight wrapper. Prefer the globally available Codex/system skill when present. The original large implementation remains under `.claude/skills/skill-creator/`.
- `a-team` is adapted into a lightweight Codex-native entry skill under `.codex/skills/a-team/` and `.agents/skills/a-team/`. It intentionally omits Claude-only slash-command fields.
- `.codex/skills/` is the maintenance copy. `.agents/skills/` is the runtime copy. Keep them in sync.
- `prompt-patterns` is adapted as a lightweight Codex-native skill. Claude-specific raw research assets are retained under `.claude/skills/prompt-patterns/` and are not canonical Codex runtime assets.
- `settings-json`, `hooks-integration`, `frontmatter-optional-patterns`, and `skill-context-fork` are not copied directly. Their portable intent lives in `.codex/rules/codex-runtime-config.md`, `.codex/rules/codex-agent-config-patterns.md`, and `.codex/rules/context-isolation.md`.
- See `.codex/docs/claude-adaptation-audit.md` for the current migration decision log.

## Conversion Use Cases

- Claude -> Codex: import legacy team assets into the canonical Codex layout, generate `agents/*.toml`, then regenerate `.agents/skills/` as the runtime mirror.
- Codex -> Claude: export from the canonical Codex layout using the retained mapping artifact instead of inferring structure from prompts.
- Dual-format delivery: treat Codex as the source package and produce Claude-compatible output as a follow-up conversion step.
