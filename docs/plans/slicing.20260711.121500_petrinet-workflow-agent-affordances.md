```json
{
  "title": "Petri-net workflow agent affordances slicing note",
  "artifact_type": "slicing-package",
  "status": "revised-proposed-for-user-hermes-approval",
  "datetime": "20260711.121500Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_intake": "docs/plans/spec-intake.20260711.115957_agent-skills-for-workflow-inspectability.md",
  "supersedes": [
    "docs/plans/slicing.20260711.120200_agent-skills-workflow-inspectability.md",
    "docs/plans/slicing.20260711.120900_agent-skills-workflow-project.md"
  ],
  "parent_effort": "Petri-net workflow harness / workflow inspectability",
  "previous_slice": "live-petri-net-skeleton-slice-0",
  "next_slice": "petrinet-workflow-agent-status-skill-slice-1"
}
```

# Slicing note 20260711.121500: Petri-net workflow agent affordances

## Correction being applied

This note supersedes the earlier framing that treated the work as either a harness-global skill registration task or a separate workflow-project skill surface.

USER clarified that this is not a new project. It is part of the same Petri-net workflow harness / workflow inspectability effort.

## Parent effort

Parent effort: Petri-net workflow harness / workflow inspectability.

Already accepted live slice:

- `live-petri-net-skeleton-slice-0`
- command: `uv run projectkoios workflow status`
- purpose: expose Petri-net state visibly: active workflow net, token/place, enabled transitions, and user-decision requirement.

New request:

- add agent-facing skill/control affordances so agents know how to consume, report, and act on the Petri-net status surface.

## Revised slice sequence

### Slice 1: `petrinet-workflow-agent-status-skill-slice-1`

Purpose: add the first agent-facing Petri-net workflow affordance for status inspection.

This slice teaches agents how to use the existing live status command. It does not create a new project identity.

Candidate implementation placement:

```text
src/python/projectkoios/workflow/skills/
  README.md
  manifest.json
  petrinet-workflow-status/SKILL.md
```

Placement is implementation detail: these files are part of the Petri-net workflow harness/control surface, not a standalone skills project and not harness-global propagation.

Required behavior:

1. Run/consult `uv run projectkoios workflow status` before advancing workflow work.
2. Report active workflow/net, current token/place, enabled transitions, user-decision requirement, and one recommendation.
3. If user decision is required, stop and ask/await approval unless explicitly delegated.
4. Do not fire transitions or mutate workflow state.
5. Do not treat the static bootstrap fixture as canonical workflow authority.
6. Do not spawn subagents or expand scope just because a transition is enabled.

### Slice 2: `petrinet-workflow-interactive-control-skill-slice-2`

Purpose: add the interactive-control affordance for moments when the user asks what is happening, expresses confusion/frustration, or requests interactive operation.

Expected behavior:

- inspect → summarize → recommend → ask/act;
- no subagents without explicit approval;
- no edits without explicit approval or narrow delegated instruction;
- always provide one recommendation;
- prefer smallest visible state change that restores operator control;
- treat tests as validation evidence, not the main explanation of progress.

### Later: harness propagation, if needed

Only after the Petri-net workflow affordance exists should a later slice decide whether and how to expose the skill to harness-specific directories such as `agents/global/pi/skills/`.

Harness-global placement is distribution, not the parent effort.

## Non-goals

This slicing does not authorize:

- transition firing;
- persistence;
- Petri-net runtime changes;
- Operator Console integration;
- workflow-object runtime coupling;
- schema authority under `docs/schemas/`;
- live adapter/session reads;
- role/permission expansion;
- product/mothership workflow authority;
- creating a new standalone agent-skills project;
- harness-global propagation in Slice 1.

## Recommended next action

Route `petrinet-workflow-agent-status-skill-slice-1` to VULCAN planning/implementation after USER/HERMES approval.
