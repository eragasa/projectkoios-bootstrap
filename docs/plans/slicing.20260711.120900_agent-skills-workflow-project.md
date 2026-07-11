```json
{
  "title": "Workflow-project agent skills slicing package",
  "artifact_type": "slicing-package",
  "status": "superseded-by-petrinet-workflow-affordance-slicing",
  "datetime": "20260711.120900Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_intake": "docs/plans/spec-intake.20260711.115957_agent-skills-for-workflow-inspectability.md",
  "supersedes": "docs/plans/slicing.20260711.120200_agent-skills-workflow-inspectability.md",
  "scope": "agent-facing skill surfaces attached to the existing workflow project/control surface",
  "next_owner": "USER_HERMES_APPROVAL"
}
```

# Slicing package 20260711.120900: Workflow-project agent skills

## Supersession note

This package is superseded by `docs/plans/slicing.20260711.121500_petrinet-workflow-agent-affordances.md` after USER clarified this work is part of the existing Petri-net workflow harness / workflow inspectability effort, not a new workflow-project or agent-skills project.

## Correction being applied

This package supersedes the earlier harness-global-first slicing in `docs/plans/slicing.20260711.120200_agent-skills-workflow-inspectability.md`.

USER clarified that the skills should be added into the existing workflow project and sliced into that workflow surface, not treated primarily as `agents/global/pi/skills/...` plus skill-register work.

## Revised purpose

Make workflow inspectability and interactive-control practices agent-facing capabilities of the existing workflow project/control surface that now exposes:

```bash
uv run projectkoios workflow status
```

The skill instructions should live with the workflow project so agents can consume workflow-specific operating behavior from the same surface that owns Petri-net inspectability.

## Authority stance

No new ADR is needed for the revised Slice 0.

Reasoning:

- Existing Petri-net/workflow architecture authorizes the workflow project/control surface and read-only inspectability command.
- This slice adds project-local agent-facing instructions and metadata; it does not change runtime semantics or product authority.
- Harness-global propagation is deferred until the workflow-project skill surface exists and proves useful.

If implementation discovers that putting agent-facing skill files under the workflow project source tree creates packaging/discovery ambiguity, VULCAN should pause and report the exact placement gap.

## Revised placement for Slice 0

Use a workflow-project-local skill surface:

```text
src/python/projectkoios/workflow/agent_skills/
  README.md
  manifest.json
  koios-workflow-status/SKILL.md
```

Rationale:

- This location attaches the skill to the existing workflow project/control surface.
- It keeps workflow-specific behavior near `src/python/projectkoios/workflow/` and the `projectkoios workflow status` command.
- It avoids prematurely turning the request into Pi/Hermes global harness configuration.
- It can later be copied, symlinked, installed, or mirrored into harness-global skill directories by a separate propagation slice if needed.

The `manifest.json` is a small project-local index, not a new runtime loader or schema authority. Its purpose is to make the workflow-project skill surface inspectable and testable.

## Slice 0: `agent-skills-workflow-status-slice-0`

Goal: add a workflow-project-local agent skill for status inspectability.

Primary artifacts:

- `src/python/projectkoios/workflow/agent_skills/README.md`
- `src/python/projectkoios/workflow/agent_skills/manifest.json`
- `src/python/projectkoios/workflow/agent_skills/koios-workflow-status/SKILL.md`
- focused tests or validation for presence/consistency
- implementation report under `docs/implementation/`

Expected skill behavior:

1. Run or consult `uv run projectkoios workflow status` at relevant Project Koios workflow starts, handoffs, and before advancing workflow state.
2. Report:
   - active workflow/net;
   - current token/place;
   - enabled transitions;
   - whether user decision is required;
   - one recommendation.
3. If user decision is required, stop and ask/await approval unless the user explicitly delegated the next action.
4. Do not fire transitions, mutate workflow state, or treat the static fixture as canonical workflow authority.
5. If the command is unavailable or fails, report that failure as an inspectability gap and do not fabricate workflow state.

## Slice 1: `agent-skills-interactive-control-slice-1`

Goal: add workflow-project-local interactive-control guidance after Slice 0 is accepted.

Likely artifacts:

- `src/python/projectkoios/workflow/agent_skills/koios-interactive-control/SKILL.md`
- update `src/python/projectkoios/workflow/agent_skills/manifest.json`
- focused tests/validation
- implementation report

Expected behavior:

1. Trigger when the user asks what is happening, expresses confusion/frustration, requests interactive operation, or indicates the agent is expanding too far.
2. Use inspect → summarize → recommend → ask/act.
3. Do not launch subagents unless explicitly approved in that moment.
4. Do not edit files without explicit approval or a narrow delegated instruction.
5. Always provide one clear recommendation.
6. Prefer the smallest visible state change that restores operator control.
7. Treat tests as validation evidence, not the main explanation of progress.

## Slice 2: harness propagation, if needed

After workflow-project-local skills exist, decide whether and how to expose them to harness skill directories:

- `agents/global/pi/skills/`
- `agents/global/opencode/skills/`
- `agents/global/goose/skills/`
- `agents/global/archon/skills/`

This is deferred because propagation is a distribution/install concern, not the first workflow-project surface.

## Non-goals

These slices do not authorize:

- changing Petri-net runtime behavior;
- transition firing;
- persistence;
- Operator Console integration;
- workflow-object runtime coupling;
- schema authority under `docs/schemas/`;
- live adapter/session reads;
- role/permission expansion;
- product/mothership workflow authority;
- broad ADR expansion;
- harness-global propagation in Slice 0.

## Recommended next action

Route revised Slice 0 to VULCAN implementation planning/approval:

```text
agent-skills-workflow-status-slice-0
```

Implement only the workflow-project-local status skill surface first. Pause before coding unless USER/HERMES explicitly approves direct implementation from the revised brief.
