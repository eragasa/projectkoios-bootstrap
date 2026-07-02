# Phase P6 — SQLite index backend (optional)

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
