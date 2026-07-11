---
status: draft-direction-accepted-pending-hierarchy-addendum-review
date: 20260711.132100Z
last_updated: 20260711.133600Z
back_to: architecture.00
related_architecture: architecture.json-adr-storage-topology.md
---

# Architecture: ADR Bidirectional JSON↔Markdown Objects

## Status

Draft direction accepted by USER/HERMES for continued architecture work; hierarchy/disposition addendum pending HERMES/USER review.

This document is an architecture surface only. It does not implement code, mutate ADR contents, publish `docs/schemas/` authority, authorize bulk migration, move or rename files, normalize statuses, or decide repository-wide ADR storage authority.

## Purpose

Define a bounded architecture model for rationalizing ADRs as explicit objects that can preserve a structured JSON ADR payload, generated Markdown projection metadata, provenance/conversion evidence, and conflict policy without losing authority clarity.

The USER concern is that existing ADRs are messy: ADR Markdown files, schema-valid JSON records, generated Markdown projections, and sidecar evidence already coexist, but the object/envelope boundary is not yet explicit. This document defines that boundary before any implementation or migration work.

## Source basis

This draft is grounded in:

- `docs/plans/architecture-intake.20260711.131140_adr-bidirectional-json-markdown-objects.md`
- `workspaces/koios/working/provenance-intake.20260711_adr-rationalization-json-md-object-track.md`
- `workspaces/koios/working/candidate-schema.20260711_adr-bidirectional-json-md-object.md`
- `workspaces/koios/working/classification-proposal.20260711_adr-hierarchy-rationalization.md`
- `docs/architecture/architecture.json-adr-storage-topology.md`

Related evidence includes:

- `docs/schemas/adr.schema.json`
- `dev/adr-json-database-one-adr-pilot/`
- `dev/adr-json-schemas-conformance/`
- `docs/implementation/adr-json-database-one-adr-pilot.20260711.035759.md`
- `docs/implementation/json-document-database-separation.20260711.051951.md`
- `docs/implementation/json-schemas-adr-conformance.20260711.065704.md`

## Scope

In scope:

- ADR object/envelope vocabulary.
- Relationship between ADR payload, Markdown projection metadata, source references, sidecar evidence, validation evidence, and conflict policy.
- Bidirectional JSON↔Markdown semantics for generated projections.
- Authority boundaries for candidate objects versus current ADR authority.
- Canary-first path for a reversible one-ADR slice.
- Rules for when candidate envelope/schema material may be promoted.

Out of scope:

- Code implementation.
- Editing or rewriting `docs/adr/*.md` source files.
- Bulk ADR migration.
- Publishing or modifying `docs/schemas/` authority.
- Promoting JSON, database, or generated Markdown projections to repository-wide ADR authority.
- Committing mutable database files.
- Replacing the accepted ADR lifecycle/naming authority.
- Petri-net workflow, Operator Console, or workflow-object integration.

## Relationship to JSON ADR storage topology

`docs/architecture/architecture.json-adr-storage-topology.md` remains the current storage topology/as-built surface for generalized JSON document storage, ADR-specific document-family code, SQLite pilot behavior, JSON checkpoints, Markdown projections, and deferred storage authority.

This document does not supersede that topology. It adds an explicit ADR object/envelope model above the existing topology:

```text
Generic document store
  stores JSON payloads behind adapter boundary

ADR document layer
  validates ADR payloads, projects Markdown, preserves mapping/evidence

AdrBidirectionalObject envelope
  groups content payload + projection metadata + provenance/evidence + conflict policy
```

The generic document store must stay free of ADR-specific columns and policy. ADR object behavior belongs in the ADR document-family layer above generic storage.

## Object model

### ADR content payload

`content` is the ADR payload intended to validate against `docs/schemas/adr.schema.json`.

Rules:

- Keep conversion/provenance-only fields out of `content` unless a separate schema decision promotes them into `docs/schemas/adr.schema.json`.
- Treat lifecycle status as ADR content only where the current ADR schema carries it.
- Do not force source filename suffixes, conversion warnings, source hashes, or unsupported source fields into the ADR payload.

### Bidirectional object envelope

The candidate envelope is an `AdrBidirectionalObject`, not a replacement for the plain ADR schema payload.

Conceptual fields:

