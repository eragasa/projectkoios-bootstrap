```json
{
  "title": "Workflow object static Operator Console record implementation plan",
  "artifact_type": "implementation-plan",
  "status": "planned-paused-for-approval",
  "datetime": "20260711.103626Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "source_architecture": "docs/architecture/architecture.workflow-object.md",
  "source_brief": "docs/plans/implementation-brief.20260711.102123_workflow-object-static-operator-console-record.md",
  "source_schema_candidate": "docs/plans/schema-proposal.workflow-object.static-record.20260711.102743.md",
  "source_roadmap": "docs/plans/roadmap.20260711.102324_workflow-object-future-slices.md",
  "source_example_skeleton": "docs/plans/example.workflow-object.operator-console-skeleton.20260711.103748.json",
  "source_plan_review": "docs/reviews/architecture-plan-review.20260711.104117_workflow-object-static-operator-console-record.md",
  "slice_name": "workflow-object-static-operator-console-record",
  "target_record": "dev/workflow-objects/operator-console-bootstrap-bundle.workflow-object.json",
  "next_owner": "USER_OR_HERMES_APPROVAL",
  "coding_started": false
}
```

# Implementation plan 20260711.103626: Workflow object static Operator Console record

## Status

Revised plan after ATHENA/KOIOS/HERMES shape-watchpoint resolution. Planned and paused for ATHENA approval before USER/HERMES coding approval. No coding has started for this slice.

Shape watchpoint resolution: VULCAN will use `docs/plans/example.workflow-object.operator-console-skeleton.20260711.103748.json` as the ATHENA-approved concrete candidate shape for implementation planning. VULCAN must not invent fields outside this skeleton/candidate package during Slice 0 implementation.

## Source authority

- Architecture: `docs/architecture/architecture.workflow-object.md`.
- Implementation brief: `docs/plans/implementation-brief.20260711.102123_workflow-object-static-operator-console-record.md`.
- Candidate shape: `docs/plans/schema-proposal.workflow-object.static-record.20260711.102743.md`.
- Future guidance only: `docs/plans/roadmap.20260711.102324_workflow-object-future-slices.md`.
- Concrete candidate skeleton: `docs/plans/example.workflow-object.operator-console-skeleton.20260711.103748.json`.
- Architecture plan review: `docs/reviews/architecture-plan-review.20260711.104117_workflow-object-static-operator-console-record.md`.

## Objective

Add exactly one static, non-authoritative workflow-object projection/index record for the accepted Operator Console bootstrap bundle:

- `dev/workflow-objects/operator-console-bootstrap-bundle.workflow-object.json`

The record will preserve the artifact-vs-Petri-net distinction and use DataObject vocabulary for JSON record sections. It will point back to source artifact paths/hashes/evidence rather than absorbing source authority.

Minimality constraint: the first record should prove the shape, not index the whole Operator Console history. The final record should follow the skeleton's representative/minimal shape: nine `artifact_records`, including exactly one package/source ref (`src/typescript/projectkoios/ui/operator-console/package.json`), unless an additional artifact is strictly required to support a claim and explicitly justified in the implementation report.

## Scope

In scope:

- Create one static JSON `WorkflowObjectRecord` DataObject at the target path.
- Keep the first record minimal/representative and skeleton-aligned:
  - one `work_item`;
  - nine representative `artifact_records` from the skeleton;
  - three `gate_evaluations` from the skeleton;
  - one `validation_evidence` entry;
  - one `preview_evidence` entry;
  - explicit `authority_boundary` and reconciled non-authority markers;
  - explicit deferred extension/note that related artifacts are intentionally omitted in the first pass.
- Include only the required minimal package/source ref: `src/typescript/projectkoios/ui/operator-console/package.json`.
- Defer broad package/source indexing, source-directory indexing, preview-CLI indexing, full AAR closure, and related artifact closure.
- Use only candidate snake_case JSON fields from the ATHENA-approved skeleton/candidate package; do not invent additional schema detail during implementation.
- Compute SHA-256 file hashes for referenced file artifacts where feasible.
- Use explicit directory-summary/path-only `ContentRef` records for directories only if a directory artifact becomes strictly required and approved/justified; do not recursive-hash source trees.
- Add one small test-only validator for this static record.
- Write implementation report and update VULCAN state/active after coding.

Out of scope:

- Repository-wide schema authority or `docs/schemas/` files.
- Production validator framework, reusable schema package, or CLI.
- Storage/database adapter.
- UI or Operator Console integration.
- Petri-net runtime changes or transition firing.
- Live intercom/session/terminal adapters or live repository scans at runtime.
- Bulk workflow-object generation.
- Mutating referenced source artifacts.
- Updating `docs/adr/`.

## Implementation tasks after approval

