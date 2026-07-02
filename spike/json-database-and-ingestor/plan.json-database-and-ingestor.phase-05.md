# Phase P5 — AAR ingester

**Files:**
- `src/python/projectkoios/bootstrap/ingesters/aar_ingester.py`

**What:**
- Parse AAR markdown: extract scope, what_happened, process_issues, follow_up, candidate_adr_topics, current_status
- Map to Document fields
- Store via JsonStore
- Register in `document ingest` dispatcher

**Verification:** ingest known AAR, get it back with correct fields.
