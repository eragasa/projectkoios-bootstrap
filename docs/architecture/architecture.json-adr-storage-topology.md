---
status: pilot-as-built
date: 20260711.032904Z
last_updated: 20260711.040952Z
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
- Schema-backed ADR JSON records compatible with `docs/schemas/adr.schema.json`.
- SQLite as an operational store for the current pilot.
- JSON checkpoint/export artifacts for repository review.
- Markdown ADR projection surfaces under `docs/adr/`.
- One-ADR pilot evidence using `docs/adr/adr.json-database-for-adr-storage.draft.md` as the representative source.

Out of scope:

- Bulk ADR migration.
- Product-domain architecture in the `projectkoios` mothership.
- Generic document ingestion.
- Generic database framework design.
- Removing Markdown review/navigation surfaces.

## Control

This note is controlled by:

- `docs/adr/adr.json-database-for-adr-storage.draft.md`

Related implementation planning is currently captured in:

- `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md`

The implementation brief may define a bounded pilot, but it must not silently change ADR storage authority. Any durable authority change requires ADR revision, replacement, promotion, acceptance, or supersession through the normal ADR lifecycle.

This architecture note is the controlling blueprint/as-built surface for the system shape. VULCAN implementation reports must identify any deviations from this blueprint. After implementation evidence exists, ATHENA must update this note from intended blueprint to as-built documentation or explicitly record why the implementation should not be treated as the as-built system.

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

### Storage adapter layer

ADR storage must be accessed through a narrow storage adapter interface rather than through SQLite-specific implementation logic spread through mapping, projection, validation, or workflow code.

The adapter boundary should expose storage operations such as load/store/export/query for ADR records while hiding backend-specific details. SQLite is the approved backend for the current pilot, but it must be one adapter implementation, not the architecture of the whole ADR storage system.

For the current pilot, the adapter layer should be minimal and decision-evidence oriented. It should not become a generic database framework, but it must prevent the pilot from hard-coding SQLite assumptions into the ADR record model, projection logic, or future authority decision.

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

The current pilot must have an explicit committed manifest/config artifact:

- `dev/adr-json-database-one-adr-pilot/manifest.json`

The manifest is the pilot's configuration and evidence index. It should declare at minimum:

- pilot name and non-authoritative pilot status;
- source ADR path and source content hash;
- canonical pilot `id`, `slug`, and status-location rule;
- JSON checkpoint path and JSON content hash;
- generated Markdown projection path;
- storage adapter policy and SQLite adapter selection for the pilot;
- SQLite operational-store policy, including that mutable `.sqlite`/`.db` files are local/generated and not committed;
- schema path and schema `$id` or version when available;
- generation method/tool entry point when implemented;
- conflict rule between source Markdown, SQLite operational state, JSON checkpoint, and generated projection;
- validation/evidence artifact paths;
- architecture blueprint path and implementation brief/plan paths.

For this pilot, configuration belongs with the bounded pilot evidence under `dev/adr-json-database-one-adr-pilot/`. Do not introduce a reusable or global ADR storage configuration surface until pilot evidence justifies one and Athena/user approve the next architecture slice.

## Candidate authority models

### JSON-file canonical

- JSON ADR records in git are the durable source of truth.
- SQLite is an index/cache.
- Markdown is generated or editable according to an explicit ingest/conflict rule.

Strengths:

- Reviewable git diffs.
- Simple repository history.
- Lower local-state risk.

Risks:

- Database workflow may remain secondary.
- Query/update behavior can drift from operational use.

### Database-authoritative

- Database row/document state is the source of truth.
- JSON and Markdown are exports/projections.
- Git review requires dumps, migrations, exported JSON checkpoints, or another review surface.

Strengths:

- Directly supports query/update workflows.
- Clear operational source for tooling.

Risks:

- Mutable database authority is harder to review and merge in git.
- Requires stronger backup, migration, conflict, and projection rules.
- Local runtime state can accidentally become hidden authority.

### Database-operational / JSON-checkpointed

- SQLite is the operational store during workflows.
- JSON export/checkpoint is the committed reviewable authority surface unless a later ADR says otherwise.
- Markdown remains a projection surface.

Strengths:

- Exercises real database behavior.
- Preserves git-reviewable checkpoints.
- Supports evidence-gathering before committing to full database authority.

