# Spike: Custom GraphRAG Ingestion Blueprint

## Problem

How should we ingest noisy meta-harness execution logs, ADRs, and AARs into a
GraphRAG-style system so they become durable, queryable knowledge without
hallucinated structure?

## Summary

This spike is best split into two planning planes:

| Athena architecture planning | Vulcan implementation planning |
|---|---|
| define the ingestion boundary | build the parsing/extraction pipeline |
| choose the source surfaces | implement storage sync |
| fix the ontology and edge rules | implement retrieval and synthesis |
| define validation criteria | write tests and operational checks |
| decide whether the graph is authoritative or derived | choose concrete DB/runtime components |

## Athena architecture planning

These are the questions that change the architecture:

- which source surfaces are in scope first: ADRs, AARs, workflow logs, or all three?
- should the graph be authoritative or only a derived index?
- should the ontology stay fixed at four entity types initially?
- which causal edge types are allowed?
- what is the minimum useful retrieval depth: 1-hop, 2-hop, or adaptive?
- what validation proves the ingestion boundary is correct?
- what is the promotion target once the boundary stabilizes?

### Working ontology

Use a tight ontology with only four entity types for the first pass:

- Workflow Step (`WS`)
- Harness Event (`HE`)
- Failure Mode (`FM`)
- Mitigation (`MI`)

### Explicit edges

Use only explicit causal edges:

- `DEPENDS_ON` — Workflow Step → Workflow Step
- `TRIGGERED` — Harness Event → Failure Mode
- `RESOLVED` — Mitigation → Failure Mode
- `VIOLATED` — Failure Mode → Workflow Step

## Vulcan implementation planning

These are the concrete build candidates:

- deterministic parsing for IDs, timestamps, exit codes, file paths, and step IDs
- heuristic extraction for prose and latent relations
- vector + graph dual storage
- k-hop neighborhood retrieval after vector seeding
- flattened context synthesis into prompt-ready prose
- source-surface allowlist and exclusions
- reference-codebase experiments
- validation tests for extraction and retrieval

### Core engine mechanics

1. **Hybrid extraction** — parse structured fields first; use the LLM only for
   unstructured prose and human reasoning.
2. **Dual vector-graph storage** — keep semantic summaries and graph topology
   synchronized by tracking identifier.
3. **K-hop retrieval** — use vector search only to seed; then stop vector search
   and expand topology by one or two hops.
4. **Synthesis prompt engineering** — serialize the subgraph into flattened,
   explicit prose before prompting the local or cloud model.

### Reference codebases to study

- **hkuds/LightRAG** — local vs global retrieval flow
- **microsoft/GraphRAG** — extractor prompts and structure enforcement
- **Intel Labs fastrag** — high-throughput sparse/dense retrieval integration

## What to test

- can the pipeline extract explicit structure deterministically?
- can human notes be converted into useful relations without inventing extra
  entity classes?
- can vector search seed the right graph neighborhood?
- can the flattened context stay readable and decision-useful?
- can the graph stay bounded to four entity types and the four explicit edge
  types above?

## Objections / risks

- hallucinated edges if the ontology is too loose
- cost creep if LLMs parse fields that regex/AST can already handle
- overreach if retrieval is designed before ingestion is stable
- drift if every new note type becomes a new entity type

## Out of scope

- broad platform design
- UI/productization work
- multi-repo expansion
- generic knowledge-graph framework ambitions

## Handoff notes

### Athena

Athena should decide:

- source-surface scope
- graph authority model
- ontology stability
- allowed edge types
- retrieval depth
- validation criteria
- promotion target

### Vulcan

If this is promoted, Vulcan will need:

- explicit parsing rules or regex/AST helpers
- the four-entity ontology and four edge types
- a retrieval validation signal
- a flattened context serialization format
- a source-surface allowlist
- concrete DB/runtime choices

## Promotion target

If the spike stabilizes, promote it to an ADR about ingestion-first GraphRAG
analysis for ADR/AAR and workflow telemetry.
