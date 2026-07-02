# Phase P3 — CLI tool scaffold

**Files:**
- `src/python/projectkoios/bootstrap/commands/document.py` — `register(subparsers)`

**What:**
- `projectkoios document ingest <path>` — ingest a single file
- `projectkoios document list [--type <type>]` — list documents
- `projectkoios document get <id>` — get by id
- `projectkoios document query <key>=<value>` — simple key-value query
- Register verb in `cli.py`

**Verification:** each command prints expected JSON or error.
