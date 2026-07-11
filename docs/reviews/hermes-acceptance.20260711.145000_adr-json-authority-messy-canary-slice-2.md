```json
{
  "title": "HERMES acceptance: ADR JSON authority messy canary slice 2",
  "artifact_type": "hermes-acceptance",
  "status": "accepted-with-watchpoints",
  "datetime": "20260711.145000Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-messy-canary-slice-2",
  "implementation_report": "docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md",
  "architecture_review": "docs/reviews/architecture-conformance.20260711.144800_adr-json-authority-messy-canary-slice-2.md",
  "provenance_review": "workspaces/koios/working/provenance-review.20260711_adr-json-authority-messy-canary-slice-2.md",
  "next_owner": "HERMES_OR_USER"
}
```

# HERMES acceptance 20260711.145000: ADR JSON authority messy canary slice 2

## Verdict

Accepted with watchpoints.

HERMES accepts `adr-json-authority-messy-canary-slice-2` as a one-source, evidence-only messy canary that succeeds by blocking conversion pending review. This acceptance does not authorize corpus conversion, source mutation, schema publication, authoritative JSON ADR records, replacement projections, database/storage authority, or authority cutover.

## Basis

Reviewed inputs:

- `docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md`
- `docs/reviews/architecture-conformance.20260711.144800_adr-json-authority-messy-canary-slice-2.md`
- `workspaces/koios/working/provenance-review.20260711_adr-json-authority-messy-canary-slice-2.md`

ATHENA and KOIOS both accepted the slice with watchpoints. Both reviews agree that the implementation preserves the missing Markdown/ADR status, keeps embedded JSON `status: draft` as sidecar/source metadata only, records schema/implementation-contract ambiguity, and leaves the candidate blocked pending review.

## HERMES validation rerun

From repository root, HERMES reran:

```bash
uv run projectkoios workflow status
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
find dev/adr-json-authority-messy-canary-slice-2 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-messy-canary-slice-2 \( -name '*.sqlite' -o -name '*.db' \) -print
git status --short -- docs/adr docs/schemas
git diff --check
```

Observed results:

- Petri-net status reported `current-slice` at `user_decision`; enabled transition `approve_next_slice`; user decision required `yes`.
- Focused pytest: `26 passed in 0.23s`.
- Mypy: `Success: no issues found in 19 source files`.
- Python policy: `summary: 0 finding(s), 19 file(s)`.
- JSON validity passed for the Slice 2 evidence directory.
- DB-file scan produced no output.
- `git status --short -- docs/adr docs/schemas` produced no output.
- `git diff --check` passed.

## Accepted boundaries

Accepted as true for this slice:

- Exactly one source was attempted: `docs/adr/adr.schema-base.md`.
- The source remains unmodified.
- Missing Markdown/ADR status remains missing and is not invented.
- Embedded JSON `status: draft` remains sidecar/provenance metadata only.
- Outcome remains `conversion_candidate_blocked_pending_review`.
- Evidence remains candidate-only and non-authoritative.
- No projection was generated; omission is acceptable because projection could imply schema-valid content or require invented status.
- No ADR/schema mutation, status normalization, draft supersession, file move/rename/delete/archive, database/storage authority, or authority cutover occurred.

## Watchpoints

1. This acceptance proves one blocked messy canary only; it is not proof of corpus conversion, cutover readiness, or automatic migration readiness.
2. Embedded `status: draft` must not be promoted into ADR lifecycle/content status unless ATHENA/USER explicitly defines a later mapping.
3. Projection behavior is not proven by this slice because projection was conservatively omitted.
4. Later proof points should test either a messy-but-projectable source or richer conflict/lossiness handling while preserving candidate-only/no-mutation boundaries.
5. The workflow remains at a user-decision point before another bounded slice is activated or defined.

## Next owner

HERMES/USER for packaging/commit and deciding the next bounded ADR JSON authority proof point or workflow-engine action.
