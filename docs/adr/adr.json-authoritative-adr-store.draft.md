```json
{
  "title": "JSON-Authoritative ADR Store",
  "artifact_type": "adr-proposal",
  "status": "draft",
  "datetime": "20260711.135000Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "docs/adr authority, JSON ADR records, Markdown projections, migration policy",
  "source_architecture": [
    "docs/architecture/architecture.adr-bidirectional-objects.md",
    "docs/architecture/architecture.json-adr-storage-topology.md"
  ],
  "source_brief": "docs/plans/implementation-brief.20260711.134200_adr-bidirectional-object-canary-slice-0.md",
  "next_owner": "HERMES_USER"
}
```

# ADR 20260711.135000Z: JSON-Authoritative ADR Store

## Status

draft

## Context

USER clarified the desired end state for ADR rationalization:

- mass convert ADR Markdown to JSON;
- make JSON the authoritative ADR record format;
- keep Markdown as generated projection/review surface unless explicitly marked source-only/provenance.

This is an authority-changing decision. It is broader than `adr-bidirectional-object-canary-slice-0`, which only proves one-source canary mechanics. The canary-first posture remains useful as migration evidence, but it does not itself change repository authority.

Current related surfaces:

- `docs/architecture/architecture.adr-bidirectional-objects.md` defines a candidate envelope, generated-projection bidirectional semantics, classification/disposition metadata, provenance proportionality, and canary-first mechanics.
- `docs/architecture/architecture.json-adr-storage-topology.md` defines JSON document storage topology, generic document-store separation, SQLite pilot storage guarantees, and deferred storage authority.
- `docs/adr/adr.json-database-for-adr-storage.draft.md` already proposes JSON files as canonical storage with Markdown as render/presentation and SQLite as index/cache unless promoted.
- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` controls ADR lifecycle/status vocabulary and explicitly does not authorize bulk rewrites, status migration, schema changes, or file renames by implication.
- KOIOS classification/provenance inputs identify `docs/adr/` as heterogeneous: current decisions, source/provenance drafts, architecture blueprints, policy/process surfaces, template/schema/contract documents, implementation workflow support, and product/future-system drafts.

The repository needs an explicit authority-change ADR before mass conversion, schema publication, source/projection policy changes, or database authority promotion can proceed.

## Decision

If accepted, Project Koios bootstrap ADRs SHALL migrate toward JSON-authoritative ADR records after an approved migration plan and gates are satisfied.

### Authority target

After approved migration:

1. JSON records SHALL be the authoritative ADR record format for migrated ADRs.
2. Markdown under `docs/adr/` SHALL become generated projection/review/navigation surface for migrated ADRs unless a file is explicitly marked `source-only` or `provenance-only` by the migration evidence.
3. Existing Markdown sources SHALL remain preserved as audit/provenance either in place, under an approved provenance location, or through hash-addressed evidence. The final disposition must be decided by the migration plan before mutation.
4. JSON authority SHALL be file-based JSON authority by default, not SQLite/database authority.
5. SQLite or another database MAY be used as an operational index/cache/import-export store behind the generic document-store adapter, but it SHALL NOT become authoritative unless a later accepted ADR explicitly promotes database authority.

### Relationship to canary-first work

The accepted end state MAY supersede the prior canary-first posture only after this ADR or a successor authority decision is accepted.

Until then:

- `adr-bidirectional-object-canary-slice-0` remains evidence/mechanics only;
- no mass conversion is authorized;
- no Markdown authority demotion is authorized;
- no schema publication/change is authorized;
- no database authority is authorized.

After acceptance, the canary becomes Phase 0 evidence for the migration path rather than the end state.

## Migration phases and gates

### Phase 0: One-source canary

Purpose: prove one ADR source can become a candidate JSON object plus generated projection without mutating source authority.

Candidate source:

- `docs/adr/adr.json-schemas.draft.md`

Gates:

- exactly one source converted;
- source Markdown unmodified;
- candidate `AdrBidirectionalObject` evidence produced;
- generated projection parse-back semantic equality proven;
- unsupported fields preserved in sidecar/evidence;
- source/projection/schema hashes recorded;
- no `docs/schemas/` changes;
- no mutable DB commit;
- no repository authority change.

### Phase 1: Corpus inventory and classification

Purpose: classify every ADR Markdown file before migration.

Required outputs:

- inventory of `docs/adr/*.md` and non-ADR index/control files such as `README.md`;
- observed status/casing and parse confidence;
- proposed hierarchy category/disposition;
- source/provenance vs current decision vs policy/process vs architecture blueprint vs template/schema/contract vs implementation workflow support vs product/future-system draft;
- uncertainty flags and required owner/domain review;
- list of files excluded from automatic conversion.

Gate: HERMES/USER acceptance of inventory/classification before any corpus mutation.

### Phase 2: Schema and envelope authority proposal

Purpose: decide the JSON record and envelope schema surfaces before mass conversion.

Required decisions:

- whether `AdrBidirectionalObject` envelope schema is published under `docs/schemas/` or remains implementation-local;
- how `content` references `docs/schemas/adr.schema.json` and schema versions;
- how classification/disposition metadata is represented outside `content`;
- how sidecar/provenance fields are versioned;
- compatibility rules for existing conformance artifacts.

Gate: accepted schema/versioning decision before generated JSON records are treated as authoritative.

### Phase 3: Dry-run corpus conversion

Purpose: generate JSON records and projections for the selected corpus without source mutation.

Required evidence:

- per-file conversion report;
- source hashes;
- generated JSON hashes;
- generated projection hashes;
- validation status;
- sidecar/provenance status;
- conflict classifications;
- excluded/blocked records.

Gate: HERMES/USER review of dry-run evidence and conflicts.

### Phase 4: Authority cutover package

Purpose: prepare the actual authority transition.

Required decisions:

- JSON record directory/path convention;
- Markdown projection path convention;
- where source-only/provenance Markdown remains;
- how generated projections are marked;
- update plan for indexes and architecture references;
- rollback plan;
- package-level validation commands.

Gate: explicit HERMES/USER approval of cutover package.

### Phase 5: Committed migration

Purpose: execute the approved conversion/migration package.

Rules:

- convert only approved files;
- preserve source hashes and audit trail;
- do not silently supersede drafts;
- record old/new paths and authority modes;
- generate projections deterministically;
- validate JSON records and projection equality;
- prove no unapproved ADR source mutation occurred.

Gate: post-migration ATHENA/KOIOS/HERMES review before acceptance.

## Conflict policy

No silent overwrite is allowed.

Conflict states SHALL include at least:

- `no_conflict`: source Markdown converts to JSON and generated projection round-trips semantically.
- `unsupported_fields_preserved`: source fields are outside the ADR content schema but preserved in sidecar/evidence.
- `status_normalization_required`: source status/casing differs from canonical vocabulary and needs explicit mapping.
- `lossy_requires_review`: conversion would drop or normalize material not safely preserved.
- `source_ambiguous`: source Markdown cannot be parsed with sufficient confidence.
- `domain_review_required`: product/future-system ownership or bootstrap authority is unclear.
- `authority_conflict`: existing Markdown, generated JSON, prior dev conformance artifact, or database/index state disagree.

Conflict resolution rules:

1. JSON MUST NOT replace Markdown authority for a conflicted record until the conflict is resolved or the record is explicitly excluded.
2. Unsupported fields SHOULD be preserved in sidecar/evidence rather than forced into ADR `content`.
3. Lossy conversion MUST require human review.
4. Existing hand-authored Markdown edits MUST be preserved as source evidence even when JSON becomes authority.
5. Generated projections MUST be visibly marked so they are not mistaken for hand-authored source ADRs.

## Status and lifecycle normalization

This ADR does not itself rewrite statuses.

Migration tooling and evidence SHALL:

- preserve observed status text and casing in source refs or sidecar evidence;
- map statuses to canonical lifecycle vocabulary only through an approved migration map;
- distinguish ADR lifecycle status from workspace active work state;
- avoid ambiguous phrases such as `active ADRs` unless referring specifically to documents whose ADR lifecycle status is `active`;
- prefer precise language such as `documents marked active/accepted pending hierarchy review`, `current conformance artifact`, `source Markdown`, `generated projection`, or `JSON authority candidate`.

The initial canonical vocabulary remains controlled by `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` unless a later accepted ADR changes it.

Status normalization options to decide in migration planning:

- normalize only JSON `content.status` while preserving observed source status/casing in sidecar;
- preserve original status/casing in source-only/provenance Markdown;
- exclude ambiguous or domain-unclear documents from automatic authority cutover.

## Sidecar and provenance handling

JSON authority does not mean all source material must fit the ADR content schema.

Sidecar/provenance evidence SHALL preserve:

- source path;
- source hash;
- observed source status/casing;
- observed source date;
- source title;
- unsupported fields such as legacy `routing.*` or unsupported link shapes;
- normalized fields and original values;
- inferred fields and rationale;
- source/projection/schema version and hash;
- conversion warnings and lossiness classification;
- prior dev evidence or conformance artifact refs where relevant.

Provenance should be proportional. It must be strong enough to prevent authority loss, silent supersession, or source-context loss, but it should not become ceremony that blocks bounded conversion when the evidence is already inspectable.

## Schema authority and versioning

A JSON-authoritative ADR store requires explicit schema authority.

Required decisions before corpus cutover:

- the canonical ADR content schema path and versioning rule;
- whether and where an `AdrBidirectionalObject` envelope schema is published;
- whether sidecar/provenance schema is formalized or remains evidence structure;
- how generated projections record schema version/hash;
- how migration handles records that cannot validate against the current schema;
- how schema changes are reviewed without mutating historical evidence.

Default until accepted otherwise:

- `docs/schemas/adr.schema.json` remains the content payload schema;
- no envelope schema is published under `docs/schemas/`;
- sidecar/provenance remains evidence structure;
- schema publication or changes require explicit HERMES/USER approval.

## Storage authority relationship

The target authority is file JSON authority unless later changed.

| Surface | Authority after accepted migration | Notes |
|---|---|---|
| JSON ADR record files | Authoritative for migrated records | Path convention to be decided in migration package. |
| Markdown projections | Generated review/navigation surface | Not source authority unless explicitly marked source-only/provenance. |
| Source/provenance Markdown | Audit/provenance evidence | May remain in place or move only under approved plan. |
| SQLite/database | Operational index/cache/import-export store by default | ACID under normal configuration, but not authority unless later ADR promotes. |
| Dev canary/conformance artifacts | Evidence | Not repository-wide authority by themselves. |
| Sidecar/provenance files | Audit and conversion evidence | Authority level depends on later schema/storage decision. |

SQLite/database caveats from storage topology remain controlling:

- do not commit mutable DB files by default;
- do not weaken durability settings such as `synchronous=OFF` without explicit documented approval;
- do not assume server-style multi-writer semantics;
- preserve the generic storage adapter boundary.

## What happens to `docs/adr/*.md` after migration

The final Markdown disposition must be explicit per category.

Allowed target dispositions:

1. `generated_projection`: Markdown is generated from JSON and visibly marked as generated.
2. `source_only_provenance`: Markdown remains source/provenance and is not regenerated.
3. `excluded_pending_review`: Markdown remains as-is until conflict/domain/status review completes.
4. `index_or_control_surface`: files such as README/index surfaces remain Markdown control/navigation unless separately migrated.
5. `archived_source`: source Markdown may move to an approved archive/provenance location only if the migration package explicitly authorizes the move and preserves old/new refs and hashes.

No Markdown file may be deleted, overwritten, moved, renamed, or status-normalized by implication from this draft ADR.

## Rollback and audit trail

The migration package SHALL include rollback and audit evidence:

- manifest of every source file, generated JSON record, generated projection, and sidecar/evidence file;
- old/new paths and hashes;
- authority mode before/after;
- conflict decisions;
- records excluded from migration;
- validation commands and outputs;
- reviewer signoff references;
- rollback procedure to restore prior Markdown-authoritative behavior for migrated records if acceptance fails.

No silent supersession is allowed:

- source drafts must not be marked superseded solely because they were converted;
- accepted/current decisions must not lose source trace;
- product/future-system drafts must not become bootstrap authority by conversion;
- generated projections must not be mistaken for source Markdown.

## Consequences

Positive consequences:

- ADRs become easier to validate, query, diff structurally, and project into multiple review surfaces.
- Status/lifecycle inconsistencies become explicit migration findings rather than hidden prose drift.
- Markdown remains available for human review while JSON owns migrated record authority.
- Database/index use remains decoupled from repository authority.

Tradeoffs:

- Migration requires explicit inventory, conflict handling, and review gates.
- Existing Markdown habits must adapt to generated projections and JSON authority.
- Some current ADR-space files may be excluded or remain provenance-only until hierarchy/domain questions are resolved.
- Schema/version governance becomes more important because JSON becomes authoritative.

## Non-goals

This draft does not authorize:

- implementation;
- immediate mass conversion;
- mutation of any `docs/adr/*.md` file;
- schema publication or schema changes;
- database authority;
- committed mutable DB files;
- file moves or renames;
- status normalization;
- draft supersession;
- product/future-system authority promotion;
- hand-authored Markdown ingest without accepted conflict policy and migration gates.

## Acceptance criteria for this ADR decision

This ADR may be accepted only if HERMES/USER agrees that:

1. JSON file records are the intended authority target for migrated ADRs.
2. Markdown projections become generated review/navigation surfaces for migrated ADRs unless explicitly marked source-only/provenance.
3. File JSON authority is the default storage authority, not SQLite/database authority.
4. Mass conversion requires inventory, dry-run evidence, conflict resolution, schema/version decisions, and cutover approval.
5. Observed status/casing and unsupported source fields remain preserved in sidecar/provenance evidence.
6. Existing Markdown files are not silently deleted, overwritten, moved, renamed, status-normalized, or superseded.
7. The prior canary-first work becomes Phase 0 evidence, not a substitute for authority approval.

## Implementation brief, if accepted

If HERMES/USER accepts this ADR direction, ATHENA should draft a migration planning brief before VULCAN implementation.

Recommended next brief:

```text
json-authoritative-adr-store-migration-plan-slice-0
```

Scope of that brief:

- no source mutation;
- inventory and classification only;
- proposed JSON record path convention;
- proposed projection path convention;
- schema/envelope versioning proposal;
- conflict taxonomy validation on the corpus;
- dry-run migration plan.

The existing `adr-bidirectional-object-canary-slice-0` may remain a prerequisite or be folded into Phase 0 depending on HERMES/USER decision.

## Review request

HERMES/USER should review this draft as an authority-change proposal.

Until accepted, the repository remains under the prior authority boundaries: no mass migration, no Markdown authority demotion, no schema publication/change, no DB authority, and no ADR source mutation.
