```json
{
  "title": "JSON schemas ADR conformance implementation plan",
  "artifact_type": "implementation-plan",
  "status": "planned-paused-for-approval",
  "datetime": "20260711.062654Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "source_request": "ATHENA/User handoff from subagent-chat-019f4f7e for next active YAGNI conformance slice",
  "target_source": "docs/adr/adr.json-schemas.draft.md",
  "schema": "docs/schemas/adr.schema.json",
  "next_owner": "ATHENA_OR_USER_OR_HERMES_APPROVAL",
  "coding_started": false
}
```

# Implementation plan 20260711.062654: JSON schemas ADR conformance

## Status

Planned and paused for ATHENA/user/Hermes approval. No implementation coding has been started by this plan.

## Source authority

- Handoff/request: ATHENA/User handoff from `subagent-chat-019f4f7e`.
- Target source ADR-shaped Markdown: `docs/adr/adr.json-schemas.draft.md`.
- Required schema: `docs/schemas/adr.schema.json` as currently updated, with no `routing` property.
- Existing storage substrate to reuse:
  - `src/python/projectkoios/bootstrap/control_surface/documents/`
  - `src/python/projectkoios/bootstrap/control_surface/storage/`
  - `src/python/projectkoios/bootstrap/control_surface/adr/`
- Existing one-ADR pilot evidence to leave intact unless explicitly needed as reference only:
  - `dev/adr-json-database-one-adr-pilot/`

## Objective

Convert/map the single source `docs/adr/adr.json-schemas.draft.md` into a schema-valid ADR JSON record using `docs/schemas/adr.schema.json`, without `routing` in the record.

The conformed JSON record is an active conformance artifact for this ADR going forward. It is not merely historical migration evidence. Sidecars preserve source and conversion provenance without reframing the conformed record as historical-only.

## Directory decision

Use a new target-specific conformance directory:

- `dev/adr-json-schemas-conformance/`

Rationale:

- The existing `dev/adr-json-database-one-adr-pilot/` is the representative storage-topology pilot for `adr.json-database-for-adr-storage`; reusing it for `adr.json-schemas` would mix two ADR identities and make evidence harder to review.
- A target-specific directory keeps the new active conformed record, projection, manifest, and sidecar evidence together.
- This remains YAGNI: no reusable repo-level ADR storage config, no bulk migration directory, and no global naming machinery.

## Proposed output artifact paths

Create these artifacts in the target-specific directory:

| Artifact | Proposed path | Purpose |
|---|---|---|
| JSON checkpoint / active conformed record | `dev/adr-json-schemas-conformance/adr.json-schemas.json` | Schema-valid ADR content record for `adr.json-schemas`, with no `routing`. |
| Markdown projection | `dev/adr-json-schemas-conformance/adr.json-schemas.projected.md` | Deterministic projection from the JSON record for review; does not overwrite source Markdown. |
| Conversion sidecar evidence | `dev/adr-json-schemas-conformance/conversion-evidence.json` | Source/provenance/mapping/hash evidence, including omitted `routing` and `links.related`. |
| Mapping sidecar | `dev/adr-json-schemas-conformance/mapping.json` | Field-level mapping details from source sections to schema fields. |
| Manifest/evidence index | `dev/adr-json-schemas-conformance/manifest.json` | Index of source, checkpoint, projection, schema, hashes, storage backend policy, and validation commands. |
| Database evidence | `dev/adr-json-schemas-conformance/database-evidence.md` | Human-readable evidence that the generic document store was exercised and no mutable DB file is committed. |
| Generated local DB path | `dev/adr-json-schemas-conformance/generated-local/conformance.sqlite` | Runtime-only/generated SQLite file; must be deleted or ignored before commit and verified absent from git. |

Do not mutate:

- `docs/adr/adr.json-schemas.draft.md`

## Reuse of existing document/storage substrate

Reuse the already-separated substrate rather than adding new storage architecture:

- Use `AdrMarkdownRecordParser` or a narrow extension of it to parse `docs/adr/adr.json-schemas.draft.md` into an ADR record shape.
- Use ADR-layer validation against `docs/schemas/adr.schema.json`.
- Use `DocumentStoreAdrStorageAdapter` over `DocumentStore` to persist/export the ADR record.
- Use `DocumentType.ADR` for document kind.
- Use `MemoryDocumentStore` in tests where possible to prove ADR logic is not coupled to SQLite.
- Use `SqliteDocumentStore` only to exercise the storage backend and capture database evidence.
- Use the generic `json_documents` table only; do not add ADR-specific columns.

No new backend kind, source-of-truth mode, lifecycle, naming, projection-policy, reusable config, or storage-authority model should be introduced unless approval explicitly expands scope.

## Record identity and lifecycle treatment

Planned JSON record identity:

```json
{
  "id": "adr.json-schemas",
  "slug": "json-schemas"
}
```

