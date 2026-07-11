```json
{
  "title": "Architecture extraction brief: ADR schema-base",
  "artifact_type": "architecture-extraction-planning-brief",
  "status": "proposal-only-pending-hermes-user-acceptance",
  "datetime": "20260711.184325Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-schema-base-architecture-extraction-planning-slice-13",
  "target_source": "docs/adr/adr.schema-base.md",
  "source_disposition_brief": "docs/plans/source-disposition-brief.20260711.183536_adr-schema-base.md",
  "hermes_decision": "docs/reviews/hermes-decision.20260711.184325_adr-schema-base-architecture-extraction-planning-slice-13.md",
  "source_mutation": false,
  "schema_mutation": false,
  "architecture_artifact_created": false,
  "authority_change": false,
  "next_owner": "HERMES_USER"
}
```

# Architecture extraction brief 20260711.184325: ADR schema-base

## Purpose

Plan a later ATHENA-owned extraction of still-current schema-family record-envelope concepts from `docs/adr/adr.schema-base.md` into a clearer durable architecture surface.

This brief is proposal-only. It does not edit `docs/adr/adr.schema-base.md`, edit `docs/schemas/`, create the final architecture extraction artifact, change lifecycle state, accept, activate, supersede, reject, promote, demote, move, rename, delete, archive, split, generate projections/JSON records, migrate, or cut over authority.

## Accepted source disposition

HERMES accepted the Slice 12 disposition for `docs/adr/adr.schema-base.md`:

```text
source/provenance for schema-family record-envelope architecture; not current ADR authority until lifecycle/status and surface placement are resolved
```

This planning brief uses that disposition as its starting boundary.

The embedded JSON value:

```json
"status": "draft"
```

is observed source metadata only. It is not inferred top-level ADR lifecycle status.

## Source basis

Target source:

```text
docs/adr/adr.schema-base.md
```

Planning inputs:

```text
docs/reviews/hermes-decision.20260711.184325_adr-schema-base-architecture-extraction-planning-slice-13.md
docs/reviews/hermes-acceptance.20260711.184119_adr-schema-base-source-disposition-planning-slice-12.md
docs/plans/source-disposition-brief.20260711.183536_adr-schema-base.md
docs/reviews/hermes-acceptance.20260711.155200_adr-semantic-rationalization-six-entry-slice-5.md
docs/reviews/semantic-rationalization.20260711_adr-six-entry-slice-5.md
docs/schemas/README.md
docs/adr/adr.adr-template-schema-contract.md
docs/adr/adr.adr-lifecycle.20260705.011836Z.md
docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md
```

Current boundaries to preserve:

- `docs/adr/adr.adr-template-schema-contract.md` is current ADR template/schema contract authority.
- `docs/adr/adr.schema-base.md` remains unchanged source/provenance.
- `docs/schemas/adr.schema.json` is current ADR content-shape schema until later approved replacement/wrap/retirement.
- `docs/schemas/schema.record-base.json` remains draft record-envelope direction, not current universal emitted-record authority.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated projections remain evidence/review surfaces unless later cutover changes a file's disposition.

## Useful/current concepts to extract

A later architecture extraction should consider preserving these still-useful concepts, with current boundaries tightened:

