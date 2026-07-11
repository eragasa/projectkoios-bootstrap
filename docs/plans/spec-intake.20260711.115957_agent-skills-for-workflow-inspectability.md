```json
{
  "title": "Agent skills for workflow inspectability and interactive control",
  "artifact_type": "spec-intake",
  "status": "athena-slicing-requested",
  "datetime": "20260711.115957Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "source": "USER instruction in Hermes session",
  "scope": "project skills that make agents use live workflow status and interactive control practices",
  "next_owner": "ATHENA"
}
```

# Spec intake 20260711.115957: Agent skills for workflow inspectability and interactive control

## User request

The workflow inspectability and interactive-control behaviors should be implemented as skills for agents to use.

Immediate user direction:

> add this to the project and tell athena to slice it up

## Problem

Project Koios agents can produce docs, plans, tests, and implementation artifacts without consistently exposing:

- what workflow state is active;
- where the current token/work item sits;
- which transitions are enabled;
- whether the user must decide;
- what the agent recommends next;
- when agents must stop instead of expanding scope.

The new `uv run projectkoios workflow status` command is the first live inspectability surface, but agents need skill-level operating instructions to use it consistently.

## Candidate skill surfaces

### `koios-workflow-status`

Purpose: make agents inspect and report the live workflow status before starting or advancing Project Koios bootstrap work.

Expected behavior:

1. Run or consult:

   ```bash
   uv run projectkoios workflow status
   ```

2. Report:
   - active workflow/net;
   - current token and place;
   - enabled transitions;
   - whether user decision is required;
   - one clear recommendation.

3. Stop and ask/await approval if status indicates user decision is required, unless the user explicitly delegates action.

### `koios-interactive-control`

Purpose: prevent runaway agent behavior when the user asks what is happening, expresses uncertainty/frustration, or requests interactive operation.

Expected behavior:

1. Do not launch subagents unless explicitly approved.
2. Do not edit files without either explicit approval or a narrow delegated instruction.
3. Use an inspect → summarize → recommend → ask/act loop.
4. Always provide one recommendation.
5. Prefer the smallest visible state change that restores operator control.
6. Treat tests as validation only, not as the main explanation of progress.

## Placement candidates

ATHENA should decide slice/placement, but HERMES recommends project-versioned shared skills first, then promotion if successful.

Possible locations:

- Project-level skills, if supported by all relevant harnesses:
  - `.agents/skills/koios-workflow-status/SKILL.md`
  - `.agents/skills/koios-interactive-control/SKILL.md`

- Existing shared harness skill examples:
  - `agents/global/pi/skills/`
  - `agents/global/opencode/skills/`
  - `agents/global/goose/skills/`
  - `agents/global/archon/skills/`

## User correction after initial slicing

USER clarified that these skills should be added into the existing Petri-net/workflow effort and sliced into that surface, not treated as a new project and not primarily as a Pi/Hermes global skill-registration task.

Implication for ATHENA:

- Re-slice as part of the existing Petri-net workflow runtime / workflow inspectability effort.
- Treat skills as agent-facing Petri-net/workflow control affordances that teach agents how to consume the existing `projectkoios workflow status` surface.
- Do not spawn a separate "agent skills project".
- Do not make Slice 0 merely `agents/global/pi/skills/...` plus a register entry unless that placement is explicitly subordinate to the Petri-net workflow slice.
- Defer harness-global propagation until the Petri-net workflow skill surface is clear.

## Slicing request for ATHENA

Please slice this into bounded implementation work for the existing workflow project.

Recommended first slice:

```text
agent-skills-workflow-status-slice-0
```

Potential acceptance:

- Adds a skill usable by pi/Hermes that instructs agents to run `uv run projectkoios workflow status` at relevant workflow starts and report status plus recommendation.
- Does not change workflow runtime behavior.
- Does not add more ADR/process ceremony.
- Includes minimal validation that skill files are discoverable/structured according to the skill format used by the repository.

Recommended second slice:

```text
agent-skills-interactive-control-slice-1
```

Potential acceptance:

- Adds skill instructions for interactive-control/recovery mode.
- Encodes stop conditions and subagent-approval rules.
- Requires agents to provide recommendations and avoid autonomous expansion when user uncertainty/frustration is detected.

## Boundary conditions

This request does not authorize:

- changing the Petri-net runtime;
- adding transition firing;
- adding persistence;
- changing product/mothership workflow authority;
- using skills as a substitute for the live workflow state command;
- creating broad new ADRs unless ATHENA finds a specific decision gap.

## HERMES recommendation

Slice and implement the workflow-status skill first. It directly connects the new live Petri-net status command to day-to-day agent behavior and makes the harness inspectability improvement reusable.
