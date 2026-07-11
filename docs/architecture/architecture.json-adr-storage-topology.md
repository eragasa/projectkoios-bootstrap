---
status: pilot-as-built
date: 20260711.032904Z
last_updated: 20260711.062407Z
back_to: architecture.00
controlled_by: docs/adr/adr.json-database-for-adr-storage.draft.md
---

# JSON ADR Storage Topology

## Purpose

This architecture note is the blueprint for the structured ADR storage system in `projectkoios-bootstrap`.

Before implementation, it defines the intended long-term system shape, authority boundaries, invariants, and evidence questions that implementation must answer. Implementation work is sliced from this blueprint into bounded briefs, plans, and patches. After implementation, this document is revised into as-built documentation that describes the system actually delivered, including validated behavior, known deviations, and remaining decision gaps.

As of the one-ADR pilot completed at `20260711.035759Z`, this document records both the longer-term architecture blueprint and the pilot as-built state. The as-built state is evidence for the next ADR decision; it is not, by itself, a durable promotion of database authority for all ADRs.

It exists because ADR storage authority has more moving parts than a single implementation brief can safely carry:

- canonical ADR content model
- operational database behavior
- JSON checkpoint/export behavior
- Markdown projection behavior under `docs/adr/`
- git review and merge implications
- authority boundaries between accepted ADRs, generated projections, pilot evidence, and local runtime state

The controlling ADR owns the durable decision. This architecture note describes the topology, terms, invariants, and pilot questions that the ADR must resolve or supersede.

## Scope

In scope:

- ADR records for this bootstrap repository.
- Separation between a generalized JSON document database substrate and ADR-specific document-family code.
- Schema-backed ADR JSON records compatible with `docs/schemas/adr.schema.json`.
- SQLite as the first operational backend for the generalized JSON document database pilot.
- JSON checkpoint/export artifacts for repository review.
- Markdown ADR projection surfaces under `docs/adr/`.
- One-ADR pilot evidence using `docs/adr/adr.json-database-for-adr-storage.draft.md` as the representative source.

Out of scope:

- Bulk ADR migration.
- Product-domain architecture in the `projectkoios` mothership.
- Generic document ingestion beyond the minimal JSON document database substrate needed for this bootstrap pilot.
- A broad generic database framework beyond storing/querying JSON documents behind an adapter boundary.
- Removing Markdown review/navigation surfaces.

## Control

This note is controlled by:

- `docs/adr/adr.json-database-for-adr-storage.draft.md`

Related implementation planning is currently captured in:

- `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md`
- `docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md`

The implementation brief may define a bounded pilot, but it must not silently change ADR storage authority. Any durable authority change requires ADR revision, replacement, promotion, acceptance, or supersession through the normal ADR lifecycle.

This architecture note is the controlling blueprint/as-built surface for the system shape. VULCAN implementation reports must identify any deviations from this blueprint. After implementation evidence exists, ATHENA must update this note from intended blueprint to as-built documentation or explicitly record why the implementation should not be treated as the as-built system.

## Control boundary summary

| Concern | Controlled by this document? | Controlling surface | Storage-topology obligation |
|---|---:|---|---|
| Generalized JSON document database substrate | Yes | This architecture note and separation-of-concerns brief | Separate generic JSON document persistence from ADR-specific document behavior. |
| Storage adapter boundary | Yes | This architecture note | Define and preserve backend isolation. |
| SQLite as pilot backend | Yes | This architecture note and implementation brief | Exercise SQLite as the first backend for the generic JSON document store; do not commit mutable DB authority. |
| JSON checkpoint/export behavior | Yes | This architecture note until a follow-up ADR changes authority | Keep checkpoint reviewable and explicitly non-authoritative for the pilot. |
| Pilot manifest/config | Yes | This architecture note | Keep pilot-local config/evidence index under `dev/adr-json-database-one-adr-pilot/`. |
| Markdown projection behavior | Yes for pilot evidence; durable edit/ingest policy deferred | This architecture note for pilot; future ADR for editable projection policy | Generate deterministic non-authoritative projection and preserve source evidence. |
| ADR naming, slug rules, repeated-topic handling | No | `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`, `docs/architecture/architecture.adr.names.md`, naming child drafts as source/provenance | Reference and preserve; do not redefine. |
| ADR lifecycle status and transition semantics | No | `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` | Preserve lifecycle metadata; do not turn storage state into lifecycle authority. |
| Supersession, activation, replacement, amendment chains | No | ADR lifecycle/naming control surfaces | Preserve relationship metadata defined elsewhere; do not collapse relation types. |
| Bulk ADR migration | No | Requires separate user/Hermes approval and follow-up ADR/brief | Explicitly out of scope. |
| Database-authoritative repository policy | No | Requires follow-up ADR action | Treat database authority as recommendation/evidence only. |

