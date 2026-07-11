# AAR 20260712: ADR successor activation role-boundary recovery

## Scope

HERMES session in `projectkoios-bootstrap` reconciling workflow queue visibility with accepted ADR successor-planning state and activating `adr-template-schema-contract-successor-draft-slice-11`.

## What happened

- Startup workflow status showed no active slice and queue showed only `pi-skill-determinism-slice-0`, while accepted Slice 10 docs recommended `adr-template-schema-contract-successor-draft-slice-11`.
- HERMES reconciled the queue fixture so Slice 11 is visible as the recommended next item and committed that as `c0c6e482`.
- USER said `go`, meaning proceed with the recommended action within the meta-harness framework.
- HERMES correctly activated Slice 11 and reconciled workflow status to show the active slice.
- HERMES then incorrectly authored an ATHENA-owned ADR draft directly. That exceeded the HERMES orchestration role boundary.
- Recovery removed the draft artifact and kept only the HERMES-owned activation/routing state.

## Process issues

- HERMES interpreted `go` too broadly and bundled role-owned artifact production into workflow activation.
- The correct HERMES action was to activate/route the slice, then stop with ATHENA as next owner for ADR drafting.
- Delegated-operator provenance is not a substitute for the owning role/harness when the user has not explicitly authorized cross-role authorship.

## Proposed follow-up improvements

- Treat `go` as permission to proceed only with the previously recommended action and only within the current role's authority.
- For role-owned artifacts, HERMES MUST stop after routing/activation unless USER explicitly delegates that role-owned artifact production and provenance is recorded.
- Add a startup/recovery checklist that compares workflow queue state with recent HERMES acceptance artifacts when the user asks what happened or what is next.

## Candidate ADR or implementation topics

- Workflow queue/document-state reconciliation rule.
- Delegated-operator provenance policy for unavailable role harnesses.
- HERMES guardrail: activation is not authorization to produce another role's artifact.

## Current status

Slice 11 is active in the workflow fixtures. The ATHENA-owned successor ADR draft was removed during recovery. Next owner is ATHENA for drafting `docs/adr/adr.adr-template-schema-contract.draft.md` from the accepted successor brief.
