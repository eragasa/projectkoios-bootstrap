```json
{
  "title": "Workflow object static Operator Console record implementation brief",
  "artifact_type": "implementation-brief",
  "status": "vulcan-planning-ready",
  "datetime": "20260711.102123Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_architecture": "docs/architecture/architecture.workflow-object.md",
  "slice_name": "workflow-object-static-operator-console-record",
  "next_owner": "VULCAN"
}
```

# Implementation brief 20260711.102123: Workflow object static Operator Console record

## Purpose

Create exactly one static workflow-object record representing the accepted Operator Console bootstrap-incubation P0/P1/readability bundle.

The record should prove the workflow-object architecture vocabulary without creating schema, storage, CLI, UI, Petri-net runtime, or live orchestration authority.

## Source architecture

Controlling architecture:

- `docs/architecture/architecture.workflow-object.md`

Candidate record shape and tiny example skeleton for this slice:

- `docs/plans/schema-proposal.workflow-object.static-record.20260711.102743.md`
- `docs/plans/example.workflow-object.operator-console-skeleton.20260711.103748.json`

The schema proposal and example skeleton are candidate static JSON guidance, not `docs/schemas/` authority.

Relevant source architecture/evidence:

- `docs/architecture/architecture.operator-console.md`
- `docs/architecture/architecture.workflows.00.md` as workflow context only
- `docs/architecture/architecture.petrinet.00.md` as Petri-net context only

## Required architecture distinction

VULCAN must preserve the accepted distinction:

- documents/artifacts are durable `ArtifactRecord`-like references with source path, status/lifecycle evidence, provenance, owner/domain, authority boundary, and hash/version/ref where required;
- Petri-net places are workflow states, not document files;
- workflow tokens reference work items and artifact versions/records;
- transition gates evaluate typed artifact/evidence/status predicates;
- workflow objects are projection/index records, not source artifact authority and not completion authority.

Do not make an artifact/document a Petri-net node/place. Do not name implementation-facing artifact records `Node` unless the name is explicitly scoped to graph visualization and cannot be confused with Petri-net places.

## Scope

In scope:

- Add one static workflow-object record for the accepted Operator Console P0/P1/readability bundle.
- Use `docs/plans/example.workflow-object.operator-console-skeleton.20260711.103748.json` as the representative minimum shape, while replacing placeholders and correcting evidence details during implementation.
- Put the record under an explicitly non-authoritative fixture/dev path selected by VULCAN planning.
- Use existing source artifacts by path and content hash/ref.
- Include work item identity, artifact refs, gate evaluations, validation evidence, user preview evidence, review/acceptance refs, non-authority markers, and process-capture links.
- Preserve generated/fixture/static/non-live markers for Operator Console artifacts.
- Include validation that referenced paths exist and source hashes/refs are present where required.

Required first-slice representation:

- `dev/workflow-objects/operator-console-bootstrap-bundle.workflow-object.json`

VULCAN should use the candidate JSON shape in `docs/plans/schema-proposal.workflow-object.static-record.20260711.102743.md`. This does not authorize a repository-wide JSON Schema or any file under `docs/schemas/`.

## Explicit out of scope

- Accepted repository-wide JSON schema or schema migration.
- Database/storage adapter.
- CLI command.
- UI support or Operator Console rendering of the workflow object.
- Petri-net runtime changes or firing transitions.
- Live intercom/session/terminal adapters.
- Live repository scanning beyond validation performed while creating the static record.
- Bulk workflow-object generation.
- Mutation of source artifacts referenced by the record.
- Product/mothership authority or extraction.
- Updating `docs/adr/`.

## Required record contents

The static record must include the following content categories.

### Work item identity

Required fields/semantics:

- stable work item id, suggested: `workflow-object.operator-console-bootstrap-bundle.20260711`;
- title: `Operator Console bootstrap P0/P1/readability bundle`;
- slice/work item names included:
  - `operator-console-review-one-proposal-fixture`;
  - `operator-console-fixture-interaction-visibility`;
  - `operator-console-readability-navigation-fixture`;
- repository: `projectkoios-bootstrap`;
- incubation package path: `src/typescript/projectkoios/ui/operator-console/`;
- represented record producer role/domain: `ATHENA` for the brief, `VULCAN` for implementation evidence produced by VULCAN;
- status/lifecycle value: accepted/read-model/static fixture, with source/evidence for that assertion;
- non-authority statement: record is a projection/index only and does not replace source artifacts, completion decisions, or Operator Console product authority.

### Artifact refs

Each artifact ref must include:

- artifact id;
- path/locator;
- artifact type;
- owner role/domain;
- status/lifecycle value with source/evidence for the assertion;
- authority boundary;
- content hash/ref/version, required for generated, fixture-backed, or immutable review evidence unless explicitly unavailable;
- provenance/source notes;
- produced-by or consumed-by transition references where useful.

The first implementation should use a representative minimum artifact set rather than indexing the whole Operator Console universe. It may start from the skeleton's 5-8 representative artifact records and add only artifacts needed to satisfy evidence claims.

