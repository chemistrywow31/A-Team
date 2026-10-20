---
name: Hybrid Strategy
category: context-strategies
applies_when:
  - generating-coordinator
  - generating-execution-agent
  - generating-coding-team
  - context-constrained
tags: [hybrid, pre-loaded, autonomous, exploration, CLAUDE-md]
source: raw/context-engineering-blog.md
---

# Hybrid Strategy

## Core Principle

Combine pre-loaded context (fast, reliable) with autonomous exploration (precise, current). Some information is stable enough to pre-load; other information must be discovered at runtime. The balance depends on content dynamism and task characteristics.

## Pattern

**Pre-loaded context (upfront, zero-latency):**
- CLAUDE.md — team norms, architectural decisions, workflow rules
- `@path/to/file` imports — stable reference documents
- System prompts — agent role definitions and behavioral constraints
- Project conventions that do not change between sessions

**Autonomous exploration (just-in-time, high-precision):**
- Glob and grep for navigating code — bypasses stale indexing and complex syntax trees
- File reads targeted by metadata signals (names, sizes, timestamps)
- Bash commands for data analysis without loading full objects
- Tool calls for current state (git status, test results, API responses)

**Claude Code exemplifies this:** CLAUDE.md files are naively dropped into context upfront. Glob and grep allow runtime navigation and just-in-time retrieval.

**Guidance for balance:**
- Less dynamic content (legal, finance, stable APIs): heavier pre-loading
- Highly dynamic content (active codebases, live data): heavier exploration
- As model capabilities improve, trend toward allowing models to explore more with less pre-curation
- "Do the simplest thing that works" remains the best starting advice

**Failure mode:** Without proper tools and heuristics, agents waste context through tool misuse, dead-ends, or failing to identify key information. Exploration requires guidance.

## A-Team Application

When generating teams: CLAUDE.md carries pre-loaded norms (team objectives, deployment mode, worklog structure, communication language). Rules with `paths` frontmatter load conditionally — a form of just-in-time pre-loading. When generating execution agents: equip with exploration tools and include heuristics for when to read versus when to search. When generating coding teams: pre-load architectural constraints and coding standards in CLAUDE.md, leave code-level context to glob/grep at runtime. Do not pre-load file-by-file codebase descriptions — let agents discover structure autonomously.
