```json
{
  "title": "Architecture conformance review: ADR JSON authority inventory review/overrides slice 1",
  "artifact_type": "architecture-conformance-review",
  "status": "accepted-with-watchpoints",
  "datetime": "20260711.143300Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-inventory-review-overrides-slice-1",
  "reviewed_implementation": "docs/implementation/adr-json-authority-inventory-review-overrides-slice-1.20260711.143000.md",
  "source_brief": "docs/plans/implementation-brief.20260711.142200_adr-json-authority-inventory-review-overrides-slice-1.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.142700_adr-json-authority-inventory-review-overrides-slice-1.md",
  "source_recommendations": "workspaces/koios/working/override-recommendations.20260711_adr-json-authority-inventory-slice-1.md",
  "next_owner": "HERMES_USER"
}
```

# Architecture conformance review 20260711.143300: ADR JSON authority inventory review/overrides slice 1

## Verdict

Accepted with watchpoints for HERMES/USER final acceptance.

The implementation conforms to the Slice 1 brief and HERMES decision as review-only override evidence. It reviews all Slice 0 inventory entries, downgrades authority-forward `proposed_authority` labels to candidate-level planning evidence, applies KOIOS domain/provenance/category recommendations, preserves non-authority boundaries, and does not perform conversion or cutover.

## Reviewed artifacts

- `docs/plans/implementation-brief.20260711.142200_adr-json-authority-inventory-review-overrides-slice-1.md`
- `docs/reviews/hermes-decision.20260711.142700_adr-json-authority-inventory-review-overrides-slice-1.md`
- `workspaces/koios/working/override-recommendations.20260711_adr-json-authority-inventory-slice-1.md`
- `docs/implementation/adr-json-authority-inventory-review-overrides-slice-1.20260711.143000.md`
- `dev/adr-json-authority-inventory-classification-slice-0/source-inventory.json`
- `dev/adr-json-authority-inventory-review-overrides-slice-1/manifest.json`
- `dev/adr-json-authority-inventory-review-overrides-slice-1/reviewed-inventory.json`
- `dev/adr-json-authority-inventory-review-overrides-slice-1/overrides.json`
- `dev/adr-json-authority-inventory-review-overrides-slice-1/review-summary.json`
- `src/python/projectkoios/bootstrap/control_surface/adr/overrides.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrInventoryOverrideRunner__review.py`

## Conformance findings

### Review/override scope

Conforms.

The implementation produces review-only evidence under:

```text
dev/adr-json-authority-inventory-review-overrides-slice-1/
```

It emits the expected artifacts: `manifest.json`, `reviewed-inventory.json`, `overrides.json`, and `review-summary.json`.

All 43 Slice 0 entries are reviewed. The implementation report and review summary record:

- total reviewed: 43;
- changed decisions: 43;
- reviewed authority effects: 37 `candidate`, 5 `domain_review_required`, 1 `none`;
- automatic-conversion eligibility reduced to 17;
- primary messy canary recommendation: `docs/adr/adr.schema-base.md`.

### Authority-forward label correction

Conforms.

ATHENA spot-checked the generated decisions against the Slice 0 source inventory. Every source entry with `authority_effect: proposed_authority` or `disposition_candidate: json_authority_candidate` has a corresponding review decision with `candidate_only: true`. No reviewed decision retains `authority_effect: proposed_authority`.

`json_authority_candidate` remains in some reviewed dispositions only as candidate conversion-planning evidence, with top-level and per-decision non-authority markers.

### Domain/product and category review

Conforms.

The four KOIOS/HERMES called-out domain-review files are reviewed with `disposition_candidate: domain_review_required`, `domain_review_required: true`, and automatic conversion disabled:

- `docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md`
- `docs/adr/adr.agent-windows-on-message-triggers.draft.md`
- `docs/adr/adr.ui-core.draft.md`
- `docs/adr/adr.workflow-ui.draft.md`

