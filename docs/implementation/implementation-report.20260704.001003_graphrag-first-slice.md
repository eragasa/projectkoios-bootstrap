---
Kind: implementation-report
From: VULCAN
To: HERMES
Scope: projectkoios-bootstrap
Status: complete
Commit: 6e1d91d
---

# Implementation report: GraphRAG first slice

## Summary

Implemented the first config-driven GraphRAG slice for ADR-only ingestion. The slice provides a committed YAML config, JSON Schema validation, runtime validation, explicit replacement presets, in-memory ADR section indexing, retrieval with file/line citations, cited answer composition, a configurable Ollama backend adapter, and CLI entrypoints.

## Source artifacts

- `workspaces/athena/handoffs/outgoing/20260703_graphrag_consolidated_implementation_brief.md`
- `docs/plans/projectkoios-graphrag-first-slice.md`
- `spike/graphrag-ingestion/spike.md`

## Changed implementation surface

- `projectkoios.ingestion.config` — canonical YAML config.
- `projectkoios.ingestion.schema.json` — committed schema for static config validation.
- `src/python/projectkoios/cli/` — top-level CLI router and `koios` command surface.
- `src/python/projectkoios/ingestors/` — config, schema, source resolution, index, retrieval, answering, backend, and app orchestration modules.
- `tests/projectkoios/ingestors/` — test coverage for config/schema/source/index/retrieval/app behavior.
- `pyproject.toml` — script entrypoint and pytest path configuration.
- `src/python/projectkoios/bootstrap/__main__.py` and `src/python/projectkoios/bootstrap/cli.py` — compatibility forwarding to the new CLI entrypoint.

## Delivered behavior

- Config loads from `projectkoios.ingestion.config` without code edits.
- Schema validation rejects malformed config shape before ingest.
- Runtime validation checks ADR-only v1 source globs, validation mode, pipeline mode, answer format, backend name, backend failure mode, retrieval depth, and backend timeout.
- Presets use explicit top-level section replacement; no implicit deep merge is performed.
- ADR markdown files are discovered from config-defined globs.
- ADR markdown headings are converted into an in-memory derived section index.
- Retrieval returns traceable evidence with file/line citations.
- Answers support cited summary and structured JSON formats.
- Backend selection is config-driven and currently supports one adapter: Ollama.
- Backend failures are explicit by default and may fall back only when config sets `extraction.backend.on_failure: fallback`.

## Validation evidence

Validated with the repository virtualenv interpreter:

```text
/Users/eugene/repos/projectkoios-bootstrap/.venv/bin/python3 -m pytest -q
171 passed

/Users/eugene/repos/projectkoios-bootstrap/.venv/bin/python3 -m projectkoios.bootstrap koios validate --schema projectkoios.ingestion.schema.json --preset adr
koios validate: schema=True runtime=True sources=37
```

## Known limitations / deferred work

- The derived graph index is in memory only; no persisted index file exists yet.
- Retrieval is deterministic keyword scoring over heading sections, not embeddings or a graph database.
- Only ADR sources are supported in v1.
- Only one backend adapter is implemented: Ollama.
- Ontology and extraction sections are validated structurally but not yet used for semantic extraction.
- No query log, cache, vector store, or durable evaluation report is produced.

## Recommended next slice

Add persisted index output:

1. Add an index output path to config.
2. Serialize `GraphIndex` deterministically to JSON.
3. Add `projectkoios koios index`.
4. Test that ADR ingestion produces stable index JSON with paths, section titles, line ranges, and citation-ready evidence.
