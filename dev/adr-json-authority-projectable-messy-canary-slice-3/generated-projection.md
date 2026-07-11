<!-- GENERATED SLICE 3 PROJECTION EVIDENCE: non-authoritative; do not use as ADR source. -->
# ADR Projection Evidence: Canonical ADR proposal template

## Projection metadata

- Slice name: adr-json-authority-projectable-messy-canary-slice-3
- Evidence path: dev/adr-json-authority-projectable-messy-canary-slice-3/generated-projection.md
- Source path: docs/adr/adr.adr-template-contract.md
- Source hash: 2876dfbe031105d383fa9e33cec7d5dd49cf569cea6f43eae59e8fa1da502895
- Authority mode: candidate evidence only; not repository authority
- Source mutation: false
- Schema change: false
- Database authority: false
- Reviewed category: template_schema_contract
- Reviewed disposition: manual_review_required
- Observed status text: Accepted
- Normalized status candidate: accepted
- Normalization requires review: true

```json adr-record
{
  "acceptance_criteria": [
    "New ADRs can be represented as JSON without losing any required data.",
    "The schema includes provenance, routing, the `dcn` field, and optional workflow-binding fields.- The schema enforces one architecture domain per ADR.",
    "Workflow-bound ADRs can render optional gate fields without losing schema consistency.",
    "A renderer can produce Markdown from the JSON object."
  ],
  "architecture_spec": "The canonical ADR JSON schema contains:\n\n- `dcn`\n- `id`\n- `slug`\n- `title`\n- `status`\n- `context`\n- `decision`\n- `consequences`\n- `architecture_spec`\n- `acceptance_criteria`\n- `implementation_brief`\n- `resolved_open_questions`\n- `non_goals`\n- `validation_expectations`\n- `routing`\n- `links`\n- optional `workflow_binding` fields for state, operators, and gate references\n\nThe template contract must include a `dcn` field that follows the standard defined by `adr.adr.md`.\n`context` must carry provenance and single-domain metadata:\n\n- `origin`\n- `from`\n- `acting_as`\n- `scope`\n- `repository`\n- `delegated_operator`\n- `architecture_domain`",
  "consequences": "- ADRs become machine-readable source artifacts.\n- Markdown can be generated from the same JSON in multiple styles.\n- Review and workflow tooling can validate a stable schema instead of prose\n  headings.\n- Future changes to ADR shape flow through one schema file.",
  "context": {
    "acting_as": "Hermes",
    "architecture_domain": "software",
    "from": "Hermes",
    "origin": "user request",
    "repository": "projectkoios-bootstrap",
    "scope": "projectkoios-bootstrap docs-template surface"
  },
  "decision": "Adopt `docs/schemas/adr.schema.json` as the canonical ADR schema for\nthis repository and treat Markdown as a derived rendering of that JSON.\n\nThe schema should define the ADR content model, required provenance fields,\nstatus, routing, and the renderable decision sections.\nThe `workflow_binding` extension should stay optional and must point at\nexplicit ADR links when present.",
  "id": "adr.adr-template-contract",
  "implementation_brief": "No code implementation is required for the schema decision itself.\nThe optional `workflow_binding` block is a documentation and rendering extension\nfor workflow-bound ADRs.",
  "links": {
    "back_to": "architecture.00",
    "superseded_by": null,
    "supersedes": null
  },
  "non_goals": [
    "This ADR does not define the renderer implementation.",
    "This ADR does not convert existing archived ADRs yet.",
    "This ADR does not broaden ADR scope beyond one architecture domain."
  ],
  "normalization_requires_review": true,
  "normalized_status_candidate": "accepted",
  "observed_status_text": "Accepted",
  "resolved_open_questions": [
    "Should Markdown be one renderer or multiple render profiles?",
    "Should the archived ADR set be converted to JSON later?"
  ],
  "slug": "canonical-adr-proposal-template",
  "status": "Accepted",
  "title": "Canonical ADR proposal template",
  "validation_expectations": [
    "The JSON schema validates a representative ADR object.",
    "The create-ADR workflow can emit JSON matching the schema.",
    "A Markdown render can be generated from the same object."
  ]
}
```

## Status

Accepted

## Candidate note

This projection is generated evidence only. Projection parse-back does not resolve template/schema-contract or status-casing review blockers.
