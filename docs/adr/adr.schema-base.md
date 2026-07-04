# ADR: Schema Base Class for ADR Records

## Context

```json
{
  "record_id": "adr.schema-base",
  "schema_id": "https://projectkoios.local/schemas/schema.record-base.json",
  "schema_version": "0.1.0-draft",
  "record_version": "0.1.0-draft",
  "title": "Schema Base Class for ADR Records",
  "status": "draft",
  "created_on": "20260704.153108",
  "updated_on": "20260704.172632",
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
  },
  "source_artifacts": [
    {
      "path": "docs/plans/schema-base-adr-records-workplan.md",
      "role": "ATHENA",
      "relationship": "controls",
      "note": "Workplan integrating KOIOS, HERMES, and VULCAN review points for the pre-Vulcan schema-base slice."
    },
    {
      "path": "docs/schemas/README.md",
      "role": "ATHENA",
      "relationship": "supports",
      "note": "Schema namespace authority and migration table."
    },
    {
      "path": "docs/schemas/schema.record-base.json",
      "role": "ATHENA",
      "relationship": "supports",
      "note": "Draft base schema for the metadata/content envelope."
    },
    {
      "path": "docs/schemas/adr-draft.schema.json",
      "role": "ATHENA",
      "relationship": "supports",
      "note": "Draft ADR-family schema composed with the base schema."
    },
    {
      "path": "intercom:subagent-chat-019f2c6d/bd69199b-c1dd-4bef-bcc1-ff94fc892ede",
      "role": "KOIOS",
      "relationship": "review",
      "note": "KOIOS provenance review of this pre-Vulcan slice."
    }
  ],
  "derived_from": [],
  "evidence": [
    {
      "kind": "file",
      "ref": "docs/schemas/README.md",
      "claim": "docs/schemas/ is the draft durable namespace for machine-readable schema artifacts until ADR promotion."
    },
    {
      "kind": "file",
      "ref": "docs/schemas/schema.record-base.json",
      "claim": "The base schema draft defines the metadata/content envelope and provenance field definitions."
    },
    {
      "kind": "file",
      "ref": "docs/schemas/adr-draft.schema.json",
      "claim": "The draft ADR-family schema composes with the base schema and constrains draft ADR content."
    },
    {
      "kind": "review",
      "ref": "intercom:subagent-chat-019f2c6d/bd69199b-c1dd-4bef-bcc1-ff94fc892ede",
      "claim": "KOIOS reviewed provenance, projection, and rejected-content semantics and identified pre-handoff corrections."
    }
  ],
  "projections": [
    {
      "path": "docs/adr/adr.schema-base.md",
      "projection_type": "editable_markdown",
      "source_record_id": "adr.schema-base",
      "source_schema_id": "https://projectkoios.local/schemas/schema.record-base.json",
      "source_schema_version": "0.1.0-draft",
      "projection_method": "manual",
      "generated_by": "ATHENA",
      "editable": true,
      "source_of_truth": "projection"
    }
  ]
}
```

## Content

In this draft architecture slice, the repository keeps machine-readable schema artifacts under `docs/schemas/`, including:

- `docs/schemas/adr.schema.json`
- `docs/schemas/schema.record-base.json`
- `docs/schemas/adr-draft.schema.json`
- `docs/schemas/adr-active.schema.json`
- `docs/schemas/legacy-architecture.adr.schema-adr.json`
- `docs/schemas/adr.schema-implementation.json`
- `docs/schemas/legacy-architecture.adr.schema-implementation.json`

These files do not yet share an explicit schema-family architecture. The ADR
record schema and implementation schema repeat common concepts such as identity,
status, owner, human-readable surface, governed scope, invariants, and transition
rules. Without a shared base contract, schema evolution can drift by file and the
project cannot reliably move toward schema-first document state.

The user specifically identified `adr.schema-ADR.md` / ADR schema material as a
surface that should have a schema base class.

## Decision

Define a schema-family architecture with a shared base class for repository
schema records.

The shared schema base class MUST define fields and invariants common to all
schema-backed repository document records. ADR-specific, implementation-specific,
workspace-state-specific, or future schema families MUST extend the base class
rather than duplicate its core identity and lifecycle fields.

