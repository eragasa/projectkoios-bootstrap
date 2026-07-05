```json
{
  "title": "Athena active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active-dirty-state-stabilization",
  "datetime": "20260705.220000",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/athena/",
  "priority_count": 3,
  "active_working_items": []
}
```

# Athena active work

## Current priority stack

1. Stabilize the large dirty repo state from template/lifecycle/Petri-net/archive changes.
2. Validate and package the changes into coherent commits.
3. Only after packaging, resume Petri-net architecture elaboration or template/schema follow-up work.

## Waiting on

- User packaging preference if the dirty state should be split differently than:
  1. lifecycle/template/schema controls,
  2. Petri-net report/index restructuring,
  3. archive relocation.
- Decision on whether `docs/archive/...` references should be rewritten or left as historical provenance through `docs/archive/README.md`.
- Decision on whether `/Users/eugene/repos/projectkoios-spec/` needs git initialization or separate repo handling.

## Current dirty-state categories

- Template/lifecycle/schema:
  - `docs/adr/adr.templates.md`
  - `docs/adr/adr.templates-adr.md`
  - `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`
  - `docs/policies/architecture.adr.lifecycle.md`
  - `docs/architecture/architecture.lifecycle.00.md`
  - `docs/templates/ADR.proposal.template.md`
  - `docs/templates/architecture.template.md`
  - schema files under `docs/schemas/`
- Petri-net/workflow architecture/report restructuring:
  - `docs/architecture/architecture.workflows.00.md`
  - `docs/architecture/architecture.petrinet.00.md`
  - topic-first implementation report files under `docs/implementation/`
  - related conformance reviews and source records.
- Archive relocation:
  - `docs/archive/` files deleted from this repo.
  - archive files moved to `/Users/eugene/repos/projectkoios-spec/archive/`.
  - `docs/archive/README.md` pointer added.

## Required before commit

- Review `git status --short --branch` and diff stats.
- Rerun validation:
  - JSON parse checks for touched schema/metadata files.
  - `PYTHONPATH=src/python python -m pytest tests/projectkoios/bootstrap/schema/test__DraftAdrRecord__markdown.py -q`.
  - `git diff --check`.
- Confirm archive destination contains moved files.
- Commit and push only after user approval or explicit packaging direction.

## Ignore for now

- New Petri-net ADR slices.
- Template JSON↔Markdown implementation work.
- Product-domain workflow decisions.
- Full repo-wide reference rewriting unless explicitly requested.

## Exit criteria

Athena state is stable when the dirty repo state is either committed/pushed or clearly handed off with validation status, packaging plan, archive destination, and remaining risks documented.
