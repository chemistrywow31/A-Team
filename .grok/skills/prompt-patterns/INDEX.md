# A-Team Prompt Engineering Knowledge Base

Maintained patterns informed by official native guidance, with A-Team-authored contracts and examples. Read only relevant candidates. Selection is not blanket prompt assembly: adapt each pattern to the actual task, model/mode, and runtime. Technique sources were checked in the original adaptation on 2026-10-06; Grok runtime details follow `.grok/policies/grok-agent-config.md`. Historical snapshots remain archive-only provenance.

## How to Use

**Manual selection:** Coordinator reads this index, picks relevant files by scenario, includes paths in writer dispatch.

**Script selection:** `python .grok/skills/prompt-patterns/select.py --scenario "generating-coordinator"` outputs matching file paths.

**Writer dispatch format:**
```xml
<knowledge_refs>
Read these before writing:
- .grok/skills/prompt-patterns/assets/templates/parallel-tool-calls.md
- .grok/skills/prompt-patterns/assets/context-strategies/compaction.md
</knowledge_refs>
```

---

## Scenario Quick Reference

| Generating... | Key Knowledge Files |
|---------------|-------------------|
| **Coordinator** | `templates/parallel-tool-calls.md`, `context-strategies/compaction.md`, `context-strategies/sub-agent-dispatch.md`, `templates/commitment-over-exploration.md`, `context-strategies/system-prompt-design.md` |
| **Execution agent** | `templates/default-to-action.md`, `templates/investigate-before-answering.md`, `advanced-techniques/anti-hallucination.md`, `context-strategies/system-prompt-design.md` |
| **Research agent** | `templates/research-structured.md`, `advanced-techniques/chain-of-thought.md`, `advanced-techniques/few-shot-patterns.md`, `context-strategies/progressive-disclosure.md` |
| **Review/QA agent** | `templates/conservative-action.md`, `advanced-techniques/anti-hallucination.md`, `templates/avoid-excessive-markdown.md` |
| **Coding team** | `templates/investigate-before-answering.md`, `templates/anti-over-engineering.md`, `templates/anti-hard-coding.md`, `advanced-techniques/xml-tag-separation.md` |
| **Frontend team** | `templates/frontend-aesthetics.md`, `templates/anti-over-engineering.md` |
| **Long-running tasks** | `context-strategies/compaction.md`, `context-strategies/multi-window-workflow.md`, `context-strategies/structured-notes.md`, `templates/context-awareness.md` |
| **Rules writing** | `context-strategies/system-prompt-design.md`, `advanced-techniques/xml-tag-separation.md` |
| **Skill writing** | `advanced-techniques/few-shot-patterns.md`, `advanced-techniques/complex-prompt-template.md` |
| **Prompt optimization** | `context-strategies/system-prompt-design.md`, `advanced-techniques/few-shot-patterns.md`, `advanced-techniques/chain-of-thought.md` |

---

## File Catalog

### templates/ — Attributed Prompt Blocks
Candidate prompt blocks with source attribution. Preserve useful content, adapt native details, and obey current A-Team contracts; selection does not authorize injection without checking applicability.

| File | Purpose |
|------|---------|
| `default-to-action.md` | Make agents proactive — implement rather than suggest |
| `conservative-action.md` | Make agents cautious — research before acting |
| `parallel-tool-calls.md` | Batch independent calls while preserving dependencies |
| `investigate-before-answering.md` | Anti-hallucination — read code before claiming |
| `avoid-excessive-markdown.md` | Flowing prose instead of bullet-point fragments |
| `frontend-aesthetics.md` | Distinctive UI design, avoid "AI slop" aesthetic |
| `anti-over-engineering.md` | Four-pillar constraint: scope, docs, defensive, abstraction |
| `anti-hard-coding.md` | General-purpose solutions, no test-specific hacks |
| `research-structured.md` | Competing hypotheses, confidence tracking, self-critique |
| `autonomy-safety.md` | Reversibility-aware actions, confirm before destructive ops |
| `context-awareness.md` | Context window compaction awareness for long tasks |
| `commitment-over-exploration.md` | Commit to an approach; reconsider when evidence changes |
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
| `chain-of-thought.md` | Native thinking/effort versus public worked solutions; no private transcripts |
| `few-shot-patterns.md` | Relevant worked examples and boundary cases; no universal count |
| `anti-hallucination.md` | Give-an-out + evidence-first extraction patterns |
| `complex-prompt-template.md` | Task-specific components and a worked review prompt |
| `xml-tag-separation.md` | Descriptive source/data boundaries, not a security guarantee |
| `prompt-chaining.md` | Generate → review → refine self-correction pattern |
| `long-context.md` | Task-specific document/query placement and grounded citations |

### claude-4-patterns/ — Historical, Excluded From Selection
These patterns retain their original text only at `reference/platform-sources/.claude/skills/prompt-patterns/assets/claude-4-patterns/` for provenance. `select.py` scans only templates, context-strategies, and advanced-techniques; scenario and tag queries never return this directory or `raw/`. Inspect historical files only for an explicit historical comparison, not current defaults.

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
| `reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/tutorial-advanced-techniques.md` | 714 | github.com/anthropics/prompt-eng-interactive-tutorial |
| `reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/courses-advanced-patterns.md` | 891 | github.com/anthropics/courses |
| `reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/context-engineering-blog.md` | 405 | anthropic.com/engineering |
| `reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/claude-4-best-practices.md` | 1301 | platform.claude.com (5 pages merged) |

## Selection Interface

`--scenario/-s`, `--tags/-t` (comma-separated), `--list-scenarios`, `--list-tags`, `--verbose/-v`, and `--prefix` retain their interfaces. Scenario matches remain exact; tag matches remain case-insensitive substring matches. Combined filters select the union with scenario-weighted ordering. Use list commands for the actual active metadata; the table above is a curated starting point, not the full selector output.

## Historical Technique Sources

[Claude prompting guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), [effort](https://platform.claude.com/docs/en/build-with-claude/effort), and [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-10-06. Active files mark historical attribution separately from A-Team-authored workflow examples.

## Native Adaptation

Source: `reference/platform-sources/.claude/skills/prompt-patterns/INDEX.md`. Main-session coordinator adoption, explicit native tool schemas and reference-only historical folders are A-Team Grok adaptations, not Anthropic claims.
