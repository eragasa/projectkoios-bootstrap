```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260705.003351",
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

1. Get user decision on staging/commit boundaries for the reviewed dirty tree.
2. If committing separately, stage workspace-state protocol reconciliation first and Python-policy/test-remediation second.
3. Decide whether untracked Koios workspace control files belong in the current closeout or require Koios review first.

## Next action

- Ask user whether to commit as one integrated closeout or split into bounded commits:
  1. workspace-state protocol acceptance/reconciliation plus role control-surface updates;
  2. Python policy validator CLI and bounded test-remediation chain;
  3. optional Koios workspace control files after owner confirmation.

## Waiting on

- User direction for staging/commit boundaries.
- Koios only if the untracked Koios `state.md` and `active.md` should be owner-reviewed before inclusion.
- Vulcan only if the user requests remediation beyond the reported and validated slices.

## Active working material

- `state.md`
- `active.md`
- `docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`
- `docs/implementation/implementation-report.20260705.003351_workspace-state-protocol-bootstrap-reconciliation.md`
- `docs/AAR/aar.20260705.003351_workspace-state-protocol-bootstrap-reconciliation.md`

## Ignored scope

- Product architecture decisions.
- New implementation work.
- Broad ADR lifecycle refactors.
- GraphRAG/schema/Python-policy dirty-file clusters unless explicitly included in repo closeout review.

## Exit criteria

Hermes state is stable when a new session can read `state.md` and `active.md`, identify the accepted workspace-state protocol, see that policy/bootstrap reconciliation and Python-policy/test-remediation are reported and spot-validated, and know that the next decision is how to stage/commit the reviewed slices.
