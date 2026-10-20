---
name: Subagent Usage
category: templates
applies_when:
  - generating-coordinator
  - long-running-tasks
  - context-constrained
tags: [subagent, delegation, orchestration, task-isolation]
historical-source: reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/claude-4-best-practices.md
source: https://code.claude.com/docs/en/sub-agents
reviewed: 2026-10-06
---

# Subagent Usage

## When To Use

Use for a coordinator deciding whether independent specialist work improves the outcome. Select the actual runtime first. In Grok the model-facing tool is `spawn_subagent`; canonical metadata IDs differ. Follow `.grok/policies/context-isolation.md` and the live schema; custom role selection requires an advertised enum.

## Template

```text
Delegate a bounded task when it supplies independent evidence, useful parallel work,
or a distinct owned deliverable. Give it exact inputs, owned and forbidden paths,
acceptance criteria, and the report destination. Continue useful owned work while
it runs. Join when the next step depends on its result.
For tightly coupled or trivial work, use the existing owner without adding a worker.
```

## A-Team Adaptation

The coordinator keeps user dialogue, integration, and its explicitly assigned synthesis; it does not absorb specialist-owned files. Preserve the current topology policy and actual tool restrictions. Do not add a sub-coordinator. Grok specialists do not delegate under A-Team policy; source-backed `disallowedTools: [Task]` still needs installed enforcement evidence. Optional messaging is not a required workflow dependency.

If the host disallows delegation, execute locally within authorized scope and record the runtime limitation. Do not invent a successful dispatch or broaden permissions to create one.

## Examples

### Rejection Case

Reject spawning a worker to read one known line when the current owner can inspect it directly. Keep a fresh independent reviewer for a frozen batch when the acceptance contract requires one.

## Sources And Attribution

A-Team-authored template and ownership policy, informed by [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-10-06. Runtime capability and A-Team delegation policy are separate claims.

## Grok Adaptation

Maintained A-Team pattern adapted from `reference/platform-sources/.claude/skills/prompt-patterns/assets/templates/subagent-usage.md`. Anthropic links describe the pattern’s origin, not Grok runtime guarantees. Grok loading and lifecycle follow `.grok/policies/grok-agent-config.md` and `.grok/policies/context-isolation.md`; evaluate prompt effects on representative tasks.
