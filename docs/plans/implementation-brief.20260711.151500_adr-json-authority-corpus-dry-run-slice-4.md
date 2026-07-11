```json
{
  "title": "ADR JSON authority corpus dry-run inventory slice 4 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "draft-pending-hermes-user-approval",
  "datetime": "20260711.151500Z",
  "revised_datetime": "20260711.151900Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "parent_effort": "ADR rationalization / JSON-authoritative ADR store",
  "slice_name": "adr-json-authority-corpus-dry-run-inventory-slice-4",
  "evidence_path": "dev/adr-json-authority-corpus-dry-run-inventory-slice-4/",
  "koios_input": "workspaces/koios/working/next-proof-input.20260711_adr-json-authority-corpus-dry-run-slice-4.md",
  "next_owner": "HERMES_USER"
}
```

# Implementation brief 20260711.151500: ADR JSON authority corpus dry-run inventory slice 4

## Revision note

Revised per HERMES request to align with KOIOS primary six-entry subset in:

```text
workspaces/koios/working/next-proof-input.20260711_adr-json-authority-corpus-dry-run-slice-4.md
```

This brief uses slice name:

```text
adr-json-authority-corpus-dry-run-inventory-slice-4
```

and evidence path:

```text
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/
```

## Purpose

Implement the next bounded ADR JSON authority proof point: a candidate-only corpus-style dry-run inventory over a small selected ADR subset.

This slice tests multi-file manifest/report behavior across different reviewed dispositions without authority cutover. It should show whether ADR JSON authority candidate tooling can report per-source conversion/skipped outcomes, lossiness/conflict findings, blocker categories, sidecar/provenance needs, and aggregate summary counts across more than one file while preserving the no-mutation/no-authority boundaries proven by Slices 2 and 3.

This is a bounded subset dry-run. The word `corpus` means corpus-style reporting/manifest shape over the approved six-entry subset, not all ADRs and not a migration.

## Control inputs

VULCAN must consume or reference these accepted inputs:

- staged direction: `docs/adr/adr.json-authoritative-adr-store.draft.md`
- Slice 2 acceptance: `docs/reviews/hermes-acceptance.20260711.145000_adr-json-authority-messy-canary-slice-2.md`
- Slice 3 acceptance: `docs/reviews/hermes-acceptance.20260711.151000_adr-json-authority-projectable-messy-canary-slice-3.md`
- inventory evidence: `dev/adr-json-authority-inventory-classification-slice-0/`
- reviewed inventory/overrides evidence: `dev/adr-json-authority-inventory-review-overrides-slice-1/`
- KOIOS Slice 4 proof input: `workspaces/koios/working/next-proof-input.20260711_adr-json-authority-corpus-dry-run-slice-4.md`

If implementation findings conflict with KOIOS input, this brief, or accepted Slice 2/Slice 3 watchpoints, VULCAN must pause and report the conflict rather than resolving it in code.

## Selected dry-run subset

The dry-run subset is fixed. It must include exactly these six entries, in this order unless implementation requires a deterministic sorted form that preserves the same membership:

```text
docs/adr/adr.json-schemas.draft.md
docs/adr/adr.petrinet.20260705.132740Z.md
docs/adr/adr.adr-template-contract.md
docs/adr/adr.schema-base.md
docs/adr/adr.adr-lifecycle.draft.md
docs/adr/README.md
```

No other ADR source may be converted, projected, parsed as a candidate, or counted as part of the dry-run subset.

Explicitly excluded from default Slice 4 subset unless separately justified and approved by HERMES/USER:

```text
docs/adr/adr.20260702.144539_agent-production-trace-and-training-capture.draft.md
docs/adr/adr.20260702.043600_koios-adversarial-code-review-authority.draft.md
```

Optional domain-review files must not be added without explicit HERMES/USER approval.

## Selection rationale and required source expectations

| Role in proof | Source path | Required reviewed-input behavior | Required watchpoint |
|---|---|---|---|
| Clean candidate control | `docs/adr/adr.json-schemas.draft.md` | Reviewed as `template_schema_contract`, `json_authority_candidate`, `authority_effect: candidate`, auto candidate `true` | Candidate evidence may be generated if no source facts are invented; still `candidate_only: true` and `authority_change: false`. |
| Accepted/current decision candidate | `docs/adr/adr.petrinet.20260705.132740Z.md` | Reviewed as `template_schema_contract`, `json_authority_candidate`, `authority_effect: candidate`, auto candidate `true` | Accepted/current source status must not imply accepted JSON authority or cutover. |
| Slice 3 regression/manual review | `docs/adr/adr.adr-template-contract.md` | Reviewed as `template_schema_contract`, `manual_review_required`, `authority_effect: candidate`, auto candidate `false` | Preserve `Accepted` exactly, normalized candidate separately, template-contract/manual-review blockers, generated projection labeling, and Slice 3 wrapped-list continuation preservation. |
| Missing-status/manual review blocker | `docs/adr/adr.schema-base.md` | Reviewed as `template_schema_contract`, `manual_review_required`, `authority_effect: candidate`, auto candidate `false` | Do not invent top-level ADR status; record missing-status blocker and either skip projection or generate only clearly blocked candidate evidence if safe. |
| Source/provenance draft exclusion | `docs/adr/adr.adr-lifecycle.draft.md` | Reviewed as `template_schema_contract`, `source_only_provenance_candidate`, `authority_effect: candidate`, auto candidate `false` | Report as source/provenance draft; do not promote as current lifecycle authority and do not supersede accepted lifecycle ADRs. |
| Index/control exclusion row | `docs/adr/README.md` | Reviewed as `index_or_control_surface`, `authority_effect: none`, auto candidate `false` | Report as skipped/excluded index/control surface; do not convert to ADR candidate object unless tooling has an explicit non-ADR control-surface record type, and even then it remains non-authoritative evidence only. |

