# MD Generation Standard（.md 檔案生成標準）

## 描述

定義所有 .md 檔案的通用寫作標準、格式規範和品質要求。所有 writer agent 在生成檔案時都必須遵守。

## 使用者

- `agent-writer`：撰寫 agent .md 時遵循
- `skill-writer`：撰寫 skill .md 時遵循
- `rule-writer`：撰寫 rule .md 時遵循

## 通用格式規範

### 檔案命名
- 使用 kebab-case：`content-reviewer.md`，不使用 `contentReviewer.md` 或 `content_reviewer.md`
- 名稱應直接反映角色/技能/規則的核心功能
- 保持簡潔，通常 2-4 個單詞

### 文件結構
- 第一行必須是 `# 標題`（h1），整個檔案只能有一個 h1
- 使用 `##`（h2）作為主要段落標題
- 使用 `###`（h3）作為次要段落標題
- 不使用 h4 以下的層級，避免過度嵌套

### 語言規範
- 主體內容使用繁體中文
- 技術術語保留英文（如 agent, skill, rule, PR, CI/CD, API）
- 技術術語首次出現時可括號附中文解釋，後續直接使用英文
- 指令性內容使用祈使句（「你必須...」而非「應該...」）

### 路徑引用
- 引用其他檔案時使用相對路徑
- 路徑格式：`{type}/{category}/{filename}.md`
- 範例：`skills/shared/structured-interview.md`

## 品質檢查清單

每個 .md 檔案交付前必須通過：
- [ ] 檔案有且僅有一個 h1 標題
- [ ] 所有引用的檔案路徑真實存在
- [ ] 沒有使用「盡量」「適當」「合理」等模糊詞（除非附有判斷標準）
- [ ] 單檔不超過 300 行
- [ ] 沒有重複描述其他檔案已涵蓋的內容
