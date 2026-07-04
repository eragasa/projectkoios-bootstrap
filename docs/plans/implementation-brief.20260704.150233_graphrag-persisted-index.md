# Implementation brief 20260704.150233: GraphRAG persisted index execution slice

## Status

Draft VULCAN execution brief.

## Provenance

- Acting-As: VULCAN
- Repository: projectkoios-bootstrap
- Workspace: workspaces/vulcan/
- Derived from: `docs/plans/projectkoios-graphrag-next-slice.md`
- Implementation plan: `docs/plans/implementation-plan.20260704.150233_graphrag-persisted-index.md`

## Authority boundary

This brief translates the existing accepted GraphRAG next-slice brief into a concrete VULCAN execution slice. It does not create new architecture authority. If this brief conflicts with `docs/plans/projectkoios-graphrag-next-slice.md`, the source brief controls.

## Objective

Add deterministic persisted GraphRAG index output that can be built from config and inspected on disk, while preserving existing ADR-only source discovery, config-driven behavior, citation fallback, and Ollama-only backend support.

## Required changes

1. Config must expose a persisted index output path.
2. `GraphIndex` must serialize to deterministic JSON.
3. Serialized sections must include source path, section title, line range, and citation-ready evidence text.
4. Citation data must support optional richer metadata without removing `file:line-line` fallback.
5. App/service code must write the persisted index artifact from config.
6. CLI must expose an index build command.
7. Existing query and answer behavior must remain compatible.

## Suggested JSON contract

The persisted artifact should be reviewable and stable. A minimal acceptable shape is:

```json
{
  "version": 1,
  "root": "/absolute/config/root",
  "documents": [
    {
      "path": "/absolute/path/to/source.md",
      "relative_path": "docs/adr/source.md",
      "sections": [
        {
          "relative_path": "docs/adr/source.md",
          "title": "Context",
          "heading_level": 2,
          "line_start": 10,
          "line_end": 20,
          "citation": "docs/adr/source.md:10-20",
          "evidence": "section text or deterministic excerpt",
          "metadata": {
            "page": null,
            "bibtex_key": null
          }
        }
      ]
    }
  ]
}
```

Final field names may differ if tests document the chosen shape, but the artifact must remain deterministic, citation-ready, and traceable to source line ranges.

## CLI behavior

Add:

```bash
projectkoios koios index build --config projectkoios.ingestion.config --schema projectkoios.ingestion.schema.json
```

Expected behavior:

- loads config
- validates runtime constraints
- resolves ADR-only sources
- builds the index
- writes the configured index artifact
- exits non-zero on validation or write failure
- prints a concise success line with output path and section count

## Test obligations

Tests must prove:

- configured index path is loaded and resolved correctly
- persisted JSON is stable across repeated writes
- CLI/app can build the index from config
- retrieval evidence can be matched to persisted section path/title/line range
- citation fallback remains `relative/path.md:start-end`
- existing answer behavior still passes

## Out of scope

Do not add:

- non-ADR sources
- AAR or workflow-log sources
- embeddings or vector stores
- graph database persistence
- second backend implementation
- UI/productization behavior
- architecture/source-authority changes

## Ready-to-implement condition

Implementation may start after this brief and its paired implementation plan are present in `docs/plans/` and the working tree changes are limited to this GraphRAG slice plus any pre-existing unrelated local changes.
