```json
{
  "title": "HERMES decision: ADR template/schema contract successor draft slice 11",
  "artifact_type": "workflow-decision",
  "status": "packaged-draft-for-review",
  "datetime": "20260711.181920Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-template-schema-contract-successor-draft-slice-11",
  "draft_artifact": "docs/adr/adr.adr-template-schema-contract.draft.md",
  "next_owner": "HERMES_USER"
}
```

# HERMES decision 20260711.181920: ADR template/schema contract successor draft slice 11

## Decision

HERMES packages the ATHENA-authored successor draft `docs/adr/adr.adr-template-schema-contract.draft.md` as the Slice 11 draft artifact for USER/HERMES review and later acceptance consideration.

This decision does not accept, activate, supersede, or otherwise change ADR authority.

## Checklist verified

- Root `AGENTS.md` checked.
- Hermes workspace `AGENTS.md` checked.
- `workspaces/hermes/state.md` and `workspaces/hermes/active.md` checked.
- Document-domain owner for the draft artifact: ATHENA.
- HERMES role: orchestration, review packaging, and cross-domain consistency only.
- Required reviews before HERMES packaging: ATHENA draft present; VULCAN implementation-reality review received; KOIOS provenance review received.
- USER waiver: none needed for packaging the draft as draft-only; no cross-role artifact production by HERMES occurred.

## Review inputs

ATHENA authored/reconstructed the draft fresh after HERMES routed the active Slice 11 work to the ATHENA session. Invalid HERMES reflog and Archon/Codex drafts were treated as non-authoritative and were not used as source text.

VULCAN implementation-reality review reported:

- verdict: implementation-feasible / no blocking implementation objection;
- blockers: none;
- watchpoints: parser/ingester compatibility if immediate machine ingest is requested, future source-disposition decisions, and preserving `metadata.record_id` / `dcn` distinction.

KOIOS provenance review reported:

- verdict: provenance-adequate for HERMES/USER review / no blocking provenance issues;
- blockers: none;
- watchpoints: later explicit relation decision for `docs/adr/adr.adr-template-contract.md`, draft-internal proposed resolutions becoming authority only if/when accepted, invalid drafts remaining non-authoritative, and closeout checks before packaging.

## What this authorizes

This decision authorizes committing the draft artifact and HERMES packaging state as a draft-only workflow state change.

## What this does not authorize

This decision does not authorize:

- accepting or activating `docs/adr/adr.adr-template-schema-contract.draft.md`;
- superseding, editing, normalizing, moving, renaming, deleting, archiving, splitting, promoting, demoting, or rejecting `docs/adr/adr.adr-template-contract.md`;
- editing `docs/schemas/`;
- changing source status or casing;
- migrating ADR records;
- generating or replacing projections;
- creating authoritative JSON ADR records;
- database/storage authority changes;
- JSON authority cutover;
- Petri-net workflow runtime, Operator Console, or lifecycle authority changes.

## Closeout validation

HERMES ran:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Observed result at packaging time: only the new successor draft appeared under `docs/adr/` on the constrained surface; no `docs/schemas` or Slice 4 dry-run evidence mutation; diff hygiene passed.

## Next required decision

HERMES_USER must decide a later relation and lifecycle path for the draft, including whether it remains draft-only, is revised, is accepted, or is used to make a separate source-disposition decision for `docs/adr/adr.adr-template-contract.md`.
