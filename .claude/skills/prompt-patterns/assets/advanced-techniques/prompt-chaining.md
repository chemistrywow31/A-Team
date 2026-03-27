---
name: Prompt Chaining
category: advanced-techniques
applies_when:
  - generating-review-agent
  - generating-execution-agent
  - writing-skill-prompts
  - generating-coding-team
tags: [chaining, self-correction, iterative, multi-turn, extract-then-process]
source: raw/tutorial-advanced-techniques.md
---

# Prompt Chaining

## Core Principle

Claude improves its own responses when asked to revise. Multi-turn conversations where Claude checks or improves its own work are a powerful pattern. Each step is a separate API call, enabling inspection and intervention between steps. The key insight: decompose complex work into generate-review-refine cycles.

## Pattern

**Self-correction chain (Anthropic verbatim):**
```
Step 1: "Name ten words that all end with the exact letters 'ab'."
Step 2: "Please find replacements for all 'words' that are not real words.
         If all the words are real words, return the original list."
```
The escape clause ("If all words are real") prevents Claude from second-guessing correct answers due to expectation bias.

**Extract-then-process chain:**
```
Step 1: "Find all names from the below text: {TEXT}"
        Prefill: <names>
Step 2: "Alphabetize the list."
```

**Quality improvement chain:**
```
Chain: Generate -> Review -> Improve
Step 1: "Write a three-sentence short story about a girl who likes to run."
Step 2: "Make the story better."
```

**Conditional verification pattern (from courses):**
- Original: "Find replacements for all invalid items."
- Improved: "Find replacements for invalid items. If all items are valid, return the original list."

This prevents unnecessary modifications to correct output.

**Multi-turn message format:**
```python
messages = [
    {"role": "user", "content": first_user},
    {"role": "assistant", "content": first_response},
    {"role": "user", "content": second_user}
]
```

## A-Team Application

When generating teams with quality review cycles:

- Code review agents must use the self-correction pattern: first pass identifies issues, second pass verifies fixes. Include the conditional escape clause so the reviewer does not fabricate issues when code is correct.
- Skill-writer must structure multi-step skills as explicit chains: step 1 extracts/generates, step 2 reviews, step 3 refines. Document each step as a separate section in SKILL.md.
- For coding teams, embed the generate-review-refine cycle directly in the workflow: developer agent generates code, code reviewer evaluates, developer incorporates feedback. Each handoff is a separate Task dispatch.
- Process reviewer agents must use extract-then-process: first extract observations from the execution log, then analyze patterns, then produce recommendations. This prevents premature conclusions.
