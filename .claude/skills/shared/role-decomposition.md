# Role Decomposition（職責拆解方法論）

## 描述

提供將團隊職責拆解為適當顆粒度 agent 角色的方法論和決策框架。

## 使用者

- `role-designer`：用於角色設計階段的職責拆分
- `team-architect`：用於驗收階段的結構合理性評估

## 核心框架：MECE 職責拆分

每個 agent 的職責必須符合 MECE 原則：
- **Mutually Exclusive（互斥）**：任何一項具體工作只應歸屬於一個 agent
- **Collectively Exhaustive（窮盡）**：所有工作加總後不應有遺漏

## 顆粒度校準方法

### 過粗的信號（需要拆分）
- agent 的職責描述超過 5 項核心工作
- agent 需要在兩個以上不同專業領域間切換
- agent 的產出物類型超過 3 種
- 用一句話無法概括這個 agent 是做什麼的

### 過細的信號（需要合併）
- 兩個 agent 的輸入來源完全相同
- 一個 agent 的產出物只有唯一一個下游消費者，且兩者的專業領域相同
- 一個 agent 的工作量不足以獨立存在（只有 1-2 項簡單工作）
- 拆分後兩個 agent 的每個任務都需要互相溝通

### 合適顆粒度的標誌
- 每個 agent 可以用一句話清楚描述其核心職責
- 每個 agent 有 3-5 項核心工作
- agent 間的互動以「交付產出物」為主，而非「持續性討論」
- 移除任何一個 agent 都會導致某類工作無人負責

## 分組策略

按優先順序選擇分組依據：

1. **工作流程階段**（最推薦）
   - 適用場景：團隊工作有明確的前後順序
   - 範例：discovery → planning → execution → review

2. **專業領域**
   - 適用場景：團隊跨多個專業，但每個專業內流程相似
   - 範例：content → technical → quality

3. **產出物導向**
   - 適用場景：團隊的產出物類型差異大
   - 範例：code → documentation → visual-assets
