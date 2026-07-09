# Architecture conformance review 20260709.011055: Template representation schema-backed revision

## Status

conforms

## Provenance

- Acting-As: ATHENA
- Repository: projectkoios-bootstrap
- Workspace: workspaces/athena/
- Requested by: VULCAN via intercom after schema-backed parser revision
- Source brief: `docs/plans/implementation-brief.20260708.041245_template-representation-roundtrip.md`
- Revision request: `docs/plans/revision-request.20260708.070651_template-representation-schema-backed.md`
- Prior review: `docs/reviews/architecture-conformance.20260708.052436_template-representation-roundtrip.md`
- Implementation report: `docs/implementation/template-representation-roundtrip.20260708.044531.md`
- Schema: `docs/schemas/template-record.schema.json`
- Implementation package: `src/python/projectkoios/bootstrap/template_representation/`
- Tests: `tests/projectkoios/bootstrap/template_representation/`

## Review scope

ATHENA reviewed the schema-backed revision against the user correction that template parsing must parse down to a schema-backed record. This review covers architecture/spec conformance only; VULCAN remains owner of implementation, tests, validation, implementation reports, and deviation reports.

This review also determines whether the schema-backed parser gate is satisfied for later draft skill integration. It does not itself implement or approve a stable skill.

## Inspected artifacts

- `docs/schemas/template-record.schema.json`
- `src/python/projectkoios/bootstrap/template_representation/models.py`
- `src/python/projectkoios/bootstrap/template_representation/markdown.py`
- `src/python/projectkoios/bootstrap/template_representation/paths.py`
- `src/python/projectkoios/bootstrap/template_representation/__init__.py`
- `tests/projectkoios/bootstrap/template_representation/test__TemplateRepresentation__roundtrip.py`
- `docs/implementation/template-representation-roundtrip.20260708.044531.md`

## Validation rerun by ATHENA

```bash
cd /Users/eugene/repos/projectkoios-bootstrap
uv run pytest tests/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/schema -q
# 34 passed in 0.15s

uv run mypy src/python/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/template_representation
# Success: no issues found in 5 source files

uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/template_representation
# summary: 0 finding(s), 5 file(s)

git diff --check
# clean
```

ATHENA also ran an interactive schema-backed round-trip inspection:

- `TemplateMarkdownParser.parse_file_schema_record()` produced a record with schema ID `https://projectkoios.local/schemas/template-record.schema.json`.
- `SchemaRegistry().validate("template-record.schema.json", record)` accepted the parsed record.
- Parsed content included the expected keys: `template_id`, `source_path`, `title`, `sections`, `markers`, `representation_version`, `preamble`, and `lead_body`.
- The live fixture produced 13 template sections.
- `TemplateMarkdownRenderer.render_schema_record()` produced Markdown byte-identical to `docs/templates/ADR.proposal.template.md`.
- Re-parsing the rendered Markdown through `parse_schema_record()` produced schema-validated content semantically equal to the first parsed content.
- Adding an extra controlled content field was rejected by JSON Schema validation.

ATHENA did not rerun the full VULCAN validation matrix, but the implementation report records full pytest, full mypy, full Python-policy validation, and diff hygiene as passing.

## Conformance findings

### 1. Canonical schema surface

Conforms.

`docs/schemas/template-record.schema.json` uses project-local schema ID `https://projectkoios.local/schemas/template-record.schema.json` and composes the existing `schema.record-base.json` envelope. Template-specific content constrains `template_id`, `source_path`, `title`, ordered `sections`, `markers`, `representation_version`, `preamble`, and `lead_body`.

The schema remains bootstrap-template-specific and does not define a generic Markdown ingestion model.

### 2. Parser output is schema-backed

Conforms.

The implementation adds `parse_file_schema_record()` and `parse_schema_record()` paths that convert parsed Markdown into a schema-backed record envelope and validate it through `SchemaRegistry`. Dataclasses remain as internal/convenience content models, but the schema-backed record path now exists and is tested.

### 3. Round-trip contract

Conforms.

The implementation proves:

```text
Markdown fixture
  -> schema-backed record
  -> SchemaRegistry validation
  -> deterministic Markdown render
  -> schema-backed record
  -> SchemaRegistry validation
  -> semantic equality
```

The live ADR proposal template render is byte-identical to the source fixture in ATHENA inspection.

### 4. Error distinction

Conforms for this slice.

Tests distinguish JSON Schema `ValidationError` from `TemplateMarkdownError`. Schema rejection for missing required content and additional content properties is covered.

### 5. Non-goals and authority boundary

Conforms.

ATHENA found no implementation evidence of:

- Graphify ingestion daemon changes;
- vault, PDF, source-crawling, or evidence ingestion;
- `src/python/ingestion/` or `projectkoios.ingestion` expansion;
- product-facing template architecture;
- all-template migration;
- ADR status or lifecycle authority changes.

The revision remains a bootstrap-local, one-fixture, schema-backed template representation slice.

## Blockers before packaging or commit

No architecture blockers identified for the schema-backed parser revision.

The earlier packaging blocker from `docs/plans/revision-request.20260708.070651_template-representation-schema-backed.md` is satisfied for the first fixture. Packaging may proceed after normal repo-state review, user-required commit approval, and any desired skill-draft integration.

## Residual risks

- The parser remains controlled bootstrap-template Markdown only, not arbitrary Markdown ingestion.
- The schema validates the first-slice template record shape; it does not imply every file in `docs/templates/` is migrated or validated.
- Placeholder detection remains deterministic angle-bracket matching for this slice.
- Direct `parse(markdown, source_path=...)` remains an internal controlled-string helper; schema-backed public use should prefer `parse_file_schema_record()` or `parse_schema_record()`.
- The planned `template-record-roundtrip` skill still needs implementation and should remain draft/gated until created and reviewed.

## Decision

ATHENA accepts the schema-backed parser revision as conformant to the revision request for the first-slice template representation round trip.

Recommended next state: VULCAN may proceed to draft/gated skill integration from `docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md`, or package the schema-backed parser slice if the user chooses to commit before skill integration.
