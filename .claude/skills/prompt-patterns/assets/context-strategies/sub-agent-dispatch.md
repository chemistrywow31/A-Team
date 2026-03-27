---
name: Sub-Agent Dispatch
category: context-strategies
applies_when:
  - generating-coordinator
  - generating-research-agent
  - context-constrained
  - long-running-tasks
tags: [sub-agents, context-isolation, delegation, multi-agent]
source: raw/context-engineering-blog.md
---

# Sub-Agent Dispatch

## Core Principle

Sub-agent architectures solve context pollution by isolating deep work into separate context windows. The main agent coordinates with high-level plans while sub-agents explore extensively — potentially consuming tens of thousands of tokens — but return only condensed summaries (1,000-2,000 tokens). Research shows substantial improvement over single-agent systems on complex tasks.

## Pattern

**When multi-agent beats single-agent:**
- Investigation tasks that read many files (codebase exploration, research)
- Parallel independent workstreams that do not share state
- Verification/review work (fresh context avoids bias toward own output)
- Any task where exploration tokens would pollute the coordinator's window

**When single-agent is better:**
- Simple sequential operations and single-file edits
- Tasks requiring shared state across steps
- Quick lookups where a direct grep call suffices

**Guard against overuse:** Opus-class models have a strong predilection for spawning sub-agents even when unnecessary. Add explicit guidance: "For simple tasks, work directly rather than delegating."

**Writer/Reviewer pattern:** Session A writes code, Session B reviews with fresh context (no bias from authorship). Feedback flows back to Session A for fixes.

## A-Team Application

When generating coordinators: enforce that all execution goes through Task dispatch (per coordinator-mandate.md). The coordinator accumulates only structured summaries. When generating research agents: design them to return findings in the structured summary format (status + key outcomes + worklog path), never raw dumps. When generating review agents: specify they run in isolated context to ensure unbiased assessment. Include sub-agent usage guidance in generated CLAUDE.md to prevent over-delegation on simple tasks.
