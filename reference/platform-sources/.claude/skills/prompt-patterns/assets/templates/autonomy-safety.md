---
name: Autonomy and Safety
category: templates
applies_when:
  - generating-coordinator
  - generating-execution-agent
  - generating-coding-team
  - generating-rules
tags: [safety, reversibility, destructive-actions, confirmation]
historical-source: raw/claude-4-best-practices.md
source: https://code.claude.com/docs/en/permissions
reviewed: 2026-10-06
---

# Autonomy And Safety

## When To Use

Use when a role performs mutations or outward actions. Preserve the actual task authorization and runtime permission boundary.

## Template

```text
Carry forward authorization already supplied for this operation and target.
Complete scoped reversible work and prepare concrete reviewable results.
Before an external or irreversible action not covered by that authorization, obtain
the missing decision. Explicit instructions are required to send messages to others.
Assess impact and reversibility for the actual action; do not repeat approval simply
because a phase changed or an action belongs to a broad category.
Respect host permissions. Do not discard unfamiliar files, revert another writer's
changes, or bypass checks to get past an obstacle.
```

## Examples

- Authorized: the user requests edits to a named skill family; proceed with those reversible edits and verify them.
- Defer: a repository maintenance task exposes a useful email update, but no instruction authorizes sending it. Prepare the relevant result and request that authorization before sending.
- Defer: an authorized repair would also delete an unrelated directory. Continue the covered repair and obtain the missing scope decision for deletion.

## Adaptation Notes

For unattended workflows, use explicitly authorized operations and native permission controls. The absence of a person does not grant new authority. A read-only reviewer usually needs the ownership/evidence contract rather than this execution template.

## Sources And Attribution

This is an A-Team adaptation of the historical-source pattern, grounded in the current user authorization and execution-contract precedence rules. [Claude Code permissions](https://code.claude.com/docs/en/permissions), checked 2026-10-06 in the native research, describes runtime permission controls; it does not grant task authorization.
