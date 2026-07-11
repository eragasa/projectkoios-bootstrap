```json
{
  "title": "ADR JSON authority messy canary slice 2 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "draft-pending-hermes-user-approval",
  "datetime": "20260711.143800Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "parent_effort": "ADR rationalization / JSON-authoritative ADR store",
  "slice_name": "adr-json-authority-messy-canary-slice-2",
  "source_canary": "docs/adr/adr.schema-base.md",
  "source_reviewed_inventory": "dev/adr-json-authority-inventory-review-overrides-slice-1/",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260711.143600_adr-json-authority-inventory-review-overrides-slice-1.md",
  "next_owner": "HERMES_USER"
}
```

# Implementation brief 20260711.143800: ADR JSON authority messy canary slice 2

## Purpose

Implement one bounded messy/ambiguous ADR-space canary using:

```text
docs/adr/adr.schema-base.md
```

The slice should prove conversion behavior after the reviewed inventory/override evidence, especially:

- missing status handling;
- schema/implementation contract ambiguity;
- conflict/lossiness reporting;
- sidecar/provenance preservation;
- evidence-only JSON/object generation without inventing authority.

This is a canary/evidence slice. It must not perform authority cutover, bulk conversion, schema publication, source mutation, status normalization, or database/storage authority work.

## Source authority

Controlling staged direction and prior accepted evidence:

- `docs/adr/adr.json-authoritative-adr-store.draft.md`
- `docs/reviews/hermes-acceptance.20260711.140500_json-authoritative-adr-store.md`
- `dev/adr-json-authority-inventory-classification-slice-0/`
- `docs/reviews/hermes-acceptance.20260711.142000_adr-json-authority-inventory-classification-slice-0.md`
- `dev/adr-json-authority-inventory-review-overrides-slice-1/`
- `docs/reviews/architecture-conformance.20260711.143300_adr-json-authority-inventory-review-overrides-slice-1.md`
- `workspaces/koios/working/provenance-review.20260711_adr-json-authority-inventory-review-overrides-slice-1.md`
- `docs/reviews/hermes-acceptance.20260711.143600_adr-json-authority-inventory-review-overrides-slice-1.md`

## Canary source

Exactly one source file is in scope:

```text
docs/adr/adr.schema-base.md
```

No other `docs/adr/` source may be converted, projected, rewritten, moved, renamed, status-normalized, superseded, or included as a second source canary.

## Required input evidence

The implementation must consume or reference the reviewed inventory/override evidence from:

```text
dev/adr-json-authority-inventory-review-overrides-slice-1/
```

At minimum, it must preserve or reference the Slice 1 reviewed values for `docs/adr/adr.schema-base.md`, including:

- source path;
- source hash;
- category/disposition/authority-effect candidate values;
- automatic-conversion eligibility false;
- manual-review / missing-status rationale;
- messy canary recommendation;
- `candidate_only: true` and `authority_change: false` boundaries.

## Required evidence path

Create candidate canary evidence under a dedicated dev path, preferred:

```text
dev/adr-json-authority-messy-canary-slice-2/
```

Expected artifacts may include:

```text
dev/adr-json-authority-messy-canary-slice-2/manifest.json
dev/adr-json-authority-messy-canary-slice-2/adr.schema-base.candidate-object.json
dev/adr-json-authority-messy-canary-slice-2/conversion-evidence.json
dev/adr-json-authority-messy-canary-slice-2/conflict-lossiness-report.json
dev/adr-json-authority-messy-canary-slice-2/sidecar-provenance.json
```

If a generated projection and parse-back check is appropriate, it may additionally produce evidence such as:

```text
dev/adr-json-authority-messy-canary-slice-2/adr.schema-base.projected.md
dev/adr-json-authority-messy-canary-slice-2/projection-parseback-evidence.json
```

Projection evidence is optional and must remain evidence-only. A generated projection must not replace, mutate, or become authority over the source Markdown.

## Candidate object requirements

The candidate JSON/object evidence should represent a messy-canary object or conversion candidate, not an authoritative ADR record.

Required markers:

- `slice_name: adr-json-authority-messy-canary-slice-2`;
- `source_path: docs/adr/adr.schema-base.md`;
- `authority_mode`: candidate/evidence only;
- `authority_change: false`;
- `candidate_only: true`;
- `source_mutation: false`;
- `schema_change: false`;
- `database_authority: false`;
- `conversion_scope`: exactly one source.

