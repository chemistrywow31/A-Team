# A-Team Prompt Engineering Knowledge Base

Reference materials distilled from Anthropic's official documentation, tutorials, courses, and engineering blog. Writers read specific knowledge files during generation — not the entire index.

## How to Use

**Manual selection:** Coordinator reads this index, picks relevant files by scenario, includes paths in writer dispatch.

**Script selection:** `python .claude/skills/prompt-patterns/select.py --scenario "generating-coordinator"` outputs matching file paths.

**Writer dispatch format:**
```xml
<knowledge_refs>
Read these before writing:
- .claude/skills/prompt-patterns/assets/templates/parallel-tool-calls.md
- .claude/skills/prompt-patterns/assets/context-strategies/compaction.md
</knowledge_refs>
```

---

## Scenario Quick Reference

| Generating... | Key Knowledge Files |
|---------------|-------------------|
| **Coordinator** | `templates/parallel-tool-calls.md`, `context-strategies/compaction.md`, `context-strategies/sub-agent-dispatch.md`, `templates/commitment-over-exploration.md`, `claude-4-patterns/anti-overthinking.md` |
| **Execution agent** | `templates/default-to-action.md`, `templates/investigate-before-answering.md`, `advanced-techniques/anti-hallucination.md`, `claude-4-patterns/tone-calibration.md` |
| **Research agent** | `templates/research-structured.md`, `advanced-techniques/chain-of-thought.md`, `advanced-techniques/few-shot-patterns.md`, `context-strategies/progressive-disclosure.md` |
| **Review/QA agent** | `templates/conservative-action.md`, `advanced-techniques/anti-hallucination.md`, `templates/avoid-excessive-markdown.md` |
| **Coding team** | `templates/investigate-before-answering.md`, `templates/anti-over-engineering.md`, `templates/anti-hard-coding.md`, `claude-4-patterns/over-engineering-prevention.md` |
| **Frontend team** | `templates/frontend-aesthetics.md`, `templates/anti-over-engineering.md` |
| **Long-running tasks** | `context-strategies/compaction.md`, `context-strategies/multi-window-workflow.md`, `context-strategies/structured-notes.md`, `templates/context-awareness.md` |
| **Rules writing** | `claude-4-patterns/tone-calibration.md`, `advanced-techniques/xml-tag-separation.md` |
| **Skill writing** | `advanced-techniques/few-shot-patterns.md`, `advanced-techniques/complex-prompt-template.md` |
| **Prompt optimization** | `claude-4-patterns/tone-calibration.md`, `claude-4-patterns/anti-overthinking.md`, `claude-4-patterns/prefill-migration.md` |

---

## File Catalog

### templates/ — Ready-to-Use Anthropic Prompt Blocks
Verbatim prompt blocks from official Anthropic documentation. Inject directly into generated prompts.

| File | Purpose |
|------|---------|
| `default-to-action.md` | Make agents proactive — implement rather than suggest |
| `conservative-action.md` | Make agents cautious — research before acting |
| `parallel-tool-calls.md` | Maximize parallel tool execution (~100% success rate) |
| `investigate-before-answering.md` | Anti-hallucination — read code before claiming |
| `avoid-excessive-markdown.md` | Flowing prose instead of bullet-point fragments |
| `frontend-aesthetics.md` | Distinctive UI design, avoid "AI slop" aesthetic |
| `anti-over-engineering.md` | Four-pillar constraint: scope, docs, defensive, abstraction |
| `anti-hard-coding.md` | General-purpose solutions, no test-specific hacks |
| `research-structured.md` | Competing hypotheses, confidence tracking, self-critique |
| `autonomy-safety.md` | Reversibility-aware actions, confirm before destructive ops |
| `context-awareness.md` | Context window compaction awareness for long tasks |
| `commitment-over-exploration.md` | Prevent Opus 4.6 over-exploration loops |
| `subagent-usage.md` | When to delegate vs work directly |
| `reduce-thinking.md` | Prevent unnecessary extended thinking |

### context-strategies/ — Agent Context Management
Patterns for managing context across multi-agent, multi-turn, and long-horizon workflows.

| File | Purpose |
|------|---------|
| `compaction.md` | Summarize → reinitialize when approaching context limit |
| `sub-agent-dispatch.md` | Context isolation via sub-agents returning compressed summaries |
| `progressive-disclosure.md` | JIT context loading with lightweight identifiers |
| `structured-notes.md` | Agent memory via periodic note-writing outside context |
| `system-prompt-design.md` | "Right altitude" — not too specific, not too vague |
| `multi-window-workflow.md` | Cross-context-window state management patterns |
| `hybrid-strategy.md` | Pre-loaded context (speed) + autonomous exploration (precision) |

### advanced-techniques/ — Prompt Engineering Techniques
Core techniques from Anthropic's tutorial and courses, distilled for A-Team's generation use.

| File | Purpose |
|------|---------|
| `chain-of-thought.md` | Visible reasoning steps before answering |
| `few-shot-patterns.md` | 3-5 diverse examples = most effective steering tool |
| `anti-hallucination.md` | Give-an-out + evidence-first extraction patterns |
| `complex-prompt-template.md` | 10-element template with assembly order |
| `xml-tag-separation.md` | Claude-specific XML boundary training advantage |
| `prompt-chaining.md` | Generate → review → refine self-correction pattern |
| `long-context.md` | Long documents top, instructions bottom, quote-grounding |

### claude-4-patterns/ — Claude 4.6 Specific Patterns
Behavioral changes and migration patterns specific to Claude 4.6.

| File | Purpose |
|------|---------|
| `adaptive-thinking.md` | Effort parameter replaces budget_tokens |
| `tone-calibration.md` | Reduced urgency language — normal tone prevents over-triggering |
| `anti-overthinking.md` | Prevent excessive upfront exploration |
| `prefill-migration.md` | Alternatives to deprecated prefilled responses |
| `subagent-orchestration.md` | Native delegation — manage overuse tendency |
| `over-engineering-prevention.md` | Four-pillar constraint + anti-hard-coding |

---

## Raw Sources

| File | Lines | Origin |
|------|-------|--------|
| `assets/raw/tutorial-advanced-techniques.md` | 714 | github.com/anthropics/prompt-eng-interactive-tutorial |
| `assets/raw/courses-advanced-patterns.md` | 891 | github.com/anthropics/courses |
| `assets/raw/context-engineering-blog.md` | 405 | anthropic.com/engineering |
| `assets/raw/claude-4-best-practices.md` | 1301 | platform.claude.com (5 pages merged) |
