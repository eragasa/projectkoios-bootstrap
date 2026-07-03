# GraphRAG next-slice implementation brief

## Objective
The implementation **MUST** extend the first GraphRAG slice with a persisted index output and richer citation metadata while preserving the ADR-only, config-driven architecture.

## Source
This brief **MUST** be read together with:
- `docs/implementation/implementation-report.20260704.001003_graphrag-first-slice.md`
- `docs/plans/projectkoios-graphrag-first-slice.md`
- `docs/archive/incubator/graphrag/20260703_graphrag_consolidated_implementation_brief.md`

## Next-slice scope
The next slice **MUST**:
- persist the derived ADR index to a deterministic JSON artifact
- preserve ADR-only source discovery
- preserve config-driven retrieval and answer formatting
- enrich citation metadata beyond file:line where available
- expose a CLI command or subcommand for building the persisted index
- keep the current Ollama backend as the only required backend in v2

## Required behavior
- The persisted index **MUST** serialize deterministically.
- The persisted index **MUST** include source path, section title, line range, and citation-ready evidence.
- Retrieval **MUST** remain traceable to the persisted index.
- The citation layer **MUST** preserve file:line fallback behavior.
- BibTeX and page metadata **MAY** be added where the source supports them.
- The backend layer **MUST NOT** require a second provider in this slice.

## Out of scope
The next slice **MUST NOT** include:
- AAR sources
- workflow-log sources
- embeddings or vector store integration
- graph database persistence
- second backend implementation
- UI/productization work
- source-authority changes

## Configuration changes
The system **SHOULD** add an explicit config field for the persisted index output path.
The system **MAY** add citation metadata fields if needed for deterministic serialization.

## Verification method
The implementation **MUST** prove that:
- the index artifact is written deterministically
- repeated runs produce stable output for unchanged inputs
- the CLI can build the index from config
- retrieval reads traceable evidence from the persisted index
- citations still fall back to file:line when richer metadata is absent

## Task breakdown
1. add persisted index path support to config
2. serialize GraphIndex to JSON deterministically
3. add a CLI index/build command
4. extend tests for stable serialized output
5. extend citation data model for optional page/BibTeX metadata
6. preserve existing query/answer behavior

## Acceptance criteria
- a reviewer can find a persisted index artifact on disk
- the persisted index is stable across identical runs
- citation fallback behavior still works
- the first backend remains Ollama
- the slice remains ADR-only and config-driven

## Escalation note
If persisted index shape or citation metadata requirements force a broader retrieval redesign, the change **MUST** be split and rebriefed before implementation continues.
