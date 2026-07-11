```json
{
  "title": "Operator Console current implementation review fixture implementation brief",
  "artifact_type": "implementation-brief",
  "status": "vulcan-planning-ready",
  "datetime": "20260711.110430Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_architecture": [
    "docs/architecture/architecture.operator-console.md",
    "docs/architecture/architecture.workflow-object.md"
  ],
  "slice_name": "operator-console-current-implementation-review-fixture",
  "target_path": "src/typescript/projectkoios/ui/operator-console/",
  "next_owner": "VULCAN"
}
```

# Implementation brief 20260711.110430: Operator Console current implementation review fixture

## Purpose

Add a bounded, read-only Operator Console fixture screen/section that lets the user inspect the current accepted implementation bundle as represented by this static fixture/read-model in the browser.

This slice should make the current implementation status reviewable by a human without adding live backend/orchestration, mutation controls, product authority, or workflow-object schema/storage authority. Displayed accepted status must be visibly copied from cited ATHENA/HERMES/user/review artifacts, not computed live by the console.

## User-facing goal

As an operator using the local browser preview, the user should be able to review the current accepted implementation bundle and answer:

- What implementation slices are currently accepted as represented by this static fixture/read-model?
- Which architecture, implementation report, review, validation, workflow-object, and preview evidence supports that status?
- Which displayed statuses are fixture-derived from cited artifacts rather than live console computation?
- What is static fixture/projection data versus live/product authority?
- Is the current implementation review surface clear enough to support the next acceptance decision?

## Source architecture

Controlling architecture:

- `docs/architecture/architecture.operator-console.md`
- `docs/architecture/architecture.workflow-object.md`

Relevant accepted evidence:

- `docs/architecture/architecture.operator-console.md`
- `docs/architecture/architecture.workflow-object.md`
- `docs/implementation/operator-console-review-one-proposal-fixture.20260711.081405.md`
- `docs/reviews/architecture-conformance.20260711.081734_operator-console-review-one-proposal-fixture.md`
- `docs/reviews/architecture-conformance.20260711.082740_operator-console-actionobject-refactor.md`
- `docs/implementation/operator-console-fixture-interaction-visibility.20260711.090601.md`
- `docs/reviews/architecture-conformance.20260711.091137_operator-console-fixture-interaction-visibility.md`
- `docs/implementation/operator-console-readability-navigation-fixture.20260711.092524.md`
- `docs/reviews/architecture-conformance.20260711.093009_operator-console-readability-navigation-fixture.md`
- `docs/implementation/workflow-object-static-operator-console-record.20260711.105117.md`
- `docs/reviews/architecture-conformance.20260711.105430_workflow-object-static-operator-console-record.md`
- `docs/reviews/implementation-review.20260711.105822_workflow-object-static-operator-console-record.md`
- `dev/workflow-objects/operator-console-bootstrap-bundle.workflow-object.json`
- `tests/projectkoios/bootstrap/workflow_objects/test__operator_console_static_record.py`

The listed paths are fixture/evidence sources for this slice. They do not become live runtime dependencies or product authority.

## Scope

In scope:

- Add one prominent read-only current-implementation review section/panel to the existing Operator Console page under `src/typescript/projectkoios/ui/operator-console/`; do not add a new route/screen unless USER/HERMES identifies a specific need.
- Recommended first cut: a compact `CurrentImplementationReviewPanel`/renderer near existing summary/navigation and above detailed proposal/evidence content.
- Use static fixture/read-model data derived from the accepted implementation bundle. Implementation must copy or encode fixture/read-model values at build/source time; browser code must not import Node `fs`/`path`, read `dev/workflow-objects` at runtime, fetch repository files, or derive status live.
- Show the accepted status of at least:
  - Operator Console P0 review-one-proposal fixture;
  - Operator Console ActionObject/DataObject refactor;
  - Operator Console P1 interaction visibility;
  - Operator Console P2 readability/navigation fixture;
  - workflow-object Slice 0 static Operator Console record.
