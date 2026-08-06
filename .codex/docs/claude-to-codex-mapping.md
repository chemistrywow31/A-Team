# Claude And Codex Format Mapping

## Goal

For the A-Team repository itself, `.claude/` is the canonical source design and `AGENTS.md`, `.codex/`, `agents/`, and `.agents/skills/` are its Codex projection. Mapping is retained so regeneration and future conversion remain deterministic. Generated teams do not inherit A-Team's self-hosting authority automatically; their confirmed format and per-team manifest declare their own canonical runtime.

## Mapping Principles

- A-Team repository canonical source: `.claude/` plus root `CLAUDE.md`
- A-Team repository Codex projection: root `AGENTS.md`, `.codex/`, `agents/`, and `.agents/skills/`
- Discovery must confirm the user's requested delivery format before planning or generation
- Each generated team's mapping manifest declares its canonical runtime; never infer authority from directory presence
- Change the declared canonical source first, then regenerate only affected projections
- Generated Codex agents use project-level registration in `.codex/config.toml` plus per-agent TOML files under `agents/`
- Inside `.codex/config.toml`, every `config_file` is resolved relative to `.codex/`. For team-local runtime agent configs stored under project-root `agents/`, generated entries therefore use `../agents/...`.

## Mapping Table

| Codex Asset | Claude Counterpart | Direction | Notes |
| --- | --- | --- | --- |
| `AGENTS.md` | `CLAUDE.md` | Bidirectional | Root runtime contract; content must stay semantically aligned |
| `.codex/agents/` | `.claude/agents/` | Bidirectional adaptation | Runtime-specific authoritative playbooks; preserve role intent while translating lifecycle tools, delegation depth, paths, and context rules |
| `agents/` | `.claude/agents/` frontmatter and sidecars | Bidirectional adaptation | Thin Codex runtime TOMLs hold model, effort, sandbox, and a bootstrap pointer to the matching `.codex/agents/` playbook |
| `.codex/config.toml` | N/A | Codex anchor | Project-level runtime registration, feature flags, and agent registry metadata |
| `.codex/rules/` | `.claude/rules/` | Bidirectional | Hard constraints and process rules |
| `.codex/skills/` | `.claude/skills/` | Claude -> Codex adaptation | Codex-authored mirror uses Codex-valid frontmatter and vocabulary |
| `.agents/skills/` | `.claude/skills/` | Claude -> Codex runtime | Runtime-discoverable Codex skill copy mirrors authored or adapted skills |
| `.codex/docs/format-mapping.md` | N/A | Codex anchor | Per-team retained mapping artifact for round-trip conversion |
| Codex `spawn_agent`, `send_message`, `followup_task`, `list_agents`, `interrupt_agent`, `wait_agent` | Claude `Task` / Agent Teams lifecycle | Bidirectional concept mapping | Map intent, ownership, and lifecycle; do not translate by tool-name substitution |
| `scripts/` (repo root) | `scripts/` (repo root) | Shared placement, runtime-specific tools | `preflight-permissions.sh` is Claude-only; `preflight-codex-runtime.sh` and `validate_codex_team.py` are Codex-only |
| `teams/{name}/docs/RUNTIME-SETUP.md` | same path | Bidirectional | Same filename both trees; body differs by probed runtime — Codex reports sandbox/approval posture, Claude Code reports auto-mode carve-outs |
| N/A | Claude auto-mode carve-out (`autoMode` in user settings) | Claude-only | No Codex counterpart. Codex gates normal work with `approval_policy` / `sandbox_mode`, while protected `.codex/` and `.agents/` rewrites still require the documented bootstrap/approval posture. |

## Agent Transform Rules

### Codex -> Claude

Convert each Codex agent from three inputs:

1. the registry entry in `.codex/config.toml`
2. the referenced agent TOML file after resolving `config_file` relative to `.codex/config.toml` (normally `../agents/**/*.toml`)
3. the authoritative playbook at the same relative path under `.codex/agents/**/*.md`

Deterministic path rule:

- `.codex/agents/{path}.md` + `agents/{path}.toml` -> `.claude/agents/{path}.md`

Deterministic field mapping:

| Codex source | Claude target | Mode | Notes |
| --- | --- | --- | --- |
| `[agents.<id>]` table name | output file identity | adapted | use the id for stable conversion bookkeeping |
| `[agents.<id>].description` | summary line or frontmatter description | adapted | keep wording stable when possible |
| `config_file` | playbook and target identity | adapted | resolve it relative to `.codex/config.toml`, then use the same grouped path under `.codex/agents/` and `.claude/agents/` |
| `.codex/agents/{path}.md` body | markdown body | adapted | preserve role intent and section contract; translate Codex lifecycle tools, bounded helper rules, path references, and fork semantics into Claude-valid Task/Agent behavior |
| `developer_instructions` | runtime bootstrap evidence | runtime-only | verify that the thin TOML points to the corresponding `.codex/agents/` playbook; do not export the bootstrap wrapper as the Claude role body |
| `model` | sidecar metadata | sidecar | Claude agent markdown has no direct equivalent |
| `model_reasoning_effort` | sidecar metadata | sidecar | retain only when round-trip preservation matters |
| `sandbox_mode` | sidecar metadata | sidecar | retain only when round-trip preservation matters |

Section handling:

- `.codex/agents/**/*.md` contains the role contract; the TOML `developer_instructions` is intentionally a thin runtime bootstrap
- tool names are not copied verbatim: Claude subagent mode keeps coordinator-only Task/Agent delegation, while Codex v2 may allow one bounded specialist helper hop
- runtime-only TOML keys that Claude cannot express must be retained in a sidecar when round-trip fidelity is required
- Codex-native research agents such as `agents/research/domain-researcher.toml` and `agents/research/decision-auditor.toml` map to `.claude/agents/research/*.md` when exporting to Claude
- `name` and `description` in TOML are runtime metadata in Codex and map to Claude frontmatter or heading metadata during export

### Claude -> Codex

Convert each Claude agent markdown file into:

1. one adapted `.codex/agents/**/*.md` playbook
2. one thin `agents/**/*.toml` runtime config
3. one `[agents.<id>]` registration in `.codex/config.toml`

Deterministic path rule:

- `.claude/agents/{path}.md` -> `.codex/agents/{path}.md` + `agents/{path}.toml`
- register that file in `.codex/config.toml` as `../agents/{path}.toml` because the registry file lives under `.codex/`

Deterministic field mapping:

| Claude source | Codex target | Mode | Notes |
| --- | --- | --- | --- |
| file path | `config_file` | adapted | swap `.md` for `.toml`, then store it relative to `.codex/config.toml` as `../agents/{path}.toml` |
| frontmatter `description` or first summary line | `[agents.<id>].description` | adapted | prefer explicit frontmatter when present |
| markdown body | `.codex/agents/{path}.md` body | adapted | preserve role intent and section contract; translate Task/Agent behavior into current Codex lifecycle, task-path, shared-filesystem, and fork semantics |
| generated playbook path | `developer_instructions` | adapted | write a thin bootstrap that tells the runtime agent to read `AGENTS.md` and the corresponding `.codex/agents/{path}.md` playbook |
| unsupported Claude-specific metadata | sidecar or dropped | lossy/manual | call out in mapping artifact if present |

Default injection policy:

- if Claude provides no explicit runtime model metadata, inject Codex defaults during conversion
- record injected defaults in the manifest so reverse conversion does not pretend they came from Claude
- convert Claude `settings.json` and hook intent to `.codex/config.toml`, optional Codex hooks, worklog rules, or mapping notes; do not require `.claude/settings.json` in Codex-native output
- convert Claude skill `context: fork` intent to registered Codex subagents plus structured summary handoffs; do not add Claude-only skill frontmatter to Codex-native skills

## Runtime Split

- `AGENTS.md`: the active project contract for Codex.
- `agents/`: project-level Codex agent configs referenced by `.codex/config.toml`.
- `.codex/`: active Codex project config plus adapted rules, skills, playbooks, and mapping docs.
- `.agents/skills/`: runtime skill packages that Codex can discover automatically.
- `.claude/`: canonical source design for A-Team itself. For generated teams, consult the per-team manifest.

## Per-Team Mapping Artifact

Each Codex or dual-format generated team should retain `teams/{team-name}/.codex/docs/format-mapping.md` and `format-mapping.manifest.yaml`. A Claude-only team needs these when conversion retention is requested. These artifacts are authoritative for later restructuring.

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