The base class SHOULD be represented in implementation as a small immutable model
or abstract data contract. The JSON Schema representation SHOULD expose the same
base fields through `$defs` and `$ref`, or through an equivalent schema
composition mechanism.

The initial base class SHOULD include exactly two top-level fields:

   - `metadata`
   - `content`

The `metadata` object SHOULD include only common fields needed to identify,
route, prove, and govern the record:

   - `record_id`
   - `schema_id`
   - `schema_version`
   - `record_version`
   - `title`
   - `status`
   - `created_on`
   - `updated_on`
   - `origin`
   - `scope`
   - `repository`
   - `domain`
   - `source_artifacts`
   - `derived_from`
   - `evidence`
   - `projections`

`origin` MUST describe only how the record entered the system:

   - `type`
   - `method`
   - `actor`
   - `authority`

`origin` MUST NOT carry source evidence, derivation, projection, or claim-support
semantics. Those semantics MUST live in `source_artifacts`, `derived_from`,
`evidence`, and `projections`.

`source_artifacts` lists records, files, messages, or other inputs cited or
reviewed by the current record. `derived_from` lists records whose content has
been transformed, inherited, or migrated into the current record. A
`SourceArtifact.relationship` value describes the source's relationship to the
current record within the array where it appears; records SHOULD avoid using a
`derived_from` relationship value in `source_artifacts` when the separate
`derived_from` array is the intended semantic.

Each projection MUST declare the source record identity, source schema identity
and version, projection method, generated-by actor or component, editability,
and source-of-truth status. Until a separate schema-backed JSON source record is
materialized, an editable Markdown ADR with embedded metadata MUST declare itself
as a draft editable projection rather than implying that an external schema
record is already the source of truth.

The `content` object SHOULD contain all family-specific document content. The
base class MUST NOT define ADR-specific, implementation-specific, or
workspace-specific content fields. Those fields MUST be deferred to the
controlling family schema.

The schema base class MUST NOT decide product architecture, renderer behavior,
transport mechanics, or runtime implementation strategy. It defines common record
shape only.

## Consequences

- ADR, implementation, workspace-state, and future schema records gain a common
  metadata/content envelope.
- Duplicate ADR schema files can be reconciled against a single family model.
- Schema-first document state becomes easier to validate and evolve.
- Future implementation can introduce code-level models without inventing field
  semantics from each schema file independently.
- Existing schema files may need migration or compatibility aliases.

## architecture-spec

The schema architecture has three layers:

1. Base record contract
   - Defines only the shared `metadata` + `content` envelope.
   - Defines common metadata fields for identification, routing, provenance, and domain typing.
   - Does not define family-specific `content` fields.

2. Family-specific record contracts
   - ADR schema constrains the `content` object for decision and architecture fields.
   - Implementation schema constrains the `content` object for execution, validation, and deviation fields.
   - Workspace-state schema may later constrain the `content` object for live state surfaces.

3. Rendered document surfaces
   - Markdown ADRs, implementation reports, and workspace state files are
     human-readable surfaces.
   - JSON Schema and code models define machine-checkable structure.
   - A rendered document MUST NOT become a separate authority when a schema-backed
     record exists; it is a projection or companion of the record state.
   - Markdown ADR renders MAY be editable projection surfaces when a controlling
     ingester maps them back into schema-backed JSON and preserves provenance.
   - Generated Markdown projections MUST declare source record identity, schema
     identity/version, projection method, editability, and source-of-truth status.
   - Schema-backed Markdown sections SHOULD render in the general form:

      ```text
      ## <Section>

      <Non-normative descriptive paragraph. Length limit defined by the controlling schema.>

      ### Concern

      - MUST ...
      - MUST NOT ...
      - SHOULD ...
      - SHOULD NOT ...
      - MAY ...

      ### <Subsection>
      ```

   - Normative concern keywords SHOULD be ordered as `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, then `MAY` when multiple concern levels appear together.
   - The controlling schema MUST define required sections, allowed subsections, and descriptive paragraph length limits.
   - Draft ADR section descriptions SHOULD NOT exceed 600 characters unless a later controlling schema changes that limit.
   - Markdown content that does not conform to the controlling schema MUST be handled by one of two deterministic ingester paths:
     - reject the document as a fatal ingest error when required metadata is missing or invalid, required sections are omitted, required section order is violated, normative concern keywords are malformed, heading depth is ambiguous, or metadata/content separation would be lost;
     - capture the material under `## Rejected` when the source document is otherwise valid but contains extra sections, unknown subsections, non-normative overflow text, duplicate optional sections, or other mappable-but-out-of-contract content.
   - Ingester normalization MAY be limited to presentational whitespace, line wrapping, and ordered concern grouping when tests prove semantic equivalence.