1. Seek ATHENA approval of this revised implementation plan before coding.
   - The concrete candidate shape is `docs/plans/example.workflow-object.operator-console-skeleton.20260711.103748.json`.
   - If ATHENA requests shape or plan changes, update the plan and remain paused.

2. Inspect only skeleton-selected representative source artifacts.
   - Confirm selected files/paths exist or record explicit unavailable reasons.
   - Do not edit source artifacts referenced by the workflow object.

3. Build the static JSON record manually/deterministically from the skeleton.
   - Copy the skeleton shape to `dev/workflow-objects/operator-console-bootstrap-bundle.workflow-object.json` and replace placeholders such as `TO_BE_FILLED_BY_VULCAN` with actual content refs/hashes.
   - Preserve top-level `record_type`, `record_shape_version: candidate-0`, `shape_authority`, `record_id`, title, status, authority boundary, and reconciled non-authority markers.
   - Preserve the skeleton's one `work_item` for the Operator Console P0/P1/readability bundle.
   - Preserve the skeleton's nine representative `artifact_records`, including `artifact:package.operator-console-package-json` and no broader package/source index.
   - Preserve the skeleton's three `workflow_places`, one `workflow_token`, three `transition_gates`, and three `gate_evaluations` unless ATHENA approves a change.
   - Preserve one `validation_evidence` entry and one `preview_evidence` entry.
   - Preserve `deferred_extensions`/open questions stating related artifacts and broader source/package indexing are intentionally omitted in first pass.
   - Keep every `gate_evaluations[*].completion_authority_created` value `false`.

3. Preserve DataObject / ActionObject.method vocabulary.
   - JSON sections remain snake_case collections but map to DataObjects in naming/comments/reporting.
   - Any validator behavior is described as test-only `WorkflowObjectValidator.validateRecord(...)` behavior, not production schema authority.

4. Add a small test-only validator.
   - Suggested path: `tests/projectkoios/bootstrap/workflow_objects/test__operator_console_static_record.py`.
   - Validate JSON parses and target record exists.
   - Validate required top-level fields/non-authority markers.
   - Validate selected `artifact_records` locators exist unless explicitly unavailable.
   - Validate selected `content_ref` values are present or explicitly unavailable.
   - Validate no artifact id/path is used as a workflow place id.
   - Validate all gate evaluations set `completion_authority_created: false`.
   - Validate skeleton-bounded evidence counts: exactly nine artifact records unless explicitly justified, three gate evaluations, one validation evidence entry, one preview evidence entry.
   - Validate the only package/source ref is `src/typescript/projectkoios/ui/operator-console/package.json` unless an additional source ref is explicitly justified.
   - Do not introduce a reusable validator package, JSON Schema, CLI, storage, UI, or runtime code.

5. Validate from repo root.
   - `uv run pytest tests/projectkoios/bootstrap/workflow_objects/test__operator_console_static_record.py`
   - `git diff --check`
   - `git status --short -- docs/adr`
   - `find dev -path '*workflow-object*' -type f -maxdepth 4 -print || true`
   - If Python test code is added, run focused `uv run ruff check ...` and `uv run mypy ...` on the new test file if practical.

6. Report and close out.
   - Write `docs/implementation/workflow-object-static-operator-console-record.<timestamp>.md`.
   - Update `workspaces/vulcan/state.md` and `workspaces/vulcan/active.md`.
   - Write an AAR only if implementation exposes a durable process lesson or validation gap.
   - Run Graphify update if source/test structure changes materially.

## Hash/ref strategy

- File artifacts: SHA-256 of current file bytes from repository root, recorded as `content_ref.ref_type: sha256`, `availability: present`.
- Required minimal package/source ref: hash only `src/typescript/projectkoios/ui/operator-console/package.json`.
- Directory artifacts: not expected from the current skeleton. If a directory ref becomes strictly required, use `content_ref.ref_type: directory-summary` with path-only value and limitations; no recursive tree hash for candidate-0.
- Unavailable/nonexistent refs: keep the artifact record only if needed and set `availability: explicitly-unavailable` with `unavailable_reason`.
- The workflow object record itself will not self-hash in candidate-0 to avoid update loops.

## Pause triggers

Pause if implementation requires schema authority, `docs/schemas/`, production validator framework, CLI, storage/database, UI integration, Petri-net runtime changes, live adapters, bulk generation, mutating referenced source artifacts, recursive package/source hashing, broad workflow architecture changes, adding fields not present in the ATHENA-approved skeleton/candidate package, adding package/source refs beyond `package.json` without strict justification, or changing `completion_authority_created` away from `false`.

## Approval request

ATHENA approval is requested for this revised plan before coding. After ATHENA approval, VULCAN should still await USER/HERMES coding approval if required by the active workflow.
