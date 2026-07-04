# Implementation brief 20260704.172632: Schema-record base and draft ADR record slice

## Status

Implementation-ready draft for VULCAN review/execution.

## Provenance

- Acting-As: ATHENA
- Repository: projectkoios-bootstrap
- Workspace: workspaces/athena/
- Source ADR: `docs/adr/adr.schema-base.md`
- Source workplan: `docs/plans/schema-base-adr-records-workplan.md`
- Source schemas: `docs/schemas/schema.record-base.json`, `docs/schemas/adr-draft.schema.json`
- Source namespace note: `docs/schemas/README.md`
- KOIOS provenance review: `intercom:subagent-chat-019f2c6d/bd69199b-c1dd-4bef-bcc1-ff94fc892ede`
- HERMES document-state review: `intercom:subagent-chat-019f2c3f`
- VULCAN implementation-readiness review: `intercom:subagent-chat-019f2c4b`

## Authority boundary

This brief translates the draft schema-base architecture into a bounded implementation slice. It does not promote `docs/adr/adr.schema-base.md` to accepted ADR status and does not authorize broad schema migration, historical ADR migration, GraphRAG changes, or product architecture decisions.

VULCAN owns implementation, tests, validation, implementation reports, and deviation reports. ATHENA owns architecture-conformance review. KOIOS owns durable knowledge/provenance review if new knowledge claims are added. Hermes/user direction is still needed for staging or commit separation if this slice coexists with dirty GraphRAG work in the same checkout.

## Objective

Introduce a narrow schema-record foundation for draft ADR records:

1. base record envelope with exactly `metadata` and `content`;
2. local loading/validation of JSON Schemas from `docs/schemas/`;
3. immutable Python record models for the base metadata and one concrete `DraftAdrRecord`;
4. deterministic JSON -> Markdown rendering for draft ADR records;
5. strict Markdown -> JSON ingest for the controlled draft ADR render;
6. round-trip tests proving metadata/provenance preservation.

## Package boundary

Implement outside the active GraphRAG ingestor tree. Recommended package boundary:

```text
src/python/projectkoios/bootstrap/schema_records/
  __init__.py
  models.py
  schemas.py
  adr_markdown.py
  paths.py
```

If an equivalent package path is chosen, document the reason in the implementation report. Do not add this slice under `src/python/projectkoios/ingestors/`.

## Required implementation behavior

1. Load canonical schemas from `docs/schemas/`.
2. Provide an explicit local schema registry/resolver for `https://projectkoios.local/schemas/<filename>` so validation does not require network access.
3. Validate against JSON Schema draft 2020-12 with a named/pinned Python validator API.
4. Enforce the base top-level envelope: only `metadata` and `content` are allowed.
5. Enforce required base metadata fields from `schema.record-base.json`.
6. Preserve `origin` as `{type, method, actor, authority}` and do not mix evidence/derivation/projection semantics into it.
7. Represent source artifacts, derived-from artifacts, evidence, and projections as separate metadata fields.
8. Implement immutable construction from valid dictionaries/JSON for the base record and `DraftAdrRecord`.
9. Keep `content` family-owned; do not turn the base model into a generic Markdown/document model.
10. Implement `DraftAdrRecord` only; defer active/completed/superseded/rejected ADR states.

## Markdown renderer contract

The renderer consumes a validated draft ADR record and emits deterministic Markdown.

Renderer output MUST:

- project title from `metadata.title` only;
- preserve metadata/provenance fields without inventing fields not present in the source record or explicit schema/model defaults;
- render sections in the deterministic draft ADR order defined by the family model/schema;
- render normative concerns in the order `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, `MAY` when grouping is required;
- distinguish generated Markdown from editable projection metadata according to the projection fields;
- avoid treating the Markdown render as an independent authority when a schema-backed JSON record exists.

## Markdown ingester contract

The ingester consumes controlled draft ADR Markdown and emits a schema-backed JSON/dict record.

The ingester MUST fail fatally for:

- missing or invalid metadata;
- missing required sections;
- required section order violations;
- malformed normative concern keywords;
- ambiguous heading depth;
- any case that would lose metadata/content separation.

The ingester SHOULD capture otherwise valid but out-of-contract content under `content.rejected` / `## Rejected` when deterministic mapping is possible, including extra sections, unknown subsections, non-normative overflow text, and duplicate optional sections.

Unmappable or lossy content MUST be a fatal ingest error, not `rejected` content.

Purely presentational whitespace, line wrapping, or concern grouping normalization MAY be allowed only when tests prove semantic equivalence and document the normalization.

## Test obligations

### Schema validation tests

- Base schema accepts only top-level `metadata` and `content`.
- Base schema rejects extra top-level fields.
- Base schema requires all settled metadata fields.
- Draft ADR schema narrows `metadata.schema_id` and `metadata.status` while preserving base metadata requirements.
- Local registry resolves project-local `$id` URLs offline.
- `allOf` plus base `additionalProperties: false` behavior is proven with the chosen validator.

### Model tests

- Immutable construction succeeds from valid JSON/dict fixtures.
- Missing or invalid metadata fails before render or ingest.
- ADR content remains ADR-family-owned and does not become generic document behavior.
- Timestamp and enum validation use new fixtures; do not migrate historical records in this slice.

### Renderer tests

- Renderer emits deterministic section order.
- Title is projected from metadata only.
- Normative concerns are ordered consistently.
- Renderer does not invent fields/defaults except explicit schema/model defaults.

### Ingester tests

- JSON -> Markdown -> JSON round trip preserves metadata/provenance exactly, except for explicitly documented allowed normalization.
- Fatal rejection occurs for missing metadata, missing sections, section order violations, malformed concern keywords, ambiguous heading depth, and metadata/content separation loss.
- Extra valid-but-out-of-contract material is captured under `rejected` / `## Rejected` when deterministic.
- Paragraphs exceeding the 600-character draft ADR section description limit are tested explicitly.

### Path and namespace tests

- Canonical schemas load from `docs/schemas/`.
- Legacy schema files are not treated as canonical.
- The local schema registry maps `https://projectkoios.local/schemas/<filename>` to the matching file under `docs/schemas/`.

## Validation commands

VULCAN should choose the final test command set, but the implementation report SHOULD include at minimum:

```bash
python -m json.tool docs/schemas/schema.record-base.json
python -m json.tool docs/schemas/adr-draft.schema.json
pytest <schema-record test paths>
```

If the project uses a broader required test command, include it in the implementation report and identify any unrelated failures.

## Non-goals

Do not add in this slice:

- implementation under `projectkoios.ingestors`;
- GraphRAG behavior changes;
- CLI integration unless needed only for isolated test support;
- active/completed/superseded/rejected ADR record implementations;
- implementation-report or workspace-state record families;
- broad historical ADR migration;
- legacy schema reconciliation beyond proving legacy files are non-canonical;
- product architecture decisions;
- database, vector-store, or renderer productization behavior.

## Expected output artifacts

- New implementation files under the schema-record package boundary.
- Tests covering schema loading, model construction, renderer behavior, ingester behavior, and namespace/path behavior.
- Implementation report under `docs/implementation/` summarizing changes, validation output, deviations, and any validator/API version decisions.
- Deviation report if validator behavior or package boundaries require changing this brief.

## Ready-to-implement condition

This brief is ready for VULCAN implementation after worktree isolation or commit/staging separation is agreed for the concurrent dirty GraphRAG/schema migration state. Implementation should proceed from this brief and the cited source artifacts, not from hidden intercom/chat memory.
