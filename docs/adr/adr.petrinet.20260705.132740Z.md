```json
{
  "title": "Separate Petri-net Definition, Marking, Binding, and Execution Runtime",
  "artifact_type": "adr",
  "status": "accepted",
  "datetime": "20260705.132740",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "bootstrap-held workflow Petri-net implementation vocabulary and runtime separation",
  "proposal_surface": "dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.record.json",
  "canonical_location": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "source_artifacts": [
    "dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.record.json",
    "dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.schema-backed.md",
    "dev/petrinet-definition-marking-runtime/user-proposal.20260705.132740_petrinet-definition-marking-runtime.md",
    "dev/petrinet-definition-marking-runtime/decision-source-addendum.20260705.md",
    "src/python/projectkoios/workflow/petrinet.py",
    "docs/petri-net-model.md",
    "docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md",
    "docs/plans/projectkoios-workflow-petri-net-executor.md"
  ],
  "review_inputs": [
    "HERMES initial review: revise-before-acceptance for schema validation, lifecycle state, prior vocabulary, dirty-state boundary, and acceptance boundary",
    "KOIOS initial review: preserve user proposal, add current-symbol evidence, vocabulary mapping, source distinctions, and bootstrap/extraction boundary",
    "VULCAN naming review: mandatory prefixed implementation names, low-risk rename slice, kinded arcs under YAGNI",
    "KOIOS re-review: durable later-decision source, conceptual-vs-prefixed cleanup, exact prior vocabulary disposition, bounded older-doc follow-on",
    "HERMES final re-review: accept-ready; route to user for acceptance/promotion decision"
  ],
  "accepted_from": "dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.record.json",
  "accepted_by": "user direction \"accepted\" after HERMES final re-review",
  "acceptance_boundary": "Architecture authority for bootstrap-held workflow implementation slice only; does not validate current dirty implementation or authorize broad workflow/product architecture."
}
```

# ADR 20260705.132740Z: Separate Petri-net Definition, Marking, Binding, and Execution Runtime

## Status

accepted

## Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this ADR are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

## Provenance

Origin: user proposal and follow-up acceptance direction
From: user
Acting-As: ATHENA
Scope: projectkoios-bootstrap bootstrap-held workflow Petri-net implementation slice
Repository: projectkoios-bootstrap
Architecture-Domain: workflow-runtime / Petri-net model
Proposal-Record: `dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.record.json`
Proposal-Projection: `dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.schema-backed.md`
Accepted-Location: `docs/adr/adr.petrinet.20260705.132740Z.md`
Accepted-By: user direction "accepted" after HERMES final re-review

Acceptance records vocabulary and ownership separation only. It does not validate current dirty `src/python/projectkoios/workflow/*` implementation changes, authorize broad workflow/product architecture, or complete any Vulcan implementation slice. Older workflow executor ADR/plan updates and implementation remediation require bounded follow-on handoffs.

Durable source artifacts:

- `dev/petrinet-definition-marking-runtime/user-proposal.20260705.132740_petrinet-definition-marking-runtime.md`
- `dev/petrinet-definition-marking-runtime/decision-source-addendum.20260705.md`
- `dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.record.json`
- `dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.schema-backed.md`

Review inputs:

- HERMES initial review: revise-before-acceptance for schema validation, lifecycle state, prior vocabulary, dirty-state boundary, and acceptance boundary.
- KOIOS initial review: preserve user proposal, add current-symbol evidence, vocabulary mapping, source distinctions, and bootstrap/extraction boundary.
- VULCAN naming review: mandatory prefixed implementation names, low-risk rename slice, kinded arcs under YAGNI.
- KOIOS re-review: durable later-decision source, conceptual-vs-prefixed cleanup, exact prior vocabulary disposition, bounded older-doc follow-on.
- HERMES final re-review: accept-ready; route to user for acceptance/promotion decision.

## Context

The workflow Petri-net model needs a clean separation between static graph definition, runtime marking, binding witnesses, and execution/runtime events.

