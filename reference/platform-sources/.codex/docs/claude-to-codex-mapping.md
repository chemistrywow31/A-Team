# Claude And Codex Format Mapping

## Goal

For the A-Team repository itself, `.claude/` plus `CLAUDE.md` is the canonical source design for shared role intent, workflow, ownership, authority, and quality. `AGENTS.md`, `.codex/`, `agents/`, and `.agents/skills/` are its Codex projection with bounded runtime details from inventoried Codex adaptation inputs. Source authority does not require Claude runtime instructions to carry Codex execution details. Mapping is retained for regeneration and future conversion. Generated teams do not inherit A-Team's self-hosting authority automatically; their confirmed format, declaration, runnable entries, and per-team manifest declare their own authority.

## Mapping Principles

- A-Team repository canonical source: `.claude/` plus root `CLAUDE.md`
- A-Team repository Codex projection: root `AGENTS.md`, `.codex/`, `agents/`, and `.agents/skills/`
- Discovery must confirm the user's requested delivery format before planning or generation
- Each generated team declares exactly one authority: `CLAUDE.md` is the declaration for Claude canonical, `AGENTS.md` for Codex canonical, and `shared/team.yaml` for platform-neutral canonical; never infer authority from directory presence
- Every other runnable entry must agree. Multi-surface or conversion-retained teams require a manifest with matching authority, roots, surface state, and canonical-source-to-projection mappings; an unmapped single-surface team does not require one
- Generated-team writes normally stay under `teams/{team-name}/`; an external root additionally requires explicit authorization of that exact real root, exact dispatched owned paths, consistent declaration evidence, resolved-path confinement, scoped verification, and rollback
- Change the declared canonical source first, then regenerate only affected projections
- Inject Codex-only model/schema/lifecycle details only from the three `adaptation_inputs` in A-Team's manifest, within each row's exact scope and targets. The matching human audit records the same rows. These inputs do not own shared roles, workflow, or authority and do not make whole mapped trees platform-only.
- A host generating another platform's team reads the selected target specification on demand. Claude-only generation does not load Codex runtime rules; Codex output retains native model, registry, isolation, and validation requirements.
- Generated Codex agents use project-level registration in `.codex/config.toml` plus per-agent TOML files under `agents/`
- Inside `.codex/config.toml`, every `config_file` is resolved relative to `.codex/`. For team-local runtime agent configs stored under project-root `agents/`, generated entries therefore use `../agents/...`.
- Each `[agents.<id>]` table id is the stable snake_case runtime identity. The referenced TOML must repeat that identity exactly in `name`; display labels belong in descriptions or playbook prose, not in the runtime identity field.

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
| Codex `spawn_agent`, `send_message`, `followup_task`, `list_agents`, `interrupt_agent`, `wait_agent` | Claude `Agent` (legacy `Task` alias) / Agent Teams lifecycle | Bidirectional concept mapping | Map intent, ownership, and lifecycle; do not translate by tool-name substitution |
| `scripts/` (repo root) | `scripts/` (repo root) | Shared placement, runtime-specific tools | `preflight-permissions.sh` is Claude-only; `preflight-codex-runtime.sh` and `validate_codex_team.py` are Codex-only |
| `teams/{name}/docs/RUNTIME-SETUP.md` | same path | Bidirectional | Same filename both trees; body differs by probed runtime — Codex reports sandbox/approval posture, Claude Code reports auto-mode carve-outs |
| N/A | Claude auto-mode carve-out (`autoMode` in user settings) | Claude-only | No Codex counterpart. Codex gates normal work with `approval_policy` / `sandbox_mode`, while protected `.codex/` and `.agents/` rewrites still require the documented bootstrap/approval posture. |

## Platform-Neutral Shared Canonical

Use this mapping only when all authority declarations agree:

- the target team declaration identifies `shared/` as the platform-neutral canonical root
- every runnable `CLAUDE.md` and/or `AGENTS.md` entry document says it is a projection of that same root
- `.codex/docs/format-mapping.manifest.yaml` sets `canonical_authority` to `shared/` and maps canonical shared sources to the runnable projections
- the retained human mapping describes the same direction when that document is present

Map the shared families as follows:

| Shared canonical source | Sequential projections | Writer owner |
| --- | --- | --- |
| `shared/team.yaml`, `shared/roles/**` | `.claude/agents/**` and `CLAUDE.md`; then `.codex/agents/**`, `AGENTS.md`, mapping artifacts, and `agents/**/*.toml` | Agent Writer |
| `shared/rules/**` | `.claude/rules/**`; then `.codex/rules/**` | Rule Writer |
| `shared/skills/**` | `.claude/skills/**`; then `.codex/skills/**` and `.agents/skills/**` | Skill Writer |

Treat these family paths as maximum eligible surfaces, not blanket ownership. Require every dispatch to enumerate exact mutable paths. Preserve semantic parity across adapted projections and byte identity between `.codex/skills/**` and `.agents/skills/**` runtime mirrors.

For any external target, record the user's authorization for the exact normalized root before dispatch. Resolve each owned path against that root, including existing symlinks and the nearest existing parent of a new path. Missing or conflicting authority evidence, dual-canonical claims, reference-only promotion, or incomplete required mappings returns `NEEDS_CONTEXT` without mutation. Reject `..`, absolute paths outside the root, symlink escapes, and any resolved path outside the authorized root. Start at the declared Claude, Codex, or shared canonical family and regenerate only its mapped projections under the same owner.

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
| `[agents.<id>]` table name plus referenced TOML `name` | output file identity | adapted | require exact equality and use the stable snake_case id for conversion bookkeeping |
| `[agents.<id>].description` | summary line or frontmatter description | adapted | keep wording stable when possible |
| `config_file` | playbook and target identity | adapted | resolve it relative to `.codex/config.toml`, then use the same grouped path under `.codex/agents/` and `.claude/agents/` |
| `.codex/agents/{path}.md` body | markdown body | adapted | preserve role intent and section contract; translate Codex lifecycle tools, bounded helper rules, path references, and fork semantics into the selected Claude Agent/subagent or Agent Teams behavior |
| `developer_instructions` | runtime bootstrap evidence | runtime-only | verify that the thin TOML points to the corresponding `.codex/agents/` playbook; do not export the bootstrap wrapper as the Claude role body |
| `model` | frontmatter `model` plus sidecar | adapted/manual | Claude has native aliases, full IDs, and `inherit`; choose a supported target model explicitly and retain the original provider-specific pin for round-trip fidelity |
| `model_reasoning_effort` | frontmatter `effort` plus sidecar | adapted/manual | Claude has native effort; matching labels do not prove equivalent behavior or support. Preserve the original and verify the effective target model |
| `sandbox_mode` | sidecar metadata | sidecar | retain only when round-trip preservation matters |

Section handling:

- `.codex/agents/**/*.md` contains the role contract; the TOML `developer_instructions` is intentionally a thin runtime bootstrap
- tool names are not copied verbatim: Claude subagent mode keeps coordinator-only Agent delegation by A-Team policy, while Codex v2 may allow one bounded specialist helper hop
- runtime-only TOML keys that Claude cannot express must be retained in a sidecar when round-trip fidelity is required
- Codex-native research agents such as `agents/research/domain-researcher.toml` and `agents/research/decision-auditor.toml` map to `.claude/agents/research/*.md` when exporting to Claude
- TOML `name` is the Codex runtime identity and must equal the registry id exactly; `description` or playbook prose carries any human-facing display label during export

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
| stable role identity derived from the canonical path/role vocabulary | `[agents.<id>]` table id and referenced TOML `name` | adapted | emit the same snake_case value in both places; a mismatch is invalid |
| file path | `config_file` | adapted | swap `.md` for `.toml`, then store it relative to `.codex/config.toml` as `../agents/{path}.toml` |
| frontmatter `description` or first summary line | `[agents.<id>].description` | adapted | prefer explicit frontmatter when present |
| markdown body | `.codex/agents/{path}.md` body | adapted | preserve role intent and section contract; translate the selected Claude Agent lifecycle into target-supported Codex lifecycle, task-path, shared-filesystem, and fork semantics |
| generated playbook path | `developer_instructions` | adapted | write a thin bootstrap that tells the runtime agent to read `AGENTS.md` and the corresponding `.codex/agents/{path}.md` playbook |
| unsupported Claude-specific metadata | sidecar or dropped | lossy/manual | call out in mapping artifact if present |