| Codex path | Claude path | Direction | Status | Notes |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | `CLAUDE.md` | bidirectional | direct | root contract |
| `agents/coordinator.toml` | `.claude/agents/coordinator.md` | bidirectional | adapted | `developer_instructions` maps to Markdown body; runtime keys use sidecar if needed |
| `.codex/config.toml` | N/A | codex-only | direct | project-level registry and runtime flags |
| `.agents/skills/research/SKILL.md` | `.claude/skills/research/SKILL.md` | claude-to-codex | adapted | runtime copy maps to canonical or declared source bundle |

Status values:

- `direct`: one-to-one conversion is expected
- `adapted`: semantic mapping exists but structure differs
- `lossy`: some structure or metadata cannot round-trip cleanly
- `manual`: human review is required

Recommended manifest shape:

```yaml
spec_version: 1
requested_format: dual-format
canonical_runtime: claude
supported_directions:
  - claude_to_codex
  - codex_to_claude
canonical_roots:
  claude_authored:
    - ".claude"
  codex_projection:
    - ".codex"
    - "agents"
    - ".agents"
default_policies:
  ambiguity: fail
  lossy_transform: require_sidecar
artifacts:
  - id: root-project-doc
    kind: project_doc
    source:
      runtime: claude
      path: "CLAUDE.md"
    targets:
      - runtime: codex
        path: "AGENTS.md"
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
    canonical: false
    lossy: false
  - id: coordinator-agent
    kind: agent_config
    source:
      runtime: claude
      path: ".claude/agents/coordinator.md"
    targets:
      - runtime: codex
        path: "agents/coordinator.toml"
        canonical: false
    relation: "1:1"
    transform_mode: adapted
    canonical: true
    field_map:
      frontmatter.description: "description"
      markdown_body: "developer_instructions"
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
- every registered TOML has a same-relative-path authoritative playbook under `.codex/agents/`, and its bootstrap points to that playbook
- Claude and Codex playbooks are checked for semantic parity, not byte identity; runtime-specific lifecycle and path vocabulary must differ where their host contracts differ
- requested format, canonical authority, and runnable surfaces are explicit and non-conflicting
- every runnable root entry has a complete `Generated by A-Team on {yyyy-mm-dd}` stamp; dual projections have matching generation stamps
- the manifest explicitly states which runtime-only fields require sidecars
- generated paths preserve group structure in both directions
- any injected defaults are recorded as injected, not source-authored

## Generated Team Structure

```text
teams/{team-name}/
├── CLAUDE.md                         # when Claude-runnable or reference mirror is requested
├── .claude/                          # when declared by requested format/mapping
├── AGENTS.md                          # when Codex-runnable
├── agents/                            # when Codex-runnable
├── .codex/                            # when Codex-runnable or mapping retention requires it
│   ├── config.toml
│   ├── docs/
│   │   ├── format-mapping.md
│   │   └── format-mapping.manifest.yaml
│   ├── rules/
│   └── skills/
└── .agents/                           # when Codex runtime skills are shipped
    └── skills/
```

## Special Cases

- `skill-creator` is bridged into Codex as a lightweight wrapper. Prefer the globally available Codex/system skill when present. The original large implementation remains under `.claude/skills/skill-creator/`.
- `a-team` is adapted into a lightweight Codex-native entry skill under `.codex/skills/a-team/` and `.agents/skills/a-team/`. It intentionally omits Claude-only slash-command fields.
- `.codex/skills/` is the maintenance copy. `.agents/skills/` is the runtime copy. Keep them in sync.
- `prompt-patterns` is adapted as a lightweight Codex-native skill. Claude-specific raw research assets remain canonical source/reference assets under `.claude/skills/prompt-patterns/` and are deliberately not copied into the runtime package.
- `settings-json`, `hooks-integration`, `frontmatter-optional-patterns`, and `skill-context-fork` are not copied directly. Their portable intent lives in `.codex/rules/codex-runtime-config.md`, `.codex/rules/codex-agent-config-patterns.md`, and `.codex/rules/context-isolation.md`.
- See `.codex/docs/claude-adaptation-manifest.toml` for the machine-readable M5 inventory and `.codex/docs/claude-adaptation-audit.md` for its rationale.

## Conversion Use Cases

- Claude-canonical -> Codex: adapt the declared Claude source into `AGENTS.md`, `.codex/`, and `agents/*.toml`, then regenerate `.agents/skills/` as the runtime mirror.
- Codex-canonical -> Claude: export from the declared Codex source using the retained mapping artifact instead of inferring structure from prompts.
- Dual-format delivery: use the manifest's `canonical_runtime`; never choose a source package merely because both trees exist.
