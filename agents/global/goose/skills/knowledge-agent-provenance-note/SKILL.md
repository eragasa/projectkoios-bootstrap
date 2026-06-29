---
name: knowledge-agent-provenance-note
description: Convert validated artifacts into durable, provenance-backed knowledge
metadata:
  agent: knowledge-agent
  harness_role: consumer-producer
  consumes:
    - architecture-spec
    - implementation-report
    - test-results
  produces:
    - knowledge-note
    - provenance-index
---

## When to use this skill

When the task asks to create or update notes, extract claims, record decisions, build provenance, or convert implementation facts into durable documentation. The knowledge agent (goose/Koios) owns this skill.

## Agent responsibility

Convert validated artifacts into durable, provenance-backed knowledge. Own claim extraction, provenance capture, note generation, architecture decision records, implementation fact records, and open-question indexing. Do not invent architecture. Do not resolve disagreements between spec and implementation.

## Inputs

- `architecture-spec` — the approved decision
- `implementation-report` — the implementation summary
- `test-results` — validation output

## Procedure

1. Extract factual claims from the spec and implementation report.
2. For each claim, capture provenance (source artifact, line number, date).
3. Classify each claim as: decision, implementation fact, rationale, or open question.
4. Write durable notes (Obsidian vault or architecture decision record).
5. Build provenance index mapping claims to sources.
6. Update open-question index with any unresolved items.

## Output artifact

- `knowledge-note` — durable note derived from validated artifacts
- `provenance-index` — mapping from claims to sources with classification

## Failure modes

- Claims cannot be extracted due to ambiguous artifact language — mark as unresolved
- Provenance chain is incomplete — note the gap, do not fabricate

## Escalation rule

If source artifacts are contradictory and the contradiction was not flagged during implementation, escalate to meta-harness (pi) for disagreement resolution.
