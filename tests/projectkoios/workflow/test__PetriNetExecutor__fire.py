from __future__ import annotations

from projectkoios.workflow import (
    PetriNetArc,
    PetriNetArcKind,
    PetriNetFiringRequest,
    PetriNetState,
    PetriNetFiringResult,
    PetriNetMarking,
    PetriNetMarkingChangedEvent,
    PetriNetRuntimeEvent,
    PetriNetPlace,
    PetriNetToken,
    PetriNetTransition,
    PetriNet,
    PetriNetExecutor,
    PetriNetTransitionFiredEvent,
)


def test__PetriNetExecutor__fire__moves_token_and_records_event() -> None:
    """Validate firing an enabled transition moves a token and records trace."""
    # Workflow net fixture moves one token from draft to review.
    net: PetriNet = PetriNet(
        places=(PetriNetPlace("draft"), PetriNetPlace("review")),
        transitions=(PetriNetTransition("submit"),),
        arcs=(
            PetriNetArc(place_id="draft", transition_id="submit", kind=PetriNetArcKind.INPUT),
            PetriNetArc(place_id="review", transition_id="submit", kind=PetriNetArcKind.OUTPUT),
        ),
    )
    # PetriNetToken fixture represents the colored artifact being routed.
    token: PetriNetToken = PetriNetToken.from_color("artifact-1", {"kind": "implementation-brief"})
    # Initial state puts the token in the draft place.
    state: PetriNetState = PetriNetState(net=net, marking=PetriNetMarking.from_tokens({"draft": [token]}))
    # Runtime owns enabledness checks and firing semantics.
    runtime: PetriNetExecutor = PetriNetExecutor()

    # Firing request identifies the transition to execute.
    request: PetriNetFiringRequest = PetriNetFiringRequest(transition_id="submit")
    # Fired result contains the next marking and emitted debug events.
    result: PetriNetFiringResult = runtime.fire(state, request)

    assert result.state.marking.tokens_at("draft") == ()
    assert result.state.marking.tokens_at("review") == (token,)
    # Fired event records the fired transition and its static arc endpoints.
    fired_event: PetriNetRuntimeEvent = result.events.events[0]
    assert isinstance(fired_event, PetriNetTransitionFiredEvent)
    assert fired_event.transition_id == "submit"
    assert fired_event.input_place_ids == ("draft",)
    assert fired_event.output_place_ids == ("review",)
    # PetriNetMarking event records the changed places in deterministic order.
    marking_event: PetriNetRuntimeEvent = result.events.events[1]
    assert isinstance(marking_event, PetriNetMarkingChangedEvent)
    assert marking_event.changed_place_ids == ("draft", "review")


def test__PetriNetExecutor__enabled_bindings__uses_guard() -> None:
    """Validate enabled bindings honor transition guards."""

    def guard(tokens: tuple[PetriNetToken, ...]) -> bool:
        """Accept only implementation-brief tokens."""
        # First token color is the guard input under assertion.
        first_token: PetriNetToken = tokens[0]
        return first_token.color["kind"] == "implementation-brief"

    # Workflow net fixture applies a guard to the submit transition.
    net: PetriNet = PetriNet(
        places=(PetriNetPlace("draft"), PetriNetPlace("review")),
        transitions=(PetriNetTransition("submit", guard=guard),),
        arcs=(
            PetriNetArc(place_id="draft", transition_id="submit", kind=PetriNetArcKind.INPUT),
            PetriNetArc(place_id="review", transition_id="submit", kind=PetriNetArcKind.OUTPUT),
        ),
    )
    # Matching token satisfies the transition guard.
    matching_token: PetriNetToken = PetriNetToken.from_color("artifact-1", {"kind": "implementation-brief"})
    # State contains the matching token at the input place.
    state: PetriNetState = PetriNetState(net=net, marking=PetriNetMarking.from_tokens({"draft": [matching_token]}))

    assert len(PetriNetExecutor().enabled_bindings(state)) == 1
