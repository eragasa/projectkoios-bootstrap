```json
{
  "title": "JSON document database separation implementation plan",
  "artifact_type": "implementation-plan",
  "status": "planned-paused-for-approval",
  "datetime": "20260711.050606Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "source_brief": "docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md",
  "architecture": "docs/architecture/architecture.json-adr-storage-topology.md",
  "next_owner": "USER_OR_HERMES_APPROVAL",
  "coding_started": false
}
```

# Implementation plan 20260711.050606: JSON document database separation

## Status

Planned and paused for user/Hermes approval. No implementation coding has been started by this plan.

## Source authority

- Brief: `docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md`
- Architecture: `docs/architecture/architecture.json-adr-storage-topology.md`
- Current pilot code: `src/python/projectkoios/bootstrap/control_surface/adr/`
- Current pilot evidence: `dev/adr-json-database-one-adr-pilot/`

## Implementation objective

Refactor the one-ADR pilot so SQLite-backed JSON persistence is a generic JSON document-store substrate, while ADR-specific mapping, schema validation, naming/lifecycle metadata, projection, equality, and pilot evidence remain in the ADR layer.

This is an intentional replacement slice. Backward compatibility with prior ADR-specific adapter/table names is not required. Prior names and hashes must be preserved as migration/migration evidence.

## Proposed package and module paths

### Generic document-store substrate

New package:

- `src/python/projectkoios/bootstrap/control_surface/documents/` and `src/python/projectkoios/bootstrap/control_surface/storage/`

Proposed modules:

- `__init__.py` — exports generic substrate types.
- `models.py` — `DocumentRecord`, `DocumentMetadata`, and scoped enum/type definitions for generic semantic values.
- `hashing.py` — canonical JSON text/hash helpers for generic payloads, or imports existing generic-safe canonicalization if kept shared.
- `store.py` — `DocumentStore` protocol and in-memory implementation.
- `sqlite.py` — SQLite implementation and generic DDL.

### ADR wrapper/delegation layer

Existing package retained:

- `src/python/projectkoios/bootstrap/control_surface/adr/`

Planned changes:

- `storage.py` becomes ADR-facing wrapper/delegation layer over the generic storage protocol.
- `pilot.py` uses the ADR wrapper, not SQLite directly.
- `manifest.py`, `markdown.py`, `validation.py`, `equality.py`, and `models.py` remain ADR-specific.
- ADR code may consume generic document-store metadata and payload hashes, but the generic package must not import ADR modules.

### Tests

New generic tests:

- `tests/projectkoios/bootstrap/control_surface_storage/`
- likely file: `test__DocumentStore__sqlite_and_memory.py`

Existing ADR pilot tests retained and updated:

- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrStoragePilot__run.py`

## Generic document-store contract

The generic substrate will support only the current pilot needs:

- store one JSON object document;
- get/export one JSON object document by stable document ID;
- list/query document IDs by generic document kind/family;
- compute/store a canonical content hash for the JSON payload;
- persist deterministic created/updated timestamps supplied by caller/test;
- hide SQLite behind a protocol/interface;
- provide a non-SQLite in-memory implementation/test double.

Planned generic record shape:

```python
DocumentRecord(
    document_id: str,
    document_kind: DocumentType,
    payload: JsonObject,
    content_hash: str,
    created_at: str,
    updated_at: str,
)
```

Generic constraints:

- `document_id` is opaque to the generic store.
- `document_kind` is a scoped enum/type boundary, not an untyped string constant. The ADR layer may pass `DocumentType.ADR`, whose serialized value is `adr`; the generic store stores the enum value but does not interpret ADR semantics.
- `payload` is canonical JSON object content.
- `content_hash` is the hash of canonical JSON payload text.
- timestamps are supplied by caller/test for deterministic evidence.
- no ADR fields (`slug`, `status`, `routing`, `owner`, `next_phase`, lifecycle relations, projection paths) appear as generic columns or generic model properties.

Minimal generic query behavior:

- `get(document_id: str) -> DocumentRecord`
- `export(document_id: str) -> JsonObject` or equivalent payload accessor
- `list_by_kind(document_kind: DocumentType) -> tuple[str, ...]`

No generic query by ADR lifecycle status or routing fields.

## Enumerated semantic values and constants policy

Enumerated semantic values in this slice must be represented by scoped enum/type definitions or schema enums. Do not introduce dangling module-level semantic constants such as `DOCUMENT_KIND_ADR = "adr"`.

Planned enum/type surfaces:

| Concept | Representation | Owner/scope | Notes |
|---|---|---|---|
| Document kind/family | `DocumentType(StrEnum)` or equivalent scoped type in `documents.models` | Generic document-store boundary | Includes `ADR = "adr"` for the current pilot; callers pass enum members, not free strings. |
| Backend kind, if represented | `DocumentStoreBackend(StrEnum)` or local call-site value if not reused | Generic substrate or immediate pilot evidence generation | Only add if evidence/config needs it; otherwise avoid a reusable concept. |
| Source-of-truth mode, if represented | `SourceOfTruthMode(StrEnum)` or schema enum in manifest/evidence model | ADR/pilot evidence layer, not generic substrate | Values remain out of generic store. |
| Artifact disposition | `ArtifactDisposition(StrEnum)` or schema enum in migration evidence builder | Pilot evidence layer | Used for replaced/retained/deleted/generated-local classifications. |
| Replacement action | `ReplacementAction(StrEnum)` or schema enum in migration evidence builder | Pilot evidence layer | Used for replace/retain/delete/move/report-only evidence. |

Reusable semantic values must live on their enum/type. Values that are not reusable domain concepts should remain local to the immediate call site instead of becoming module-level constants.

## SQLite table and payload shape

Replace the ADR-specific `adr_records` table with a generic table.

Proposed generic table name:

- `json_documents`

Proposed DDL:

```sql
CREATE TABLE IF NOT EXISTS json_documents (
  document_id TEXT PRIMARY KEY,
  document_kind TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
)
```

Proposed generic indexes:

```sql
CREATE INDEX IF NOT EXISTS idx_json_documents_kind
ON json_documents (document_kind, document_id)
```

Intent:

- `payload_json` stores deterministic canonical JSON text.
- `document_kind` stores the serialized value of the `DocumentType` enum/type.
- SQLite has no ADR-specific columns.
- SQLite-specific DDL lives only in `storage/sqlite.py`.
- mutable SQLite database path remains generated/local under the pilot directory during test/pilot run and is removed after evidence capture.

## ADR-specific query column decision

Current ADR-specific columns in `adr_records`:

- `slug`
- `title`
- `status`
- `routing_owner`
- `routing_next_phase`
- `schema_id`

Plan decision:

- Remove these from the generic SQLite table.
- Retain the old `adr_records` table/columns only as historical migration evidence in a migration evidence artifact and database evidence narrative.
- Do not introduce an ADR-specific index/projection table in this slice unless approval explicitly adds that scope.
- Replace `list_by_status('draft')` evidence with generic `list_by_kind(DocumentType.ADR)` evidence plus ADR-layer validation/projection evidence.

Pause trigger:

- If approval requires ADR-specific querying by status/routing/title in this slice, VULCAN should pause and propose a separate ADR-specific index/projection table outside the generic substrate.

## ADR wrapper/delegation behavior

Planned ADR-facing storage wrapper:

- `AdrStorageAdapter` remains or is renamed to clarify it delegates to `DocumentStore`.
- ADR wrapper constructs `DocumentRecord(document_id=record["id"], document_kind=DocumentType.ADR, payload=record, ...)`.
- ADR wrapper validates/assumes ADR payload shape only in ADR package.
- ADR wrapper may expose ADR-friendly `store(record)`, `get(record_id)`, `export(record_id)`.
- ADR wrapper should not expose `list_by_status` unless implemented by scanning exported ADR payloads in the ADR layer and clearly not as a generic database column. Preferred for this slice: remove/replace `list_by_status` usage with `list_by_kind` evidence.

## Intentional replacement behavior

### Code/package/adapter names

| Prior surface | Replacement | Treatment |
|---|---|---|
| `projectkoios.bootstrap.control_surface.adr.storage.SqliteAdrStorageAdapter` | `projectkoios.bootstrap.control_surface.storage.sqlite.SqliteDocumentStore` plus ADR wrapper in `adr.storage` | Replace in code; cite old name in migration evidence. |
| `projectkoios.bootstrap.control_surface.adr.storage.MemoryAdrStorageAdapter` | `projectkoios.bootstrap.control_surface.storage.store.MemoryDocumentStore` plus ADR wrapper/test double | Replace in tests; cite old name in migration evidence. |
| `AdrStorageAdapter` protocol as SQLite-hiding boundary | ADR wrapper protocol delegating to generic `DocumentStore` | Retain ADR-facing API only if useful; generic contract lives outside ADR package. |
| `CREATE_TABLE_SQL` in ADR package | generic DDL in document-store SQLite module | Move out of ADR package; old DDL retained in evidence only. |

### SQLite table names

| Prior table | Replacement | Treatment |
|---|---|---|
| `adr_records` | `json_documents` | Replace; old table/columns cited in migration evidence and database evidence. |

### Pilot evidence files

Current pilot directory remains:

- `dev/adr-json-database-one-adr-pilot/`

Planned artifact treatment:

| Artifact | Plan |
|---|---|
| `manifest.json` | Replace/regenerate; add generic document-store package/table/adapter metadata and migration evidence references. |
| `mapping.json` | Replace/regenerate while preserving prior mapping provenance: source `.draft.md` path/hash, old pilot identity, copied/normalized/inferred fields, prior JSON hash. |
| `database-evidence.md` | Replace/regenerate; show generic `json_documents` DDL, `list_by_kind(DocumentType.ADR)` result, no ADR-specific columns, and old `adr_records` replacement note. |
| `adr.json-database-for-adr-storage.json` | Regenerate if payload/hash changes; otherwise retain path and record hash in migration evidence. |
| `adr.json-database-for-adr-storage.projected.md` | Regenerate from ADR layer if manifest/projection metadata changes. |
| generated/local `pilot.sqlite` | Generated and removed; must not be committed. |

No source file under `docs/adr/*.md` will be modified.

## Migration/migration evidence artifact

Add a new pilot-local evidence artifact:

- `dev/adr-json-database-one-adr-pilot/document-store-migration-evidence.json`

Proposed shape:

```json
{
  "status": "pilot-derived-non-authoritative",
  "source_brief": "docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md",
  "old_surfaces": {
    "package": "projectkoios.bootstrap.control_surface.adr.storage",
    "sqlite_adapter": "SqliteAdrStorageAdapter",
    "memory_adapter": "MemoryAdrStorageAdapter",
    "table": "adr_records",
    "query_columns": ["slug", "title", "status", "routing_owner", "routing_next_phase", "schema_id"],
    "json_checkpoint_path": "dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json",
    "json_checkpoint_hash": "<prior hash from mapping/manifest>",
    "source_path": "docs/adr/adr.json-database-for-adr-storage.draft.md",
    "source_hash": "<prior source hash>",
    "old_pilot_identity": {
      "id": "adr.json-database-for-adr-storage",
      "slug": "json-database-for-adr-storage"
    }
  },
  "new_surfaces": {
    "documents_package": "projectkoios.bootstrap.control_surface.documents",
    "sqlite_store": "SqliteDocumentStore",
    "memory_store": "MemoryDocumentStore",
    "table": "json_documents",
    "generic_columns": ["document_id", "document_kind", "content_hash", "payload_json", "created_at", "updated_at"],
    "adr_wrapper_package": "projectkoios.bootstrap.control_surface.adr.storage",
    "document_kind_enum": "DocumentType.ADR",
    "document_kind_value": "adr",
    "json_checkpoint_hash": "<new hash>"
  },
  "field_treatment": {
    "copied_fields": [],
    "normalized_fields": {},
    "inferred_fields": {},
    "new_fields": [],
    "retained_outside_schema": {}
  },
  "provenance_preserved": {
    "mapping_json_prior_fields_retained": true,
    "source_draft_path_hash_retained": true,
    "old_pilot_identity_retained_as_evidence": true
  },
  "commit_safety": {
    "docs_adr_modified": false,
    "committed_sqlite_or_db_files": false
  }
}
```

The exact arrays/values will be populated during implementation from current and regenerated artifacts.

## Validation and tests

Planned test updates/additions:

1. Generic document-store tests:
   - SQLite store creates `json_documents`, stores canonical payload, returns by `document_id`.
   - `list_by_kind(DocumentType.ADR)` returns deterministic IDs and public examples avoid untyped dangling constants.
   - content hash equals canonical JSON payload hash.
   - in-memory store has matching behavior.
   - generic package/table has no ADR-specific columns or imports.
   - semantic value sets introduced by the slice are enum/type-owned or schema-owned, not dangling module-level constants.

2. ADR wrapper tests:
   - ADR wrapper stores/exports existing ADR record through generic SQLite store.
   - ADR behavior also works with in-memory document store/test double.
   - ADR schema validation and projection remain outside the generic package.

3. Pilot evidence tests:
   - `manifest.json`, `mapping.json`, `database-evidence.md`, JSON checkpoint, projection, and migration evidence are generated under `dev/adr-json-database-one-adr-pilot/`.
   - prior `mapping.json` provenance is preserved: source `.draft.md` path/hash, old pilot identity, copied/normalized/inferred fields, JSON hash history where applicable.
   - no source `docs/adr/*.md` file is modified by pilot run.
   - no mutable `.sqlite`/`.db` file remains under `dev/adr-json-database-one-adr-pilot/`.

Planned validation commands:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/schema -q
uv run mypy src/python/projectkoios/bootstrap/control_surface/documents src/python/projectkoios/bootstrap/control_surface/storage src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/control_surface_adr
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/documents src/python/projectkoios/bootstrap/control_surface/storage src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/control_surface_adr
git diff --check
find dev/adr-json-database-one-adr-pilot -type f \( -name '*.sqlite' -o -name '*.db' \) -print
```

Expected final `find` output: no output.

## File-level implementation sequence after approval

1. Create `documents` and `storage` packages: document models/hash behavior in `documents`, protocol/memory/SQLite storage in `storage`.
2. Refactor `adr.storage` into an ADR wrapper over the generic store.
3. Update `adr.pilot` to construct `SqliteDocumentStore` and ADR wrapper; replace status query evidence with kind query evidence.
4. Update manifest/database evidence generation to record generic document-store metadata and old surface replacement.
5. Add `document-store-migration-evidence.json` generation.
6. Add generic document-store tests and update ADR pilot tests.
7. Regenerate pilot evidence artifacts.
8. Run validation commands.
9. Update implementation report, workspace state/active files, and AAR if implementation proceeds.

## Pause triggers / blockers

VULCAN should not code until this plan is approved.

Pause during implementation if any of these arise:

- approval changes the generic table shape or document-store contract;
- implementation would require dangling module-level semantic constants instead of scoped enum/type or schema-owned values;
- ADR-specific query by `status`, `routing`, `title`, or `slug` is required in the same slice;
- any requirement appears to alter ADR naming/lifecycle policy rather than preserve metadata;
- generated evidence would require modifying `docs/adr/*.md` source files;
- mutable `.sqlite`/`.db` files would need to be committed;
- pilot evidence paths need to move outside `dev/adr-json-database-one-adr-pilot/`;
- broader repository-level config, bulk ADR migration, or database-authority promotion is requested.

## Approval question

Approve this plan to proceed with implementation, or revise the requested package paths, generic document-store contract, SQLite table shape, ADR-specific query handling, or migration evidence format before VULCAN codes.