Risks:

- Authority split must be explicit.
- Checkpoint freshness and conflict rules must be tested.
- Users may confuse operational DB state with durable repo authority.

The completed one-ADR pilot exercised this third model.

## Identity and status invariant

Canonical ADR identity should not encode mutable lifecycle status such as `draft`, `proposed`, `accepted`, or `superseded` in the filename, record ID, or slug.

Lifecycle status belongs inside the ADR record content and projection metadata. Existing filenames that include status suffixes, such as `.draft`, may be treated as legacy/source evidence during migration, but generated canonical records and projections should prefer status-free identity names unless a later ADR explicitly decides otherwise.

For the current pilot, the source fixture path remains:

- `docs/adr/adr.json-database-for-adr-storage.draft.md`

The pilot should record that `.draft` was present in the source filename, while deriving canonical pilot identity from the status-free ADR topic:

- `id`: `adr.json-database-for-adr-storage`
- `slug`: `json-database-for-adr-storage`
- `status`: `draft` inside the ADR record

For generated pilot artifacts, prefer status-free canonical stems where feasible:

- `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json`
- `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.projected.md`

The source path with `.draft.md` must remain cited in mapping evidence.

The current pilot may use topic-stable identity as decision evidence, but it must not silently establish a permanent global ADR identity policy. The implementation report should identify whether future canonical identity should be topic-stable, event/timestamp-stable, or another scheme.

The source date `20260702.121432Z` is important provenance. If the current ADR schema cannot store it directly, the pilot must preserve it in mapping evidence and report the schema gap rather than dropping it or inventing an unreviewed field.

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

As-built adapter boundary:

- `AdrStorageAdapter` exposes minimal storage operations for the pilot: store, get, export, and list/query by status.
- `SqliteAdrStorageAdapter` contains SQLite-specific implementation details.
- A memory adapter test proves ADR mapping, schema validation, Markdown projection, and semantic equality are not directly coupled to SQLite.
- The adapter layer is intentionally narrow and must not be treated as a generic database framework.

As-built manifest/config behavior:

- `manifest.json` is the pilot-local configuration and evidence index.
- The manifest declares non-authoritative pilot status, source/checkpoint/projection paths, hashes, storage adapter policy, selected SQLite adapter, local/generated DB policy, conflict rule, and architecture/brief/plan/report paths.
- No reusable or global ADR storage configuration has been introduced.

As-built validation evidence:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/schema -q
# 24 passed

uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
# success

uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
# summary: 0 finding(s), 10 file(s)

git diff --check
# clean

