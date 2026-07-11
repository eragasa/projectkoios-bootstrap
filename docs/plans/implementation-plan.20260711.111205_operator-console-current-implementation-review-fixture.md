```json
{
  "title": "Operator Console current implementation review fixture implementation plan",
  "artifact_type": "implementation-plan",
  "status": "planned-paused-for-approval",
  "datetime": "20260711.111205Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "source_brief": "docs/plans/implementation-brief.20260711.110430_operator-console-current-implementation-review-fixture.md",
  "source_architecture": [
    "docs/architecture/architecture.operator-console.md",
    "docs/architecture/architecture.workflow-object.md"
  ],
  "slice_name": "operator-console-current-implementation-review-fixture",
  "target_path": "src/typescript/projectkoios/ui/operator-console/",
  "next_owner": "USER_OR_HERMES_APPROVAL",
  "coding_started": false
}
```

# Implementation plan 20260711.111205: Operator Console current implementation review fixture

## Status

Revised after KOIOS/HERMES staleness watchpoints were incorporated into the brief/architecture. Planned and paused for USER/HERMES approval. No coding has started for this slice.

## Source authority

- Implementation brief: `docs/plans/implementation-brief.20260711.110430_operator-console-current-implementation-review-fixture.md`.
- Source architecture:
  - `docs/architecture/architecture.operator-console.md`.
  - `docs/architecture/architecture.workflow-object.md`.

## Objective

Add one compact, read-only current implementation review panel to the existing Operator Console page. The panel will display deterministic copied fixture/read-model data for the current accepted implementation bundle without live reads, mutation controls, or workflow-object/schema/storage authority.

## Scope

In scope:

- Edit only `src/typescript/projectkoios/ui/operator-console/` for UI/package changes, plus VULCAN report/state files after implementation.
- Add fixture/read-model DataObjects such as `ImplementationReviewItem` and `WorkflowObjectSummaryFixture`.
- Add an ActionObject renderer such as `CurrentImplementationReviewRenderer.render(...)`.
- Place one prominent compact panel in the existing page near summary/navigation and before detailed proposal/evidence content.
- Display static rows/cards for:
  - Operator Console P0 review-one-proposal fixture;
  - Operator Console ActionObject/DataObject refactor;
  - Operator Console P1 interaction visibility;
  - Operator Console P2 readability/navigation fixture;
  - workflow-object Slice 0 static Operator Console record.
- For each row/card, show slice name, fixture-derived status, owner/domain, implementation report path when applicable, acceptance/review path, validation source/summary, and authority boundary.
- Add one compact workflow-object summary copied from accepted Slice 0 evidence: record id, status, non-authority markers, `artifact_records=9`, `gate_evaluations=3`, `validation_evidence=1`, `preview_evidence=1`, package source ref `src/typescript/projectkoios/ui/operator-console/package.json`, snapshot/generated timestamp, source-hash timestamp/label where available, and the required working-tree/static-snapshot hash caveat.
- Keep evidence paths as display locators only.
- Use loud UI language: `static snapshot`, `not live`, and `stale-by-design until refreshed`.
- Preserve existing P0/P1/P2 content and readability/navigation affordances.

Out of scope:

- New route/screen, tabs, filters, graph visualization, artifact drilldowns, live refresh, workflow-object browser/editor, or route-level navigation.
- Browser runtime reads of repository files, `dev/workflow-objects`, Node `fs`/`path`, fetches, polling, backend/API service, live adapters, or live status derivation.
- Send/reply/ask/apply/save/approve/reject/activate controls or mutation of any source/workflow/workflow-object state.
- Workflow-object schema authority, `docs/schemas/`, storage/database adapter, production validator framework, Petri-net runtime changes, recursive hashing, product extraction, or new framework/design-system adoption.

## Implementation tasks after approval

1. Inspect current package structure and tests.
   - Confirm where fixture data and renderers currently live.
   - Confirm generated directories are absent before editing.