- Show accepted bundle rows/cards for P0, ActionObject/DataObject refactor, P1, P2, and workflow-object Slice 0 with 2-4 key evidence references each; do not attempt to render every listed source artifact.
- Show artifact/evidence references for each accepted slice, including architecture, implementation report, ATHENA review, and when relevant workflow-object record/test validator paths.
- For each displayed slice row/card, include at least: slice name, status label, owner/domain, source implementation report path, acceptance/review path, validation source path or summary, authority boundary, and whether the status is fixture-derived.
- Evidence paths are display locators only; they are not clickable live file readers unless separately approved.
- Include one compact read-only workflow-object summary card copied from accepted Slice 0 evidence, not imported or parsed by browser runtime, with:
  - record id;
  - status;
  - non-authority markers;
  - `artifact_records=9`;
  - `gate_evaluations=3`;
  - `validation_evidence=1`;
  - `preview_evidence=1`;
  - package source ref: `src/typescript/projectkoios/ui/operator-console/package.json`;
  - note that hashes are working-tree content hashes, not commit identity.
- If counts or hashes from `dev/workflow-objects/operator-console-bootstrap-bundle.workflow-object.json` are displayed, label them as working-tree content hashes / static record snapshot, not durable commit identity.
- The workflow-object summary is a fixture projection copied from accepted Slice 0 evidence; it is not a workflow-object browser/editor.
- The workflow-object summary must state that a refresh protocol is not yet defined; if referenced source hashes become stale, VULCAN must rerun the workflow-object static-record validator before packaging or explicitly record intentional staleness.
- Do not add a package source index beyond the already accepted minimal `package.json` reference unless separately approved.
- Show validation/review status summaries as fixture-backed/static data.
- Include loud labels that all displayed bundle status is a static snapshot, stale-by-design until refreshed, projection/index/fixture-only, bootstrap-incubation, non-live, and not product authority.
- Display snapshot/generated timestamp and source-hash timestamp/label where available. If exact source-hash time is not available, label the value as a fixture-generation/source-snapshot timestamp rather than implying live freshness.
- Include this wording, or substantively identical UI fixture copy/README/report text: "Hashes identify the referenced working-tree file contents at fixture generation time; they are not commit IDs and do not make this UI or workflow object source authority. This screen is a static snapshot, not live operational truth, and may be stale until intentionally refreshed."
- Preserve the existing P0/P1/P2 UI and readability/navigation affordances unless deliberately improved without changing authority.
- Avoid filters, tabs, graph visualization, workflow-object explorer, artifact drilldowns, live refresh, or route-level navigation in the first cut.
- Preserve ActionObject/DataObject convention: behavior in classes; fixture/read-model data in typed interfaces/constants.
- Prefer small DataObject shapes such as `ImplementationReviewItem` and `WorkflowObjectSummaryFixture`, with ActionObject renderer behavior such as `CurrentImplementationReviewRenderer.render(...)`.
- Include package-local preview command, local URL, and concrete user browser inspection as a completion gate.

## Explicit out of scope

- Live filesystem reads from the UI.
- Backend/API service.
- Live intercom/session/terminal adapters.
- Live polling or runtime repository scanning.
- Send/reply/ask/apply/save/approve/reject/activate controls.
- Mutation of source artifacts, workflow definitions, workflow-object records, or active state.
- Workflow activation/versioning.
- Petri-net runtime changes or graph editor.
- General workflow-object browser/editor.
- Filters, tabs, graph visualization, artifact drilldowns, live refresh, or route-level navigation for this slice.
- Workflow-object schema authority, `docs/schemas/` additions, storage/database adapter, or production validator framework.
- Recursive source/package hashing.
- Product/mothership UI authority or extraction.
- New framework/design-system adoption unless separately justified and approved.

## Required preservation

VULCAN must preserve:

