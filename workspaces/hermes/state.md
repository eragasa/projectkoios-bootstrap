```json
{
  "title": "Hermes workspace state",
  "artifact_type": "workspace-state",
  "status": "active",
  "datetime": "20260711.160700Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/hermes/",
  "document_domain": "orchestration, repo-state reconciliation, cross-domain consistency",
  "control_files": ["state.md", "active.md"],
  "next_owner": "HERMES_OR_USER",
  "blockers": []
}
```

# Hermes workspace state

## Current focus

Close out accepted `adr-template-schema-contract-repair-planning-slice-6`, then choose the next bounded action.

## Current validated state

- Slice 5 is complete, committed, and pushed as `f2df856 Accept ADR semantic rationalization slice 5`.
- USER selected template/schema contract repair planning.
- KOIOS provided provenance input in `workspaces/koios/working/next-proof-input.20260711_template-schema-contract-repair-planning.md`.
- ATHENA produced `docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md`.
- KOIOS reviewed Slice 6 provenance in `workspaces/koios/working/provenance-review.20260711_adr-template-schema-contract-repair-planning-slice-6.md` and found it adequate for proposal-only acceptance/packaging with minor watchpoints.
- VULCAN provided implementation-reality input in `docs/reviews/implementation-reality.20260711_adr-template-schema-contract-repair-planning-slice-6.md`, supporting the plan and clarifying current code/schema/tooling constraints.
- HERMES accepted Slice 6 as proposal-only repair planning in `docs/reviews/hermes-acceptance.20260711.160700_adr-template-schema-contract-repair-planning-slice-6.md`.
- Closeout validation passed for planning-only scope:
  - `git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4` produced no output.
  - `git diff --check` passed.

## Accepted Slice 6 scope

Slice name:

```text
adr-template-schema-contract-repair-planning-slice-6
```

Target source:

```text
docs/adr/adr.adr-template-contract.md
```

Accepted repair plan:

```text
docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md
```

## Accepted recommendation

- Primary next path: draft a successor ADR/template-schema contract proposal in a future approved slice.
- Fallback: create a review-only errata/reconciliation note first if HERMES/USER wants lower-risk staging.
- Do not mutate `docs/adr/adr.adr-template-contract.md` in place as the first repair action.
- VULCAN implementation-reality constraints for successor planning:
  - current tooling treats `routing` as sidecar/provenance, not ADR content;
  - current tooling does not implement `dcn`;
  - `workflow_binding` is schema-supported but not operational workflow authority;
  - hand-authored Markdown remains source/control for unmigrated records and generated projections are non-authoritative evidence.

## Acceptance boundaries

Slice 6 acceptance is proposal-only. It does not authorize editing `docs/adr/adr.adr-template-contract.md`, editing any source ADR, status normalization or lifecycle state changes, formal supersession/acceptance/activation/rejection/promotion/demotion, schema changes, file moves/renames/deletes/archives/splits, JSON conversion/projection generation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, JSON authority cutover, or creating a successor ADR draft without future explicit approval.

## Current blockers

- None for accepted Slice 6.

## Next owner

- HERMES_OR_USER for packaging/commit and choosing the next bounded action.

## Current status summary

`adr-template-schema-contract-repair-planning-slice-6` is complete and accepted as proposal-only repair planning. The working tree contains Slice 6 planning/approval/review/acceptance artifacts plus role workspace state updates awaiting packaging/commit.
