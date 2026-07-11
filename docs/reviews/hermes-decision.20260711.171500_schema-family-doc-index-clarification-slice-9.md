```json
{
  "title": "HERMES decision: schema-family doc/index clarification slice 9",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-doc-edit",
  "datetime": "20260711.171500Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "schema-family-doc-index-clarification-slice-9",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260711.171000_adr-schema-family-contract-reconciliation-slice-8.md",
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260711.171500: schema-family doc/index clarification slice 9

## Decision

HERMES approves `schema-family-doc-index-clarification-slice-9` for a bounded ATHENA documentation/index clarification.

## Approved edit scope

Only this control/index document may be edited:

```text
docs/schemas/README.md
```

The edit must make the accepted Slice 8 content-schema vs record-envelope boundary visible to readers.

## Required clarification

The README should state that:

- `adr.schema.json` is the current ADR content-shape schema until explicitly wrapped, replaced, or retired;
- `schema.record-base.json` is the draft record-envelope direction;
- `adr-draft.schema.json` demonstrates ADR-family composition with the base envelope;
- `adr-active.schema.json` is a compatibility/reconciliation candidate, not co-authoritative with the newer base-envelope family by implication;
- Markdown remains source/control for unmigrated records and generated projections remain evidence unless later cutover is accepted;
- `routing` and `dcn` are not current ADR content-schema fields;
- `workflow_binding` is optional schema content, not operational workflow authority.

## Boundaries

This approval does not authorize editing JSON schema files, editing `docs/adr/`, creating a new ADR draft, changing source status or casing, supersession, acceptance, activation, rejection, promotion, demotion, file moves/renames/deletes/archives/splits, JSON conversion/projection generation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, or cutover.

## Required closeout

Closeout should verify:

```bash
git status --short -- docs/adr docs/schemas/*.json dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```
