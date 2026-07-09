# Implementation brief 20260708.041245: Template representation round-trip first slice

## Status

Implementation-ready draft for VULCAN review/execution after user approval.

## Provenance

- Acting-As: ATHENA
- Repository: projectkoios-bootstrap
- Workspace: workspaces/athena/
- User direction: `new session` → selected option `3` from Athena startup choices, meaning draft a VULCAN handoff if implementation is desired.
- Source ADR draft: `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md`
- Source schema-backed ADR proposal: `dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.schema-backed.md`
- Source workplan: `docs/plans/template-representation-and-implementation-namespace-split.md`
- Source indexes: `docs/templates/templates.00.md`, `docs/implementation/implementation.00.md`
- Existing schema/ADR rendering precedent: `src/python/projectkoios/bootstrap/schema/`, `tests/projectkoios/bootstrap/schema/`

## Authority boundary

This brief translates the current ATHENA template-representation draft surfaces into a bounded implementation handoff. It does not promote the draft ADRs to accepted status and does not authorize broad ingestion, product-domain template architecture, Graphify ingestion changes, vault ingestion, source crawling, or a new top-level ingestion package.

VULCAN owns implementation, tests, validation, implementation reports, and deviation reports. ATHENA owns architecture-conformance review. If VULCAN finds the requested package boundary or round-trip contract cannot be implemented without changing architecture semantics, stop and produce a deviation report rather than broadening the slice.

## Objective

Implement the smallest useful template-representation slice:

1. define a canonical JSON representation for one reusable bootstrap template fixture;
2. render that canonical representation to deterministic Markdown;
3. parse controlled Markdown back into the canonical JSON representation;
4. prove JSON → Markdown → JSON round-trip equivalence for the first fixture;
5. keep template-document handling separate from implementation-document indexing and from broad ingestion systems.

## Package boundary

Preferred first-slice package boundary:

```text
src/python/projectkoios/bootstrap/template_representation/
  __init__.py
  models.py
  markdown.py
  paths.py
```

Tests should live under:

```text
tests/projectkoios/bootstrap/template_representation/
```

VULCAN may choose equivalent file names inside this package. Do not implement this slice under `src/python/ingestion/`, `src/python/projectkoios/ingestion/`, or `src/python/projectkoios/ingestors/`.

## First supported fixture

Use one existing template as the initial proof fixture. Recommended fixture:

- `docs/templates/ADR.proposal.template.md`

If that template proves ambiguous, VULCAN may select a simpler existing template from `docs/templates/`, but the implementation report must explain why.

## Required representation behavior

The canonical template representation MUST capture, at minimum:

- template identifier or name;
- source path;
- title/heading;
- ordered Markdown sections;
- section body text;
- explicit placeholders or instruction markers when deterministically detectable;
- representation version.

The representation SHOULD keep Markdown formatting details out of semantic equality unless the formatting changes meaning. The model MUST remain local to bootstrap template representation and MUST NOT become a generic repository ingestion model.

## Markdown renderer contract

The renderer consumes the canonical template representation and emits deterministic Markdown.

Renderer output MUST:

- preserve section order from the canonical representation;
- render a stable top-level heading;
- preserve placeholder/instruction text without inventing content;
- normalize presentation-only whitespace consistently;
- avoid using filesystem traversal or broad document ingestion behavior.

## Markdown parser contract

The parser consumes controlled Markdown for supported templates and emits the canonical representation.

The parser MUST fail with a typed/inspectable error for:

- missing required heading/title;
- ambiguous heading hierarchy that would change section identity;
- content that cannot be mapped without semantic loss;
- attempts to parse files outside the supported template namespace unless explicitly passed as a test fixture.

The parser MAY normalize presentation-only differences such as blank-line count, trailing whitespace, or line wrapping when tests prove canonical equivalence.

## Namespace classification behavior

Add a minimal namespace helper only if needed for the first slice.

Namespace handling MUST distinguish:

- template documents under `docs/templates/`;
- implementation reports and execution records under `docs/implementation/`;
- plan/brief documents under `docs/plans/`.

Namespace handling MUST NOT reclassify implementation documents as templates or depend on a nonexistent ingestion package.

## Test obligations

VULCAN should add focused tests for:

1. construction of the canonical template representation from the first fixture;
2. JSON/dict serialization and deserialization of that representation;
3. deterministic JSON → Markdown rendering;
4. Markdown → JSON parsing for the controlled render;
5. JSON → Markdown → JSON round-trip equivalence;
6. allowed presentation variance fixtures;
7. typed/inspectable errors for semantic parse failures;
8. namespace classification boundaries for `docs/templates/`, `docs/implementation/`, and `docs/plans/`.

The first implementation slice MUST prove one template round-trip before expanding to every file in `docs/templates/`.

## Validation commands

VULCAN should choose the final test command set. The implementation report SHOULD include at minimum:

```bash
uv run pytest tests/projectkoios/bootstrap/template_representation -q
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/template_representation
git diff --check
```

If VULCAN modifies shared schema, CLI, or documentation indexes, include the relevant existing tests and explain the expanded validation set.

## Non-goals

Do not add in this slice:

- Graphify ingestion daemon changes;
- vault ingestion, PDF ingestion, source crawling, or evidence ingestion;
- `src/python/ingestion/`, `projectkoios.ingestion`, or a generic ingestion framework;
- product-facing template architecture for the mothership or product repositories;
- broad migration of all templates before one fixture is proven;
- changes to ADR status or lifecycle authority;
- implementation from the Athena workspace.

## Expected output artifacts

- Implementation files under `src/python/projectkoios/bootstrap/template_representation/` or documented equivalent inside `projectkoios.bootstrap`.
- Tests under `tests/projectkoios/bootstrap/template_representation/`.
- Implementation report under `docs/implementation/` summarizing files changed, validation output, deviations, and any ambiguity in the template fixture.
- Deviation report if the package boundary, fixture, or semantic equivalence contract requires architecture clarification.

## Ready-to-implement condition

This brief is ready for VULCAN review/execution only after explicit user approval to implement. VULCAN should proceed from this brief and cited repository artifacts, not from hidden chat context.
