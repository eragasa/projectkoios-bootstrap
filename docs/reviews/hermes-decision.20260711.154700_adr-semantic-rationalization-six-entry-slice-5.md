```json
{
  "title": "HERMES decision: ADR semantic rationalization six-entry slice 5",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-review",
  "datetime": "20260711.154700Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-semantic-rationalization-six-entry-slice-5",
  "reviewed_artifact": "docs/plans/architecture-review-brief.20260711.154300_adr-semantic-rationalization-slice-5.md",
  "provenance_input": "workspaces/koios/working/next-proof-input.20260711_adr-semantic-rationalization-after-slice-4.md",
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260711.154700: ADR semantic rationalization six-entry slice 5

## Decision

HERMES approves `adr-semantic-rationalization-six-entry-slice-5` for ATHENA semantic rationalization review.

## Rationale

ATHENA revised the architecture-review brief to align with KOIOS provenance input. The slice is bounded to the six accepted Slice 4 entries, reordered for semantic review, and separates semantic authority review from JSON conversion mechanics.

This is the appropriate next step after Slice 4 because Slice 4 proved candidate-only corpus-style reporting but did not decide whether selected ADR/control-surface entries actually make sense as current project authority.

## Approved subset and order

Use exactly these six entries in semantic review order:

```text
docs/adr/README.md
docs/adr/adr.petrinet.20260705.132740Z.md
docs/adr/adr.adr-template-contract.md
docs/adr/adr.json-schemas.draft.md
docs/adr/adr.schema-base.md
docs/adr/adr.adr-lifecycle.draft.md
```

Do not add domain-review/product/future-system ADRs and do not expand to all `docs/adr/*.md`.

## Approved review direction

Produce one ATHENA review artifact, preferred:

```text
docs/reviews/semantic-rationalization.20260711_adr-six-entry-slice-5.md
```

The review should classify each selected entry semantically using the brief vocabulary or a justified refinement, including observed status/casing, Slice 4 outcome, omitted/source-preserved sections, current authority assessment, conflicts/stale claims, recommended next actions, owner decision needed, and explicit non-authority markers.

Recommended follow-ups are proposal input only. They do not change ADR lifecycle state.

## Boundaries

This approval does not authorize source Markdown mutation, status changes or normalization, formal supersession, acceptance, rejection, promotion, demotion, file moves/renames/deletes/archives, schema changes, JSON conversion/projection generation, authoritative JSON ADR records, database/storage authority, bulk/corpus migration, or authority cutover.

Do not treat Slice 4 generated evidence or projections as semantic authority; use them only as provenance and conversion-boundary evidence.

## Required closeout

Before HERMES final acceptance, the ATHENA review must be checked for exact subset coverage, no source/schema/dev/code mutation, proposal-only recommendations, and clear separation between semantic authority and JSON conversion readiness. KOIOS provenance review may be requested if the review introduces cross-source provenance claims or conflicts requiring evidence audit.
