---
name: Complex Prompt Template
category: advanced-techniques
applies_when:
  - writing-agent-prompts
  - writing-skill-prompts
  - generating-coordinator
  - generating-execution-agent
tags: [template, ten-element, assembly-order, prompt-structure, query-placement]
source: raw/tutorial-advanced-techniques.md
---

# Complex Prompt Template

## Core Principle

Anthropic's 10-element template is the recommended structure for complex prompts. Not all prompts need every element. Start comprehensive, then refine. Placing the user's query close to the bottom yields ~30% quality improvement over placing it at the top.

## Pattern

**The 10 elements in recommended assembly order:**

| # | Element | Placement |
|---|---------|-----------|
| 1 | User role | Always first |
| 2 | Task context | Early -- role, goals, background |
| 3 | Tone context | Early -- communication style |
| 4 | Task description & rules | After context -- constraints, escape hatches |
| 5 | Examples | Middle -- `<example>` tags, edge cases |
| 6 | Input data | Middle -- XML-tagged variable content |
| 7 | Immediate task request | Near end -- reiterate what to do |
| 8 | Precognition | Near end -- "think step by step" |
| 9 | Output formatting | Near end -- response structure |
| 10 | Prefilling | Assistant turn -- force format |

**Verbatim Career Coach prompt (Anthropic reference) -- demonstrates all 10 elements:**
```
[Element 2: Task context]    You will be acting as an AI career coach named Joe...
[Element 3: Tone]            You should maintain a friendly customer service tone.
[Element 4: Rules]           - Always stay in character, as Joe
                             - If unsure: "Sorry, I didn't understand that..."
                             - If irrelevant: "Sorry, I am Joe and I give career advice..."
[Element 5: Example]         <example>Customer: Hi... Joe: Hello! My name is Joe...</example>
[Element 6: Input data]      <history>{HISTORY}</history> <question>{QUESTION}</question>
[Element 7: Task request]    How do you respond to the user's question?
[Element 8: Precognition]    Think about your answer first before you respond.
[Element 9: Output format]   Put your response in <response></response> tags.
[Element 10: Prefill]        [Joe] <response>
```
Full verbatim prompt: see `raw/tutorial-advanced-techniques.md` Chapter 9.

**Key ordering rules:**
- Context and background go FIRST; user query and format instructions go LAST
- Precognition goes between task request and output format
- Query at end = 30% quality improvement (Anthropic measured)

## A-Team Application

When agent-writer constructs agent .md files:

- Map the 10-element template to agent .md sections: frontmatter (element 1-2), Role/Context Tier (element 2-3), Responsibilities/Rules (element 4), Workflow with examples (element 5-6), Output format (element 9).
- For coordinator agents, the "immediate task request" (element 7) maps to the dispatch instructions -- reiterate the specific task near the end of every Task dispatch.
- For skill prompts, place the user's input data late in the prompt body and put format instructions after it. Skill-writer must structure SKILL.md examples following this order.
- Precognition (element 8) must appear in every agent that makes judgment calls -- embed "analyze first, then decide" before the output format section.