- fixture/static/stale-by-design/non-live labeling;
- bootstrap-incubation and not-product-authority labeling;
- workflow-object as projection/index only;
- candidate JSON shape and test-only validator as non-schema/non-production authority;
- existing no-mutation/no-live-backend boundaries;
- no durable top-level/free behavior functions except allowed thin entrypoints or test-local helpers;
- scoped enum/type ownership for durable semantic values;
- package-local dependency/tooling boundary.

## Required review/acceptance flow

This slice intentionally includes a post-implementation multi-role feedback gate. Feedback collection is post-implementation review and must not expand pre-coding architecture scope.

Required flow:

1. VULCAN writes an implementation plan and pauses for USER/HERMES approval unless USER/HERMES explicitly authorizes direct coding from this brief.
2. VULCAN implements the fixture review screen and reports validation plus preview command/local URL.
3. USER/HERMES performs concrete browser inspection of the current implementation review surface.
4. ATHENA collects focused post-implementation feedback from:
   - ATHENA: architecture/conformance and whether the user-review surface matches this intended slice;
   - VULCAN: implementability/deviation/validation notes and whether the UI/read-model remains maintainable;
   - KOIOS: provenance/authority review, evidence/source mapping, whether fixture/projection data could be mistaken for live operational truth or product acceptance, and whether all status claims have visible source references;
   - HERMES/user: orchestration/state reconciliation and concrete user browser inspection result.
5. ATHENA issues final conformance/as-built review, or a revision request if feedback exposes a boundary or acceptance issue.

## Acceptance criteria

1. Browser UI includes a current-implementation review surface that is visible in the local preview.
2. The review surface summarizes the accepted current implementation bundle: Operator Console P0, ActionObject/DataObject refactor, P1, P2, and workflow-object Slice 0.
3. The review surface includes artifact/evidence paths or link-like references sufficient for a user to identify source architecture, implementation reports, reviews, workflow-object record, and validator evidence.
4. Each displayed slice row/card includes at least source implementation report path, acceptance/review path, validation source path or summary, and whether the status is fixture-derived.
5. Displayed accepted status is visibly copied from cited ATHENA/HERMES/user/review artifacts, not computed live by the console.
6. The review surface includes validation/review status summaries as static fixture data.
7. The workflow-object summary is compact and read-only, and it does not imply schema/storage/runtime/completion authority.
8. Workflow-object counts/hashes, if shown, are labeled as working-tree content hashes / static record snapshot, not durable commit identity.
9. UI labels clearly state static snapshot/stale-by-design-until-refreshed/non-live, bootstrap-incubation, projection/index-only, and not-product-authority boundaries, and include the hash/static-snapshot wording required in Scope or substantively identical wording.
10. The review surface displays snapshot/generated timestamp and source-hash timestamp/label where available, without implying live freshness.
11. The workflow-object summary states that refresh protocol is not yet defined and stale source hashes require validator rerun before packaging or explicit intentional-staleness recording.
12. No mutation, activation, approval, send/reply/ask, live refresh, backend, or runtime adapter controls are introduced.
13. Existing Operator Console P0/P1/P2 content remains available and semantically preserved.
14. ActionObject/DataObject convention remains satisfied.
15. Tests cover the new review surface/read-model where practical, including absence of forbidden controls and presence of non-authority labels.
16. Tests or scans for forbidden action words are scoped to buttons, forms, interactive controls, or explicit control-surface selectors so read-only safety copy does not fight validation. UI copy should avoid forbidden action words where practical and prefer labels such as "decision authority is elsewhere," "read-only status review," and "no outbound messaging features."
17. Package validation passes: install, typecheck, tests, build, audit as applicable.
18. Validation includes scans/checks for no live primitives, no forbidden action controls, no durable free behavior functions, no enum-like dangling semantic raw strings, `git diff --check`, `docs/adr` unchanged, and generated artifact cleanup.
19. If referenced workflow-object source artifacts changed before packaging, VULCAN reruns the workflow-object static-record validator or records why the fixture was intentionally left stale.
20. VULCAN provides preview command and local URL.
21. USER performs browser inspection and confirms whether the current implementation review surface is acceptable.
22. ATHENA collects VULCAN, KOIOS, and HERMES/user feedback before final acceptance or revision request; KOIOS specifically verifies the new UI screen cannot be mistaken for live operational truth or product acceptance and that all status claims have visible source references.
23. `node_modules`, `dist`, `coverage`, preview state, screenshots, local sessions, and secrets are not committed.

