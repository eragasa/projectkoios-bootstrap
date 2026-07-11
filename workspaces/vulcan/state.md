```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "adr-json-authority-projectable-messy-canary-slice-3-implemented-validated-pending-review",
  "datetime": "20260711.150000Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "document_domain": "implementation, tests, validation, implementation reports, deviation reports",
  "source_brief": "docs/plans/implementation-brief.20260711.145300_adr-json-authority-projectable-messy-canary-slice-3.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.145600_adr-json-authority-projectable-messy-canary-slice-3.md",
  "koios_input": "workspaces/koios/working/next-proof-input.20260711_adr-json-authority-after-messy-canary-slice-2.md",
  "slice_name": "adr-json-authority-projectable-messy-canary-slice-3",
  "latest_report": "docs/implementation/adr-json-authority-projectable-messy-canary-slice-3.20260711.150000.md",
  "latest_aar": "docs/AAR/aar.20260711.150000_adr-json-authority-projectable-messy-canary-slice-3.md",
  "evidence_dir": "dev/adr-json-authority-projectable-messy-canary-slice-3/",
  "control_files": ["state.md", "active.md"],
  "next_owner": "KOIOS_ATHENA_REVIEW",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

- Current scope: implemented and validated ADR JSON authority projectable messy canary Slice 3.
- Slice name: `adr-json-authority-projectable-messy-canary-slice-3`.
- Exact source: `docs/adr/adr.adr-template-contract.md`.
- Evidence directory: `dev/adr-json-authority-projectable-messy-canary-slice-3/`.
- Brief: `docs/plans/implementation-brief.20260711.145300_adr-json-authority-projectable-messy-canary-slice-3.md`.
- HERMES decision: `docs/reviews/hermes-decision.20260711.145600_adr-json-authority-projectable-messy-canary-slice-3.md`.
- KOIOS input: `workspaces/koios/working/next-proof-input.20260711_adr-json-authority-after-messy-canary-slice-2.md`.
- Report: `docs/implementation/adr-json-authority-projectable-messy-canary-slice-3.20260711.150000.md`.
- AAR: `docs/AAR/aar.20260711.150000_adr-json-authority-projectable-messy-canary-slice-3.md`.

## Current status

- Projectable messy canary evidence exists under `dev/adr-json-authority-projectable-messy-canary-slice-3/`.
- Observed Markdown status `Accepted` is preserved separately from normalized candidate `accepted`.
- Generated projection exists only under the Slice 3 `dev/` evidence path and is visibly non-authoritative.
- KOIOS-identified wrapped-list continuation lossiness is corrected; candidate/projection now preserve `Workflow-bound ADRs can render optional gate fields without losing schema consistency.`
- Parse-back reads only generated projection evidence and preserves `Accepted` casing.
- Template/schema-contract ambiguity and manual-review blockers remain explicit.
- Outcome is `projectable_candidate_blocked_pending_template_contract_and_status_review`.
- No ADR source authority, schema authority, storage authority, lifecycle status, filenames, or Markdown source content is changed.

## Validation evidence

From repository root:

- `uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q` => `30 passed in 0.27s`.
- `uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr` => `Success: no issues found in 21 source files`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr` => `summary: 0 finding(s), 21 file(s)`.
- `find dev/adr-json-authority-projectable-messy-canary-slice-3 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null` => passed.
- `find dev/adr-json-authority-projectable-messy-canary-slice-3 \( -name '*.sqlite' -o -name '*.db' \) -print` => no output.
- `git status --short -- docs/adr docs/schemas` => no output.
- `find dev/adr-json-authority-projectable-messy-canary-slice-3 -name 'generated-projection.md' -print` => only the Slice 3 projection path.
- `git diff --check` => passed.

## Dirty tree caution

Treat VULCAN-owned changes for this slice as:

- `dev/adr-json-authority-projectable-messy-canary-slice-3/`
- `src/python/projectkoios/bootstrap/control_surface/adr/projectable_messy_canary.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrProjectableMessyCanaryRunner__template_contract.py`
- `docs/implementation/adr-json-authority-projectable-messy-canary-slice-3.20260711.150000.md`
- `docs/AAR/aar.20260711.150000_adr-json-authority-projectable-messy-canary-slice-3.md`
- `workspaces/vulcan/active.md`
- `workspaces/vulcan/state.md`

Known ATHENA/HERMES/KOIOS authorizing files and workspace state may also exist in the dirty tree. Keep commit boundaries explicit.

## Next transition

- Owner: KOIOS and ATHENA review, then HERMES acceptance.
- Expected action: KOIOS provenance review and ATHENA architecture/conformance review of Slice 3 evidence before HERMES final acceptance.
- Blockers: none from VULCAN.
