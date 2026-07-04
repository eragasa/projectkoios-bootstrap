---
name: knowledge-provenance-audit
adr_binding:
  - docs/adr/adr.skill-register-and-adr-binding-policy.draft.md
  - docs/adr/adr.control-surfaces-and-ownership-boundaries.draft.md
description: |
  Verify completed work has been captured durably as knowledge
  Bound to ADRs: adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md.
metadata:
  agent: knowledge-agent
  harness_role: consumer
  consumes:
    - completion-decision
    - implementation-report
    - deviation-report
    - provenance-index
  produces:
    - provenance-audit
---
## When to use this skill

When asked to audit whether completed work has durable knowledge capture, to
find orphaned implementation artifacts without corresponding knowledge notes,
or to verify provenance index coverage. Koios owns this skill.

Supports two trigger modes:
- **Scan-mode**: proactive audit across a set of completed workflows
- **Flag-mode**: reactive check when an implementation artifact is encountered
  without a matching knowledge note

## Agent responsibility

Inspect the relationship between completed work artifacts and their
corresponding knowledge/provenance artifacts. Report any gaps where
implementation was completed (per `CompletionDecision`) but no `KnowledgeNote`
or `ProvenanceIndex` exists.

Do not create knowledge notes during audit — the audit is a detection pass.
Capture should be sent through `knowledge-agent-provenance-note`.

## Inputs

- `completion-decision` — one or more completion records to audit
- `implementation-report` — reports whose capture status to verify
- `deviation-report` — deviations that should have been captured
- `provenance-index` — existing index to check for gaps

## Procedure

1. For each `CompletionDecision` or `ImplementationReport` in scope, check
   whether a corresponding `KnowledgeNote` and `ProvenanceIndex` exist.

2. If found, verify the existing provenance index covers the claims from the
   implementation report. Note any claims present in the report but missing
   from the index.

3. If not found, record the gap: which artifacts are missing capture, their
   source paths, and the date they were completed.

4. For scan-mode: repeat for all completed workflows in the audit scope.

5. For flag-mode: check the single encountered artifact and report immediately.

6. Distinguish in the report:
   - validated capture (capture exists, provenance covers claims)
   - partial capture (capture exists but provenance is incomplete)
   - missed capture (no capture found for completed work)
   - unresolved (capture status cannot be determined)

7. Do not produce knowledge notes during audit. The audit output is a
   `ProvenanceAudit` for Hermes to send to the appropriate capture workflow.

## Output artifact

- `ProvenanceAudit` — report of capture gaps, partial captures, and validated
  captures with source references. Distinguishes: validated, partial, missed,
  unresolved.

## Failure modes

- Cannot determine if work was completed (no `CompletionDecision` found) —
  mark as unresolved
- Source artifacts referenced in the index are missing from the filesystem —
  note the gap but do not infer capture status
- Scan scope is ambiguous — restrict to explicitly provided artifact list,
  do not guess

## Escalation rule

If systemic missed capture is detected (multiple completed workflows without
corresponding knowledge artifacts), escalate to Hermes with the
`ProvenanceAudit`. Hermes decides whether to send knowledge capture work into
the Koios sandbox, or to request a process change from Athena.
