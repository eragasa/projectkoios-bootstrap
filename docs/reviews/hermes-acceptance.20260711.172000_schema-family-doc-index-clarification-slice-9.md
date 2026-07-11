```json
{
  "title": "HERMES acceptance: schema-family doc/index clarification slice 9",
  "artifact_type": "completion-decision",
  "status": "accepted-doc-clarification",
  "datetime": "20260711.172000Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "schema-family-doc-index-clarification-slice-9",
  "reviewed_artifact": "docs/schemas/README.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.171500_schema-family-doc-index-clarification-slice-9.md",
  "authority_change": false,
  "schema_json_mutation": false,
  "source_adr_mutation": false,
  "next_owner": "HERMES_USER"
}
```

# HERMES acceptance 20260711.172000: schema-family doc/index clarification slice 9

## Decision

HERMES accepts `schema-family-doc-index-clarification-slice-9` as a bounded documentation/index clarification.

## Accepted change

Edited only:

```text
docs/schemas/README.md
```

The README now states the accepted Slice 8 boundary between ADR content schema, schema-backed record envelope, Markdown source/control, generated projections, and unresolved/unsupported fields.

## Acceptance rationale

The edit makes the current schema-family layering visible without mutating machine-readable schemas or ADR source authority.

Accepted clarifications:

- `adr.schema.json` is current ADR content-shape schema until explicitly wrapped, replaced, or retired.
- `schema.record-base.json` is the draft record-envelope direction.
- `adr-draft.schema.json` demonstrates ADR-family composition with the base envelope.
- `adr-active.schema.json` is a compatibility/reconciliation candidate, not co-authoritative with the newer base-envelope family by implication.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated projections remain evidence or review/navigation surfaces unless later cutover changes a specific file's disposition.
- `routing` and `dcn` are not current ADR content-schema fields.
- `workflow_binding` is optional schema content, not operational workflow authority.

## Boundaries preserved

This acceptance does not authorize editing JSON schema files, editing `docs/adr/`, creating a new ADR draft, changing source status or casing, supersession, acceptance, activation, rejection, promotion, demotion, file moves/renames/deletes/archives/splits, JSON conversion/projection generation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, or cutover.

## Recommended next action

Primary next action: decide whether to proceed with source-facing repair.

Recommended bounded option:

```text
adr-template-schema-contract-successor-planning-slice-10
```

Purpose: draft a proposal-only successor plan or explicit ADR-creation brief for `docs/adr/adr.adr-template-contract.md`, preserving old-source provenance and requiring separate approval before ADR creation, supersession, source mutation, or schema edits.

## Closeout validation

Observed validation:

```bash
git status --short -- docs/adr docs/schemas/*.json dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Both produced no output / passed at acceptance time.
