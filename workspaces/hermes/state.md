```json
{
  "title": "Hermes workspace state",
  "artifact_type": "workspace-state",
  "status": "active",
  "datetime": "20260706.000000",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/hermes/",
  "document_domain": "orchestration, repo-state reconciliation, cross-domain consistency",
  "control_files": ["state.md", "active.md"],
  "next_owner": "HERMES",
  "blockers": []
}
```

# Hermes workspace state

## Current focus

- Reconcile workflow state after acceptance and implementation of the canonical workspace-state / next-action protocol.
- Preserve the boundary that workspace `state.md` and `active.md` are control surfaces, not replacements for ADRs, implementation reports, validation results, or knowledge notes.

## Validated current state

- Accepted ADR exists at `docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`.
- Proposal and historical draft are provenance/historical surfaces only.
- User separately authorized policy/bootstrap reconciliation after ADR acceptance.
- Vulcan completed the authorized reconciliation and reported it in `docs/implementation/implementation-report.20260705.003351_workspace-state-protocol-bootstrap-reconciliation.md`.
- Vulcan AAR exists at `docs/AAR/aar.20260705.003351_workspace-state-protocol-bootstrap-reconciliation.md`.
- Reported validation for that slice: focused workspace tests passed, mypy passed, python policy validator returned 0 findings, full pytest passed, and graphify update completed.
- Declared deferred gap was Hermes-owned control-surface update; this file and `active.md` now record that update.

## Repo closeout review

Hermes grouped the current dirty tree into these bounded slices:

1. Workspace-state protocol acceptance and reconciliation
   - Owner/evidence: ATHENA accepted ADR and VULCAN reconciliation report.
   - Key artifacts: `docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`, `docs/implementation/implementation-report.20260705.003351_workspace-state-protocol-bootstrap-reconciliation.md`, `docs/AAR/aar.20260705.003351_workspace-state-protocol-bootstrap-reconciliation.md`.
   - Key patch surfaces: workspace policy/architecture pointers, README, workspace bootstrap code/tests, role workspace control files.
   - Status: reported and locally spot-validated by Hermes.

2. Python policy validator and test-remediation chain
   - Owner/evidence: VULCAN implementation reports from `20260704.235450` through `20260705.002345`.
   - Key patch surfaces: `src/python/projectkoios/cli/main.py`, `src/python/projectkoios/bootstrap/commands/validate_python_policy.py`, Python-policy tests, schema tests, and ingestors tests.
   - Status: reported and locally spot-validated by Hermes.

3. Koios workspace seed/control files
   - Owner/evidence: KOIOS workspace control-surface files exist as untracked files.
   - Status: should be included only if user wants current Koios control state committed with the workspace protocol closeout; otherwise leave for Koios-specific review.

Hermes local validation after grouping:

- `git diff --check` => passed.
- `uv run pytest tests/test_bootstrap_flow.py tests/test__workspaces_command.py tests/projectkoios/bootstrap/python_policy tests/projectkoios/bootstrap/schema tests/projectkoios/ingestors -q` => `63 passed in 0.71s`.

## Blockers

- None for the Hermes control-surface update.

## Open questions

- Schema namespace reconciliation:
  - Should `adr-draft.schema.json` become `schema.adr-draft.json`, and if so what alias/registry strategy preserves existing `$id` and `schema_id` references?
  - Should `adr-active.schema.json` be renamed/reclassified as a candidate rather than implied canonical active schema?
  - Should `adr.schema-implementation.json` be retained and reclassified as an implementation-record schema candidate, then eventually renamed to something like `schema.implementation-record.json`?
  - Should `legacy-architecture.*.json` remain temporary provenance markers until a reconciliation artifact records what was preserved/superseded?
  - Should `architecture-note` / `subsystem-architecture` become a new schema family, owned first by Athena as architecture/schema design?
- Whether to commit as one integrated closeout or split into bounded commits by slice.
- Whether to include untracked Koios `state.md`/`active.md` in this closeout or route them to Koios for review first.
- Whether Koios should capture durable provenance after reconciliation and validation reports are committed.

## Next owner

- HERMES/user for prioritization.
- ATHENA for a bounded schema namespace / record-family naming reconciliation artifact if the user chooses to proceed.
- VULCAN only after an accepted schema reconciliation handoff authorizes code/test/schema registry changes.

## Current status summary

Repo-level closeout review is complete for prior slices. A new schema governance item has been added to Hermes' queue: reconcile schema filenames, `$id` conventions, candidate/legacy status, `adr.schema-implementation.json` classification, and possible architecture-note/subsystem-architecture schema work. This should be handled as an Athena-owned schema architecture artifact before any file renames or implementation changes.
