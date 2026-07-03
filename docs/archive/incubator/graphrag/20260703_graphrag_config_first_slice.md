# GraphRAG config-first slice

## Goal
Build the smallest useful GraphRAG prototype as a generic, config-driven pipeline.

## Canonical config
- File: `projectkoios.ingestion.config`
- Format: YAML
- Scope: reusable, not corpus-specific

## v1 slice
- source discovery from config-defined globs
- deterministic extraction for explicit structure
- derived graph index only
- 1-hop retrieval
- cited answer synthesis
- no hardcoded corpus, user persona, or question type

## Config responsibilities
- source roots and include/exclude globs
- document types enabled
- ontology definition
- extraction rules
- retrieval depth
- answer format
- citation format
- evaluation mode
- optional presets layered over defaults

## Minimal pipeline
1. load config
2. discover sources
3. extract entities and relations
4. build derived graph index
5. retrieve evidence
6. synthesize cited answer

## Design constraint
Everything variable stays in config. The code only provides the generic engine.

## Next build step
Draft the config schema and map it to the smallest implementation scaffold.