2. Add DataObject fixture/read-model data.
   - Extend or add contracts for `ImplementationReviewItem` and `WorkflowObjectSummaryFixture` if useful.
   - Add deterministic fixture constants derived from accepted source artifacts; do not import/parse workflow-object JSON at browser runtime.
   - Use copied counts/paths/status summaries from source artifacts.
   - Include snapshot/generated timestamp and source-hash timestamp/label values in fixture data where available; otherwise label the value as fixture-generation/source-snapshot time, not live freshness.

3. Add renderer ActionObject.
   - Add `CurrentImplementationReviewRenderer` or equivalent class.
   - Render a compact read-only panel/table/card list.
   - Use safe UI wording that avoids forbidden action words where practical, e.g. “read-only status review,” “decision authority is elsewhere,” and “no outbound messaging features.”
   - Include required hash/static-snapshot caveat or substantively identical wording: hashes identify working-tree file contents at fixture generation time, are not commit IDs, do not make the UI/workflow object source authority, and the screen is a static snapshot that may be stale until intentionally refreshed.
   - State that the workflow-object refresh protocol is not yet defined and stale source hashes require static-record validator rerun before packaging or explicit intentional-staleness recording.

4. Compose into existing page.
   - Add the panel to `OperatorConsoleRenderer` near summary/navigation and before deeper proposal/evidence content.
   - Preserve current navigation/readability behavior and existing sections.

5. Add/update tests.
   - Test the current implementation review panel renders all five accepted bundle items.
   - Test workflow-object summary counts and package source ref render.
   - Test required non-authority/static snapshot labels, stale-by-design-until-refreshed language, snapshot/generated timestamp/label, and hash caveat render.
   - Keep no-live-dependency tests passing.
   - Update forbidden control tests to check interactive controls/selectors rather than read-only explanatory text if expanded action-word scanning would conflict with safety copy.

6. Validate and preview.
   - From package: install, typecheck, tests, build, audit, dependency listing, preview.
   - From repo root: `git diff --check`, `git status --short -- docs/adr`, generated artifact cleanup check, no-live primitive scan, no durable free behavior function scan, enum-like raw string scan.
   - If workflow-object referenced artifacts changed, rerun `uv run pytest tests/projectkoios/bootstrap/workflow_objects/test__operator_console_static_record.py -q` or document explicit intentional staleness. Do not implement a broader refresh/staleness policy in this slice.
   - Record preview command/local URL and require concrete browser inspection before completion.

7. Report and close out.
   - Write implementation report under `docs/implementation/` with validation evidence, preview URL, deviations, and explicit boundary statement.
   - Update `workspaces/vulcan/state.md` and `workspaces/vulcan/active.md`.
   - Write AAR only if implementation exposes durable process lessons or validation gaps.
   - Run Graphify update after source/test changes.

## Validation watchpoints

- Safety copy must not accidentally fail forbidden-action scans. Prefer selector/control-based tests for controls and avoid forbidden action words in rendered UI where practical.
- Evidence paths are display locators only, not live links/readers unless explicitly approved.
- Status values are copied fixture/read-model claims from cited artifacts, not computed live.
- Workflow-object summary is a copied fixture projection, not a browser/editor or schema authority.
- Refresh protocol is not yet defined; broader refresh/staleness ownership is deferred to candidate future slice `workflow-object-staleness-and-refresh-policy`.
- Stale source hashes require workflow-object static-record validator rerun before packaging or explicit intentional-staleness recording.
- Existing P0/P1/P2 UI semantics must remain available.

## Pause triggers

Pause if implementation would require live repository/session reads, backend/API, storage, CLI, schema authority, Petri-net runtime changes, workflow-object browser/editor behavior, broad source/package indexing, forbidden mutation controls, source artifact mutation, new dependencies/frameworks, architecture/policy edits, product authority changes, or implementing the deferred `workflow-object-staleness-and-refresh-policy`.

## Approval request

USER/HERMES approval is requested to implement this bounded slice.
