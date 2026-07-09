```json
{
  "title": "Template representation schema-backed round-trip first slice",
  "artifact_type": "implementation-report",
  "status": "validated",
  "datetime": "20260709.010748Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "source_brief": "docs/plans/implementation-brief.20260708.041245_template-representation-roundtrip.md",
  "revision_request": "docs/plans/revision-request.20260708.070651_template-representation-schema-backed.md",
  "schema": "docs/schemas/template-record.schema.json",
  "scope": "bootstrap template representation one-fixture schema-backed Markdown/JSON round trip",
  "validation_status": "pass"
}
```

# Template representation schema-backed round-trip first slice

## Summary

Implemented the approved bootstrap template representation round trip and the ATHENA schema-backed revision request.

The slice now proves one controlled fixture can be parsed into a schema-backed TemplateRecord instance, validated offline through `SchemaRegistry`, rendered to deterministic Markdown, parsed back into a schema-backed record, validated again, and compared semantically.

## Source artifacts

- Implementation brief: `docs/plans/implementation-brief.20260708.041245_template-representation-roundtrip.md`
- Revision request: `docs/plans/revision-request.20260708.070651_template-representation-schema-backed.md`
- Schema: `docs/schemas/template-record.schema.json`

## Files changed

- `docs/schemas/template-record.schema.json`
- `src/python/projectkoios/bootstrap/template_representation/__init__.py`
- `src/python/projectkoios/bootstrap/template_representation/models.py`
- `src/python/projectkoios/bootstrap/template_representation/markdown.py`
- `src/python/projectkoios/bootstrap/template_representation/paths.py`
- `tests/projectkoios/bootstrap/template_representation/test__TemplateRepresentation__roundtrip.py`

## Implemented behavior

- Canonical `TemplateRecord`, `TemplateSection`, and `TemplateMarker` DataObjects.
- Schema-backed record envelope using project-local schema ID `https://projectkoios.local/schemas/template-record.schema.json`.
- JSON Schema validation through existing `SchemaRegistry` / `docs/schemas/` registry behavior.
- Controlled Markdown parser for bootstrap template Markdown.
- Deterministic Markdown renderer for parsed template records and schema-backed records.
- Minimal namespace classifier for `docs/templates/`, `docs/implementation/`, and `docs/plans/`.
- First fixture support for `docs/templates/ADR.proposal.template.md`.
- Typed parse errors via `TemplateMarkdownError`, distinct from JSON Schema `ValidationError` failures.

## Tests added

- Schema registry loads `template-record.schema.json`.
- Parsed `docs/templates/ADR.proposal.template.md` validates as a schema-backed record.
- Schema rejects missing required template content fields.
- Schema rejects additional content properties at controlled boundaries.
- JSON-compatible serialization/deserialization round trip.
- Schema-backed record -> Markdown -> schema-backed record semantic round trip.
- Presentation-only whitespace variance normalization.
- Typed parse failures for missing required title and ambiguous heading hierarchy.
- Namespace classification for templates, implementation docs, and plans.
- Rejection of non-template source paths by default.

## Explicit non-goals preserved

- No Graphify ingestion daemon changes.
- No vault, PDF, source crawling, or evidence ingestion.
- No `src/python/ingestion/`, `projectkoios.ingestion`, or generic ingestion framework.
- No product-facing template architecture.
- No broad migration of all templates.
- No ADR status or lifecycle authority changes.

## Validation

- `uv run pytest tests/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/schema -q` => `34 passed in 0.16s`.
- `uv run mypy src/python/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/template_representation` => `Success: no issues found in 5 source files`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/template_representation` => `summary: 0 finding(s), 5 file(s)`.
- `git diff --check` => clean.
- `uv run pytest -q` => `243 passed in 1.30s`.
- `uv run mypy src/python tests` => `Success: no issues found in 123 source files`.
- `uv run projectkoios bootstrap validate-python-policy --all` => `summary: 0 finding(s), 123 file(s)`.
- Prior `graphify update /Users/eugene/repos/projectkoios-bootstrap` for this slice rebuilt graph with `8352 nodes, 9435 edges, 779 communities`.

## Deviations

None. The implementation uses the preferred package boundary, test boundary, recommended fixture, and requested schema-backed record validation.

## Residual risks

- The parser supports controlled bootstrap template Markdown, not arbitrary Markdown ingestion.
- Placeholder detection is intentionally first-slice deterministic angle-bracket marker detection.
- This slice validates one fixture and does not claim enforcement or migration readiness for every file in `docs/templates/`.
- Direct `parse(markdown, source_path=...)` remains an internal controlled-string helper; `parse_file()` enforces namespace before reading files.