VULCAN should preserve exact source path and current source hash for every selected file, comparing against reviewed Slice 1 values where available and reporting any mismatch as staleness or source-change evidence rather than silently accepting stale values.

## Required evidence path

All generated evidence must live under:

```text
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/
```

Expected artifacts should include, or equivalent names with the same information:

```text
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/manifest.json
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/selected-sources.json
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/per-source-results.json
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/conflict-lossiness-report.json
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/projection-parseback-report.json
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/skipped-or-blocked-sources.json
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/candidate-objects/
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/generated-projections/
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/sidecars/
```

Projection files, if produced, must remain under this evidence directory only. VULCAN may omit projection for any source where projection would imply normalization, authority promotion, schema change, or misleading completeness; omitted projections must be reported per source with reasons.

## Candidate-only behavior requirements

Every evidence artifact and per-source result must make these markers machine-visible:

- `slice_name: adr-json-authority-corpus-dry-run-inventory-slice-4`
- `authority_mode`: candidate/evidence only
- `authority_change: false`
- `candidate_only: true`
- `source_mutation: false`
- `schema_change: false`
- `database_authority: false`
- `conversion_completed_as_authoritative_record: false`
- `corpus_dry_run: true`
- `bounded_subset_only: true`
- `bulk_migration: false`
- `cutover_authorized: false`

The dry-run may generate candidate objects and projections only as review evidence. It must not create authoritative JSON ADR records or update any final authority location.

## Per-source result requirements

For each selected entry, report:

- source path;
- source hash before/after, or explicit unchanged-source check;
- reviewed inventory category, disposition, authority effect, eligibility, and blocker flags from Slice 1;
- whether the entry is an ADR source candidate, source/provenance draft, or index/control surface;
- attempted candidate-conversion status, or skipped/excluded reason;
- projection status: generated, omitted, skipped, or blocked, with reason;
- parse-back status for generated projections only;
- observed source status text/casing and normalized candidate status if one is produced;
- all lossiness/conflict findings;
- all unsupported/omitted/inferred/normalized/sidecar-preserved fields;
- final per-source outcome.

Suggested per-source outcome vocabulary:

- `candidate_projectable_pending_review`
- `accepted_source_candidate_not_json_authority`
- `projectable_candidate_blocked_pending_template_contract_and_status_review`
- `blocked_missing_status_pending_review`
- `source_only_provenance_draft_skipped_or_blocked`
- `index_control_surface_skipped`
- `projection_omitted_to_avoid_authority_implication`

VULCAN may refine names for consistency, but outcomes must distinguish projectable candidate, accepted-source candidate, blocked messy/manual-review, missing-status blocker, source-only/provenance draft, and index/control exclusion cases.

## Aggregate reporting requirements

The dry-run summary must aggregate at minimum:

- selected entry count and exact selected source list;
- count by reviewed inventory category;
- count by reviewed disposition;
- count by authority effect;
- count by automatic-conversion eligibility candidate;
- count by entry type: ADR source candidate, source/provenance draft, index/control surface;
- count by final dry-run outcome;
- count of generated candidate objects;
- count of skipped/excluded entries with reasons;
- count of generated projections;
- count of omitted/blocked/skipped projections with reasons;
- count of parse-back comparisons run and their outcomes;
- count of missing-status findings;
- count of status-casing/normalization-sensitive findings;
- count of source-only/provenance blockers;
- count of index/control-surface exclusions;
- count of manual-review blockers;
- count of candidate records that would require sidecar/provenance preservation before any future authority promotion.

The summary must not imply corpus readiness, migration readiness, cutover readiness, or authoritative JSON completeness.

## Conflict/lossiness requirements

Conflict/lossiness aggregation must preserve the Slices 2 and 3 lessons and KOIOS Slice 4 watchpoints:

- missing source status must remain missing and must not be invented;
- embedded or sidecar status values must not be promoted into source lifecycle status;
- observed status casing such as `Accepted` must be preserved separately from normalized candidates;
- accepted/current source statuses must not become accepted JSON authority;
- projection equality must be scoped to candidate fields only and must not resolve domain, manual-review, source-only, index/control, or authority blockers;
- manual-review, template-contract, source-only/provenance, and index/control blockers must remain blockers or skips;
- unsupported, omitted, inferred, normalized, or sidecar-preserved fields must be visible per source and aggregate-counted;
- Slice 3 wrapped-list continuation preservation must be tested or otherwise explicitly protected in multi-file mode.

