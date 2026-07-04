# Implementation plan 20260704.150233: GraphRAG persisted index

## Status

Draft VULCAN implementation plan.

## Provenance

- Acting-As: VULCAN
- Repository: projectkoios-bootstrap
- Workspace: workspaces/vulcan/
- Controlling source artifact: `docs/plans/projectkoios-graphrag-next-slice.md`
- Supporting policy: `docs/policies/python-coding.md`

## Scope

Implement the next GraphRAG slice by adding deterministic persisted-index output while preserving ADR-only, config-driven behavior and the current Ollama-only backend requirement.

## Non-authority note

This plan is an implementation artifact only. It does not change GraphRAG architecture authority, source authority, ADR lifecycle authority, or backend strategy.

## Files expected to change

- `src/python/projectkoios/ingestors/config.py`
- `src/python/projectkoios/ingestors/index.py`
- `src/python/projectkoios/ingestors/retrieval.py`
- `src/python/projectkoios/ingestors/app.py`
- `src/python/projectkoios/cli/koios.py`
- `src/python/projectkoios/ingestors/__init__.py`
- `tests/projectkoios/ingestors/_helpers.py`
- `tests/projectkoios/ingestors/test__KoiosConfigLoader__load.py`
- `tests/projectkoios/ingestors/test__KoiosGraphIndexBuilder__build.py`
- `tests/projectkoios/ingestors/test__KoiosRetriever__retrieve.py`

A new focused CLI/app persistence test file MAY be added if it keeps tests clearer than expanding existing test files.

## Implementation sequence

1. Add a config-driven persisted index output path.
   - Prefer a small explicit config property on `Config`.
   - Keep path resolution relative to the config file directory unless the value is absolute.
   - Update test schema/config helpers to cover the field.

2. Add deterministic `GraphIndex` serialization.
   - Serialize with stable key ordering and stable collection ordering.
   - Include source path, relative path, section title, heading level, line range, and citation-ready evidence text.
   - Preserve deterministic output across identical runs.

3. Extend citation metadata without breaking fallback.
   - Add optional richer metadata fields only where needed.
   - Preserve current `relative/path.md:start-end` fallback behavior when page or BibTeX metadata is absent.

4. Add an application service method for writing the persisted index.
   - Load and validate config.
   - Resolve ADR-only sources.
   - Build the derived index.
   - Write JSON to the configured output path.
   - Return enough data for CLI success output and tests.

5. Add CLI index build command.
   - Add `projectkoios koios index build --config ... --schema ... --preset ...`.
   - Keep CLI adapter thin over `App`.
   - Print concise success summary including output path and indexed section count.

6. Preserve existing query and answer behavior.
   - Current retrieval may continue to use the in-memory derived index.
   - The persisted artifact must still be traceable to retrieval evidence by matching section path/title/line range.

## Tests to add or update

- Config loader exposes the persisted index path.
- GraphIndex serialization is deterministic.
- Writing the index twice for unchanged inputs produces exact matching JSON text.
- App or CLI writes the index artifact to disk from config.
- Retrieval evidence remains traceable to persisted-index section metadata.
- Citation fallback still uses `file:line-line` when richer metadata is absent.
- Existing answer/query behavior remains unchanged.

## Validation commands

Run from repository root:

```bash
.venv/bin/python3 -m pytest tests/projectkoios/ingestors -q
.venv/bin/python3 -m pytest -q
koios validate
```

## Escalation criteria

Stop and request rebriefing if implementation requires any of the following:

- retrieval redesign beyond traceability to the persisted artifact
- non-ADR source support
- embeddings, vector stores, or graph database persistence
- a second backend provider
- product/UI behavior
- source-authority changes

## Closeout requirements

- Write implementation report under `docs/implementation/`.
- Update `workspaces/vulcan/state.md` and `workspaces/vulcan/active.md`.
- Run relevant validation and record exact results.
- Write an AAR if the session changes files beyond the plan/brief or exposes process lessons.
