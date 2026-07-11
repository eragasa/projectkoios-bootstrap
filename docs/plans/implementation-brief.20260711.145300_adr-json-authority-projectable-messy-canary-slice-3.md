```json
{
  "title": "ADR JSON authority projectable messy canary slice 3 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "draft-pending-hermes-user-approval",
  "datetime": "20260711.145300Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "parent_effort": "ADR rationalization / JSON-authoritative ADR store",
  "slice_name": "adr-json-authority-projectable-messy-canary-slice-3",
  "source_canary": "docs/adr/adr.adr-template-contract.md",
  "source_reviewed_inventory": "dev/adr-json-authority-inventory-review-overrides-slice-1/",
  "source_messy_canary": "dev/adr-json-authority-messy-canary-slice-2/",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260711.145000_adr-json-authority-messy-canary-slice-2.md",
  "next_owner": "HERMES_USER"
}
```

# Implementation brief 20260711.145300: ADR JSON authority projectable messy canary slice 3

## Purpose

Implement the next bounded ADR JSON authority proof point: a messy-but-projectable one-source canary.

Use exactly one source:

```text
docs/adr/adr.adr-template-contract.md
```

This file is the KOIOS-recommended primary messy-but-projectable candidate after Slice 2 and exercises different risks than the blocked missing-status canary:

- observed Markdown status exists but uses noncanonical casing: `Accepted`;
- reviewed inventory marks it `template_schema_contract` / `manual_review_required`, not automatic-conversion eligible;
- conversion should be projectable without inventing a missing status;
- generated projection/parse-back behavior can be tested while preserving template/contract ambiguity and candidate-only boundaries.

The slice should prove that projection evidence can be generated for a messy source while preserving status casing, manual-review blockers, conflict/lossiness findings, sidecar/provenance, and no-authority boundaries.

## Source authority and required inputs

Controlling staged direction and accepted evidence:

- `docs/adr/adr.json-authoritative-adr-store.draft.md`
- `docs/reviews/hermes-acceptance.20260711.140500_json-authoritative-adr-store.md`
- `dev/adr-json-authority-inventory-classification-slice-0/`
- `dev/adr-json-authority-inventory-review-overrides-slice-1/`
- `docs/reviews/hermes-acceptance.20260711.143600_adr-json-authority-inventory-review-overrides-slice-1.md`
- `dev/adr-json-authority-messy-canary-slice-2/`
- `docs/reviews/hermes-acceptance.20260711.145000_adr-json-authority-messy-canary-slice-2.md`

Required Slice 1 reviewed values for the source must be consumed or referenced:

- source hash: `2876dfbe031105d383fa9e33cec7d5dd49cf569cea6f43eae59e8fa1da502895` if unchanged;
- reviewed category: `template_schema_contract`;
- reviewed disposition: `manual_review_required`;
- reviewed authority effect: `candidate`;
- automatic-conversion eligibility: `false`;
- candidate-only / no-authority markers.

## Canary source

Exactly one source file is in scope:

```text
docs/adr/adr.adr-template-contract.md
```

No other `docs/adr/` source may be converted, projected, rewritten, moved, renamed, status-normalized, superseded, or included as a second source canary.

## Required evidence path

Create candidate canary evidence under a dedicated dev path, preferred:

```text
dev/adr-json-authority-projectable-messy-canary-slice-3/
```

Expected artifacts should include:

```text
dev/adr-json-authority-projectable-messy-canary-slice-3/manifest.json
dev/adr-json-authority-projectable-messy-canary-slice-3/candidate-object.json
dev/adr-json-authority-projectable-messy-canary-slice-3/generated-projection.md
dev/adr-json-authority-projectable-messy-canary-slice-3/projection-parseback-evidence.json
dev/adr-json-authority-projectable-messy-canary-slice-3/conversion-evidence.json
dev/adr-json-authority-projectable-messy-canary-slice-3/conflict-lossiness-report.json
dev/adr-json-authority-projectable-messy-canary-slice-3/sidecar-provenance.json
```

VULCAN may adjust filenames for consistency, but the evidence directory must be dedicated to this slice and the implementation report must document all evidence artifacts.

## Candidate object requirements

The candidate object must be evidence-only, not an authoritative ADR record.

Required markers:

- `slice_name: adr-json-authority-projectable-messy-canary-slice-3`;
- `source_path` exactly the selected source;
- `authority_mode`: candidate/evidence only;
- `authority_change: false`;
- `candidate_only: true`;
- `source_mutation: false`;
- `schema_change: false`;
- `database_authority: false`;
- `conversion_scope`: exactly one source;
- `conversion_completed_as_authoritative_record: false`.

The candidate object may include a content candidate only when it preserves observed source facts and clearly reports blockers. It must not imply repository authority, product authority, or cutover readiness.

## Status and projection requirements

This slice specifically tests status-casing and projection behavior.

Required behavior:

- preserve observed Markdown status exactly as `Accepted`;
- record a normalized status candidate such as `accepted` separately, if useful;
- record that status casing normalization would be required before any authority promotion;
- do not rewrite source status;
- do not silently normalize source status in sidecar/provenance;
- do not treat `Accepted` casing as final accepted JSON authority beyond source observation and review;
- generated projection must be visibly marked as generated evidence, not source authority;
- generated projection should preserve observed status casing or explicitly report if it cannot do so without normalization;
- parse-back must parse only the generated projection, not hand-authored source Markdown as a replacement;
- parse-back evidence must compare semantic fields and explicitly report status casing/normalization behavior;
- projection equality must not resolve domain-review or authority blockers.

