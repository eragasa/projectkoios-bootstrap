```json
{
  "title": "Schema-change brief: schema record envelope",
  "artifact_type": "schema-change-planning-brief",
  "status": "proposal-only-pending-hermes-user-acceptance",
  "datetime": "20260712.023116Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "schema-record-envelope-schema-change-planning-slice-16",
  "target_surfaces": [
    "docs/architecture/architecture.schema-record-envelope.md",
    "docs/schemas/schema.record-base.json",
    "docs/schemas/README.md"
  ],
  "hermes_decision": "docs/reviews/hermes-decision.20260712.023116_schema-record-envelope-schema-change-planning-slice-16.md",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260712.021113_schema-record-envelope-doc-index-slice-15.md",
  "schema_mutation": false,
  "source_mutation": false,
  "authority_change": false,
  "next_owner": "HERMES_USER"
}
```

# Schema-change brief 20260712.023116: schema record envelope

## Purpose

Decide a safe proposed path for `docs/schemas/schema.record-base.json` after acceptance of the schema record-envelope architecture and schema README index clarification.

This brief is proposal-only. It does not edit `docs/schemas/`, edit `docs/adr/`, change lifecycle state, accept schema authority, make `metadata` + `content` current universal emitted-record authority, generate projections, create authoritative JSON records, add database/storage authority, implement renderer/ingester behavior, migrate, or cut over JSON authority.

## Source basis

Target surfaces:

```text
docs/architecture/architecture.schema-record-envelope.md
docs/schemas/schema.record-base.json
docs/schemas/README.md
```

Control inputs:

```text
docs/reviews/hermes-decision.20260712.023116_schema-record-envelope-schema-change-planning-slice-16.md
docs/reviews/hermes-acceptance.20260712.021113_schema-record-envelope-doc-index-slice-15.md
docs/architecture/architecture.schema-record-envelope.md
docs/schemas/README.md
```

Current boundaries:

- `docs/architecture/architecture.schema-record-envelope.md` is accepted architecture direction only.
- `docs/schemas/schema.record-base.json` remains draft record-envelope direction until a later approved schema-change/acceptance slice changes that state.
- `metadata` + `content` is not current universal emitted-record authority.
- `docs/schemas/adr.schema.json` remains current ADR content-shape schema until later approved replacement/wrap/retirement.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated projections remain evidence/review surfaces unless later cutover changes a file's disposition.

## Current schema assessment

`docs/schemas/schema.record-base.json` already expresses a concrete draft envelope shape:

- top-level `metadata` and `content` are required;
- additional top-level properties are disallowed;
- `RecordMetadata` requires record identity, schema identity/versioning, title, status, timestamps, origin, scope, repository, domain, source artifacts, derivation, evidence, and projections;
- `content` remains family-specific and intentionally unconstrained by the base schema;
- `$id` uses the project-local schema URL form.

This broadly matches the accepted architecture direction. However, the current JSON schema is more specific than the architecture's accepted authority currently warrants because it can be read as a fully authoritative envelope contract rather than draft direction. It also encodes several policy details that may need review before promotion, including status placement, required projection arrays, projection source-of-truth values, role/actor enums, source-artifact relationship enums, and timestamp format constraints.

## Options evaluated

### Option A: Keep unchanged as draft direction

Assessment: safest immediate path.

Pros:

- Preserves existing tests and schema-family examples.
- Avoids premature schema authority promotion.
- Avoids expanding scope into renderer/ingester, migration, or cutover policy.
- Matches Slice 14/15 boundary that `schema.record-base.json` is draft direction.

Cons:

- The schema may continue to look more authoritative than intended unless readers observe the README/architecture boundary.
- No machine-readable marker is added to distinguish draft direction from accepted authority.

Recommended as the immediate disposition.

### Option B: Revise in a later schema-change slice

Assessment: likely useful later, but not yet required.

Possible revisions:

- add a description note that the schema is draft direction;
- add `$comment` references to `docs/architecture/architecture.schema-record-envelope.md` and `docs/schemas/README.md`;
- review required metadata fields and arrays for minimal viable envelope semantics;
- clarify whether `projections` is required before projection/cutover authority exists;
- clarify `metadata.status` relationship to ADR `content.status` for ADR-family schemas;
- refine enum vocabularies only when implementation evidence requires it.

Pros:

- Could make the draft boundary visible in the machine-readable schema.
- Could reduce future validator ambiguity.

Cons:

- Any JSON schema edit can be mistaken for schema authority expansion.
- Premature field/enum changes may churn before renderer/ingester/migration needs are clearer.

Use only after HERMES/USER approves a schema-edit slice with concrete acceptance criteria.

### Option C: Wrap or split the schema

Assessment: defer.

Potential split:

- a minimal base envelope schema with only `metadata` and `content`;
- shared `$defs` schema for metadata/provenance/evidence/projection structures;
- family schemas that import the base and constrain content.

Pros:

- Could make base vs shared metadata vocabulary cleaner.
- Could avoid overloading one file with all shared definitions.

Cons:

- Adds schema files and references before implementation pressure proves the need.
- Requires schema registry and test updates.
- Risks creating migration/schema authority before renderer/ingester evidence exists.

Defer until schema composition or validator needs are clearer.

### Option D: Promote some portion toward accepted schema-envelope authority

Assessment: not recommended now.

The architecture is accepted as direction, but HERMES acceptance explicitly says it is not machine-readable schema authority. Promoting even a subset should wait until there is a concrete record-family use case, validation evidence, and owner decision about status placement, projection metadata, and source/control semantics.

