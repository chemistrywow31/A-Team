

## A-Team: Agent-Based Team Designer for Claude Agents

team-designer-claude/          ← 整個資料夾複製到你的 .claude/ 中即可
├── agents/
│   ├── team-architect.md              ← 總調度者
│   ├── discovery/
│   │   ├── requirements-analyst.md    ← 需求深挖
│   │   └── role-designer.md           ← 角色拆分
│   ├── planning/
│   │   └── skill-planner.md           ← 技能/規則規劃
│   └── generation/
│       ├── generation-lead.md         ← 生成階段子調度者
│       ├── agent-writer.md            ← 專寫 agent
│       ├── skill-writer.md            ← 專寫 skill
│       └── rule-writer.md             ← 專寫 rule
├── skills/
│   ├── shared/
│   │   ├── structured-interview.md
│   │   ├── role-decomposition.md
│   │   └── md-generation-standard.md
│   └── specialized/
│       ├── team-topology-analysis.md
│       ├── granularity-calibration.md
│       └── quality-validation.md
└── rules/
├── coordinator-mandate.md         ← 調度者強制存在
├── output-structure.md            ← 產出目錄規範
├── conversation-protocol.md       ← 對話流程規範
└── writing-quality-standard.md    ← 撰寫品質規範