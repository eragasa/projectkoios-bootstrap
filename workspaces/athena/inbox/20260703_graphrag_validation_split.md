# GraphRAG validation split

## Decision
Validate GraphRAG configuration in two layers.

## Layer 1: JSON Schema
Validate static structure only.

Covers:
- required keys
- field types
- enums
- nested object shape

## Layer 2: Runtime validation
Validate filesystem and reference state at run time.

Covers:
- source globs resolve
- preset overlays exist
- referenced files exist
- ontology and edge references are coherent
- declared retrieval and evaluation settings are usable

## Rationale
- schema stays portable and deterministic
- runtime checks reflect the current corpus state
- scientific workflows need both structural and environmental validation

## Consequences
- bad configs fail early
- invalid paths are caught before ingestion
- the same config can be reused across corpora while still being verified per run
