```json
{
  "title": "ADR JSON authority inventory/classification slice 0 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "draft-pending-hermes-user-approval",
  "datetime": "20260711.140700Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "parent_effort": "ADR rationalization / JSON-authoritative ADR store",
  "slice_name": "adr-json-authority-inventory-classification-slice-0",
  "source_adr": "docs/adr/adr.json-authoritative-adr-store.draft.md",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260711.140500_json-authoritative-adr-store.md",
  "next_owner": "HERMES_USER"
}
```

# Implementation brief 20260711.140700: ADR JSON authority inventory/classification slice 0

## Purpose

Implement Phase 0 of the accepted JSON-authoritative ADR migration path: a review-only inventory/classification manifest for ADR-space Markdown and ADR index/control surfaces.

This slice must make the current corpus inspectable before conversion or authority changes. It is classification/evidence only. It must not create authoritative JSON ADR records, mutate ADR sources, normalize statuses, publish schemas, or perform migration.

## Source authority

Controlling staged direction:

- `docs/adr/adr.json-authoritative-adr-store.draft.md`
- `docs/reviews/hermes-acceptance.20260711.140500_json-authoritative-adr-store.md`

Supporting architecture and evidence:

- `docs/architecture/architecture.adr-bidirectional-objects.md`
- `docs/architecture/architecture.json-adr-storage-topology.md`
- `docs/implementation/adr-bidirectional-object-canary-slice-0.20260711.134900.md`
- `dev/adr-bidirectional-object-canary-slice-0/`

## Scope

In scope:

- inspect and classify every `docs/adr/*.md` file;
- inspect and classify ADR index/control files, including `docs/adr/README.md` when present, plus any directly relevant ADR index/control file discovered by the implementation;
- produce a review-only manifest/evidence package under `dev/`;
- record parse confidence and uncertainty for each inspected file;
- record observed source status/casing separately from any normalized status candidate;
- propose category/disposition and `authority_effect` candidate values for review;
- flag owner/domain review needs;
- identify files excluded from automatic conversion or blocked pending review.

Out of scope:

- source mutation;
- `docs/schemas/` changes;
- file moves or renames;
- status normalization;
- draft supersession;
- authoritative JSON ADR records;
- corpus conversion;
- generated Markdown projections;
- database authority;
- committed mutable `.sqlite` or `.db` files.

## Required evidence path

Create review-only evidence under a dedicated dev path, preferred:

```text
dev/adr-json-authority-inventory-classification-slice-0/
```

Expected artifacts should include at minimum:

```text
dev/adr-json-authority-inventory-classification-slice-0/manifest.json
dev/adr-json-authority-inventory-classification-slice-0/source-inventory.json
dev/adr-json-authority-inventory-classification-slice-0/classification-summary.json
```

VULCAN may adjust filenames for consistency, but the implementation report must document every evidence artifact and keep the output review-only.

## Manifest requirements

The manifest must be valid JSON and deterministic for unchanged source inputs.

At minimum, record top-level metadata:

- `slice_name`: `adr-json-authority-inventory-classification-slice-0`;
- `mode`: review-only inventory/classification;
- `authority_change`: false;
- `source_mutation_allowed`: false;
- `schema_change_allowed`: false;
- `database_authority`: false;
- inspected glob/path set;
- generated timestamp or stable generation metadata;
- source architecture/ADR/acceptance references;
- validation command summary.

For each inspected file, record:

- source path;
- source hash;
- file kind: ADR source candidate, index/control surface, or other discovered control/reference surface;
- source title if parseable;
- observed status text exactly as found;
- observed status casing exactly as found;
- normalized status candidate, if safely inferable;
- whether status normalization is required;
- parse confidence: e.g. `high`, `medium`, `low`, or `failed`;
- parse warnings and uncertainty flags;
- category candidate;
- disposition candidate;
- authority_effect candidate;
- owner/domain review flags;
- automatic-conversion eligibility candidate;
- exclusion/blocking reason where applicable.

