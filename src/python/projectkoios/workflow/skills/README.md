# Petri-net workflow agent affordances

This directory contains agent-facing affordances for the Project Koios Petri-net workflow harness.

These files teach agents how to inspect the existing workflow runtime surface before advancing work. The first affordance, `petrinet-workflow-status`, explains how to consume:

```bash
uv run projectkoios workflow status
```

The affordances in this directory are part of the workflow inspectability effort. They are not a new project identity, not product authority, and not harness-global skill propagation by themselves.

## Boundaries

- These files do not authorize runtime mutation.
- These files do not authorize transition firing.
- These files do not authorize persistence or durable workflow-state storage.
- These files do not make the static bootstrap workflow-net fixture canonical workflow authority.
- These files do not propagate themselves into `agents/global/*/skills/`.
- Interactive workflow-control behavior remains deferred to a later slice.
