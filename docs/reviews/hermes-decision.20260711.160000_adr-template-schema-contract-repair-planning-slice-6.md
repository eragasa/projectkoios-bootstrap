```json
{
  "title": "HERMES decision: ADR template/schema contract repair planning slice 6",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-planning-review",
  "datetime": "20260711.160000Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-template-schema-contract-repair-planning-slice-6",
  "reviewed_artifact": "docs/plans/architecture-brief.20260711.155500_adr-template-contract-repair-planning-slice-6.md",
  "provenance_input": "workspaces/koios/working/next-proof-input.20260711_template-schema-contract-repair-planning.md",
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260711.160000: ADR template/schema contract repair planning slice 6

## Decision

HERMES approves `adr-template-schema-contract-repair-planning-slice-6` for ATHENA planning/review execution.

## Rationale

ATHENA revised the brief to align with KOIOS provenance input. The slice is bounded to exactly one source, `docs/adr/adr.adr-template-contract.md`, and is limited to repair-path planning. It does not authorize source mutation or lifecycle/authority changes.

This is the appropriate next step after Slice 5 because the semantic rationalization found this file authority-relevant but semantically mixed: accepted-like status casing, stale `routing` claims, JSON-vs-Markdown source-of-truth claims ahead of current authority, and template/schema-contract ambiguity.

## Approved scope

Exactly one target source is in scope:

```text
docs/adr/adr.adr-template-contract.md
```

Do not add `docs/adr/adr.schema-base.md` or other ADRs to this slice.

## Approved planning direction

Produce one ATHENA planning/review artifact, preferred:

```text
docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md
```

The artifact should inventory current claims, compare them against current schema/lifecycle/JSON-authority/bidirectional-object surfaces, evaluate leave/revise/replace/split/defer options, and recommend one primary next path plus any fallback. Recommendations are proposal input only.

## Required issues to address

- Preserve observed status/casing `Accepted`; do not normalize.
- Treat `routing` claims as likely stale or sidecar/provenance/workflow metadata pending owner decision.
- Distinguish future JSON-source-of-truth target state from current repository authority.
- Distinguish ADR content schema from bidirectional object envelope/sidecar evidence.
- Classify template/schema/control role separately from ordinary ADR decision authority.
- Account for Slice 4 source-to-candidate incompleteness and omitted/source-preserved sections.

## Boundaries

This approval does not authorize editing `docs/adr/adr.adr-template-contract.md` or any source ADR, status normalization, lifecycle state changes, formal supersession, acceptance, activation, rejection, promotion, demotion, schema changes, file moves/renames/deletes/archives/splits, JSON conversion/projection generation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, or cutover.

## Required closeout

The planning artifact must be review/planning only. Closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

If a recommended repair requires source mutation, schema change, status change, supersession, split, conversion, or cutover, it must be routed as a separate HERMES/USER-approved slice.