### Concern
- MUST Model the static net as N = (P, T, A), where places, transitions, and arcs define possible structure.
- MUST Model the runtime state as a marking M mapping place identifiers to token multisets.
- MUST NOT Let Place own tokens or callbacks because token distribution belongs to the marking and updates belong to runtime execution.
- SHOULD Correct misleading vocabulary such as FiringRule when the object is an imperative request rather than a semantic rule.

### Relationship To Existing Artifacts

This draft refines workflow Petri-net vocabulary found in existing drafts, plans, and implementation reports; those artifacts remain provenance until explicitly updated.

### Concern
- MUST Treat docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md and docs/plans/projectkoios-workflow-petri-net-executor.md as source/provenance for the prior vocabulary, not as silently superseded text.
- MUST State in any acceptance or follow-on brief whether FiringRule, ExecutionState, Binding, Arc, and WorkflowNet vocabulary is superseded, refined, or retained for compatibility.
- SHOULD Update existing workflow docs and plans only through an explicit follow-on documentation or implementation handoff after acceptance.

### Naming Compatibility

Conceptual Petri-net names may map to prefixed implementation names when needed for extraction readability or conflict avoidance.

### Concern
- MUST Define whether conceptual Place, Transition, Token, Arc, Binding, and Marking map to implementation names such as PetriNetPlace, PetriNetTransition, PetriNetToken, PetriNetArc, PetriNetBinding, and PetriNetMarking.
- MUST Require a deliberate implementation choice between shorter conceptual names and prefixed names before large-scale rename work proceeds.
- SHOULD Prefer compatibility aliases or staged migration when dirty implementation work already depends on prefixed names.

### Dirty State Boundary

Current dirty implementation and report files are context for this draft, not validation authority or accepted completion evidence.

### Concern
- MUST Not treat current dirty workflow implementation changes as retroactively validated by acceptance of this architecture decision.
- MUST Require Vulcan implementation evidence and Athena conformance review before marking any follow-on implementation complete.
- SHOULD Route accepted follow-on work through a bounded remediation brief that accounts for existing dirty implementation state.

### Durable User Proposal Source

The initiating user proposal is preserved as an editable source artifact because chat/session context is not durable repository provenance.

### Concern
- MUST Use dev/petrinet-definition-marking-runtime/user-proposal.20260705.132740_petrinet-definition-marking-runtime.md as the durable user-proposal source for review and future revisions.
- MUST NOT Rely on hidden chat context as the only source for user-proposed vocabulary, rejection rationale, or execution-flow claims.

### Prior Vocabulary Tension

Existing workflow ADR and plan surfaces use vocabulary that this draft narrows or replaces for the current implementation slice.

### Concern
- MUST Treat FiringRule, ExecutionState, WorkflowNet, Orchestrator, Event, Arc, Guard, Binding, ExecutionTrace, and EventLog in the older workflow executor draft as prior vocabulary requiring explicit reconciliation.
- MUST If accepted, this ADR narrows and supersedes specific conflicting prior workflow-executor draft vocabulary for this bootstrap implementation slice while preserving those files as provenance.
- SHOULD Record follow-on documentation edits to the older ADR/plan surfaces as a separate bounded state transition.

### Vocabulary Mapping

Reviewers need an explicit old/current to proposed vocabulary map before acceptance or implementation routing.

### Concern
- MUST Use the prefixed implementation names specified by this draft for the accepted implementation slice; do not substitute shorter conceptual names in code without a later accepted change.
- MUST Map PetriNetBinding to TransitionBinding, PetriNetFiringRule to FiringRequest, and PetriNetExecutionState to PetriNetState unless compatibility requires staged aliases.
- MUST Map PetriNetArc plus input/output kind to the accepted first-slice implementation boundary; defer InputArc and OutputArc split under YAGNI.
- SHOULD Mark TransitionFiredEvent and MarkingChangedEvent as proposed event vocabulary derived from user direction, not as currently observed petrinet.py classes.

### Bootstrap Extraction Boundary

Acceptance in this repository governs the bootstrap-held workflow implementation slice, not product-domain workflow semantics elsewhere.

### Concern
- MUST Limit authority to projectkoios-bootstrap and the bootstrap-held src/python/projectkoios/workflow implementation slice.
- MUST NOT Decide mothership or future product-domain workflow semantics without a separate accepted decision in that repository/domain.
- MUST NOT Authorize broad workflow orchestration, external event-bus integration, adapter/backend selection changes, or product-domain architecture from this vocabulary decision alone.

