---
name: Work Shape
description: Decide, for each user flow, whether to build one agent that loads skills or an agent group, and record the decision in docs/work-shape.json. Use before designing roles for a new team and when assessing the structure of an existing one.
---

# Work Shape

Decide the shape of the work before designing any role. A team is built for one or more user flows. A flow is what the user asks for and gets back, start to finish: a weekly newsletter issue, a reviewed pull request, a migrated database.

## The decision

The default is **one agent that loads skills** (`skill-workflow`). The steps, standards and judgement calls that specialist prompts would have held go into skills, and the agent loads each one when it reaches that part of the work. This is the right shape whenever the work shares one context and has one owner, even when it has several stages and draws on several professions.

Choose an **agent group** (`agent-group`) only when at least one of these is true of the flow and you can say what it is:

- **Parallel.** Branches that really run at the same time and do not need each other's intermediate results. Each can work in a context that is thrown away once it returns a compact result. Stages that run one after another are not parallel, however different they are.
- **Isolated check.** A check that is only worth something if the checker has not seen the author's reasoning: accepting generated code or configuration, checking facts nobody else will review, a security or compliance sign-off. A person who approves the output is already an isolated check. Do not add an agent to repeat their check unless the user wants one.
- **Overflow.** The material the flow must hold at once would not fit in one context, even with skills and references loaded only when needed. A long flow is not overflow when each stage can work from the files the stage before it wrote.

The default leans toward one agent for a reason. Every handoff returns a summary, and a summary drops detail the next stage needed. Every subagent is another model loop that adds latency and another prompt someone has to maintain. Stages that chain on each other's output, touch the same files, or are always called together do better in one context.

These look like triggers and are not: the stages sound like different jobs (researcher, writer, editor); there are many steps; the user called it a team; each deliverable "should have an owner".

## Sizing a group

The triggers decide which roles exist: one role per parallel branch, one fresh-context checker per isolated check, one role per overflow partition, and a coordinator that runs in the main session. Nothing else gets a role. There is no relay role and no reviewer whose only reason is that teams usually have one. What each role knows how to do still goes into skills.

A flow whose only trigger is an isolated check is two roles: the author and the checker.

## The record

Write `docs/work-shape.json` at the team root before role design. One entry per flow:

```json
{
  "flows": [
    {
      "name": "weekly-newsletter",
      "shape": "skill-workflow",
      "parallel": "",
      "isolated_check": "",
      "overflow": "",
      "why": "Research, draft and source check run in sequence in one context. The owner approves every draft."
    }
  ]
}
```

Each trigger field holds a sentence of evidence from this flow, or `""` when the trigger does not apply. `why` is one or two sentences a reader could disagree with. A team with any `agent-group` flow is built as a group, and its skill-workflow flows are run by the coordinator with skills.

`python3 scripts/check_work_shape.py <team-root>` checks the record against the rule and against the tree that was built. Both validators run it, so a group with no trigger, a skill workflow with one, or a tree that contradicts the record fails review. The record also selects what the team must ship; see `.claude/rules/output-structure.md`.

## When the user wants the other shape

If the user asks for a group and no trigger holds, say so and describe the skill workflow you would build instead. If they still want separate agents, ask what the separation should buy them. Independent review and parallel speed are triggers; record their answer as the evidence. If the user asks for one agent and a trigger holds, tell them what they give up: the check will be made by the author, or the branches will run one after another.

## Existing teams

Apply the same test to each flow of an existing team. A role with no trigger behind it is a candidate to fold into a skill. Fold one role at a time, run the team's own tasks before and after, and keep the role if the folded version does worse. Folding changes structure, so it goes through restructuring, not text-only optimization.

## Sources

[When to fold subagents into your main agent loop](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop) and [Safely scaling multi-agent teams](https://claude.dev/blog/safely-scaling-multi-agent-teams-with-fable-5-2/), checked 2026-11-26. The three triggers and the record format are A-Team policy.
