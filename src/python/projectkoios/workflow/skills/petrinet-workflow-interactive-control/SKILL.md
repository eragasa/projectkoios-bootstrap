---
name: petrinet-workflow-interactive-control
description: |
  Operate Petri-net workflow sessions interactively by inspecting status, summarizing observed state, recommending one next action, and asking before action.
metadata:
  surface: projectkoios.workflow.petrinet.agent_affordances
  parent_effort: petri-net-workflow-inspectability
  previous_slice: petrinet-workflow-current-slice-status-reconciliation-slice-2
  command: uv run projectkoios workflow status
  runtime_mutation_allowed: false
  harness_global_propagation: deferred
---

# Petri-net workflow interactive control

Use this workflow-local affordance when the user asks what is happening, expresses confusion or frustration, asks to operate the workflow interactively, asks what is next, or asks to regain control of a Petri-net workflow session.

This skill belongs to the existing Petri-net workflow harness / workflow inspectability effort. It is not a new project identity and is not harness-global propagation.

## Operating pattern

Always use this pattern:

```text
inspect → summarize → recommend → ask/act
```

1. **Inspect first.** Run or consult the read-only status command from the repository root when possible:

   ```bash
   uv run projectkoios workflow status
   ```

2. **Summarize observed state before recommending action.** Include:
   - workflow id;
   - current token/place;
   - active slice if visible;
   - enabled transitions;
   - whether user decision is required;
   - active vs queued vs superseded/deferred distinction when known from workspace state.

3. **Recommend exactly one primary next action** unless the user explicitly asks for options.

4. **Ask before acting** when user decision is required, when the action would edit files, route work to another agent, launch subagents, change active/queued state, or perform any user-decision-gated action.

5. **Act only after approval** when the user explicitly approves the action or has already delegated a narrow action in the current request.

6. **Keep the explanation user-readable.** Do not treat tests, commits, or internal artifact lists as the main explanation of progress unless the user asks for evidence.

7. **Preserve queue discipline.** Do not replace current active work with new incoming topics unless USER/HERMES explicitly says to switch active work.

8. **If the command fails or is unavailable,** report the failure as an inspectability gap and do not invent workflow id, active slice, current token/place, enabled transitions, user-decision state, active work, or queued work.

## Recommended response shape

```text
Petri-net interactive control:
- observed: <workflow/token/place/user-decision summary>
- active: <active item or none>
- queued/deferred: <short queue summary if relevant>
- recommendation: <one clear next action>
- approval needed: <yes/no and why>
```

## Required boundaries

- Do not fire transitions.
- Do not mutate workflow state.
- Do not edit files unless the user explicitly approves or delegates a narrow edit.
- Do not launch subagents or route work merely because a transition is enabled.
- Do not activate queued work without explicit USER/HERMES direction.
- Do not treat the static bootstrap workflow-net fixture as canonical workflow authority.
- Do not treat tests as the main explanation of progress.
- Do not introduce persistence, schema authority, live adapter/session reads, role/permission semantics, Operator Console integration, workflow-object runtime coupling, or product/mothership authority.
- Do not change Petri-net runtime behavior or `uv run projectkoios workflow status` behavior from this skill.
- Do not propagate this skill into global skill directories.
- Do not replace or supersede `pi-skill-determinism-slice-0`; leave that work queued unless USER/HERMES explicitly activates it.
