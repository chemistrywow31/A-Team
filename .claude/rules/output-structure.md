---
name: Output Structure
description: Specify directory configuration and naming rules for all generated team structures
---

# Output Structure

## Applicability

- Applies to: `team-architect`, `agent-writer`, `skill-writer`, `rule-writer`

## Rule Content

### Directory Structure

All generated team structures must follow this directory configuration:

```
teams/{team-name}/
├── CLAUDE.md                         ← Team-wide instructions all agents must follow
├── .worklog/                         ← Phase-level work documentation (created at runtime)
│   └── {yyyymm}/
│       └── {task-name}/
│           ├── phase-1-{label}/
│           │   ├── references.md     ← Sources consulted
│           │   ├── findings.md       ← Key discoveries and analysis
│           │   └── decisions.md      ← Decisions with rationale and evidence
│           └── phase-{n}-{label}/
│               └── ...
└── .claude/
    ├── agents/
    │   ├── {coordinator}.md          ← Coordinator, in agents/ root directory
    │   ├── {group-a}/                ← Grouped by function or workflow
    │   │   ├── {agent-1}.md
    │   │   └── {agent-2}.md
    │   └── {group-b}/
    │       └── {agent-3}.md
    ├── skills/
    │   ├── boss/                     ← Entry-point skill (invokes coordinator)
    │   │   └── SKILL.md
    │   ├── {skill-1}/                ← Each skill has its own folder
    │   │   └── SKILL.md              ← Fixed filename (uppercase)
    │   ├── {skill-2}/
    │   │   └── SKILL.md
    │   └── {skill-3}/
    │       └── SKILL.md
    ├── rules/
    │   ├── {rule-1}.md               ← Unconditional or path-scoped
    │   ├── {rule-2}.md
    │   └── {subdirectory}/           ← Optional grouping (e.g., frontend/, backend/)
    │       └── {rule-3}.md
    └── settings.json                 ← Hooks, permissions, env (per rules/settings-json.md)
```

### Naming Conventions

- Team name: kebab-case, reflecting team purpose (e.g., `english-teaching-content`)
- Folder names: kebab-case
- File names: kebab-case, ending with `.md`
- Spaces, underscores, and uppercase letters are prohibited

### CLAUDE.md Content Guidelines

`CLAUDE.md` is placed at the team root (`teams/{team-name}/CLAUDE.md`), at the same level as `.claude/`. It contains instructions that **every agent in the team** must follow. When deployed, it becomes the project-level `CLAUDE.md` that Claude Code automatically loads for all agents and teammates.

Content to include in CLAUDE.md:
- Team objectives and scope summary
- Universal behavioral norms (e.g., communication language, output format)
- Project-wide technical constraints (e.g., tech stack, coding standards)
- Deployment mode instructions (subagent vs Agent Teams, see below)
- Worklog and context management instructions (mandatory, see below)
- `@path/to/file` imports to reference shared documents (e.g., `@README.md`, `@docs/architecture.md`). Imported files expand into context at launch. Relative paths resolve from the CLAUDE.md location. Maximum import depth is 5 levels.

Content NOT to include in CLAUDE.md (put these in `rules/` instead):
- Rules that apply to only a subset of agents
- Role-specific behavioral constraints
- Quality standards for specific deliverable types
- File-type-specific conventions (use `paths` frontmatter in rules/ to scope them)

### Deployment Mode Section in CLAUDE.md

Every generated CLAUDE.md must include a deployment mode section specifying how the team is intended to run:

- **Subagent mode**: Agents are invoked via the Task tool within a single session. Coordinator manages all delegation. Suitable for sequential workflows with clear handoffs.
- **Agent Teams mode** (experimental): Agents run as independent Claude Code instances with shared task lists and direct messaging. Suitable for parallel workflows where agents need peer-to-peer communication.

Agent Teams mode requires additional configuration:

- `.claude/settings.json` must set `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"` and `teammateMode: "in-process"` (default) or `"tmux"`
- CLAUDE.md must list the **known limitations**: no `/resume` recovery for teammates, fixed lead per session, one team per session, no nested teams, no split-pane support in VS Code / Windows Terminal / Ghostty
- Each agent .md must declare File Ownership (which directories it owns) — see `agent-writer.md` template
- Direct messaging channels between agents must be enumerated in CLAUDE.md (which agent talks to which, on what topics)

### CLAUDE.md Lifecycle

- **Precedence**: Managed (org-wide) > User (`~/.claude/CLAUDE.md`) > Project (team root `CLAUDE.md`) > Local (`.claude.local.md`, gitignored). Generated team CLAUDE.md sits at project scope.
- **Nested CLAUDE.md**: Place additional CLAUDE.md files in subdirectories only when subdirectory-specific rules exist. Nested CLAUDE.md loads on-demand when Claude reads files in that subdirectory.
- **Compaction behavior**: The team-root CLAUDE.md is re-injected after auto-compaction. Nested CLAUDE.md files are NOT re-injected — they reload on-demand. Put load-bearing rules in the root, not in nested files.
- **`@imports`**: Resolve relative to the CLAUDE.md location. Maximum import depth is 5 hops. Imported content expands at session start and counts toward context budget.
- **`claudeMdExcludes`**: Settings can exclude paths from CLAUDE.md auto-loading (e.g., to skip vendored CLAUDE.md files in `node_modules/`).

