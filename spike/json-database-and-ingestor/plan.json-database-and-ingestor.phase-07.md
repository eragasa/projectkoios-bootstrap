# Phase P7 — Directory watcher daemon

**Files:**
- `src/python/projectkoios/bootstrap/ingesters/watcher.py`

**What:**
- Poll-based directory watcher (stdlib only, no watchdog dependency)
- On new or changed file: detect type, ingest via ingester pipeline
- Debounce and coalesce for rapid changes
- CLI: `projectkoios document watch <path> [--interval <sec>]`

**Verification:** drop an ADR markdown into watched dir, see it appear in document list.
