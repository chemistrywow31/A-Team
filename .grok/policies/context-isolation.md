---
name: Context Isolation
description: Choose inline skills or explicit native child dispatch with evidence-backed context and loading boundaries
---

# Context Isolation

## Applicability

- Applies to coordinators, skill writers, agent writers, and independent reviewers.

## Rule Content

### Choose The Execution Mode

| Mode | Use | Context consequence |
| --- | --- | --- |
| Inline skill | Coordinator entry, small deterministic work, work needing current user context | Skill instructions and intermediate output remain in the current session |
| New native child | Bounded research, exploration, checks, independent acceptance | Pinned source creates a fresh child when `resume_from` is absent; return file paths and summary |
| Resumed completed child | Correction or continuation of the same logical task | `resume_from` reuses that child's transcript; not independent acceptance |

The coordinator alone starts children through advertised `spawn_subagent`. A skill can instruct the main-session coordinator to delegate a standalone task; it cannot give a specialist permission to delegate. No automatic skill-fork field is part of this branch's native contract.

### Isolate Noisy Independent Work

Use a new child when all are true: the task produces substantial intermediate research or logs; the parent needs only the result; the task can be expressed with standalone inputs and does not depend on uncaptured conversation history. Examples include literature scans, large code exploration, verbose test runs, and multi-source gathering.

Run inline when the task is small, needs current conversation context, or when dispatch overhead exceeds its work. Store large logs and evidence in assigned files regardless of mode.

### Keep Entry Skills In Main

Identify an entry by its declared coordinator-workflow purpose, not its folder name or a metadata flag. It makes the current session read and adopt the coordinator playbook and keeps user communication there. Do not spawn or resume the coordinator, and do not isolate the entire workflow into a child.

### Load Skills Explicitly

Use `.grok/skills/{name}/SKILL.md`. Agent `skills` names preloads; `discoverSkills` controls cwd skill discovery; `inheritSkills` affects a child. These source-backed fields need installed-session evidence for effective behavior. Name exact required skill reads in dispatches instead of assuming a parent's loaded skills will appear.

Keep `agentsMd: true` so native project instructions and `.grok/rules/core.md` participate in startup discovery. Setting it false skips all initial instruction discovery; do not use it as a shortcut to make a reviewer fresh. Freshness means no producer conversation, not removal of the team's governing instructions.

### Fresh Acceptance Contract

For EC-3 dispatch a new reviewer with only frozen artifact paths and acceptance criteria in `prompt`, without `resume_from`. Native source constructs an ordinary model-issued child with no forked conversation and returns a new empty conversation at bootstrap. This supports the design; installed end-to-end behavior remains a runtime gate. Do not invent a model-facing history parameter.

`isolation: worktree` concerns filesystem isolation when available; it is not proof of conversation isolation or fresh review. `grok inspect --json` observes discovery and typed loading, not the child's effective prompt, toolset, or fresh context. Record those as UNVERIFIED until bounded session evidence exists.

### Rejection Example

A research skill asks a direct specialist to launch a helper and claims a skill metadata field automatically creates a clean context. Reject both claims. Root may dispatch the bounded research directly, with exact inputs and report paths, under its advertised native schema.

## Violation Determination

- Entry skill spawns the coordinator or specialist dispatches a helper -> Violation.
- A resumed transcript or filesystem worktree is called fresh independent context -> Violation.
- Skill metadata is treated as an automatic context or permission control without native evidence -> Violation.
- Required skills are assumed inherited, or `agentsMd: false` silently removes bootstrap policy -> Violation.
- Inspect discovery is reported as effective prompt/tool/context proof -> Violation.

## Exceptions

During debugging, root may run normally isolated work inline to inspect intermediate output. It must still use a fresh reviewer for independent acceptance.

Tradeoff: Child dispatch costs an invocation and explicit input preparation. Use inline execution when those costs exceed the context benefit; keep review independence separate from that convenience decision.