### Implementation Naming Compatibility Decision Candidate

Vulcan review and user decision require prefixed implementation names while mapping them to shorter conceptual architecture vocabulary.

### Concern
- MUST Map conceptual Place, Token, Transition, and Marking to PetriNetPlace, PetriNetToken, PetriNetTransition, and PetriNetMarking in implementation for extraction clarity and grep/readability.
- MUST Use PetriNetFiringRequest for conceptual FiringRequest, PetriNetTransitionBinding for conceptual TransitionBinding, and PetriNetState for the net-plus-marking state object.
- MUST Keep PetriNetArc plus PetriNetArcKind for the first implementation slice under YAGNI; do not split into PetriNetInputArc and PetriNetOutputArc until a later accepted need requires stronger type boundaries.
- MUST Use prefixed event names PetriNetTransitionFiredEvent and PetriNetMarkingChangedEvent for implementation DataObjects.

### Reusable PetriNet And WorkflowNet Boundary

PetriNet is expected to remain a reusable generic substrate for applications beyond workflow, so workflow-specific semantics should live in a wrapper or specialization.

### Concern
- MUST Keep PetriNet generic enough to be repurposed for non-workflow applications.
- MUST Use WorkflowNet or an equivalent domain wrapper for workflow-specific semantics, validation, adapters, and runtime conventions that should not pollute the generic PetriNet substrate.
- MUST NOT Collapse workflow-domain concerns into PetriNet merely because the current implementation slice lives under projectkoios.workflow.
- SHOULD Allow WorkflowNet to subclass, contain, or adapt PetriNet only when the implementation preserves the generic PetriNet boundary.

### Event Emitter Debugging Boundary

Runtime event emission is required for debugging state transitions, but the first slice should keep emission bounded and inspectable.

### Concern
- MUST Include an event emitter or equivalent event collection surface in the first runtime execution slice so transition firing and marking changes can be debugged.
- MUST Emit or record prefixed event DataObjects such as PetriNetTransitionFiredEvent and PetriNetMarkingChangedEvent when execution changes state.
- MUST NOT Expand the first slice into external event-bus integration, distributed messaging, or broad observability infrastructure.
- SHOULD Keep the first event emitter in-process, deterministic, and easy to inspect in tests.

### Older Draft And Process Surface Update Policy

Because most related ADRs are drafts and the user expects process-oriented surfaces to become Petri-net defined over time, accepted vocabulary should be propagated to older workflow draft/plan surfaces through a bounded follow-on.

### Concern
- MUST After acceptance, create a bounded documentation/control-surface follow-on to update older workflow executor ADR and plan surfaces to reflect this ADR vocabulary rather than leaving conflicting draft vocabulary in place.
- MUST Preserve older documents as provenance while making their current-control text point to the accepted Petri-net vocabulary decision.
- MUST Treat the update as a bounded documentation/control-surface follow-on before or alongside Vulcan implementation routing, not as silent direct edit authority.
- SHOULD Record the user-directed expectation that process-oriented architecture surfaces will increasingly be expressed through Petri-net vocabulary unless a later accepted decision narrows that direction.

### Specific Prior Vocabulary Disposition

Accepted implementation vocabulary should explicitly supersede, refine, or retain prior terms from workflow executor drafts and plans.

### Concern
- MUST Supersede FiringRule and PetriNetFiringRule with PetriNetFiringRequest for the first implementation slice.
- MUST Supersede ExecutionState and PetriNetExecutionState with PetriNetState when the object only pairs PetriNet and PetriNetMarking.
- MUST Refine Binding and PetriNetBinding to PetriNetTransitionBinding as the witness for selected consumed tokens.
- MUST Retain PetriNetArc plus PetriNetArcKind for the first slice under YAGNI rather than splitting InputArc and OutputArc now.
- MUST Retain WorkflowNet as a workflow-domain wrapper or specialization because PetriNet is a reusable generic substrate.

## Decision

Separate the implementation into static net definition, runtime state, and execution runtime layers with explicit names and ownership boundaries.