Recommended implementation names:

   - `SchemaRecordBase`
   - `MarkdownRenderer`
   - `MarkdownIngester`
   - `AdrRecordBase`
   - `DraftAdrRecord`
   - `ImplementationSchemaRecord`
   - `WorkspaceStateSchemaRecord` only if and when workspace state becomes
     schema-backed beyond top JSON metadata sections.

The first implementation slice SHOULD provide four bounded components:

   1. JSON to Markdown renderer
      - Consumes a schema-backed JSON record.
      - Emits the Markdown render form defined by the controlling schema.
      - MUST NOT invent fields not present in the JSON record or schema defaults.

   2. Markdown to JSON ingester
      - Consumes a Markdown render that follows the controlled section form.
      - Emits a schema-backed JSON record.
      - MUST preserve metadata/content separation.
      - SHOULD reject Markdown that cannot be mapped to the controlling schema.

   3. Constrained ADR abstraction
      - Defines ADR-family behavior shared by all ADR lifecycle states.
      - MUST remain constrained by `AdrRecordBase` and the ADR schema.
      - MUST NOT become a generic document model for non-ADR records.

   4. Concrete Draft ADR implementation
      - Implements the draft ADR state as a concrete ADR record type.
      - MUST satisfy the base schema and ADR-family schema.
      - SHOULD support round-trip JSON -> Markdown -> JSON tests before other ADR states are added.

Recommended schema composition:

   - `schema.record-base.json` is the base envelope schema.
   - Family schemas SHOULD compose the base with JSON Schema `$ref` plus `allOf` for the first implementation slice.
   - Family schemas MUST constrain `content` and MAY narrow metadata constants such as `schema_id` and `status` without redefining unrelated base metadata fields.
   - If the lightweight validator cannot resolve project-local `$id` URLs directly, implementation SHOULD provide an explicit local schema registry that maps `https://projectkoios.local/schemas/<filename>` to `docs/schemas/<filename>`.
   - `adr-draft.schema.json` is the first new ADR-family schema and references the base definition.
   - `adr-active.schema.json` preserves the migrated current ADR record schema candidate for reconciliation.
   - `adr.schema-implementation.json` references the base definition in a later slice.

Schema `$id` values SHOULD use the project schema URL form:

   - `https://projectkoios.local/schemas/<filename>`

Machine-readable schema artifacts SHOULD live under `docs/schemas/`.

The previous duplicate schema locations under `docs/adr/` and `docs/architecture/`
SHOULD remain retired from draft schema authority. During migration,
compatibility mirrors or redirects MAY be added if tooling requires them, but the
draft durable schema namespace SHOULD be `docs/schemas/` until this ADR is
promoted or accepted. Implementation MUST NOT assume legacy copies are equally
authoritative after the namespace migration.

## acceptance-criteria

- A reviewer can identify the shared `metadata` + `content` envelope without reading ADR or
  implementation-specific schema files.
- ADR schema and implementation schema are specified as constraints on the `content`
  object within a shared base record contract.
- The architecture distinguishes schema contracts from Markdown render surfaces.
- `docs/schemas/` is identified as the preferred durable namespace for machine-readable schema artifacts.
- Duplicate ADR schema contents are explicitly identified as a reconciliation issue inside `docs/schemas/`.
- No implementation work is authorized until the `docs/schemas/` schema-family migration path is confirmed.
- Base metadata provenance fields are explicit and not overloaded into `origin`.
- Markdown projection/editable-projection semantics are defined before renderer/ingester implementation.

