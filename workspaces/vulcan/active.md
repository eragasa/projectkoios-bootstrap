```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260704.123845",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": ["docs/plans/projectkoios-graphrag-next-slice.md"],
  "scratch_directory": "scratch/",
  "local_decision_record": "decisions/workspace.state.canonical.vulcan.20260704.123845.md",
  "controlling_workspace_policy": "docs/policies/workspace-layout.md"
}
```

# Vulcan active work

## Current priority stack

1. Implement `docs/plans/projectkoios-graphrag-next-slice.md`.
2. Preserve ADR-only, config-driven behavior while adding deterministic persisted index output.
3. Apply `docs/policies/python-coding.md` during Python implementation and closeout review.

## Waiting on

- No current blocker.
- Rebrief from ATHENA is required only if persisted index shape or citation metadata forces a broader retrieval redesign.

## Working material

- Active implementation source: `docs/plans/projectkoios-graphrag-next-slice.md`.
- Python coding control surface: `docs/policies/python-coding.md`.
- Prior implementation report: `docs/implementation/implementation-report.20260704.001003_graphrag-first-slice.md`.
- Prior process chain: `docs/process-capture/20260704_graphrag-first-slice-athena-vulcan-process-chain.md`.
- Active working items: no files under `working/` are active right now.
- Scratch: `scratch/` is available for temporary notes and non-durable exploration.

## Ignore for now

- second backend adapter
- embeddings or vector store integration
- graph database persistence
- UI/productization work
- AAR or workflow-log sources
- source-authority changes
- broad architecture refactors outside the active plan

## Exit criteria

The persisted-index slice is ready for handoff when:

- the index artifact is written deterministically
- repeated runs produce stable output for unchanged inputs
- CLI can build the index from config
- retrieval remains traceable to persisted index evidence
- citation fallback behavior still works
- existing query/answer behavior is preserved
- relevant tests pass
- Python changes have been self-reviewed against `docs/policies/python-coding.md`
- implementation report is written under `docs/implementation/`
- `state.md` and `active.md` are updated with the new validated state and next expected artifact