## Suggested validation commands

When implementing tests or scans, distinguish forbidden interactive controls from read-only explanatory copy. If grep output contains safety text only, VULCAN should either scope the automated check more narrowly or document why the output is non-interactive and non-mutating.

From `src/typescript/projectkoios/ui/operator-console/`:

```bash
npm install --ignore-scripts
npm run typecheck
npm test
npm run build
npm audit --audit-level=moderate
npm ls --depth=0
npm run preview -- --host 127.0.0.1
```

From repository root:

```bash
git diff --check
git status --short -- docs/adr
find src/typescript/projectkoios/ui/operator-console -type d \
  \( -name node_modules -o -name dist -o -name coverage \) -prune -print
grep -R "fetch(\|WebSocket\|EventSource\|setInterval\|setTimeout\|XMLHttpRequest\|localStorage\|sessionStorage" -n \
  src/typescript/projectkoios/ui/operator-console/src \
  src/typescript/projectkoios/ui/operator-console/fixtures \
  --include='*.ts' || true
grep -R "send\|reply\|ask\|approve\|reject\|apply\|save\|activate\|mutate" -n \
  src/typescript/projectkoios/ui/operator-console/src \
  src/typescript/projectkoios/ui/operator-console/fixtures \
  --include='*.ts' || true
grep -R "^export function\|^function " -n \
  src/typescript/projectkoios/ui/operator-console/src \
  src/typescript/projectkoios/ui/operator-console/fixtures || true
grep -R "kind: \"\|status: \"\|category: \"\|state: \"\|statusClass: \"\|displayedAs: \"\|fixtureStatus: \"\|approvalState: \"\|deliveryStatus: \"\|sourceArtifactType: \"\|hashLabel: \"" -n \
  src/typescript/projectkoios/ui/operator-console/src \
  src/typescript/projectkoios/ui/operator-console/fixtures \
  --include='*.ts' || true
```

If referenced workflow-object source artifacts change before packaging, rerun the workflow-object static record validator or explicitly record why the fixture is intentionally stale. Broader staleness/refresh ownership is intentionally deferred to a candidate `workflow-object-staleness-and-refresh-policy` slice:

```bash
uv run pytest tests/projectkoios/bootstrap/workflow_objects/test__operator_console_static_record.py -q
```

## Deferred follow-up candidate

KOIOS/HERMES identified a broader policy gap: workflow-object static snapshots need a refresh/staleness policy defining static snapshot vs stale snapshot vs refreshed snapshot, required timestamp/hash display language, when validator failure blocks acceptance, who owns refresh decisions, and how UI fixtures display staleness. Candidate future slice: `workflow-object-staleness-and-refresh-policy`. This brief only incorporates immediate UI-facing static snapshot language and does not authorize broad refresh-protocol implementation.

## Pause triggers

Pause and request direction if implementation would require:

- live adapters or live transcript/session/repository reads;
- send/reply/ask/apply/save/approve/reject/activate controls;
- backend/API service;
- persistent storage;
- workflow-object schema/storage/production validator authority;
- workflow mutation/activation;
- Petri-net runtime or graph/editor scope;
- broader workflow-object browser/editor scope;
- framework adoption or broad product design-system decisions;
- source artifact mutation;
- architecture or policy edits beyond this bounded scope.

## Handoff to VULCAN

VULCAN should produce an implementation plan for `operator-console-current-implementation-review-fixture` and pause for USER/HERMES approval before coding, unless USER/HERMES explicitly permits direct implementation from this brief.
