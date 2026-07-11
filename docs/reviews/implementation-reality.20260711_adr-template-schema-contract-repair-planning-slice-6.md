```json
{
  "title": "Implementation reality check: ADR template/schema contract repair planning slice 6",
  "artifact_type": "implementation-reality-check",
  "status": "complete-read-only-input-to-hermes",
  "datetime": "20260711",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-template-schema-contract-repair-planning-slice-6",
  "target_source": "docs/adr/adr.adr-template-contract.md",
  "requested_by": "HERMES",
  "source_repair_plan": "docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md"
}
```

# Implementation reality check: ADR template/schema contract repair planning slice 6

## Summary verdict

VULCAN implementation reality supports the Slice 6 repair plan's recommendation: do **not** revise `docs/adr/adr.adr-template-contract.md` in place as the first repair action. The safest implementation-constrained next step is a future explicitly approved successor proposal that separates current schema/tooling reality from target JSON-authority aspirations.

Current code/schema/tooling treats `routing` and some source sections as sidecar/provenance, does not implement `dcn`, only schemas `workflow_binding` without operational use, and treats generated Markdown as non-authoritative projection/evidence rather than source replacement.

## Findings by HERMES question

### Does current code/schema/tooling rely on or implement `routing`?

Implementation reality: **routing is not current ADR content-schema data; code preserves it outside records when encountered.**

Evidence:

- `docs/schemas/adr.schema.json` has no top-level `routing` property and `additionalProperties: false`.
- `AdrMarkdownRecordParser.parse_source_record()` builds records with `title`, `status`, `context`, `decision`, `consequences`, `architecture_spec`, `acceptance_criteria`, `implementation_brief`, `resolved_open_questions`, `non_goals`, `validation_expectations`, and `links`; it does not put `routing` into the record.
- `AdrMarkdownRecordParser.source_mapping_notes()` explicitly preserves `routing_section` and parsed `routing` under `preserved_outside_schema`.
- `AdrConformanceRunner` records `routing_allowed: false`, `routing_absent_from_record`, and `omitted_from_record` entries for `routing.owner`, `routing.next_phase`, and `routing.notes`.
- Tests assert `routing` is not in conformed records/checkpoints/projection records and is preserved in sidecar/conversion evidence.
- The document-store table is generic (`document_id`, `document_kind`, `content_hash`, `payload_json`, timestamps); tests assert `routing_next_phase` is not a storage column.

Constraint for successor planning:

- Do not list `routing` as current `docs/schemas/adr.schema.json` content unless a later schema-change slice explicitly adds it.
- If retained, it should be framed as sidecar/envelope/provenance/workflow metadata or intentionally excluded legacy source material.

### Does current code/schema/tooling rely on or implement `dcn`?

Implementation reality: **no current Python ADR conversion/storage/schema tooling implements `dcn`.**

Evidence:

- Target source and `docs/adr/adr.adr.md` mention `dcn`, but `docs/schemas/adr.schema.json` has no `dcn` property and requires no `dcn` field.
- `rg` over `src/python`, `tests`, and `docs/schemas` found no `dcn` implementation or tests.
- Current parser/model/storage code uses `id` and `slug` as candidate/canonical identities, not `dcn`.

Constraint for successor planning:

- Treat `dcn` as unresolved namespace/control metadata unless a later approved schema/envelope decision adds it.
- Do not silently add `dcn` to schema or remove it from namespace guidance as part of template repair.

### Does current code/schema/tooling implement/use `workflow_binding`?

Implementation reality: **schema supports optional `workflow_binding`; current Python ADR conversion/control-surface code does not operationally use it.**

Evidence:

- `docs/schemas/adr.schema.json` defines `$defs.WorkflowBinding` and an optional top-level `workflow_binding` property.
- Target source mentions optional `workflow_binding` as a documentation/rendering extension.
- `rg` over `src/python` and `tests` found no operational parser, renderer, storage, or validator behavior specific to `workflow_binding` beyond generic schema validation potential.

Constraint for successor planning:

- It is safe to say `workflow_binding` is schema-supported as optional content, but not safe to imply workflow runtime/control-surface implementation depends on it.
- Successor should preserve the boundary that `workflow_binding` is optional schema content or an extension point, not current lifecycle/workflow authority.

### Does current ADR conversion/control-surface code treat Markdown as source authority vs generated projection/evidence?

Implementation reality: **current tooling treats hand-authored Markdown as source input/evidence and generated Markdown as projection evidence only, not authoritative replacement.**

Evidence:

- `AdrMarkdownRecordParser` docstring says it is intentionally narrow, reads pilot source ADR Markdown, reads generated projection embedded JSON, and is not a general ADR Markdown importer.
- Pilot/conformance/bidirectional runners read source Markdown, write JSON checkpoints/evidence under `dev/`, and generate projections under `dev/`; they do not overwrite source Markdown.
- Bidirectional/conformance evidence marks projections as generated/non-authoritative and parse-back scope as generated projection only.
- Slice 3 and Slice 4 runners explicitly mark projections as generated evidence only, parse generated projection JSON only, and preserve source-to-candidate incompleteness in sidecars/lossiness evidence.
- Existing no-mutation tests verify source Markdown is byte-for-byte unchanged in relevant runs.

Constraint for successor planning:

- A successor should not state that Markdown is already universally derived from JSON in the current repository state.
- More accurate current wording: Markdown remains source/control material for unmigrated records; generated Markdown projections are evidence artifacts under `dev/` unless and until a future authority cutover is explicitly accepted.

## Additional implementation constraints for successor template/schema proposal

- Current `docs/schemas/adr.schema.json` is a content-shape schema, not a full storage/envelope schema. It has optional `id`, `slug`, `links`, `workflow_binding`; required core fields are `title`, `status`, `context`, `decision`, `consequences`, `architecture_spec`, `acceptance_criteria`, `implementation_brief`, `resolved_open_questions`, `non_goals`, and `validation_expectations`.
- The schema enum uses lowercase statuses: `proposal`, `draft`, `accepted`, `active`, `superseded`. The target source's observed `Accepted` casing remains noncanonical for current schema validation and should be preserved as source observation, not silently normalized.
- Current sidecar/envelope evidence has repeatedly preserved unsupported source fields (`routing`, related links, source date, filename status suffix, omitted sections) outside content. A successor should decide whether those belong in content schema, envelope metadata, sidecar/provenance, or legacy-only material.
- Current JSON authority work is staged and evidence-oriented. Do not let a successor proposal imply that generated `dev/` JSON/projections are durable authority.

## VULCAN recommendation to HERMES

VULCAN recommends HERMES keep the Slice 6 acceptance/packaging watchpoints and, before any successor proposal slice executes, require the successor brief to explicitly distinguish:

1. current ADR content schema fields versus future envelope/sidecar metadata;
2. `routing` as currently sidecar/provenance, not schema content;
3. `dcn` as unresolved namespace/control metadata, not implemented schema/tooling field;
4. optional `workflow_binding` as schema-supported but not operational workflow authority;
5. Markdown source/control for unmigrated records versus generated projection evidence;
6. observed source status `Accepted` versus schema-valid `accepted`.

## Read-only validation

VULCAN performed a read-only implementation check using source inspection and search. No code, schema, ADR source, evidence, or plan file was changed by this check except this implementation-reality review artifact.

Observed closeout commands:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Both produced no output / passed at the time of this check.
