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
- **Shape and size:** one agent with a set of skills for work that stays in one thread, or several agents where the work really runs in parallel or needs an independent check.
- **Workflow and handoffs:** who starts, what each role passes on, and when you review the result.
- **Style and quality:** your language, tone, audience, source requirements, and what counts as a finished result.
- **Tools and platform:** the tools available in your environment and the team format your client supports.

You can bring a detailed process or just a goal. A-Team helps you work out the rest.

### From a request to a team plan

> “I publish a weekly newsletter for busy teachers. Help me build a small team that finds useful research, drafts in Traditional Chinese, and checks sources. Keep the tone practical, and let me approve the final draft.”

A-Team first decides the shape of the work. Here the steps run one after another on the same issue, and you approve every draft, so the plan is one agent with skills for finding research, drafting in Traditional Chinese, and checking sources. It is not four agents passing notes to each other.

The flow is **find research → draft → check sources → your approval**. If drafts later go out without your review, the plan adds a separate checker that has not seen how the draft was written. If the newsletter becomes a lesson series, the skills and outputs can evolve with it.

### How it works

1. **Describe your goal.** Share the work, your audience, constraints, and preferred AI client.
2. **Shape the team together.** Agree on responsibilities, handoffs, tools, and what a good result looks like.
3. **Receive your team files.** Review the generated instructions, configuration, and setup guidance.
4. **Refine as your needs evolve.** Adjust an existing team's wording, roles, or workflow as your work changes.

### What you get

Your team is saved under `teams/{team-name}/`, with:

- Reusable skills tailored to the task: how your work is done, step by step.
- When the work needs more than one agent, role instructions that explain who does what and how work moves between them.
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
- **型態與規模：** 工作在同一條脈絡中完成時，用一個代理人搭配一組技能；確實需要平行進行或獨立查核時，才分成多個代理人。
- **流程與交接：** 誰先開始、每個角色要交出什麼，以及何時由你檢視成果。
- **風格與品質：** 語言、語氣、讀者、資料來源要求，以及完成標準。
- **工具與平台：** 依照你的環境中可用的工具，以及所選 AI 工具支援的團隊格式設計。

你可以帶著完整流程來，也可以只有一個目標。A-Team 會協助你把其他細節釐清。

### 從一句需求，到團隊規劃

>「我每週會發一份給忙碌教師看的電子報。幫我設計一個小團隊，找實用的研究、用繁體中文寫稿，並查核來源。語氣要務實，最後由我確認稿件。」

A-Team 會先判斷這份工作的型態。這個例子裡，各步驟依序處理同一期內容，而且每份稿件都由你確認，所以規劃是一個代理人，搭配找研究、用繁體中文寫稿、查核來源三項技能，而不是四個互相交接的代理人。

流程是 **找研究 → 寫初稿 → 查核來源 → 你確認稿件**。如果之後稿件不再經過你確認就發出，規劃會加入一個獨立的查核者，它不會看到稿件的寫作過程。日後若改做系列教材，技能與產出也能一起調整。

### 如何打造你的團隊？

1. **說明目標。** 告訴 A-Team 你要做的工作、服務對象、限制，以及偏好的 AI 工具。
2. **一起設計團隊。** 確認分工、交接、工具，以及什麼樣的成果才算完成。
3. **取得團隊檔案。** 檢視產出的角色指引、設定與啟動說明。
4. **隨需求持續調整。** 當工作改變時，再更新既有團隊的文字、角色或流程。

### 你會拿到什麼？

團隊會儲存在 `teams/{team-name}/`，包含：

- 依任務設計的可重用技能：一步一步說明你的工作怎麼做。
- 工作需要多個代理人時，另有角色指引，說明誰負責什麼，以及彼此如何交接。
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