### Worklog and Context Management Section in CLAUDE.md

Every generated CLAUDE.md must include a worklog and context management section that defines:

1. **Worklog structure**: `.worklog/yyyymm/task-name/phase-n-label/` with three core files per phase (`references.md`, `findings.md`, `decisions.md`)
2. **Coordinator dispatch rules**: Every Task dispatch must include the worklog path and upstream reference paths
3. **Agent return format**: Agents must return structured summaries with completion status (`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`); full detail goes to the worklog
4. **Phase-end archival**: Coordinator verifies worklog completeness before phase transitions

### Template Consistency for Mandatory Sections

The worklog section, context management section, and deployment mode section in generated CLAUDE.md files must follow a standardized structure. Agent-writer must not rewrite these sections from scratch for each team. Instead, adapt the template defined in this rule and in `rules/context-management.md`, substituting only team-specific variables (team name, phase labels, agent names). This ensures consistency across generated teams and prevents drift.

The generated team's `rules/` directory must also include:
- A **worklog rule** defining the `.worklog/` structure and evidence chain requirements
- A **context management rule** defining task isolation, summary-based reporting, and worklog-based context recovery

### Entry-Point Skill

Every generated team must include an entry-point skill at `skills/boss/SKILL.md`, invokable as `/boss`. This skill spawns the team's coordinator agent via the Agent tool, ensuring users always enter through the coordinator's full workflow.

The entry-point skill must:
- Use `boss` as the skill folder name and slash command name (consistent across all generated teams)
- Spawn the coordinator agent with `subagent_type` matching the coordinator's name
- Pass any user-provided arguments as context to the coordinator
- Support bare invocation (no arguments → coordinator starts from Phase 1 or the beginning of its workflow)

The entry-point skill frontmatter must declare:

```yaml
---
name: Boss
description: {Entry point that spawns the {coordinator} to run {workflow description}}
disable-model-invocation: true
allowed-tools: ["Agent"]
argument-hint: "[team-specific hint]"
---
```

- `disable-model-invocation: true` prevents Claude from auto-triggering the full workflow from conversational context. The workflow must be explicitly invoked by the user.
- `allowed-tools: ["Agent"]` pre-approves the Agent tool so `/boss` does not prompt for permission mid-invocation.
- `argument-hint` provides autocomplete guidance for the team's expected arguments.

### Path-Scoped Rules

Rules in `.claude/rules/` support an optional `paths` field in YAML frontmatter. Use this to scope rules to specific file types, reducing context consumption and improving adherence:

- **Unconditional rules** (no `paths`): Load at session start for all files. Use for process rules, communication norms, and team-wide behavioral constraints.
- **Path-scoped rules** (with `paths`): Load only when Claude reads files matching the glob patterns. Use for file-type-specific conventions (e.g., TypeScript style, test coverage requirements, API format standards).

```yaml
---
name: TypeScript Conventions
description: Enforce TypeScript coding standards across all source files
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
---
```

### Placement Rules

- `CLAUDE.md` must be at the team root directory, at the same level as `.claude/`
- Coordinator .md must be in `agents/` root directory, cannot be placed in subfolders
- Non-coordinator agents must be in subfolders under `agents/`
- Each skill must have its own folder, containing `SKILL.md` (uppercase)
- Rules are in `rules/` directory. Subdirectories are allowed for grouping (e.g., `rules/frontend/`, `rules/backend/`). All `.md` files are discovered recursively

## Violation Determination

- Team root directory missing `CLAUDE.md` → Violation
- `CLAUDE.md` placed inside `.claude/` instead of at team root → Violation
- `CLAUDE.md` missing deployment mode section → Violation
- `CLAUDE.md` missing worklog and context management section → Violation
- Generated team missing worklog rule in `rules/` → Violation
- Generated team missing context management rule in `rules/` → Violation
- Coordinator .md appears in a subfolder → Violation
- Non-coordinator agent placed directly in `agents/` root directory (same level as coordinator) → Violation
- Skill exists directly as `.md` file instead of `{skill-name}/SKILL.md` format → Violation
- File or folder name does not follow kebab-case → Violation
- Generated team missing entry-point skill at `skills/boss/SKILL.md` → Violation
- Entry-point skill `skills/boss/SKILL.md` missing `disable-model-invocation: true` → Violation
- Entry-point skill missing `allowed-tools: ["Agent"]` → Violation
- Entry-point skill missing `argument-hint` → Violation
- Generated team missing `.claude/settings.json` → Violation (see `rules/settings-json.md`)
- Team declares Agent Teams mode in CLAUDE.md but `settings.json` lacks `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` → Violation
- Agent Teams mode team missing File Ownership section in any agent .md → Violation
- Agent Teams mode team CLAUDE.md missing the known-limitations list → Violation
- Generated team missing baseline hook set in `settings.json` → Violation (see `rules/hooks-integration.md`)

## Exceptions

- If the team has only 1 group (e.g., all agents belong to the same specialty), at least one subfolder must still be created; agents cannot be placed directly in `agents/` root directory
