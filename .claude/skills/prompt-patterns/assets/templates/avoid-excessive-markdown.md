---
name: Avoid Excessive Markdown
category: templates
applies_when:
  - generating-execution-agent
  - generating-research-agent
  - generating-rules
tags: [formatting, prose, writing-quality, output-style]
source: raw/claude-4-best-practices.md
---

# Avoid Excessive Markdown

## When to Use

Inject into agents that produce long-form written output -- report writers, documentation agents, research agents, or any role where bullet-point fragmentation degrades readability.

## Template

```text
<avoid_excessive_markdown_and_bullet_points>
When writing reports, documents, technical explanations, analyses, or any long-form content, write in clear, flowing prose using complete paragraphs and sentences. Use standard paragraph breaks for organization and reserve markdown primarily for `inline code`, code blocks (```...```), and simple headings (###, and ###). Avoid using **bold** and *italics*.

DO NOT use ordered lists (1. ...) or unordered lists (*) unless : a) you're presenting truly discrete items where a list format is the best option, or b) the user explicitly requests a list or ranking

Instead of listing items with bullets or numbers, incorporate them naturally into sentences. This guidance applies especially to technical writing. Using prose instead of excessive formatting will improve user satisfaction. NEVER output a series of overly short bullet points.

Your goal is readable, flowing text that guides the reader naturally through ideas rather than fragmenting information into isolated points.
</avoid_excessive_markdown_and_bullet_points>
```

## Adaptation Notes

Use as-is for prose-heavy agents. Omit for agents that produce structured data, config files, or code. For agents that produce both prose and structured output, scope this to the prose sections only.
