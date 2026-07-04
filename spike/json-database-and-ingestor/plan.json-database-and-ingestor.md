# Implementation Plan: JSON Document Database + Ingestor

## Source

- Spike: `spike/json-database-and-ingestor/spike.md`
- ADR: `docs/adr/adr.json-database-for-adr-storage.draft.md`
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

## Phases

| Phase | Description | Plan |
|---|---|---|
| P1 | Document model + DocumentType enum | `plan.json-database-and-ingestor.phase-01.md` |
| P2 | JsonStore backend | `plan.json-database-and-ingestor.phase-02.md` |
| P3 | CLI tool scaffold | `plan.json-database-and-ingestor.phase-03.md` |
| P4 | ADR ingester | `plan.json-database-and-ingestor.phase-04.md` |
| P5 | AAR ingester | `plan.json-database-and-ingestor.phase-05.md` |
| P6 | SQLite index backend (optional) | `plan.json-database-and-ingestor.phase-06.md` |
| P7 | Directory watcher daemon | `plan.json-database-and-ingestor.phase-07.md` |
| P8 | Tests | `plan.json-database-and-ingestor.phase-08.md` |

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
