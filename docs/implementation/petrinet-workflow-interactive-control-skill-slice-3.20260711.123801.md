```json
{
  "title": "Petri-net workflow interactive-control skill slice 3 implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated",
  "datetime": "20260711.123801Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_brief": "docs/plans/implementation-brief.20260711.123305_petrinet-workflow-interactive-control-skill-slice-3.md",
  "slice_name": "petrinet-workflow-interactive-control-skill-slice-3",
  "parent_effort": "Petri-net workflow harness / workflow inspectability"
}
```

# Implementation report 20260711.123801: Petri-net workflow interactive-control skill slice 3

## Summary

Implemented the approved workflow-local interactive-control skill affordance for the existing Petri-net workflow harness / workflow inspectability effort.

The new skill encodes the operating pattern:

```text
inspect → summarize → recommend → ask/act
```

It requires exactly one primary recommendation unless the user asks for options, and requires asking before file edits, routing, subagent launch, active/queued-state changes, or user-decision-gated actions.

## Changed files

- `src/python/projectkoios/workflow/skills/manifest.json` — now lists both workflow-local skills and marks Slice 3 status.
- `src/python/projectkoios/workflow/skills/README.md` — describes both status and interactive-control affordances while preserving workflow-local boundaries.
- `src/python/projectkoios/workflow/skills/petrinet-workflow-interactive-control/SKILL.md` — new interactive-control skill instructions.
- `tests/projectkoios/workflow/test__PetriNetWorkflowSkills__status_skill.py` — updated manifest expectations to preserve the Slice 1 status skill in the Slice 3 manifest.
- `tests/projectkoios/workflow/test__PetriNetWorkflowSkills__interactive_control_skill.py` — focused tests for manifest shape, required behavior, and boundary language.
- `docs/implementation/petrinet-workflow-interactive-control-skill-slice-3.20260711.123801.md` — this report.
- `docs/AAR/aar.20260711.123801_petrinet-workflow-interactive-control-skill-slice-3.md` — session/process note.
- `workspaces/vulcan/active.md` and `workspaces/vulcan/state.md` — VULCAN workspace state updated.

## Implemented behavior

The interactive-control skill instructs agents to:

- use the skill when the user asks what is happening, expresses confusion/frustration, asks for interactive operation, asks what is next, or asks to regain control;
- inspect first with `uv run projectkoios workflow status`;
- summarize workflow id, current token/place, active slice if visible, enabled transitions, user-decision requirement, and active/queued/superseded/deferred distinctions when known;
- provide exactly one primary recommendation unless the user asks for options;
- ask before acting when user decision is required or when action would edit files, route work, launch subagents, or change active/queued state;
- preserve queue discipline and report inspectability failures without inventing workflow state.

## Boundary confirmation

This slice did not change:

- Petri-net runtime behavior;
- `uv run projectkoios workflow status` behavior;
- workflow-net fixture content;
- transition firing or dry-run behavior;
- persistence;
- live adapter/session reads;
- Operator Console integration;
- workflow-object runtime coupling;
- schema/product authority;
- role/permission semantics;
- global skill directories;
- `pi-skill-determinism-slice-0` queued status.

## Validation results

From repository root:

```bash
uv run pytest tests/projectkoios/workflow/test__PetriNetWorkflowSkills__status_skill.py tests/projectkoios/workflow/test__PetriNetWorkflowSkills__interactive_control_skill.py -q
```

Result: passed, `6 passed in 0.01s`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow
```

Result: passed, `summary: 0 finding(s), 13 file(s)`.

```bash
git diff --check
```

Result: passed with no output.
