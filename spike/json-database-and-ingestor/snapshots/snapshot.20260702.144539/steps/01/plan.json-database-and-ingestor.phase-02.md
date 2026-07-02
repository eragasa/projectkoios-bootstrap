# Phase P2 — JsonStore backend

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
