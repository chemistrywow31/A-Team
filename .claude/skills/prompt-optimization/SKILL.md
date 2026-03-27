---
name: Prompt Optimization
description: Provide systematic prompt optimization methodology to improve instruction quality while preserving original characteristics
---

# Prompt Optimization

## Description

Provide systematic prompt optimization methodology, including optimization principles, common problem diagnosis, rewriting techniques, and quality checklists. Enable AI agent prompts to achieve optimal instruction effectiveness while preserving original role definitions.

## Belongs To

This skill belongs exclusively to `agents/optimization/prompt-optimizer.md`

## Optimization Principles

### Principle 1: Fidelity

Optimize the expression method, not the content essence.

**Checklist:**
- Is the role's core identity unchanged?
- Is the responsibility scope exactly the same?
- Are collaboration relationships maintained?
- Are boundary definitions consistent?

### Principle 2: Specificity

Transform abstract descriptions into actionable specific instructions.

**Rewriting formula:**
```
Abstract description → Specific action + Verifiable result
```

### Principle 3: Conciseness

Remove words that don't add information value.

**Checklist:**
- Are there sentences that repeat the same meaning?
- Are there modifiers that can be removed?
- Is there unnecessary explanatory text?

### Principle 4: Directiveness

Use imperative sentences, directly tell the AI what to do.

### Principle 5: Computational Offloading

Extract static, repetitive, or computable content from prompts into executable scripts. Replace verbose data with compact script-generated output.

## Common Problems and Optimization Patterns

### Problem 1: Vague Verbs

**Symptom:** Using verbs like "handle", "manage", "be responsible for" that have no specific behavioral direction

**Before:**
> Responsible for handling user feedback

**After:**
> Collect user feedback, classify into bug/feature/question categories, transfer bugs to developers, record features in backlog, respond directly to questions

### Problem 2: Implicit Assumptions

**Symptom:** Assuming readers know certain unstated information

**Before:**
> Review according to standard process

**After:**
> Review using the following process: 1. Check format completeness 2. Verify reference paths 3. Confirm terminology consistency

### Problem 3: Redundant Modifiers and Passive Voice

**Before:** "Carefully and thoroughly check every detail to ensure high-quality output" / "Tasks will be assigned to the corresponding executor"

**After:** "Check each field against template requirements" / "Assign tasks to the corresponding executor"

### Problem 5: Vague Conditions

**Symptom:** Using conditions that cannot be evaluated like "if needed", "when appropriate"

**Before:**
> Perform additional validation if needed

**After:**
> When input data comes from external sources, execute format validation

### Problem 6: Repeated Definitions and Over-explanation

**Before:** "You are a content reviewer. Your role is to review content. You are responsible for ensuring content quality." / "JSON is a data format that uses key-value pairs. You need to output results in JSON format."

**After:** "You are a content reviewer, responsible for checking and flagging non-compliant content according to quality standards." / "Output format: JSON"

### Problem 8: Computable Content Embedded in Prompt

**Symptom:** Prompt contains data tables, repetitive patterns, or reference lists exceeding 200 tokens that a script can generate deterministically

**Before (≈40,000 tokens):**
> Full API specification listing 127 endpoints with parameters, validation rules, response schemas, and examples... [thousands of lines of structured data]

**After (≈1,500 tokens):**
> `python extract_api_spec.py --summary` output: 127 endpoints across 5 categories. Per entry: method, path, required params, response type.

### Problem 9-12: Claude 4.6 Anti-patterns

See `rules/prompt-engineering-patterns.md` for full rationale. Quick reference:

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 9 | Instructional-only constraint | "Do not guess when you don't know" | Add `## Uncertainty Protocol` section with `INSUFFICIENT_DATA` escape hatch |
| 10 | Urgency over-triggering | "You MUST ALWAYS use the search tool" | "Use the search tool when the question requires information not in context" |
| 11 | Missing escape hatch | "Produce a technical specification" | Add "When requirements are insufficient, report `INSUFFICIENT_DATA`" |
| 12 | Exploration trap | "If in doubt, research further" | "Choose an approach and commit. Revisit only when new evidence contradicts" |

## Optimization Checklist

For each .md file, check sequentially:

### Structural Level
- [ ] YAML frontmatter complete (name, description, model)
- [ ] Only one h1 heading
- [ ] Section order matches template; reference paths exist and are correct

### Language Level
- [ ] Uses imperative sentences ("You must" not "should")
- [ ] No prohibited vague words (try to, appropriately, reasonably, as needed)
- [ ] Verbs are specific and actionable
- [ ] No passive voice or redundant modifiers

### Content Level
- [ ] Role identity is clear (one paragraph explaining who they are)
- [ ] Responsibilities are specific and actionable (each has a clear action)
- [ ] Boundaries are explicit (lists things not done)
- [ ] No repeated definitions or implicit assumptions
- [ ] No computable content that a script can generate (data tables, pattern expansions, file analysis)

### Claude 4.6 Optimization Level
- [ ] No urgency language (`CRITICAL`, `MUST`, `ALWAYS`, `NEVER`) for non-safety preferences
- [ ] Behavioral constraints use structural solutions (sections, templates) not just instructions
- [ ] Agent has explicit escape hatch for insufficient data scenarios
- [ ] No open-ended exploration triggers ("if in doubt, investigate further")
- [ ] Examples cover normal, edge, and rejection cases (not just happy path)
- [ ] Element ordering: identity/context first, instructions/output format last

### Consistency Level
- [ ] Terminology is unified within the file
- [ ] Terminology is consistent with other files
- [ ] Collaboration relationships are bidirectionally symmetric

## Optimization Priority

When time is limited, process in this priority order:

1. **Fix errors**: Reference path errors, format non-compliance
2. **Extract computables**: Offload data tables, lists, and repetitive content to scripts
3. **Eliminate ambiguity**: Vague words, implicit assumptions
4. **Strengthen and refine**: Passive→active, abstract→specific, remove redundancy

## Example

### Input

```markdown
## Responsibilities

This role is mainly responsible for managing the team's daily work. They handle various task assignments and ensure work can proceed smoothly. If problems are encountered, they also coordinate appropriately.
```

### Output

```markdown
## Responsibilities

1. Receive upstream tasks and decompose into assignable subtasks
2. Assign subtasks based on each agent's responsibility scope
3. Track completion status of each subtask
4. When dependency conflicts exist between subtasks, adjust execution order or reassign
5. Aggregate all subtask outputs, verify completeness, and deliver downstream
```

### Optimization Explanation

| Original Problem | Optimization Method |
|-----------------|---------------------|
| "mainly responsible for managing" | Remove redundancy, list specific actions |
| "handle various task assignments" | Concretize into "receive→decompose→assign" |
| "coordinate appropriately" | Replace vague word with specific: "adjust order or reassign" |
