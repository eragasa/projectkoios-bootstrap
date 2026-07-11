```json
{
  "title": "Agent skills for workflow inspectability slicing package",
  "artifact_type": "slicing-package",
  "status": "superseded-by-workflow-project-slicing",
  "datetime": "20260711.120200Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_intake": "docs/plans/spec-intake.20260711.115957_agent-skills-for-workflow-inspectability.md",
  "scope": "agent skills for workflow status inspectability and interactive control",
  "next_owner": "USER_HERMES_APPROVAL"
}
```

# Slicing package 20260711.120200: Agent skills for workflow inspectability

## Supersession note

This package is superseded by `docs/plans/slicing.20260711.120900_agent-skills-workflow-project.md` after USER clarified that the skills should be added into the existing workflow project/control surface, not treated primarily as Pi/Hermes global skill registration.

## Purpose

Turn the new live Petri-net inspectability command into reusable agent behavior without adding more ADR/process sprawl.

The first implementation should add a skill that makes agents run or consult:

```bash
uv run projectkoios workflow status
```

and report the active workflow state before advancing work.

## Architecture/authority stance

No new ADR is needed for the first skill slice.

Reasoning:

- The live command already exists as accepted Slice 0 behavior.
- Existing skill placement and registration practice is already documented by `docs/skills/skill-register.md`.
- Existing skill frontmatter conventions are visible under `agents/global/*/skills/*/SKILL.md`.
- The first slice adds operating instructions only; it does not change Petri-net runtime behavior, workflow authority, or product semantics.

If implementation discovers that a single project-level skill cannot be shared across the relevant harnesses without duplication or install changes, VULCAN should pause and report the placement gap rather than inventing a new skill distribution mechanism.

## Placement decision for Slice 0

Use the existing committed shared harness skill pattern, not a new `.agents/skills/` mechanism.

First placement:

```text
agents/global/pi/skills/koios-workflow-status/SKILL.md
```

Rationale:

- Pi/Hermes is the active orchestration layer for workflow status decisions.
- `docs/skills/skill-register.md` already indexes canonical skills under `agents/global/<harness>/skills/`.
- This avoids introducing a new project-level skill loader convention before proving the behavior.

Later slices may mirror or adapt the skill for other harnesses:

- `agents/global/opencode/skills/koios-workflow-status/SKILL.md` for VULCAN/code-agent use;
- `agents/global/goose/skills/koios-workflow-status/SKILL.md` for KOIOS/provenance use;
- `agents/global/archon/skills/koios-workflow-status/SKILL.md` for ATHENA/architecture use;
- or a separately approved shared project-skill distribution mechanism.

## Slice 0: `agent-skills-workflow-status-slice-0`

Goal: add one workflow-status skill for the orchestration/meta-harness path.

Primary artifacts:

- `agents/global/pi/skills/koios-workflow-status/SKILL.md`
- `docs/skills/skill-register.md`
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
5. If the command is unavailable or fails, report that failure as inspectability gap and avoid fabricating workflow state.

## Slice 1: `agent-skills-interactive-control-slice-1`

Goal: add an interactive-control skill after Slice 0 is accepted.

Likely primary artifacts:

- `agents/global/pi/skills/koios-interactive-control/SKILL.md`
- `docs/skills/skill-register.md`
- implementation report under `docs/implementation/`

Expected behavior:

1. Trigger when the user asks what is happening, expresses confusion/frustration, requests interactive operation, or indicates the agent is expanding too far.
2. Use inspect → summarize → recommend → ask/act.
3. Do not launch subagents unless explicitly approved in that moment.
4. Do not edit files without explicit approval or a narrow delegated instruction.
5. Always provide one clear recommendation.
6. Prefer the smallest visible state change that restores operator control.
7. Treat tests as validation evidence, not the main explanation of progress.

## Deferred slices

### Multi-harness propagation

After Slice 0 and Slice 1 prove useful for Pi/Hermes, decide whether to mirror/adapt skills into opencode, goose, and archon global skill directories.

This should be separate because each harness has different skill-discovery and role expectations.

### Shared project-level skill mechanism

If repeated mirroring creates maintenance friction, a later slice may define a shared project skill distribution convention. That is not needed for Slice 0.

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
- broad ADR expansion.

## Recommended next action

Route Slice 0 to VULCAN implementation planning/approval:

```text
agent-skills-workflow-status-slice-0
```

Implement only the Pi/Hermes skill and skill-register update first. Pause before coding unless USER/HERMES explicitly approves direct implementation from the brief.