## Classification vocabulary

Use explicit values so review can compare files without interpreting prose.

Recommended category candidates:

- `current_decision`;
- `source_provenance`;
- `policy_process`;
- `architecture_blueprint`;
- `template_schema_contract`;
- `implementation_workflow_support`;
- `product_future_system_draft`;
- `index_or_control_surface`;
- `unknown_requires_review`.

Recommended disposition candidates:

- `json_authority_candidate`;
- `source_only_provenance_candidate`;
- `generated_projection_candidate`;
- `excluded_pending_review`;
- `index_or_control_surface`;
- `domain_review_required`;
- `manual_review_required`.

Required `authority_effect` candidates:

- `none`;
- `candidate`;
- `proposed_authority`;
- `accepted_authority`;
- `excluded`;
- `domain_review_required`.

This slice must not treat these candidate values as final authority decisions.

## Status handling

The inventory must preserve observed status evidence and avoid implicit lifecycle changes.

Rules:

- Record the exact observed status text/casing from each source when present.
- Record a normalized status candidate separately, if the implementation can infer one without rewriting source.
- Mark ambiguous, missing, inconsistent, or non-canonical statuses as review findings.
- Do not rewrite status in source Markdown.
- Do not mark drafts accepted, superseded, active, inactive, or excluded by mutating the source.
- Do not use inventory classification to demote Markdown authority.

## Source and authority boundaries

The implementation must prove it did not alter the ADR source corpus or authority surfaces.

Forbidden actions:

- modify any `docs/adr/*.md` file;
- modify any ADR index/control Markdown file such as `docs/adr/README.md`;
- change anything under `docs/schemas/`;
- write authoritative JSON records outside the review-only `dev/` evidence path;
- create generated projections intended to replace source Markdown;
- move, rename, delete, or archive ADR files;
- normalize statuses in source;
- mark drafts superseded;
- create or commit mutable database files.

## Implementation guidance

Prefer small reusable parsing/classification code only if needed to make the manifest deterministic and testable. If implementation would require schema publication, storage authority changes, corpus conversion, or source mutation, VULCAN must pause and ask for approval.

The inventory may be conservative. Low-confidence parse results, uncertain category, or domain ownership ambiguity should produce review flags rather than invented certainty.

Index/control files must be classified distinctly from ADR decision records so they are not accidentally included in automatic authority conversion.

## Validation requirements

Required validation evidence in the implementation report:

- command proving source non-mutation for `docs/adr/` and ADR index/control files;
- JSON validity check for all generated manifest/evidence JSON files;
- deterministic or stable manifest generation check when practical;
- no changes under `docs/schemas/`;
- no committed `.sqlite` or `.db` files under the evidence path or repository;
- `git diff --check` clean.

Suggested commands may include equivalents of:

```bash
git status --short -- docs/adr docs/schemas
python -m json.tool dev/adr-json-authority-inventory-classification-slice-0/manifest.json >/dev/null
find dev/adr-json-authority-inventory-classification-slice-0 -name '*.json' -print -exec python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-inventory-classification-slice-0 \( -name '*.sqlite' -o -name '*.db' \) -print
git diff --check
```

If tests are added, they should verify manifest validity, required per-file fields, review-only authority markers, status preservation fields, and source non-mutation assumptions.

## Pause gate

After this brief is drafted, pause for HERMES/USER approval before VULCAN routing or implementation.

After implementation, the generated inventory/classification manifest must be reviewed and accepted by HERMES/USER before any messy canary, corpus dry-run, source mutation, schema publication, JSON authority cutover, or migration slice proceeds.

## Non-goals

This slice does not authorize:

- authoritative JSON ADR records;
- mass conversion;
- corpus dry-run conversion;
- generated Markdown projection replacement;
- source Markdown mutation;
- schema publication or schema changes;
- SQLite/database authority;
- committed mutable DB files;
- file moves or renames;
- status normalization;
- draft supersession;
- acceptance/rejection of any individual ADR record;
- final per-file authority decisions.