### Concern
- MUST Use conceptual static-definition vocabulary PetriNet, Place, Transition, InputArc, OutputArc, and TransitionGuard while requiring prefixed implementation names and kinded arcs for the first slice.
- MUST Use conceptual runtime vocabulary Token, Marking, TransitionBinding, FiringRequest, and PetriNetState while requiring the mapped prefixed implementation names for code.
- MUST Use conceptual runtime vocabulary BindingResolver and PetriNetExecutor plus prefixed implementation event DataObjects and bounded in-process event emission for debugging.
- MUST Limit acceptance to architecture vocabulary and future refactor authority; acceptance must not validate current dirty implementation.
- MUST Preserve PetriNet as a reusable generic substrate and place workflow-specific behavior in WorkflowNet or an equivalent domain wrapper.
- MUST Treat prefixed implementation names as mandatory for this implementation slice: PetriNetPlace, PetriNetToken, PetriNetTransition, PetriNetArc, PetriNetArcKind, PetriNetMarking, PetriNetTransitionBinding, PetriNetFiringRequest, PetriNetState, PetriNetTransitionFiredEvent, and PetriNetMarkingChangedEvent.
- MUST If accepted, promptly reconcile older workflow draft and plan surfaces so their current vocabulary points to this accepted Petri-net separation decision.
- MUST NOT Use FiringRule, broad ExecutionState for net-plus-marking only, on_update, place.tokens, or transition.fire_mutating_state as controlling vocabulary.

## Consequences

The model is expected to become easier to validate against Petri-net mathematics and safer for replay, provenance, dry-run execution, and UI/runtime integration as follow-on implementation evidence accumulates.

### Concern
- MUST Represent execution as (N, M) transitioning to (N, M prime) through a selected transition and transition binding.
- MUST Keep graph objects immutable and free of runtime mutation ownership.
- SHOULD Prepare colored-token support by keeping token color/data on Token and token selection on TransitionBinding, consistent with docs/petri-net-model.md and current PetriNetToken.color implementation.
- SHOULD Make runtime changes inspectable through explicit fired/marking-changed events rather than vague update callbacks.

## Acceptance Criteria

A reviewer must be able to classify every Petri-net object as static definition, runtime state, binding witness, or executor/event behavior.

### Concern
- MUST Show that Place has identity and optional metadata but no token collection.
- MUST Show that Marking owns the mapping from place identifiers to immutable token collections.
- MUST Show that FiringRequest replaces FiringRule for explicit transition-fire requests.
- MUST Show that PetriNetState pairs exactly a static PetriNet with the current Marking.
- MUST Show that executor/runtime code, not Place or Transition data objects, owns state update and event emission behavior.

## Implementation Brief

If accepted, Vulcan should refactor the workflow Petri-net implementation and tests to match the separated vocabulary and ownership model.

### Concern
- MUST Keep PetriNetArc plus PetriNetArcKind for the first implementation slice under YAGNI; defer PetriNetInputArc and PetriNetOutputArc unless a later accepted decision requires stronger type boundaries.
- MUST Rename PetriNetFiringRule to PetriNetFiringRequest and PetriNetExecutionState to PetriNetState where the object only contains net and marking.
- MUST Rename or introduce PetriNetTransitionBinding as the implementation witness for selected consumed tokens satisfying a transition.
- MUST Keep firing semantics in PetriNetExecutor or equivalent runtime service that returns a new PetriNetState and emits explicit events.
- MUST Account for current dirty implementation state and existing prefixed names before applying renames or semantic refactors.
- MUST Add a bounded event emitter or event collection interface sufficient to debug transition firing and marking changes in tests.
- MUST Use mandatory prefixed implementation names for this slice and update imports/tests/docs accordingly; shorter conceptual names remain architecture vocabulary only.
- MUST Produce a bounded documentation/control-surface follow-on for older workflow executor ADR and plan updates before or alongside implementation routing; acceptance does not authorize silent direct edits outside that follow-on.
- SHOULD Add identifier aliases such as PlaceId, TransitionId, and TokenId if that improves type readability without overbuilding the slice.
- SHOULD First implementation slice should include PetriNetFiringRequest, PetriNetState, PetriNetTransitionBinding, existing kinded arcs, prefixed event DataObjects, and a bounded in-process event emitter for debugging; it should not add external event-bus integration.
- SHOULD Keep or introduce WorkflowNet as the workflow-domain wrapper around the generic PetriNet substrate when workflow-specific semantics are needed.