Use only after a future schema-change slice proves the need and HERMES/USER explicitly accepts machine-readable schema-envelope authority.

### Option E: Add or adjust references only

Assessment: safe candidate for the first actual schema-edit slice, if HERMES/USER wants a minimal edit.

Possible minimal edit:

- update the schema `description` and/or `$comment` to reference `docs/architecture/architecture.schema-record-envelope.md` and state that the file is draft direction.

Pros:

- Low semantic risk.
- Makes the architecture link discoverable from the schema file.

Cons:

- Still mutates JSON schema and therefore needs explicit schema-edit approval.
- Does not resolve deeper field/enum questions.

Recommended only as a later minimal schema-edit slice, not in this planning slice.

### Option F: Defer schema changes until renderer/ingester or migration needs are clearer

Assessment: preferred strategic path after keeping the schema unchanged now.

Pros:

- Avoids schema churn.
- Lets concrete implementation/migration evidence identify which fields are necessary, optional, or too strict.
- Preserves the architecture/readme boundary without expanding authority.

Cons:

- Leaves schema file as draft direction without machine-readable clarification.

Recommended.

## Recommended path

Primary recommendation: **keep `docs/schemas/schema.record-base.json` unchanged as draft record-envelope direction for now, and defer substantive schema changes until renderer/ingester, family-schema composition, or migration needs become concrete.**

Secondary recommendation: if HERMES/USER wants a small next schema-edit slice, limit it to reference/description clarification only. Do not revise field semantics, required arrays, enum vocabularies, status mirroring, projection authority, or family-schema composition in the first edit.

Suggested future minimal schema-edit slice:

```text
schema-record-envelope-reference-comment-slice-17
```

Possible scope:

- edit only `docs/schemas/schema.record-base.json`;
- add or adjust `description` / `$comment` to cite `docs/architecture/architecture.schema-record-envelope.md`;
- explicitly mark the schema as draft direction, not accepted universal emitted-record authority;
- keep all validation semantics unchanged.

Suggested strategic follow-up after more evidence:

```text
schema-record-envelope-field-reconciliation-slice-later
```

Possible scope:

- decide required vs optional metadata arrays;
- decide status placement and mirroring rule for ADR family schemas;
- decide projection metadata requirements after projection/cutover architecture matures;
- decide whether to split shared `$defs` from the base envelope.

## Later schema-edit acceptance criteria

A future schema-edit slice should be accepted only if it meets the relevant criteria below.

### Minimal reference/comment edit criteria

1. Edits only the explicitly approved JSON schema file, likely `docs/schemas/schema.record-base.json`.
2. Does not change validation semantics.
3. Adds a concise reference to `docs/architecture/architecture.schema-record-envelope.md` or equivalent architecture pointer.
4. States or comments that the schema remains draft record-envelope direction unless separately accepted.
5. Does not make `metadata` + `content` current universal emitted-record authority.
6. Does not edit `docs/adr/`.
7. Does not edit ADR content schema fields in `docs/schemas/adr.schema.json`.
8. Includes JSON validity and focused schema tests if the repository has relevant validators for the touched file.
9. `git diff --check` passes.

### Substantive schema reconciliation criteria

1. Identifies the exact schema fields/enums/required properties being changed.
2. Explains the source authority for each semantic change.
3. States whether the change affects validation behavior.
4. Keeps `content` family-specific and avoids ADR-specific content fields in the base envelope.
5. Preserves ADR content-schema authority separately from envelope metadata.
6. Defines any `metadata.status` / `content.status` relationship before applying it to ADR-family schemas.
7. Does not add projection authority without accepted projection/cutover policy.
8. Includes tests proving expected valid and invalid records.
9. Does not trigger migration or source rewrite by implication.
10. Preserves old source/provenance and reports compatibility risks.

## Explicit non-goals for later schema-edit slices

A later schema-edit slice must not, unless separately and explicitly approved:

- edit `docs/adr/` sources;
- change ADR lifecycle state;
- accept `schema.record-base.json` as repository-wide universal emitted-record authority;
- make all repository documents schema-backed;
- demote Markdown source/control for unmigrated records;
- generate projections;
- create authoritative JSON ADR records;
- add database/storage authority;
- implement renderer/ingester behavior;
- migrate records;
- cut over JSON authority;
- revise ADR content fields in `adr.schema.json` as a side effect of envelope planning;
- promote `docs/adr/adr.schema-base.md` to current ADR authority;
- infer lifecycle status from embedded JSON in old source files.

## Owner decisions required before promotion

Before any portion of the record envelope becomes accepted machine-readable schema authority, HERMES/USER should decide:

- whether the authority applies to one family, several families, or all schema-backed records;
- whether `schema.record-base.json` remains one file or is split into base envelope plus shared definitions;
- which metadata fields are required for the first accepted use case;
- whether projections are required before migration/cutover exists;
- how `metadata.status` relates to family content status fields;
- whether accepted authority belongs in schema JSON alone, an ADR, architecture, README, or a combined package;
- what tests and validators prove the authority change.

## Closeout validation expectations

ATHENA/HERMES closeout for this planning slice should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git status --short -- docs/plans/schema-change-brief.20260712.023116_schema-record-envelope.md
git diff --check
```

Expected result for this planning slice: no mutation to `docs/adr/`, `docs/schemas/`, or Slice 4 dry-run evidence; only this planning brief appears on its scoped plan path; diff hygiene passes.
