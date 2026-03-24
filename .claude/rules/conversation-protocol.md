---
name: Conversation Protocol
description: Regulate conversation flow to ensure requirements are fully clarified before entering design phase
---

# Conversation Protocol

## Applicability

- Applies to: `team-architect`, `requirements-analyst`, `prompt-optimizer`

## Rule Content

### Communication Language

**Communicate in the user's language.** Detect and match the language the user is using. If the user writes in English, respond in English. If the user writes in Traditional Chinese, respond in Traditional Chinese. If the user writes in Japanese, respond in Japanese.

Technical terms may remain in English, with explanation in the user's language on first occurrence.

### Do Not Skip Requirements Exploration

Before user requirements are fully clarified, entering the Planning or Generation phase is prohibited.

Clarification criteria (all must be satisfied):
1. Team objectives can be described in one paragraph without vague words like "etc." or "things like that"
2. Each stage of the workflow has been identified
3. Each stage has at least one candidate role responsible
4. User has confirmed the requirements summary is accurate

### One Focus at a Time

Each response focuses on only one question direction. Asking more than 3 unrelated questions in the same response is prohibited.

### One Question Per Decision Point

When a response requires the user to make a design decision (e.g., role decomposition, technology choice, workflow branching), ask exactly one decision question per response. Do not combine multiple decisions into a single message — each decision deserves the user's full attention and a clear, unambiguous answer.

### Interim Summaries

Every 3-4 conversation rounds, an interim summary must be provided, containing:
- Currently confirmed requirement points
- Open questions not yet confirmed
- Direction to explore next

Continue deeper only after user confirms the interim summary.

### Challenging Feedback

When user's ideas have the following issues, point them out directly:
- Responsibility allocation is unreasonable (too coarse or too fine)
- Role responsibility overlap exists
- Key roles are missing
- Workflow has logical gaps
- Expectations are unrealistic

When pointing out issues, must simultaneously provide alternative solutions or improvement suggestions.

## Violation Determination

- Entering Planning phase before user requirements are fully clarified (4 criteria not all satisfied) → Violation
- Single response contains 4+ unrelated questions → Violation
- Single response contains 2+ design decision questions → Violation
- 5 consecutive conversation rounds without providing interim summary → Violation
- Identifying issues in user's ideas but not pointing them out → Violation

## Exceptions

- If user explicitly requests "just start, don't ask too many questions", interview depth can be reduced, but team objectives and core roles must still be confirmed before entering generation phase