Default injection policy:

- Claude supports explicit model/effort metadata and inheritance. Preserve the source intent; select target-native values from its verified profile, and record any cross-provider choice or injected default
- for new Codex teams, use `.codex/rules/context-tier.md` with target availability and task requirements; explicit user choices outrank examples. A-Team retains its current per-role Astra/Terra pins while its host supplies root/default choices; this does not mandate those models for every target
- restructuring preserves a target's existing model pins unless model migration is part of the authorized change; do not silently replace compatibility pins or reduce reasoning effort
- record injected defaults in the manifest so reverse conversion does not pretend they came from Claude
- convert Claude `settings.json` and hook intent to `.codex/config.toml`, optional Codex hooks, worklog rules, or mapping notes; do not require `.claude/settings.json` in Codex-native output
- convert Claude skill `context: fork` intent to registered Codex subagents plus structured summary handoffs; do not add Claude-only skill frontmatter to Codex-native skills

## Runtime Split

Claude's context-tier rule owns native Claude tiers and shared context principles, not the Codex model profile. Codex projections combine those shared principles with `codex-runtime-config.md`, `codex-agent-config-patterns.md`, and `context-isolation.md` as listed in the scoped adaptation-input inventory. Keep target model/effort pins during unrelated maintenance; never infer a model conversion from a context tier alone.

The 2026-10-06 adaptation keeps one task-specific `Reasoning` -> `Workflow` -> `Self-Critique` triad per agent. Adapt task-specific decisions and verification checks without duplicate Preflight/Verification forms or mandatory nine-slot essays. Preserve role ownership, uncertainty, required metadata, a meaningful boundary example plus useful positive/contrast cases, and runtime-specific lifecycle semantics. Prompt effectiveness comes first; the J5 size targets require an independent usefulness review when exceeded, rather than automatic content removal. Interim summaries are nonblocking; an existing scoped authorization satisfies that scope's approval requirement, while new-team confirmation and uncovered material-change approvals remain explicit. Review frozen batches independently and invalidate changed-file criteria plus dependent mapping/parity checks after corrections.

- `AGENTS.md`: the active project contract for Codex.
- `agents/`: project-level Codex agent configs referenced by `.codex/config.toml`.
- `.codex/`: active Codex project config plus adapted rules, skills, playbooks, and mapping docs.
- `.agents/skills/`: runtime skill packages that Codex can discover automatically.
- `.claude/`: canonical source design for A-Team itself. For generated teams, consult the per-team manifest.

### Current native evidence and capability scope

