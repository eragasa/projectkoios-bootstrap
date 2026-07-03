# GraphRAG consolidated implementation brief

## Objective
The implementation **MUST** deliver a small, config-driven GraphRAG system for ADRs only, with explicit validation, pluggable model backends, and traceable cited answers.

## Canonical config
The system **MUST** use `projectkoios.ingestion.config` as the canonical configuration file.
The configuration **MUST** be authored in YAML.

## First slice
The first slice **MUST**:
- ingest ADRs only
- build a derived graph index
- default to 1-hop retrieval
- support prompt-selected answer formats
- emit citations with fallbacks
- require only one working backend adapter

## Configuration rules
The configuration **MUST** define:
- source scope
- ontology
- extraction settings
- retrieval settings
- evaluation settings
- backend selection
- validation mode

Overlays **MUST** use explicit replacement for any section they change.
Implicit deep merge **MUST NOT** be used.

## Validation
Validation **MUST** occur in two layers:
1. JSON Schema for static structure
2. runtime checks for paths, globs, presets, and references

Validation mode **MUST** default to strict fail-fast and **MAY** be relaxed by flag.

## Sources
The first slice **MUST** support ADRs only.
Other document families **MUST NOT** be required for v1.

## Retrieval and answers
Retrieval depth **MUST** be configurable.
The system **MUST** surface the relevant section or evidence, not just the file.
The answer format **MUST** be selectable by prompt.
Supported formats **MUST** include cited summary and structured JSON.

## Citations
The system **MUST** support citation fallbacks.
BibTeX and page numbers **MAY** be emitted when available.
file:line **MUST** be supported as the universal fallback.

## Backends
The backend layer **MUST** be pluggable.
The architecture **MUST** allow Ollama, OpenRouter, and Hugging Face adapters.
Only one backend **MUST** be implemented in the first slice.

## Acceptance criteria
The implementation **MUST** satisfy all of the following:
- runs can be configured without code edits
- ADR sources are discovered from config only
- malformed config fails before ingest
- retrieval returns traceable evidence
- answers include citations
- backend selection is configuration-driven

## Out of scope
The first slice **MUST NOT** include:
- AARs
- workflow logs
- deep-merge inheritance
- multiple backend implementations
- source authority changes
- UI/productization work
