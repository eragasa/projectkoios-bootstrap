# ATHENA intake 20260711.063019: `adr.json-schemas.draft.md` conformance slice

## Scope

Prepare review material while waiting for VULCAN's plan for a one-document active conformance slice.

Target source:

- `docs/adr/adr.json-schemas.draft.md`

Current schema:

- `docs/schemas/adr.schema.json`
- `routing` is not part of the schema.

## Source field inventory

### Schema-compatible fields present

- `title`: `JSON Schemas Namespace`
- `status`: `draft`
- `context`:
  - `origin`: `user request`
  - `from`: `HERMES`
  - `acting_as`: `user(Eugene)`
  - `scope`: `projectkoios-bootstrap`
  - `repository`: `projectkoios-bootstrap`
  - `delegated_operator`: `pi`
  - `architecture_domain`: `software`
- `decision`: present
- `consequences`: present
- `architecture_spec`: present
- `acceptance_criteria`: present as bullets
- `implementation_brief`: present, including `verification_method` prose
- `resolved_open_questions`: present as bullets
- `non_goals`: present as bullets
- `validation_expectations`: present as bullets
- `links.back_to`: `architecture.00`
- `links.supersedes`: source `None`, should normalize to JSON `null`
- `links.superseded_by`: source `None`, should normalize to JSON `null`

### Optional schema fields likely generated

- `id`: not explicitly present in source body; if produced, should be derived as `adr.json-schemas` or plan-approved equivalent.
- `slug`: not explicitly present in source body; if produced, should be `json-schemas` or plan-approved equivalent.
- `workflow_binding`: absent; do not add.

### Source-only fields to preserve outside schema record

These must not be silently dropped:

- source date: `20260702.213000Z`
- source status/date block formatting
- `routing.owner`: `Athena`
- `routing.next_phase`: `proposed`
- `routing.notes`: `JSON schema/contract surface for the UI/core family.`
- `links.related`: `[ADR 20260702.213000Z: Shared UI Core Namespace](adr.ui-core.draft.md)`

## Active-forward interpretation

- The conformed record should be treated as active going forward.
- Sidecar evidence preserves source/conversion provenance only.
- Do not frame the conformed record as historical-only or non-authoritative unless the user explicitly says so.

## Plan-review checklist for VULCAN

Accept the VULCAN plan only if it states:

1. Source `docs/adr/adr.json-schemas.draft.md` is not mutated without separate approval.
2. Output record validates against current `docs/schemas/adr.schema.json` with no `routing` property.
3. `routing.*` is preserved only in sidecar conversion evidence.
4. `links.related` is preserved only in sidecar conversion evidence unless schema is explicitly changed later.
5. `links.supersedes: None` and `links.superseded_by: None` normalize to JSON `null`, with normalization recorded.
6. `Acting-As: user(Eugene)` is copied exactly or any normalization is explicitly recorded as provenance.
7. `Architecture-Domain: software`, `Scope`, and `Repository` are copied without broadening.
8. Source path, source hash, source status, and source date are recorded.
9. Generated JSON hash and projection hash are recorded if those artifacts are produced.
10. Output artifact paths are target-specific or otherwise clearly separated from the prior one-ADR pilot.
11. Existing document/storage substrate is reused; no schema/lifecycle/workflow/storage-authority redesign is introduced.
12. No inference of acceptance, activation, supersession, implementation readiness, schema namespace architecture, UI/core boundary changes, or workflow state is made from conformance.
13. Pause triggers include any need to change `adr.schema.json`, expand `links`, reintroduce `routing`, or mutate source `docs/adr` files.

## Recommendation

Approve `docs/adr/adr.json-schemas.draft.md` as the next one-document active conformance target if VULCAN's plan satisfies the checklist above.