The candidate object may include an ADR content payload only if it is clearly marked as candidate/incomplete/review-only and accompanied by conflict/lossiness findings for missing or noncanonical fields.

## Required preservation

The evidence must preserve or reference:

- source path;
- source hash;
- source title, if parseable;
- observed missing status as missing, not invented;
- parse warnings from Slice 0/Slice 1 and from this conversion attempt;
- reviewed category/disposition/authority-effect from Slice 1;
- missing-status and schema/implementation contract ambiguity rationale;
- source text hash before/after or equivalent source non-mutation proof;
- any unsupported, ambiguous, inferred, omitted, or noncanonical fields in sidecar/provenance evidence.

## Conflict/lossiness requirements

The slice must demonstrate conflict/lossiness reporting rather than silently normalizing or inventing fields.

At minimum, report:

- `missing_status`: status absent or not parseable from source;
- whether a normalized status candidate was omitted, inferred, or blocked;
- whether the candidate object can validate against current ADR content schema without invented status;
- any fields omitted from content and preserved in sidecar/provenance;
- any inferred fields, with rationale and `requires_review: true`;
- whether the source is blocked from authority promotion until missing-status/manual-review findings are resolved;
- final canary outcome such as `conversion_candidate_blocked_pending_review`, `candidate_object_generated_with_conflicts`, or equivalent review-only result.

Do not invent a status solely to satisfy schema or conversion expectations.

## Projection and parse-back boundary

Generated projection and parse-back evidence is allowed only if VULCAN can keep it bounded and evidence-only.

If implemented:

- generate projection under the dedicated `dev/` evidence path only;
- mark projection as generated evidence, not source or authority;
- parse back only the generated projection, not hand-authored source Markdown as a replacement;
- compare candidate object/projection semantics and report mismatches;
- record that projection equality does not resolve the missing source status or authorize cutover.

If projection would require source mutation, schema changes, or invented status, omit projection and record why.

## Source and authority boundaries

Forbidden actions:

- modify `docs/adr/adr.schema-base.md`;
- modify any other `docs/adr/*.md` file;
- modify `docs/adr/README.md` or ADR index/control Markdown;
- change anything under `docs/schemas/`;
- convert any source except `docs/adr/adr.schema-base.md`;
- create authoritative JSON ADR records;
- create generated projections intended to replace source Markdown;
- move, rename, delete, or archive files;
- normalize source status or insert a status into source;
- mark drafts superseded;
- perform authority cutover;
- add database/storage authority;
- create or commit mutable `.sqlite` or `.db` files.

## Validation requirements

Required validation evidence in the implementation report:

- source non-mutation check for `docs/adr/adr.schema-base.md` and `docs/adr/` generally;
- `docs/schemas/` non-mutation check;
- JSON validity for all generated candidate/evidence JSON files;
- no `.sqlite` or `.db` files under the Slice 2 evidence path;
- proof only one source file was converted/attempted;
- tests if code is added or changed;
- type checks and Python policy if Python is changed;
- `git diff --check` clean.

Suggested commands may include equivalents of:

```bash
git status --short -- docs/adr docs/schemas
find dev/adr-json-authority-messy-canary-slice-2 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-messy-canary-slice-2 \( -name '*.sqlite' -o -name '*.db' \) -print
git diff --check
```

If code is added under the ADR control-surface package, also run focused pytest, mypy, and Python policy for that package/tests.

## Pause gate

After this brief is drafted, pause for HERMES/USER approval before VULCAN routing or implementation.

After implementation, HERMES/USER must review the messy-canary evidence before any corpus dry-run, source mutation, schema publication, JSON authority cutover, bulk conversion, or migration slice proceeds.

## Non-goals

This slice does not authorize:

- bulk ADR migration;
- conversion of any file except the one canary source;
- authoritative JSON ADR records;
- final per-file authority decisions;
- schema publication or schema changes;
- source Markdown mutation;
- status normalization;
- file moves or renames;
- draft supersession;
- database/storage authority;
- committed mutable DB files;
- corpus dry-run conversion;
- authority cutover.