| Field | Meaning | Authority boundary |
|---|---|---|
| `object_type` | Identifies the envelope as an ADR bidirectional object. | Envelope metadata only. |
| `object_version` | Version for envelope evolution. | Separate from ADR schema version. |
| `authority_mode` | Explicit authority label such as candidate, pilot evidence, active conformance record, or authority deferred. | Must not silently promote repository authority. |
| `content` | ADR schema-compatible payload. | Governed by current ADR schema unless separately changed. |
| `markdown_projection` | Projection mode, path/hash, generation method, marker expectation, and round-trip support. | Projection metadata, not source authority by default. |
| `conversion_evidence` | Source mutation flag, omitted/normalized/inferred fields, lossiness, warnings, mapping notes. | Evidence/provenance, not ADR content. |
| `source_refs` | Source, projection, schema, sidecar, report, and provenance refs with hashes/status observations where available. | Evidence for review and staleness detection. |
| `sidecar` | Fields preserved outside the ADR payload, such as unsupported source fields. | Durable or migration evidence depending on later decision. |
| `validation` | Schema, round-trip, source-mutation, database-file, and command evidence. | Evidence only. |
| `conflict_policy` | JSON-vs-Markdown, unsupported-field, and bulk-migration rules. | Must be explicit before mutation. |

## Bidirectional semantics

### First supported mode: generated projection round-trip

The first architecture-supported bidirectional mode is narrow:

```text
JSON object content
  -> deterministic generated Markdown projection
  -> parse generated projection
  -> compare semantic equality to original object content
```

This mode proves projection determinism and generated-projection parseability. It does not authorize broad hand-authored Markdown ingest.

Required invariants:

- Projection output is deterministic for unchanged object content and projection configuration.
- Generated projection carries enough marker/metadata to distinguish it from hand-authored source Markdown.
- Parse-back equality is semantic, not byte-for-byte Markdown equality.
- Projection metadata and sidecar evidence are preserved or explicitly classified as projection-only.
- Source Markdown mutation remains false unless a separate source-mutation decision is approved.

### Deferred mode: hand-authored Markdown ingest

Broad Markdown→JSON ingest for hand-authored ADRs is deferred.

Before hand-authored ingest is allowed, architecture must define:

- marker expectations for editable Markdown;
- conflict classification when source Markdown and JSON differ;
- preservation rules for comments, formatting-only changes, unsupported fields, source status casing, and filename-derived metadata;
- review gates before any source file overwrite;
- validation evidence proving source hash and projection hash behavior.

### Conflict policy

No silent overwrite is allowed.

Minimum conflict states:

- `no_conflict`: JSON content and generated Markdown parse-back are semantically equal.
- `projection_stale`: generated Markdown hash or content no longer matches current JSON content.
- `source_changed`: source Markdown hash changed since object creation.
- `unsupported_fields_preserved`: source fields are outside the ADR schema but preserved in sidecar.
- `lossy_requires_review`: conversion would drop or normalize material not safely preserved.
- `authority_conflict`: JSON, Markdown, or database state disagree and current authority rules do not choose a winner.

The first canary should use `projection_only_no_ingest` for JSON-vs-Markdown conflict policy.

## Authority boundaries

Current authority is not changed by this document.

Rules:

- Existing `docs/adr/*.md` files remain the current source/control surface according to existing ADR lifecycle and storage-topology boundaries unless a later ADR changes authority.
- `dev/` JSON records, generated projections, manifests, mappings, and conversion evidence remain bounded evidence unless explicitly promoted.
- The `AdrBidirectionalObject` envelope is candidate architecture, not `docs/schemas/` authority.
- JSON database/storage authority remains deferred to the ADR/storage topology decision path.
- Lifecycle/naming authority remains controlled by existing ADR lifecycle/naming surfaces; this object model must preserve those fields/refs but must not redefine status, activation, supersession, amendment, filename policy, or repeated-topic handling.

## Sidecar and provenance rules

Unsupported or extra source fields must not be discarded silently.

Preserve in `sidecar` or `conversion_evidence`:

- source Markdown path and content hash;
- observed source status and original casing where available;
- observed source date where available;
- filename suffixes such as `.draft.md` when relevant to source provenance;
- source fields not in `docs/schemas/adr.schema.json`, including legacy `routing.*` or unsupported link shapes such as `links.related`;
- normalized fields and their source values;
- inferred fields and rationale;
- projection path/hash and generation method;
- schema path/hash used for validation;
- source mutation flag.

Whether `sidecar` is durable companion object state or migration-only evidence remains a later decision. Until decided, sidecar material must be retained in evidence for every conversion canary.

