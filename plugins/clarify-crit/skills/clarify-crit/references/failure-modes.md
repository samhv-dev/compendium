# CRIT Failure Modes

Use these corrections when behaviour drifts. They are diagnostic guidance, not headings to reproduce for the user.

## Solving before understanding

**Failure:** Substantial execution begins while material ambiguity remains.

**Correction:** Identify the smallest decision separating plausible interpretations. Ask it, research it, or apply a transparent low-risk default.

## Complexity-triggered overactivation

**Failure:** CRIT activates merely because a task is long, technical, or multi-step even though it is fully specified.

**Correction:** Complexity alone is insufficient. Activate automatically only when unresolved material uncertainty exists and refinement is worth the interaction.

## Interview inflation

**Failure:** A broad questionnaire is used when one decision would unlock the task.

**Correction:** Trace every question to a changed deliverable, method, risk, cost, approval, or success criterion. Remove the rest and resolve foreseeable blockers together.

## Repeated clarification turns

**Failure:** Questions are spread across several turns even though later blockers were foreseeable from the start.

**Correction:** Consolidate current blockers into one efficient clarification turn. Ask again only when the user's answer creates a new material dependency.

## Visible framework theatre

**Failure:** The response displays request state, Context, Role, Interview, Task, or internal reasoning when the user only needs the result.

**Correction:** Keep the reasoning non-visible. Show only decisions, consequential assumptions, a useful brief, and the required action.

## Redundant visible brief

**Failure:** The model presents a brief and then immediately repeats the same information in the completed output.

**Correction:** Refine internally and execute directly unless the brief supports handoff, approval, traceability, or formal specification.

## Role theatre

**Failure:** A fictional expert panel or simulated debate is narrated.

**Correction:** Use one professional perspective internally. Add or expose another discipline only when it materially changes the method or risk.

## Prompt hijacking

**Failure:** A modest request is expanded into a larger project or replaced with the model's preferred objective.

**Correction:** Preserve the requested outcome. Label genuinely useful expansion ideas as optional and keep them outside the core brief.

## Confirmation loops

**Failure:** The model repeatedly asks permission to continue despite sufficient context and reversible defaults.

**Correction:** Proceed. Ask for approval only when approval is substantively required.

## Hidden consequential assumptions

**Failure:** Audience, platform, budget, jurisdiction, data sensitivity, approval, or scope is silently chosen when it materially changes the result.

**Correction:** Reuse, research, ask, or state a default according to the routing rules.

## Research inflation

**Failure:** The model performs unnecessary searches for details that are immaterial or safely defaultable.

**Correction:** Research only material external facts when reliable verification is available and worth the retrieval cost.

## Asking the user for researchable facts

**Failure:** The user is asked to supply current facts, specifications, rules, prices, or documentation that accessible tools can retrieve more reliably.

**Correction:** Research the fact or state the exact research dependency. Reserve questions for preferences, approvals, inaccessible private facts, and value judgments.

## Artificial multiple choice

**Failure:** Discovery is forced into incomplete options, too many options, or distinctions without meaningful consequences.

**Correction:** Use the smallest set of materially distinct choices, usually two to four. Use a bounded open question when the space is not closed.

## Requirement conflict overlooked

**Failure:** The model treats incompatible requirements as simultaneously achievable.

**Correction:** Identify the smallest incompatible pair and request the governing priority or propose a transparent trade-off.

## Non-portable brief

**Failure:** The brief relies on phrases such as `as discussed`, `the file above`, or unstated history.

**Correction:** Include every execution-critical fact directly or name an explicitly accessible source.

## Duplicate reporting

**Failure:** Objectives, constraints, assumptions, and deliverables are repeated in separate Context and Task sections.

**Correction:** Put resolved context directly into the brief. Show a separate decision section only for unresolved blockers.

## Undefined request treated as ordinary incompleteness

**Failure:** An unformed objective is filled with arbitrary assumptions or detailed implementation questions are asked too early.

**Correction:** Ask one high-leverage outcome question before discussing implementation.

## Reference overloading

**Failure:** Every reference document is loaded during every request.

**Correction:** The core procedure is sufficient for ordinary use. Consult only the specific reference needed for an unfamiliar response pattern, unusual edge case, or behavioural review.

## Non-functional conversational padding

**Failure:** Generic praise, framework announcements, repeated summaries, or open-ended offers add tokens without helping execution.

**Correction:** Retain framing only when it communicates a blocker, assumption, status, limitation, or next action.
