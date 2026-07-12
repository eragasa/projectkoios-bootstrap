```json
{
  "title": "HERMES decision: Schema record-envelope reference comment slice 17",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-edit",
  "datetime": "20260712.024500Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "schema-record-envelope-reference-comment-slice-17",
  "source_plan": "docs/plans/schema-change-brief.20260712.023116_schema-record-envelope.md",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260712.023900_schema-record-envelope-schema-change-planning-slice-16.md",
  "target_surfaces": [
    "docs/schemas/schema.record-base.json"
  ],
  "user_authorization": "USER requested ATHENA make the discussed reference/comment-only changes",
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260712.024500: Schema record-envelope reference comment slice 17

## Decision

HERMES records USER authorization for ATHENA to perform a minimal reference/comment-only schema edit:

```text
schema-record-envelope-reference-comment-slice-17
```

## Scope

ATHENA may edit only:

```text
docs/schemas/schema.record-base.json
```

The edit may add a non-semantic draft-boundary/reference annotation linking:

```text
docs/architecture/architecture.schema-record-envelope.md
docs/schemas/README.md
```

## Required boundaries

The edit must preserve validation semantics.

The edit must not change `required`, `additionalProperties`, `$defs`, enum values, timestamp pattern, `$id`, `$schema`, `$ref` behavior, `type`, `properties`, content constraints, schema authority, ADR sources, generated projections, renderer/ingester behavior, migration, database/storage authority, or JSON authority cutover.

The edit must avoid normative authority-promotion wording such as `must`, `canonical`, `source of truth`, or claims that the schema is accepted machine-readable authority.

## Closeout expectations

ATHENA/HERMES closeout should verify:

```bash
python3 -m json.tool docs/schemas/schema.record-base.json >/dev/null
git diff --check
```

Reviewers should verify the diff is annotation-only and does not alter validation-affecting keywords.
