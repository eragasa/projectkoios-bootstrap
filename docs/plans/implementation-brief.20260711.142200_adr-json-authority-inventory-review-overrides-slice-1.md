```json
{
  "title": "ADR JSON authority inventory review/overrides slice 1 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "draft-pending-hermes-user-approval",
  "datetime": "20260711.142200Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "parent_effort": "ADR rationalization / JSON-authoritative ADR store",
  "slice_name": "adr-json-authority-inventory-review-overrides-slice-1",
  "source_inventory": "dev/adr-json-authority-inventory-classification-slice-0/",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260711.142000_adr-json-authority-inventory-classification-slice-0.md",
  "next_owner": "HERMES_USER"
}
```

# Implementation brief 20260711.142200: ADR JSON authority inventory review/overrides slice 1

## Purpose

Implement a bounded review/override evidence slice for the accepted Phase 0 ADR JSON authority inventory.

This slice reviews and corrects candidate labels from:

```text
dev/adr-json-authority-inventory-classification-slice-0/
```

The goal is to make candidate category, disposition, authority-effect, and owner/domain-review fields safer for later planning before any messy canary or conversion slice consumes the inventory.

This is review/override evidence only. It must not convert ADRs, mutate ADR sources, normalize statuses, publish schemas, or perform authority cutover.

## Source authority

Controlling staged direction and accepted inventory evidence:

- `docs/adr/adr.json-authoritative-adr-store.draft.md`
- `docs/reviews/hermes-acceptance.20260711.140500_json-authoritative-adr-store.md`
- `docs/plans/implementation-brief.20260711.140700_adr-json-authority-inventory-classification-slice-0.md`
- `docs/implementation/adr-json-authority-inventory-classification-slice-0.20260711.141200.md`
- `docs/reviews/architecture-conformance.20260711.141500_adr-json-authority-inventory-classification-slice-0.md`
- `workspaces/koios/working/provenance-review.20260711_adr-json-authority-inventory-classification-slice-0.md`
- `docs/reviews/hermes-acceptance.20260711.142000_adr-json-authority-inventory-classification-slice-0.md`
- `dev/adr-json-authority-inventory-classification-slice-0/`

## Scope

In scope:

- read the accepted Slice 0 inventory evidence;
- identify and review authority-forward candidate labels, especially `authority_effect: proposed_authority` and `disposition_candidate: json_authority_candidate`;
- review/correct under-flagged product/future-system or domain-review files;
- review/correct architecture, policy/process, template/schema/contract, implementation workflow support, source/provenance, and index/control distinctions;
- produce explicit per-file override evidence under `dev/`;
- produce a reviewed inventory view that references the original source entry and records any override values and rationale;
- produce a summary of changed vs unchanged candidate labels;
- preserve observed status/casing from Slice 0 and avoid source status mutation;
- mark all outputs as review-only and non-authoritative.

Out of scope:

- source ADR mutation;
- `docs/schemas/` changes;
- Markdown-to-JSON conversion;
- generated Markdown projections;
- authority cutover;
- file moves or renames;
- status normalization in source files;
- draft supersession;
- database authority;
- committed mutable `.sqlite` or `.db` files.

## Required evidence path

Create review-only evidence under a dedicated dev path, preferred:

```text
dev/adr-json-authority-inventory-review-overrides-slice-1/
```

Expected artifacts should include at minimum:

```text
dev/adr-json-authority-inventory-review-overrides-slice-1/manifest.json
dev/adr-json-authority-inventory-review-overrides-slice-1/reviewed-inventory.json
dev/adr-json-authority-inventory-review-overrides-slice-1/overrides.json
dev/adr-json-authority-inventory-review-overrides-slice-1/review-summary.json
```

VULCAN may adjust filenames for consistency, but the implementation report must document each evidence artifact and keep the output review-only.

## Review requirements

The implementation must explicitly address the HERMES/KOIOS watchpoints from Slice 0.

### Authority-forward labels

