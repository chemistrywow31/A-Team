---
name: Structured Notes
category: context-strategies
applies_when:
  - long-running-tasks
  - generating-coordinator
  - generating-execution-agent
  - context-constrained
tags: [memory, note-taking, persistence, state-tracking]
source: raw/context-engineering-blog.md
---

# Structured Notes

## Core Principle

Agents regularly write notes persisted to memory outside the context window, then pull them back when needed. This simple pattern enables coherence across thousands of steps and context resets. After a reset, agents read their own notes and continue multi-hour sequences without loss.

## Pattern

**Evidence — Claude playing Pokemon:** The agent maintained precise tallies across thousands of game steps ("for the last 1,234 steps I've been training my Pokemon in Route 1, Pikachu has gained 8 levels toward the target of 10"). Without prompting about memory structure, it developed maps of explored regions, remembered unlocked achievements, and maintained strategic notes about combat effectiveness.

**Implementation forms:**
- `NOTES.md` or `progress.txt` — freeform progress tracking
- `tests.json` or structured state files — schema-based tracking for test results, task status
- To-do lists — track pending work across context windows
- Git commits — log of what was done, restorable checkpoints

**State management best practices:**
- Use structured formats (JSON) for data with schema requirements (test results, task status)
- Use unstructured text for general progress notes and context
- Use git for state tracking — provides history log and restorable checkpoints
- Emphasize incremental progress: track what was done and what comes next

## A-Team Application

When generating any team: the worklog system (`.worklog/` with references.md, findings.md, decisions.md) is A-Team's implementation of structured notes. Ensure every generated team includes the worklog rule and context management rule. When generating coordinators: instruct them to write interim summaries to the worklog after every 5 sequential task dispatches. When generating execution agents: require them to persist critical state to worklog before context limits approach. For coding teams with long tasks: include a progress-tracking file pattern (e.g., `progress.txt`) alongside the worklog.
