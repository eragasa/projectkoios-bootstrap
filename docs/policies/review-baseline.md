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

### AP-007: Review Across Control Surfaces

Review should look for cross-surface coherence, improvement opportunities, and
debt that should be combined, split, or promoted.

Findings should be triaged into:

- recommendation only
- debt item
- implementation task
- ADR candidate

Human judgment may override automated priority when the leverage/effort balance
justifies it.

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

### CP-005: Separate Objects From Actions

Implementation should preserve the separation between state-bearing objects and
state-transforming actions.

Good:

- `DataObject`
- `ActionObject`
- explicit action classes with clear boundaries

Bad:

- dangling utility functions that mutate control surfaces without ownership
- untyped helper logic that hides state transitions

### CP-006: Keep Control-Surface Boundaries Visible

Code that participates in a control surface should make its boundary explicit in
names, docstrings, and types.

## Review Template Additions

### C5: PEP 8 And Tooling

Result: pass / concern / fail / unknown

Evidence:

Tool result:

Required change:

### C6: Public Documentation

Result: pass / concern / fail / unknown

Evidence:

Missing docstrings:

Missing parameter documentation:

Missing return-value documentation:

Missing exception documentation:

Missing side-effect, mutation, or I/O documentation:

Required change:

### C7: Type Annotations

Result: pass / concern / fail / unknown

Evidence:

Missing or weak annotations:

Required change:

### C8: Public Examples

Result: pass / concern / fail / unknown

Evidence:

Example gap:

Required change:

### R1: Control-Surface Coherence

Result: pass / concern / fail / unknown

Evidence:

Cross-surface agreement:

Required change:

### R2: Improvement / Debt Discovery

Result: pass / concern / fail / unknown

Evidence:

Findings:

Debt triage:

Required change:
