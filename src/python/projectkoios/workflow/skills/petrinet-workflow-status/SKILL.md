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

4. If `user decision required: yes`, treat it as a workflow-state gate only. Stop before activating queued work, firing transitions, changing workflow fixtures, or choosing a next workflow slice. Do not stop unrelated user-delegated implementation, documentation, validation, review, or investigation work merely because the static workflow fixture is waiting on a decision.

5. If the current user request explicitly delegates a non-workflow-state task, continue that task after reporting the observed workflow status in one concise sentence.

6. If the command fails or is unavailable, report the failure as an inspectability gap and do not invent an active workflow, token/place, enabled transition, or recommendation.

## Required boundaries

- Do not fire transitions.
- Do not mutate workflow state.
- Do not treat the static bootstrap fixture as canonical workflow authority.
- Do not launch subagents merely because a transition is enabled.
- Do not expand scope beyond the user's current request.
- Do not change `uv run projectkoios workflow status` behavior from this skill.
- Do not introduce persistence, schema authority, live adapter/session reads, role/permission semantics, Operator Console integration, workflow-object runtime coupling, or product/mothership authority.

## Recommendation guidance

The recommendation must be one clear sentence grounded in the observed status and scoped to the user's current request. If user decision is required, recommend asking the user to approve or choose the next bounded workflow action only when the user is asking to advance workflow state. For ordinary delegated work, state that the workflow fixture is decision-gated but does not block the requested non-workflow-state task.
