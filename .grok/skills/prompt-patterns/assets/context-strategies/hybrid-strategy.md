---
name: Hybrid Strategy
category: context-strategies
applies_when:
  - generating-coordinator
  - generating-execution-agent
  - generating-coding-team
  - context-constrained
tags: [hybrid, pre-loaded, autonomous, exploration, AGENTS-md]
source: reference/platform-sources/.claude/skills/prompt-patterns/assets/raw/context-engineering-blog.md
---

# Hybrid Strategy

## Core Principle

Combine pre-loaded context (fast, reliable) with autonomous exploration (precise, current). Some information is stable enough to pre-load; other information must be discovered at runtime. The balance depends on content dynamism and task characteristics.

## Pattern

**Pre-loaded context (upfront, zero-latency):**
- AGENTS.md — team norms, architectural decisions, workflow rules
- `.grok/rules/core.md` — shared bootstrap with exact on-demand policy paths
- System prompts — agent role definitions and behavioral constraints
- Project conventions that do not change between sessions

**Autonomous exploration (just-in-time, high-precision):**
- Glob and grep for navigating code — bypasses stale indexing and complex syntax trees
- File reads targeted by metadata signals (names, sizes, timestamps)
- Bash commands for data analysis without loading full objects
- Tool calls for current state (git status, test results, API responses)

**Grok-native application:** trusted root AGENTS.md and flat `.grok/rules/*.md` are discovered initially. Native file reads, grep and directory listing provide just-in-time retrieval; inspect source identities to establish what was actually loaded.

**Guidance for balance:**
- Verified stable project conventions: selective pre-loading; time-sensitive legal, financial or API claims still require current evidence
- Highly dynamic content (active codebases, live data): heavier exploration
- As model capabilities improve, trend toward allowing models to explore more with less pre-curation
- "Do the simplest thing that works" remains the best starting advice

**Failure mode:** Without proper tools and heuristics, agents waste context through tool misuse, dead-ends, or failing to identify key information. Exploration requires guidance.

## A-Team Application

When generating teams: AGENTS.md carries pre-loaded norms (team objectives, deployment mode, worklog structure, communication language). Keep the short automatic core separate from full `.grok/policies/` files, which roles read explicitly as needed. When generating execution agents: equip with exploration tools and include heuristics for when to read versus when to search. When generating coding teams: pre-load architectural constraints and coding standards in AGENTS.md, leave code-level context to glob/grep at runtime. Do not pre-load file-by-file codebase descriptions — let agents discover structure autonomously.

## Grok Adaptation

Maintained A-Team pattern adapted from `reference/platform-sources/.claude/skills/prompt-patterns/assets/context-strategies/hybrid-strategy.md`. Anthropic links describe the pattern’s origin, not Grok runtime guarantees. Grok loading and lifecycle follow `.grok/policies/grok-agent-config.md` and `.grok/policies/context-isolation.md`; evaluate prompt effects on representative tasks.
