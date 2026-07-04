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

## Canonical schema files

- `adr.schema.json` — canonical ADR content schema migrated from `docs/adr/`.
- `schema.record-base.json` — draft base `metadata` + `content` envelope schema.
- `adr-draft.schema.json` — draft ADR record schema using the base envelope.
- `adr-active.schema.json` — migrated current ADR record schema candidate; requires reconciliation with legacy architecture copy.
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

`metadata` carries identity, routing, provenance, and domain typing. `content` is
family-specific and is constrained by the controlling family schema.

Current base and ADR-family schema drafts:

- `schema.record-base.json`
- `adr-draft.schema.json`

The migrated current ADR schema is retained as:

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
