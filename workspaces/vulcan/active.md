```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "template-representation-schema-backed-roundtrip-validated",
  "datetime": "20260709.010748Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": [
    "docs/implementation/template-representation-roundtrip.20260708.044531.md",
    "docs/AAR/aar.20260708.044531_template-representation-roundtrip.md",
    "docs/schemas/template-record.schema.json"
  ],
  "scratch_directory": "scratch/",
  "source_brief": "docs/plans/implementation-brief.20260708.041245_template-representation-roundtrip.md",
  "revision_request": "docs/plans/revision-request.20260708.070651_template-representation-schema-backed.md"
}
```

# Vulcan active work

## Current priority stack

1. Request ATHENA conformance re-review for the schema-backed revision.
2. Package/commit/push the validated template representation schema-backed round-trip slice after review or explicit user direction.
3. Do not expand to broad template migration, CLI enforcement, or ingestion systems without a new brief.

## Latest working material

- Source brief: `docs/plans/implementation-brief.20260708.041245_template-representation-roundtrip.md`.
- Revision request: `docs/plans/revision-request.20260708.070651_template-representation-schema-backed.md`.
- Latest report: `docs/implementation/template-representation-roundtrip.20260708.044531.md`.
- Latest AAR: `docs/AAR/aar.20260708.044531_template-representation-roundtrip.md`.
- Schema: `docs/schemas/template-record.schema.json`.

## Latest validation evidence

- `uv run pytest tests/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/schema -q` => `34 passed in 0.16s`.
- `uv run mypy src/python/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/template_representation` => `Success: no issues found in 5 source files`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/template_representation` => `summary: 0 finding(s), 5 file(s)`.
- `git diff --check` => clean.
- `uv run pytest -q` => `243 passed in 1.30s`.
- `uv run mypy src/python tests` => `Success: no issues found in 123 source files`.
- `uv run projectkoios bootstrap validate-python-policy --all` => `summary: 0 finding(s), 123 file(s)`.

## Implementation notes

- New schema: `docs/schemas/template-record.schema.json`.
- New package: `src/python/projectkoios/bootstrap/template_representation/`.
- New tests: `tests/projectkoios/bootstrap/template_representation/`.
- First fixture: `docs/templates/ADR.proposal.template.md`.
- Round trip proven: controlled Markdown -> schema-backed record -> deterministic Markdown -> schema-backed record.

## Ignore for now

- Graphify ingestion daemon changes.
- Vault/PDF/source/evidence ingestion.
- `src/python/ingestion/`, `projectkoios.ingestion`, or generic ingestion framework.
- Product-facing template architecture.
- Broad migration of all templates.
- ADR lifecycle/status changes.

## Next expected artifact

- ATHENA schema-backed conformance review, commit/push instruction, or follow-up brief.
