---
name: Writing Quality Standard
description: The standard every generated prompt, skill, rule and entry document is written and reviewed against
paths:
  - "teams/**"
---

# Writing Quality Standard

## Applicability

- Applies to: `agent-writer`, `skill-writer`, `rule-writer`, `prompt-optimizer`, and the independent reviewer
- Scope: files a Claude model will read. Codex-target files follow `.codex/rules/writing-quality-standard.md`.

## Rule Content

Write for a capable reader who has the repository open. Say what the work is for, what is particular to this team, and where the traps are. Leave the rest to the reader's judgement. Source: [the new rules of context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/), checked 2026-11-26.

### Six Checks

Read each file against these. They are a rubric for judgement, not a form to fill in.

1. **Judgement before absolutes.** State the goal and the reason and let the reader apply them: "match the comment density of the surrounding code", not "never write comments". Keep an absolute only where a mistake is costly and cannot be undone, such as secrets, destructive commands, publishing and spending, and give the reason in the same sentence. Emphasis by capitals or repetition adds nothing.
2. **Interfaces before examples.** Describe the contract directly: named inputs and outputs, a file format, a small set of statuses, tool parameters that say what they mean. Add an example only when it shows something the contract cannot, and make it clearly one case among many. A worked example becomes the shape of every answer.
3. **Loaded when needed.** An entry document or an agent prompt holds what every run needs. Procedures for particular moments, such as review, verification, release, recovery or a rare format, are skills or reference files named at the point of use. A long skill is a short `SKILL.md` plus files under `references/`.
4. **Said once.** Each instruction has one home, and other files point to it. How to use a tool or a skill belongs in its own description, not in every agent that uses it.
5. **A short entry document.** `CLAUDE.md` says what the project is for and the gotchas the tree does not show. It has no directory listing, no role table and no copies of rules.
6. **References before prose specs.** When a standard can be a test, a script, a schema, a sample file or a rubric, ship that and point to it.

### Do Not Carry A-Team's Contract Into A Team

A-Team's execution contract, worklog triad, section floors and `JUDGMENT.md` describe how A-Team builds teams. A generated team gets its own files, sized by its work-shape profile (`.claude/rules/output-structure.md`): a group writes its own short handoff contract, and a rule exists only because one of the team's flows needs it.

### Signs A File Needs Another Pass

- The same instruction appears in two files, or twice in one.
- Two instructions conflict, or an absolute has an obvious case where it is wrong.
- The text repeats what the tree, the code or a tool description already shows.
- A section is there because a template had it, and nothing in it is specific to this role.
- An example is longer than the instruction it illustrates.
- Always-loaded text describes something that rarely happens.

### Size

The 300, 200 and 100 line marks for agents, skills and rules are a prompt to look again, not a target. The validator reports `REVIEW_REQUIRED` above them and the independent reviewer decides. A short file that leaves out a real gotcha is worse than a longer one that has it. A long file that repeats itself is worse than both.

### A Template Outranks Its Own Prose

When a file has both a policy and a template the reader copies, the template wins. After changing a policy, update every template, skeleton and example that instantiates it. `scripts/validate-team.sh` cannot see prose contradictions.

## Violation Determination

- A generated file copies A-Team's rule pack or section skeleton when no flow of the team needs it -> Violation
- An instruction has more than one home, or two instructions in one team conflict -> Violation
- An absolute has no stated reason, or plainly covers a case where it is wrong -> Violation
- A template or example contradicts a policy in the same file or in the rule it implements -> Violation
- A file over its size mark is accepted without an independent look -> Violation

## Exceptions

- Vendored external skills keep their upstream text.
- Safety rules stay absolute: no secrets in files, no merge, push, deploy or deletion without an explicit yes.
