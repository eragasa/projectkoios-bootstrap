# Implementation Plan: JSON Document Database + Ingestor

## Source

- Spike: `spike/20260702/json-database-and-ingestor/spike.md`
- ADR: `docs/architecture/adr/adr.json-database-for-adr-storage.draft.md`
- Owner: VULCAN
- Status: draft
- Date: 2026-07-02

## Scope

Implement the JSON document database and ingestor as described by the spike:

- Document model with typed payload and metadata
- JSON filesystem storage backend
- ADR and AAR ingesters
- CLI tool for document operations
- SQLite index backend (optional)
- Directory watcher daemon

## Repository target

- Primary target: `src/python/projectkoios/bootstrap/storage/` and `src/python/projectkoios/bootstrap/ingesters/`
- CLI verb: `src/python/projectkoios/bootstrap/commands/document.py`
- Tests: `tests/`

## Implementation phases

### Phase P1 — Document model + DocumentType enum

**Files:**
- `src/python/projectkoios/bootstrap/storage/__init__.py` — package init, re-exports
- `src/python/projectkoios/bootstrap/storage/document.py` — Document dataclass, DocumentType enum

**What:**
- Define `DocumentType(Enum)` with `ADR`, `AAR`, `GENERIC`
- Define `Document` frozen dataclass: `id`, `doc_type`, `status`, `title`, `created_at`, `updated_at`, `body` (dict), `metadata` (dict)
- Define `DocumentStatus(Enum)` with `draft`, `active`, `archived`, `superseded`
- Validation: required fields, type constraints on status transitions

**Verification:** unit test creates Document instances, validates field constraints, tests enum membership.

---

### Phase P2 — JsonStore backend

**Files:**
- `src/python/projectkoios/bootstrap/storage/store.py` — abstract `DocumentStore` protocol
- `src/python/projectkoios/bootstrap/storage/json_store.py` — `JsonStore` implementation

**What:**
- `DocumentStore` protocol: `put(doc)`, `get(id) -> Document`, `list() -> list[Document]`, `query(filter) -> list[Document]`, `delete(id)`
- `JsonStore`: stores one JSON file per document under `<base_path>/<doc_type>/<id>.json`
- List walks directory; query does in-memory filter on loaded docs
- Directory creation on first put
- Concurrent-write safety via atomic rename

**Verification:** round-trip put/get, list returns correct count, query by type, delete removes file.

---

### Phase P3 — CLI tool scaffold

**Files:**
- `src/python/projectkoios/bootstrap/commands/document.py` — `register(subparsers)`

**What:**
- `projectkoios document ingest <path>` — ingest a single file
- `projectkoios document list [--type <type>]` — list documents
- `projectkoios document get <id>` — get by id
- `projectkoios document query <key>=<value>` — simple key-value query
- Register verb in `cli.py`

**Verification:** each command prints expected JSON or error.

---

### Phase P4 — ADR ingester

**Files:**
- `src/python/projectkoios/bootstrap/ingesters/__init__.py`
- `src/python/projectkoios/bootstrap/ingesters/adr_ingester.py`

**What:**
- Parse ADR markdown: extract frontmatter (Status, Context, Decision, Consequences) and header fields (Origin, From, Acting-As, Scope, Repository)
- Map to Document fields (id from filename, status from Status header, body contains rendered sections)
- Store via JsonStore
- Register in `document ingest` dispatcher

**Verification:** ingest a known ADR, get it back with correct fields.

---

### Phase P5 — AAR ingester

**Files:**
- `src/python/projectkoios/bootstrap/ingesters/aar_ingester.py`

**What:**
- Parse AAR markdown: extract scope, what_happened, process_issues, follow_up, candidate_adr_topics, current_status
- Map to Document fields
- Store via JsonStore
- Register in `document ingest` dispatcher

**Verification:** ingest known AAR, get it back with correct fields.

---

### Phase P6 — SQLite index backend (optional)

**Files:**
- `src/python/projectkoios/bootstrap/storage/sqlite_index.py`
- `src/python/projectkoios/bootstrap/storage/migration.py`

**What:**
- SQLite schema with document metadata fields
- Sync index from JSON store on init
- `query(filter)` backed by SQL instead of in-memory
- Schema versioning in `migration.py`
- Schema migration on version mismatch

**Verification:** same query returns same results as JsonStore query.

---

### Phase P7 — Directory watcher daemon

**Files:**
- `src/python/projectkoios/bootstrap/ingesters/watcher.py`

**What:**
- Poll-based directory watcher (stdlib only, no watchdog dependency)
- On new or changed file: detect type, ingest via ingester pipeline
- Debounce and coalesce for rapid changes
- CLI: `projectkoios document watch <path> [--interval <sec>]`

**Verification:** drop an ADR markdown into watched dir, see it appear in document list.

---

### Phase P8 — Tests

**Files:**
- `tests/test_storage_document.py`
- `tests/test_storage_json_store.py`
- `tests/test_ingesters_adr.py`
- `tests/test_ingesters_aar.py`
- `tests/test_ingesters_watcher.py`
- `tests/test_cli_document.py`

**What:**
- Unit tests per phase
- Round-trip tests (file to document to file)
- CLI integration tests via subprocess runner
- Temp directory fixtures for isolation

**Verification:** `pytest tests/` passes.

## Code layout

```
src/python/projectkoios/bootstrap/
├── storage/
│   ├── __init__.py
│   ├── document.py
│   ├── store.py
│   ├── json_store.py
│   ├── sqlite_index.py    (P6)
│   └── migration.py       (P6)
├── ingesters/
│   ├── __init__.py
│   ├── adr_ingester.py
│   ├── aar_ingester.py
│   └── watcher.py         (P7)
├── commands/
│   ├── ...
│   └── document.py        (P3)

tests/
├── test_storage_document.py
├── test_storage_json_store.py
├── test_ingesters_adr.py
├── test_ingesters_aar.py
├── test_ingesters_watcher.py
└── test_cli_document.py
```

## Open questions

- Should the store interface be sync-only or support async?
- Should the daemon watch a single directory or configurable multiple directories?
- Should ingested documents preserve the original markdown as a `body.markdown` field?

## Escalation note

If the abstract store interface conflicts with the existing ADR draft's authority
model, escalate to Athena via Hermes before implementing P2.