If projection generation would require status normalization, source mutation, schema changes, or authority implication, VULCAN must pause rather than generate a misleading projection.

## Conflict/lossiness requirements

The slice must demonstrate conflict/lossiness reporting for a projectable but still blocked source.

At minimum, report:

- observed status casing is noncanonical or normalization-sensitive;
- template/schema-contract ambiguity from the reviewed inventory;
- source is blocked from authority promotion by manual-review and status-normalization findings;
- any fields omitted from content and preserved in sidecar/provenance;
- any inferred fields, with rationale and `requires_review: true`;
- whether generated projection parse-back is semantically equal for allowed candidate fields;
- whether projection/parse-back introduced, removed, or normalized any source-sensitive field;
- final outcome such as `projectable_candidate_blocked_pending_template_contract_and_status_review`.

## Sidecar/provenance requirements

Preserve or reference:

- source path;
- source hash before/after;
- source title;
- observed source status text/casing;
- normalized status candidate, if produced;
- Slice 1 reviewed category/disposition/authority-effect and manual-review flags;
- conflict/lossiness findings;
- generated projection path/hash if projection is produced;
- parse-back evidence path/hash;
- any unsupported, omitted, inferred, normalized, or domain-sensitive material.

## Acceptance criteria

HERMES/USER may accept the slice only if evidence shows:

1. Exactly one source was used: `docs/adr/adr.adr-template-contract.md`.
2. No `docs/adr` source, `docs/schemas` file, or ADR index/control Markdown was mutated.
3. Observed status `Accepted` is preserved separately from any normalized status candidate.
4. Projection, if generated, is under `dev/` only and marked generated evidence / non-authoritative.
5. Parse-back is performed only against the generated projection and reports status-casing behavior.
6. Candidate object and evidence remain `candidate_only: true` and `authority_change: false`.
7. Template/schema-contract manual review remains blocking; no authority promotion is implied.
8. Conflict/lossiness report blocks cutover until template-contract/status review resolves or excludes the record.
9. No authoritative JSON ADR record, source projection replacement, database authority, bulk conversion, file moves/renames, status normalization, draft supersession, or cutover is introduced.

## Required KOIOS/VULCAN inputs

Required implementation inputs:

- VULCAN must consume/reference Slice 1 reviewed inventory evidence for the selected source.
- VULCAN must consume/reference Slice 2 acceptance/watchpoints so this slice does not regress blocked-candidate/no-authority behavior.

Required post-implementation review:

- KOIOS provenance review is required before HERMES final acceptance, focused on status-casing preservation, template-contract/manual-review blockers, projection safety, and whether generated projection/parse-back could be mistaken for authority.
- ATHENA architecture/conformance review is required before HERMES final acceptance.

If VULCAN finds that projection cannot be generated safely without status normalization or authority ambiguity, VULCAN must pause and report that finding rather than forcing projection.

## Source and authority boundaries

Forbidden actions:

- modify the selected source Markdown;
- modify any other `docs/adr/*.md` file;
- modify `docs/adr/README.md` or ADR index/control Markdown;
- change anything under `docs/schemas/`;
- convert or project any source except the selected one;
- create authoritative JSON ADR records;
- create generated projections intended to replace source Markdown;
- move, rename, delete, or archive files;
- normalize source status in source Markdown;
- mark drafts superseded;
- perform authority cutover;
- add database/storage authority;
- create or commit mutable `.sqlite` or `.db` files;
- treat template/schema-contract manual-review findings as resolved.

## Validation requirements

Required validation evidence in the implementation report:

- source non-mutation check for selected source and `docs/adr/` generally;
- `docs/schemas/` non-mutation check;
- JSON validity for all generated candidate/evidence JSON files;
- no `.sqlite` or `.db` files under the Slice 3 evidence path;
- proof only one source file was converted/projected/attempted;
- generated projection file exists only under the Slice 3 `dev/` path, if projection is generated;
- tests if code is added or changed;
- type checks and Python policy if Python is changed;
- `git diff --check` clean.

Suggested commands may include equivalents of:

```bash
git status --short -- docs/adr docs/schemas
find dev/adr-json-authority-projectable-messy-canary-slice-3 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-projectable-messy-canary-slice-3 \( -name '*.sqlite' -o -name '*.db' \) -print
git diff --check
```

If code is added under the ADR control-surface package, also run focused pytest, mypy, and Python policy for that package/tests.

## Pause gate

After this brief is drafted, pause for HERMES/USER approval before VULCAN routing or implementation.

After implementation, HERMES/USER must receive KOIOS and ATHENA reviews before accepting the slice. Acceptance of this slice still must not authorize corpus dry-run, source mutation, schema publication, JSON authority cutover, bulk conversion, or migration.

## Non-authorizations

This slice does not authorize:

- corpus conversion;
- conversion or projection of any file beyond the one selected source;
- authoritative JSON ADR records;
- final per-file authority decisions;
- schema publication or schema changes;
- source Markdown mutation;
- source status normalization;
- file moves or renames;
- draft supersession;
- database/storage authority;
- committed mutable DB files;
- authority cutover;
- product/future-system domain authority resolution.
