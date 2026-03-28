# A-Team

A-Team is a multi-agent team designer. It interviews the user, decomposes responsibilities, plans skills and rules, and generates ready-to-run team structures.

This repository supports **dual-platform** operation:

- **Claude Code**: `CLAUDE.md` + `.claude/` (agents, skills, rules)
- **Codex**: `AGENTS.md` + project `.codex/` + runtime `agents/` + `.agents/skills/`

Each platform has its own native configuration. Format conversion between platforms is also supported.

---

## English

### What A-Team Does

A-Team is not the final agent team. It is a **team-design system** that generates agent teams.

It takes a vague request such as:

> "I need a content operations team for an education product"

and turns it into:

- a coordinator role
- grouped specialist roles
- reusable skills
- hard rules
- worklog and context management rules
- a ready-to-use team folder under `teams/{team-name}/`

### Dual-Platform Generation

A-Team supports **dual-platform team generation**:

- **Claude Code native generation**: produces `CLAUDE.md` + `.claude/` structure
- **Codex native generation**: produces `AGENTS.md` + project `.codex/` + runtime `agents/` + `.agents/skills/` structure
- **Dual-format**: generates both platform formats in one pass

During discovery, A-Team asks which delivery format the user wants and generates the corresponding native structure directly.

### Format Conversion Support

A-Team also supports **format conversion** between Codex and Claude Code team layouts.

Supported conversion flows:

- **Claude Code → Codex**: convert an existing Claude Code team to Codex format
- **Codex → Claude Code**: convert an existing Codex team to Claude Code format

### Codex Quick Start

1. Open this repo in Codex.
2. Let Codex load the root `AGENTS.md`.
3. Use the existing A-Team runtime directly at the repo root. This repo already ships project-level multi-agent registration in `.codex/config.toml` and `agents/`.
4. Tell A-Team what kind of team you want to design.
5. Follow the discovery interview.
6. Review the generated output under `teams/{team-name}/`.

### Codex Settings

The project-level Codex settings live in `.codex/config.toml`:

```toml
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
disable_response_storage = true
project_doc_fallback_filenames = ["AGENTS.md", "CLAUDE.md"]

[features]
multi_agent = true

[agents]
max_threads = 6
max_depth = 1

[agents.team_architect]
description = "Coordinate A-Team discovery, planning, generation, review, and delivery."
config_file = "../agents/team-architect.toml"
```

`config_file` is resolved relative to `.codex/config.toml`, not the repo root. Because this repo keeps runtime agent configs in the top-level `agents/` directory, the correct path form is `../agents/...`.

What these settings are for:

- `model = "gpt-5.4"`: use the current frontier agentic coding model as the repo default
- `model_reasoning_effort = "xhigh"`: prefer maximum reasoning headroom for coordination-heavy and multi-step design work
- `disable_response_storage = true`: reduces saved output overhead for multi-agent sessions
- `project_doc_fallback_filenames = ["AGENTS.md", "CLAUDE.md"]`: lets Codex open both new Codex teams and older Claude-only teams
- `[features] multi_agent = true`: enables Codex multi-agent at the project level for this repo
- `[agents]` plus `[agents.<id>]`: registers A-Team's coordinator and specialists for Codex runtime

### How Multi-Agent Works In Codex Here

For this repo, the orchestration logic is driven by `AGENTS.md` and `.codex/agents/team-architect.md`. Codex multi-agent is enabled from this project's `.codex/config.toml`, not from a required user-level flag.

This repo also ships its own official agent registry under `agents/`. The runtime `agents/*.toml` files are thin Codex-facing configs; the `.codex/agents/*.md` files remain the source-of-truth playbooks those configs point to.

When a team or generation pass uses `multi-agent` mode, the coordinator:

- checks the target project's `.codex/config.toml` for `[features] multi_agent = true` and agent registry conflicts
- checks `~/.claude/settings.json` for `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` only when Claude Code support also matters
- delegates focused specialist work with `spawn_agent`
- sends clarifications or follow-up tasks with `send_input`
- joins work only at real synchronization points with `wait`

Recommended rule of thumb:

