# Implementation Plan: Template Representation Contract and Implementation Namespace Split

## Source

- ADR: `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md`
- Related surfaces: `docs/templates/templates.00.md`, `docs/implementation/implementation.00.md`

## Scope

Implement the narrowly scoped template/document ingestion boundary for this repo slice:

- make the JSON↔Markdown template contract real in code
- define the canonical template representation and round-trip transforms
- separate template and implementation document surfaces in the docs index layer
- keep Markdown presentation differences intentionally allowed when meaning is preserved
- avoid broad ingestion behavior outside the template/document surface

## Repository target

- Current source root: `src/python/projectkoios/bootstrap/`
- Blocking mismatch: `src/python/ingestion/` does not exist in this repository
- Recommended approach: implement in the existing Python package tree and keep the slice inside the bootstrap package boundary

## File-level tasks

### 1) Template model layer

- add a canonical template data model
- define the JSON shape for reusable templates
- define a Markdown-facing representation that can be rendered and ingested
- keep the model tolerant of formatting variance that does not change meaning
- keep any ingestion naming strictly local to template/document handling

### 2) JSON → Markdown rendering

- implement a renderer that emits stable Markdown from the canonical template form
- preserve semantic content while allowing presentation-only differences
- ensure the renderer can support the existing template namespace files

### 3) Markdown → JSON ingestion

- implement an ingester that reconstructs the canonical template form from Markdown
- normalize allowed presentation variance into the same JSON output
- reject only meaning-changing differences, not cosmetic layout choices

### 4) Namespace-aware document handling

- align template documents with `docs/templates/`
- align implementation documents with `docs/implementation/`
- keep the two surfaces independent in code and navigation
- do not expand this plan into general repository ingestion

### 5) Index and guidance updates

- ensure `docs/templates/templates.00.md` lists the template files that belong to the namespace
- ensure `docs/implementation/implementation.00.md` lists implementation docs and links back to controlling ADRs
- update any architecture-index links that point at the new namespace split
- keep implementation-plan links pointed at the new narrow ADR

### 6) Tests

- JSON → Markdown round-trip tests
- Markdown → JSON round-trip tests
- tests for allowable Markdown presentation variance
- tests for namespace index/link correctness
- regression tests for current template docs

## Task breakdown order

1. confirm package location and module boundary
2. define canonical template data model
3. implement Markdown renderer
4. implement Markdown ingester
5. wire namespace-aware document handling
6. update index/link surfaces
7. add tests
8. validate against current docs

## Verification method

- unit tests for template round-tripping
- fixture-based tests for allowed Markdown variance
- link/path checks for `docs/templates/` and `docs/implementation/`
- inspection of current repository paths to confirm no hidden `src/python/ingestion/` package is assumed

## Risks / escalation

- If the new package path must truly be `src/python/ingestion/`, escalate before coding so the repository layout can be reconciled first.
- If Markdown variance proves ambiguous, narrow the contract before hardening parser behavior.
- If implementation docs need a different naming convention, stop and align the namespace index before adding more files.

## Deliverables

- template model and JSON↔Markdown transform code
- namespace-aware handling for template and implementation documents
- round-trip and variance tests
- updated namespace index surfaces

## Notes

- The current repository already has `src/python/projectkoios/bootstrap/` and no `src/python/ingestion/` tree.
- Keep the first slice small: prove one template can round-trip cleanly before expanding to the full namespace.
