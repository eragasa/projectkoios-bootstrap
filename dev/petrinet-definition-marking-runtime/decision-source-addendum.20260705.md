# Decision source addendum 20260705: Petri-net separation follow-up decisions

## Provenance

Origin: interactive user decisions and intercom review during Athena drafting session
From: user, VULCAN, KOIOS, HERMES
Acting-As: ATHENA for preservation
Repository: projectkoios-bootstrap
Scope: Petri-net definition, marking, binding, runtime, naming, and follow-on documentation policy

## User follow-up decisions

After the initial proposal was drafted, the user resolved remaining open questions as follows:

1. Arc model: follow Vulcan/YAGNI; keep `PetriNetArc + PetriNetArcKind` for the first implementation slice and defer `PetriNetInputArc` / `PetriNetOutputArc` unless a later accepted need requires stronger type boundaries.
2. Reusable substrate boundary: `PetriNet` will likely be repurposed for other applications, so it should remain generic; workflow-specific semantics belong in `WorkflowNet` or an equivalent domain wrapper.
3. Event scope: an event emitter is necessary for debugging; first runtime slice should include bounded in-process event emission and prefixed event DataObjects, but not external event-bus or broad observability integration.
4. Naming authority: prefixed implementation names are mandatory for the first implementation slice; shorter names remain conceptual architecture vocabulary.
5. Older docs: after acceptance, update older workflow executor ADR/plan surfaces promptly because most related ADRs are drafts and process-oriented surfaces are expected to become Petri-net defined over time.
6. Acceptance path: request KOIOS re-review, integrate changes, then request HERMES re-review before acceptance.

## Vulcan naming review summary

Vulcan recommended:

- Keep prefixed implementation names for generic primitives for extraction clarity and grep/readability.
- Map conceptual `Place`, `Token`, `Transition`, and `Marking` to implementation `PetriNetPlace`, `PetriNetToken`, `PetriNetTransition`, and `PetriNetMarking`.
- Rename `PetriNetFiringRule` to `PetriNetFiringRequest`.
- Rename `PetriNetExecutionState` to `PetriNetState`.
- Rename `PetriNetBinding` to `PetriNetTransitionBinding`.
- Keep `PetriNetArc + PetriNetArcKind` for the first slice unless an accepted decision requires an arc split.
- Use prefixed event names: `PetriNetTransitionFiredEvent` and `PetriNetMarkingChangedEvent`.
- Treat rename/import drift as the main migration risk; do not mix this implementation slice with unrelated dirty workspace files.

## KOIOS re-review summary

KOIOS re-review found most prior provenance concerns addressed and requested one cleanup pass before HERMES/user acceptance:

- Preserve later user decisions durably, not only as message refs.
- Clarify conceptual vocabulary versus mandatory prefixed implementation names.
- Remove stale text saying full source remains only in session context.
- Preserve Vulcan naming review as repo-local source context.
- Name exact prior terms that are superseded, retained, or refined.
- Clarify that older-doc updates should happen through a bounded follow-on handoff, not silent direct edits.
- Phrase prospective benefits and broad Petri-net process direction as expected/user-directed rather than already validated.

## Authority note

This addendum is source/provenance for the draft ADR. It is not accepted architecture authority by itself.
