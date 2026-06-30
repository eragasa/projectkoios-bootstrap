---
name: knowledge-agent-provenance-note
description: Convert validated artifacts into durable, provenance-backed knowledge
metadata:
  agent: knowledge-agent
  harness_role: consumer-producer
  consumes:
    - architecture-spec
    - acceptance-criteria
    - implementation-report
    - test-results
    - completion-decision
    - deviation-report
  produces:
    - knowledge-note
    - provenance-index
    - repo-state-summary
    - routing-recommendation
---

## When to use this skill

When the task asks to create or update notes, extract claims, record decisions,
build provenance, or convert implementation facts into durable documentation.
Koios owns this skill.

## Agent responsibility

Convert validated artifacts into durable, provenance-backed knowledge. Own
claim extraction, provenance capture, note generation, architecture decision
records, implementation fact records, and open-question indexing.

Before durable capture, verify the artifact chain:
`ArchitectureSpec -> ImplementationReport -> TestResults -> CompletionDecision`
when applicable. Flag missing links rather than fabricating them.

Do not invent architecture. Do not resolve disagreements between spec and
implementation. Flag contradictory or unresolved provenance rather than
normalizing it.

## Inputs

- `architecture-spec` — the approved decision
- `acceptance-criteria` — measurable criteria the implementation satisfies
- `implementation-report` — the implementation summary
- `test-results` — validation output
- `completion-decision` — Hermes completion gate result
- `deviation-report` — any spec-vs-implementation deviations found

## Procedure

1. Verify chain integrity: check that the artifact sequence
   `ArchitectureSpec -> ImplementationReport -> TestResults ->
   CompletionDecision` is complete for the workflow being captured. Flag any
   missing link as unresolved — do not fabricate.

2. Extract factual claims from the spec, implementation report, and deviation
   report.

3. For each claim, capture provenance (source artifact path, line reference
   when practical, producing role, date).

4. Classify each claim as: decision, implementation fact, rationale,
   open question, observed state, or recommendation.

5. Flag any contradictory claims or unresolved validation status — do not
   silently normalize.

6. Write durable knowledge note with all claims, classifications, provenance,
   and validation statuses.

7. Build provenance index mapping claims to sources with classification.

8. Update open-question index with any unresolved items.

9. If the context includes a relevant repo state query, optionally produce a
   `RepoStateSummary` (advisory, for Hermes).

10. If a routing question arose during capture, optionally produce a
    `RoutingRecommendation` (advisory, for Hermes).

## Output artifacts

- `KnowledgeNote` — durable note derived from validated artifacts
- `ProvenanceIndex` — mapping from claims to sources with classification and
  validation status
- `RepoStateSummary` — advisory, for Hermes (optional)
- `RoutingRecommendation` — advisory, for Hermes (optional)

## Failure modes

- Claims cannot be extracted due to ambiguous artifact language — mark as
  unresolved rather than fabricating
- Provenance chain is incomplete — note the gap with unresolved status, do not
  fabricate the missing link
- Contradictory claims between spec and implementation — flag both, do not
  blend or resolve

## Escalation rule

If source artifacts are contradictory and the contradiction was not flagged
during implementation, escalate to meta-harness (pi/Hermes) for disagreement
resolution. If the artifact chain is incomplete and cannot be resolved locally,
escalate to Hermes for direction.