Current [Claude subagent guidance](https://code.claude.com/docs/en/sub-agents) supports nesting and native model/effort metadata. A-Team enforces its direct-specialist Claude policy using `disallowedTools: [Agent]`; Codex's supported helper policy is adapted independently. Useful XML, worked examples, and checks are selected by model/task guidance, not copied as universal private-thinking requests.

The installed Codex 0.160.1 and active host support A-Team's v2 profile. The [published config reference](https://learn.chatgpt.com/docs/config-file/config-reference) documents a spawned-thread limit excluding root; the active host's total-session slots include root. A future target's setup/mapping records its own observed profile, version and verification, without inserting invented profile keys into `config.toml`. Public docs, local parser support, live tool availability and model entitlement are separate evidence.

Before any target classification or write, distinguish maintaining A-Team's restructuring capability from actually maintaining named teams or an explicitly requested fleet. Capability-only work remains in the designer. For authorized targets, report observed legacy baseline versus scope-triggered requirements; root declaration coverage is not proof that every assigned role/rule/skill is mapped. Validate the exact assigned family, and keep unassigned historical families outside the write scope.

## Per-Team Mapping Artifact

Each Codex or dual-format generated team should retain `teams/{team-name}/.codex/docs/format-mapping.md` and `format-mapping.manifest.yaml`. A Claude-only team needs these when conversion retention is requested. These artifacts are authoritative for later restructuring.

For a Claude-canonical team, `CLAUDE.md` is both its canonical runnable entry and team declaration. For a Codex-canonical team, `AGENTS.md` serves both roles. The declaration names the authority and canonical roots; every other runnable root entry must agree.

For a platform-neutral `shared/` team, also retain a target-local team declaration such as `shared/team.yaml`. It must name `shared/` as platform-neutral canonical authority, enumerate or map the canonical role/rule/skill families, and agree with every runnable root entry and the machine-readable manifest. A mismatch blocks mutation.

Required sections:

1. requested delivery format
2. canonical authored format
3. Codex -> Claude asset mapping
4. Claude -> Codex asset mapping
5. lossy conversions and exceptions
6. round-trip preservation notes

Required manifest fields:

- `spec_version`
- `requested_format`
- `canonical_authority`
- `supported_directions`
- `canonical_roots`
- `surface_state`
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
canonical_authority: claude
surface_state:
  claude: runnable
  codex: runnable
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
        path: ".codex/agents/coordinator.md"
        canonical: false
      - runtime: codex
        path: "agents/coordinator.toml"
        canonical: false
    relation: "1:N"
    transform_mode: adapted
    canonical: true
    field_map:
      frontmatter.description: "registry/TOML description"
      frontmatter.model: "explicitly selected target-native model; preserve source in sidecar"
      frontmatter.effort: "verified target-native effort; preserve source in sidecar"
    section_map:
      markdown_body: ".codex/agents/coordinator.md body"
    validation:
      - "config_file must resolve from .codex/config.toml to ../agents/coordinator.toml"
      - "developer_instructions bootstraps AGENTS.md and .codex/agents/coordinator.md"
      - "role intent, authority, and completion contract retain semantic parity"
    lossy: true
    sidecar:
      path: ".codex/docs/mapping-sidecars/agents/coordinator.runtime.yaml"
      carries:
        - source_model_and_effort
        - target_model_and_model_reasoning_effort
        - sandbox_mode
```

Use sidecars only for lossy or bundle-style transforms such as registry metadata, frontmatter remapping, or bridge skills.

For a `shared/` canonical manifest, use `canonical_authority: "shared/"`, include `shared_to_claude` and/or `shared_to_codex` in `supported_directions`, and set each semantic artifact's canonical source to `runtime: shared` under `shared/`. Keep runtime-only Claude and Codex artifacts non-canonical. Do not relabel a shared target from directory presence alone.

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
├── shared/                            # when platform-neutral canonical authority is declared
│   ├── team.yaml
│   ├── roles/
│   ├── rules/
│   └── skills/
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
- Shared-canonical -> Claude/Codex: update the exact assigned `shared/` family first, then regenerate its declared Claude, Codex, runtime, root, and mapping projections sequentially under one family owner.
- Dual-format delivery: use the manifest's declared `canonical_runtime` or `canonical_authority` field according to its retained schema; never choose a source package merely because both trees exist.
- External-root delivery/evolution: require exact user authorization, one consistent Claude/Codex/shared declaration quorum, every required mapping, exact owned paths, resolved-path confinement, canonical-first projection order, scoped verification, and rollback.
