```json
{
  "title": "Petri-net workflow queue state slice 4 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "draft-pending-user-hermes-review",
  "datetime": "20260711.124106Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "parent_effort": "Petri-net workflow harness / workflow inspectability",
  "previous_slices": [
    "live-petri-net-skeleton-slice-0",
    "petrinet-workflow-agent-status-skill-slice-1",
    "petrinet-workflow-current-slice-status-reconciliation-slice-2",
    "petrinet-workflow-interactive-control-skill-slice-3"
  ],
  "slice_name": "petrinet-workflow-queue-state-slice-4",
  "next_owner": "USER_HERMES"
}
```

# Implementation brief 20260711.124106: Petri-net workflow queue state slice 4

## Purpose

Move the Petri-net workflow harness from prose/skill-only queue discipline toward a mechanical, machine-visible workflow queue/status control surface.

The goal is to make active, queued/proposed, completed/accepted, superseded, and deferred workflow state inspectable by command, rather than inferred from chat history or workspace prose.

This slice stays inside the existing Petri-net workflow harness / workflow inspectability effort. It is not a new project, not product/mothership workflow authority, and not a global skill propagation slice.

## Prior context

Completed/packaged context from HERMES:

- `petrinet-workflow-interactive-control-skill-slice-3` accepted, committed, and pushed as `b4de9c64 Add Petri net interactive control skill`.
- Follow-up VULCAN state fix committed and pushed as `ed9110b9 Update Vulcan interactive control state`.

Current priority from HERMES/USER: prioritize workflow engine work so the project has a sensible workflow engine.

## Slice name

`petrinet-workflow-queue-state-slice-4`

## Goal

Add a read-only queue/status command surface that reports:

- active item, or explicitly none;
- queued/proposed items in order;
- completed/accepted recent slices;
- superseded/rejected/deferred items where known;
- exact next decision needed.

The first implementation should use a static/read-only project fixture or manifest. No transition firing or activation mutation is authorized in this slice.

## Candidate command surface

Preferred command:

```bash
uv run projectkoios workflow queue
```

Acceptable alternative if VULCAN finds it materially simpler and cleaner:

```bash
uv run projectkoios workflow status --queue
```

ATHENA preference is `workflow queue` because it separates queue/control-surface inspection from the existing Petri-net marking status output while remaining under the same `projectkoios workflow` command group.

## Scope

In scope:

```text
dev/workflow-nets/bootstrap-harness.queue-state.json
src/python/projectkoios/cli/workflow.py
tests/projectkoios/cli/test__workflow_queue.py
docs/implementation/<implementation-report>.md
docs/AAR/<aar-if-useful>.md
workspaces/vulcan/state.md and workspaces/vulcan/active.md if VULCAN implements
```

VULCAN may choose a different fixture filename if it keeps the same narrow meaning and records it in the implementation plan/report.

The fixture should be explicit static input, not inferred from git history, chat logs, intercom state, or mutable local harness state.

## Static fixture minimum shape

The queue-state fixture should be small, explicit, and read-only. It is not schema authority.

Minimum conceptual fields:

```json
{
  "surface": "projectkoios.workflow.queue_state",
  "parent_effort": "petri-net-workflow-inspectability",
  "status": "static-read-only-fixture",
  "active_item": null,
  "queued_items": [
    {
      "name": "pi-skill-determinism-slice-0",
      "state": "queued",
      "artifact_refs": ["docs/plans/queued-slice.20260711.122000_pi-skill-determinism-slice-0.md"],
      "why": "Future Pi skill determinism improvement topic.",
      "dependency_or_blocker": "Requires explicit USER/HERMES activation; must not replace workflow-engine work.",
      "recommendation": "Not next while workflow-engine controls are prioritized."
    }
  ],
  "completed_items": [
    {
      "name": "petrinet-workflow-interactive-control-skill-slice-3",
      "state": "accepted-committed-pushed",
      "commit": "b4de9c64",
      "artifact_refs": ["docs/implementation/petrinet-workflow-interactive-control-skill-slice-3.20260711.123801.md"]
    }
  ],
  "superseded_items": [],
  "deferred_items": [],
  "next_decision_needed": "Approve or revise petrinet-workflow-queue-state-slice-4 implementation plan."
}
```

VULCAN may refine field names for code clarity, but must preserve the semantics above.

## Required output behavior

The command must print an operator-readable summary including:

1. active item, or `none`;
2. queued/proposed items in order;
3. completed/accepted recent slices;
4. superseded/rejected/deferred items where present;
5. exact next decision needed;
6. fixture path or source reference;
7. a visible statement that the queue state is a static read-only fixture and not canonical product workflow authority.

Suggested output shape:

```text
workflow queue: bootstrap-harness.queue-state
fixture: dev/workflow-nets/bootstrap-harness.queue-state.json
mode: static read-only fixture; not canonical workflow authority

active:
  none

queued/proposed:
  1. pi-skill-determinism-slice-0
     why: ...
     blocker: ...
     recommendation: ...

completed/recent:
  - petrinet-workflow-interactive-control-skill-slice-3 commit=b4de9c64

superseded/deferred:
  - <none or items>

next decision needed:
  Approve or revise petrinet-workflow-queue-state-slice-4 implementation plan.
```

## Initial fixture content requirements

The initial fixture must preserve known current facts:

- Last completed/pushed:
  - `petrinet-workflow-interactive-control-skill-slice-3` — `b4de9c64 Add Petri net interactive control skill`.
  - `ed9110b9 Update Vulcan interactive control state` as follow-up state fix.
- `pi-skill-determinism-slice-0` remains queued, not superseded.
- `petrinet-workflow-queue-state-slice-4` is the current proposed/next planning topic until USER/HERMES accepts/revises it.
- Superseded/rejected skill-framing artifacts remain superseded, including:
  - `docs/plans/slicing.20260711.120200_agent-skills-workflow-inspectability.md`;
  - `docs/plans/implementation-brief.20260711.120300_agent-skills-workflow-status-slice-0.md`;
  - `docs/plans/slicing.20260711.120900_agent-skills-workflow-project.md`;
  - `docs/plans/implementation-brief.20260711.121000_agent-skills-workflow-status-slice-0.md`.

## Boundaries

This slice must not add:

- transition firing;
- activation mutation;
- queue mutation;
- persistence beyond a static read-only fixture committed to the repo;
- generalized workflow database/storage;
- live intercom/session reads;
- git-history-derived state reconstruction;
- Operator Console integration;
- workflow-object runtime coupling;
- schema authority under `docs/schemas/`;
- product/mothership workflow authority;
- global skill propagation;
- replacement or supersession of `pi-skill-determinism-slice-0`.

If VULCAN believes a smaller mechanical mutation is necessary, VULCAN must pause and justify it before coding. HERMES preference for this slice is read-only queue first.

## Acceptance criteria

1. A read-only workflow queue command is available, preferably:

   ```bash
   uv run projectkoios workflow queue
   ```

2. The command loads an explicit static project fixture/manifest.
3. The command prints active item or none.
4. The command prints queued/proposed items in deterministic order.
5. The command prints completed/accepted recent slices with commit references where known.
6. The command prints superseded/rejected/deferred items where known.
7. The command prints exact next decision needed.
8. The command labels the fixture as static/read-only and non-canonical workflow authority.
9. Tests validate the command output and fixture parsing narrowly.
10. `pi-skill-determinism-slice-0` remains queued and is not superseded.
11. No runtime transition firing, activation mutation, persistence, Operator Console, workflow-object coupling, schema/product authority, live adapter, git-history inference, or global skill propagation is introduced.

## Suggested validation

From repository root:

```bash
uv run projectkoios workflow queue
uv run pytest tests/projectkoios/cli/test__workflow_queue.py tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/workflow -q
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow src/python/projectkoios/cli tests/projectkoios/workflow tests/projectkoios/cli
uv run python -m json.tool dev/workflow-nets/bootstrap-harness.queue-state.json >/dev/null
git diff --check
```

If the command is implemented as `workflow status --queue`, VULCAN should substitute that command in validation and explain the choice in the implementation plan/report.

## Pause triggers

Pause and ask USER/HERMES if implementation would require:

- changing Petri-net executor/runtime semantics;
- firing, simulating, or mutating transitions;
- mutating queue state from the command;
- persistence/storage beyond the static fixture;
- deriving state from git history, chat logs, or intercom;
- adding Operator Console integration;
- coupling workflow-object runtime behavior;
- creating schema/product authority;
- changing global skill directories;
- superseding or implementing `pi-skill-determinism-slice-0`.

## Handoff

This is a brief only. Pause for USER/HERMES queue/control review before routing to VULCAN planning or implementation.