The implementation also applies the KOIOS source/provenance and mixed-document review recommendations, including source-only provenance treatment for lifecycle/naming source drafts and manual-review handling for schema/template/architecture/policy mixed documents.

### Review-only authority boundary

Conforms.

The generated manifest and decisions preserve the required markers:

- `authority_change: false`
- `candidate_only: true`
- `source_mutation_allowed: false`
- `schema_change_allowed: false`
- `conversion_performed: false`
- `database_authority: false`

This slice does not make final per-file authority decisions.

### Source/schema/conversion/storage boundaries

Conforms.

ATHENA found no evidence of:

- `docs/adr` mutation;
- `docs/schemas` changes;
- authoritative JSON ADR records;
- Markdown-to-JSON conversion;
- generated projection replacement;
- file moves/renames/deletes/archives;
- source status normalization;
- draft supersession;
- database/storage authority;
- mutable `.sqlite` or `.db` files under the Slice 1 evidence path.

## ATHENA validation rerun

Commands rerun from repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Result: `22 passed in 0.26s`.

```bash
uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Result: `Success: no issues found in 17 source files`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Result: `summary: 0 finding(s), 17 file(s)`.

```bash
find dev/adr-json-authority-inventory-review-overrides-slice-1 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-inventory-review-overrides-slice-1 \( -name '*.sqlite' -o -name '*.db' \) -print
git diff --check
```

Result: JSON validity passed; DB-file scan produced no output; `git diff --check` passed.

Additional spot checks:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-inventory-review-overrides-slice-1
```

Result: only the new Slice 1 evidence directory was shown; `docs/adr` and `docs/schemas` had no output.

ATHENA also ran a script confirming:

- Slice 1 reviewed 43/43 Slice 0 entries;
- every review decision has `candidate_only: true`, `authority_change: false`, and `source_mutation: false`;
- no reviewed `authority_effect` remains `proposed_authority`;
- every Slice 0 authority-forward entry was reviewed;
- the four KOIOS domain-review paths are set to domain review and automatic-conversion false;
- the primary messy canary recommendation is `docs/adr/adr.schema-base.md`.

## Watchpoints for HERMES/USER final acceptance

1. This slice is safer review/override evidence, not conversion/cutover authority.
2. Remaining `json_authority_candidate` dispositions must still be read as candidate-only planning labels.
3. The reviewed inventory references the Slice 0 source inventory by path/hash rather than duplicating every observed status/casing field in each reviewed decision. Future automation must preserve the join to Slice 0 evidence or explicitly carry observed status/casing forward.
4. `manifest.json` still contains pre-closeout `pending closeout validation` labels in `validation_command_summary`; the implementation report and this ATHENA review provide closeout validation evidence.
5. HERMES/USER should explicitly accept or correct the reviewed override evidence before any messy canary, dry-run, source mutation, schema publication, JSON authority cutover, or migration slice consumes it.

## Non-authorizations preserved

This acceptance does not authorize:

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

## KOIOS provenance addendum

ATHENA observed a KOIOS provenance review for this slice at:

```text
workspaces/koios/working/provenance-review.20260711_adr-json-authority-inventory-review-overrides-slice-1.md
```

KOIOS found Slice 1 provenance-safe as review-only override evidence with minor watchpoints. ATHENA incorporates the KOIOS watchpoints into this review:

- `manifest.json` still carries pre-closeout `pending closeout validation` labels; implementation, KOIOS, and ATHENA reviews provide closeout validation evidence.
- Some remaining automatic-conversion-eligible entries still have imperfect category labels; later canary/conversion work must not treat category labels as final hierarchy truth.
- The remaining 17 automatic-conversion candidates still require a conversion/canary slice to prove unsupported-field preservation, projection equality, sidecar behavior, and conflict/lossiness reporting.
- `docs/adr/adr.schema-base.md` remains the recommended first messy canary after the clean `docs/adr/adr.json-schemas.draft.md` canary.

## Next owner

HERMES/USER final acceptance of this review-only override evidence before any follow-on migration work consumes the reviewed inventory.
