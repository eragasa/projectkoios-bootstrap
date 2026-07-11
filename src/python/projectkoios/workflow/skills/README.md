# Petri-net workflow agent affordances

This directory contains agent-facing affordances for the Project Koios Petri-net workflow harness.

These files teach agents how to inspect and operate the existing workflow runtime surface before advancing work:

- `petrinet-workflow-status` explains how to consume and report the read-only status command:

  ```bash
  uv run projectkoios workflow status
  ```

- `petrinet-workflow-interactive-control` explains how to conduct operator-facing interactive control conversations with the pattern inspect → summarize → recommend → ask/act.

The affordances in this directory are part of the workflow inspectability effort. They are workflow-local, not a new project identity, not product authority, and not harness-global skill propagation by themselves.

## Boundaries

- These files do not authorize runtime mutation.
- These files do not authorize transition firing or dry-run behavior.
- These files do not authorize persistence or durable workflow-state storage.
- These files do not make the static bootstrap workflow-net fixture canonical workflow authority.
- These files do not authorize live adapter/session reads, Operator Console integration, workflow-object runtime coupling, schema authority, role/permission expansion, or product/mothership authority.
- These files do not propagate themselves into `agents/global/*/skills/`.
- Interactive workflow-control behavior must still ask before file edits, routing, subagent launch, active/queued-state change, or user-decision-gated action.