Planned lifecycle field treatment:

- Copy source status `draft` into record field `status: "draft"`.
- Do not promote the ADR to `accepted` or `active` lifecycle status in this slice.
- Interpret "active going forward" as: the JSON checkpoint is the active conformed record artifact for this target ADR after this slice, not historical-only evidence.
- Preserve source status date `20260702.213000Z` in sidecar evidence, not in the schema record, because the schema has no top-level `date` property.

Pause trigger: if ATHENA/user intends lifecycle status `active` inside the ADR JSON record rather than active artifact treatment, VULCAN must pause because that would be an ADR lifecycle decision, not a conformance-only implementation step.

## Mapping rules

### Copied fields

Copy these source values into the schema record with only structural conversion needed for JSON shape:

- `title`: from heading text after the timestamp prefix, expected value `JSON Schemas Namespace`.
- `status`: from `## Status`, expected value `draft`.
- `context.origin`: from `Origin`.
- `context.from`: from `From`.
- `context.acting_as`: from `Acting-As`.
- `context.scope`: from `Scope`.
- `context.repository`: from `Repository`.
- `context.delegated_operator`: from `Delegated-Operator`.
- `context.architecture_domain`: from `Architecture-Domain`.
- `decision`: from `## Decision` body.
- `consequences`: from `## Consequences` body.
- `architecture_spec`: from `## architecture-spec` body.
- `acceptance_criteria`: bullets from `## acceptance-criteria`.
- `implementation_brief`: from `## implementation-brief` body.
- `resolved_open_questions`: bullets from `## resolved_open_questions`.
- `non_goals`: bullets from `## non_goals`.
- `validation_expectations`: bullets from `## validation_expectations`.
- `links.back_to`: from `links.back_to`.
- `links.supersedes`: from `links.supersedes`, normalizing textual `None` to JSON `null`.
- `links.superseded_by`: from `links.superseded_by`, normalizing textual `None` to JSON `null`.

### Normalized fields

Normalize only where required by schema shape or existing parser conventions:

| Source | Record value / treatment |
|---|---|
| Markdown heading `# ADR 20260702.213000Z: JSON Schemas Namespace` | `title: "JSON Schemas Namespace"`; timestamp preserved in sidecar. |
| Source filename `adr.json-schemas.draft.md` | `id: "adr.json-schemas"`; `slug: "json-schemas"`. |
| Context labels with hyphens / capitals | Convert to schema snake_case keys. |
| Section headings with hyphenated names | Convert to schema snake_case field names. |
| `None` link values | Convert to JSON `null` for schema-compatible optional links. |
| Markdown bullets | Convert to arrays of strings for array-valued schema fields. |
| Canonical JSON formatting | Deterministic canonical JSON for record content hash and checkpoint output. |

### Omitted from schema record, preserved in sidecar

Do not populate these in the schema record because `docs/schemas/adr.schema.json` disallows them or does not define them:

- `routing.owner`
- `routing.next_phase`
- `routing.notes`
- `links.related`
- source status date line (`date: 20260702.213000Z`)
- source path and source hash
- generated projection path/hash
- database runtime path/evidence

Sidecar preservation is required; omission from the record must be explicit in `conversion-evidence.json` and `mapping.json`.

## Sidecar evidence shape

Planned `conversion-evidence.json` top-level shape:

```json
{
  "status": "active-conformance-record",
  "source": {
    "path": "docs/adr/adr.json-schemas.draft.md",
    "sha256": "<computed>",
    "date": "20260702.213000Z",
    "status": "draft"
  },
  "schema": {
    "path": "docs/schemas/adr.schema.json",
    "sha256": "<computed>",
    "routing_allowed": false
  },
  "record": {
    "id": "adr.json-schemas",
    "slug": "json-schemas",
    "path": "dev/adr-json-schemas-conformance/adr.json-schemas.json",
    "document_type": "adr",
    "content_hash": "<computed canonical JSON hash>",
    "schema_valid": true,
    "active_going_forward": true
  },
  "projection": {
    "path": "dev/adr-json-schemas-conformance/adr.json-schemas.projected.md",
    "sha256": "<computed>",
    "generated_from_record_hash": "<computed canonical JSON hash>"
  },
  "storage": {
    "documents_package": "projectkoios.bootstrap.control_surface.documents",
    "storage_package": "projectkoios.bootstrap.control_surface.storage",
    "adr_wrapper": "DocumentStoreAdrStorageAdapter",
    "sqlite_store": "SqliteDocumentStore",
    "memory_store": "MemoryDocumentStore",
    "table": "json_documents",
    "generated_local_database": "dev/adr-json-schemas-conformance/generated-local/conformance.sqlite",
    "committed_sqlite_or_db_files": false
  },
  "field_treatment": {
    "copied_fields": ["..."],
    "normalized_fields": {"...": "..."},
    "omitted_from_record_preserved_in_sidecar": {
      "routing": {
        "owner": "Athena",
        "next_phase": "proposed",
        "notes": "JSON schema/contract surface for the UI/core family."
      },
      "links.related": [
        {
          "label": "ADR 20260702.213000Z: Shared UI Core Namespace",
          "path": "adr.ui-core.draft.md"
        }
      ]
    }
  },
  "artifact_paths": {
    "old_source_markdown": "docs/adr/adr.json-schemas.draft.md",
    "new_json_checkpoint": "dev/adr-json-schemas-conformance/adr.json-schemas.json",
    "new_projection": "dev/adr-json-schemas-conformance/adr.json-schemas.projected.md",
    "new_manifest": "dev/adr-json-schemas-conformance/manifest.json",
    "new_mapping": "dev/adr-json-schemas-conformance/mapping.json",
    "new_conversion_evidence": "dev/adr-json-schemas-conformance/conversion-evidence.json"
  }
}
```

