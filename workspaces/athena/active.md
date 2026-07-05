```json
{
  "title": "Athena active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260705.010958",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/athena/",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": [],
  "scratch_directory": "scratch/",
  "local_decision_record": "decisions/workspace.state.canonical.athena.20260704.041431.md",
  "controlling_workspace_policy": "docs/policies/workspace-layout.md"
}
```

# Athena active work

## Current priority stack

1. Petri-net definition/marking/binding/runtime separation ADR accepted at `docs/adr/adr.petrinet.20260705.132740Z.md`; VULCAN remediation report exists at `docs/implementation/implementation-report.20260705.142149_petrinet-separation-adr-remediation.md`; ATHENA conformance review exists at `docs/reviews/architecture-conformance.20260705.144506_petrinet-separation-adr-remediation.md` with outcome `conforms-with-followups`; next bounded follow-on is older workflow ADR/plan documentation reconciliation plus packaging/commit.
2. Template representation and namespace split proposal now has a schema-backed draft record at `dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.record.json` and generated projection at `dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.schema-backed.md`; await HERMES/user review before acceptance or Vulcan handoff.
3. Keep Athena work bounded to architecture/spec surfaces while VULCAN-owned dirty implementation/test work remains present.

## Waiting on

- Push/closeout item resolved as of startup check: `git status --short --branch` reported `## master...origin/master` with no ahead/behind or dirty files.
- No remaining dirty/untracked files were present at startup check.
- Petri-net separation accepted ADR: `docs/adr/adr.petrinet.20260705.132740Z.md`; VULCAN implementation routing returned validated remediation; ATHENA conformance review completed at `docs/reviews/architecture-conformance.20260705.144506_petrinet-separation-adr-remediation.md`; older workflow ADR/plan documentation-control follow-on remains separate.
- HERMES/user review decision for `dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.proposed.md`.
- Hermes/user direction before editing `docs/architecture/architecture.workspaces.00.md` or `docs/architecture/architecture.00.md`.
- Authority check before turning any draft ADR or plan into implementation authority.
- Any needed action by another role/agent should be sent as an explicit intercom handoff/request, then recorded here as waiting-on.
- Schema-base conformance review output exists at `docs/reviews/architecture-conformance.20260704.212913_schema-record-base-slice.md` with outcome `conforms-with-gaps`.
- Template representation proposal: `dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.proposed.md`.
- Template representation schema-backed draft: `dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.record.json`; generated projection: `dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.schema-backed.md`.
- Petri-net separation accepted ADR: `docs/adr/adr.petrinet.20260705.132740Z.md`; source record: `dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.record.json`; generated projection: `dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.schema-backed.md`; durable sources: `dev/petrinet-definition-marking-runtime/user-proposal.20260705.132740_petrinet-definition-marking-runtime.md`, `dev/petrinet-definition-marking-runtime/decision-source-addendum.20260705.md`.
- ADR lifecycle/naming consolidation proposal provenance: `dev/adr-lifecycle-and-naming-consolidation/adr.adr-lifecycle-and-naming-consolidation.proposed.md`.

## Working material

- Active working items: `docs/adr/adr.schema-base.md`, `docs/plans/schema-base-adr-records-workplan.md`, `docs/plans/implementation-brief.20260704.172632_schema-record-base.md`, `docs/schemas/README.md`, `docs/schemas/schema.record-base.json`, `docs/schemas/adr-draft.schema.json`, `docs/implementation/implementation-report.20260704.174859_schema-record-base.md`.
- Workspace-state accepted ADR: `docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`; proposal retained as review provenance at `dev/canonical-workspace-state-next-action-protocol/adr.canonical-workspace-state-next-action-protocol.proposed.md`; historical draft `docs/adr/adr.canonical-workspace-state-next-action-protocol.draft.md` points to the accepted ADR.
- Conformance-review output: `docs/reviews/architecture-conformance.20260704.212913_schema-record-base-slice.md`; outcome `conforms-with-gaps`; gap is shallow immutability in metadata/generic mappings.
- Scratch: `scratch/` is available for temporary notes and non-durable exploration.
- Note: files may exist under `working/` as transitional artifacts; they are not active unless explicitly re-opened.
- `working/` has no `incoming/` or `outgoing/` subdirectories.

## Ignore for now

- Broad ADR lifecycle refactors.
- Full-repo archive cleanup.
- Machine-readable companion schema design outside the schema-base ADR scope.
- Further implementation work from this Athena workspace.
- Any attempt to implement or test the GraphRAG persisted-index slice from Athena.
- Editing Python implementation files while Vulcan has active/shared-tree work.

## Exit criteria

Athena state is stable when a new session can read `state.md`, `active.md`, and any active `working/` material, then identify the represented role, current scope, validated state, open questions, next transition, and ignored scope without chat history.
