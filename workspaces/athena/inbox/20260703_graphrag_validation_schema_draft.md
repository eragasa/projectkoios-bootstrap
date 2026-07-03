# GraphRAG validation schema draft

## Goal
Validate `projectkoios.ingestion.config` and its presets before any run starts.

## Validation layers

1. **Shape validation**
   - required top-level keys exist
   - field types are correct
   - allowed enum values are enforced

2. **Reference validation**
   - source globs resolve
   - preset names exist
   - ontology IDs are unique
   - edge types are from the allowed set

3. **Scientific-run validation**
   - explicit replacement rules are satisfied
   - no hidden inheritance is used
   - retrieval depth is declared
   - citation format is declared

## Suggested format
Use a machine-readable schema alongside the YAML config.

Options:
- JSON Schema
- YAML-aware schema definition
- lightweight custom validator

## Minimum required checks
- `version` present
- `project` present
- `pipeline.mode` present
- `source.include` present
- `ontology.entities` present
- `ontology.edges` present
- `retrieval.strategy` present
- `evaluation.require_citations` present

## Failure behavior
- fail fast before ingestion
- print the exact invalid field
- do not partially run with fallback defaults

## Recommendation
Use a formal schema plus a small validator so the config is both human-editable and machine-checkable.
