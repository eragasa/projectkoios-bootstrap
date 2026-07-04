# Workplan: Schema Base and ADR Record Architecture

## Context

```json
{
  "title": "Schema Base and ADR Record Architecture Workplan",
  "status": "draft",
  "created_on": "20260704.161309",
  "origin": {
    "type": "user_request",
    "method": "manual",
    "actor": "ATHENA",
    "authority": "user"
  },
  "scope": "projectkoios-bootstrap",
  "repository": "projectkoios-bootstrap",
  "domain": {
    "domain_type": "architecture",
    "domain_subtype": "software",
    "domain_scope": "schema"
  }
}
```

## Content

This workplan integrates ATHENA drafting, KOIOS provenance review, HERMES state-reconciliation review, and VULCAN implementation-readiness review for the schema-base and ADR-record architecture.

### Concern

- MUST keep architecture, schema migration, and implementation as separate commits or handoff slices.
- MUST treat `docs/adr/adr.schema-base.md` as draft architecture until explicitly promoted.
- MUST keep `docs/schemas/` as the durable namespace for machine-readable schema artifacts.
- MUST NOT treat legacy schema files as co-authoritative after migration.
- SHOULD settle metadata, origin, status, title, Markdown grammar, and schema `$id` strategy before Vulcan implementation.
- SHOULD treat metadata, origin, status, title, and schema `$id` strategy as settled once `docs/adr/adr.schema-base.md`, `docs/schemas/README.md`, and `docs/schemas/schema.record-base.json` agree.
- MAY preserve legacy schema contents under `docs/schemas/legacy-*` until reconciliation is complete.

## Current Inputs

The active architecture draft is:

- `docs/adr/adr.schema-base.md`

The canonical schema namespace is being established at:

- `docs/schemas/`

Migrated schema artifacts currently include:

- `docs/schemas/adr.schema.json`
- `docs/schemas/adr-draft.schema.json`
- `docs/schemas/adr-active.schema.json`
- `docs/schemas/adr.schema-implementation.json`
- `docs/schemas/legacy-architecture.adr.schema-adr.json`
- `docs/schemas/legacy-architecture.adr.schema-implementation.json`

### Concern

- MUST add a migration table to `docs/schemas/README.md` mapping old paths to new paths.
- MUST document that `legacy-*` files are compatibility/migration markers, not canonical schema authority.
- SHOULD update active references to point at `docs/schemas/`.
- SHOULD NOT rewrite historical AAR/provenance records solely to update old paths.

## Integrated Review Findings

### KOIOS Review Findings

KOIOS supports the `metadata` + `content` envelope but finds provenance incomplete.

Required provenance improvements:

- `record_id`
- `schema_id`
- `schema_version`
- `record_version`
- `created_on`
- `updated_on`
- `source_artifacts`
- `derived_from`
- `evidence`
- `projections`

KOIOS recommends replacing overloaded origin fields with:

```json
"origin": {
  "type": "user_request | role_output | migration | import | derived",
  "method": "manual | intercom | filesystem | renderer | ingester | script",
  "actor": "ATHENA | VULCAN | KOIOS | HERMES | user | tool",
  "authority": "user | role | policy | adr | none"
}
```

KOIOS also recommends that Markdown projections declare source record identity, schema identity/version, projection method, generated-by actor or component, editability, and source-of-truth status.

### Concern

- MUST NOT overload `origin` with evidence, derivation, projection, and authority semantics.
- MUST add explicit source/evidence/projection fields before renderer/ingester implementation.
- SHOULD distinguish generated projections from editable projection surfaces.
- SHOULD document `source_artifacts` as cited/reviewed inputs and `derived_from` as transformed/inherited inputs so relationship labels do not blur provenance categories.
- MAY rename ambiguous fields such as `scope` or `domain` if they create product-domain confusion.

### HERMES Review Findings

HERMES supports `docs/schemas/` as the durable schema namespace and recommends keeping `legacy-*` files as migration markers.

HERMES finds the `metadata` / `content` split helpful if:

- `metadata` remains routing/provenance only;
- `content` stays family-owned;
- workspace-state JSON headers remain loose until a workspace-state schema exists.

HERMES recommends the next coherent state:

1. refine the ADR to settle provenance and namespace rules;
2. add the base schema JSON draft in `docs/schemas/`;
3. update the schemas README/migration table;
4. do not hand off to Vulcan until those three are internally consistent.

### Concern