## Non Goals

This decision does not require a complete colored Petri-net engine or UI/event-bus implementation in the first refactor slice.

### Concern
- MUST NOT Implement broad workflow orchestration features beyond the naming and ownership separation unless separately authorized.
- MUST NOT Make Place a mutable token container or callback owner.
- MUST NOT Collapse static PetriNet definition and runtime Marking into one mutable object.
- MAY Avoid external event-bus integration or broad observability infrastructure in the first slice; bounded in-process event emission for debugging is in scope.

## Validation Expectations

Validation should prove semantic separation, immutable state transitions, and stable compatibility with existing workflow tests or documented migrations.

### Concern
- SHOULD Test that firing consumes input tokens, produces output tokens, and returns a new Marking and PetriNetState without mutating the old state.
- SHOULD Test that TransitionBinding records consumed tokens by input place and is used by guard or firing validation.
- SHOULD Test that Place and Transition definitions do not contain runtime token collections.
- SHOULD Run workflow unit tests, type checks, and any repository Python policy checks affected by the refactor.

## Rejected

### Prior vocabulary rejected by this draft

Reason: The names imply incorrect ownership or overly broad responsibility relative to the proposed architecture.

```text
Rejected terms and patterns: FiringRule, broad ExecutionState for only net-plus-marking, vague on_update callbacks on graph objects, place.tokens, and transition.fire_mutating_state().
```

### Original extended user proposal

Reason: The schema-backed draft captures the proposal in structured sections; durable source artifacts preserve the original proposal and later decisions.

```text
The original user proposal is durably preserved at dev/petrinet-definition-marking-runtime/user-proposal.20260705.132740_petrinet-definition-marking-runtime.md. Later user decisions and Vulcan/KOIOS review summaries are preserved at dev/petrinet-definition-marking-runtime/decision-source-addendum.20260705.md.
```

### Review and revision location

Reason: Generated projection is non-editable; reviewers need an explicit comment/revision target.

```text
The generated Markdown projection is non-editable. Review comments should identify JSON record fields/sections in dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.record.json or be captured in separate review/source artifacts, then the projection should be regenerated.
```

### Vocabulary mapping table

Reason: The current schema represents tables as rejected/freeform Markdown; this mapping is still durable reviewer context.

```text
| Conceptual term | Recommended implementation term | Layer | Disposition |
|---|---|---|---|
| Place | PetriNetPlace | Static definition | Keep prefixed for extraction clarity and grep/readability. |
| Token | PetriNetToken | Runtime state | Keep prefixed and preserve color/data support. |
| Transition | PetriNetTransition | Static definition | Keep prefixed. |
| Marking | PetriNetMarking | Runtime state | Keep prefixed. |
| Arc / InputArc / OutputArc | PetriNetArc + PetriNetArcKind initially | Static definition | Keep kinded arc for first slice under YAGNI; defer PetriNetInputArc/PetriNetOutputArc to a later accepted need. |
| Binding / TransitionBinding | PetriNetTransitionBinding | Runtime state | Rename from PetriNetBinding for clarity. |
| FiringRequest | PetriNetFiringRequest | Runtime request | Rename from PetriNetFiringRule because current object is request, not semantic rule. |
| PetriNetState | PetriNetState | Runtime state | Rename from PetriNetExecutionState when object only pairs PetriNet and marking. |
| TransitionFiredEvent | PetriNetTransitionFiredEvent | Runtime event | Required prefixed event DataObject for bounded in-process debugging emission; no external event bus in first slice. |
| MarkingChangedEvent | PetriNetMarkingChangedEvent | Runtime event | Required prefixed event DataObject for bounded in-process debugging emission; no external event bus in first slice. |
| WorkflowNet | WorkflowNet(PetriNet) or domain wrapper | Static definition/domain wrapper | Retain for workflow-specific semantics because PetriNet is intended as a reusable generic substrate. |
```
