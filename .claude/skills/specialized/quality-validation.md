# Quality Validation（產出品質驗證）

## 描述

提供驗證最終產出（整個團隊的 agents/skills/rules 結構）是否完整且一致的檢查方法。

## 歸屬

本 skill 專屬於 `agents/generation/generation-lead.md`

## 驗證流程

### Level 1: 結構完整性

```
✓ teams/{team-name}/ 目錄存在
✓ agents/ 目錄存在且包含至少一個調度者 .md
✓ skills/ 目錄存在且包含 shared/ 和 specialized/ 子目錄
✓ rules/ 目錄存在且包含至少一個 .md 檔案
✓ 所有 .md 檔案名稱使用 kebab-case
✓ 所有 agent 分組資料夾名稱使用 kebab-case
```

### Level 2: 內容完整性

```
✓ 每個 agent .md 都包含：身份、職責、輸入與輸出、工作流程、可用技能、適用規則、協作關係、邊界
✓ 調度者 .md 額外包含：團隊概覽、下屬 Agent 清單、任務分配策略、品質把關機制
✓ 每個 skill .md 都包含：描述、使用者/歸屬、核心知識
✓ 每個 rule .md 都包含：適用範圍、規則內容、違反判定
```

### Level 3: 引用一致性

```
✓ agent .md 中引用的每個 skill 路徑都對應到實際存在的檔案
✓ agent .md 中引用的每個 rule 路徑都對應到實際存在的檔案
✓ skill .md 中列出的使用者都對應到實際存在的 agent
✓ rule .md 中的適用範圍都對應到實際存在的 agent
✓ 調度者的下屬清單涵蓋所有非調度者 agent
```

### Level 4: 邏輯一致性

```
✓ 沒有兩個 agent 的職責存在重疊（除非是設計為 review 關係）
✓ 所有 agent 的職責加總後覆蓋團隊的完整工作範圍
✓ 沒有 agent 同時出現在兩個不同的分組中
✓ 協作關係是雙向一致的（A 說下游是 B，B 也應說上游是 A）
```

## 驗證結果格式

```markdown
# 品質驗證報告：{team-name}

## 結構完整性：✓ 通過 / ✗ 未通過
{如未通過，列出具體問題}

## 內容完整性：✓ 通過 / ✗ 未通過
{如未通過，列出具體問題}

## 引用一致性：✓ 通過 / ✗ 未通過
{如未通過，列出具體問題}

## 邏輯一致性：✓ 通過 / ✗ 未通過
{如未通過，列出具體問題}

## 總結
{通過 / 需修正，以及修正建議}
```
