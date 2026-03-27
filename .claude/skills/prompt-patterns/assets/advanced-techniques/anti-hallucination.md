---
name: Anti-Hallucination
category: advanced-techniques
applies_when:
  - generating-research-agent
  - generating-review-agent
  - writing-agent-prompts
  - writing-skill-prompts
tags: [hallucination, evidence-first, grounding, status-routing, uncertainty]
source: raw/tutorial-advanced-techniques.md
---

# Anti-Hallucination

## Core Principle

Claude sometimes hallucinate and makes untrue claims. Two primary strategies counter this: (1) give Claude an explicit "out" so it can admit uncertainty instead of fabricating, and (2) force evidence extraction before answering so claims are grounded in source material. Combine both for maximum reliability.

## Pattern

**Strategy 1: Give Claude an out (Anthropic verbatim):**
```
Only answer if you know the answer with certainty.
```
Without this escape clause, Claude fabricates plausible-sounding answers. With it, Claude admits "I don't have that information."

**Strategy 2: Evidence-first with scratchpad (Anthropic verbatim):**
```
Please read the below document. Then, in <scratchpad> tags, pull the most
relevant quote from the document and consider whether it answers the user's
question or whether it lacks sufficient detail. Then write a brief answer
in <answer> tags.
```
Force Claude to extract relevant quotes before answering. This reduces hallucination from distractor information because Claude must locate evidence first.

**Full evidence-first pattern with document reference:**
```
<question>What was the subscriber base on May 31, 2020?</question>
Please read the below document. Then, find the exact quotes from the
document that are most relevant to answering the question, and write
them in <quotes> tags. Then, answer the question in <answer> tags.

<document>{DOCUMENT_TEXT}</document>
```
Prefill: `<quotes>`

**Status-Based Output Routing (from Anthropic courses):**
```json
{
  "status": "COMPLETE | INSUFFICIENT_DATA | ERROR",
  "result": { ... },
  "ambiguities": [ ... ]
}
```
Define clear criteria for each status:
- **COMPLETE**: All required information present and processed
- **INSUFFICIENT_DATA**: Input fails minimum quality thresholds (enumerate them)
- **ERROR**: Processing failed (include error details)

## A-Team Application

When generating agents that consume external information (researchers, reviewers, analysts):

- Every research agent must include the "give an out" clause: "If the source material does not contain sufficient information to answer, state explicitly what is missing. Do not infer or fabricate."
- Review agents must use evidence-first: extract specific quotes/references in a scratchpad step before rendering a verdict. This directly maps to A-Team's evidence chain requirement (references -> findings -> decisions).
- For agents producing structured output, use Status-Based Output Routing. Map to A-Team's completion statuses: COMPLETE -> DONE, INSUFFICIENT_DATA -> NEEDS_CONTEXT, ERROR -> BLOCKED.
- Skill-writer must embed the scratchpad pattern in any skill that processes documents or external data.
