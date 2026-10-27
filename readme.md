# A-Team

**Build your own AI team.**

Tailored to your goals and the way you work.

**打造你的專屬 AI 團隊。**

從目標到工作方式，為你量身設計。

[English](#english) · [繁體中文](#繁體中文)

The Grok-adapted version of A-Team lives on the branch `chemistrywow31/grok-native`. It designs teams for **Grok Build**. To get it, run `git checkout chemistrywow31/grok-native`.

為 Grok 改編的 A-Team 在分支 `chemistrywow31/grok-native`。這一版為 **Grok Build** 設計團隊。取得方式：`git checkout chemistrywow31/grok-native`。

---

## English

A-Team helps you turn an idea into a reusable AI team: clear roles, a shared way of working, and expectations for the result. Describe what you want to accomplish, and shape the team through conversation.

You receive team files and configuration to run in your own AI client. This edition supports **Claude Code and Codex**, including both formats when requested.

### What would you like your team to do?

| Your work | A team you could design |
| --- | --- |
| Content | Research topics, draft a newsletter, and review it for your audience and voice. |
| Research | Compare sources, organize findings, and prepare a brief with citations. |
| Software testing | Plan test coverage, investigate failures, and review fixes. |
| Education | Develop lesson outlines, create exercises, and check clarity for your learners. |

These are starting ideas. A-Team designs the roles and workflow around your request; these examples are not a catalog of prebuilt teams.

### Make it yours

- **Goals and deliverables:** a weekly brief, a set of lesson materials, or a testing plan.
- **Roles and team size:** a compact team for focused work, or more specialized roles where they help.
- **Workflow and handoffs:** who starts, what each role passes on, and when you review the result.
- **Style and quality:** your language, tone, audience, source requirements, and what counts as a finished result.
- **Tools and platform:** the tools available in your environment and the team format your client supports.

You can bring a detailed process or just a goal. A-Team helps you work out the rest.

### From a request to a team plan

> “I publish a weekly newsletter for busy teachers. Help me build a small team that finds useful research, drafts in Traditional Chinese, and checks sources. Keep the tone practical, and let me approve the final draft.”

A possible plan gives a coordinator responsibility for the schedule and handoffs, a researcher responsibility for sources, a writer responsibility for the draft, and an editor responsibility for clarity and source checks.

The handoff could be **research notes → draft → editorial review → your approval**. If you already have a researcher, the plan can focus on writing and review. If the newsletter becomes a lesson series, the roles and outputs can evolve with it.

### How it works

1. **Describe your goal.** Share the work, your audience, constraints, and preferred AI client.
2. **Shape the team together.** Agree on responsibilities, handoffs, tools, and what a good result looks like.
3. **Receive your team files.** Review the generated instructions, configuration, and setup guidance.
4. **Refine as your needs evolve.** Adjust an existing team's wording, roles, or workflow as your work changes.

### What you get

Your team is saved under `teams/{team-name}/`, with:

- Role instructions that explain who does what and how work moves between people and agents.
- Reusable skills and working rules tailored to the task.
- Native configuration for the format you chose.
- A setup guide explaining how to start the team and what still needs configuring or verifying.

You keep the files and run them in your chosen client. A-Team designs the team; your client provides the models, tools, permissions, and execution environment.

### Get started

Use an installed, authenticated Claude Code or Codex client, and open this repository as the project.

**In Claude Code**, enter:

```text
/A-Team Help me design a team for my weekly newsletter.
```

**In Codex**, enter:

```text
$a-team Help me design a team for my weekly newsletter.
```

Tell A-Team whether you want Claude Code files, Codex files, or both. You can also ask to adapt an existing team between those formats.

After generation, open `teams/{team-name}/` and follow its `docs/RUNTIME-SETUP.md` before running it. Available tools and setup depend on your client; the repository's [runtime setup notes](.codex/docs/RUNTIME-SETUP.md) describe what has been checked and what remains unverified.

<details>
<summary>Technical references</summary>

- [Claude Code project instructions](CLAUDE.md) and [entry skill](.claude/skills/a-team/SKILL.md)
- [Codex project instructions](AGENTS.md) and [entry skill](.agents/skills/a-team/SKILL.md)
- [Claude Code ↔ Codex format mapping](.codex/docs/claude-to-codex-mapping.md)

</details>

---

## 繁體中文

A-Team 幫你把一個想法，變成可以重複使用的 AI 團隊：有清楚的分工、共同的工作方式，以及對成果的要求。說出你想完成的事，再透過對話一起設計適合你的團隊。

你會拿到團隊檔案與設定，在自己的 AI 工具中執行。本版本支援 **Claude Code 與 Codex**，也能依需求同時產出兩種格式。

### 你想讓團隊做什麼？

| 你的工作 | 可以設計的團隊方向 |
| --- | --- |
| 內容製作 | 研究主題、撰寫電子報，並依照讀者與品牌語氣審稿。 |
| 研究整理 | 比較資料來源、整理發現，產出附有引用的研究摘要。 |
| 軟體測試 | 規劃測試範圍、調查失敗原因，並審查修正。 |
| 教學設計 | 發展課程大綱、設計練習，並檢查內容是否適合學習者。 |

這些都是發想方向。A-Team 會依你的需求設計角色與流程，並非提供上列團隊的現成模板。

### 哪些地方可以客製化？

- **目標與產出：** 每週摘要、一套教材，或一份測試計畫。
- **角色與團隊規模：** 集中處理特定工作的精簡團隊，或有需要時再細分專業角色。
- **流程與交接：** 誰先開始、每個角色要交出什麼，以及何時由你檢視成果。
- **風格與品質：** 語言、語氣、讀者、資料來源要求，以及完成標準。
- **工具與平台：** 依照你的環境中可用的工具，以及所選 AI 工具支援的團隊格式設計。

你可以帶著完整流程來，也可以只有一個目標。A-Team 會協助你把其他細節釐清。

### 從一句需求，到團隊規劃

>「我每週會發一份給忙碌教師看的電子報。幫我設計一個小團隊，找實用的研究、用繁體中文寫稿，並查核來源。語氣要務實，最後由我確認稿件。」

一種可能的規劃是：由協調角色掌握進度與交接，研究角色整理來源，寫作角色完成初稿，編輯角色檢查表達與引用。

交接流程可以是 **研究筆記 → 初稿 → 編輯審查 → 你確認稿件**。如果你已經有人負責研究，就可以把設計重心放在寫作與審稿；日後若改做系列教材，也能一起調整角色與產出。

### 如何打造你的團隊？

1. **說明目標。** 告訴 A-Team 你要做的工作、服務對象、限制，以及偏好的 AI 工具。
2. **一起設計團隊。** 確認分工、交接、工具，以及什麼樣的成果才算完成。
3. **取得團隊檔案。** 檢視產出的角色指引、設定與啟動說明。
4. **隨需求持續調整。** 當工作改變時，再更新既有團隊的文字、角色或流程。

### 你會拿到什麼？

團隊會儲存在 `teams/{team-name}/`，包含：

- 角色指引，說明誰負責什麼，以及人與 AI 角色之間如何交接。
- 依任務設計的可重用技能與工作規則。
- 所選格式的原生設定。
- 啟動說明，列出使用方式，以及仍需設定或驗證的項目。

你保留這些檔案，並在自己選擇的 AI 工具中執行。A-Team 負責設計團隊；模型、工具、權限與執行環境由你使用的 AI 工具提供。

### 開始使用

先安裝並登入 Claude Code 或 Codex，再以專案方式開啟這個儲存庫。

**在 Claude Code 中輸入：**

```text
/A-Team 幫我設計一個製作每週電子報的團隊。
```

**在 Codex 中輸入：**

```text
$a-team 幫我設計一個製作每週電子報的團隊。
```

告訴 A-Team 你需要 Claude Code、Codex，或兩種格式。你也可以請它協助轉換既有團隊的格式。

產出後，開啟 `teams/{team-name}/`，依照其中的 `docs/RUNTIME-SETUP.md` 完成設定再執行。可用工具與設定取決於你使用的 AI 工具；本儲存庫的[執行環境設定說明](.codex/docs/RUNTIME-SETUP.md)列有已檢查的項目與尚未驗證的部分。

<details>
<summary>技術參考</summary>

- [Claude Code 專案指引](CLAUDE.md)與[入口技能](.claude/skills/a-team/SKILL.md)
- [Codex 專案指引](AGENTS.md)與[入口技能](.agents/skills/a-team/SKILL.md)
- [Claude Code ↔ Codex 格式對照](.codex/docs/claude-to-codex-mapping.md)

</details>
