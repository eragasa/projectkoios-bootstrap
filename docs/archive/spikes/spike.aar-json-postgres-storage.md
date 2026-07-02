# Spike: AAR JSON Storage Contract with PostgreSQL Upgrade Path

## Problem

How should AARs be stored as structured JSON/AST documents locally so the same
storage contract can later move to PostgreSQL without rewriting the AAR model or
business logic?

## Summary

This spike is split into two planning planes:

| Athena architecture planning | Vulcan implementation planning |
|---|---|
| define the canonical AAR shape | build the local JSON storage backend |
| choose the storage contract | define the adapter interface |
| decide what metadata is authoritative | implement query/list/update operations |
| define migration rules to PostgreSQL | add tests for backend parity |
| decide whether the register is doc-first or DB-first | prepare the upgrade path |

## Athena architecture planning

These are the questions that change the architecture:

- what is the canonical AAR schema: Markdown AST, JSON AST, or both?
- which fields are required vs optional?
- is JSON the source of truth, or just a transport/index format?
- should local storage be filesystem-backed JSON files or a small embedded DB?
- what makes the storage contract PostgreSQL-ready later?
- which metadata is authoritative for lookup and promotion?
- what validation proves the storage contract is stable enough for implementation?

### Canonical AAR shape

A likely structured AAR should include:

- `id`
- `timestamp`
- `scope`
- `what_happened`
- `process_issues`
- `proposed_follow_up_improvements`
- `candidate_adr_or_implementation_topics`
- `current_status`
- provenance / operator fields when needed
- links to related artifacts

## Vulcan implementation planning

These are the concrete build candidates:

- a local JSON file store for AAR records
- a storage interface with `put`, `get`, `list`, `query`, `update`, `delete`, and `migrate`
- a repository layout for durable AAR documents
- validation for schema shape and required fields
- a PostgreSQL adapter that can slot in later with the same interface
- parity tests between local JSON and PostgreSQL backends
- migration tooling to move existing AARs without changing content shape

### Implementation mechanics

1. **AST/JSON document model** — keep AAR content structured and machine-readable.
2. **Storage interface** — code against an abstract backend, not directly against
   files or SQL.
3. **Local-first backend** — start with JSON files on disk so the repo remains
   transparent and diffable.
4. **PostgreSQL adapter boundary** — define the same contract in a way that a
   DB backend can replace the local store later.
5. **Validation** — ensure parity in reads, writes, and query behavior across
   backends.

## What to test

- can the AAR model round-trip through JSON without losing meaning?
- can local file storage satisfy current repo needs?
- can the same interface support PostgreSQL later?
- do query and list operations behave the same across backends?
- can migration happen without changing the AAR schema?

## Objections / risks

- JSON may drift into ad hoc structure if the schema is not enforced
- PostgreSQL may become accidental authority if the migration rules are vague
- a DB-first design may be too heavy for bootstrap usage
- file-based storage may be too limiting if query needs grow

## Out of scope

- changing the meaning of AARs
- replacing ADR storage
- building a generic document database platform
- coupling AARs to the GraphRAG spike

## Handoff notes

### Athena

Athena should decide:

- canonical AAR schema
- whether JSON is source of truth or transport
- local storage shape
- authoritative metadata
- migration rules to PostgreSQL
- validation criteria

### Vulcan

If this is promoted, Vulcan will need:

- the final schema
- the storage interface
- file layout conventions
- PostgreSQL adapter contract
- migration and parity tests

## Promotion target

If the spike stabilizes, promote it to an ADR about structured AAR storage with
local JSON first and PostgreSQL as the upgrade path.
