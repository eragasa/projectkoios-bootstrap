```json
{
  "title": "HERMES decision: schema-family repair planning slice 7",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-planning-review",
  "datetime": "20260711.165218Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "schema-family-repair-planning-slice-7",
  "user_selection": "broader schema-family repair planning",
  "prior_acceptance": "docs/reviews/hermes-acceptance.20260711.160700_adr-template-schema-contract-repair-planning-slice-6.md",
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260711.165218: schema-family repair planning slice 7

## Decision

HERMES records USER selection of option 3 and approves `schema-family-repair-planning-slice-7` for ATHENA planning/review execution.

## Rationale

Slice 6 found `docs/adr/adr.adr-template-contract.md` to be authority-relevant but semantically mixed, with stale `routing` claims, ahead-of-authority JSON/Markdown source-of-truth wording, ambiguous `dcn` handling, bounded `workflow_binding` support, and a template/schema/source-of-truth contract role that is not cleanly represented as an ordinary ADR decision.

The USER selected the broader schema-family repair planning path rather than drafting an immediate single successor ADR or lower-risk errata note. That path is appropriate because the Slice 6 watchpoints overlap with schema-base, ADR content schema, record-envelope, projection, and migration-authority surfaces.

## Approved scope

The planning slice is review/planning only. ATHENA may compare and inventory the following schema-family surfaces:

```text
docs/adr/adr.adr-template-contract.md
docs/adr/adr.schema-base.md
docs/adr/adr.json-authoritative-adr-store.draft.md
docs/plans/schema-base-adr-records-workplan.md
docs/schemas/README.md
docs/schemas/adr.schema.json
docs/schemas/schema.record-base.json
docs/schemas/adr-draft.schema.json
docs/schemas/adr-active.schema.json
```

ATHENA may cite related accepted Slice 0-6 evidence and reviews only as context. Do not expand into all ADRs, all schemas, implementation code, product/mothership architecture, or migration execution.

## Approved planning direction

Produce one ATHENA planning/review artifact, preferred:

```text
docs/plans/repair-plan.20260711.165300_schema-family-adr-contract-slice-7.md
```

The artifact should:

1. classify current schema-family surfaces by role: content schema, record envelope, ADR lifecycle/status, projection/rendering, source/provenance, migration authority, and compatibility/legacy marker;
2. identify contradictions, stale claims, and ahead-of-authority claims across the approved scope;
3. preserve source status/casing and existing lifecycle meanings as observations, not normalization actions;
4. recommend a staged repair sequence that separates proposal/errata, successor ADR(s), schema edits, source mutations, projections, and authority cutover;
5. identify which future slices require HERMES/USER approval and which owner domain should produce them;
6. explicitly say whether the next concrete slice should be a successor contract proposal, a schema-base reconciliation, or a non-mutating errata/index note.

## Required issues to address

- Relationship between `docs/schemas/adr.schema.json` as ADR content-shape schema and `schema.record-base.json` / `adr-draft.schema.json` as record-envelope schemas.
- Relationship between Markdown source/control for unmigrated records and future generated projections after migration/cutover.
- Disposition options for stale `routing` claims: legacy prose, sidecar/provenance, workflow metadata, schema-envelope metadata, or excluded field.
- Disposition options for `dcn`: root ADR namespace guidance, content schema field, envelope/metadata field, filename/record-id convention, or deferred.
- Boundary for optional `workflow_binding`: schema-supported content only unless a later workflow authority decision promotes operational meaning.
- Relationship between `accepted-staged-direction` JSON authority and non-executed migration/cutover gates.
- Relationship between legacy schema markers and canonical `docs/schemas/` namespace.

## Boundaries

This approval does not authorize editing `docs/adr/`, editing `docs/schemas/`, changing any source status, normalizing status casing, superseding, accepting, activating, rejecting, promoting, demoting, moving, renaming, deleting, archiving, splitting files, generating or replacing projections, creating authoritative JSON ADR records, adding database/storage authority, running migration, or performing authority cutover.

The planning artifact must be proposal input only. Any recommended repair that requires source mutation, schema change, lifecycle/status change, supersession, split, conversion, generated projection replacement, migration, or cutover must be routed as a separate HERMES/USER-approved slice.

## Required closeout

Closeout should verify the planning-only boundary with:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

If planning identifies contradictions that cannot be resolved without authority changes, HERMES should record the inconsistency and ask USER to choose the next bounded repair slice.
