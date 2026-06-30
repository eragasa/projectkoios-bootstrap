# Review Principles

## Architecture Principles

### AP-001: Preserve The Core Boundary

Core schema/model code must not depend on UI, runtime engines, Petri-net
libraries, process-mining libraries, or external adapters.

Good:

```text
schema <- runtime
schema <- ui
schema <- petri
schema <- adapters
```

Bad:

```text
schema -> runtime
schema -> ui
schema -> snakes
schema -> pm4py
```

### AP-002: Separate Objects From Actions

Objects carry state.

Actions transform state.

`ObjectClass` defines artifact/token types.

`ActionClass` defines transition/action types.

Object classes should not execute actions.

Action classes should not own persistent object state.

### AP-003: Keep Petri-Net Compatibility Possible

The workflow model should be expressible as places, transitions, markings,
guards, and firing events.

The core model should not directly depend on a Petri-net library.

### AP-004: Dry-Run Before Mutation

Any mutating action should have a dry-run path that reports the expected state
change before execution.

### AP-005: Provenance Is Required

Any meaningful state transition should produce a provenance record.

### AP-006: Prefer Small Current Abstractions

Do not add abstractions for speculative future needs.

A new abstraction is justified only if it protects a current boundary, removes
real duplication, isolates an unstable dependency, or represents a real domain
concept.

## Code Principles

### CP-001: Public API First

Tests should primarily exercise public behavior.

### CP-002: Explicit Mutation

Mutating functions should be named and typed clearly.

Good:

- `dry_run()`
- `fire()`
- `commit()`

Bad:

- `process()`
- `resolve()`
- `update_everything()`

### CP-003: Thin Adapters

External libraries belong behind adapters.

### CP-004: Test Invariants

Tests should check important invariants:

- dry-run does not mutate state
- disabled actions cannot fire
- core does not import UI
- core does not import Petri-net backends
- successful action produces provenance
