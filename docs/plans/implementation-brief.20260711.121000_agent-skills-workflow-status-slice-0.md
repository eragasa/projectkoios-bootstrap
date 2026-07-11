```json
{
  "title": "Workflow-project agent skill workflow status slice 0 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "superseded-by-petrinet-workflow-affordance-brief",
  "datetime": "20260711.121000Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_intake": "docs/plans/spec-intake.20260711.115957_agent-skills-for-workflow-inspectability.md",
  "source_slicing": "docs/plans/slicing.20260711.120900_agent-skills-workflow-project.md",
  "supersedes": "docs/plans/implementation-brief.20260711.120300_agent-skills-workflow-status-slice-0.md",
  "slice_name": "agent-skills-workflow-status-slice-0",
  "next_owner": "VULCAN"
}
```

# Implementation brief 20260711.121000: Workflow-project agent skill workflow status slice 0

## Supersession note

This brief is superseded by `docs/plans/implementation-brief.20260711.121600_petrinet-workflow-agent-status-skill-slice-1.md` after USER clarified this work is part of the existing Petri-net workflow harness / workflow inspectability effort, not a separate workflow-project skill surface.

## Purpose

Add the first workflow-project-local agent skill surface that makes agents use the live Petri-net inspectability command:

```bash
uv run projectkoios workflow status
```

This revised brief supersedes the earlier harness-global-first brief. The skill belongs to the existing workflow project/control surface first, not primarily to Pi/Hermes global skill registration.

## Scope

In scope:

- Add workflow-project-local skill surface:

  ```text
  src/python/projectkoios/workflow/agent_skills/README.md
  src/python/projectkoios/workflow/agent_skills/manifest.json
  src/python/projectkoios/workflow/agent_skills/koios-workflow-status/SKILL.md
  ```

- Add focused validation, likely under:

  ```text
  tests/projectkoios/workflow/test__WorkflowAgentSkills__status_skill.py
  ```

- Write an implementation report under `docs/implementation/`.
- Update VULCAN workspace state if VULCAN performs implementation.

Out of scope:

- Updating `agents/global/pi/skills/` or `docs/skills/skill-register.md` in Slice 0.
- Implementing `koios-interactive-control`; that is Slice 1.
- Mirroring skills into opencode/goose/archon/pi harness-global directories.
- Creating a new cross-harness install/distribution mechanism.
- Changing `uv run projectkoios workflow status` behavior.
- Changing Petri-net runtime, transition firing, persistence, Operator Console, workflow-object runtime coupling, schema authority, live adapters, role/permission semantics, or product authority.

## Required files

### `src/python/projectkoios/workflow/agent_skills/README.md`

Must explain:

- these are workflow-project-local agent skills;
- they are attached to the Project Koios workflow/Petri-net inspectability surface;
- they are not runtime code, not product authority, and not harness-global installation by themselves;
- harness propagation is deferred;
- Slice 0 includes `koios-workflow-status` only.

### `src/python/projectkoios/workflow/agent_skills/manifest.json`

Minimum fields:

```json
{
  "surface": "projectkoios.workflow.agent_skills",
  "status": "candidate-workflow-project-surface",
  "skills": [
    {
      "name": "koios-workflow-status",
      "path": "src/python/projectkoios/workflow/agent_skills/koios-workflow-status/SKILL.md",
      "purpose": "Inspect live Project Koios workflow status before advancing workflow work",
      "command": "uv run projectkoios workflow status",
      "runtime_mutation_allowed": false,
      "harness_global_propagation": "deferred"
    }
  ]
}
```

VULCAN may add small provenance fields if useful, but must not turn this into a broad schema authority.

### `src/python/projectkoios/workflow/agent_skills/koios-workflow-status/SKILL.md`

The skill should use the repository's skill markdown/frontmatter style where practical, but it is workflow-project-local and does not need to bind through `docs/skills/skill-register.md` in Slice 0.

Minimum frontmatter:

```yaml
---
name: koios-workflow-status
description: |
  Inspect live Project Koios workflow status and report active workflow state before advancing workflow work.
metadata:
  surface: projectkoios.workflow.agent_skills
  command: uv run projectkoios workflow status
  runtime_mutation_allowed: false
  harness_global_propagation: deferred
---
```

