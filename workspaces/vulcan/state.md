```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "active",
  "datetime": "20260704.123845",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "document_domain": "implementation, tests, validation, implementation reports, deviation reports",
  "controlling_workspace_policy": "docs/policies/workspace-layout.md",
  "process_model": "docs/process-capture/workflow.process-capture.md",
  "python_coding_policy": "docs/policies/python-coding.md",
  "control_files": ["state.md", "active.md"],
  "workspace_material_dirs": {
    "working": "working/",
    "scratch": "scratch/",
    "decisions": "decisions/",
    "sessions": "sessions/"
  },
  "local_decision_record": "decisions/workspace.state.canonical.vulcan.20260704.123845.md",
  "next_owner": "VULCAN",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

- Focus: GraphRAG persisted-index next slice.
- Active implementation source: `docs/plans/projectkoios-graphrag-next-slice.md`.
- Previous completed slice: GraphRAG first slice.
- Previous implementation report: `docs/implementation/implementation-report.20260704.001003_graphrag-first-slice.md`.
- Process chain: `docs/process-capture/20260704_graphrag-first-slice-athena-vulcan-process-chain.md`.
- Authority boundary: Vulcan implements accepted filesystem-visible work items and records validation evidence; Vulcan does not create architecture authority.

## Validated state

- Workspace layout policy uses `AGENTS.md`, `state.md`, `active.md`, `decisions/`, `working/`, `scratch/`, and `sessions/`.
- Python implementation is governed by the draft Vulcan coding control surface at `docs/policies/python-coding.md`.
- `state.md` is the durable Vulcan resume snapshot.
- `active.md` is the current implementation queue and exit criteria.
- `working/` exists for transitional implementation material only; files in `working/` are not active unless named in `active.md`.
- Durable implementation output belongs in public docs surfaces, primarily `docs/plans/` and `docs/implementation/`.
- GraphRAG first slice is complete, reported, reviewed by ATHENA, and captured as a process chain.
- Current repo validation last known after workspace layout commit: `.venv/bin/python3 -m pytest -q` => `170 passed`; `koios validate` => `schema=True runtime=True sources=38`.

## Open questions

- Exact persisted index JSON shape for the next GraphRAG slice is governed by `docs/plans/projectkoios-graphrag-next-slice.md`; if implementation pressure requires a broader retrieval redesign, stop and request rebriefing.
- Whether a durable ATHENA review artifact should be created for future slices instead of relying on intercom review text.
- Whether Vulcan session logs should be written for every multi-turn implementation run or only for interrupted/long-running runs.

## Next transition

- Owner: VULCAN.
- Highest-leverage next action: implement the persisted-index slice from `docs/plans/projectkoios-graphrag-next-slice.md`.
- Expected successor artifact after implementation: `docs/implementation/implementation-report.<timestamp>_graphrag-persisted-index.md`.
- Expected review artifact after report: ATHENA conformance review linked to the implementation report.
- Blockers: none currently.

## Startup checklist

1. Confirm represented role from workspace and user request.
2. Read `state.md` and `active.md`.
3. Read `docs/plans/projectkoios-graphrag-next-slice.md` before changing code.
4. Check `git status --short --branch`.
5. Read `docs/policies/python-coding.md` before Python implementation work.
6. Run focused tests if touching existing GraphRAG modules.
7. Preserve Vulcan boundary: implement, test, validate, report; do not invent architecture.
