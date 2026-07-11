```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "adr-json-authority-messy-canary-slice-2-implemented-validated",
  "datetime": "20260711.144500Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "document_domain": "implementation, tests, validation, implementation reports, deviation reports",
  "source_brief": "docs/plans/implementation-brief.20260711.143800_adr-json-authority-messy-canary-slice-2.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.144200_adr-json-authority-messy-canary-slice-2.md",
  "source_inventory": "dev/adr-json-authority-inventory-review-overrides-slice-1/",
  "slice_name": "adr-json-authority-messy-canary-slice-2",
  "latest_report": "docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md",
  "latest_aar": "docs/AAR/aar.20260711.144500_adr-json-authority-messy-canary-slice-2.md",
  "evidence_dir": "dev/adr-json-authority-messy-canary-slice-2/",
  "control_files": ["state.md", "active.md"],
  "next_owner": "HERMES_USER_REVIEW",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

- Current scope: implemented and validated ADR JSON authority messy canary Slice 2.
- Slice name: `adr-json-authority-messy-canary-slice-2`.
- Exact source: `docs/adr/adr.schema-base.md`.
- Evidence directory: `dev/adr-json-authority-messy-canary-slice-2/`.
- Brief: `docs/plans/implementation-brief.20260711.143800_adr-json-authority-messy-canary-slice-2.md`.
- HERMES decision: `docs/reviews/hermes-decision.20260711.144200_adr-json-authority-messy-canary-slice-2.md`.
- Report: `docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md`.

## Current status

- Messy canary evidence exists under `dev/adr-json-authority-messy-canary-slice-2/`.
- Missing Markdown status is preserved as missing; embedded JSON `status: draft` is sidecar/provenance only.
- Schema/implementation-contract ambiguity is explicit.
- Outcome is `conversion_candidate_blocked_pending_review`.
- No generated projection was produced because projection would risk implying schema-valid ADR content or require invented status.
- No ADR source authority, schema authority, storage authority, lifecycle status, filenames, or Markdown source content is changed.

## Validation evidence

From repository root:

- `uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q` => `26 passed in 0.23s`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr` => `summary: 0 finding(s), 19 file(s)`.
- `find dev/adr-json-authority-messy-canary-slice-2 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null` => passed.
- `find dev/adr-json-authority-messy-canary-slice-2 \( -name '*.sqlite' -o -name '*.db' \) -print` => no output.
- `git status --short -- docs/adr docs/schemas` => no output.
- `git diff --check` => passed.
- Source/schema stability check around regeneration: before/after corpus hash matched, `stable_source_schema_hash=yes`.
- Evidence determinism check: repeated evidence hash matched, `stable_evidence_hash=yes`.

## Dirty tree caution

Treat VULCAN-owned changes for this slice as:

- `dev/adr-json-authority-messy-canary-slice-2/`
- `src/python/projectkoios/bootstrap/control_surface/adr/messy_canary.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrMessyCanaryRunner__schema_base.py`
- `docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md`
- `docs/AAR/aar.20260711.144500_adr-json-authority-messy-canary-slice-2.md`
- `workspaces/vulcan/active.md`
- `workspaces/vulcan/state.md`

Known ATHENA/HERMES authorizing files and workspace state may also exist in the dirty tree. Keep commit boundaries explicit.

## Next transition

- Owner: HERMES/USER review.
- Expected action: review messy canary evidence before any corpus dry-run, source mutation, schema publication, JSON authority cutover, bulk conversion, or migration slice.
- Blockers: none from VULCAN.
