```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.000000Z",
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

1. Review VULCAN's approval-gated one-ADR JSON/database pilot implementation plan.
2. Reconcile untracked `src/python/projectkoios/bootstrap/adr_records/` files against VULCAN's reported planning-only state.
3. Get user decision on staging/commit boundaries for the current dirty tree.
4. Keep broader schema namespace/record-family reconciliation as a separate Athena-owned planning item unless the user explicitly joins it to the pilot.

## Next action

- Ask user/Hermes to approve, revise, or stop `docs/plans/implementation-plan.20260711.033558_adr-json-database-one-adr-pilot.md`.
- Before approval or packaging, reconcile the untracked `src/python/projectkoios/bootstrap/adr_records/` directory because VULCAN's state says coding has not started.
- If plan is approved, hand off to VULCAN with this boundary:
  1. one representative source ADR only: `docs/adr/adr.json-database-for-adr-storage.draft.md`;
  2. no bulk migration, no mutable database authority, no overwrite of hand-authored source ADR without explicit approval;
  3. implementation must conform to the approved plan or produce a deviation report.

- For repo closeout, ask user whether to commit as one integrated closeout or split into bounded commits:
  1. ATHENA pilot brief and AAR;
  2. VULCAN implementation plan;
  3. architecture/meta-harness updates for architecture-led slicing and ADR storage topology;
  4. Athena/Vulcan/Koios/Hermes workspace control-surface updates as separate role-owned slices where needed;
  5. any separate schema namespace governance work only if produced later.

## Waiting on

- User direction for implementation-plan approval, revision, or stop.
- Reconciliation of untracked `src/python/projectkoios/bootstrap/adr_records/` against the planning-only gate.
- User direction for staging/commit boundaries.
- VULCAN coding only after the plan is approved.

## Active working material

- `state.md`
- `active.md`
- `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md`
- `docs/AAR/aar.20260709.014124_adr-json-database-pilot-brief.md`
- `docs/architecture/architecture.json-adr-storage-topology.md`
- `docs/architecture/architecture.workflows.00.md`
- `docs/meta-harness.md`
- `workspaces/athena/state.md`
- `workspaces/athena/active.md`
- `docs/plans/implementation-plan.20260711.033558_adr-json-database-one-adr-pilot.md`
- `workspaces/vulcan/state.md`
- `workspaces/vulcan/active.md`
- `workspaces/koios/state.md`
- `workspaces/koios/active.md`
- `workspaces/koios/working/provenance-note.20260711T033323Z_architecture-led-workflow-doctrine.md`
- `src/python/projectkoios/bootstrap/adr_records/`

## Ignored scope

- Product architecture decisions.
- New implementation work unless separately handed to Vulcan.
- Ad hoc schema file renames before an accepted reconciliation artifact exists.
- Broad ADR lifecycle refactors.
- GraphRAG/Python-policy dirty-file clusters unless explicitly included in repo closeout review.

## Exit criteria

Hermes state is stable when a new session can read `state.md` and `active.md`, identify that ATHENA produced the bounded one-ADR JSON/database pilot brief, VULCAN produced the approval-gated implementation plan, coding is not authorized, and the next decision is plan approval/revision plus commit boundary after reconciling untracked `adr_records` files.