Every Slice 0 entry with either of these values must be reviewed:

```text
authority_effect: proposed_authority
disposition_candidate: json_authority_candidate
```

For each such entry, the reviewed output must either:

- keep the value as a candidate with explicit `candidate_only: true` and rationale; or
- override to a safer candidate such as `candidate`, `manual_review_required`, `domain_review_required`, `source_only_provenance_candidate`, or `excluded_pending_review`.

No reviewed label may be interpreted as final authority approval.

### Domain/product review flags

The implementation must review at least the specific files called out by KOIOS, if present:

```text
docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md
docs/adr/adr.agent-windows-on-message-triggers.draft.md
docs/adr/adr.ui-core.draft.md
docs/adr/adr.workflow-ui.draft.md
```

For each, record whether owner/domain review is required and why. If the file is not present, record that fact explicitly.

### Mixed-document category distinctions

Review category/disposition for files classified as:

- `template_schema_contract`;
- `implementation_workflow_support`;
- `policy_process`;
- `architecture_blueprint`;
- `source_provenance`;
- `index_or_control_surface`;
- `unknown_requires_review`.

The reviewed output should prefer conservative review flags over automatic conversion eligibility when document authority/domain is unclear.

## Override record shape

Each override or explicit keep decision should include:

- source path;
- source hash from Slice 0;
- original category/disposition/authority-effect/owner-domain-review values;
- reviewed category/disposition/authority-effect/owner-domain-review values;
- whether the value changed;
- rationale;
- reviewer/source basis, e.g. KOIOS watchpoint, HERMES acceptance watchpoint, or deterministic rule;
- `candidate_only: true`;
- `authority_change: false`;
- `source_mutation: false`.

## Manifest requirements

The manifest must be valid JSON and deterministic for unchanged inputs.

At minimum, record:

- `slice_name`: `adr-json-authority-inventory-review-overrides-slice-1`;
- `mode`: review-only inventory override evidence;
- `authority_change`: false;
- `source_mutation_allowed`: false;
- `schema_change_allowed`: false;
- `conversion_performed`: false;
- `database_authority`: false;
- source inventory path and hash;
- references to Slice 0 implementation, ATHENA/KOIOS/HERMES reviews, and HERMES final acceptance;
- evidence artifact paths and hashes;
- validation command summary.

## Boundaries

Forbidden actions:

- modify any `docs/adr/*.md` file;
- modify `docs/adr/README.md` or other ADR index/control Markdown source;
- change anything under `docs/schemas/`;
- create authoritative JSON ADR records;
- convert Markdown ADRs to JSON records;
- create generated projections intended to replace source Markdown;
- move, rename, delete, or archive ADR files;
- normalize statuses in source files;
- mark drafts superseded;
- create or commit mutable database files;
- treat override values as final authority cutover decisions.

## Validation requirements

Required validation evidence in the implementation report:

- JSON validity check for all generated override/review evidence;
- check that no `docs/adr/` or ADR index/control Markdown source was mutated by this slice;
- check that no `docs/schemas/` files changed;
- check that no `.sqlite` or `.db` files exist under the new evidence path;
- deterministic/stable output check when practical;
- focused tests if code is added;
- Python policy and type checks if Python is changed;
- `git diff --check` clean.

Suggested commands may include equivalents of:

```bash
git status --short -- docs/adr docs/schemas
find dev/adr-json-authority-inventory-review-overrides-slice-1 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-inventory-review-overrides-slice-1 \( -name '*.sqlite' -o -name '*.db' \) -print
git diff --check
```

## Pause gate

After this brief is drafted, pause for HERMES/USER approval before VULCAN routing or implementation.

After implementation, HERMES/USER must review and accept the override evidence before any messy canary, corpus dry-run, source mutation, schema publication, JSON authority cutover, or migration slice consumes the reviewed inventory.

## Non-goals

This slice does not authorize:

- final per-file authority decisions;
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
- draft supersession.
