# A-Team

A-Team is a multi-agent team designer. It interviews the user, decomposes responsibilities, plans skills and rules, and generates ready-to-run team structures.

This repository now ships with a **Codex-native runtime layer**:

- `AGENTS.md` for the project entrypoint
- `.codex/` for prompts, rules, config, and authored skills
- `.agents/skills/` for runtime-discoverable Codex skills

The original `.claude/` tree is kept as the **legacy/source design** and migration reference.

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
- a Codex-ready team folder under `teams/{team-name}/`

### Dual-Platform Generation

A-Team now supports **dual-platform team generation**:

- Codex-native generation
- Claude-compatible delivery planning
- dual-format planning for teams that may need both runtimes

The important constraint is that **Codex remains the canonical authored format**. During discovery, A-Team asks which delivery format the user wants. Even if the user wants Claude compatibility, A-Team generates the Codex package first and preserves mapping for later conversion.

### Format Conversion Support

A-Team also supports **future format conversion** between Codex and Claude-style team layouts.

For each generated team, A-Team retains:

- `.codex/docs/format-mapping.md` for human-readable bidirectional mapping
- `.codex/docs/format-mapping.manifest.yaml` for machine-readable artifact mapping

This makes these flows possible:

- Claude -> Codex import into the canonical Codex layout
- Codex -> Claude export from the canonical Codex layout
- dual-format delivery where Codex is authored first and Claude-compatible output is derived afterward

### Codex Quick Start

1. Open this repo in Codex.
2. Let Codex load the root `AGENTS.md`.
3. Use the existing A-Team runtime directly at the repo root.
4. Tell A-Team what kind of team you want to design.
5. Follow the discovery interview.
6. Review the generated output under `teams/{team-name}/`.

### Codex Settings

The project-level Codex settings live in `.codex/config.toml`:

```toml
model_reasoning_effort = "high"
disable_response_storage = true
project_doc_fallback_filenames = ["AGENTS.md", "CLAUDE.md"]
```

What these settings are for:

- `model_reasoning_effort = "high"`: better fit for coordination-heavy and multi-step design work
- `disable_response_storage = true`: reduces saved output overhead for multi-agent sessions
- `project_doc_fallback_filenames = ["AGENTS.md", "CLAUDE.md"]`: lets Codex open both new Codex teams and older Claude-only teams

For Codex multi-agent itself, the user-level setting lives in `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

A-Team checks this user-level file before generating a `multi-agent` team.

### How Multi-Agent Works In Codex Here

For this repo, the orchestration logic is driven by `AGENTS.md` and `.codex/agents/team-architect.md`, but Codex multi-agent still depends on the user-level feature flag in `~/.codex/config.toml`.

When a team or generation pass uses `multi-agent` mode, the coordinator:

- checks `~/.codex/config.toml` for `[features] multi_agent = true`
- checks `~/.claude/settings.json` for `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` when Claude Code support also matters
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
│   ├── agents/
│   ├── rules/
│   ├── skills/
│   └── docs/
├── .agents/
│   └── skills/
├── .claude/                 # legacy/source design
└── teams/
```

### Core Workflow

1. Discovery
   Clarify the requested delivery format, objectives, scope, workflow, role candidates, and whether `single-agent` or `multi-agent` is appropriate.
2. Planning
   Decide shared skills, specialist skills, external skill reuse, hard rules, and retained conversion requirements.
3. Generation
   Generate `AGENTS.md`, `.codex/`, `.agents/skills/`, and mapping artifacts for the target team.
4. Optional optimization
   Tighten prompts and reduce ambiguity.
5. Review
   Validate structure, paths, ownership, and execution mode consistency.
6. Dialogue review
   Audit the quality of the consultation itself.

### Generated Team Output

Generated teams follow this structure:

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

### Migration Notes

`CLAUDE.md` and `.claude/` were not deleted. They remain the source implementation and migration baseline.

The platform mapping is bidirectional:

| Claude layout | Codex layout | Direction |
| --- | --- | --- |
| `CLAUDE.md` | `AGENTS.md` | Bidirectional |
| `.claude/agents/` | `.codex/agents/` | Bidirectional |
| `.claude/rules/` | `.codex/rules/` | Bidirectional |
| `.claude/skills/` | `.codex/skills/` + `.agents/skills/` | Bidirectional with runtime mirroring |

See `.codex/docs/claude-to-codex-mapping.md` for the conversion model and retained mapping artifact design.

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
- 一個可直接拿去用的 `teams/{team-name}/` 輸出資料夾

