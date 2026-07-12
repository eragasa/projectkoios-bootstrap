---
status: draft-architecture
created: 20260711.190407Z
acting_as: ATHENA
source_slice: adr-schema-record-envelope-architecture-slice-14
source_provenance: docs/adr/adr.schema-base.md
---

# Architecture: Schema Record Envelope

## Status and non-authority boundary

This is an ATHENA architecture surface for schema-family record-envelope direction.

It extracts still-current concepts from `docs/adr/adr.schema-base.md` while preserving that file as unchanged source/provenance. It does not make `docs/adr/adr.schema-base.md` current ADR authority, infer its top-level lifecycle status, or mutate it.

This document does not accept `docs/schemas/schema.record-base.json` as current record-envelope authority and does not make `metadata` + `content` the current universal emitted-record shape for repository documents.

This document does not edit schemas, change lifecycle state, generate projections, create JSON records, migrate records, or cut over JSON authority.

## Source and provenance basis

Primary source/provenance:

- `docs/adr/adr.schema-base.md`

Planning and acceptance basis:

- `docs/plans/architecture-extraction-brief.20260711.184325_adr-schema-base.md`
- `docs/reviews/hermes-acceptance.20260711.185430_adr-schema-base-architecture-extraction-planning-slice-13.md`
- `docs/reviews/hermes-decision.20260711.190407_adr-schema-record-envelope-architecture-slice-14.md`
- `docs/plans/source-disposition-brief.20260711.183536_adr-schema-base.md`
- `docs/reviews/semantic-rationalization.20260711_adr-six-entry-slice-5.md`
- `docs/schemas/README.md`
- `docs/adr/adr.adr-template-schema-contract.md`
- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`

The embedded JSON `"status": "draft"` in `docs/adr/adr.schema-base.md` is observed source metadata only, not inferred top-level ADR lifecycle status.

## Current schema-family control surfaces

Current control surfaces are layered:

- `docs/adr/adr.adr-template-schema-contract.md` controls the ADR template/schema contract.
- `docs/schemas/adr.schema.json` is the current ADR content-shape schema until an approved slice wraps, replaces, or retires it.
- `docs/schemas/schema.record-base.json` is draft record-envelope direction.
- `docs/schemas/README.md` documents the schema namespace and current schema-family layering.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated projections remain evidence/review surfaces unless later cutover changes a file's disposition.

## Record-envelope purpose

A schema record envelope is a candidate common wrapper for schema-backed repository records.

Its purpose is to separate:

- common record metadata;
- family-specific content;
- provenance and evidence;
- projection/cutover state;
- schema identity and validation context.

The envelope is intended to reduce duplicated metadata semantics across ADR, implementation, workspace-state, and future document families when those families become schema-backed.

## Record-envelope non-purpose

The record envelope must not:

- redefine ADR lifecycle states;
- replace ADR content schema fields;
- make all repository documents schema-backed by default;
- demote Markdown source/control for unmigrated records;
- create database or storage authority;
- authorize renderer/ingester implementation;
- authorize migration or JSON authority cutover.

## `metadata` + `content` model as draft direction

The draft record-envelope direction uses exactly two top-level fields:

```text
metadata
content
```

`metadata` carries record-family-independent context such as identity, schema identity/versioning, lifecycle value when schema-backed, provenance, evidence, projection metadata, repository/domain typing, and timestamps.

`content` carries family-specific document content. ADR-specific fields belong in ADR content schemas, not in the generic envelope.

This model is draft direction only until a future schema-change/acceptance slice promotes it for a specific record family or repository-wide use.

## Metadata, provenance, and evidence separation

The extracted architecture preserves these separations:

- `origin` describes how the record entered the system.
- `source_artifacts` cites reviewed or input surfaces.
- `derived_from` identifies transformed or inherited source records.
- `evidence` records claim-supporting artifacts and validation evidence.
- `projections` records generated or rendered surfaces and their source/projection relationship.

`origin` must not be overloaded with source evidence, derivation, projection, or claim-support semantics.

Unsupported source material, observed status/casing, source hashes, conversion warnings, and omitted sections belong in metadata/provenance/evidence or sidecar material, not in ADR content unless a later schema decision explicitly promotes them.

## Relationship to ADR content schema

`docs/schemas/adr.schema.json` remains the current ADR content-shape schema.

The record envelope must not force envelope metadata into ADR `content`. ADR content remains responsible for ADR decision fields such as title/status/context/decision/consequences and other renderable ADR sections defined by the current ADR schema.

If future schema-backed ADR records use both `metadata.status` and `content.status`, a later schema-change slice must define the mirroring or conflict rule. This architecture does not implement that rule.

## Relationship to Markdown source/control and generated projections

Markdown under `docs/adr/` remains source/control for unmigrated records.

Generated Markdown projections are evidence or review/navigation surfaces unless a later accepted cutover package changes the disposition of a specific file.

The future target of JSON-authoritative records may use projection metadata to track render surfaces, hashes, generation methods, editability, and source-of-truth state. That target remains gated by later migration/cutover decisions.

## Relationship to `docs/schemas/README.md` and schema files

`docs/schemas/README.md` is the human-readable schema namespace/index surface.

Machine-readable schema authority lives in JSON schema files under `docs/schemas/` only when those files are explicitly accepted or preserved as current/draft/candidate by the schema namespace rules.

This architecture does not edit `docs/schemas/README.md` or any JSON schema. A future schema-change slice must decide whether to revise, wrap, replace, retire, or promote `schema.record-base.json` and related family schemas.

## Deferred renderer/ingester requirements

`docs/adr/adr.schema-base.md` contains useful renderer/ingester ideas, but implementation is deferred.

Future renderer/ingester work should require:

- deterministic JSON-to-Markdown rendering;
- strict Markdown-to-JSON mapping only for controlled surfaces;
- preservation of metadata/content separation;
- explicit handling of unsupported or out-of-contract material;
- validation evidence for round trips;
- no source overwrite without explicit review and approval.

Those requirements need a separate implementation brief and approval before VULCAN work.

## Non-actions and later gates

This architecture does not authorize:

- editing `docs/adr/adr.schema-base.md`;
- editing `docs/schemas/`;
- changing lifecycle state;
- accepting, activating, superseding, rejecting, promoting, or demoting existing sources;
- moving, renaming, deleting, archiving, or splitting files;
- JSON conversion or projection generation;
- generated projection replacement;
- authoritative JSON ADR records;
- database/storage authority;
- migration;
- JSON authority cutover.

Later gates remain required for:

1. schema-envelope authority under `docs/schemas/`;
2. renderer/ingester implementation;
3. source status repair for `docs/adr/adr.schema-base.md`;
4. generated projection policy;
5. migration and cutover packages.