- MUST keep workspace-state `state.md` / `active.md` metadata looser until a dedicated workspace-state schema exists.
- MUST NOT force current workspace surfaces into the schema-base contract prematurely.
- SHOULD NOT use redirects as the primary schema migration mechanism.
- MAY use short-lived compatibility mirrors only when path-based tooling requires them.

### VULCAN Review Findings

VULCAN says the first implementation slice is feasible only if narrow:

- base JSON schema;
- ADR-family schema;
- immutable Python models;
- one concrete `DraftAdrRecord`;
- JSON to Markdown renderer;
- Markdown to JSON ingester;
- round-trip tests preserving provenance.

VULCAN recommends module boundary:

```text
src/python/projectkoios/bootstrap/schema_records/
  models.py
  schemas.py
  adr_markdown.py
  paths.py
```

VULCAN says Athena must resolve before implementation:

- exact metadata fields and required/optional status;
- canonical origin object keys;
- canonical status enum;
- title placement semantics;
- projection-only vs editable Markdown input;
- exact Markdown grammar and rejection/normalization rules;
- schema `$id` strategy;
- whether first slice adds new base schema or mutates existing candidates.

### Concern

- MUST keep the first implementation slice out of GraphRAG `ingestors`.
- MUST keep schema-record implementation separate from current dirty GraphRAG work.
- MUST include deterministic renderer and strict ingester tests.
- SHOULD add new schema files rather than mutate legacy candidates until reconciliation is explicit.
- SHOULD use JSON Schema `$ref` plus `allOf` for the first family-schema composition strategy, backed by a local project schema registry if URL resolution is not available.

## Workstream A: Architecture Refinement

Refine `docs/adr/adr.schema-base.md` into a coherent draft that can authorize a narrow implementation brief later.

### Concern

- MUST define the top-level record envelope as exactly `metadata` and `content`.
- MUST define `content` as family-owned and deferred to the controlling schema.
- MUST define `metadata` as routing/provenance only.
- MUST include KOIOS provenance fields in metadata.
- MUST use canonical origin shape `{type, method, actor, authority}`.
- MUST clarify that workspace-state top JSON blocks are not yet required to conform.
- SHOULD define Markdown renders as projections or editable projections.
- MAY leave implementation-family records out of the first slice.

### Decisions Settled in Current Draft

1. Base records have exactly two top-level fields: `metadata` and `content`.
2. Required base metadata fields are `record_id`, `schema_id`, `schema_version`, `record_version`, `title`, `status`, `created_on`, `updated_on`, `origin`, `scope`, `repository`, `domain`, `source_artifacts`, `derived_from`, `evidence`, and `projections`.
3. `origin` uses `{type, method, actor, authority}` and does not carry evidence or projection semantics; the workplan itself uses `origin.method: manual` and `origin.actor: ATHENA`.
4. Base status enum is `draft`, `proposed`, `accepted`, `completed`, `superseded`, `rejected`.
5. `title` is metadata; Markdown renderers may project it into headings.
6. Markdown ADR files may be editable projection surfaces when strict ingest preserves provenance.
7. Schema `$id` values use `https://projectkoios.local/schemas/<filename>`.
8. Fatal ingest errors are reserved for invalid/missing metadata, missing required sections, required section order violations, malformed normative concern keywords, ambiguous heading depth, and any case that would lose metadata/content separation.
9. Otherwise valid but out-of-contract extra material is captured under `## Rejected` when deterministic mapping is possible.
10. ADR-family schemas use JSON Schema `$ref` plus `allOf` against `schema.record-base.json` for the first slice, with a local schema registry if needed.

### Decisions Still Open

None for the current pre-Vulcan schema-base slice after KOIOS provenance corrections are applied.

## Workstream B: Schema Namespace Migration

Make `docs/schemas/` coherent as a namespace before implementation.

### Concern

- MUST update `docs/schemas/README.md` with a migration table.
- MUST identify canonical files and legacy compatibility files.
- MUST preserve legacy contents while marking them non-authoritative.
- MUST update active docs/templates that point to old schema paths.
- SHOULD NOT edit historical AARs solely for path migration.

Current status: `docs/schemas/README.md` now contains namespace authority rules and a migration table.

### Migration Table Draft

| Old path | New path | Status |
|---|---|---|
| `docs/adr/adr.schema.json` | `docs/schemas/adr.schema.json` | canonical |
| `docs/adr/adr.schema-adr.json` | `docs/schemas/adr-active.schema.json` | candidate; migrated current/active schema; reconcile with legacy architecture copy |
| `docs/adr/adr.schema-implementation.json` | `docs/schemas/adr.schema-implementation.json` | candidate; reconcile with legacy architecture copy |
| `docs/architecture/adr.schema-adr.json` | `docs/schemas/legacy-architecture.adr.schema-adr.json` | legacy compatibility/migration marker |
| `docs/architecture/adr.schema-implementation.json` | `docs/schemas/legacy-architecture.adr.schema-implementation.json` | legacy compatibility/migration marker |

