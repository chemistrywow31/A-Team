---
name: Compaction
category: context-strategies
applies_when:
  - long-running-tasks
  - context-constrained
  - generating-coordinator
tags: [compaction, summarization, context-window, long-horizon]
source: raw/context-engineering-blog.md
---

# Compaction

## Core Principle

Compaction summarizes a conversation nearing the context limit and reinitializes a new context window with that summary. It is the first lever for maintaining coherence in long-running tasks. The art lies in selecting what to keep versus discard — overly aggressive compaction risks losing subtle context whose importance only surfaces later.

## Pattern

**What to preserve:** Architectural decisions, unresolved bugs, implementation details, the full list of modified files, test commands, and active goals.

**What to discard:** Old tool call/result pairs are the lowest-risk targets. Once a tool has been called deep in message history, raw results are rarely needed again. Redundant messages and superseded plans are next.

**Tuning approach:**
1. Maximize recall first — capture all potentially relevant information
2. Iterate to improve precision by eliminating superfluous content
3. Test compaction prompts on complex agent traces, not simple ones

**Claude Code implementation:** Pass message history to the model for summarization. Continue with compressed context plus the five most recently accessed files.

**User control:** `/compact <instructions>` allows focused compaction (e.g., `/compact Focus on the API changes`). CLAUDE.md can include persistent compaction guidance: "When compacting, always preserve the full list of modified files and any test commands."

## A-Team Application

When generating coordinators: include compaction guidance in the coordinator's CLAUDE.md section — specify what categories of information must survive compaction (decision rationale, worklog paths, active phase state). When generating long-running execution agents: add a rule that agents must write critical state to the worklog before compaction triggers, so nothing depends solely on in-context memory. Generated teams with long-horizon workflows must include compaction instructions in their CLAUDE.md.
