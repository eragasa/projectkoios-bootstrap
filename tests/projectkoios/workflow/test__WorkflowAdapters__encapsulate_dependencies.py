from __future__ import annotations

from types import ModuleType

import pytest

from projectkoios.workflow import (
    AdapterExport,
    AdapterUnavailableError,
    PetriNetArc,
    PetriNetArcKind,
    PetriNetPlace,
    Pm4pyProcessMiningAdapter,
    SnakesColoredNetAdapter,
    PetriNetTransition,
    PetriNet,
    PetriNetPayload,
    PetriNetPayloadBuilder,
)


def workflow_fixture() -> PetriNet:
    """Create a minimal workflow net fixture for adapter tests."""
    return PetriNet(
        places=(PetriNetPlace("draft", "Draft"), PetriNetPlace("review", "Review")),
        transitions=(PetriNetTransition("submit", "Submit"),),
        arcs=(
            PetriNetArc(place_id="draft", transition_id="submit", kind=PetriNetArcKind.INPUT),
            PetriNetArc(place_id="review", transition_id="submit", kind=PetriNetArcKind.OUTPUT),
        ),
    )


def test__PetriNetPayloadBuilder__build__returns_payload_data_object() -> None:
    """Validate the payload builder creates a stable workflow payload data object."""
    # Net fixture is the canonical source being adapted.
    net: PetriNet = workflow_fixture()

    # Payload builder is the action object that converts nets to payload data.
    payload: PetriNetPayload = PetriNetPayloadBuilder().build(net)

    assert payload.to_dict() == {
        "places": [
            {"place_id": "draft", "label": "Draft"},
            {"place_id": "review", "label": "Review"},
        ],
        "transitions": [{"transition_id": "submit", "label": "Submit"}],
        "arcs": [
            {"place_id": "draft", "transition_id": "submit", "kind": "input", "weight": 1},
            {"place_id": "review", "transition_id": "submit", "kind": "output", "weight": 1},
        ],
    }


def test__PetriNetPayloadBuilder__build__preserves_topology_weight_without_backend() -> None:
    """Validate always-on topology payloads preserve arc weights without backends."""
    # Weighted net fixture proves topology equivalence does not require optional libraries.
    net: PetriNet = PetriNet(
        places=(PetriNetPlace("draft", "Draft"), PetriNetPlace("review", "Review")),
        transitions=(PetriNetTransition("submit", "Submit"),),
        arcs=(
            PetriNetArc(place_id="draft", transition_id="submit", kind=PetriNetArcKind.INPUT, weight=2),
            PetriNetArc(place_id="review", transition_id="submit", kind=PetriNetArcKind.OUTPUT, weight=1),
        ),
    )

    # Payload builder records arc endpoints, direction, and weight deterministically.
    payload: PetriNetPayload = PetriNetPayloadBuilder().build(net)

    assert payload.to_dict()["arcs"] == [
        {"place_id": "draft", "transition_id": "submit", "kind": "input", "weight": 2},
        {"place_id": "review", "transition_id": "submit", "kind": "output", "weight": 1},
    ]


def test__PetriNetPayloadBuilder__build__omits_non_serializable_guard() -> None:
    """Validate payload serialization excludes backend-unsafe guard callables."""

    def guard(tokens: tuple[object, ...]) -> bool:
        """Guard callable that must not leak into adapter payloads."""
        return bool(tokens)

    # Net fixture includes a guard that cannot be serialized into adapter payload data.
    net: PetriNet = PetriNet(
        places=(PetriNetPlace("draft", "Draft"),),
        transitions=(PetriNetTransition("submit", "Submit", guard=guard),),
        arcs=(),
    )

    # Payload builder preserves accepted Petri-net vocabulary and omits callables.
    payload: PetriNetPayload = PetriNetPayloadBuilder().build(net)

    assert payload.to_dict()["transitions"] == [{"transition_id": "submit", "label": "Submit"}]


