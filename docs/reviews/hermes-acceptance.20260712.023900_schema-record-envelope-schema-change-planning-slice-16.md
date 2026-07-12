```json
{
  "title": "HERMES acceptance: Schema record-envelope schema-change planning slice 16",
  "artifact_type": "workflow-acceptance",
  "status": "accepted-proposal-only",
  "datetime": "20260712.023900Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "schema-record-envelope-schema-change-planning-slice-16",
  "accepted_artifact": "docs/plans/schema-change-brief.20260712.023116_schema-record-envelope.md",
  "source_decision": "docs/reviews/hermes-decision.20260712.023116_schema-record-envelope-schema-change-planning-slice-16.md",
  "athena_author": "subagent-chat-019f5213",
  "koios_review": "subagent-chat-019f51a8 intercom reply 20260712",
  "vulcan_review": "subagent-chat-019f527d intercom reply 20260712",
  "authority_change": false,
  "schema_mutation": false,
  "source_mutation": false,
  "next_owner": "HERMES_USER"
}
```

# HERMES acceptance 20260712.023900: Schema record-envelope schema-change planning slice 16

## Decision

HERMES accepts ATHENA's Slice 16 schema-change planning brief as proposal-only planning:

```text
docs/plans/schema-change-brief.20260712.023116_schema-record-envelope.md
```

## Accepted recommendation

The accepted planning recommendation is to keep:

```text
docs/schemas/schema.record-base.json
```

unchanged as draft record-envelope direction for now, and defer substantive schema changes until renderer/ingester, family-schema composition, or migration needs become concrete.

If HERMES/USER later chooses a minimal schema-edit slice, the bounded candidate is a reference/description/comment-only edit that links `docs/architecture/architecture.schema-record-envelope.md` while preserving validation semantics.

## Review basis

ATHENA reported:

- no mutation to `docs/adr/`, `docs/schemas/`, or `dev/adr-json-authority-corpus-dry-run-inventory-slice-4`;
- only the new planning brief appeared on its scoped plan path;
- `git diff --check` passed.

HERMES independently observed:

```text
?? docs/plans/schema-change-brief.20260712.023116_schema-record-envelope.md
```

on the scoped surfaces, with no `docs/adr/`, `docs/schemas/`, or Slice 4 dry-run evidence mutation, and `git diff --check` passed.

KOIOS provenance review reported the brief provenance-adequate for HERMES proposal-only acceptance, with no blockers.

VULCAN implementation-reality comments reported no blockers for accepting the proposal-only Option A/F path. VULCAN found keeping `docs/schemas/schema.record-base.json` unchanged implementation-safe because it preserves current validator behavior and avoids accidental migration/cutover work. VULCAN identified the main unchanged-schema risk as operator/agent authority confusion rather than code breakage.

VULCAN watchpoints integrated into this acceptance:

- Do not ask implementation agents to validate new records against `schema.record-base.json` unless the task explicitly says draft-envelope validation.
- If a future minimal reference/comment edit is selected, prefer tooling-neutral `$comment` for draft-boundary notes; `description` is more discoverable but more likely to be read as user-facing authority.
- Avoid normative language such as "must use" or "canonical" in any future draft-boundary annotation.
- Treat any change to `required`, `additionalProperties`, `$defs`, enum values, timestamp pattern, `$id`, `$ref` behavior, or other validation-affecting keywords as semantic and out of scope for a reference/comment-only slice.

## Boundaries preserved

This acceptance does not approve any schema JSON edit.

This acceptance does not edit `docs/schemas/`, edit `docs/adr/`, change lifecycle state, accept machine-readable schema authority, make `metadata` + `content` current universal emitted-record authority, generate projections, create authoritative JSON records, add database/storage authority, implement renderer/ingester behavior, migrate records, or cut over JSON authority.

`docs/schemas/schema.record-base.json` remains draft direction. `docs/schemas/adr.schema.json` remains current ADR content-shape schema until a later approved replacement, wrapping, or retirement decision.

## Follow-up options

HERMES/USER may next choose one of these bounded paths:

1. Stop the ADR/schema planning track here and leave `schema.record-base.json` unchanged until implementation or migration pressure appears.
2. Activate a minimal future schema-edit slice, tentatively `schema-record-envelope-reference-comment-slice-17`, limited to non-semantic reference/description/comment changes in `docs/schemas/schema.record-base.json`. Required closeout should include JSON parse validity, any available JSON Schema self-check, confirmation that validation semantics are unchanged for key schema keywords or representative valid/invalid examples, a check that the architecture reference and draft-boundary phrase exist, and `git diff --check`.
3. Defer substantive schema reconciliation until field-level authority mapping, validation-behavior expectations, tests, and compatibility risks are available. Substantive reconciliation should include concrete valid/invalid fixture records, projection/status/source/evidence enum coverage, timestamp accepted/rejected cases, ADR-family composition checks, and local schema-registry resolution tests before relying on composition.

## Workflow state change

HERMES clears active queue item:

```text
schema-record-envelope-schema-change-planning-slice-16
```

and reconciles the static workflow fixture to `active_slice=none` pending HERMES/USER next decision.
