---
name: Delivery Management
description: Enforce systematic delivery information tracking across sprints to enable team continuity and handover
---

# Delivery Management

## Applicability

- Applies to: All agents (coordinator and all team members)

## Rule Content

### Delivery Directory Structure

Every team must maintain a `.deliver/` directory at the project root with sprint-based organization:

```
.deliver/
├── sprint-001/
│   ├── deliverables.md      # List of completed work items
│   ├── handover-notes.md    # Context for next team/sprint (optional)
│   ├── retro.md             # Retrospective report (auto-generated)
│   └── artifacts/           # Half-finished work, drafts, WIP files
├── sprint-002/
│   └── ...
└── current -> sprint-00X    # Symlink to active sprint
```

### Sprint Lifecycle

#### At Sprint Start

Coordinator must:
1. Create new sprint directory: `.deliver/sprint-{number}/`
2. Check previous sprint's `handover-notes.md` for unfinished work
3. Read previous sprint's `retro.md` for lessons learned
4. Update `current` symlink to new sprint directory

#### During Sprint

All members must:
1. Update `.deliver/current/deliverables.md` when completing tasks
2. Store half-finished work in `.deliver/current/artifacts/` with clear naming
3. Add comments in artifacts explaining continuation steps

#### At Sprint End

Coordinator must:
1. Verify all deliverables are documented in `deliverables.md`
2. If unfinished work exists, write `.deliver/current/handover-notes.md`
3. Trigger retrospective (generates `retro.md` automatically)

### Deliverables.md Format

Use this minimal structure:

```markdown
# Sprint {number} Deliverables

## Completed
- [Task ID] Brief description (Status: ✅ Delivered)
- [Task ID] Brief description (Status: ✅ Delivered)

## In Progress (hand over to next sprint)
- [Task ID] Brief description (Status: 🚧 60% done, see artifacts/task-123/)

## Blocked
- [Task ID] Brief description (Status: ⛔ Blocked by: reason)
```

### Handover Notes Requirements

Write `handover-notes.md` only when:
- Unfinished work exists (work > 0% but < 100% completion)
- Critical context must transfer to next sprint
- External dependencies changed mid-sprint

Structure:

```markdown
# Handover Notes - Sprint {number}

## Unfinished Work
- **[Task ID]**: What's done, what remains, where to continue

## Critical Context
- Key decisions made this sprint
- External blockers or dependencies

## Next Sprint Priorities
- Must-do items to continue momentum
```

### Artifact Naming Convention

Files in `artifacts/` must follow:

```
artifacts/
├── task-123-component-redesign-draft.md
├── task-456-api-spec-v2.sketch
└── wip-team-retro-template.md
```

Format: `{task-id}-{description}-{status}.{ext}` or `wip-{description}.{ext}`

## Violation Determination

- Sprint starts without checking `.deliver/sprint-{prev}/handover-notes.md` → Violation
- Sprint ends without `deliverables.md` updated → Violation
- Unfinished work exists but no `handover-notes.md` created → Violation
- `artifacts/` contains files without clear naming or continuation instructions → Violation
- Team restarts and cannot locate previous work due to missing delivery info → Violation

## Exceptions

- For short-lived teams (single-task, < 2 hours), `.deliver/` can be skipped if coordinator confirms no handover needed