| Source concept | Current extraction treatment |
|---|---|
| Shared `metadata` + `content` envelope | Useful as draft schema-backed record-envelope direction; do not claim universal current emitted-record authority. |
| Family-specific records constrain `content` | Useful architecture pattern for ADR, implementation, and possible workspace-state families; keep family-specific policy outside the base. |
| Common metadata fields | Useful as candidate record-envelope metadata: identity, schema identity/versioning, title, status, timestamps, provenance, domain, evidence, projections. |
| `origin` vs provenance/evidence separation | Useful and current as design principle: origin should not be overloaded with source evidence or derivation. |
| `source_artifacts`, `derived_from`, `evidence`, `projections` separation | Useful as provenance model input; should remain envelope/provenance architecture, not ADR content schema. |
| Schema `$id` form `https://projectkoios.local/schemas/<filename>` | Useful if future schema-family implementation needs local schema registry/resolver; already echoed in schema README/workplans. |
| Machine-readable schemas under `docs/schemas/` | Current namespace guidance already exists in `docs/schemas/README.md`; extraction can cite rather than recreate authority. |
| Markdown render surfaces as human-readable projections/companions | Useful only with boundary: existing Markdown remains source/control for unmigrated records. |
| Renderer/ingester needs deterministic mapping and provenance preservation | Useful future implementation concern; should remain deferred until an approved implementation/schema slice. |
| Fatal ingest vs mappable out-of-contract handling | Useful future parser/ingester design input; not current broad ingest authority. |

## Stale, ahead-of-authority, or superseded concepts

A later extraction should not carry these forward as current authority without explicit qualification:

| Source concept | Classification | Extraction handling |
|---|---|---|
| Source lacks top-level `## Status` but embeds `status: draft` in JSON | unsafe lifecycle/status placement | Preserve as source metadata; do not infer top-level ADR status. |
| Editable Markdown declares itself as projection/source-of-truth in embedded metadata | ahead/confusing relative to current Markdown source/control boundary | Reframe: Markdown remains source/control for unmigrated records; generated projections are evidence/review surfaces unless later cutover. |
| Rendered document MUST NOT become separate authority when schema-backed record exists | ahead of current cutover | Keep only as target future after record-envelope/cutover authority exists. |
| Markdown ADR renders may be editable projection surfaces when ingester maps them back | future mode | Defer to later ingest/projection architecture and tests. |
| Broad renderer/ingester implementation plan | implementation planning, not architecture authority | Extract only as deferred candidate requirements; no implementation authorization. |
| Base class MUST define fields/invariants common to all schema-backed repository document records | too broad if read as current authority | Restate as candidate/draft direction for schema-backed records, not all repository documents. |
| Family schemas MUST extend base class | ahead of current schema authority | Reframe as future schema-family goal pending schema-change slice. |
| Existing schema files may need migration or compatibility aliases | still plausible but not authorized | Keep as future reconciliation topic, no migration now. |
| Duplicate schema file behavior tests/compatibility mirrors | implementation/schema repair concern | Defer to schema-change or implementation slice. |
| Current file as an ADR authority surface | unsafe | Treat as source/provenance, not current ADR authority. |

## Recommended future durable surface

Recommended future durable surface:

```text
docs/architecture/architecture.schema-record-envelope.md
```

Rationale:

- The useful material is primarily architecture/specification for schema-family record envelopes.
- The current source is not safe as ADR authority because lifecycle/status and surface placement are unresolved.
- An architecture surface can preserve design direction without accepting a new ADR or mutating the source.
- Schema changes remain separately gated under `docs/schemas/`.
- Implementation remains separately gated for VULCAN.

This path is a recommendation only. HERMES/USER should explicitly approve the final path before creation.

## Surface placement decision

Recommended placement by concern:

| Concern | Future surface |
|---|---|
| Schema-family record-envelope architecture, metadata/content layering, provenance/evidence separation | `docs/architecture/architecture.schema-record-envelope.md` |
| ADR content-schema contract and Markdown/source/projection boundaries | Existing `docs/adr/adr.adr-template-schema-contract.md` and later accepted amendments only |
| Machine-readable schema namespace and file list | `docs/schemas/README.md` for documentation; JSON schema files only by separate schema-change slice |
| Machine-readable envelope schema authority | Future explicit schema-change proposal/ADR plus edits under `docs/schemas/`, not this extraction |
| Lifecycle status rules | Existing active lifecycle ADR, unless a later lifecycle amendment is approved |
| Renderer/ingester implementation requirements | Future implementation brief for VULCAN after architecture/schema boundaries are accepted |
| Old `docs/adr/adr.schema-base.md` disposition | Review/plan/source-disposition artifacts; leave source unchanged unless later approved |

