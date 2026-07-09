# Implementation brief 20260709.010343: Template record round-trip skill integration

## Status

Implementation-ready draft for VULCAN review/execution after user approval; skill MUST remain draft/gated until schema-backed parser validation has durable VULCAN report and ATHENA conformance evidence.

## Provenance

- Acting-As: ATHENA
- Repository: projectkoios-bootstrap
- Workspace: workspaces/athena/
- User direction: integrate the schema-backed template parser/round-trip flow into a skill.
- Related brief: `docs/plans/implementation-brief.20260708.041245_template-representation-roundtrip.md`
- Related revision request: `docs/plans/revision-request.20260708.070651_template-representation-schema-backed.md`
- Related conformance review: `docs/reviews/architecture-conformance.20260708.052436_template-representation-roundtrip.md`
- Schema namespace: `docs/schemas/`
- Skill register: `docs/skills/skill-register.md`
- Skill template: `docs/templates/skill.template.md`
- KOIOS comments: intercom response from `subagent-chat-019f321e`, received after ATHENA request for provenance/process review.

## Authority boundary

This brief authorizes a narrowly scoped VULCAN implementation/configuration slice: add a reusable skill that instructs VULCAN/opencode how to perform schema-backed bootstrap template record round trips.

This brief does not authorize broad ingestion, product-facing template architecture, Graphify/vault/source/PDF ingestion, all-template migration, or changes to ADR lifecycle authority.

If the current schema-backed parser revision is not yet implemented or validated, the skill MUST describe the intended gate and MUST remain draft until the implementation and schema validation pass.

The skill MUST NOT present itself as stable reusable practice, completion evidence, or packaging evidence until a VULCAN implementation report and ATHENA conformance review explicitly cover the schema-backed parser revision.

## Objective

Create and register a reusable VULCAN skill for this repeatable transition:

```text
bootstrap template Markdown
  -> schema-backed TemplateRecord instance
  -> JSON Schema validation through docs/schemas/template-record.schema.json
  -> deterministic Markdown render
  -> parse again
  -> JSON Schema validation again
  -> semantic equality check
```

The skill should make future agents use the schema-backed contract instead of stopping at Python-local dataclasses or informal JSON-compatible dictionaries.

The skill must also prevent future agents from overgeneralizing this slice: it is a reusable VULCAN procedure for bootstrap template records, not a generic Markdown ingestion skill, all-template migration, or product template contract.

## Required skill file

Add a skill at:

```text
agents/global/opencode/skills/template-record-roundtrip/SKILL.md
```

Recommended frontmatter:

```yaml
---
name: template-record-roundtrip
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
```

VULCAN may refine artifact names if they match current repo vocabulary better, but the skill MUST remain VULCAN/opencode-owned.

The skill frontmatter and body MUST make the skill status visibly `draft` or gated while schema-backed parser validation is still pending.

## Required skill content

The skill MUST include these sections:

1. `## When to use this skill`
2. `## Agent responsibility`
3. `## Inputs`
4. `## Procedure`
5. `## Output artifact`
6. `## Failure modes`
7. `## Escalation rule`

### Required prerequisite/gate content

The skill MUST include an explicit prerequisite gate before its procedure:

- `docs/schemas/template-record.schema.json` exists;
- the schema loads through `SchemaRegistry` or an equivalent offline local registry;
- focused tests demonstrate Markdown → schema-backed record validation;
- focused tests demonstrate schema-backed record → Markdown → schema-backed record semantic equality;
- invalid schema instances fail validation;
- parser errors and schema validation errors are distinguishable;
- a VULCAN implementation report records schema-backed validation;
- an ATHENA conformance review accepts the schema-backed parser revision before the skill is treated as stable or packaging evidence.

If those prerequisites are not all met, the skill may be used only for draft/validation work and MUST NOT be cited as completion evidence.

### Required procedure content

The procedure MUST instruct the agent to:

1. Confirm the source template is under `docs/templates/` unless explicitly using a test fixture.
2. Confirm `docs/schemas/template-record.schema.json` exists and loads through the canonical schema registry.
3. Confirm the current implementation has a VULCAN report and ATHENA conformance review for the schema-backed parser revision; if not, mark the run as draft/validation-only.
4. Parse Markdown into the schema-backed TemplateRecord instance, not merely a Python-local object.
5. Validate the parsed record against `template-record.schema.json` using `SchemaRegistry` or an equivalent offline local registry.
6. Render deterministic Markdown from the schema-backed record.
7. Parse the rendered Markdown back into a schema-backed record.
8. Validate the second record against the schema.
9. Compare semantic equality of the schema-backed records.
10. Confirm the skill is not being used as a generic Markdown ingestion or product-template workflow.
11. Run focused tests and policy validation.
12. Produce an implementation report or deviation report when repository files change.

### Required failure modes

The skill MUST say to stop and produce a deviation report if:

- the parser cannot preserve metadata/content separation;
- the record cannot validate against `template-record.schema.json`;
- schema and implementation disagree about required fields or object boundaries;
- the flow requires broad ingestion, product template semantics, or non-bootstrap package layout;
- the template fixture cannot round-trip without semantic loss;
- schema-backed validation is inferred from file presence instead of demonstrated by tests/reports;
- the skill would imply all `docs/templates/` files are validated or migrated when only one fixture is covered.

## Skill register update

Update `docs/skills/skill-register.md` with a row for the new skill.

Recommended row values:

| Field | Value |
|---|---|
| Skill | `template-record-roundtrip` |
| Canonical path | `agents/global/opencode/skills/template-record-roundtrip/SKILL.md` |
| Owning harness | `opencode` |
| Purpose | `Parse bootstrap templates into schema-backed TemplateRecord data and prove Markdown/schema round-trip equivalence` |
| Bound ADRs | `adr.templates.md, adr.schema-base.md, adr.skill-register-and-adr-binding-policy.draft.md` |
| Binding mode | `supporting` |
| Status | `draft` |
| Binding note | `Draft/gated VULCAN procedure for template-record validation against the schema-backed representation contract; not stable until schema-backed parser report and ATHENA conformance review exist` |

## Test and validation expectations

Before marking the skill stable or using it as completion evidence, VULCAN MUST produce or update an implementation report explicitly covering:

- `docs/schemas/template-record.schema.json` loading through `SchemaRegistry`;
- Markdown → schema-backed record validation;
- schema-backed record → Markdown → schema-backed record semantic equality;
- invalid schema instance failures;
- parser error vs schema validation error distinction.

VULCAN should validate at minimum:

```bash
uv run pytest tests/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/schema -q
uv run projectkoios bootstrap validate-python-policy agents/global/opencode/skills/template-record-roundtrip
```

If the Python policy validator is not intended for Markdown skill files, record that as not applicable and run an appropriate syntax/frontmatter inspection instead.

Also run:

```bash
git diff --check
```

## Non-goals

Do not add in this skill slice:

- broad ingestion workflows;
- Graphify ingestion behavior;
- vault/source/PDF ingestion;
- product-facing template architecture;
- all-template migration;
- runtime CLI integration unless separately authorized;
- ADR promotion or lifecycle status changes.

## Expected output artifacts

- `agents/global/opencode/skills/template-record-roundtrip/SKILL.md`
- updated `docs/skills/skill-register.md`
- implementation report or AAR if VULCAN changes repository skill/config surfaces
- VULCAN implementation report for the schema-backed parser revision, or an update to the existing implementation report if that is the repo convention
- ATHENA conformance review of the schema-backed parser revision and skill draft before the skill is treated as stable
- deviation report if the schema-backed contract is not ready enough for a usable skill

## Ready-to-implement condition

This skill can be drafted now, but must not be considered stable until the schema-backed parser revision validates and has durable VULCAN report plus ATHENA conformance evidence. If VULCAN implements the skill before the parser revision completes, mark the skill status as `draft`, explicitly state that it depends on the schema-backed parser gate, and do not use the skill as packaging/completion evidence.
