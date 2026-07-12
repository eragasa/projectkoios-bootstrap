```json
{
  "title": "HERMES decision: Schema record-envelope schema-change planning slice 16",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-handoff",
  "datetime": "20260712.023116Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "schema-record-envelope-schema-change-planning-slice-16",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260712.021113_schema-record-envelope-doc-index-slice-15.md",
  "target_surfaces": [
    "docs/architecture/architecture.schema-record-envelope.md",
    "docs/schemas/schema.record-base.json",
    "docs/schemas/README.md"
  ],
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260712.023116: Schema record-envelope schema-change planning slice 16

## Decision

HERMES keeps priority on the ADR/schema architecture track and approves `schema-record-envelope-schema-change-planning-slice-16` for ATHENA handoff.

## Rationale

Slice 14 accepted the schema record-envelope architecture surface, and Slice 15 linked that architecture from `docs/schemas/README.md` without changing machine-readable schema authority.

The next coherent bounded action is proposal-only schema-change planning for how `docs/schemas/schema.record-base.json` should relate to the accepted architecture surface.

## Handoff target

ATHENA should produce one proposal-only schema-change planning brief.

Suggested output path:

```text
docs/plans/schema-change-brief.20260712.023116_schema-record-envelope.md
```

## Required ATHENA output content

The brief should decide a proposed path for `docs/schemas/schema.record-base.json`, including whether to:

- keep it unchanged as draft direction;
- revise it in a later schema-change slice;
- wrap or split it;
- promote any portion toward accepted schema-envelope authority;
- add/adjust references between schema JSON, schema README, and `docs/architecture/architecture.schema-record-envelope.md`;
- defer schema changes until renderer/ingester or migration needs are clearer.

The brief must define acceptance criteria and explicit non-goals for any later schema-edit slice.

## Current boundaries to preserve

- `docs/architecture/architecture.schema-record-envelope.md` is accepted architecture direction only.
- `docs/schemas/schema.record-base.json` remains draft record-envelope direction until a later approved schema-change/acceptance slice changes that state.
- `metadata` + `content` is not current universal emitted-record authority.
- `docs/schemas/adr.schema.json` remains current ADR content-shape schema until later approved replacement/wrap/retirement.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated projections remain evidence/review surfaces unless later cutover changes a file's disposition.

## Boundaries

This HERMES decision does not authorize HERMES to produce the ATHENA planning artifact directly.

This decision authorizes only proposal-only planning. It does not authorize editing `docs/schemas/`, editing `docs/adr/`, changing lifecycle state, accepting schema authority, making `metadata` + `content` current universal emitted-record authority, generated projections, authoritative JSON records, database/storage authority, migration, renderer/ingester implementation, or JSON authority cutover.

## Required closeout for ATHENA output

ATHENA/HERMES closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git status --short -- docs/plans/schema-change-brief.20260712.023116_schema-record-envelope.md
git diff --check
```