The exact arrays/maps may be tightened during implementation, but the evidence must preserve at least the fields listed in the handoff.

## Markdown projection behavior

Generate `dev/adr-json-schemas-conformance/adr.json-schemas.projected.md` from the conformed JSON record.

Projection constraints:

- Do not overwrite `docs/adr/adr.json-schemas.draft.md`.
- Do not render a schema-record `routing` field, because no such field exists.
- It may include a generated-evidence preamble or sidecar references only if consistent with existing projection behavior; do not redesign projection policy.
- Source `routing` and `links.related` remain in sidecar evidence, not in the schema record.

## Tests and validation plan

Planned focused tests or test updates:

- Add or update ADR conformance test for `docs/adr/adr.json-schemas.draft.md` using the existing parser/validation/storage path.
- Assert generated record validates against `docs/schemas/adr.schema.json`.
- Assert `routing` is absent from the generated JSON record.
- Assert source routing owner/next_phase/notes and `links.related` are present in sidecar evidence.
- Assert `links.related` is not present in the schema record.
- Assert source file hash/path/date/status are present in sidecar evidence.
- Assert JSON checkpoint hash and projection hash are generated and recorded.
- Assert storage goes through `DocumentStoreAdrStorageAdapter` / generic `DocumentStore` behavior, not ADR-specific SQLite columns.
- Assert no `.sqlite` or `.db` files are committed under `dev/adr-json-schemas-conformance/`.

Validation commands planned from repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/schema -q
uv run mypy src/python/projectkoios/bootstrap/control_surface tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/control_surface_storage
uv run ruff check src/python/projectkoios/bootstrap/control_surface tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/control_surface_storage
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/control_surface_storage
git diff --check
find dev/adr-json-schemas-conformance -type f \( -name '*.sqlite' -o -name '*.db' \) -print
```

If implementation only touches evidence-generation tests and existing code already supports the source, the full `uv run pytest -q` may also be run as final validation.

## Explicit non-goals

Do not:

- mutate `docs/adr/adr.json-schemas.draft.md`;
- populate `routing` in the ADR schema record;
- alter `docs/schemas/adr.schema.json`;
- redesign lifecycle status, routing, workflow state, naming machinery, projection policy, reusable config, or storage authority;
- bulk migrate other ADRs;
- reuse `dev/adr-json-database-one-adr-pilot/` as the target output directory;
- commit generated SQLite/database files;
- add ADR-specific query columns to the generic `json_documents` table;
- treat sidecars as the canonical ADR content record.

## Pause triggers / blockers

VULCAN must pause before coding now for approval of this plan.

Additional pause triggers during implementation:

1. The existing parser cannot represent `adr.json-schemas.draft.md` without adding broad parsing machinery.
2. Approval expects the JSON record's lifecycle `status` to become `active` instead of preserving source `draft`.
3. Approval expects output under `docs/adr/` or mutation of `docs/adr/adr.json-schemas.draft.md`.
4. Approval expects `links.related` in the schema record, requiring schema redesign.
5. Approval expects `routing` or workflow state in the schema record.
6. Implementation requires reusable repo-level config rather than target-local manifest/evidence.
7. Generic storage would need ADR-specific query columns or lifecycle indexes.
8. Source parsing reveals ambiguous field content that would require ATHENA architecture interpretation rather than mechanical mapping.

## Requested approval decision

Approve or revise:

1. New target-specific directory: `dev/adr-json-schemas-conformance/`.
2. Active conformed JSON checkpoint path: `dev/adr-json-schemas-conformance/adr.json-schemas.json`.
3. Preserve source status `draft` in the record while treating the checkpoint artifact as active going forward.
4. Preserve `routing.*` and `links.related` only in sidecar evidence.
5. Reuse existing generic document/storage substrate with no architecture expansion.
