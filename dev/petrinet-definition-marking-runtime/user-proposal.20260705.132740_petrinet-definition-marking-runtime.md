# User proposal 20260705.132740: Separate Petri-net definition, marking, binding, and execution runtime

## Provenance

Origin: interactive user prompt
From: user
Acting-As: user
Repository: projectkoios-bootstrap
Scope: workflow Petri-net implementation vocabulary and runtime separation

## Proposal excerpt

The user proposed an ADR titled `Separate Petri-net definition, marking, binding, and execution runtime`.

Core proposal:

- A Petri net has two distinct layers: static net structure and current marking.
- Static net structure is `N = (P, T, A)` where `P` is places, `T` is transitions, and `A` is arcs.
- Runtime state is a marking `M : P -> Multiset(Token)` mapping each place to the multiset of tokens located there.
- Places do not own tokens; tokens belong to the current marking.
- This separation is required for execution semantics, replay, provenance, validation, and future colored Petri-net compatibility.
- `FiringRule` is misleading because the object is an explicit request to fire a transition, not a semantic rule.
- `ExecutionState` is too broad if the object only pairs a static net with current marking.

Proposed conceptual layers:

1. Static net definition:
   - `PetriNet`
   - `Place`
   - `Transition`
   - `InputArc`
   - `OutputArc`
   - `TransitionGuard`

2. Runtime state:
   - `Token`
   - `Marking`
   - `TransitionBinding`
   - `FiringRequest`
   - `PetriNetState`

3. Execution runtime:
   - `BindingResolver`
   - `PetriNetExecutor`
   - `TransitionFiredEvent`
   - `MarkingChangedEvent`

Rejected vocabulary/patterns:

- `FiringRule`
- `ExecutionState`
- vague `on_update`
- `place.tokens`
- `transition.fire_mutating_state()`

Execution flow proposed:

```text
PetriNetState + FiringRequest
→ resolve TransitionBinding
→ validate TransitionGuard
→ consume input tokens
→ produce output tokens
→ return new PetriNetState
→ emit event
```

Minimal implementation shape included immutable dataclasses for `PetriNet`, `Place`, `Transition`, `InputArc`, `OutputArc`, `Token`, `Marking`, `PetriNetState`, `TransitionBinding`, and `FiringRequest`.

## Preservation note

This file preserves the user's proposal as durable repository provenance for the schema-backed ADR draft. It is source input, not accepted architecture authority by itself.
