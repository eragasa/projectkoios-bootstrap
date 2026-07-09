```json
{
  "title": "Template record round-trip skill integration",
  "artifact_type": "implementation-report",
  "status": "validated-draft-skill",
  "datetime": "20260709.012011Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "source_brief": "docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md",
  "related_conformance_review": "docs/reviews/architecture-conformance.20260709.011055_template-representation-schema-backed.md",
  "scope": "draft/gated opencode skill for schema-backed bootstrap template record round trips",
  "validation_status": "pass"
}
```

# Template record round-trip skill integration

## Summary

Implemented the bounded draft/gated VULCAN skill integration requested by `docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md`.

The new skill instructs opencode/VULCAN agents to use the schema-backed `TemplateRecord` flow for bootstrap templates:

```text
bootstrap template Markdown
  -> schema-backed TemplateRecord instance
  -> JSON Schema validation through docs/schemas/template-record.schema.json
  -> deterministic Markdown render
  -> parse again
  -> JSON Schema validation again
  -> semantic equality check
```

The skill is explicitly marked draft/gated and does not claim stable reuse, packaging evidence, broad ingestion behavior, all-template migration, product-template architecture, or ADR lifecycle authority.

## Source artifacts

- Implementation brief: `docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md`
- Parser implementation report: `docs/implementation/template-representation-roundtrip.20260708.044531.md`
- Parser ATHENA conformance review: `docs/reviews/architecture-conformance.20260709.011055_template-representation-schema-backed.md`
- Schema: `docs/schemas/template-record.schema.json`

## Files changed

- Added `agents/global/opencode/skills/template-record-roundtrip/SKILL.md`
- Updated `docs/skills/skill-register.md`

## Implemented behavior

- Added skill frontmatter with `name: template-record-roundtrip`, `status: draft`, ADR bindings, opencode/VULCAN ownership metadata, inputs, and outputs.
- Added required skill sections:
  - `When to use this skill`
  - `Agent responsibility`
  - `Inputs`
  - `Procedure`
  - `Output artifact`
  - `Failure modes`
  - `Escalation rule`
- Added explicit prerequisite gate covering schema existence, `SchemaRegistry` load, focused validation tests, invalid schema rejection, parser/schema error distinction, VULCAN implementation report, and ATHENA conformance review.
- Required schema-backed entrypoints rather than Python-local dataclass-only parsing, specifically preferring `TemplateMarkdownParser.parse_file_schema_record()` or `TemplateMarkdownParser.parse_schema_record()`.
- Added failure modes requiring a deviation report if the flow cannot preserve metadata/content separation, validate against `template-record.schema.json`, stay within bootstrap-local boundaries, round-trip without semantic loss, or avoid implying all templates are migrated.
- Registered the skill in `docs/skills/skill-register.md` with draft/supporting status and matching ADR bindings.

## Explicit non-goals preserved

- No broad ingestion workflows.
- No Graphify ingestion behavior.
- No vault/source/PDF ingestion.
- No product-facing template architecture.
- No all-template migration.
- No runtime CLI integration.
- No ADR promotion or lifecycle status changes.
- No claim that the skill is stable before ATHENA reviews the skill draft itself.

## Validation

- `uv run pytest tests/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/schema -q` => `34 passed in 0.16s`.
- `uv run projectkoios bootstrap validate-python-policy agents/global/opencode/skills/template-record-roundtrip` => `summary: 0 finding(s), 0 file(s)`.
  - Note: Python policy validation found no Python files under the Markdown skill path; this is not treated as skill Markdown validation.
- Frontmatter/Markdown inspection script checked the skill file starts with YAML frontmatter and includes required identifiers/sections => `frontmatter/markdown inspection: ok`.
- `git diff --check` => clean.

## Deviations

None. The skill is draft/gated, opencode/VULCAN-owned, registered, and bounded to the schema-backed bootstrap template-record contract.

## Residual risks

- The skill draft still needs ATHENA review before it is treated as stable reusable practice.
- The underlying parser remains a controlled bootstrap-template Markdown parser, not arbitrary Markdown ingestion.
- The current schema-backed parser evidence covers the first fixture and does not imply all templates have been migrated or validated.
