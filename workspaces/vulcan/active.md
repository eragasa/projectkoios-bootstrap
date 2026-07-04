```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "review-handoff",
  "datetime": "20260704.174859",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "worktree": "/Users/eugene/repos/projectkoios-bootstrap-schema-record-base",
  "branch": "vulcan/schema-record-base",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": [
    "docs/implementation/implementation-report.20260704.174859_schema-record-base.md",
    "docs/implementation/implementation-report.20260704.193035_python-policy-validator.md",
    "docs/implementation/implementation-report.20260704.205637_schema-package-policy-remediation.md"
  ],
  "scratch_directory": "scratch/",
  "controlling_workspace_policy": "docs/policies/workspace-layout.md"
}
```

# Vulcan active work

## Current priority stack

1. Hand off schema-record base implementation for ATHENA conformance review.
2. Hand off Python policy validator first slice for review.
3. Hand off schema package policy remediation for review.

## Waiting on

- ATHENA review of `docs/implementation/implementation-report.20260704.174859_schema-record-base.md` and the associated patch in worktree `/Users/eugene/repos/projectkoios-bootstrap-schema-record-base`.
- Review or user direction for `docs/implementation/implementation-report.20260704.193035_python-policy-validator.md`.
- Review or user direction for `docs/implementation/implementation-report.20260704.205637_schema-package-policy-remediation.md`.
- User/Hermes decision on commit/merge timing relative to the original checkout's dirty GraphRAG/schema-record state.

## Working material

- Controlling implementation source: `docs/plans/implementation-brief.20260704.172632_schema-record-base.md`.
- Source ADR: `docs/adr/adr.schema-base.md`.
- Source workplan: `docs/plans/schema-base-adr-records-workplan.md`.
- Source schemas: `docs/schemas/schema.record-base.json`, `docs/schemas/adr-draft.schema.json`.
- Schema-record implementation report: `docs/implementation/implementation-report.20260704.174859_schema-record-base.md`.
- Python policy validator plan: `docs/plans/implementation-plan.20260704.192620_python-policy-validator.md`.
- Python policy validator implementation report: `docs/implementation/implementation-report.20260704.193035_python-policy-validator.md`.
- Schema package policy remediation report: `docs/implementation/implementation-report.20260704.205637_schema-package-policy-remediation.md`.
- Implementation package: `src/python/projectkoios/bootstrap/schema/`.
- Tests: `tests/projectkoios/bootstrap/schema/`.
- Python coding control surface: `docs/policies/python-coding.md`.
- Active working items: no files under `working/` are active right now.
- Scratch: `scratch/` is available for temporary notes and non-durable exploration.

## Ignore for now

- GraphRAG behavior changes
- projectkoios ingestor refactors
- CLI integration for schema records
- active/completed/superseded/rejected ADR lifecycle states
- implementation-report or workspace-state schema families
- historical ADR migration
- legacy schema reconciliation beyond non-canonical path detection
- product architecture decisions

## Exit criteria

The schema-record base slice is ready for review handoff when:

- worktree isolation avoids dirty-tree mixing — complete
- schema package is outside `projectkoios.ingestors` — complete
- canonical schemas load from `docs/schemas/` — complete
- project-local `$id` values resolve offline — complete
- base envelope and required metadata are validated — complete
- draft ADR schema narrows `schema_id` and `status` while preserving base metadata — complete
- immutable model construction is implemented and tested — complete
- deterministic draft ADR Markdown rendering is implemented and tested — complete
- strict Markdown ingest is implemented and tested — complete
- rejected extra-section capture is implemented and tested — complete
- relevant tests pass — complete
- implementation report is written under `docs/implementation/` — complete
- `state.md` and `active.md` are updated with validated state and next expected artifact — complete

## Next expected artifact

- ATHENA conformance review linked to `docs/implementation/implementation-report.20260704.174859_schema-record-base.md`.