def test__WorkflowAdapters__export__returns_library_neutral_payload_without_backend_import(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Validate adapter exports do not import optional backend dependencies."""

    def forbidden_import(name: str) -> ModuleType:
        """Fail if export crosses the lazy dependency boundary."""
        raise AssertionError(f"unexpected backend import: {name}")

    # Import hook fails the test if export tries to load SNAKES or PM4Py.
    monkeypatch.setattr("projectkoios.workflow.adapters.import_module", forbidden_import)
    # Net fixture is the canonical source being exported by both adapters.
    net: PetriNet = workflow_fixture()

    # SNAKES export is library-neutral and does not require optional installations.
    snakes_exported: AdapterExport = SnakesColoredNetAdapter().export(net)
    # PM4Py export is library-neutral and does not require optional installations.
    pm4py_exported: AdapterExport = Pm4pyProcessMiningAdapter().export(net)

    assert snakes_exported.adapter_name == "snakes"
    assert pm4py_exported.adapter_name == "pm4py"
    assert snakes_exported.payload.to_dict() == pm4py_exported.payload.to_dict()


def test__Pm4pyProcessMiningAdapter__backend_module__raises_clear_unavailable_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Validate PM4Py dependency loading is lazy and clearly reported."""

    def missing_import(name: str) -> ModuleType:
        """Simulate a missing optional backend dependency."""
        raise ModuleNotFoundError(name)

    # Import hook simulates an environment without PM4Py installed.
    monkeypatch.setattr("projectkoios.workflow.adapters.import_module", missing_import)

    with pytest.raises(AdapterUnavailableError, match="pm4py"):
        Pm4pyProcessMiningAdapter().backend_module()


def test__SnakesColoredNetAdapter__topology_round_trip__preserves_canonical_payload() -> None:
    """Validate SNAKES topology conversion round trips to canonical payload data."""
    pytest.importorskip("snakes.nets", reason="optional SNAKES backend unavailable")
    # Net fixture includes the topology fields required by ATHENA's adapter acceptance test.
    net: PetriNet = PetriNet(
        places=(PetriNetPlace("draft", "Draft"), PetriNetPlace("review", "Review")),
        transitions=(PetriNetTransition("submit", "Submit"),),
        arcs=(
            PetriNetArc(place_id="draft", transition_id="submit", kind=PetriNetArcKind.INPUT, weight=2),
            PetriNetArc(place_id="review", transition_id="submit", kind=PetriNetArcKind.OUTPUT, weight=1),
        ),
    )
    # Adapter under test owns the concrete SNAKES dependency boundary.
    adapter: SnakesColoredNetAdapter = SnakesColoredNetAdapter()

    # Backend net is a topology-only SNAKES representation, not runtime state.
    backend_net: object = adapter.export_backend_topology(net)
    # Round-tripped payload canonicalizes backend ordering and identity away.
    round_tripped_payload: PetriNetPayload = adapter.import_backend_topology_payload(backend_net)

    assert round_tripped_payload.to_dict() == PetriNetPayloadBuilder().build(net).to_dict()


def test__SnakesColoredNetAdapter__backend_module__raises_clear_unavailable_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Validate SNAKES dependency loading failure is clearly reported."""

    def missing_import(name: str) -> ModuleType:
        """Simulate a missing optional backend dependency."""
        raise ModuleNotFoundError(name)

    # Import hook simulates an environment without SNAKES installed.
    monkeypatch.setattr("projectkoios.workflow.adapters.import_module", missing_import)

    with pytest.raises(AdapterUnavailableError, match="snakes"):
        SnakesColoredNetAdapter().backend_module()


def test__SnakesColoredNetAdapter__backend_module__loads_only_when_requested(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Validate SNAKES backend loading is isolated behind the adapter method."""
    # Fake backend module stands in for the optional SNAKES package.
    fake_module: ModuleType = ModuleType("snakes")

    def fake_import(name: str) -> ModuleType:
        """Return a fake backend module for the requested dependency."""
        assert name == "snakes"
        return fake_module

    # Import hook proves the adapter method owns dependency loading.
    monkeypatch.setattr("projectkoios.workflow.adapters.import_module", fake_import)

    assert SnakesColoredNetAdapter().backend_module() is fake_module
