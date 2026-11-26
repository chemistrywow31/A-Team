---
name: Prompt Optimization
description: Rewrite an existing team's prompts, skills and documents to the writing standard without changing what the team does. Use for wording-only refinement of a runnable surface.
---

# Prompt Optimization

## What this lane is

The optimization lane rewrites text inside assigned files so the team behaves the same with less to read and nothing that pulls against itself. The standard is `.claude/rules/writing-quality-standard.md`. Read it first; this skill adds only what is particular to rewriting an existing team.

It stays wording-only. Adding or removing a file, a role, a rule, a hook, or changing topology, runtime or config, ownership, mapping, canonical authority, stamps, or a surface's runnable state is restructuring. Hand those to `team-restructuring-master` through the coordinator, including folding a role into a skill.

## How to work

1. For a named team, classify it first: surfaces, stamp, canonical authority, mapping. For A-Team capability maintenance, stay inside the assigned A-Team paths.
2. Read the whole surface before editing one file. Most of what needs fixing is between files: the same instruction in three places, or a skill that says the opposite of the entry document.
3. For each passage ask whether the team would behave differently without it. Typical cuts in a team built by an older generator:
   - an instruction repeated across agents, which gets one home and pointers
   - a ban that is wrong in some ordinary case, rewritten as the goal and its reason
   - sections that exist because a template had them, holding nothing specific to the role
   - a worked example that every output now copies, replaced by the contract it was illustrating
   - entry-document text that restates the tree, the role list, or rule content
4. Keep exactly: safety rules, explicit model and effort settings, paths, runtime keys, acceptance criteria, and any gotcha that records something the team learned the hard way.
5. Edit a canonical source before its projections, and keep the selected runtime's own vocabulary.
6. Report what you removed and why, and what you routed to restructuring. A fresh-context verifier accepts the result; you do not.

A shorter file is not the goal and neither is a longer one. The test is whether a first-time reader does the right thing.

## Sources

[The new rules of context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/), checked 2026-11-26, for Claude targets. The lane boundary is A-Team policy. Codex targets use their own inventoried guidance.
