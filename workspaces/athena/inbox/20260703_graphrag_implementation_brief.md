# GraphRAG implementation brief

## Objective
The implementation **MUST** deliver the smallest config-driven GraphRAG slice for ADRs only, with explicit validation, pluggable backends, and cited answers.

## First-slice scope
The system **MUST** support:
- canonical config file: `projectkoios.ingestion.config`
- YAML authoring format
- JSON Schema validation for config shape
- runtime validation for paths, globs, and references
- ADR-only source discovery
- derived graph index only
- 1-hop retrieval as the default
- prompt-selected answer format
- citation fallback support
- one working model backend adapter

## Out of scope
The system **MUST NOT** include:
- AARs or workflow docs
- deep-merge config inheritance
- multiple backend implementations in v1
- source authority changes
- UI/productization work
- hardcoded corpus assumptions

## Required behavior
- The config **MUST** declare source scope, ontology, retrieval, evaluation, and backend choice.
- Invalid config **MUST** fail fast in strict mode.
- Runtime validation **MUST** verify source paths and preset references.
- Retrieval **MUST** return the relevant section/evidence, not just the file.
- Answers **MUST** emit the strongest supported citation available.
- Output formats **MUST** support both cited summary and structured JSON.

## Suggested build surfaces
The implementation **SHOULD** include:
- config loader
- preset resolver
- schema validator
- runtime validator
- ADR ingestor
- graph index builder
- retrieval engine
- answer formatter
- backend interface + one adapter

## Acceptance criteria
- A run **MUST** be configurable without code edits.
- ADR sources **MUST** be discovered from config only.
- Validation **MUST** catch malformed config before ingest.
- Retrieval **MUST** return traceable evidence.
- Answers **MUST** include citations with fallback behavior.
- Backend selection **MUST** be pluggable by configuration.

## Deliverable shape
The implementation **SHOULD** produce:
- implementation notes
- config/schema artifacts
- a minimal working pipeline for ADR-only retrieval and cited answering
