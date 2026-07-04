# Implementation report 20260704.151640: GraphRAG persisted index

## Status

Implemented and locally validated.

## Provenance

- Acting-As: VULCAN
- Repository: projectkoios-bootstrap
- Workspace: `workspaces/vulcan/`
- Controlling source artifact: `docs/plans/projectkoios-graphrag-next-slice.md`
- Implementation plan: `docs/plans/implementation-plan.20260704.150233_graphrag-persisted-index.md`
- Execution brief: `docs/plans/implementation-brief.20260704.150233_graphrag-persisted-index.md`

## Scope implemented

Added deterministic persisted GraphRAG index output while preserving ADR-only source discovery, config-driven behavior, current in-memory retrieval/answer behavior, citation fallback, and Ollama as the only configured backend.

## Changed files

- `projectkoios.ingestion.config`
  - Added `pipeline.index_path: graph/index.json`.
- `projectkoios.ingestion.schema.json`
  - Added required `pipeline.index_path` schema field.
- `src/python/projectkoios/ingestors/config.py`
  - Added `Config.index_path` with relative-path resolution from config root.
  - Added runtime validation for non-empty `pipeline.index_path`.
- `src/python/projectkoios/ingestors/index.py`
  - Added `Section.citation` and optional `page` / `bibtex_key` citation metadata fields.
  - Added `GraphIndexJsonSerializer` for deterministic JSON serialization and writes.
- `src/python/projectkoios/ingestors/retrieval.py`
  - Added optional citation metadata to `Evidence`.
  - Preserved `relative/path.md:start-end` fallback behavior.
- `src/python/projectkoios/ingestors/app.py`
  - Added `PersistedIndexReport` and `App.persist_index(...)`.
- `src/python/projectkoios/cli/koios.py`
  - Added `projectkoios koios index build` command.
- `src/python/projectkoios/ingestors/__init__.py`
  - Exported persisted-index report and serializer types.
- `tests/projectkoios/ingestors/_helpers.py`
  - Updated test config/schema helpers for `pipeline.index_path`.
- `tests/projectkoios/ingestors/test__App__answer.py`
  - Added app-level persisted-index write coverage.
- `tests/projectkoios/ingestors/test__JsonSchemaValidator__validate.py`
  - Updated schema validation fixture.
- `tests/projectkoios/ingestors/test__KoiosConfigLoader__load.py`
  - Added config path resolution assertion.
- `tests/projectkoios/ingestors/test__KoiosGraphIndexBuilder__build.py`
  - Added deterministic serializer and stable write tests.
- `tests/projectkoios/ingestors/test__KoiosRetriever__retrieve.py`
  - Added retrieval-to-persisted-index traceability test.
- `tests/projectkoios/ingestors/test__KoiosCli__index.py`
  - Added CLI index build test.
- `graph/index.json`
  - Generated persisted index artifact from the repository config.

## Persisted index behavior

The persisted artifact is written to the configured `pipeline.index_path`. For the repository config, the generated artifact is:

- `graph/index.json`

The artifact includes deterministic JSON with source/document paths, section titles, heading levels, line ranges, citations, evidence text, and optional citation metadata fields.

## Validation evidence

Commands run from repository root:

```bash
.venv/bin/python3 -m pytest tests/projectkoios/ingestors -q
# 19 passed in 0.07s

.venv/bin/python3 -m pytest -q
# 175 passed in 0.84s

.venv/bin/projectkoios koios validate
# koios validate: schema=True runtime=True sources=38

.venv/bin/projectkoios koios validate --schema projectkoios.ingestion.schema.json
# initial implementation validation: koios validate: schema=True runtime=True sources=38
# closeout rebuild after ADR/schema planning docs changed: koios validate: schema=True runtime=True sources=39

.venv/bin/projectkoios koios index build --schema projectkoios.ingestion.schema.json
# initial implementation validation: koios index build: output=/Users/eugene/repos/projectkoios-bootstrap/graph/index.json sources=38 sections=555
# closeout rebuild after ADR/schema planning docs changed: koios index build: output=/Users/eugene/repos/projectkoios-bootstrap/graph/index.json sources=39 sections=573

shasum -a 256 graph/index.json
.venv/bin/projectkoios koios index build --schema projectkoios.ingestion.schema.json >/tmp/koios-index-build-second.out
shasum -a 256 graph/index.json
# initial implementation validation:
# bcab4230d336357f75b5666dff6d1509f04c63ce6c7c2056430dad01731fc69c  graph/index.json
# bcab4230d336357f75b5666dff6d1509f04c63ce6c7c2056430dad01731fc69c  graph/index.json
# closeout rebuild after ADR/schema planning docs changed:
# 7f9ebc0079c28ca1ecb0b2ab4c58eaf7ca93482a9194f6a5e346e3921273a143  graph/index.json
# 7f9ebc0079c28ca1ecb0b2ab4c58eaf7ca93482a9194f6a5e346e3921273a143  graph/index.json
```

Additional note:

```bash
koios validate
# failed in the local shell because the `koios` shim points at a Python environment without this package importable.
# The repository virtualenv command above passed.
```

## Acceptance criteria status

- Persisted index artifact written deterministically: satisfied.
- Repeated runs stable for unchanged inputs: satisfied by matching SHA-256 hashes.
- CLI can build index from config: satisfied.
- Retrieval remains traceable to persisted index evidence: covered by test.
- Citation fallback behavior still works: covered by existing and extended retrieval tests.
- Existing query/answer behavior preserved: full test suite passed.
- Ollama remains the only backend: unchanged.
- ADR-only source discovery preserved: runtime validation and validation command passed.

## Deviations or follow-up

- Retrieval still builds from the in-memory derived index and does not reload from `graph/index.json`. This matches the implementation plan's bounded approach and avoids a retrieval redesign.
- Optional page/BibTeX metadata is represented in the data model and serialized as nullable fields, but no source parser populates it yet.
- `koios validate` without the repository virtualenv failed due to local shim environment mismatch, not implementation behavior.
