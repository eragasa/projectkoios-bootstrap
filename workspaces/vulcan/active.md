```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "review-handoff",
  "datetime": "20260704.151640",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "priority_count": 2,
  "working_directory": "working/",
  "active_working_items": [
    "docs/implementation/implementation-report.20260704.151640_graphrag-persisted-index.md",
    "graph/index.json"
  ],
  "scratch_directory": "scratch/",
  "controlling_workspace_policy": "docs/policies/workspace-layout.md"
}
```

# Vulcan active work

## Current priority stack

1. Hand off GraphRAG persisted-index implementation for ATHENA conformance review.
2. Await review feedback or user instruction for the next implementation slice.

## Waiting on

- ATHENA review of `docs/implementation/implementation-report.20260704.151640_graphrag-persisted-index.md` and the associated patch.
- No implementation blocker currently.

## Working material

- Controlling implementation source: `docs/plans/projectkoios-graphrag-next-slice.md`.
- Implementation plan: `docs/plans/implementation-plan.20260704.150233_graphrag-persisted-index.md`.
- Execution brief: `docs/plans/implementation-brief.20260704.150233_graphrag-persisted-index.md`.
- Implementation report: `docs/implementation/implementation-report.20260704.151640_graphrag-persisted-index.md`.
- Generated artifact: `graph/index.json`.
- Python coding control surface: `docs/policies/python-coding.md`.
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

The persisted-index slice is ready for review handoff when:

- the index artifact is written deterministically — complete
- repeated runs produce stable output for unchanged inputs — complete
- CLI can build the index from config — complete
- retrieval remains traceable to persisted index evidence — complete
- citation fallback behavior still works — complete
- existing query/answer behavior is preserved — complete
- relevant tests pass — complete
- Python changes have been self-reviewed against `docs/policies/python-coding.md` — complete
- implementation report is written under `docs/implementation/` — complete
- `state.md` and `active.md` are updated with the new validated state and next expected artifact — complete

## Next expected artifact

- ATHENA conformance review linked to `docs/implementation/implementation-report.20260704.151640_graphrag-persisted-index.md`.