- use `single-agent` when the work is mostly sequential or tightly coupled
- use `multi-agent` when role boundaries are clear and file ownership can stay non-overlapping

### Skills In Codex

Codex runtime skill discovery happens from `.agents/skills/`.

That means:

- `.codex/skills/` = authored/maintained mirror
- `.agents/skills/` = runtime-discoverable mirror

Do not rely on `.codex/skills/` alone if you want Codex to auto-discover project skills.

### Repository Layout

```text
.
├── AGENTS.md
├── .codex/
│   ├── config.toml
│   ├── agents/             # A-Team's internal playbook library
│   ├── rules/
│   ├── skills/
│   └── docs/
├── agents/                  # A-Team's own Codex runtime agent configs
├── .agents/
│   └── skills/
├── .claude/                 # Claude Code native config
├── .worklog/                # Phase-level work documentation
│   └── {yyyymm}/{task}/    # references.md, findings.md, decisions.md per phase
└── teams/
```

### Quick Start

```
/A-Team
```

This slash command spawns the Team Architect coordinator and runs the full 6-phase workflow. You can also pass arguments:

```
/A-Team 自動化測試團隊          # start with a direction
/A-Team --restructure teams/x   # restructure an existing team
```

Every generated team also gets a `/boss` entry-point skill so team members can invoke their coordinator the same way.

### Core Workflow

1. Discovery
   Clarify the requested delivery format, objectives, scope, workflow, role candidates, and whether `single-agent` or `multi-agent` is appropriate. Domain Researcher investigates best practices in parallel.
2. Planning
   Decide shared skills, specialist skills, external skill reuse, hard rules, and retained conversion requirements. Decision Auditor reviews Phase 1 decisions.
3. Generation
   Generate `AGENTS.md`, `.codex/`, `agents/`, `.agents/skills/`, worklog/context management rules, and mapping artifacts for the target team.
4. Optional optimization
   Tighten prompts and reduce ambiguity.
5. Review
   Validate structure, paths, ownership, and execution mode consistency.
6. Dialogue review
   Audit the quality of the consultation itself.

Cross-phase support: `domain-researcher` (external investigation) and `decision-auditor` (decision quality audit) are available at any phase boundary or on-demand.

### Worklog System

Every task maintains a `.worklog/` directory with phase-level documentation:

```
.worklog/202603/team-name/
├── phase-1-discovery/
│   ├── references.md      ← Sources consulted
│   ├── findings.md        ← Key discoveries
│   └── decisions.md       ← Decisions + rationale
└── phase-2-planning/
    └── ...
```

This provides **verifiability** (every decision traces to evidence), **traceability** (full audit trail), and **continuity** (interrupted work can be resumed from worklog). The worklog also serves as a context offloading mechanism — agents read from worklog files instead of carrying full context.

### Generated Team Output

Generated teams follow this structure:

```text
teams/{team-name}/
├── AGENTS.md
├── agents/
├── .codex/
│   ├── config.toml
│   ├── docs/
│   │   ├── format-mapping.md
│   │   └── format-mapping.manifest.yaml
│   ├── rules/                # Includes worklog + context management rules
│   └── skills/
├── .worklog/                  # Phase-level documentation (created at runtime)
└── .agents/
    └── skills/
```

### Platform Mapping

Both platforms coexist in this repo, each with its own native configuration:

| Claude Code | Codex | Notes |
| --- | --- | --- |
| `CLAUDE.md` | `AGENTS.md` | Project entrypoint |
| `.claude/agents/` | `agents/` + `.codex/config.toml` | Agent definitions and registry |
| `.claude/rules/` | `.codex/rules/` | Rule definitions |
| `.claude/skills/` | `.codex/skills/` + `.agents/skills/` | Skills (Codex has runtime mirror) |

Format conversion between the two is supported in both directions.

---

## 繁體中文

### A-Team 是做什麼的

A-Team 不是最終要執行工作的 agent team，本身是**用來設計 agent team 的系統**。

它會把像這樣的需求：

>「我想做一個教育產品的內容營運團隊」

轉成：

- 一個 coordinator
- 一組有清楚分工的 specialist agents
- 可重用的 skills
- 不可違反的 rules
- worklog 與上下文管理規則
- 一個可直接拿去用的 `teams/{team-name}/` 輸出資料夾