## Required skill behavior

The skill must instruct agents to:

1. Use the skill when starting or resuming Project Koios workflow work, before advancing workflow state, during handoffs, or when the user asks what is active/blocked/next.
2. Run from repository root when possible:

   ```bash
   uv run projectkoios workflow status
   ```

3. Summarize command output into:
   - active workflow/net;
   - current token and place;
   - enabled transitions;
   - whether user decision is required;
   - one clear recommendation.
4. If `user decision required: yes`, stop and ask/await approval unless the user explicitly delegated the next action.
5. If the command fails or is unavailable, report the failure as an inspectability gap and do not fabricate workflow state.
6. Preserve boundaries:
   - do not fire transitions;
   - do not mutate workflow state;
   - do not treat the static fixture as canonical workflow authority;
   - do not launch subagents merely because a transition is enabled;
   - do not expand scope beyond the user's current request.

## Suggested skill structure

Recommended headings:

- `When to use this skill`
- `Workflow-project responsibility`
- `Procedure`
- `Output format`
- `Stop conditions`
- `Failure modes`
- `Escalation rule`

Recommended output format:

```text
Workflow status:
- workflow: <workflow id>
- current token/place: <token> at <place>
- enabled transitions: <transition list>
- user decision required: yes/no
- recommendation: <one sentence>
```

## Acceptance criteria

1. `src/python/projectkoios/workflow/agent_skills/README.md` exists and describes the workflow-project-local skill surface.
2. `src/python/projectkoios/workflow/agent_skills/manifest.json` exists and lists `koios-workflow-status` with path, purpose, command, mutation disallowance, and deferred harness propagation.
3. `src/python/projectkoios/workflow/agent_skills/koios-workflow-status/SKILL.md` exists.
4. The skill frontmatter includes `name: koios-workflow-status`.
5. The skill instructs agents to run/consult `uv run projectkoios workflow status`.
6. The skill requires reporting workflow id, current token/place, enabled transitions, user-decision requirement, and one recommendation.
7. The skill requires stopping/asking when user decision is required unless the user explicitly delegated action.
8. The skill explicitly forbids firing transitions, mutating workflow state, treating the fixture as canonical authority, launching subagents just because a transition is enabled, or expanding scope beyond the request.
9. Tests or validation confirm the manifest path points at the skill file and required text/metadata is present.
10. No Petri-net runtime, workflow status command, Operator Console, workflow-object, schema, live adapter, role/permission, product authority, harness-global skill directory, or `docs/skills/skill-register.md` behavior is changed.

## Suggested validation

From repository root:

```bash
test -f src/python/projectkoios/workflow/agent_skills/README.md
test -f src/python/projectkoios/workflow/agent_skills/manifest.json
test -f src/python/projectkoios/workflow/agent_skills/koios-workflow-status/SKILL.md
uv run pytest tests/projectkoios/workflow/test__WorkflowAgentSkills__status_skill.py -q
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow
git diff --check
```

Suggested test assertions:

- manifest JSON parses;
- manifest `surface` is `projectkoios.workflow.agent_skills`;
- manifest has exactly one skill for Slice 0 unless explicitly approved otherwise;
- manifest skill path exists;
- skill contains `uv run projectkoios workflow status`;
- skill contains required output concepts: workflow, token/place, enabled transitions, user decision required, recommendation;
- skill contains stop/mutation boundaries.

## Pause triggers

Pause and ask USER/HERMES if implementation would require:

- defining a cross-harness installation/distribution mechanism;
- modifying `agents/global/*/skills/` or `docs/skills/skill-register.md`;
- adding skills to multiple harnesses in this slice;
- changing Petri-net runtime or workflow CLI behavior;
- adding interactive-control behavior into Slice 0;
- creating new ADR or schema authority.

## Handoff

VULCAN should produce a concise implementation plan and pause for USER/HERMES approval before coding unless USER/HERMES explicitly approves direct implementation from this revised brief.
