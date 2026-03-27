---
name: XML Tag Separation
category: advanced-techniques
applies_when:
  - writing-agent-prompts
  - writing-skill-prompts
  - generating-rules
  - generating-coding-team
tags: [xml-tags, data-separation, document-indexing, input-isolation, prompt-hygiene]
source: raw/tutorial-advanced-techniques.md
---

# XML Tag Separation

## Core Principle

Claude was trained specifically to recognize XML tags as a prompt organizing mechanism. Wrapping all variable data in descriptive tags prevents Claude from confusing instructions with input content. There are no "magic" tag names -- use whatever names make semantic sense. Claude mimics input quality: clean, well-structured prompts produce clean, well-structured output.

## Pattern

**Basic input isolation (Anthropic verbatim):**
```
Yo Claude. <email>{EMAIL}</email> <----- Make this email more polite
but don't change anything else about it.
```
Without `<email>` tags, Claude confuses the email content with the instruction text.

**List disambiguation:**
```
Below is a list of sentences. Tell me the second item on the list.
- Each is about an animal, like rabbits.
<sentences>
{SENTENCES}
</sentences>
```
Without tags, Claude misidentifies "rabbits" as a list item.

**Document indexing pattern for multiple sources:**
```
<document index="1">
<source>annual-report-2024.pdf</source>
<document_content>{CONTENT_1}</document_content>
</document>
<document index="2">
<source>quarterly-earnings.pdf</source>
<document_content>{CONTENT_2}</document_content>
</document>
```

**Hierarchical nesting:** Nest tags when data is hierarchical -- e.g., `<context>` wrapping `<user_profile>` and `<conversation_history>`, separate from `<instructions>`.

**Rules for tag usage:**
- Wrap ALL variable/dynamic data in descriptive tags
- No "magic" tag names -- `<email>`, `<document>`, `<question>` all work equally
- Nest tags when data is hierarchical
- Use consistent tag names across the prompt (do not rename mid-prompt)
- Small details matter: typos and grammar in prompts affect response quality

## A-Team Application

When generating team artifacts (agents, skills, rules):

- Agent-writer must wrap every variable input section in the agent's workflow with XML tags. If an agent receives a task description, wrap it in `<task>` tags. If it receives upstream context, wrap it in `<upstream_context>` tags.
- Skill-writer must use XML tags in all SKILL.md examples to clearly separate the skill's instructions from the user's input data. Use the document indexing pattern when skills process multiple files.
- Rule-writer must use XML tags in violation examples to separate the rule text from the example content being evaluated.
- For coding teams, use XML tags to separate code snippets (`<code>`), error messages (`<error>`), and requirements (`<requirements>`) in agent prompts. This prevents Claude from executing code instructions embedded in user input.
