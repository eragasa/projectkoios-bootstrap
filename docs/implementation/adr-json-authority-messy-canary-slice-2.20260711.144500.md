```json
{
  "title": "ADR JSON authority messy canary slice 2 implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated",
  "datetime": "20260711.144500Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_brief": "docs/plans/implementation-brief.20260711.143800_adr-json-authority-messy-canary-slice-2.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.144200_adr-json-authority-messy-canary-slice-2.md",
  "source_inventory": "dev/adr-json-authority-inventory-review-overrides-slice-1/",
  "slice_name": "adr-json-authority-messy-canary-slice-2",
  "evidence_dir": "dev/adr-json-authority-messy-canary-slice-2/",
  "next_owner": "HERMES_USER_REVIEW"
}
```

# Implementation report 20260711.144500: ADR JSON authority messy canary slice 2

## Summary

Implemented the one-source messy canary for:

```text
docs/adr/adr.schema-base.md
```

The canary preserves the missing Markdown status as missing, keeps embedded JSON status as sidecar/provenance only, and reports the outcome as:

```text
conversion_candidate_blocked_pending_review
```

No status was invented to satisfy schema validation. No authoritative JSON ADR record, replacement projection, source mutation, schema change, or database/storage authority was created.

## Changed files

Implementation and tests:

- `src/python/projectkoios/bootstrap/control_surface/adr/messy_canary.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrMessyCanaryRunner__schema_base.py`

Generated canary evidence:

- `dev/adr-json-authority-messy-canary-slice-2/manifest.json`
- `dev/adr-json-authority-messy-canary-slice-2/adr.schema-base.candidate-object.json`
- `dev/adr-json-authority-messy-canary-slice-2/conversion-evidence.json`
- `dev/adr-json-authority-messy-canary-slice-2/conflict-lossiness-report.json`
- `dev/adr-json-authority-messy-canary-slice-2/sidecar-provenance.json`

Workspace/reporting:

- `docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md`
- `docs/AAR/aar.20260711.144500_adr-json-authority-messy-canary-slice-2.md`
- `workspaces/vulcan/state.md`
- `workspaces/vulcan/active.md`

## Evidence behavior

- Consumes Slice 1 reviewed inventory evidence for `docs/adr/adr.schema-base.md`.
- Uses exactly one source file.
- Parses the source H1 title.
- Preserves absent Markdown status as `null` / missing.
- Preserves embedded JSON metadata, including embedded `status: draft`, in sidecar/provenance only.
- Records reviewed Slice 1 category/disposition/authority-effect values.
- Records schema/implementation-contract ambiguity explicitly.
- Omits generated projection because generating a projection would risk implying schema-valid ADR content or require invented status.

## Validation

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Result: `26 passed in 0.23s`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Result: `summary: 0 finding(s), 19 file(s)`.

```bash
find dev/adr-json-authority-messy-canary-slice-2 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
```

Result: passed for all generated JSON evidence files.

```bash
find dev/adr-json-authority-messy-canary-slice-2 \( -name '*.sqlite' -o -name '*.db' \) -print
```

Result: no output.

```bash
git status --short -- docs/adr docs/schemas
```

Result: no output.

```bash
git diff --check
```

Result: passed.

Source/schema non-mutation and deterministic evidence check:

```text
source_schema_hash_before=ca79b7f67852dd3d42cdce7dabc919831e49a0577a6ed7bae2b5e3694d4da3fa
source_schema_hash_after=ca79b7f67852dd3d42cdce7dabc919831e49a0577a6ed7bae2b5e3694d4da3fa
stable_source_schema_hash=yes
evidence_hash_first=7a50dd2a6095becb3ab1c66c9ff1e995a77276d8c44a5ad2e8fe3b0c74cdeaee
evidence_hash_second=7a50dd2a6095becb3ab1c66c9ff1e995a77276d8c44a5ad2e8fe3b0c74cdeaee
stable_evidence_hash=yes
```

## Boundary confirmation

Preserved boundaries:

- No `docs/adr` mutation.
- No `docs/schemas` changes.
- No conversion of any file except the one canary source attempt.
- No authoritative JSON ADR records.
- No replacement projections.
- No file moves, renames, deletes, or archives.
- No source status normalization.
- No draft supersession.
- No authority cutover.
- No database/storage authority.
- No mutable `.sqlite` or `.db` evidence files.

## Next owner

HERMES/USER review of `dev/adr-json-authority-messy-canary-slice-2/` before any corpus dry-run, source mutation, schema publication, JSON authority cutover, bulk conversion, or migration slice proceeds.