## Current decision tension

The current controlling draft ADR says:

- JSON files on disk are canonical ADR storage.
- Markdown is a render or presentation form.
- SQLite may be an index/cache only unless promoted later.

Newer user/Hermes direction asks for movement toward:

- ADRs being JSON-authoritative,
- stored on a database implementation,
- with `docs/adr/` becoming a projection surface of JSON.

That creates an unresolved authority tension. The pilot must expose evidence for the tension, not resolve it by implementation convenience.

## Topology terms

### ADR content record

The structured ADR content that validates against `docs/schemas/adr.schema.json`.

For the current pilot, this should remain a plain ADR schema instance unless Athena approves a schema revision or wrapper model.

### Generalized JSON document database substrate

The long-term storage substrate is a generalized JSON document database. It stores JSON documents by stable document identity, document-family/kind metadata, canonical JSON payload, content hash, and minimal generic timestamps or freshness metadata.

SQLite is the first pilot backend for this substrate. In the initial implementation it may store canonical JSON payloads as blobs/text with generic index columns, but SQLite must remain a backend implementation detail behind the document-store adapter.

The generic JSON document database must not contain ADR-specific policy. It must not know ADR schema fields such as `slug`, lifecycle `status`, `routing.next_phase`, supersession chains, legacy `.draft.md` filenames, or Markdown projection behavior. Those are ADR document-family concerns.

### ADR document layer

ADR concerns are separated by documents and must likewise be separated in code. ADR-specific mapping, schema validation, naming/lifecycle metadata preservation, Markdown projection, semantic equality, and pilot manifest/mapping evidence belong in the ADR document layer.

The ADR layer may call the generic JSON document database to store/load/export the ADR JSON payload, but it must not force ADR-specific fields into the generic storage schema. If ADR workflows need query acceleration for ADR-specific fields, that should be modeled as an ADR-specific index/projection layer or deferred slice, not as generic document-store policy.

### Storage adapter layer

Storage must be accessed through a narrow adapter interface rather than through SQLite-specific implementation logic spread through mapping, projection, validation, or workflow code.

The generic adapter boundary should expose storage operations such as load/store/export/query for JSON documents while hiding backend-specific details. ADR-facing storage should be a wrapper/delegator over that generic boundary, not the place where SQLite becomes ADR architecture.

For the current pilot, the adapter layer should be minimal and decision-evidence oriented. It should be generalized enough to prove separation of concerns, but it must not expand into a broad ingestion or database framework.

### SQLite operational store

A generated local SQLite database used by the pilot storage adapter to exercise database ingest, query/update as needed, export, and projection workflows.

For the current pilot, SQLite is operationally exercised behind the adapter boundary but not committed as mutable repository authority.

### JSON checkpoint/export

A schema-backed JSON export of the ADR content record.

For the current pilot, this is the committed/reviewable checkpoint artifact for git history and code review.

A schema-valid JSON checkpoint is still pilot evidence, not accepted ADR authority, unless a later ADR action promotes the storage model. Because the plain ADR schema may reject extra metadata, non-authoritative status, source citation, source hash, JSON content hash, and conflict rules may be carried in a committed manifest or mapping sidecar that reviewers must inspect with the JSON checkpoint.

### Markdown projection

A deterministic generated Markdown rendering of the ADR content record and projection metadata.

For the current pilot, generated Markdown projection is evidence only and must not overwrite the hand-authored source draft unless the user explicitly authorizes that overwrite.

