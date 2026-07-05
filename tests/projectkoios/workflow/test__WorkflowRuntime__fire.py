from __future__ import annotations

from projectkoios.workflow import (
    Arc,
    ArcKind,
    ExecutionState,
    FiredTransition,
    Marking,
    Place,
    Token,
    Transition,
    WorkflowNet,
    WorkflowRuntime,
)


def test__WorkflowRuntime__fire__moves_token_and_records_event() -> None:
    """Validate firing an enabled transition moves a token and records trace."""
    # Workflow net fixture moves one token from draft to review.
    net: WorkflowNet = WorkflowNet(
        places=(Place("draft"), Place("review")),
        transitions=(Transition("submit"),),
        arcs=(
            Arc(place_id="draft", transition_id="submit", kind=ArcKind.INPUT),
            Arc(place_id="review", transition_id="submit", kind=ArcKind.OUTPUT),
        ),
    )
    # Token fixture represents the colored artifact being routed.
    token: Token = Token.from_color("artifact-1", {"kind": "implementation-brief"})
    # Initial state puts the token in the draft place.
    state: ExecutionState = ExecutionState(net=net, marking=Marking.from_tokens({"draft": [token]}))
    # Runtime owns enabledness checks and firing semantics.
    runtime: WorkflowRuntime = WorkflowRuntime()

    # Fired result contains the next marking and trace.
    result: FiredTransition = runtime.fire(state, "submit")

    assert result.state.marking.tokens_at("draft") == ()
    assert result.state.marking.tokens_at("review") == (token,)
    assert result.trace.events[0].event_type == "transition-fired"
    assert result.trace.events[0].transition_id == "submit"


def test__WorkflowRuntime__enabled_bindings__uses_guard() -> None:
    """Validate enabled bindings honor transition guards."""

    def guard(tokens: tuple[Token, ...]) -> bool:
        """Accept only implementation-brief tokens."""
        # First token color is the guard input under assertion.
        first_token: Token = tokens[0]
        return first_token.color["kind"] == "implementation-brief"

    # Workflow net fixture applies a guard to the submit transition.
    net: WorkflowNet = WorkflowNet(
        places=(Place("draft"), Place("review")),
        transitions=(Transition("submit", guard=guard),),
        arcs=(
            Arc(place_id="draft", transition_id="submit", kind=ArcKind.INPUT),
            Arc(place_id="review", transition_id="submit", kind=ArcKind.OUTPUT),
        ),
    )
    # Matching token satisfies the transition guard.
    matching_token: Token = Token.from_color("artifact-1", {"kind": "implementation-brief"})
    # State contains the matching token at the input place.
    state: ExecutionState = ExecutionState(net=net, marking=Marking.from_tokens({"draft": [matching_token]}))

    assert len(WorkflowRuntime().enabled_bindings(state)) == 1
