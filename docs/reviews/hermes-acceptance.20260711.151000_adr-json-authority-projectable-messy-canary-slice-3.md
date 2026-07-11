```json
{
  "title": "HERMES acceptance: ADR JSON authority projectable messy canary slice 3",
  "artifact_type": "completion-decision",
  "status": "accepted-with-watchpoints",
  "datetime": "20260711.151000Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-projectable-messy-canary-slice-3",
  "implementation_report": "docs/implementation/adr-json-authority-projectable-messy-canary-slice-3.20260711.150000.md",
  "athena_review": "docs/reviews/architecture-conformance.20260711.150700_adr-json-authority-projectable-messy-canary-slice-3-post-remediation.md",
  "athena_prior_review": "docs/reviews/architecture-conformance.20260711.150300_adr-json-authority-projectable-messy-canary-slice-3.md",
  "koios_review": "workspaces/koios/working/provenance-review.20260711_adr-json-authority-projectable-messy-canary-slice-3.md",
  "evidence_dir": "dev/adr-json-authority-projectable-messy-canary-slice-3/",
  "next_owner": "HERMES_OR_USER"
}
```

# HERMES acceptance 20260711.151000: ADR JSON authority projectable messy canary slice 3

## Decision

HERMES accepts `adr-json-authority-projectable-messy-canary-slice-3` with watchpoints.

## Accepted scope

This acceptance covers exactly one projectable messy canary source:

```text
docs/adr/adr.adr-template-contract.md
```

Accepted evidence lives under:

```text
dev/adr-json-authority-projectable-messy-canary-slice-3/
```

The accepted outcome is:

```text
projectable_candidate_blocked_pending_template_contract_and_status_review
```

## Acceptance basis

HERMES reviewed the implementation report, corrected evidence, KOIOS revised provenance review, ATHENA prior blocker-incorporating conformance review, and ATHENA post-remediation conformance review.

The previous KOIOS blocker is resolved: the wrapped source acceptance-criteria item is now preserved in candidate/projection evidence as:

```text
Workflow-bound ADRs can render optional gate fields without losing schema consistency.
```

Accepted findings:

- Exactly one source was converted/projected as candidate evidence: `docs/adr/adr.adr-template-contract.md`.
- Observed Markdown status/casing `Accepted` is preserved separately from normalized candidate `accepted`.
- Status normalization remains review-only and was not applied to source Markdown.
- Template/schema-contract ambiguity remains explicit.
- Manual review remains blocking.
- Projection is generated only under the Slice 3 `dev/` evidence path and is non-authoritative.
- Parse-back reads only the generated projection and does not resolve review blockers.
- Candidate/projection semantic equality is accepted only for candidate fields and only for this one generated evidence record.
- Evidence remains `candidate_only: true` and `authority_change: false`.

## Independent HERMES validation

HERMES independently reran or observed clean validation for:

- `uv run projectkoios workflow status`
- `uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q`
- `uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr`
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr`
- JSON validity for Slice 3 evidence JSON files
- DB-file scan under Slice 3 evidence path
- `git status --short -- docs/adr docs/schemas`
- `git diff --check`

Validation passed: 30 tests, mypy clean, 0 policy findings, JSON valid, no DB files, no `docs/adr` or `docs/schemas` mutation, diff-check clean.

Petri-net workflow status remained at user decision and HERMES did not mutate workflow state.

## Watchpoints

This acceptance is bounded and does not authorize:

- corpus conversion;
- conversion or projection of any file beyond `docs/adr/adr.adr-template-contract.md`;
- authoritative JSON ADR records;
- source Markdown mutation;
- source status normalization;
- schema publication or schema changes;
- file moves, renames, deletes, or archives;
- draft supersession;
- database/storage authority;
- mutable `.sqlite` or `.db` files;
- JSON authority cutover;
- bulk migration.

Remaining review questions before broader migration:

- how template/schema-contract ADRs should be promoted, excluded, or represented in authoritative JSON;
- how noncanonical status casing should be normalized, if ever, and under whose authority;
- how corpus dry-run selection should report source-to-candidate lossiness across multiple files;
- how final authority location/cutover should be gated.
