```json
{
  "title": "ADR template/schema contract repair planning slice 6",
  "artifact_type": "architecture-brief",
  "status": "draft-pending-hermes-user-approval",
  "datetime": "20260711.155500Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "parent_effort": "ADR rationalization / JSON-authoritative ADR store",
  "slice_name": "adr-template-schema-contract-repair-planning-slice-6",
  "target_source": "docs/adr/adr.adr-template-contract.md",
  "koios_input": "workspaces/koios/working/next-proof-input.20260711_template-schema-contract-repair-planning.md",
  "next_owner": "HERMES_USER"
}
```

# Architecture brief 20260711.155500: ADR template/schema contract repair planning slice 6

## Purpose

Plan the next safe repair path for `docs/adr/adr.adr-template-contract.md` without mutating the source.

Slice 5 classified this file as `template_or_schema_contract` with `current_but_needs_revision`, source-incomplete, status-casing, and stale/ambiguous authority flags. This slice should produce a review/planning artifact that decides whether the safest next path is to revise, replace, split, leave as-is, or defer the accepted-like template/schema contract.

The planning slice is about semantic/document-authority repair strategy only. It must not perform the repair.

## Control inputs

Required inputs:

- Slice 5 semantic rationalization: `docs/reviews/semantic-rationalization.20260711_adr-six-entry-slice-5.md`
- HERMES Slice 5 acceptance: `docs/reviews/hermes-acceptance.20260711.155200_adr-semantic-rationalization-six-entry-slice-5.md`
- KOIOS Slice 5 review: `workspaces/koios/working/provenance-review.20260711_adr-semantic-rationalization-six-entry-slice-5.md`
- Source under review: `docs/adr/adr.adr-template-contract.md`
- KOIOS repair-planning input: `workspaces/koios/working/next-proof-input.20260711_template-schema-contract-repair-planning.md`

Relevant authority/context surfaces to consult as needed:

- Current ADR schema: `docs/schemas/adr.schema.json`
- JSON-authority staged direction: `docs/adr/adr.json-authoritative-adr-store.draft.md`
- ADR bidirectional-object architecture: `docs/architecture/architecture.adr-bidirectional-objects.md`
- JSON ADR storage topology: `docs/architecture/architecture.json-adr-storage-topology.md`
- Lifecycle/naming authority: `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`
- Lifecycle consumption aid: `docs/policies/architecture.adr.lifecycle.md`
- ADR control-surface README: `docs/adr/README.md`
- Slice 4 evidence for this source: `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/`

## Target source

Exactly one source is in planning scope:

```text
docs/adr/adr.adr-template-contract.md
```

Do not add `docs/adr/adr.schema-base.md` to this slice. Slice 5 recommended it as a related future repair target, but HERMES selected template/schema contract repair planning now.

## Required output artifact

Produce one ATHENA planning/review artifact, preferred path:

```text
docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md
```

KOIOS also recommends this planning/review path if a review-brief style artifact is preferred:

```text
docs/plans/architecture-review-brief.20260711_adr-template-schema-contract-repair-planning-slice-6.md
```

The output must include:

- exact target source;
- current observed status/casing (`Accepted`), with no normalization;
- current claims that appear stale, mixed, or unsafe;
- comparison against current `docs/schemas/adr.schema.json` shape;
- comparison against staged JSON-authority direction and bidirectional object architecture;
- repair-path options;
- recommended path and rationale;
- explicit non-authority/non-mutation statement;
- follow-up slice proposal if repair execution is recommended.

## Issues to reconcile

The planning artifact must explicitly address these known issues:

1. **Status casing**
   - Source says `Accepted`.
   - Current lifecycle/schema vocabulary uses lowercase values such as `accepted`.
   - Planning must preserve observed casing and decide whether a future repair should normalize, preserve, or sidecar status casing.
   - This slice must not normalize status.

2. **Stale `routing` claims**
   - Source describes `routing` as schema content and includes a `## routing` section.
   - Current `docs/schemas/adr.schema.json` does not include top-level `routing` as a required/property field.
   - Planning must decide whether future repair should remove, sidecar, reframe, or preserve routing as historical/source material.
   - This slice must not edit schema or source.