### 支援雙平台生成

A-Team 現在支援**雙平台團隊生成**：

- 直接生成 Codex-native 團隊
- 規劃 Claude-compatible 交付
- 規劃同時面向兩邊 runtime 的 dual-format 輸出

但有一個核心原則：**Codex 永遠是 canonical authored format**。A-Team 會在 discovery 階段先問使用者要哪一種團隊格式；即使使用者要 Claude 相容格式，也會先把 Codex 套件生出來，再保留 mapping 供後續轉換。

### 支援格式轉換

A-Team 也支援 **Codex 與 Claude 團隊格式之間的後續轉換**。

每個生成團隊都會保留：

- `.codex/docs/format-mapping.md`：給人看的雙向 mapping 說明
- `.codex/docs/format-mapping.manifest.yaml`：給工具或流程用的 machine-readable artifact mapping

因此可以支援：

- Claude -> Codex 匯入到 canonical Codex 結構
- Codex -> Claude 從 canonical Codex 結構匯出
- dual-format 交付，先寫 Codex，再導出 Claude-compatible 版本

### Codex 快速開始

1. 用 Codex 開啟這個 repo。
2. 讓 Codex 讀取 root `AGENTS.md`。
3. 直接在 repo root 使用 A-Team。
4. 告訴它你想設計什麼團隊。
5. 跟著 discovery 訪談把需求講清楚。
6. 到 `teams/{team-name}/` 檢查產出的 Codex 版團隊結構。

### Codex 設定放哪裡

Codex 的專案設定放在 `.codex/config.toml`：

```toml
model_reasoning_effort = "high"
disable_response_storage = true
project_doc_fallback_filenames = ["AGENTS.md", "CLAUDE.md"]
```

這三個設定的用途：

- `model_reasoning_effort = "high"`：讓這種高協調、長鏈推理的 team design 工作更穩
- `disable_response_storage = true`：降低多代理流程的回應儲存負擔
- `project_doc_fallback_filenames = ["AGENTS.md", "CLAUDE.md"]`：讓 Codex 既能讀新的 Codex team，也能讀舊的 Claude team

Codex 的 multi-agent 使用者層設定則放在 `~/.codex/config.toml`：

```toml
[features]
multi_agent = true
```

A-Team 在生成 `multi-agent` 團隊前，會先檢查這個使用者層設定檔。

### Codex 要怎麼「開啟 Multi-Agent」

這個 repo 的多代理流程雖然由 `AGENTS.md` 和 `.codex/agents/team-architect.md` 驅動，但 Codex 端仍然要先在 `~/.codex/config.toml` 開啟 `[features] multi_agent = true`。

Codex 版 multi-agent 的做法是：

- 先檢查 `~/.codex/config.toml` 的 `[features] multi_agent = true`
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
│   ├── agents/
│   ├── rules/
│   ├── skills/
│   └── docs/
├── .agents/
│   └── skills/
├── .claude/                 # 保留作為 legacy/source 設計
└── teams/
```

### A-Team 的工作流程

1. Discovery
   先確認需要的團隊格式，再釐清目標、範圍、workflow、角色候選，以及到底該用 `single-agent` 還是 `multi-agent`
2. Planning
   規劃 shared skills、specialized skills、external skill reuse、rules，以及要保留哪些轉換資訊
3. Generation
   為目標團隊產出 `AGENTS.md`、`.codex/`、`.agents/skills/` 與 mapping artifacts
4. Optional optimization
   收斂 prompt、減少模糊與冗語
5. Review
   驗證結構、路徑、ownership 與 execution mode 是否一致
6. Dialogue review
   回頭審視整個諮詢對話品質

### 產出的團隊長什麼樣子

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

### 舊版 Claude 結構還在嗎

還在。

- `CLAUDE.md` / `.claude/` 沒有刪掉
- 它們現在是 legacy/source implementation
- Codex 版則由 `AGENTS.md`、`.codex/`、`.agents/skills/` 承接

這個對照現在是雙向保留的：

| Claude 版 | Codex 版 | 方向 |
| --- | --- | --- |
| `CLAUDE.md` | `AGENTS.md` | 雙向 |
| `.claude/agents/` | `.codex/agents/` | 雙向 |
| `.claude/rules/` | `.codex/rules/` | 雙向 |
| `.claude/skills/` | `.codex/skills/` + `.agents/skills/` | 雙向，外加 runtime mirror |

更完整的對照與轉換策略請看 `.codex/docs/claude-to-codex-mapping.md`。