## implementation-brief

If accepted, prepare a Vulcan implementation brief that:

1. introduces a `SchemaRecordBase` model or equivalent immutable data contract with
   only `metadata` and `content` at the top level;
2. writes a base JSON Schema for `metadata` + unconstrained family `content`;
3. writes an ADR-family schema that constrains ADR `content`;
4. introduces a constrained `AdrRecordBase` abstraction;
5. introduces a concrete `DraftAdrRecord` implementation;
6. adds a JSON to Markdown renderer for schema-backed ADR records;
7. adds a Markdown to JSON ingester for controlled ADR Markdown renders;
8. reconciles duplicate schema JSON contents now colocated in `docs/schemas/` with documented
   compatibility mirrors or redirects where needed;
9. adds tests proving shared metadata fields, ADR-specific content fields, and
   JSON -> Markdown -> JSON round trips are enforced;
10. preserves current validation behavior while adding the base-class and renderer/ingester layer.

## resolved_open_questions

- Resolved: the durable machine-readable schema namespace should be `docs/schemas/`.
- Resolved: existing ADR and architecture JSON schema artifacts have been moved into `docs/schemas/`; duplicate contents still require schema-family reconciliation.
- Resolved: base records use exactly two top-level fields, `metadata` and `content`.
- Resolved: `origin` uses `{type, method, actor, authority}` and does not carry source evidence or projection semantics.
- Resolved: provenance fields are explicit metadata fields: `record_id`, `schema_id`, `schema_version`, `record_version`, `created_on`, `updated_on`, `source_artifacts`, `derived_from`, `evidence`, and `projections`.
- Resolved: `title` is metadata; Markdown renderers may project it into headings without making a second content authority.
- Resolved: schema `$id` values use `https://projectkoios.local/schemas/<filename>`.
- Resolved: Markdown ADR files are editable projection surfaces only when a strict ingester maps them back to schema-backed JSON while preserving provenance.
- Resolved: fatal ingest errors are reserved for invalid/missing metadata, missing required sections, required section order violations, malformed normative concern keywords, ambiguous heading depth, and any case that would lose metadata/content separation.
- Resolved: otherwise valid but out-of-contract extra material is captured under `## Rejected` when deterministic mapping is possible.
- Resolved: family schemas should use JSON Schema `$ref` plus `allOf` against `schema.record-base.json` for the first slice, with a local schema registry if the validator cannot resolve project-local `$id` URLs directly.

## open_questions

- None for the current pre-Vulcan schema-base slice.

## non_goals

- Implementing the base class in code from Athena.
- Selecting a graph database, vector store, or runtime persistence layer.
- Changing ADR lifecycle status without review.
- Editing architecture index files without Hermes/Zeus direction.

## validation-expectations

- Schema files validate as JSON Schema after refactor.
- Existing ADR schema validation tests continue to pass or are migrated to `docs/schemas/` with an
  explicit compatibility note.
- Base schema validation rejects any top-level field other than `metadata` and `content`.
- A sample ADR record and implementation record can be validated against their
  family schema while sharing the same base fields.
- A draft ADR JSON record can render to Markdown and ingest back to equivalent JSON.
- Markdown that violates required metadata, required schema sections, section ordering, normative concern syntax, heading depth, or metadata/content separation is rejected.
- Duplicate schema file behavior is tested or documented as compatibility-only.

## routing

- Owner: Athena
- Next phase: review
- Notes: Architecture draft for schema-family base class and ADR schema reconciliation.

## links

- back_to: architecture.00
- related: docs/adr/adr.json-schemas.draft.md
- related: docs/architecture/architecture.json-schemas.md
- related: docs/schemas/adr-draft.schema.json
- related: docs/schemas/adr-active.schema.json
- related: docs/schemas/legacy-architecture.adr.schema-adr.json
- supersedes: None
- superseded_by: None

## Comments

- ATHENA: Created in response to user review that ADR schema material needs a schema base class.