### 支援雙平台生成

A-Team 支援**雙平台團隊生成**：

- **Claude Code 原生生成**：產出 `CLAUDE.md` + `.claude/` 結構
- **Codex 原生生成**：產出 `AGENTS.md` + 專案 `.codex/` + runtime `agents/` + `.agents/skills/` 結構
- **Dual-format**：一次同時產出兩個平台的格式

A-Team 會在 discovery 階段詢問使用者要哪一種團隊格式，直接生成對應的原生結構。

### 支援格式轉換

A-Team 也支援 **Codex 與 Claude Code 團隊格式之間的互相轉換**：

- **Claude Code → Codex**：把現有 Claude Code 團隊轉成 Codex 格式
- **Codex → Claude Code**：把現有 Codex 團隊轉成 Claude Code 格式

### Codex 快速開始

1. 用 Codex 開啟這個 repo。
2. 讓 Codex 讀取 root `AGENTS.md`。
3. 直接在 repo root 使用 A-Team。這個 repo 已經內建 project-level multi-agent registration：`.codex/config.toml` + `agents/`
4. 告訴它你想設計什麼團隊。
5. 跟著 discovery 訪談把需求講清楚。
6. 到 `teams/{team-name}/` 檢查產出的 Codex 版團隊結構。

### Codex 設定放哪裡

Codex 的專案設定放在 `.codex/config.toml`：

```toml
model = "gpt-5.4"
model_reasoning_effort = "xhigh"
disable_response_storage = true
project_doc_fallback_filenames = ["AGENTS.md", "CLAUDE.md"]

[features]
multi_agent = true

[agents]
max_threads = 6
max_depth = 1

[agents.team_architect]
description = "Coordinate A-Team discovery, planning, generation, review, and delivery."
config_file = "../agents/team-architect.toml"
```

`config_file` 是相對於 `.codex/config.toml` 解析，不是相對於 repo root。因為這個 repo 把 runtime agent config 放在頂層 `agents/` 目錄，所以正確寫法是 `../agents/...`。

這些設定的用途：

- `model = "gpt-5.4"`：把目前的 frontier agentic coding model 設成這個 repo 的預設
- `model_reasoning_effort = "xhigh"`：對高協調、長鏈推理、稍微複雜的 agent 工作優先給最大 reasoning headroom
- `disable_response_storage = true`：降低多代理流程的回應儲存負擔
- `project_doc_fallback_filenames = ["AGENTS.md", "CLAUDE.md"]`：讓 Codex 既能讀新的 Codex team，也能讀舊的 Claude team
- `[features] multi_agent = true`：直接在這個專案內開啟 Codex multi-agent
- `[agents]` 與 `[agents.<id>]`：把 A-Team 自己的 coordinator 與 specialists 註冊給 Codex runtime

### Codex 要怎麼「開啟 Multi-Agent」

這個 repo 的多代理流程由 `AGENTS.md` 和 `.codex/agents/team-architect.md` 驅動，而 Codex multi-agent 是透過這個專案自己的 `.codex/config.toml` 啟用，不依賴使用者家目錄設定。

這個 repo 也已經在 `agents/` 提供 A-Team 自己的官方 agent registry。`agents/*.toml` 是給 Codex runtime 讀的薄設定，而 `.codex/agents/*.md` 仍是 source-of-truth 的 authored playbook。

Codex 版 multi-agent 的做法是：

- 先檢查目標專案的 `.codex/config.toml` 是否已有 `[features] multi_agent = true` 與既有 agent registry
- 如果也要兼容 Claude Code，再檢查 `~/.claude/settings.json` 的 `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`
- root `AGENTS.md` 定義 coordinator contract
- `.codex/agents/team-architect.md` 定義整個多代理流程
- coordinator 在需要時用 `spawn_agent` 拆給 specialist
- 需要補充上下文時用 `send_input`
- 只有在真正需要 join 的時候才用 `wait`

簡單判斷方式：

- `single-agent`：任務高度耦合、順序很重、拆了反而會多溝通成本
- `multi-agent`：角色邊界清楚、可平行、而且檔案 ownership 能明確切開