3. **JSON-vs-Markdown source-of-truth claims**
   - Source says Markdown is a render target and JSON is the source of truth.
   - Current repository state has JSON-authority as accepted staged direction only, not cutover.
   - Planning must distinguish future target state from current authority.

4. **Template/schema-contract role**
   - Source mixes decision-record, template contract, schema authority, renderer behavior, workflow binding, and source-of-truth claims.
   - Planning must decide whether the future repair should be a revised ADR, replacement ADR, architecture note, schema-contract document, template document, or split surfaces.

5. **Migration implications**
   - Slice 4 showed this source is source-to-candidate incomplete and has omitted/source-preserved sections.
   - Planning must specify whether this file should be excluded from automatic migration until repaired, migrated with sidecar-only preservation, or used as a canary for template/schema repair.

## Repair path options to evaluate

Evaluate at least these options:

### Option A: Leave as-is with explicit classification

Keep the file unchanged and treat it as authority-relevant source/provenance until a larger ADR schema repair effort.

Questions:
- Is this safe enough for current work?
- What must tooling/migration know to avoid treating it as clean authority?

### Option B: Revise in place later

Plan a future HERMES/USER-approved source edit that preserves provenance while updating stale claims.

Questions:
- Which exact sections would be candidates for revision?
- How would observed `Accepted` status casing be handled?
- How would old claims about `routing`, JSON source-of-truth, and Markdown render target be corrected?

### Option C: Replacement ADR / supersession candidate later

Plan a new replacement ADR that supersedes or narrows this one after review.

Questions:
- What would the replacement decide?
- Would the original become superseded, source/provenance, or retained accepted historical evidence?
- What lifecycle authority is required before supersession?

### Option D: Split surfaces later

Plan a split into multiple surfaces, for example:

- ADR template/schema contract decision;
- schema shape authority in `docs/schemas/` or schema architecture;
- renderer/projection behavior in bidirectional-object/storage topology architecture;
- migration/source-of-truth policy in JSON-authoritative ADR store path.

Questions:
- Which content belongs where?
- Which future slice should create or revise which surface first?

### Option E: Defer pending broader schema-base repair

Leave the file untouched until `adr.schema-base.md` and schema-family concepts are rationalized.

Questions:
- Does deferral block JSON-authority staged migration?
- What temporary exclusion/watchpoint is needed?

## Recommended decision shape

The output should recommend exactly one primary next path plus, if needed, one fallback path.

The recommendation must be explicit about whether the next execution slice should be:

- review-only;
- source edit/revision;
- replacement ADR draft;
- architecture-note extraction;
- schema proposal;
- migration exclusion/sidecar policy update.

## Acceptance criteria

HERMES/USER may accept this planning slice only if:

1. It covers exactly `docs/adr/adr.adr-template-contract.md`.
2. It does not mutate source, schema, dev evidence, code, or lifecycle state.
3. It identifies stale/mixed claims around `Accepted`, `routing`, JSON-vs-Markdown authority, template/schema-contract role, and migration implications.
4. It compares those claims against current schema/lifecycle/JSON-authority surfaces.
5. It evaluates revise/replace/split/leave/defer options.
6. It recommends one bounded next path as proposal input only.
7. It preserves source status casing and does not normalize it.
8. It does not authorize supersession, promotion, demotion, source rewrite, schema change, JSON conversion, or cutover.

## Validation / closeout

Because this is a review/planning slice with no source changes expected, closeout should include:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

If execution requires source mutation, schema change, status change, supersession, or conversion, stop and request a new HERMES/USER-approved implementation/revision slice.

## Non-authorizations

This brief does not authorize:

- editing `docs/adr/adr.adr-template-contract.md`;
- editing any `docs/adr/` source;
- status normalization or lifecycle state changes;
- supersession, acceptance, activation, rejection, promotion, or demotion;
- file moves, renames, deletes, archives, or splits;
- edits to `docs/schemas/`;
- JSON conversion or projection generation;
- authoritative JSON ADR records;
- database/storage authority;
- migration or cutover.

## Pause gate

After this revised brief is drafted, pause again for HERMES/USER approval before executing the repair planning review.
