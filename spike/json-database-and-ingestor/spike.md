# Spike: JSON Document Database + Ingestor

## Problem

Project Koios needs a local-first JSON document database and ingestor. ADRs,
AARs, and eventually all structured documents need canonical JSON storage with
indexed lookup, validation, and auto-ingestion from markdown sources.

## Summary

| Athena architecture planning | Vulcan implementation planning |
|---|---|
| define the canonical document schema | build the Document model and DocumentType enum |
| choose JSON vs SQLite authority model | implement JsonStore backend |
| define document lifecycle and status rules | implement ADR and AAR ingesters |
| define the ingestor boundary | build CLI tool for document commands |
| define the daemon contract | build directory watcher daemon |

## Scope

- JSON files on disk as the canonical document record
- SQLite as an optional index/cache for fast queries
- CLI tool for on-demand ingestion, listing, retrieval
- Directory watcher daemon for auto-ingestion on file changes
- Pluggable document types: ADR (first), AAR (second), general (later)
- Built on the existing draft ADR `adr.json-database-for-adr-storage.draft.md`
  (which stays draft; findings may promote or revise it)

## Out of scope

- Changing ADR storage authority
- Removing markdown from the workflow
- PostgreSQL adapter (covered by `spike.aar-json-postgres-storage.md`)
- Full-text search (deferred)
- GraphRAG ingestion (separate spike, `spike.custom-graphrag-ingestion-blueprint.md`)
- Remote or network database backends

## Architecture

- **Document**: typed JSON payload with metadata (id, type, status, timestamps)
- **Store interface**: abstract put/get/list/query/delete backed by JSON files
- **Index**: SQLite for fast indexed lookups (cache, not authority)
- **Ingestor**: detects document type from source, parses, validates, stores
- **Daemon**: polls directories, auto-ingests new/changed documents

## What to test

- can a document round-trip through JSON without losing meaning?
- can local file storage satisfy current repo needs?
- can the same store interface support SQLite later?
- do query and list operations behave the same across backends?
- can the ingester parse ADR and AAR markdown correctly?
- can the watcher daemon auto-ingest on file change?

## Objections / risks

- JSON may drift into ad hoc structure if the schema is not enforced
- SQLite may become accidental authority if the cache rule is not explicit
- A daemon adds operational complexity during bootstrap
- Markdown parsing may lose fidelity on complex ADR structures

## Related artifacts

- `docs/adr/adr.json-database-for-adr-storage.draft.md`
- `docs/incubator/idea.json-database-sqlite.md`
- `docs/spikes/spike.aar-json-postgres-storage.md`
- `docs/spikes/spike.custom-graphrag-ingestion-blueprint.md`

## Handoff notes

### Athena

Athena should decide:

- canonical document schema
- whether JSON is source of truth or transport
- local storage shape and authority model
- document lifecycle and status transition rules
- ingestor boundary (what counts as a document source)
- validation criteria for promotion from spike

### Vulcan

Vulcan will build:

- the Document model and DocumentType enum
- the JsonStore backend with abstract store interface
- ADR and AAR ingesters
- CLI tool for document operations
- directory watcher daemon
- tests and round-trip validation

## Promotion target

If this spike stabilizes, promote it to an ADR about general-purpose JSON
document storage with local JSON first and SQLite as the optional index.
The existing `adr.json-database-for-adr-storage.draft.md` should be revised
or superseded based on spike findings.

## Decision log

| Date | Decision |
|---|---|
| 2026-07-02 | Scope: ADR-first, AAR-second, general later |
| 2026-07-02 | JSON canonical, SQLite cache-only |
| 2026-07-02 | CLI + daemon both |
| 2026-07-02 | ADR stays draft; spike informs promotion |