If multi-file aggregation would hide or collapse a per-source blocker, VULCAN must preserve the per-source blocker and report the aggregation limitation rather than smoothing it away.

## Source and authority boundaries

Forbidden actions:

- mutate any `docs/adr/*.md` source;
- mutate `docs/adr/README.md` or ADR index/control Markdown;
- change anything under `docs/schemas/`;
- normalize source status in source Markdown;
- create authoritative JSON ADR records;
- create generated projections intended to replace source Markdown;
- move, rename, delete, archive, or supersede ADR files;
- mark drafts superseded;
- promote `docs/adr/adr.adr-lifecycle.draft.md` as current lifecycle authority;
- treat `docs/adr/README.md` as an ADR record;
- add database/storage authority;
- create or commit mutable `.sqlite` or `.db` files;
- convert/project/parse candidate records for sources outside the six-entry selected subset;
- treat this dry-run as corpus conversion, bulk migration, or authority cutover.

## Acceptance criteria

HERMES/USER may accept the slice only if evidence shows:

1. Exactly the six selected entries were inspected/attempted, with no extra sources and no silent expansion to all ADRs.
2. `docs/adr/`, `docs/schemas/`, and ADR index/control Markdown were not mutated.
3. Evidence lives under `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/`.
4. Every selected entry has a per-source result row with source hash, reviewed Slice 1 values, observed status/casing or explicit absence, outcome, blockers, and artifact references or skip reason.
5. `docs/adr/README.md` is skipped/excluded as an index/control surface and is not converted into an ADR record.
6. `docs/adr/adr.adr-lifecycle.draft.md` remains source/provenance draft evidence only and is not promoted, superseded, or treated as current lifecycle authority.
7. `docs/adr/adr.schema-base.md` preserves missing status as missing and does not invent source status.
8. `docs/adr/adr.adr-template-contract.md` preserves Slice 3 regression behavior, including `Accepted` casing, manual-review blockers, generated-evidence labeling if projection is produced, and wrapped-list continuation preservation.
9. `docs/adr/adr.petrinet.20260705.132740Z.md` accepted/current source status does not imply accepted JSON authority or cutover.
10. Candidate objects/projections/sidecars are under the dedicated `dev/` path only and marked generated evidence / non-authoritative.
11. Aggregate summary counts match the per-source results and distinguish projectable, blocked, skipped, manual-review, source-only, and index/control outcomes.
12. JSON evidence validates, no `.sqlite`/`.db` files are created under the evidence path, and `git diff --check` passes.
13. Tests are added or updated if code changes, including regression for Slice 3 wrapped-list continuation preservation in multi-file mode.
14. No authoritative JSON ADR records, source mutation, schema change, DB/storage authority, status normalization, source status invention, file moves/renames/deletes, draft supersession, bulk migration, or cutover is introduced.

## Required post-implementation review

Before HERMES final acceptance:

- ATHENA must perform architecture/conformance review against this brief and the accepted Slice 2/Slice 3 watchpoints.
- KOIOS provenance review is required, focused on whether multi-file aggregation preserves per-source provenance, blocker specificity, sidecar/lossiness visibility, skipped/excluded row semantics, and candidate-only/no-authority signaling.

## Validation requirements

Required validation evidence in the implementation report:

- proof exactly six selected entries were inspected/attempted and no others;
- source non-mutation check for `docs/adr/` generally and selected sources specifically;
- `docs/schemas/` non-mutation check;
- JSON validity for all generated evidence JSON files;
- no `.sqlite` or `.db` files under the Slice 4 evidence path;
- generated projections exist only under the Slice 4 `dev/` path, if any are generated;
- aggregate counts match per-source records;
- tests if code is added or changed;
- type checks and Python policy if Python is changed;
- `git diff --check` clean.

Suggested commands may include equivalents of:

```bash
git status --short -- docs/adr docs/schemas
find dev/adr-json-authority-corpus-dry-run-inventory-slice-4 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-corpus-dry-run-inventory-slice-4 \( -name '*.sqlite' -o -name '*.db' \) -print
git diff --check
```

If Python code is changed under the ADR control-surface package, also run focused pytest, mypy, and Python policy for that package/tests.

## Pause gate

After this revised brief is drafted, pause again for HERMES/USER approval before VULCAN routing or implementation.

After implementation, HERMES/USER must receive ATHENA and KOIOS reviews before accepting the slice.

## Non-authorizations

This slice does not authorize:

- mutation of any `docs/adr/` file;
- mutation or publication of `docs/schemas/`;
- source status normalization;
- authoritative JSON ADR records;
- conversion of all ADRs;
- conversion/projection of entries outside the approved six-entry subset;
- JSON authority cutover;
- database/storage authority;
- committed mutable `.sqlite` or `.db` files;
- file moves, renames, deletes, archives, or draft supersession;
- treating `dev/` evidence as durable authority;
- resolving template/schema-contract, source-only, index/control, domain-review, or product/future-system dispositions;
- product/future-system domain authority.
