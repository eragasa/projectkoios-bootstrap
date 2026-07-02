# Phase P8 — Tests

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