## Provenance proportionality

Provenance is required where JSON↔Markdown conversion could change authority, lose source context, normalize status, drop unsupported fields, or confuse generated projections with source ADRs.

Provenance should remain proportional to the slice. For canaries, use lightweight evidence: source/projection/schema refs and hashes, unsupported-field sidecar notes, source-mutation checks, and concise validation output. Do not turn provenance into ceremony that blocks bounded implementation when authority boundaries, source preservation, and lossiness are already inspectable.

## ADR hierarchy and disposition model

KOIOS classification shows `docs/adr/` is not one uniform machine-readable hierarchy today. It contains accepted/current decisions, draft/provenance sources, architecture-like blueprints, process/policy drafts, templates/contracts/schema surfaces, implementation workflow support documents, and product/future-system drafts.

This architecture uses those classes as object metadata and review guidance only. It does not move, rename, edit, accept, reject, supersede, normalize, or migrate any ADR file.

### Target categories

`AdrBidirectionalObject` may record a `classification` or `disposition` block in its envelope metadata. That block is evidence about how the object should be reviewed, not a change to ADR authority.

Target categories:

| Category | Meaning | Default disposition |
|---|---|---|
| `current_decision` | Accepted/active bounded decision records that may currently control behavior or interpretation. | Preserve as current authority; canary only with explicit non-mutation evidence. |
| `source_provenance_draft` | Drafts retained as source/provenance for accepted decisions or future architecture work. | Preserve as provenance; do not silently supersede or delete. |
| `architecture_blueprint` | Documents in ADR space that behave like controlled architecture surfaces or system blueprints. | Treat as architecture-rationalization candidates; do not move without separate approval. |
| `policy_process` | Operating policy, review procedure, lifecycle process, ownership, or workflow mechanics. | Treat as policy/process candidates; preserve current status until promoted. |
| `template_schema_contract` | Reusable template, schema, namespace, or control-surface contract material. | Treat as contract/schema candidates; no `docs/schemas/` publication without separate decision. |
| `implementation_workflow_support` | Implementation brief/plan, verification, spike, or ADR-to-implementation workflow support concepts. | Preserve as workflow-support provenance unless promoted into meta-harness policy/architecture. |
| `product_future_system_draft` | Product/domain, UI, agent-runtime, training, or future-system drafts in bootstrap ADR space. | Require owner/domain review before promotion; do not treat as bootstrap authority by default. |

### Envelope recording rules

When an `AdrBidirectionalObject` includes hierarchy/disposition metadata, the metadata must be outside the ADR schema payload:

```text
AdrBidirectionalObject
├── content                 # ADR payload compatible with docs/schemas/adr.schema.json
├── classification          # category/disposition evidence, not ADR status authority
├── source_refs             # paths, hashes, observed status/casing, source role
├── sidecar                 # unsupported source fields and provenance material
└── validation              # checks proving source files were not mutated
```

Rules:

- Do not add classification/disposition fields to `content` unless a separate ADR schema decision promotes them.
- Record observed source status and casing as provenance, not normalized status.
- Record proposed category, uncertainty, and rationale as evidence.
- Record whether a source is `canary_source`, `provenance_only`, `current_authority_source`, `architecture_candidate`, or `domain_review_required` as envelope metadata only.
- Do not let category labels change lifecycle status, filename, authority, or storage/source-of-truth mode.

### Provenance-only vs canary evidence

Remain provenance-only for now:

- lifecycle/naming source drafts unless explicitly promoted or superseded;
- draft process/protocol documents with no accepted consolidation;
- `dev/` pilot/conformance artifacts as evidence rather than repository-wide authority;
- KOIOS candidate schema and classification files under `workspaces/koios/working/`;
- product/future-system drafts until domain ownership is clarified;
- observed status/casing scans until a validated parser/tooling slice confirms them.

Canary evidence may use exactly one selected source file to prove object mechanics. Canary use means the source is cited and hashed, not moved, renamed, status-normalized, accepted, superseded, or rewritten.

Canary evidence may include:

- candidate object envelope JSON under a dev evidence path;
- copied/derived `content` payload compatible with current ADR schema;
- sidecar preservation of unsupported fields;
- generated Markdown projection under dev evidence;
- validation report proving generated-projection round-trip and unchanged source Markdown;
- category/disposition metadata proving classification can be represented without authority mutation.

### First canary category