### Source Markdown draft

The existing hand-authored ADR draft used as migration source evidence:

- `docs/adr/adr.json-database-for-adr-storage.draft.md`

It remains source evidence during the pilot. It must not be silently converted into generated authority.

### Pilot manifest/config

The completed pilot uses `dev/adr-json-database-one-adr-pilot/manifest.json` as its committed configuration and evidence index. It records source/checkpoint/projection paths, hashes, adapter policy, generated-local database policy, conflict rule, and supporting architecture/brief/plan/report paths.

For the next slice, manifest changes remain pilot-local evidence. Do not introduce reusable or global ADR storage configuration.

## Authority models deferred

The completed one-ADR pilot exercised a database-operational / JSON-checkpointed model: SQLite is operational/local, JSON checkpoint is committed review evidence, and Markdown is projection evidence.

Durable repository authority remains deferred. A follow-up ADR must decide whether the long-term model is JSON-file canonical, database-authoritative, or database-operational / JSON-checkpointed.

## Naming and lifecycle dependency

ADR naming and lifecycle policy are dependencies of this storage topology, not decisions made by this storage topology.

Controlling surfaces:

- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` — active ADR lifecycle and umbrella naming distinction.
- `docs/architecture/architecture.adr.names.md` — ADR naming architecture surface.
- `docs/adr/adr.adr-names.draft.md` and child naming drafts — non-canonical detailed naming source/provenance until separately accepted, revised, or rejected.

This storage topology may record the intended pilot identity and may require storage/projection code to preserve naming and lifecycle metadata, but it must not redefine repeated-topic handling, slug collisions, supersession, activation, replacement, amendment, lifecycle state, or filename policy.

For this surface, the intended hierarchy-ordered topic identity is:

- `id`: `adr.json-database-adr`
- `slug`: `json-database-adr`

The implemented pilot currently uses the older stem `json-database-for-adr-storage`. That stem remains pilot evidence and should be updated only by a bounded implementation slice that applies the controlling naming/lifecycle policy. The source fixture remains:

- `docs/adr/adr.json-database-for-adr-storage.draft.md`

The source path with `.draft.md` must remain cited in mapping evidence. Lifecycle status, source date, and other operational details are metadata. Keep the implementation YAGNI: represent only metadata needed for the current slice, and do not add broad naming/lifecycle machinery here.

## Projection invariants

Generated Markdown ADR projections must identify:

- source record ID,
- schema ID/version,
- generation method,
- source-of-truth mode,
- pilot derivative/non-authoritative status when applicable,
- projection freshness marker such as content hash, source version, or equivalent metadata,
- conflict rule for Markdown edits versus structured source edits.

Projection must preserve required ADR sections when present:

- status,
- context,
- decision,
- consequences,
- architecture spec,
- acceptance criteria,
- implementation brief,
- resolved open questions,
- non-goals,
- validation expectations,
- routing,
- links.

Projection must be deterministic for unchanged source content.

For the current pilot, generated Markdown projections are generated-only evidence. They are not an editable authority surface and should not be ingested back as user-authored changes except through the narrow projection parse/equality test defined by the pilot. A later ADR may define an editable Markdown ingest workflow.

## Git and review implications to test

The pilot must make these implications inspectable:

- whether reviewers inspect JSON records, generated Markdown, SQL schema/dump text, or all of them;
- whether mutable SQLite files are committed, ignored, or regenerated;
- how generated projection staleness is detected;
- how merge conflicts are expected to be resolved;
- how schema validation failures differ from projection/parse failures;
- how source Markdown evidence is preserved when generated projections exist;
- how a reviewer verifies that no hand-authored `docs/adr/*.md` source file was modified by the pilot;
- how a reviewer verifies that no mutable `.sqlite` or `.db` file was committed;
- how pilot artifacts under `dev/` are visibly marked as non-authoritative despite being committed for evidence.

For the current pilot, mutable `.sqlite` or `.db` files should remain generated/local state and should not be committed. SQLite-specific behavior should be isolated behind the pilot storage adapter so later evidence can compare or replace the backend without rewriting ADR mapping, validation, or projection logic.

## Pilot as-built state 20260711.035759Z

VULCAN implemented and validated the bounded one-ADR pilot described by this architecture blueprint, the implementation brief, and the approved implementation plan.

As-built implementation report:

- `docs/implementation/adr-json-database-one-adr-pilot.20260711.035759.md`

As-built code and tests:

- `src/python/projectkoios/bootstrap/control_surface/adr/`
- `tests/projectkoios/bootstrap/control_surface_adr/`

Package-boundary note: after KOIOS package-boundary review and user approval, VULCAN moved the implementation from `projectkoios.bootstrap.adr_records` to `projectkoios.bootstrap.control_surface.adr`. The as-built package name is intentionally control-surface oriented: it covers ADR authority, projection, storage, and evidence boundaries rather than only data records.

As-built pilot evidence directory:

- `dev/adr-json-database-one-adr-pilot/`

Delivered evidence artifacts:

- `dev/adr-json-database-one-adr-pilot/manifest.json`
- `dev/adr-json-database-one-adr-pilot/mapping.json`
- `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json`
- `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.projected.md`
- `dev/adr-json-database-one-adr-pilot/database-evidence.md`

As-built topology:

- Source Markdown `docs/adr/adr.json-database-for-adr-storage.draft.md` remains hand-authored source/migration evidence.
- Canonical pilot identity is status-free: `id = adr.json-database-for-adr-storage`, `slug = json-database-for-adr-storage`.
- Lifecycle status is record content: `status = draft`.
- JSON checkpoint is committed review evidence at `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json`.
- Markdown projection is committed generated evidence at `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.projected.md`.
- Pilot manifest/config is committed at `dev/adr-json-database-one-adr-pilot/manifest.json`.
- SQLite is the selected pilot backend behind the storage adapter boundary.
- Mutable SQLite database files are generated/local state and are not committed as repository authority.

As-built adapter boundary after separation slice:

- Generic JSON document-store substrate lives under `src/python/projectkoios/bootstrap/control_surface/documents/` and `src/python/projectkoios/bootstrap/control_surface/storage/`.
- `DocumentRecord` carries `document_id`, `document_kind`, canonical JSON payload, content hash, and caller-supplied timestamps.
- `SqliteDocumentStore` persists only generic columns: `document_id`, `document_kind`, `content_hash`, `payload_json`, `created_at`, and `updated_at`.
- `MemoryDocumentStore` provides a non-SQLite implementation for boundary tests.
- ADR storage is now `DocumentStoreAdrStorageAdapter`, an ADR-facing wrapper over the generic store.
- ADR schema validation, Markdown projection, semantic equality, naming/lifecycle metadata, and source mapping remain outside the generic store.
- Scoped enum/type values are used for semantic values introduced by the slice, including `DocumentType`, `DocumentStoreBackend`, `ArtifactDisposition`, `ReplacementAction`, and `SourceOfTruthMode`; no dangling semantic constants are authorized.

As-built manifest/config behavior:

- `manifest.json` is the pilot-local configuration and evidence index.
- The manifest declares non-authoritative pilot status, source/checkpoint/projection paths, hashes, storage adapter policy, selected SQLite adapter, local/generated DB policy, conflict rule, and architecture/brief/plan/report paths.
- No reusable or global ADR storage configuration has been introduced.

As-built validation evidence after cleanup/schema conformance:

```bash
uv run pytest -q
# 253 passed in 1.27s

uv run mypy src/python tests
# Success: no issues found in 139 source files

uv run ruff check src/python tests
# All checks passed!

uv run projectkoios bootstrap validate-python-policy src/python tests
# summary: 0 finding(s), 139 file(s)

git diff --check
# clean

find dev/adr-json-database-one-adr-pilot -type f \( -name '*.sqlite' -o -name '*.db' \) -print
# no output
```

VULCAN reported this whole-repo validation in `docs/implementation/control-surface-cleanup-and-schema-conformance.20260711.061724.md`. ATHENA has not rerun the full validation commands in this reconciliation pass.

## As-built conformance to architecture invariants

| Architecture invariant / question | As-built evidence | Conformance |
|---|---|---|
| One representative ADR only | Implementation and tests use `docs/adr/adr.json-database-for-adr-storage.draft.md` as the only source fixture. | Conforms. |
| Source `.draft.md` remains evidence only | `manifest.json` and `mapping.json` record source filename suffix separately from canonical identity. | Conforms. |
| Status-free canonical identity | JSON checkpoint uses `id = adr.json-database-for-adr-storage`, `slug = json-database-for-adr-storage`, `status = draft`. | Conforms for pilot. Global policy still open. |
| Plain ADR schema JSON checkpoint | JSON checkpoint validates against `docs/schemas/adr.schema.json`. | Conforms. |
| Pilot-local manifest/config | `manifest.json` exists and indexes paths, hashes, adapter policy, conflict rule, and evidence. | Conforms. |
| Storage adapter boundary | Generic document-store substrate is separated from ADR wrapper; SQLite implementation is generic and memory store covers boundary. | Conforms after separation slice. |
| SQLite operational/local only | SQLite is the generic document-store backend for the pilot; mutable DB file is generated/local and not committed. | Conforms. |
| Markdown projection as non-authoritative evidence | Generated projection includes non-authoritative metadata and conflict rule. | Conforms. |
| Source and JSON hashes preserved | Manifest/mapping preserve source hash and JSON hash. | Conforms. |
| Source date preserved despite schema gap | `mapping.json` preserves `20260702.121432Z` outside the plain ADR schema. | Conforms; schema gap remains. |
| Validation and parser failures distinguishable | Mapping/test evidence records schema invalid-status failure separately from round-trip projection equality. | Conforms. |
| Architecture evidence reconciled | This as-built section records delivered topology, cleanup/schema conformance evidence, and residual gaps. | Conforms for implementation-report reconciliation. |

## As-built residual gaps

The pilot produced validated evidence, but the next near-term work should remain YAGNI and use the ADR schema without routing rather than designing workflow/lifecycle machinery ahead of implementation pressure.

Current residual gaps are observations, not authorization for schema expansion:

- Existing ADRs still need to be pushed toward conformance with `docs/schemas/adr.schema.json` after routing removal.
- The current pilot stem `json-database-for-adr-storage` is as-built pilot evidence. Hierarchy-ordered naming remains a known preference, but broad naming machinery, collision policy, and repeated-topic handling should wait until actual ADR conformance work requires them.
- `routing` is not required for the Petri-net workflow and has been removed from the ADR schema. Do not redesign it into state/event workflow metadata in this slice.
- Source date remains preserved in mapping evidence only. Do not add timestamp taxonomy fields until repeated conformance work proves that sidecar preservation is insufficient.
- Generated Markdown projection embeds complete ADR JSON for deterministic parse-back. Future projection policy can wait until projection reuse or workflow implementation creates pressure.
- SQLite schema is now generic-document-store oriented and intentionally minimal; database-authoritative repository policy still requires a follow-up ADR.
- Pilot-local manifest/config worked for this slice; reusable repository-level ADR storage config remains deferred.

## Completed implementation slice: JSON document database separation and schema conformance

Active implementation evidence:

- Brief: `docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md`
- Plan: `docs/plans/implementation-plan.20260711.050606_json-document-database-separation.md`
- Report: `docs/implementation/json-document-database-separation.20260711.051951.md`
- Cleanup/conformance report: `docs/implementation/control-surface-cleanup-and-schema-conformance.20260711.061724.md`
- AAR: `docs/AAR/aar.20260711.051951_json-document-database-separation.md`

The slice separated generic document and storage concerns from ADR-specific document behavior. The generalized substrate is piloted as SQLite storing canonical JSON payloads plus minimal generic metadata. ADR parsing, schema validation, Markdown projection, record comparison, and pilot evidence remain in ADR-specific code. The cleanup/conformance pass updated generated ADR JSON to the schema without `routing`; source routing prose is preserved only in mapping/migration evidence.

Migration evidence:

- `dev/adr-json-database-one-adr-pilot/document-store-migration-evidence.json`
- `dev/adr-json-database-one-adr-pilot/database-evidence.md`
- `dev/adr-json-database-one-adr-pilot/manifest.json`

Boundaries preserved by the reported implementation:

- No backward-compatibility shim was added.
- No ADR-specific fields were added to the generic `json_documents` table.
- No bulk ADR migration was performed.
- No reusable repository-level config was added.
- No database-authority promotion was made.
- No source `docs/adr/*.md` file was modified.
- No mutable `.sqlite` or `.db` file is committed under the pilot directory.
- `workflow_binding` remains untouched until a real Petri-net workflow integration brief exists.

ATHENA review result: accept the control-surface cleanup/schema conformance report as conforming to the current architecture and user YAGNI direction.

Recommended next state: a bounded YAGNI conformance slice that pushes one additional ADR or ADR-like document toward the updated `docs/schemas/adr.schema.json` shape without `routing`. Going forward, records that enter the conformance flow are treated as active control-surface entries, not historical-only artifacts. Sidecar evidence may preserve prior source fields, source paths, and conversion facts, but the new conformed record is not framed as merely historical or non-authoritative unless the user explicitly says so. Do not expand naming/lifecycle metadata, state/event workflow semantics, reusable config, or durable storage-authority policy until actual workflow-system or conformance work creates a concrete need.

## Workflow lifecycle

Implementation briefs, plans, and reports are supporting slice artifacts. This architecture note remains the durable topology/as-built surface; see `docs/meta-harness.md` for the general blueprint-to-as-built workflow.

## Open architecture questions

### Storage authority

- Should the eventual repository authority be JSON-file canonical, database-authoritative, or database-operational/JSON-checkpointed?
- If database-authoritative, what reviewable git artifact represents authoritative changes?
- What conflict rule applies when storage-adapter state, JSON checkpoint, and Markdown projection disagree?

### Projection and metadata

- Should `docs/adr/` projections be generated-only, editable with ingest, or mixed by explicit metadata?
- Which source/projection metadata must remain in sidecar evidence while the existing ADR schema is used unchanged?
- Which schema discomforts recur during ADR conformance often enough to justify a later schema revision?

### Adapter and configuration

- Which ADR-specific query/index needs, if any, are actually required by schema-conformance work and should remain outside the generic document-store table?
- After conformance work creates real pressure, should ADR storage configuration remain per-pilot/per-slice, or should a reusable repository-level ADR storage config be introduced?
- Does `docs/schemas/schema.record-base.json` need source-of-truth enum values for database rows/documents, or can that wait until a workflow/storage authority slice exists?

## YAGNI planning boundary for next conformance slice

The next slice should be a schema-conformance slice, not a schema-redesign, naming-machinery, workflow-state, or storage-authority slice.

| Issue | YAGNI resolution | Controlling authority | Implementation impact |
|---|---|---|---|
| Existing ADR schema | Use updated `docs/schemas/adr.schema.json` without `routing`. | Current schema and user direction. | Convert or map ADRs to the current required shape before proposing further schema changes. |
| `routing` field | Removed from ADR schema because it is not required for the Petri-net workflow. | User direction. | Do not populate `routing` for conformance and do not redesign it into state/event workflow metadata now. |
| Source/projection metadata | Keep conversion/provenance facts in sidecar mapping/manifest evidence unless the current schema already has a field. Going forward, sidecars preserve provenance but do not make newly conformed records historical-only. | KOIOS provenance requirements plus current schema and user active-forward direction. | Preserve source paths, hashes, copied/normalized/inferred fields, and old/new hashes for regenerated artifacts while treating the conformed record as active. |
| Naming hierarchy | Prefer general-to-specific names when producing new identifiers, but do not build collision/repeated-topic machinery. | User direction plus existing naming/lifecycle surfaces. | If a pilot artifact identity changes, record old and new identity as migration evidence. |
| Workflow system assumptions | Defer until a workflow system exists. | User/HERMES future workflow authority. | Do not add lifecycle transition graphs, event logs, or state machines to satisfy speculative future workflow design. |

## Related files

- `docs/adr/adr.json-database-for-adr-storage.draft.md`
- `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md`
- `docs/schemas/adr.schema.json`
- `docs/schemas/schema.record-base.json`
- `docs/architecture/architecture.00.md`
