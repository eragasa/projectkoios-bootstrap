---
name: template-record-roundtrip
status: draft
adr_binding:
  - docs/adr/adr.templates.md
  - docs/adr/adr.schema-base.md
  - docs/adr/adr.skill-register-and-adr-binding-policy.draft.md
description: |
  Parse bootstrap template Markdown into schema-backed TemplateRecord data, validate it, render it back to Markdown, and prove round-trip equivalence.
  Bound to ADRs: adr.templates.md, adr.schema-base.md, adr.skill-register-and-adr-binding-policy.draft.md.
metadata:
  agent: code-agent
  harness_role: consumer-producer
  consumes:
    - template-document
    - schema
    - acceptance-criteria
  produces:
    - schema-backed-record
    - test-results
    - implementation-report
    - deviation-report
---
## Status

Draft/gated. This skill may be used for VULCAN validation work, but it MUST NOT be cited as stable reusable practice, completion evidence, or packaging evidence until the schema-backed parser revision has durable VULCAN implementation evidence and ATHENA conformance review, and until this skill draft itself is reviewed as needed.

Current parser gate references:

- VULCAN implementation report: `docs/implementation/template-representation-roundtrip.20260708.044531.md`
- ATHENA conformance review: `docs/reviews/architecture-conformance.20260709.011055_template-representation-schema-backed.md`

## When to use this skill

Use this skill when VULCAN/opencode must prove that a bootstrap template Markdown file can be represented as a schema-backed `TemplateRecord`, validated against `docs/schemas/template-record.schema.json`, rendered deterministically back to Markdown, parsed again, validated again, and compared for semantic equality.

This skill is for bootstrap template records under `docs/templates/`. It is not a generic Markdown ingestion workflow, a product-template contract, a Graphify/vault/source/PDF ingestion workflow, or evidence that every `docs/templates/` file has been migrated.

## Agent responsibility

VULCAN/opencode owns this procedure as an implementation and validation workflow. The agent must use the schema-backed record contract and must not stop at Python-local dataclasses or informal JSON-compatible dictionaries. The agent must preserve the bootstrap-local package boundary and report deviations instead of widening scope.

## Inputs

- `template-document` — a bootstrap template Markdown file, normally under `docs/templates/`
- `schema` — `docs/schemas/template-record.schema.json`
- `acceptance-criteria` — the controlling brief, review, or test obligation for the round-trip slice
- Existing implementation evidence and conformance review when the run is intended to support packaging or stable reuse

## Prerequisite gate

Before treating this skill as stable reusable practice, completion evidence, or packaging evidence, confirm all of the following are true:

- `docs/schemas/template-record.schema.json` exists.
- The schema loads through `SchemaRegistry` or an equivalent offline local registry.
- Focused tests demonstrate Markdown -> schema-backed record validation.
- Focused tests demonstrate schema-backed record -> Markdown -> schema-backed record semantic equality.
- Invalid schema instances fail validation.
- Parser errors and schema validation errors are distinguishable.
- A VULCAN implementation report records schema-backed validation.
- An ATHENA conformance review accepts the schema-backed parser revision.

If any prerequisite is not met, use this skill only for draft/validation work and do not cite it as completion evidence.

## Procedure

1. Confirm the source template is under `docs/templates/`, unless explicitly using a test fixture.
2. Confirm `docs/schemas/template-record.schema.json` exists and loads through the canonical schema registry.
3. Confirm the current implementation has a VULCAN report and ATHENA conformance review for the schema-backed parser revision; if not, mark the run as draft/validation-only.
4. Parse Markdown into the schema-backed `TemplateRecord` instance, not merely a Python-local object. Prefer public schema-backed entrypoints such as `TemplateMarkdownParser.parse_file_schema_record()` or `TemplateMarkdownParser.parse_schema_record()`.
5. Validate the parsed record against `template-record.schema.json` using `SchemaRegistry` or an equivalent offline local registry.
6. Render deterministic Markdown from the schema-backed record, for example through `TemplateMarkdownRenderer.render_schema_record()`.
7. Parse the rendered Markdown back into a schema-backed record.
8. Validate the second record against the schema.
9. Compare semantic equality of the schema-backed records.
10. Confirm the skill is not being used as a generic Markdown ingestion workflow, a product-template workflow, broad template migration, or completion evidence for untested templates.
11. Run focused validation, normally:

    ```bash
    uv run pytest tests/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/schema -q
    git diff --check
    ```

    If repository files changed, also run an appropriate policy/frontmatter/Markdown inspection. If `projectkoios bootstrap validate-python-policy` is not applicable to Markdown skill files, record that as not applicable rather than fabricating a pass.

12. Produce or update an implementation report when repository files change. Produce a deviation report if the schema-backed contract cannot be satisfied inside the authorized boundary.

## Output artifact

- `schema-backed-record` — the validated TemplateRecord schema instance
- `test-results` — validation output for schema loading, parse/render/parse equivalence, invalid schema rejection, and error distinction
- `implementation-report` — summary of repository changes and validation when this skill changes files or implements a slice
- `deviation-report` — required if the authorized schema-backed template-record contract cannot be met

## Failure modes

Stop and produce a deviation report if:

- The parser cannot preserve metadata/content separation.
- The record cannot validate against `template-record.schema.json`.
- The schema and implementation disagree about required fields or object boundaries.
- The flow requires broad ingestion, product template semantics, or non-bootstrap package layout.
- The template fixture cannot round-trip without semantic loss.
- Schema-backed validation is inferred from file presence instead of demonstrated by tests and reports.
- The skill would imply all `docs/templates/` files are validated or migrated when only one fixture is covered.

## Escalation rule

Escalate to ATHENA with a deviation report for architecture or contract ambiguity. Escalate to the user before expanding scope beyond the bootstrap-local template-record round-trip procedure. Do not promote this skill from draft or use it as stable completion evidence without the required validation and conformance evidence.
