---
name: Multi-Window Workflow
category: context-strategies
applies_when:
  - long-running-tasks
  - generating-coding-team
  - context-constrained
tags: [multi-window, state-management, fresh-context, git, setup-scripts]
source: raw/context-engineering-blog.md
---

# Multi-Window Workflow

## Core Principle

Tasks spanning multiple context windows require deliberate state management. The first window sets up the framework and verification infrastructure; subsequent windows iterate against that framework. Claude's latest models are effective at discovering state from the local filesystem, making fresh context windows viable alternatives to compaction.

## Pattern

**First window — setup:**
- Write tests in structured format (e.g., `tests.json`) before starting implementation
- Create setup scripts (`init.sh`) to start servers, run test suites, run linters
- Establish the todo list and progress tracking file
- Make initial git commit as a checkpoint

**Subsequent windows — iteration:**
- Start by reading `progress.txt`, `tests.json`, and git logs
- Run the setup script to restore working state
- Pick up from the last completed item on the todo list
- Commit incrementally for restorable checkpoints

**Fresh context vs compaction tradeoff:**
- Fresh context: No accumulated noise; model rediscovers state from filesystem and git. Better when task state is well-externalized to files.
- Compaction: Preserves conversational nuance and decision rationale. Better when implicit context matters.

**State files to maintain:**
- `tests.json` — structured test status (passing/failing/not_started)
- `progress.txt` — freeform session notes ("Fixed X, next: investigate Y")
- Git log — history of changes and restorable checkpoints
- `init.sh` — repeatable environment setup

**Key rule:** "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

## A-Team Application

When generating coding teams with long-horizon tasks: include a rule requiring agents to externalize state to structured files before context exhaustion. When generating coordinators: add guidance to prefer fresh context windows when worklog and git contain full state, and compaction when decision nuance matters. Include `init.sh` creation as a first-phase task in generated coding team workflows. The worklog system already provides the structured notes infrastructure — ensure generated teams connect their progress tracking to both worklog and git.
