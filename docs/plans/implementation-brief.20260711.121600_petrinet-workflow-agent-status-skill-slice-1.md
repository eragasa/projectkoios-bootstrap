```json
{
  "title": "Petri-net workflow agent status skill slice 1 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "vulcan-planning-ready-pending-user-hermes-approval",
  "datetime": "20260711.121600Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_intake": "docs/plans/spec-intake.20260711.115957_agent-skills-for-workflow-inspectability.md",
  "source_slicing": "docs/plans/slicing.20260711.121500_petrinet-workflow-agent-affordances.md",
  "supersedes": [
    "docs/plans/implementation-brief.20260711.120300_agent-skills-workflow-status-slice-0.md",
    "docs/plans/implementation-brief.20260711.121000_agent-skills-workflow-status-slice-0.md"
  ],
  "parent_effort": "Petri-net workflow harness / workflow inspectability",
  "previous_slice": "live-petri-net-skeleton-slice-0",
  "slice_name": "petrinet-workflow-agent-status-skill-slice-1",
  "next_owner": "VULCAN"
}
```

# Implementation brief 20260711.121600: Petri-net workflow agent status skill slice 1

## Purpose

Continue the Petri-net workflow inspectability effort by adding an agent-facing skill/control affordance for the existing live status command:

```bash
uv run projectkoios workflow status
```

This is Slice 1 after `live-petri-net-skeleton-slice-0`. It is not a new project and not primarily a harness-global skill registration task.

## Scope

In scope:

```text
src/python/projectkoios/workflow/skills/README.md
src/python/projectkoios/workflow/skills/manifest.json
src/python/projectkoios/workflow/skills/petrinet-workflow-status/SKILL.md
tests/projectkoios/workflow/test__PetriNetWorkflowSkills__status_skill.py
```

Out of scope:

- `agents/global/*/skills/` changes;
- `docs/skills/skill-register.md` changes;
- cross-harness propagation;
- a standalone agent-skills project;
- interactive-control skill behavior;
- changes to `uv run projectkoios workflow status`;
- Petri-net runtime changes;
- transition firing;
- persistence;
- Operator Console integration;
- workflow-object runtime coupling;
- schema authority;
- live adapters;
- role/permission expansion;
- product/mothership workflow authority.

## Placement meaning

The files under `src/python/projectkoios/workflow/skills/` are part of the existing Petri-net workflow harness/control surface.

They are agent-facing operating affordances for the workflow runtime. They are not a separate project namespace. If a future slice copies or exposes them through harness-global skill directories, that will be distribution/propagation only.

## Required files

### `README.md`

Must explain:

- this directory contains agent-facing affordances for the Petri-net workflow harness;
- the first affordance teaches agents how to consume `projectkoios workflow status`;
- files here are not runtime mutation authority, not product authority, and not harness-global propagation by themselves;
- transition firing and persistence remain out of scope.

### `manifest.json`

Small inspectable index, not schema authority. Minimum shape:

```json
{
  "surface": "projectkoios.workflow.petrinet.agent_affordances",
  "parent_effort": "petri-net-workflow-inspectability",
  "previous_slice": "live-petri-net-skeleton-slice-0",
  "status": "candidate-slice-1",
  "skills": [
    {
      "name": "petrinet-workflow-status",
      "path": "src/python/projectkoios/workflow/skills/petrinet-workflow-status/SKILL.md",
      "purpose": "Teach agents to inspect and report Petri-net workflow status before advancing work",
      "command": "uv run projectkoios workflow status",
      "runtime_mutation_allowed": false,
      "harness_global_propagation": "deferred"
    }
  ]
}
```

### `petrinet-workflow-status/SKILL.md`

Use skill-style Markdown/frontmatter, but identify it as a Petri-net workflow affordance.

Minimum frontmatter:

```yaml
---
name: petrinet-workflow-status
description: |
  Use the live Petri-net workflow status command to inspect and report active workflow state before advancing work.
metadata:
  surface: projectkoios.workflow.petrinet.agent_affordances
  parent_effort: petri-net-workflow-inspectability
  previous_slice: live-petri-net-skeleton-slice-0
  command: uv run projectkoios workflow status
  runtime_mutation_allowed: false
  harness_global_propagation: deferred
---
```

## Required skill behavior

The skill must instruct agents to:

1. Use it when starting/resuming Petri-net workflow work, before advancing workflow state, during handoffs, or when the user asks what is active/blocked/next.
2. Run from repository root when possible:

   ```bash
   uv run projectkoios workflow status
   ```

3. Summarize the command output into:
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
   - do not treat the static bootstrap fixture as canonical workflow authority;
   - do not launch subagents merely because a transition is enabled;
   - do not expand scope beyond the user's current request.

Recommended output format:

```text
Petri-net workflow status:
- workflow: <workflow id>
- current token/place: <token> at <place>
- enabled transitions: <transition list>
- user decision required: yes/no
- recommendation: <one sentence>
```

## Acceptance criteria

1. Workflow skill files are added under `src/python/projectkoios/workflow/skills/`.
2. README frames them as part of the Petri-net workflow harness / workflow inspectability effort.
3. Manifest lists exactly one Slice 1 skill unless USER/HERMES explicitly approves more.
4. Manifest path points to the skill file.
5. Skill frontmatter has `name: petrinet-workflow-status` and Petri-net workflow metadata.
6. Skill instructs agents to run/consult `uv run projectkoios workflow status`.
7. Skill requires reporting workflow id, current token/place, enabled transitions, user-decision requirement, and one recommendation.
8. Skill requires stopping/asking when user decision is required unless explicitly delegated.
9. Skill forbids firing transitions, mutating workflow state, treating the static fixture as canonical authority, launching subagents just because a transition is enabled, or expanding scope beyond the request.
10. Tests validate manifest/skill presence and required contents.
11. No harness-global skill directory, `docs/skills/skill-register.md`, Petri-net runtime, workflow CLI behavior, Operator Console, workflow-object, schema, live adapter, role/permission, or product authority behavior is changed.

## Suggested validation

From repository root:

```bash
uv run pytest tests/projectkoios/workflow/test__PetriNetWorkflowSkills__status_skill.py -q
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow
git diff --check
```

Suggested test assertions:

- manifest JSON parses;
- manifest `surface` is `projectkoios.workflow.petrinet.agent_affordances`;
- manifest `parent_effort` is `petri-net-workflow-inspectability`;
- manifest has one skill named `petrinet-workflow-status`;
- manifest skill path exists;
- skill contains `uv run projectkoios workflow status`;
- skill contains required output concepts: workflow, token/place, enabled transitions, user decision required, recommendation;
- skill contains stop/mutation boundaries.

## Pause triggers

Pause and ask USER/HERMES if implementation would require:

- harness-global skill registration or propagation;
- changing Petri-net runtime or workflow CLI behavior;
- adding transition firing/dry-run behavior;
- adding interactive-control behavior in this slice;
- creating a new project namespace;
- creating new ADR or schema authority.

## Handoff

VULCAN should produce a concise implementation plan and pause for USER/HERMES approval before coding unless USER/HERMES explicitly approves direct implementation from this revised brief.
