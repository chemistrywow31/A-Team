---
name: Subagent Usage
category: templates
applies_when:
  - generating-coordinator
  - long-running-tasks
  - context-constrained
tags: [subagent, delegation, orchestration, task-isolation]
historical-source: raw/claude-4-best-practices.md
source: https://code.claude.com/docs/en/sub-agents
reviewed: 2026-10-06
---

# Subagent Usage

## When To Use

Use for a coordinator deciding whether independent specialist work improves the outcome. Select the actual runtime first. In Claude subagent mode the tool is `Agent`; `Task` is a compatibility alias. Native Agent Teams is a distinct mode with its own lifecycle and capability checks.

## Template

```text
Delegate a bounded task when it supplies independent evidence, useful parallel work,
or a distinct owned deliverable. Give it exact inputs, owned and forbidden paths,
acceptance criteria, and the report destination. Continue useful owned work while
it runs. Join when the next step depends on its result.
For tightly coupled or trivial work, use the existing owner without adding a worker.
```

## A-Team Adaptation

The coordinator keeps user dialogue, integration, and its explicitly assigned synthesis; it does not absorb specialist-owned files. Preserve the current topology policy and actual tool restrictions. Do not add a sub-coordinator. Claude specialists do not delegate under A-Team policy; a Codex projection uses its inventoried native lifecycle and bounded-helper rule instead.

If the host disallows delegation, execute locally within authorized scope and record the runtime limitation. Do not invent a successful dispatch or broaden permissions to create one.

## Examples

### Rejection Case

Reject spawning a worker to read one known line when the current owner can inspect it directly. Keep a fresh independent reviewer for a frozen batch when the acceptance contract requires one.

## Sources And Attribution

A-Team-authored template and ownership policy, informed by [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-10-06. Runtime capability and A-Team delegation policy are separate claims.
