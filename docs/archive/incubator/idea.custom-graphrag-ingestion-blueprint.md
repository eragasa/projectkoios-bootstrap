# Idea: Custom GraphRAG Ingestion Blueprint

## Brainstorm

How should we ingest noisy meta-harness execution logs, ADRs, and AARs into a
GraphRAG-style system so they become durable, queryable knowledge without
hallucinated structure?

## Goal

Create an ingestion-first architecture for scientific-workflow and meta-harness
execution analytics that can later support ADR review, AAR review, and root-
cause analysis.

## Current thinking

The best first boundary is ingestion. The pipeline likely needs:

- deterministic parsing for explicit fields like IDs, timestamps, exit codes,
  file paths, and workflow steps
- heuristic extraction for human-written observations and latent relations
- dual storage for vector similarity and graph topology
- a bounded ontology so the graph does not invent new entity classes on the fly
- k-hop structural retrieval after vector seeding
- flattened synthesis into prompts for local or cloud LLM use

A likely minimum ontology is:

- Workflow Step (`WS`)
- Harness Event (`HE`)
- Failure Mode (`FM`)
- Mitigation (`MI`)

## Spike requirements

- one bounded ingestion question
- one clear promotion target
- one explicit source surface set
- one retrieval boundary
- one validation method

## Ideas considered

- regex/AST-first extraction with LLM only for prose
- hybrid vector + graph storage
- k-hop neighborhood retrieval
- prompt-time context flattening
- direct LLM-only extraction (rejected as too weak for scale and precision)

## Objections / risks

- hallucinated edges if the ontology is too loose
- drift if every new note type becomes a new entity type
- overreach if the system tries to solve retrieval before ingestion is stable
- cost creep if LLM extraction is used for structured fields

## Open questions

- Which source surfaces are in scope first: ADRs, AARs, workflow logs, or all three?
- Should the graph be authoritative or only a derived index?
- Should the ontology stay fixed at four entity types initially?
- What is the minimum useful retrieval depth: 1-hop, 2-hop, or adaptive?
- What validation would prove the ingestion boundary is correct?

## Comments

### ATHENA

| Idea | Action |
|---|---|
| Use ingestion as the first architectural boundary. | Keep; ingestion is the right control plane for the first decision. |
| Keep the ontology tight. | Keep; fixed entity classes reduce drift. |

### VULCAN

| Idea | Action |
|---|---|
| Deterministic parsing should handle all explicit structure. | Keep; do not spend tokens on parseable data. |
| Add a retrieval validation signal. | Keep; the ingest layer needs an observable success criterion. |

### KOIOS

| Idea | Action |
|---|---|
| The note should stay incubator-first, not architecture-final. | Keep; promote only after the ingestion boundary is crisp. |

### HERMES

| Idea | Action |
|---|---|
| The repo should not absorb the full GraphRAG system until the ingestion contract is stable. | Keep; bound the first slice tightly. |

## Preferred direction

Treat this as an ingestion-boundary incubator note that can promote into an ADR
only after the source surfaces, ontology, and retrieval contract are stable.

## Anything to keep out

- broad platform design
- UI or productization work
- multi-repo expansion
- fully generic knowledge-graph framework ambitions

## Resolved questions

- Ingestion is the right first control plane.
- The note should stay incubator-level until the boundary is narrower.

## Resolved comments

- [ATHENA] Use ingestion as the first architectural boundary. → Kept.
- [VULCAN] Deterministic parsing should handle all explicit structure. → Kept.
- [KOIOS] The note should stay incubator-first, not architecture-final. → Kept.
- [HERMES] The repo should not absorb the full GraphRAG system until the ingestion contract is stable. → Kept.

## Promotion target

Promoted to spike:
`docs/spikes/spike.custom-graphrag-ingestion-blueprint.md`

If this stabilizes, it can later promote to an ADR about ingestion-first
GraphRAG analysis for ADR/AAR and workflow telemetry.
