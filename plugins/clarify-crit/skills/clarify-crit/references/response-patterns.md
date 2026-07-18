# CRIT Response Patterns

These are adaptive patterns, not mandatory templates. Use the smallest structure that helps the user decide, approve, hand off, or execute. Omit headings and fields that add no distinct value.

## 1. Direct execution

Use when the request can be safely resolved internally and the same model is performing the task.

```markdown
[Consequential assumption or limitation, only when needed.]

[Completed task output.]
```

Do not display CRIT's internal classification or a redundant brief.

## 2. One blocking decision

```markdown
## Decision needed

**Question:** ...
**Recommended default:** ...

## Provisional brief

- **Objective:** ...
- **Deliverable:** ...
- **Constraints:** ...
```

Make the question answerable in one short reply. Include everything already established so the user is not asked again.

## 3. Compact portable brief

```markdown
## Execution brief

- **Objective:** ...
- **Deliverable:** ...
- **Requirements:** ...
- **Success:** ...
- **Default:** ...
```

Use only fields that carry distinct information.

## 4. Bounded ambiguity

```markdown
## Decisions needed

1. ...
2. ...

**Recommended defaults:** ...

## Provisional execution brief

- **Objective:** ...
- **Deliverables:** ...
- **Requirements and constraints:** ...
- **Success criteria:** ...
- **Output format:** ...
- **Out of scope:** ...
```

Use no more than three critical questions. Prefer one combined decision when possible.

## 5. Deep or formal specification

```markdown
# Execution brief

## Objective
...

## Deliverables and phases
...

## Requirements and constraints
...

## Risks and dependencies
...

## Success criteria
...

## Assumptions and defaults
...

## Out of scope
...

## Approval or next action
...
```

Use this only when the task genuinely benefits from a reviewable formal specification.

## 6. Undefined objective

```markdown
## Direction to establish

**Current aim:** ...
**Most useful decision:** ...
**Question:** ...
**Recommended starting point:** ...
```

Ask one high-leverage outcome question before discussing implementation detail.

## 7. Conflicting requirements

```markdown
## Trade-off needed

These requirements conflict:

- ...
- ...

**Decision:** Which requirement governs?
**Recommended trade-off:** ...

## What remains unchanged
...
```

Identify the smallest incompatible pair rather than reopening the whole brief.

## 8. Prompt-only request

Return a self-contained copy-ready prompt and stop. Do not execute the underlying task or add an unsolicited project plan.

```markdown
## Copy-ready prompt

[Portable prompt]
```

## 9. Research dependency

When a material fact is externally verifiable:

- research it when suitable tools and reliable sources are available;
- otherwise name the exact dependency and distinguish it from user preference;
- use a labelled provisional assumption only when it is safe and reversible.

## 10. Refinement plus execution

Use one of two approaches:

- **Internal refinement → direct execution** when a visible brief adds no value.
- **Compact brief → execution** when the brief supports approval, handoff, traceability, or complex work.

Do not ask for ceremonial confirmation when no blocker remains.