At minimum include refs for:

Architecture and brief/plan artifacts:

- `docs/architecture/architecture.operator-console.md`
- `docs/architecture/architecture.workflow-object.md`
- `docs/plans/implementation-plan.20260711.073912_operator-console-review-one-proposal-fixture.md`
- `docs/plans/implementation-plan.20260711.084907_operator-console-fixture-interaction-visibility.md`
- `docs/plans/implementation-brief.20260711.091622_operator-console-readability-navigation-fixture.md`
- `docs/plans/implementation-plan.20260711.092008_operator-console-readability-navigation-fixture.md`

Implementation and review artifacts:

- `docs/implementation/operator-console-review-one-proposal-fixture.20260711.081405.md`
- `docs/reviews/architecture-conformance.20260711.081734_operator-console-review-one-proposal-fixture.md`
- `docs/reviews/architecture-conformance.20260711.082740_operator-console-actionobject-refactor.md`
- `docs/implementation/operator-console-fixture-interaction-visibility.20260711.090601.md`
- `docs/reviews/architecture-conformance.20260711.091137_operator-console-fixture-interaction-visibility.md`
- `docs/implementation/operator-console-readability-navigation-fixture.20260711.092524.md`
- `docs/reviews/architecture-conformance.20260711.093009_operator-console-readability-navigation-fixture.md`

Process-capture artifacts:

- `docs/AAR/aar.20260711.081405_operator-console-review-one-proposal-fixture.md`
- `docs/AAR/aar.20260711.090601_operator-console-fixture-interaction-visibility.md`
- `docs/AAR/aar.20260711.092524_operator-console-readability-navigation-fixture.md`

Package/source refs for candidate-0:

- exactly one minimal package/source ref is required: `src/typescript/projectkoios/ui/operator-console/package.json` as a `package-manifest` artifact with a SHA-256 `ContentRef`.
- broader package/source refs such as `src/typescript/projectkoios/ui/operator-console/`, `package-lock.json`, `src/`, `fixtures/`, or specific fixture/source files are intentionally deferred unless VULCAN needs one to support an explicit evidence claim.
- if VULCAN includes a directory ref, it must use `directory-summary` / path-only content ref with limitations, not recursive hashing.

Optional related evidence if VULCAN determines it is part of the accepted closeout/proof bundle:

- `docs/implementation/operator-console-preview-cli.20260711.093303.md`
- `docs/plans/implementation-plan.20260711.094447_operator-console-preview-cli.md`
- `src/python/projectkoios/bootstrap/commands/operator_console.py`
- `tests/projectkoios/bootstrap/test__OperatorConsolePreviewCommand__run.py`

If included, mark preview CLI evidence as related operator-preview support, not as workflow-object scope expansion.

The record must include a `deferred_extensions` or notes entry explaining that broader package/source indexing is intentionally omitted to avoid quasi-bulk indexing, and must not make unsupported status claims that depend on omitted artifacts.

### Transition and gate evaluations

Include explicit transition/gate records for the observed bundle. At minimum:

1. `architecture-established`
   - consumed: user/HERMES Operator Console direction if represented by existing artifact refs;
   - produced: `docs/architecture/architecture.operator-console.md`;
   - gate result: passed/accepted as architecture control surface.
2. `p0-plan-approved`
   - consumed: architecture and P0 implementation plan;
   - produced/authorized: VULCAN P0 implementation work;
   - evidence refs: P0 plan and relevant review/acceptance notes if available.
3. `p0-implemented-and-reviewed`
   - consumed: P0 plan and implementation report;
   - produced: P0 implementation evidence and conformance reviews;
   - gate result: accepted by ATHENA review.
4. `actionobject-refactor-reviewed`
   - consumed: P0 package refactor evidence;
   - produced: `docs/reviews/architecture-conformance.20260711.082740_operator-console-actionobject-refactor.md`;
   - gate result: accepted by ATHENA review.
5. `p1-interaction-visibility-implemented-reviewed-previewed`
   - consumed: P1 plan/report;
   - produced: P1 implementation and review evidence;
   - gate result: accepted, display-only and fixture-only.
6. `p2-readability-navigation-implemented-reviewed-previewed`
   - consumed: P2 brief/plan/report;
   - produced: P2 implementation and review evidence;
   - gate result: accepted, local readability/navigation only.
7. `workflow-object-architecture-amendment-accepted`
   - consumed: `docs/architecture/architecture.workflow-object.md` and KOIOS/VULCAN/HERMES consultation summarized in source architecture;
   - produced: this brief and later static record implementation plan;
   - gate result: accepted for implementation planning.

Each gate evaluation should include:

- gate id/name;
- required artifact statuses, owner roles, evidence types, or approval predicates;
- observed result: passed/failed/warning/not-applicable/not-yet-evaluated;
- evidence refs;
- evaluator/owner role;
- timestamp or source artifact.

Gate pass/fail records are evidence only. They do not create completion authority by themselves.

### Validation evidence

Include validation records from source reports/reviews, not reinterpreted as new validation authority. At minimum represent:

- P0 package-local validation from ATHENA review:
  - `npm ci` or `npm ci --ignore-scripts` as reported;
  - `npm run typecheck`;
  - `npm test`;
  - `npm run build`;
  - `npm audit --audit-level=moderate`;
  - free-function / ActionObject checks where reported;
  - generated artifact cleanup and `git diff --check` where reported.
- P1 validation from `docs/implementation/operator-console-fixture-interaction-visibility.20260711.090601.md` and `docs/reviews/architecture-conformance.20260711.091137_operator-console-fixture-interaction-visibility.md`.
- P2 validation from `docs/implementation/operator-console-readability-navigation-fixture.20260711.092524.md` and `docs/reviews/architecture-conformance.20260711.093009_operator-console-readability-navigation-fixture.md`.

Each validation evidence entry should include command, working directory, target scope, summarized result, pass/fail/non-applicable status, source report path, and limitations if reported.

### User preview evidence

Represent user-visible preview evidence as review evidence, not product activation authority.

At minimum include:

- P0 preview: user opened local preview and confirmed UI visible, as recorded in `docs/architecture/architecture.operator-console.md` and related implementation/review artifacts.
- P1 preview: user inspected local preview at `http://127.0.0.1:4173/`, with VULCAN clarification that the slice was display-only with browser scrolling only and no internal widgets/live controls.
- P2 preview: user inspected local preview at `http://127.0.0.1:4173/`, with readability/navigation accepted by ATHENA review.

Each preview evidence entry should include preview command when available from source reports, local URL or preview method, inspected surface, user-visible behavior being validated, observed user feedback, and whether feedback changed scope.

### Non-authority and lifecycle markers

The record must include markers:

- `projection-index-only`;
- `static-record`;
- `bootstrap-incubation`;
- `fixture-only`;
- `non-live`;
- `stale-by-design`;
- `not-source-authority`;
- `not-product-authority`;
- `not-completion-authority`;
- `not-petri-net-runtime`;
- `not-schema-authority`;
- `not-storage-authority`.

The example skeleton may include extra candidate/example markers such as `static-fixture` or `representative-skeleton`, but the final record must include the required markers above.

### Process-capture links

Include links to relevant AARs listed above and any process-capture source VULCAN uses. Treat AARs and KOIOS process capture as provenance/advisory unless promoted by architecture, policy, or implementation authority.

## Validation requirements for this slice

VULCAN should validate:

1. Referenced paths exist, except any explicitly marked unavailable/nonexistent with reason.
2. Required source hashes/refs are present for generated, fixture-backed, or immutable review evidence artifacts.
3. The record includes all required content categories from this brief.
4. The record includes the required non-authority markers.
5. The record does not introduce schema/storage/CLI/UI/Petri-net runtime changes.
6. `docs/adr/` is unchanged.
7. `git diff --check` is clean.

Suggested commands from repo root:

```bash
git diff --check
git status --short -- docs/adr
find dev -path '*workflow-object*' -type f -maxdepth 4 -print || true
```

VULCAN should add a small test-only local validator for the static JSON record, unless the implementation plan explains why manual validation is safer. The validator must remain record-specific and must not create a CLI, reusable validator package, schema authority, storage layer, or auto-discovery mechanism.

Recommended validator scope:

- JSON parses;
- required top-level fields exist;
- referenced artifact `locator` paths exist unless explicitly unavailable;
- required content refs are present or explicitly unavailable;
- artifact ids are not reused as workflow place ids;
- every gate evaluation has `completion_authority_created: false`;
- required non-authority markers are present;
- at least one preview evidence entry exists for this Operator Console record.

## Pause triggers

Pause and request direction if implementation would require:

- choosing repository-wide workflow-object storage or schema;
- adding JSON schema authority;
- adding a database/storage adapter;
- adding CLI/UI support;
- modifying Petri-net runtime code;
- live session/intercom/terminal reads;
- mutating source artifacts referenced by the static record;
- broad workflow/Petri-net architecture rewrites;
- bulk generation for multiple work items;
- changing Operator Console source code beyond path/hash/reference validation needs.

## Acceptance criteria

1. Exactly one static workflow-object record is added.
2. The record represents the accepted Operator Console P0/P1/readability bundle.
3. The record preserves artifact-vs-workflow separation: artifacts are refs/records; places are workflow states; tokens reference artifacts; gates evaluate evidence.
4. All required artifact refs are present or explicitly marked unavailable with reason.
5. Source hashes/refs are present where required by the architecture amendment.
6. Gate evaluations and validation/preview evidence are represented with source refs.
7. Non-authority/lifecycle markers are explicit.
8. No schema/storage/CLI/UI/Petri-net runtime/live adapter/bulk-generation scope is introduced.
9. Validation evidence is reported in an implementation report.
10. VULCAN pauses for plan approval before coding unless USER/HERMES explicitly authorizes direct implementation.

## Handoff to VULCAN

VULCAN should produce an implementation plan for `workflow-object-static-operator-console-record` and pause for USER/HERMES approval before coding.