`docs/adr/adr.json-schemas.draft.md` belongs to category `template_schema_contract`, with an architecture-blueprint/schema-namespace aspect.

For the first canary, treat it as:

```text
category: template_schema_contract
secondary_aspect: architecture_blueprint
source_role: canary_source
source_authority_effect: none
```

Rationale:

- KOIOS classifies it as `E/C: schema namespace draft` with low uncertainty.
- It is schema-adjacent and already has one-document conformance evidence.
- It contains preservation canaries for unsupported source material.
- It exercises the category/disposition model without changing ADR status or repository-wide schema authority.

### Explicit non-actions

This hierarchy/disposition model does not authorize:

- file moves;
- file renames;
- source ADR edits;
- status normalization or status changes;
- marking drafts as superseded;
- publishing or changing schemas under `docs/schemas/`;
- bulk migration;
- code implementation;
- promoting JSON/database/generated Markdown as repository-wide ADR authority;
- treating product/future-system drafts as bootstrap authority without owner/domain review.

## Canary-first path

The first implementation slice, if later approved, should be a one-ADR canary rather than a corpus migration.

Preferred canary:

- `docs/adr/adr.json-schemas.draft.md`

Rationale:

- It is small and schema-adjacent.
- It already has one-document conformance evidence.
- It contains useful preservation canaries such as prior `routing.*` and unsupported `links.related` material.
- It avoids conflating object mechanics with the separate storage-authority ADR.

Candidate slice name:

```text
adr-bidirectional-object-canary-slice-0
```

Candidate canary scope:

- create exactly one candidate `AdrBidirectionalObject` envelope for the canary ADR;
- record canary category/disposition metadata outside the ADR `content` payload;
- preserve `content` as an ADR schema-compatible payload;
- preserve unsupported source/provenance fields in sidecar/evidence;
- generate deterministic Markdown projection under a dev evidence directory;
- prove JSON→Markdown→object semantic equality for generated projection only;
- prove source Markdown remains unmutated;
- do not write to `docs/adr/`;
- do not publish `docs/schemas/`;
- do not bulk migrate.

## Schema-promotion rules

KOIOS's candidate schema sketch is valuable input but is not schema authority.

Promotion rules:

1. Keep `docs/schemas/adr.schema.json` as the ADR content payload schema unless repeated canary/conformance evidence shows a concrete need to revise it.
2. Keep the envelope schema separate from the ADR payload schema until USER/HERMES accepts a schema-authority path.
3. Do not copy candidate schema text into `docs/schemas/` without an explicit schema-promotion decision.
4. Require at least one canary with validation evidence before promoting the envelope from architecture candidate to implementation/schema authority.
5. Require a corpus inventory/classification before any bulk migration authority.
6. Require explicit authority-mode values so candidate, evidence, active conformance, projection, and repository-authoritative states cannot be confused.
7. Require conflict policy and source-mutation checks before any editable Markdown ingest or source overwrite.
8. Preserve generic document store separation: no ADR-specific fields in generic storage schema to support this envelope.

## Future implementation brief criteria

A future VULCAN brief should not be written until HERMES/USER accepts this architecture direction or supplies corrections.

If accepted, the brief should require:

- one canary only;
- no `docs/adr/` source mutation;
- no `docs/schemas/` publication or schema change;
- no bulk migration;
- no mutable database commit;
- explicit content/schema validation;
- generated-projection parse-back semantic equality;
- sidecar preservation of unsupported fields;
- source/projection/schema hash evidence;
- `git status --short -- docs/adr` evidence showing no source ADR edits.

## Open questions for HERMES/USER

1. Is `AdrBidirectionalObject` the preferred envelope name, or should this use `AdrDocumentObject` to align with the generalized document-store vocabulary?
2. Should the envelope become a durable companion object eventually, or remain migration/conversion evidence only until storage authority is accepted?
3. Is `adr.json-schemas.draft.md` the right first canary, or should a messier ADR be selected after the generated-projection mode is proven?
4. Should the first canary include database adapter exercise, or stay file/envelope/projection-only to avoid conflating object mechanics with storage authority?

## Recommended next state

Pause for HERMES/USER review of the hierarchy/disposition addendum.

If approved, ATHENA should draft a bounded implementation brief for `adr-bidirectional-object-canary-slice-0`. Until then, this document authorizes no implementation, migration, schema publication, file movement, file rename, status normalization, bulk conversion, or source ADR mutation.
