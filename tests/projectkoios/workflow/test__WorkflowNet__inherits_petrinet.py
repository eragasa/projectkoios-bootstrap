from __future__ import annotations

from projectkoios.workflow import PetriNetArc, PetriNetArcKind, PetriNet, PetriNetPlace, PetriNetTransition, WorkflowNet


def test__WorkflowNet__inherits_petrinet__reuses_core_behavior() -> None:
    """Validate WorkflowNet inherits reusable PetriNet behavior."""
    # Workflow net fixture uses the workflow-specific subclass boundary.
    net: WorkflowNet = WorkflowNet(
        places=(PetriNetPlace("draft"), PetriNetPlace("review")),
        transitions=(PetriNetTransition("submit"),),
        arcs=(PetriNetArc(place_id="draft", transition_id="submit", kind=PetriNetArcKind.INPUT),),
    )

    assert isinstance(net, PetriNet)
    assert net.place_ids() == {"draft", "review"}
    assert net.transition_ids() == {"submit"}
    assert len(net.input_arcs("submit")) == 1
