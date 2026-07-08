```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260706.000000",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/hermes/",
  "document_domain": "orchestration, repo-state reconciliation, cross-domain consistency",
  "control_files": ["state.md", "active.md"],
  "next_owner": "HERMES",
  "blockers": []
}
```

# Hermes active work

## Current priority stack

1. Track schema namespace/record-family reconciliation as a next planning item.
2. Get user decision on staging/commit boundaries for the reviewed dirty tree.
3. If committing separately, keep workspace-state, Python-policy/test-remediation, schema governance, and Petri-net architecture slices bounded.
4. Decide whether untracked Koios workspace control files belong in a closeout or require Koios review first.

## Next action

- Route or draft a bounded Athena-owned schema namespace reconciliation artifact when user asks to act on the schema naming concern.
- The schema reconciliation should decide:
  1. canonical schema filename convention, e.g. whether `adr-draft.schema.json` becomes `schema.adr-draft.json`;
  2. canonical `$id` / `schema_id` convention and compatibility aliases;
  3. status of `adr-active.schema.json` as candidate vs canonical;
  4. reclassification/rename path for `adr.schema-implementation.json` as an implementation-record schema candidate;
  5. retention/archive/removal policy for `legacy-architecture.*.json` provenance markers;
  6. whether architecture-note / subsystem-architecture schemas should become a new schema family.

- For repo closeout, ask user whether to commit as one integrated closeout or split into bounded commits:
  1. workspace-state protocol acceptance/reconciliation plus role control-surface updates;
  2. Python policy validator CLI and bounded test-remediation chain;
  3. schema namespace governance/reconciliation if produced;
  4. optional Koios workspace control files after owner confirmation.

## Waiting on

- User direction for staging/commit boundaries.
- Koios only if the untracked Koios `state.md` and `active.md` should be owner-reviewed before inclusion.
- Vulcan only if the user requests remediation beyond the reported and validated slices.

## Active working material

- `state.md`
- `active.md`
- `docs/schemas/README.md`
- `docs/schemas/schema.record-base.json`
- `docs/schemas/adr-draft.schema.json`
- `docs/schemas/adr-active.schema.json`
- `docs/schemas/adr.schema-implementation.json`
- `docs/schemas/legacy-architecture.*.json`
- `docs/architecture/architecture.projectkoios.petrinet.md`
- `docs/templates/architecture.template.md`

## Ignored scope

- Product architecture decisions.
- New implementation work unless separately handed to Vulcan.
- Ad hoc schema file renames before an accepted reconciliation artifact exists.
- Broad ADR lifecycle refactors.
- GraphRAG/Python-policy dirty-file clusters unless explicitly included in repo closeout review.

## Exit criteria

Hermes state is stable when a new session can read `state.md` and `active.md`, identify the accepted workspace-state protocol, see that policy/bootstrap reconciliation and Python-policy/test-remediation are reported and spot-validated, and know that the next decision is how to stage/commit the reviewed slices.
