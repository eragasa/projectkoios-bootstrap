```json
{
  "title": "Architecture conformance review: ADR JSON authority messy canary slice 2",
  "artifact_type": "architecture-conformance-review",
  "status": "accepted-with-watchpoints",
  "datetime": "20260711.144800Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-messy-canary-slice-2",
  "reviewed_implementation": "docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md",
  "source_brief": "docs/plans/implementation-brief.20260711.143800_adr-json-authority-messy-canary-slice-2.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.144200_adr-json-authority-messy-canary-slice-2.md",
  "next_owner": "HERMES_USER"
}
```

# Architecture conformance review 20260711.144800: ADR JSON authority messy canary slice 2

## Verdict

Accepted with watchpoints for HERMES/USER final acceptance.

The implementation conforms to the Slice 2 brief and HERMES decision as a one-source messy canary. It uses exactly `docs/adr/adr.schema-base.md`, preserves the missing Markdown status as missing, preserves embedded `status: draft` only in sidecar/provenance, records schema/implementation-contract ambiguity, reports `conversion_candidate_blocked_pending_review`, and does not perform authority cutover, source mutation, schema change, bulk conversion, projection replacement, or database/storage authority work.

## Reviewed artifacts

- `docs/plans/implementation-brief.20260711.143800_adr-json-authority-messy-canary-slice-2.md`
- `docs/reviews/hermes-decision.20260711.144200_adr-json-authority-messy-canary-slice-2.md`
- `docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md`
- `dev/adr-json-authority-inventory-review-overrides-slice-1/`
- `dev/adr-json-authority-messy-canary-slice-2/manifest.json`
- `dev/adr-json-authority-messy-canary-slice-2/adr.schema-base.candidate-object.json`
- `dev/adr-json-authority-messy-canary-slice-2/conversion-evidence.json`
- `dev/adr-json-authority-messy-canary-slice-2/conflict-lossiness-report.json`
- `dev/adr-json-authority-messy-canary-slice-2/sidecar-provenance.json`
- `src/python/projectkoios/bootstrap/control_surface/adr/messy_canary.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrMessyCanaryRunner__schema_base.py`

## Conformance findings

### Exactly-one-source boundary

Conforms.

The evidence names exactly one source:

```text
docs/adr/adr.schema-base.md
```

`manifest.json` records `conversion_scope: exactly-one-source`; the candidate object records `source_count: 1` and only `docs/adr/adr.schema-base.md` in `sources`. No evidence artifact indicates conversion of any other ADR file.

### Missing-status preservation

Conforms.

The canary preserves missing Markdown status as missing:

- candidate object `content_candidate.status` is `null`;
- `status_preservation` says `missing in Markdown source; not invented`;
- conflict/lossiness report records `missing_status: true`, `observed_markdown_status: null`, and `normalized_status_candidate: null`;
- conversion evidence records `status_invented: false` and `normalized_status_inserted: false`.

The embedded JSON metadata value `status: draft` is preserved only in sidecar/provenance and conflict evidence, not promoted into observed Markdown status or ADR lifecycle authority.

### Ambiguity, conflict, and lossiness reporting

Conforms.

The implementation reports:

- outcome `conversion_candidate_blocked_pending_review`;
- schema validation blocked without invented status;
- `schema_implementation_contract_ambiguity`;
- manual review required;
- blocked from authority promotion;
- sidecar preservation of embedded metadata and source/provenance material.

Generated projection is intentionally omitted because producing a projection would risk implying schema-valid ADR content or require invented status. This is consistent with the brief's optional projection boundary.

### Reviewed inventory input

Conforms.

The candidate object and sidecar reference Slice 1 reviewed values for `docs/adr/adr.schema-base.md`:

- category `template_schema_contract`;
- disposition `manual_review_required`;
- authority effect `candidate`;
- automatic-conversion eligibility `false`;
- candidate-only/non-authority boundary preserved.

### Source/schema/conversion/storage boundaries

Conforms.

ATHENA found no evidence of:

- `docs/adr` mutation;
- `docs/schemas` changes;
- conversion of files other than the one canary source attempt;
- authoritative JSON ADR record creation;
- replacement projection generation;
- file moves/renames/deletes/archives;
- source status normalization;
- draft supersession;
- authority cutover;
- database/storage authority;
- mutable `.sqlite` or `.db` files under the Slice 2 evidence path.

## ATHENA validation rerun

Commands rerun from repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Result: `26 passed in 0.27s`.

```bash
uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Result: `Success: no issues found in 19 source files`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Result: `summary: 0 finding(s), 19 file(s)`.

```bash
find dev/adr-json-authority-messy-canary-slice-2 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-messy-canary-slice-2 \( -name '*.sqlite' -o -name '*.db' \) -print
git status --short -- docs/adr docs/schemas
git diff --check
```

Result: JSON validity passed; DB-file scan produced no output; `git status --short -- docs/adr docs/schemas` produced no output; `git diff --check` passed.

Additional spot checks confirmed:

- manifest source path is exactly `docs/adr/adr.schema-base.md`;
- candidate object source list contains only `docs/adr/adr.schema-base.md`;
- missing status is preserved as `null`;
- embedded metadata `status: draft` is sidecar/provenance only;
- candidate object schema validation is blocked;
- projection generation is false;
- blocked outcome is `conversion_candidate_blocked_pending_review`;
- all evidence objects preserve `authority_change: false` and `candidate_only: true`.

## Watchpoints for HERMES/USER final acceptance

1. This slice proves messy-canary conflict/lossiness behavior for one source only; it does not authorize corpus conversion, schema publication, or cutover.
2. The embedded `status: draft` remains source-side metadata in sidecar/provenance, not observed Markdown status or normalized ADR lifecycle status.
3. The canary is intentionally blocked pending review. Any later conversion/cutover slice must resolve or explicitly disposition missing status and schema/implementation-contract ambiguity.
4. `manifest.json` still contains pre-closeout `pending closeout validation` labels; the implementation report and this ATHENA review provide closeout validation evidence.
5. Because projection was omitted, this slice does not prove projection equality for this messy source; projection behavior remains a separate gate if later required.

## Non-authorizations preserved

This acceptance does not authorize:

- bulk ADR migration;
- conversion of any file beyond this one evidence-only canary attempt;
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

## KOIOS provenance addendum

ATHENA observed KOIOS provenance review at:

```text
workspaces/koios/working/provenance-review.20260711_adr-json-authority-messy-canary-slice-2.md
```

KOIOS accepted the slice with watchpoints as provenance-safe blocked/review-only messy canary evidence. ATHENA incorporates the KOIOS watchpoints into this review:

- This is successful messy-canary evidence because it remains blocked pending review; it must not be reinterpreted as completed conversion or proof that `adr.schema-base.md` can be auto-migrated.
- Embedded schema-record JSON may inform later schema/envelope design, but embedded `status: draft` remains sidecar/source metadata unless ATHENA/USER explicitly defines a mapping.
- Omitted projection is the correct conservative outcome for this source and should not be treated as missing implementation.
- Next proof points still need to test a messy-but-projectable source or extend conflict/lossiness handling while preserving candidate-only/no-mutation boundaries.

## Next owner

HERMES/USER final acceptance of this one-source messy canary evidence before any corpus dry-run, source mutation, schema publication, JSON authority cutover, bulk conversion, or migration slice proceeds.
