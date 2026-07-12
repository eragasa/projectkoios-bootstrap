# Schemas

Machine-readable schema artifacts live here.

`docs/schemas/` is the durable schema namespace for Project Koios bootstrap
documents. Human-readable ADRs and architecture notes may reference these files,
but SHOULD NOT host canonical JSON schema artifacts themselves.

## Namespace authority

### Concern

- MUST treat `docs/schemas/` as the canonical home for machine-readable schema artifacts.
- MUST NOT treat `legacy-*` files as co-authoritative with canonical schema files.
- SHOULD keep legacy schema contents only as migration markers until reconciliation is complete.
- SHOULD update active docs and templates to reference `docs/schemas/`.
- SHOULD NOT rewrite historical AARs or provenance records solely to update old paths.
- MAY add short-lived compatibility mirrors only when path-based tooling requires them.

## Schema-family layering

The current ADR schema-family boundary is layered:

1. `adr.schema.json` is the current ADR content-shape schema until a later approved slice wraps, replaces, or retires it.
2. `schema.record-base.json` is the draft record-envelope direction for schema-backed records with top-level `metadata` and `content`.
3. `adr-draft.schema.json` demonstrates ADR-family composition with the base envelope.
4. `adr-active.schema.json` is a compatibility/reconciliation candidate, not co-authoritative with the newer base-envelope family by implication.

`docs/architecture/architecture.schema-record-envelope.md` records the architecture direction for the record-envelope model. It is architecture direction only, not machine-readable schema authority; it does not make `schema.record-base.json` accepted record-envelope authority or make `metadata` + `content` the current universal emitted-record shape.

Markdown under `docs/adr/` remains source/control for unmigrated records. Generated projections remain evidence or review/navigation surfaces unless a later accepted migration/cutover package changes the specific file's disposition.

`routing` and `dcn` are not current ADR content-schema fields. `routing` defaults to sidecar/provenance preservation unless later promoted by workflow/envelope decision. `dcn` remains unresolved namespace/control metadata. `workflow_binding` is optional schema content, not operational workflow authority.

## Canonical schema files

- `adr.schema.json` — current ADR content-shape schema migrated from `docs/adr/`; not a complete record envelope.
- `schema.record-base.json` — draft base `metadata` + `content` envelope schema.
- `adr-draft.schema.json` — draft ADR record schema using the base envelope.
- `adr-active.schema.json` — migrated current ADR record schema candidate; compatibility/reconciliation candidate until wrapped, replaced, retired, or preserved for compatibility.
- `adr.schema-implementation.json` — implementation record schema candidate; requires reconciliation with legacy architecture copy.

## Legacy migration markers

- `legacy-architecture.adr.schema-adr.json` — migrated legacy architecture-copy ADR record schema requiring reconciliation.
- `legacy-architecture.adr.schema-implementation.json` — migrated legacy architecture-copy implementation record schema requiring reconciliation.

The `legacy-*` files preserve previous schema contents while the schema-family
base-class architecture is reconciled. They are not canonical unless a later ADR
explicitly promotes them.

## Migration table

| Old path | New path | Authority status | Notes |
|---|---|---|---|
| `docs/adr/adr.schema.json` | `docs/schemas/adr.schema.json` | canonical | Existing canonical ADR content schema moved to schema namespace. |
| `docs/adr/adr.schema-adr.json` | `docs/schemas/adr-active.schema.json` | candidate | Current ADR record schema candidate renamed as active/current schema; reconcile against base schema and legacy architecture copy. |
| `docs/adr/adr.schema-implementation.json` | `docs/schemas/adr.schema-implementation.json` | candidate | Implementation record schema candidate; reconcile in later implementation-family slice. |
| `docs/architecture/adr.schema-adr.json` | `docs/schemas/legacy-architecture.adr.schema-adr.json` | legacy migration marker | Preserves previous architecture-copy content; not co-authoritative. |
| `docs/architecture/adr.schema-implementation.json` | `docs/schemas/legacy-architecture.adr.schema-implementation.json` | legacy migration marker | Preserves previous architecture-copy content; not co-authoritative. |

## Base record direction

Schema-backed records use exactly two top-level fields:

   - `metadata`
   - `content`

`metadata` carries identity, provenance, evidence, projection, repository, and domain typing. `content` is
family-specific and is constrained by the controlling family schema. Do not read legacy `routing` prose as a current content-schema field unless a later schema-change slice explicitly adds it.

Current base and ADR-family schema drafts:

- `schema.record-base.json`
- `adr-draft.schema.json`

The migrated current ADR schema candidate is retained for reconciliation as:

- `adr-active.schema.json`

Recommended schema `$id` form:

- `https://projectkoios.local/schemas/<filename>`

## Composition and ingest direction

Family schemas SHOULD compose the base schema with JSON Schema `$ref` plus
`allOf` for the first schema-record implementation slice. If the validator cannot
resolve project-local `$id` URLs directly, implementation SHOULD provide a local
schema registry that maps `https://projectkoios.local/schemas/<filename>` to the
matching file in `docs/schemas/`.

Markdown ADR ingest is strict for required structure. Missing or invalid
metadata, missing required sections, required section-order violations, malformed
normative concern keywords, ambiguous heading depth, or loss of metadata/content
separation are fatal ingest errors. Otherwise valid but out-of-contract extra
material MAY be captured under `## Rejected` when deterministic mapping is
possible.