Not recommended as first extraction:

- A successor ADR: too strong until HERMES/USER wants record-envelope authority acceptance.
- A direct `docs/schemas/README.md` update: useful later, but insufficient to carry architecture.
- A schema-change proposal: premature before extracted architecture is reviewed.
- In-place source revision: unsafe provenance/lifecycle mutation.

## Proposed later extraction scope

A future extraction slice should create one architecture artifact only, with sections such as:

1. Status and non-authority boundary.
2. Source/provenance basis, including `docs/adr/adr.schema-base.md`.
3. Current schema-family control surfaces.
4. Record-envelope purpose and non-purpose.
5. `metadata` + `content` model as draft direction.
6. Metadata field families and provenance/evidence separation.
7. Relationship to ADR content schema.
8. Relationship to Markdown source/control and generated projections.
9. Relationship to `docs/schemas/README.md` and machine-readable schema files.
10. Deferred renderer/ingester requirements.
11. Explicit non-actions and later gates.

The artifact should avoid copying `docs/adr/adr.schema-base.md` wholesale. It should extract and reconcile only still-current concepts.

## Acceptance criteria for later extraction

A later extraction artifact should be accepted only if it:

1. Creates exactly one approved architecture/planning artifact.
2. Does not edit `docs/adr/adr.schema-base.md`.
3. Does not edit `docs/schemas/`.
4. Preserves embedded JSON `status: draft` as observed source metadata.
5. States that `docs/adr/adr.schema-base.md` is source/provenance, not current ADR authority.
6. States that `docs/schemas/adr.schema.json` remains current ADR content-shape schema.
7. States that `docs/schemas/schema.record-base.json` remains draft record-envelope direction.
8. Does not claim `metadata` + `content` is current universal emitted-record authority.
9. Separates ADR content schema from record-envelope metadata and sidecar/provenance evidence.
10. Preserves Markdown-under-`docs/adr/` source/control for unmigrated records.
11. Treats generated projections as evidence/review surfaces unless later cutover changes disposition.
12. Defers renderer/ingester implementation and schema edits to later approved slices.
13. Identifies stale/ahead-of-authority source claims rather than carrying them forward unqualified.
14. Does not authorize lifecycle/status repair, source mutation, schema change, migration, generated projections, database/storage authority, or JSON cutover.
15. Includes closeout evidence showing forbidden surfaces were not mutated.

## Explicit source/schema authority boundaries

This brief and any later extraction planning must preserve:

- `docs/adr/adr.schema-base.md` remains unchanged source/provenance unless HERMES/USER separately approves source mutation.
- The embedded JSON `status: draft` remains observed source metadata, not inferred top-level ADR lifecycle status.
- `docs/schemas/adr.schema.json` remains current ADR content-shape schema until explicitly wrapped, replaced, or retired.
- `docs/schemas/schema.record-base.json` remains draft record-envelope direction.
- No `docs/schemas/` file is changed without a schema-change slice.
- No existing ADR file is accepted, activated, superseded, rejected, promoted, demoted, moved, renamed, deleted, archived, split, normalized, or migrated by extraction planning.
- No generated projection, JSON record, database/storage authority, migration, or cutover is created by extraction planning.

## Recommended next transition

If HERMES/USER accepts this architecture-extraction brief, the next bounded ATHENA slice should create one architecture artifact at an approved path, preferably:

```text
docs/architecture/architecture.schema-record-envelope.md
```

Candidate slice name:

```text
adr-schema-base-architecture-extraction-slice-14
```

The slice should remain architecture-only and source-preserving unless HERMES/USER explicitly expands scope.

## Closeout validation expectations

ATHENA/HERMES closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Expected result for this planning slice: no mutation to `docs/adr/adr.schema-base.md`, no `docs/schemas/` mutation, no Slice 4 dry-run evidence mutation, and clean diff hygiene. Any pre-existing `docs/adr/` additions should be identified separately from this planning brief.
