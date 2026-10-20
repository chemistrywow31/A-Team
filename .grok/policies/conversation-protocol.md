---
name: Conversation Protocol
description: Confirm material team requirements while continuing work within existing user authorization
---

# Conversation Protocol

## Applicability

- Applies to: `team-architect`, `requirements-analyst`, `prompt-optimizer`, `team-restructuring-master`

## Rule Content

### Communicate In The User's Language

Match the user's language. Explain unfamiliar technical terms when first used.

### Confirm New-Team Requirements

Before Planning or Generation of a new team, confirm:

1. Specific objectives and scope.
2. Workflow stages from input to final output.
3. Candidate role coverage for each stage.
4. Requested format: `grok-native` is this branch's executable delivery; `let A-Team decide` delegates the choice within available verified formats. Record a request for another runtime as an explicit conversion/handoff need, not a claim that its delivery is supported here.
5. One canonical authority, surface activation state, and mapping-retention need.
6. The requirements summary is accurate.

Use prior user statements and explicit delegation of routine choices as confirmation where they supply the decision. State delegated choices in the summary; do not interpret silence as approval or infer ambiguous canonical authority. Ask early for missing format or authority decisions.

### Continue Within Existing Scope

First select A-Team capability maintenance, one named-target maintenance, or explicitly requested fleet work. Capability maintenance alone does not authorize a target inventory, downstream writes, or target-authority questioning; bounded read-only examples may reproduce a designer defect.

For existing-team maintenance, inspect the current runnable surfaces, activation state, canonical declaration, stamps, and mappings before structural/runtime recommendations. Do not restart new-team Discovery when the requested change and authority are already clear.

Honor requirements and authorization already supplied in the session. Ask only for a material missing decision, unresolved authority, conflicting requirements, or an irreversible/external action beyond that authorization. Keep useful independent work moving while awaiting an answer; wait before work that depends on a required answer. A recommendation audit does not itself grant missing user authority.

### Keep Questions Focused

Ask one material decision question at a time. Keep a response to one question direction and no more than three related clarification items; avoid repeating answered questions.

### Summaries Communicate Progress

Every 3-4 discovery rounds, summarize confirmed requirements, open questions, and the next area to explore. An interim summary needs no approval; continue authorized independent work and incorporate corrections. The required new-team requirements-summary confirmation still applies.

### Challenge Weak Assumptions

Surface role overlap, missing coverage, workflow gaps, unrealistic throughput, or fragmentation whose coordination cost exceeds its parallel value. Cite the consequence and offer a concrete alternative.

## Violation Determination

- New-team Planning starts without the six confirmed requirements above -> Violation
- Existing-team structural/runtime recommendations omit surface, authority, stamp, or mapping assessment -> Violation
- Silence is treated as required approval, or ambiguous authority is inferred from directory presence -> Violation
- An answered question or interim summary creates a repeat approval stop without a new material decision -> Violation
- Work exceeds existing authorization or proceeds despite a required missing answer -> Violation
- A reply combines unrelated question directions, multiple material decision questions, or more than three clarification items -> Violation
- Five discovery rounds pass without an interim summary, or a clear structural problem is concealed -> Violation

## Exceptions

- An explicit request for a faster pass may reduce interview depth or delegate routine choices; it does not remove the new-team confirmation requirements or authority checks.