## Workstream C: Base Schema Draft

Create the first base schema JSON draft under `docs/schemas/`.

Current draft file:

- `docs/schemas/schema.record-base.json`

### Concern

- MUST require exactly top-level `metadata` and `content`.
- MUST reject extra top-level fields.
- MUST require the settled core metadata fields from Workstream A.
- MUST keep `content` as an object whose internal constraints are supplied by family schemas.
- SHOULD include `$id` in the `https://projectkoios.local/schemas/<filename>` form.
- MAY leave `content` permissive in the base schema.

## Workstream D: ADR-Family Schema Draft

Create an ADR-family schema that composes with or references the base schema.

Chosen files:

- `docs/schemas/adr-draft.schema.json` is the new draft ADR-family schema.
- `docs/schemas/adr-active.schema.json` preserves the migrated current ADR record schema candidate for reconciliation.

### Concern

- MUST constrain ADR `content`, not top-level record fields.
- MUST support `DraftAdrRecord` as the first concrete ADR state.
- MUST define required draft ADR content fields.
- MUST define Markdown section order and accepted section names.
- MUST use a 600-character limit for non-normative section descriptions unless a later schema changes it.
- MUST use JSON Schema `$ref` plus `allOf` composition against the base schema for the first slice.
- MUST provide a `## Rejected` surface for otherwise valid extra Markdown content that is not compliant with the controlling schema but can be captured deterministically.
- SHOULD defer accepted/completed/superseded ADR states until later slices.

## Workstream E: Markdown Render and Ingest Contract

Define the controlled Markdown render before implementation.

General form:

```text
## <Section>

<Non-normative descriptive paragraph. Length limit defined by controlling schema.>

### Concern

- MUST ...
- MUST NOT ...
- SHOULD ...
- SHOULD NOT ...
- MAY ...

### <Subsection>
```

### Concern

- MUST preserve metadata/content separation through JSON -> Markdown -> JSON.
- MUST preserve provenance fields exactly unless an explicit ingester rule allows normalization.
- MUST treat Markdown ADR renders as editable projection input only when strict ingest preserves provenance.
- MUST define deterministic section ordering.
- MUST reject required-section omissions.
- MUST reject required metadata violations, required section order violations, malformed normative concern keywords, ambiguous heading depth, and any case that would lose metadata/content separation.
- SHOULD capture otherwise valid extra sections, unknown subsections, non-normative overflow text, duplicate optional sections, or other deterministic out-of-contract content under `## Rejected`.
- MAY normalize purely presentational whitespace, line wrapping, and ordered concern grouping if tests prove semantic equivalence.

## Workstream F: Implementation Handoff Preparation

Prepare a Vulcan-ready implementation brief only after Workstreams A-E are coherent.

### Concern

- MUST NOT start implementation from Athena.
- MUST NOT include implementation records, workspace-state records, lifecycle engines, or broad existing-doc migration in the first slice.
- MUST isolate schema-record implementation from GraphRAG implementation work.
- SHOULD recommend `src/python/projectkoios/bootstrap/schema_records/` as the implementation package.
- SHOULD require tests before CLI integration.

Expected first implementation slice:

1. `SchemaRecordBase` and metadata models.
2. Base JSON schema under `docs/schemas/`.
3. ADR-family schema for draft ADRs.
4. `AdrRecordBase` constrained abstraction.
5. `DraftAdrRecord` concrete implementation.
6. JSON -> Markdown renderer.
7. Markdown -> JSON ingester.
8. Round-trip tests preserving provenance.
9. Path tests proving canonical schema loading from `docs/schemas/`.

## Open Questions

None for the current pre-Vulcan schema-base slice.

## Exit Criteria

This workplan is complete when:

- `docs/adr/adr.schema-base.md` incorporates KOIOS, HERMES, and VULCAN review points;
- `docs/schemas/README.md` includes a migration table and authority rules;
- a base schema JSON draft exists under `docs/schemas/`;
- `docs/schemas/adr-draft.schema.json` exists and the ADR-family schema strategy is chosen;
- Markdown render/ingest grammar is specified enough for tests;
- a separate Vulcan implementation brief can be written without hidden chat context.
