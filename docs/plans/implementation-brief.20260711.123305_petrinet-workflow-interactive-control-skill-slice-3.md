```json
{
  "title": "Petri-net workflow interactive-control skill slice 3 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "vulcan-planning-ready-pending-user-hermes-approval",
  "datetime": "20260711.123305Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_slicing": "docs/plans/slicing.20260711.121500_petrinet-workflow-agent-affordances.md",
  "parent_effort": "Petri-net workflow harness / workflow inspectability",
  "previous_slices": [
    "live-petri-net-skeleton-slice-0",
    "petrinet-workflow-agent-status-skill-slice-1",
    "petrinet-workflow-current-slice-status-reconciliation-slice-2"
  ],
  "slice_name": "petrinet-workflow-interactive-control-skill-slice-3",
  "next_owner": "VULCAN"
}
```

# Implementation brief 20260711.123305: Petri-net workflow interactive-control skill slice 3

## Purpose

Continue the existing Petri-net workflow harness / workflow inspectability effort by adding a workflow-local interactive-control agent affordance.

This slice teaches agents how to respond when the user asks what is happening, expresses confusion/frustration, asks for interactive operation, or needs the next Petri-net workflow action made explicit.

The required operating pattern is:

```text
inspect → summarize → recommend → ask/act
```

This is Slice 3 after:

- `live-petri-net-skeleton-slice-0` — read-only `uv run projectkoios workflow status` surface;
- `petrinet-workflow-agent-status-skill-slice-1` — status-consumption skill;
- `petrinet-workflow-current-slice-status-reconciliation-slice-2` — fixture/status-output reconciliation.

This is not a new project and not harness-global propagation.

## Current workflow status context

At activation time, HERMES observed:

```text
workflow: bootstrap-harness.slice-0
current token/place: current-slice at user_decision
active_slice: petrinet-workflow-current-slice-status-reconciliation-slice-2
enabled transition: approve_next_slice
user decision required: yes
```

The interactive-control affordance must respect this style of status surface and user-decision gate.

## Scope

In scope:

```text
src/python/projectkoios/workflow/skills/manifest.json
src/python/projectkoios/workflow/skills/README.md
src/python/projectkoios/workflow/skills/petrinet-workflow-interactive-control/SKILL.md
tests/projectkoios/workflow/test__PetriNetWorkflowSkills__interactive_control_skill.py
```

VULCAN may update the existing status-skill test if needed to keep manifest expectations coherent, but should prefer adding a focused test for the new skill.

Out of scope:

- Petri-net runtime changes;
- `uv run projectkoios workflow status` command behavior changes;
- transition firing or dry-run behavior;
- persistence or canonical workflow-state storage;
- live adapter/session reads;
- Operator Console integration;
- workflow-object runtime coupling;
- schema authority;
- role/permission expansion;
- product/mothership workflow authority;
- harness-global skill propagation;
- `agents/global/*/skills/` changes;
- replacing or superseding `pi-skill-determinism-slice-0`.

## Required behavior

The new interactive-control skill must instruct agents to:

1. Use the skill when the user asks what is happening, expresses confusion/frustration, asks to operate the workflow interactively, asks what is next, or asks to regain control of a Petri-net workflow session.
2. Inspect first by running or consulting:

   ```bash
   uv run projectkoios workflow status
   ```

3. Summarize observed state before recommending action. The summary must include:
   - workflow id;
   - current token/place;
   - active slice if visible;
   - enabled transitions;
   - whether user decision is required;
   - active vs queued vs superseded/deferred distinction when known from workspace state.
4. Provide exactly one primary recommendation unless the user asks for options.
5. Ask before acting when user decision is required, when the action would edit files, route work to another agent, launch subagents, or change active/queued state.
6. Act only when the user explicitly approves the action or has already delegated a narrow action in the current request.
7. Keep explanations user-readable: do not treat tests, commits, or internal artifact lists as the main explanation of progress unless the user asks for evidence.
8. Preserve queue discipline: do not replace current active work with new incoming topics unless USER/HERMES explicitly says to switch active work.
9. Report command failure as an inspectability gap; do not invent workflow state.

Recommended output shape:

```text
Petri-net interactive control:
- observed: <workflow/token/place/user-decision summary>
- active: <active item or none>
- queued/deferred: <short queue summary if relevant>
- recommendation: <one clear next action>
- approval needed: <yes/no and why>
```

## Required boundaries

