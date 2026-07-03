# GraphRAG big plan

## Goal
Build a config-driven, scientific-workflow GraphRAG system that can ingest heterogeneous document sources, validate runs explicitly, and produce traceable answers with citations.

## Architecture outline
1. **Config layer**
   - canonical config file: `projectkoios.ingestion.config`
   - YAML authoring format
   - JSON Schema validation
   - runtime validation for paths, globs, and references
   - explicit replacement overlays only

2. **Source layer**
   - base source scope starts with ADRs
   - later presets can expand to AARs, workflow docs, and other corpora
   - source inclusion/exclusion controlled entirely by config

3. **Extraction layer**
   - deterministic extraction for explicit structure
   - semantic extraction via pluggable model backends
   - fixed ontology for the first slice, extensible by config

4. **Graph layer**
   - derived graph index, not source of truth
   - retrieval depth configurable
   - section-level evidence retained for traceability

5. **Citation layer**
   - universal fallback to file:line
   - page and BibTeX when available
   - strongest supported citation emitted per source

6. **Model backend layer**
   - pluggable adapters for Ollama, OpenRouter, and Hugging Face
   - backend selected by config
   - one backend only needs to be implemented in slice 1

7. **Answering layer**
   - prompt selects output style
   - supports cited summary and structured JSON
   - answers must surface the relevant section/evidence

## Design principles
- no hardcoded corpus or persona
- explicit over implicit
- reproducible over convenient
- config-driven over code-driven policy
- scientific auditability over hidden defaults

## Growth path
- v1: ADR-only, 1-hop, derived index, one backend, citations, validation
- v2: add preset overlays for more corpora and retrieval modes
- v3: add broader document families and evaluation harnesses
- v4: add comparative experiments across backends and retrieval settings
