# Revision request 20260708.070651: Template representation must parse to a schema-backed record

## Status

implementation-revision-required

## Provenance

- Acting-As: ATHENA
- Repository: projectkoios-bootstrap
- Workspace: workspaces/athena/
- Source brief: `docs/plans/implementation-brief.20260708.041245_template-representation-roundtrip.md`
- Prior conformance review: `docs/reviews/architecture-conformance.20260708.052436_template-representation-roundtrip.md`
- User correction: implementation must parse down to a schema.
- Existing schema precedent: `docs/schemas/schema.record-base.json`, `docs/schemas/adr-draft.schema.json`, `src/python/projectkoios/bootstrap/schema/`

## Correction

The first-slice implementation is not complete for packaging if the intended contract is schema-backed parsing. The current VULCAN implementation parses Markdown into local `TemplateRecord` dataclasses and JSON-compatible dictionaries, but it does not define or validate a canonical JSON Schema for template records.

The next implementation revision MUST make the template representation parse down to a schema-backed record, not only a Python-local model.

## Required architecture boundary

This revision remains bootstrap-local and template-specific. It still MUST NOT create broad ingestion, Graphify ingestion, vault/source/PDF ingestion, product-facing template architecture, or a top-level `projectkoios.ingestion` package.

## Required schema surface

VULCAN should add a canonical schema under `docs/schemas/`, recommended name:

```text
docs/schemas/template-record.schema.json
```

The schema MUST use the project-local `$id` convention:

```text
https://projectkoios.local/schemas/template-record.schema.json
```

The schema SHOULD follow the existing schema-record direction where practical:

- top-level `metadata` and `content` envelope if the template record is treated as a durable schema-backed Project Koios record;
- family-specific `content` constraints for template title, preamble, lead body, ordered sections, and markers;
- explicit `schema_id`, `schema_version`, `record_version`, source path, and representation version fields;
- `additionalProperties: false` at controlled object boundaries unless a field is intentionally extensible.

If VULCAN finds the base envelope incompatible with this first template representation slice, stop and produce a deviation report rather than inventing a conflicting schema style.

## Required parser behavior

The parser MUST produce a schema instance from `docs/templates/ADR.proposal.template.md` that validates against the new canonical schema.

The implementation MAY keep dataclasses as internal convenience objects, but the authoritative parsed output for the slice MUST be the schema-backed dictionary/JSON instance.

Required behavior:

1. Markdown fixture parses into a schema-backed record instance.
2. The schema-backed record validates offline through `SchemaRegistry` or an equivalent local registry using `docs/schemas/`.
3. Rendering from the schema-backed record remains deterministic.
4. Schema-backed record → Markdown → schema-backed record round trip preserves semantic equality.
5. Invalid schema instances fail JSON Schema validation with inspectable errors.
6. Parser errors and schema validation errors remain distinguishable.

## Required tests

Add or revise tests to prove:

- `docs/schemas/template-record.schema.json` loads through the canonical schema registry.
- A parsed `ADR.proposal.template.md` record validates against `template-record.schema.json`.
- The schema rejects missing required metadata/content fields.
- The schema rejects additional properties at controlled boundaries.
- Schema-backed JSON serialization/deserialization round trips.
- Markdown → schema-backed record → Markdown → schema-backed record preserves semantic equality.
- Namespace classification boundaries still hold.

## Validation expectations

At minimum, VULCAN should run:

```bash
uv run pytest tests/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/schema -q
uv run mypy src/python/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/template_representation
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/template_representation
git diff --check
```

If schema registry code changes, include the affected schema tests and full relevant validation in the implementation report.

## Packaging status

Packaging/commit SHOULD pause until this schema-backed revision is implemented or the user explicitly downgrades the requirement back to Python-local JSON-compatible records.