find dev/adr-json-database-one-adr-pilot -type f \( -name '*.sqlite' -o -name '*.db' \) -print
# no output
```

ATHENA reran the validation commands from the repository root during conformance review and confirmed the reported outcomes.

## As-built conformance to architecture invariants

| Architecture invariant / question | As-built evidence | Conformance |
|---|---|---|
| One representative ADR only | Implementation and tests use `docs/adr/adr.json-database-for-adr-storage.draft.md` as the only source fixture. | Conforms. |
| Source `.draft.md` remains evidence only | `manifest.json` and `mapping.json` record source filename suffix separately from canonical identity. | Conforms. |
| Status-free canonical identity | JSON checkpoint uses `id = adr.json-database-for-adr-storage`, `slug = json-database-for-adr-storage`, `status = draft`. | Conforms for pilot. Global policy still open. |
| Plain ADR schema JSON checkpoint | JSON checkpoint validates against `docs/schemas/adr.schema.json`. | Conforms. |
| Pilot-local manifest/config | `manifest.json` exists and indexes paths, hashes, adapter policy, conflict rule, and evidence. | Conforms. |
| Storage adapter boundary | SQLite-specific logic is isolated in adapter implementation; memory adapter test covers boundary. | Conforms. |
| SQLite operational/local only | SQLite is selected pilot adapter; mutable DB file is generated/local and not committed. | Conforms. |
| Markdown projection as non-authoritative evidence | Generated projection includes non-authoritative metadata and conflict rule. | Conforms. |
| Source and JSON hashes preserved | Manifest/mapping preserve source hash and JSON hash. | Conforms. |
| Source date preserved despite schema gap | `mapping.json` preserves `20260702.121432Z` outside the plain ADR schema. | Conforms; schema gap remains. |
| Validation and parser failures distinguishable | Mapping/test evidence records schema invalid-status failure separately from round-trip projection equality. | Conforms. |
| Architecture evidence reconciled | This as-built section records delivered topology and residual gaps. | Conforms for pilot review. |

## As-built residual gaps

The pilot produced validated evidence, but these architecture decisions remain open before broader ADR migration or authority promotion:

- Long-term ADR identity policy remains undecided: topic-stable identity worked for the pilot but may not be sufficient for repeated ADRs on the same topic or supersession chains.
- `docs/schemas/adr.schema.json` lacks a direct creation date or lifecycle timestamp field; source date is preserved in mapping evidence only.
- Generated Markdown projection embeds complete ADR JSON for deterministic parse-back; future projection policy must decide whether projections are human-readable only, JSON-embedded, or both.
- SQLite schema remains intentionally minimal and adapter-local; database-authoritative repository policy still requires a follow-up ADR.
- Pilot-local manifest/config worked for this slice; reusable repository-level ADR storage config remains a future architecture question.

## Blueprint to as-built lifecycle

Before implementation:

- this document is the architecture blueprint and long-term system vision;
- implementation slices are cut from this blueprint into bounded briefs and plans;
- implementation plans and briefs must conform to it or explicitly request a deviation;
- unresolved questions remain decision evidence requirements, not implementation freedom.

During implementation:

- VULCAN must report deviations from this blueprint as implementation decisions needing ATHENA/user review;
- test evidence should be mapped back to the invariants and open questions in this document;
- implementation convenience must not silently redefine ADR authority.

After implementation:

- ATHENA must revise this document into as-built architecture documentation;
- the as-built revision must record delivered storage topology, committed artifacts, generated/local artifacts, validation evidence, and unresolved gaps;
- the as-built revision must map implementation evidence back to this document's invariants and open questions before any broader ADR migration begins;
- if delivered behavior differs from this blueprint, the difference must be recorded as an accepted deviation, a follow-up ADR need, or a correction task;
- the implementation brief and report become supporting evidence, not the primary architecture surface.

## Pilot interaction gate

Before VULCAN writes implementation code, VULCAN must produce a short implementation plan with an explicit decision table for user/Hermes approval.

That plan must identify:

- proposed file paths,
- storage adapter boundary and SQLite adapter implementation shape,
- SQLite schema shape,
- JSON export/checkpoint shape,
- Markdown projection approach,
- validation commands,
- deviations from this architecture note or the implementation brief,
- authority-model evidence the pilot will produce;
- pilot manifest/config path and fields, with `dev/adr-json-database-one-adr-pilot/manifest.json` as the expected committed pilot configuration/evidence index;
- pilot manifest/mapping evidence for non-authoritative status, source citation, source hash, JSON content hash, and status-free identity derivation;
- guardrails proving no source `docs/adr/*.md` file and no mutable `.sqlite`/`.db` file are committed.

The plan should optimize for decision evidence with minimal code.

## Open architecture questions

- Should the eventual repository authority be JSON-file canonical, database-authoritative, or database-operational/JSON-checkpointed?
- If database-authoritative, what reviewable git artifact represents authoritative changes?
- Should `docs/adr/` projections be generated-only, editable with ingest, or mixed by explicit metadata?
- What is the long-term canonical ADR identity policy: topic-stable, event/timestamp-stable, or another scheme?
- Where should creation date and lifecycle timestamps live if `docs/schemas/adr.schema.json` does not currently contain them?
- What metadata belongs in `docs/schemas/adr.schema.json` versus a projection/record envelope?
- After the pilot, should ADR storage configuration remain per-pilot/per-slice, or should a reusable repository-level ADR storage config be introduced?
- Does `docs/schemas/schema.record-base.json` need source-of-truth enum values for database rows/documents?
- What conflict rule applies when storage-adapter state, JSON checkpoint, and Markdown projection disagree?
- Which storage adapter interface is sufficient for ADR workflows without becoming a generic database framework?
- What exact status and routing lifecycle enums should be authoritative across ADR record status and `routing.next_phase`?

## Related files

- `docs/adr/adr.json-database-for-adr-storage.draft.md`
- `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md`
- `docs/schemas/adr.schema.json`
- `docs/schemas/schema.record-base.json`
- `docs/architecture/architecture.00.md`
