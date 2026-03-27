---
name: Long Context
category: advanced-techniques
applies_when:
  - generating-research-agent
  - generating-coordinator
  - writing-skill-prompts
  - writing-agent-prompts
tags: [long-context, document-placement, query-position, grounding, context-window]
source: raw/tutorial-advanced-techniques.md
---

# Long Context

## Core Principle

When working with long documents, placement matters. Documents go at the TOP of the prompt; instructions and examples go at the BOTTOM. Placing the user's query at the end of a long prompt yields ~30% quality improvement. Ground responses in extracted quotes before answering to prevent hallucination across large context windows.

## Pattern

**Document structure with source tracking:**
```
<document index="1">
<source>annual-report-2024.pdf</source>
<document_content>
{LONG_DOCUMENT_TEXT}
</document_content>
</document>

<document index="2">
<source>competitor-analysis.pdf</source>
<document_content>
{SECOND_DOCUMENT}
</document_content>
</document>
```

**Grounding pattern -- extract quotes before answering (Anthropic verbatim):**
```
<question>{QUESTION}</question>
Please read the below document. Then, find the exact quotes from the
document that are most relevant to answering the question, and write
them in <quotes> tags. Then, answer the question in <answer> tags.

<document>{DOCUMENT_TEXT}</document>
```
Prefill: `<quotes>`

**Optimal long-context prompt layout:**
```
1. Long documents (TOP)           -- raw reference material
2. Background context             -- what this task is about
3. Rules and constraints          -- boundaries
4. Examples                       -- calibration
5. User query / immediate task    -- BOTTOM
6. Precognition instruction       -- "think first"
7. Output format                  -- structure
```

**Key placement rules (Anthropic):** Context early; user query near the bottom; task reminders and output formatting toward the end (better than at the beginning).

## A-Team Application

When generating agents that process large inputs (research agents, document analysts, coordinators reading worklogs):

- Research agent prompts must place source documents at the top and analysis instructions at the bottom. Agent-writer must structure the workflow to read documents first, then receive the specific question.
- Coordinator agents dispatching tasks with upstream worklog paths: instruct the agent to load worklog content at the top of its working context, then read task instructions. This matches A-Team's context management rule (pass paths, not inline content).
- For skills that process documents, SKILL.md must specify: "Place input documents inside `<document>` tags at the start. Place your question or instruction after all documents."
- Always include the grounding step (extract quotes in `<quotes>` tags) when agents answer questions about provided documents.
