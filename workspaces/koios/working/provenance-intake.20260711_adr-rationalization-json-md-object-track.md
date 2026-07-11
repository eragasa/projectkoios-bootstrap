```json
{
  "title": "Provenance intake: ADR rationalization / bidirectional JSON-Markdown object track",
  "artifact_type": "provenance-intake",
  "status": "koios-input-only",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "ADR rationalization and bidirectional JSON-Markdown object track",
  "output_owner": "KOIOS"
}
```

# Provenance intake: ADR rationalization / bidirectional JSON-Markdown object track

## Purpose

USER raised a knowledge/provenance concern that ADRs are messy and could be rationalized into bidirectional JSON↔Markdown objects. This note inventories relevant existing ADR/document-control surfaces and prior ADR JSON/database/conformance work so ATHENA/HERMES can decide whether to open a bounded architecture/spec track.

This is KOIOS intake only. It does not edit ADRs, schemas, architecture, source code, or generated artifacts, and it does not create implementation authority.

## Current surface inventory

### ATHENA architecture intake

New ATHENA input exists at `docs/plans/architecture-intake.20260711.131140_adr-bidirectional-json-markdown-objects.md`.

Validated claims from that intake:

- The user concern is architecture/spec intake only: ADRs are messy and may need rationalization into bidirectional JSON↔Markdown objects.
- Existing surfaces should be used first, especially `docs/architecture/architecture.json-adr-storage-topology.md`, `docs/schemas/adr.schema.json`, `src/python/projectkoios/bootstrap/control_surface/adr/`, `src/python/projectkoios/bootstrap/control_surface/documents/`, `src/python/projectkoios/bootstrap/control_surface/storage/`, `dev/adr-json-database-one-adr-pilot/`, and `dev/adr-json-schemas-conformance/`.
- ATHENA frames the main unresolved questions as object shape, meaning of bidirectional conversion, authority model, unsupported/extra field preservation, relation to the generalized JSON document store, and minimum canary slice.
- ATHENA recommends `docs/architecture/architecture.adr-bidirectional-objects.md` as the likely next artifact before implementation because authority and bidirectional semantics are the core ambiguity.

KOIOS assessment: ATHENA's intake is consistent with prior KOIOS provenance findings. The next safe move is architecture-owned definition of object vocabulary, round-trip invariants, conflict/authority rules, and canary boundaries, not bulk migration.

### ADR corpus

Observed under `docs/adr/`:

- 42 Markdown files total, including `README.md`.
- Status scan from leading frontmatter/JSON/status headings found mixed status vocabulary/casing:
  - `draft`: 31
  - `Draft`: 1
  - `active`: 2
  - `accepted`: 1
  - `Accepted`: 1
  - unknown/no parsed status: 6

Validated implication: the ADR directory is not a uniform machine-readable control surface today. Status vocabulary, casing, file naming, and structured metadata are uneven.

### ADR lifecycle/naming/control surfaces

Key sources:

- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`
- `docs/policies/architecture.adr.lifecycle.md`
- `docs/architecture/architecture.adr.00.md`
- `docs/architecture/architecture.adr.names.md`
- `docs/adr/adr.adr-lifecycle.draft.md`
- `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`
- `docs/adr/adr.adr-names.draft.md`
- `docs/adr/adr.adr-title-naming-convention.draft.md`
- `docs/adr/adr.adr-filename-naming-convention.draft.md`
- KOIOS prior notes:
  - `workspaces/koios/working/provenance-index.20260704T175525Z_adr-control-surfaces.md`
  - `workspaces/koios/working/provenance-audit.20260709T012117Z_adr-lifecycle-followon-reconciliation.md`

Validated claims:

- The accepted lifecycle/naming ADR is the current canonical consolidation for lifecycle/status compatibility and the umbrella title-vs-filename distinction.
- It preserves source drafts as provenance and explicitly does not authorize schema/tooling changes, bulk rewrites, mass renames, or file migrations.
- Detailed naming and filename rules remain non-canonical draft guidance unless separately promoted.
- Existing architecture/policy surfaces point at the accepted ADR as controlling where appropriate, but residual ambiguity remains around architecture-note status frontmatter and prose-only source-draft disposition links.

Messy/unresolved:

- ADR filenames mix timestamped, topic-only, `.draft`, and other conventions.
- Status casing and status vocabulary are not uniform across `docs/adr/`.
- Several source drafts remain draft/provenance rather than superseded, by design; this is safe but can confuse readers.
- No bulk rationalization, lifecycle migration, or structured source-draft disposition schema has been accepted.

### JSON/database/storage topology work

Key sources:

- `docs/architecture/architecture.json-adr-storage-topology.md`
- `docs/adr/adr.json-database-for-adr-storage.draft.md`
- `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md`
- `docs/plans/implementation-plan.20260711.033558_adr-json-database-one-adr-pilot.md`
- `docs/implementation/adr-json-database-one-adr-pilot.20260711.035759.md`
- `docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md`
- `docs/implementation/json-document-database-separation.20260711.051951.md`
- `docs/implementation/control-surface-cleanup-and-schema-conformance.20260711.061724.md`
- `dev/adr-json-database-one-adr-pilot/`
- `src/python/projectkoios/bootstrap/control_surface/adr/`
- `src/python/projectkoios/bootstrap/control_surface/documents/`
- `src/python/projectkoios/bootstrap/control_surface/storage/`

Validated claims:

- A bounded one-ADR pilot exists for `docs/adr/adr.json-database-for-adr-storage.draft.md`.
- The pilot created schema-backed JSON checkpoint evidence, generated Markdown projection evidence, sidecar mapping/manifest evidence, and database evidence under `dev/adr-json-database-one-adr-pilot/`.
- The generic JSON document substrate was separated from ADR-specific mapping/projection/validation behavior.
- SQLite was exercised behind an adapter as operational/local generated state; no mutable `.sqlite`/`.db` files were committed.
- Source Markdown ADR files were not mutated by the pilot.
- The architecture note records the pilot as as-built evidence but explicitly leaves durable storage authority unresolved.

Messy/unresolved:

- Durable repository authority remains undecided: JSON-file canonical, database-authoritative, or database-operational/JSON-checkpointed.
- Markdown projection policy remains unresolved: generated-only, editable with ingest, or mixed by explicit metadata.
- Review/conflict rules between Markdown, JSON checkpoint, and database state remain open architecture questions.
- The pilot uses `dev/` evidence and is not a repository-wide ADR migration.

### ADR schema and one-document conformance work

Key sources:

- `docs/schemas/adr.schema.json`
- `docs/schemas/adr-active.schema.json`
- `docs/schemas/adr-draft.schema.json`
- `docs/schemas/adr.schema-implementation.json`
- `docs/schemas/legacy-architecture.adr.schema-adr.json`
- `docs/schemas/legacy-architecture.adr.schema-implementation.json`
- `docs/adr/adr.json-schemas.draft.md`
- `docs/plans/implementation-plan.20260711.062654_json-schemas-adr-conformance.md`
- `docs/implementation/json-schemas-adr-conformance.20260711.065704.md`
- `workspaces/koios/working/provenance-audit.20260711T065332Z_adr-json-schemas-conformance.md`
- `dev/adr-json-schemas-conformance/`

Validated claims:

- A one-document active conformance slice exists for `docs/adr/adr.json-schemas.draft.md`.
- The source Markdown was not mutated.
- `dev/adr-json-schemas-conformance/adr.json-schemas.json` is the active conformed record for that slice.
- Source `routing.*`, source date/status/path/hash, and `links.related` were preserved in sidecar evidence because the current ADR schema does not carry all source fields.
- `routing` is absent from the schema record after schema/YAGNI direction; it should not be redesigned into speculative workflow state without separate authority.
- Generated projection remains a review projection; the JSON checkpoint is the active conformed record artifact for the slice.

Messy/unresolved:

- Existing ADRs have not been bulk conformed to `docs/schemas/adr.schema.json`.
- Repeated conformance may create pressure for reusable conformance policy, source/projection metadata, and storage authority, but those are not yet accepted.
- Sidecar evidence currently carries fields that may matter for provenance but do not fit the schema.
- The relationship between active conformed JSON artifacts under `dev/` and durable `docs/adr/` authority remains unresolved beyond bounded slice evidence.

## Validated vs unresolved summary

### Validated

- The ADR corpus is heterogeneous enough to justify a rationalization intake: mixed status vocabulary/casing, filename patterns, metadata styles, and draft/provenance surfaces exist.
- Accepted lifecycle/naming authority exists but is intentionally bounded; it does not authorize mass migration.
- A working JSON↔Markdown pilot exists for one ADR with schema validation, projection, sidecar evidence, and adapter-backed storage evidence.
- A generic JSON document substrate exists and is separated from ADR-specific behavior.
- A one-document ADR schema conformance slice exists and demonstrates active conformed JSON plus sidecar provenance without mutating source Markdown.
- Prior implementation and KOIOS audits consistently protect against silent authority promotion, source Markdown mutation, committed mutable DB state, and bulk migration.

### Messy / unresolved

- Which artifact is durable ADR authority long-term: Markdown under `docs/adr/`, JSON checkpoint files, database state, or a hybrid.
- Whether Markdown should be editable and ingested back into JSON, generated-only, or mixed by explicit metadata.
- How bidirectional equality should handle formatting-only changes, comments, missing schema fields, sidecar-only provenance, and generated projection metadata.
- Whether and how to migrate all existing ADRs, including draft/proposal/provenance records, without erasing history.
- How to represent source-draft disposition, supersession/rejection provenance, and lifecycle status in machine-readable form without conflating workspace live state with ADR status.
- Where conformed JSON records should live if promoted beyond `dev/` evidence directories.
- Whether schemas need revision for source/projection metadata or whether sidecars remain sufficient.

## Candidate intake requirements for an ADR rationalization track

If ATHENA/HERMES opens a bounded track, KOIOS recommends starting with a spec/intake slice, not implementation:

1. Define authority target options explicitly: Markdown-authoritative, JSON-authoritative, database-authoritative, or database-operational/JSON-checkpointed.
2. Inventory ADR records and classify by source status, schema conformance, authority status, and provenance-only status.
3. Define bidirectional JSON↔Markdown equivalence rules before mutating any ADR files.
4. Preserve source Markdown paths, hashes, original status/casing, filename suffixes, and omitted fields in sidecar evidence.
5. Decide whether sidecar provenance is temporary migration evidence or a durable companion object.
6. Keep accepted lifecycle/naming ADR boundaries intact; do not silently supersede drafts or rename files.
7. Select one additional representative ADR for a reversible round-trip/conformance slice before any bulk migration.
8. Require before/after validation evidence and `git status -- docs/adr` checks for any source-mutation decision.

## KOIOS candidate schema sketch

USER suggested KOIOS should generate schemas for ADR bidirectional JSON↔Markdown objects. Within KOIOS authority, this is captured only as candidate/provenance-derived schema input, not `docs/schemas/` publication.

Candidate schema sketch:

- `workspaces/koios/working/candidate-schema.20260711_adr-bidirectional-json-md-object.md`

The sketch proposes a non-authoritative envelope around the existing ADR payload schema:

```text
AdrBidirectionalObject
├── content                 # ADR payload compatible with docs/schemas/adr.schema.json
├── markdown_projection     # generated/editable projection metadata and round-trip mode
├── conversion_evidence     # omitted/normalized/inferred fields, lossiness, source mutation flag
├── source_refs             # source/projection/schema paths and hashes
├── sidecar                 # provenance fields outside ADR content schema
├── validation              # schema/round-trip/source-mutation/db checks
└── conflict_policy         # JSON-vs-Markdown and bulk-migration policy
```

KOIOS assessment: the envelope approach matches observed evidence better than forcing provenance/conversion fields into `docs/schemas/adr.schema.json` immediately. ATHENA/USER must decide whether any such envelope becomes architecture/schema authority.

## Boundary / non-authority statement

This KOIOS note does not authorize:

- editing ADR contents;
- changing schemas;
- changing architecture documents;
- changing source code;
- bulk ADR migration;
- committing mutable database state;
- promoting JSON/database authority over Markdown;
- treating `dev/` conformance artifacts as repository-wide ADR authority;
- replacing the accepted lifecycle/naming ADR;
- implementing bidirectional JSON↔Markdown tooling.

Any rationalization track should be owned by ATHENA for architecture/spec authority and routed to VULCAN only after an explicit brief/plan is accepted.
