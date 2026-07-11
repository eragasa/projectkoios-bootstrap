```json
{
  "title": "Queued slice: Pi skill determinism slice 0",
  "artifact_type": "queued-slice",
  "status": "queued-not-active",
  "datetime": "20260711.122000Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source": "KOIOS proposal relayed by HERMES",
  "queue_position": "after petrinet-workflow-agent-status-skill-slice-1",
  "must_not_supersede": "docs/plans/implementation-brief.20260711.121600_petrinet-workflow-agent-status-skill-slice-1.md"
}
```

# Queued slice 20260711.122000: Pi skill determinism slice 0

## Queue status

Queued, not active.

This topic must not replace or reframe the active Petri-net workflow inspectability slice:

- Active slice: `petrinet-workflow-agent-status-skill-slice-1`
- Brief: `docs/plans/implementation-brief.20260711.121600_petrinet-workflow-agent-status-skill-slice-1.md`
- Parent effort: Petri-net workflow harness / workflow inspectability

`pi-skill-determinism-slice-0` should be considered only after the Petri-net workflow status skill exists or USER/HERMES explicitly reprioritizes.

## Purpose

Make Pi skill behavior deterministic now that current orchestration is happening through Pi.

This is a Pi routing/distribution/determinism slice, not a cross-harness propagation project.

## KOIOS proposal summary

- Simplify skill rationalization to Pi first.
- Inventory `agents/global/pi/skills/*/SKILL.md`.
- Include project-local workflow skill candidates only if they affect Pi behavior, such as `src/python/projectkoios/workflow/skills/` after `petrinet-workflow-agent-status-skill-slice-1` lands.
- Classify each skill by:
  - status: stable / candidate / draft / deprecated;
  - trigger condition;
  - required command/tool;
  - stop condition;
  - output format;
  - authority boundary.
- Define a canonical Pi skill contract template.
- Add or normalize the Petri-net workflow status skill as the first mandatory workflow skill for Pi behavior.
- Define deterministic routing rule: if the user asks what is happening / what next, expresses confusion/frustration, or workflow work starts, inspect workflow status before more edits.
- Explicitly defer opencode/goose/archon/global cross-harness propagation.

## Candidate acceptance shape

- Pi agents know when to run:

  ```bash
  uv run projectkoios workflow status
  ```

- Pi agents summarize:
  - active workflow;
  - current token/place;
  - enabled transitions;
  - user-decision-required;
  - one recommendation.
- Pi agents stop when user decision is required unless delegated.
- Skill files have status/authority boundary and deterministic trigger/stop/output rules.
- No broad ADR/process sprawl.

## Non-goals

This queued topic does not authorize:

- replacing `petrinet-workflow-agent-status-skill-slice-1`;
- changing Petri-net runtime;
- changing `projectkoios workflow status`;
- transition firing or persistence;
- opencode/goose/archon propagation;
- broad ADR/process expansion.

## Recommended later slice name

`pi-skill-determinism-slice-0` is acceptable as a queued name. ATHENA may refine it when USER/HERMES activates the topic.
