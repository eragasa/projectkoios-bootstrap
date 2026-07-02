# Phase P4 — ADR ingester

**Files:**
- `src/python/projectkoios/bootstrap/ingesters/__init__.py`
- `src/python/projectkoios/bootstrap/ingesters/adr_ingester.py`

**What:**
- Parse ADR markdown: extract frontmatter (Status, Context, Decision, Consequences) and header fields (Origin, From, Acting-As, Scope, Repository)
- Map to Document fields (id from filename, status from Status header, body contains rendered sections)
- Store via JsonStore
- Register in `document ingest` dispatcher

**Verification:** ingest a known ADR, get it back with correct fields.
