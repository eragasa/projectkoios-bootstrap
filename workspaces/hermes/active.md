```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.070500Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/hermes/",
  "document_domain": "orchestration, repo-state reconciliation, cross-domain consistency",
  "control_files": ["state.md", "active.md"],
  "next_owner": "ATHENA_OR_HERMES",
  "blockers": []
}
```

# Hermes active work

## Current priority stack

1. Wait for ATHENA review of `docs/implementation/json-schemas-adr-conformance.20260711.065704.md` and `dev/adr-json-schemas-conformance/`.
2. After ATHENA review, decide closeout/commit boundaries.
3. Keep scope constrained to current forward conformance work.

## Next action

ATHENA should review VULCAN's latest implementation evidence and confirm whether:

- the active conformed record framing is acceptable;
- `routing.*` and `links.related` sidecar preservation is sufficient;
- generated projection remains review evidence while JSON checkpoint is the active conformed artifact;
- architecture needs a small as-built update or no further edit.

## Waiting on

- ATHENA conformance/as-built review.
- User/Hermes closeout packaging direction after review.

## Active working material

- `docs/implementation/json-schemas-adr-conformance.20260711.065704.md`
- `docs/AAR/aar.20260711.065704_json-schemas-adr-conformance.md`
- `docs/plans/implementation-plan.20260711.062654_json-schemas-adr-conformance.md`
- `dev/adr-json-schemas-conformance/`
- `src/python/projectkoios/bootstrap/control_surface/adr/conformance.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/markdown.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py`
- `docs/architecture/architecture.json-adr-storage-topology.md`
- role workspace state files as needed for closeout.

## Out of scope now

- Backward compatibility support.
- Bulk ADR migration.
- Mutating source Markdown under `docs/adr/`.
- Database/storage-authority promotion.
- Reusable repository-level ADR storage config.
- Schema/lifecycle/workflow redesign without repeated concrete conformance pressure.

## Exit criteria

Hermes state is stable when ATHENA has reviewed the latest VULCAN report, any required architecture reconciliation is done, and the user/Hermes can choose commit boundaries from a clear current state.