The skill must explicitly say:

- Do not fire transitions.
- Do not mutate workflow state.
- Do not edit files unless the user explicitly approves or delegates a narrow edit.
- Do not launch subagents or route work merely because a transition is enabled.
- Do not activate queued work without explicit USER/HERMES direction.
- Do not treat the static bootstrap workflow-net fixture as canonical workflow authority.
- Do not treat tests as the main explanation of progress.
- Do not introduce persistence, schema authority, live adapter/session reads, role/permission semantics, Operator Console integration, workflow-object runtime coupling, or product/mothership authority.

## Manifest expectations

Update `src/python/projectkoios/workflow/skills/manifest.json` so it remains a small inspectable index, not schema authority.

Expected minimum after this slice:

```json
{
  "surface": "projectkoios.workflow.petrinet.agent_affordances",
  "parent_effort": "petri-net-workflow-inspectability",
  "previous_slice": "petrinet-workflow-current-slice-status-reconciliation-slice-2",
  "status": "candidate-slice-3",
  "skills": [
    {
      "name": "petrinet-workflow-status",
      "path": "src/python/projectkoios/workflow/skills/petrinet-workflow-status/SKILL.md",
      "purpose": "Teach agents to inspect and report Petri-net workflow status before advancing work",
      "command": "uv run projectkoios workflow status",
      "runtime_mutation_allowed": false,
      "harness_global_propagation": "deferred"
    },
    {
      "name": "petrinet-workflow-interactive-control",
      "path": "src/python/projectkoios/workflow/skills/petrinet-workflow-interactive-control/SKILL.md",
      "purpose": "Teach agents to operate Petri-net workflow sessions interactively by inspecting, summarizing, recommending, and asking before action",
      "command": "uv run projectkoios workflow status",
      "runtime_mutation_allowed": false,
      "harness_global_propagation": "deferred"
    }
  ]
}
```

VULCAN may preserve additional manifest fields if already present, but must not turn the manifest into schema authority or a harness-global registry.

## README expectations

Update `src/python/projectkoios/workflow/skills/README.md` to mention the second affordance:

- `petrinet-workflow-status` for status inspection/reporting;
- `petrinet-workflow-interactive-control` for operator-facing interactive control conversations.

The README must continue to state that these affordances are workflow-local, not a new project identity, not product authority, not runtime mutation authority, and not harness-global propagation by themselves.

## Acceptance criteria

1. New skill file exists at `src/python/projectkoios/workflow/skills/petrinet-workflow-interactive-control/SKILL.md` with valid skill frontmatter.
2. Manifest lists both workflow-local skills and does not remove the existing status skill.
3. Interactive-control skill instructs agents to inspect first via `uv run projectkoios workflow status`.
4. Skill requires summarize → recommend → ask/act behavior.
5. Skill requires exactly one primary recommendation unless the user asks for options.
6. Skill requires asking before file edits, routing, subagent launch, active/queued-state change, or any user-decision-gated action.
7. Skill preserves active/queued/superseded/deferred distinctions.
8. Skill forbids transition firing, workflow mutation, persistence, live adapters, Operator Console integration, workflow-object runtime coupling, schema/product authority, and harness-global propagation.
9. Tests validate manifest shape, skill presence, required instruction phrases, and boundary language.
10. No Petri-net runtime, CLI status behavior, fixture content, Operator Console, workflow-object, schema, product authority, or global skill directory changes occur in this slice.

## Suggested validation

From repository root:

```bash
uv run pytest tests/projectkoios/workflow/test__PetriNetWorkflowSkills__status_skill.py tests/projectkoios/workflow/test__PetriNetWorkflowSkills__interactive_control_skill.py -q
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow
git diff --check
```

If VULCAN consolidates skill tests into one file, report the exact focused pytest command used.

## Pause triggers

Pause and ask USER/HERMES if implementation would require:

- changing Petri-net runtime or workflow CLI status behavior;
- editing the workflow-net fixture;
- firing or simulating transitions;
- adding persistence or canonical workflow-state storage;
- adding live adapters/session reads;
- integrating Operator Console;
- coupling workflow-object runtime behavior;
- adding schema/product authority;
- changing global skill directories;
- changing queue discipline;
- replacing or superseding `pi-skill-determinism-slice-0`.

## Handoff

This brief is ready for USER/HERMES review. Do not route to VULCAN implementation until USER/HERMES approves implementation or explicitly authorizes direct coding.
