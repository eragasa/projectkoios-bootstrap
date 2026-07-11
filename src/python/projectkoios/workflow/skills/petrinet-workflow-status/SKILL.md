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

# Petri-net workflow status

Use this Petri-net workflow affordance when starting or resuming Petri-net workflow work, before advancing workflow state, during handoffs, or when the user asks what is active, blocked, or next.

This skill consumes the existing read-only status command. It does not create a new project identity and does not authorize workflow mutation.

## Procedure

1. From the repository root when possible, run:

   ```bash
   uv run projectkoios workflow status
   ```

2. Read the command output. Summarize only observed status; do not fabricate workflow state if the command fails or is unavailable.

3. Report the status in this form:

   ```text
   Petri-net workflow status:
   - workflow: <workflow id>
   - current token/place: <token> at <place>
   - enabled transitions: <transition list>
   - user decision required: yes/no
   - recommendation: <one sentence>
   ```

4. If `user decision required: yes`, stop and ask or await approval unless the user explicitly delegated the next action.

5. If the command fails or is unavailable, report the failure as an inspectability gap and do not invent an active workflow, token/place, enabled transition, or recommendation.

## Required boundaries

- Do not fire transitions.
- Do not mutate workflow state.
- Do not treat the static bootstrap fixture as canonical workflow authority.
- Do not launch subagents merely because a transition is enabled.
- Do not expand scope beyond the user's current request.
- Do not change `uv run projectkoios workflow status` behavior from this skill.
- Do not introduce persistence, schema authority, live adapter/session reads, role/permission semantics, Operator Console integration, workflow-object runtime coupling, or product/mothership authority.

## Recommendation guidance

The recommendation must be one clear sentence grounded in the observed status. For example, if user decision is required, recommend asking the user to approve or choose the next bounded workflow action. If no decision is required, recommend the next inspectable action only within the user's current request.
