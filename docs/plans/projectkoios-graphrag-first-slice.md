# Project Koios GraphRAG first slice plan

## Source
- `workspaces/athena/outbox/20260703_graphrag_consolidated_implementation_brief.md`
- `workspaces/athena/inbox/20260703_graphrag_config_schema_rfc.md`
- `workspaces/athena/inbox/20260703_graphrag_implementation_brief.md`

## Scope
Build the smallest config-driven GraphRAG slice for ADRs only.

### Must include
- canonical config file: `projectkoios.ingestion.config`
- YAML authoring format
- JSON Schema validation for config shape
- runtime validation for paths, globs, and references
- ADR-only source discovery
- derived graph index
- 1-hop retrieval by default
- prompt-selected answer format
- citation fallbacks
- one working model backend adapter

### Must not include
- AARs or workflow docs
- deep-merge inheritance
- multiple backend implementations in v1
- source authority changes
- UI/productization work
- hardcoded corpus assumptions

## Verification method
- config loads without code edits
- invalid config fails before ingest
- ADR sources resolve from config only
- retrieval returns traceable evidence
- answers include citations with fallback behavior
- backend selection is configuration-driven

## Task breakdown
1. define config schema
2. implement config loader and preset resolver
3. validate config shape with JSON Schema
4. validate runtime paths and references
5. ingest ADR markdown deterministically
6. build derived graph index
7. implement 1-hop retrieval
8. emit cited summary and structured JSON outputs
9. wire one model backend adapter behind an interface

## Escalation note
If the first adapter or retrieval assumptions prove too vague, escalate the gap back to Athena before widening the slice.
