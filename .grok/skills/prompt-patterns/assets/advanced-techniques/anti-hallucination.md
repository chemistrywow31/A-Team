---
name: Anti-Hallucination
category: advanced-techniques
applies_when:
  - generating-research-agent
  - generating-review-agent
  - writing-agent-prompts
  - writing-skill-prompts
tags: [hallucination, evidence-first, grounding, status-routing, uncertainty]
source: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
historical-source: reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/tutorial-advanced-techniques.md
reviewed: 2026-10-06
---

# Anti-Hallucination

## Ground Claims And Expose Gaps

Match claims to evidence the agent actually inspected. Separate source facts, justified inferences, and unknowns. Missing evidence calls for a named gap or a targeted check; absolute certainty is not a prerequisite for every useful answer.

## Evidence Pattern

When answering from documents, collect relevant passages or precise references before drawing conclusions. Expose only the evidence needed to check the result; a source extract is an observable artifact, not a private scratchpad.

```xml
<document id="release-notes">
<source>release-notes.md, section Storage</source>
<document_content>Version 3 supports reading version 2 records.</document_content>
</document>
<question>Does version 3 read version 1 records?</question>
<output>
Cite the relevant passage, answer only to its scope, and name missing coverage.
</output>
```

Expected result: the supplied passage establishes version 2 read compatibility. It does not establish version 1 support; request or inspect version 1 compatibility evidence if that answer is required. Do not convert absence of evidence into either a success or a failure claim.

Use short quotations when exact wording matters; use file:line, section, or source links when they provide sufficient grounding. Preserve uncertainty when sources conflict or dates differ. For code claims, inspect the actual implementation and relevant execution evidence.

## A-Team Application

- Keep the references → findings → decisions chain traceable. Cite evidence for each acceptance verdict.
- Use only EC-1 statuses: `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`.
- Missing required context uses `STATUS: NEEDS_CONTEXT` and `INSUFFICIENT_DATA: {missing items}` in `CONCLUSIONS`. Partial verifiable results may use `DONE_WITH_CONCERNS` when the role contract permits; hard blockers use `BLOCKED`.
- Do not map every tool error to a final blocker; apply the existing role uncertainty and bounded retry contract.
- Label hypotheses as hypotheses. Do not demand a scratchpad transcript from every document-processing skill.

## Examples

### Rejection Case

Reject an overall PASS based solely on a successful parser when the criterion requires live tool readiness. Cite the parser result as static evidence, name the unperformed live check, and leave that criterion unverified.

## Sources And Attribution

A-Team-authored example, report routing, and evidence contract. The grounding/uncertainty approach is informed by [Anthropic hallucination guidance](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations), checked 2026-10-06. Historical tutorial extracts remain provenance, not current output mandates.

## Grok Adaptation

Maintained A-Team pattern adapted from `reference/platform-sources/.claude/skills/prompt-patterns/assets/advanced-techniques/anti-hallucination.md`. Anthropic links describe the pattern’s origin, not Grok runtime guarantees. Grok loading and lifecycle follow `.grok/policies/grok-agent-config.md` and `.grok/policies/context-isolation.md`; evaluate prompt effects on representative tasks.