### Codex 的 Skills 放哪裡

Codex runtime 會從 `.agents/skills/` 掃描 project skills，所以這裡分兩層：

- `.codex/skills/`：作者維護用、設計來源
- `.agents/skills/`：Codex runtime 真正會掃描的 skill surface

也就是說，**只有 `.codex/skills/` 不夠**。如果你希望 Codex 自動發現技能，還是要同步到 `.agents/skills/`。

### 目前 Repo 結構

```text
.
├── AGENTS.md
├── .codex/
│   ├── config.toml
│   ├── agents/             # A-Team 內部的 playbook library
│   ├── rules/
│   ├── skills/
│   └── docs/
├── agents/                  # A-Team 自己的 Codex runtime agent configs
├── .agents/
│   └── skills/
├── .claude/                 # Claude Code 原生設定
├── .worklog/                # 階段性工作文件
│   └── {yyyymm}/{task}/    # 每個 phase 有 references.md, findings.md, decisions.md
└── teams/
```

### 快速開始

```
/A-Team
```

這個 slash command 會啟動 Team Architect 指揮官，跑完整的 6 階段流程。也可以帶參數：

```
/A-Team 自動化測試團隊          # 帶方向直接開始
/A-Team --restructure teams/x   # 重構現有團隊
```

每個產出的團隊也會自動生成 `/boss` 入口 skill，讓團隊成員可以用同樣的方式啟動自己的指揮官。

### A-Team 的工作流程

1. Discovery
   先確認需要的團隊格式，再釐清目標、範圍、workflow、角色候選，以及到底該用 `single-agent` 還是 `multi-agent`。Domain Researcher 同步調查領域最佳實踐。
2. Planning
   規劃 shared skills、specialized skills、external skill reuse、rules，以及要保留哪些轉換資訊。Decision Auditor 審核 Phase 1 決策。
3. Generation
   為目標團隊產出 `AGENTS.md`、`.codex/`、`agents/`、`.agents/skills/`、worklog/上下文管理規則 與 mapping artifacts
4. Optional optimization
   收斂 prompt、減少模糊與冗語
5. Review
   驗證結構、路徑、ownership 與 execution mode 是否一致
6. Dialogue review
   回頭審視整個諮詢對話品質

跨階段支援：`domain-researcher`（外部調查）和 `decision-auditor`（決策品質審核）可在任何階段邊界或臨時需要時調用。

### Worklog 系統

每個任務都在 `.worklog/` 目錄下維護階段性文件：

```
.worklog/202603/team-name/
├── phase-1-discovery/
│   ├── references.md      ← 參考資訊來源
│   ├── findings.md        ← 關鍵發現與分析
│   └── decisions.md       ← 決策 + 理由
└── phase-2-planning/
    └── ...
```

三大核心價值：**可驗證性**（每個決策可追溯到證據）、**可追溯性**（完整審計軌跡）、**可接續性**（中斷的工作可從 worklog 恢復）。Worklog 同時作為上下文卸載機制 — agent 從 worklog 讀取資料，而非攜帶完整 context。

### 產出的團隊長什麼樣子

```text
teams/{team-name}/
├── AGENTS.md
├── agents/
├── .codex/
│   ├── config.toml
│   ├── docs/
│   │   ├── format-mapping.md
│   │   └── format-mapping.manifest.yaml
│   ├── rules/                # 包含 worklog + 上下文管理規則
│   └── skills/
├── .worklog/                  # 階段性工作文件（執行時建立）
└── .agents/
    └── skills/
```

### 雙平台對照

兩個平台各自有原生設定，共存於此 repo：

| Claude Code | Codex | 說明 |
| --- | --- | --- |
| `CLAUDE.md` | `AGENTS.md` | 專案入口 |
| `.claude/agents/` | `agents/` + `.codex/config.toml` | Agent 定義與註冊 |
| `.claude/rules/` | `.codex/rules/` | Rule 定義 |
| `.claude/skills/` | `.codex/skills/` + `.agents/skills/` | Skills（Codex 有 runtime mirror） |

兩個方向的格式轉換皆有支援。
