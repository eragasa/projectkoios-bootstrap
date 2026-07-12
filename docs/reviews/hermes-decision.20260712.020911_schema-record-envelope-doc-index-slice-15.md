```json
{
  "title": "HERMES decision: Schema record-envelope doc index slice 15",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-doc-edit",
  "datetime": "20260712.020911Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "schema-record-envelope-doc-index-slice-15",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260712.020742_adr-schema-record-envelope-architecture-slice-14.md",
  "target_surface": "docs/schemas/README.md",
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260712.020911: Schema record-envelope doc index slice 15

## Decision

HERMES keeps priority on the ADR/schema architecture track and approves `schema-record-envelope-doc-index-slice-15` for ATHENA handoff.

## Rationale

Slice 14 accepted the architecture surface:

```text
docs/architecture/architecture.schema-record-envelope.md
```

KOIOS watchpoints for Slice 14 noted that if future work updates `docs/schemas/README.md` to point to this architecture, that should be a separate documentation/schema-index slice.

The next coherent bounded action is a documentation/index clarification that links the schema namespace README to the accepted architecture surface without changing schema authority.

## Handoff target

ATHENA should edit only:

```text
docs/schemas/README.md
```

## Required ATHENA output content

The edit should add a concise reference to:

```text
docs/architecture/architecture.schema-record-envelope.md
```

The README should preserve these boundaries:

- `docs/schemas/adr.schema.json` remains current ADR content-shape schema until later approved replacement/wrap/retirement.
- `docs/schemas/schema.record-base.json` remains draft record-envelope direction.
- `docs/architecture/architecture.schema-record-envelope.md` is architecture direction only, not machine-readable schema authority.
- `metadata` + `content` is not current universal emitted-record authority.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated projections remain evidence/review surfaces unless later cutover changes a file's disposition.

## Boundaries

This HERMES decision does not authorize HERMES to edit the ATHENA-owned documentation surface directly.

This decision authorizes ATHENA to make a bounded documentation/index clarification in `docs/schemas/README.md` only.

This decision does not authorize editing JSON schema files, editing `docs/adr/`, changing lifecycle state, accepting `schema.record-base.json` as current record-envelope authority, making `metadata` + `content` current universal emitted-record authority, source mutation, schema mutation, generated projections, authoritative JSON records, database/storage authority, migration, or cutover.

## Required closeout for ATHENA output

ATHENA/HERMES closeout should verify:

```bash
git status --short -- docs/adr docs/schemas/*.json dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git status --short -- docs/schemas/README.md
git diff --check
```
