from __future__ import annotations

from types import ModuleType

import pytest

from projectkoios.workflow import (
    AdapterExport,
    AdapterUnavailableError,
    Arc,
    ArcKind,
    Place,
    Pm4pyProcessMiningAdapter,
    SnakesColoredNetAdapter,
    Transition,
    WorkflowNet,
    WorkflowNetPayload,
    WorkflowNetPayloadBuilder,
)


def workflow_fixture() -> WorkflowNet:
    """Create a minimal workflow net fixture for adapter tests."""
    return WorkflowNet(
        places=(Place("draft", "Draft"), Place("review", "Review")),
        transitions=(Transition("submit", "Submit"),),
        arcs=(
            Arc(place_id="draft", transition_id="submit", kind=ArcKind.INPUT),
            Arc(place_id="review", transition_id="submit", kind=ArcKind.OUTPUT),
        ),
    )


def test__WorkflowNetPayloadBuilder__build__returns_payload_data_object() -> None:
    """Validate the payload builder creates a workflow payload data object."""
    # Net fixture is the canonical source being adapted.
    net: WorkflowNet = workflow_fixture()

    # Payload builder is the action object that converts nets to payload data.
    payload: WorkflowNetPayload = WorkflowNetPayloadBuilder().build(net)

    assert payload.to_dict()["places"] == [
        {"place_id": "draft", "label": "Draft"},
        {"place_id": "review", "label": "Review"},
    ]
    assert payload.to_dict()["arcs"] == [
        {"place_id": "draft", "transition_id": "submit", "kind": "input", "weight": 1},
        {"place_id": "review", "transition_id": "submit", "kind": "output", "weight": 1},
    ]


def test__SnakesColoredNetAdapter__export__returns_library_neutral_payload() -> None:
    """Validate SNAKES adapter export uses canonical payload data only."""
    # Net fixture is the canonical source being exported.
    net: WorkflowNet = workflow_fixture()

    # Export payload is library-neutral and does not require SNAKES installation.
    exported: AdapterExport = SnakesColoredNetAdapter().export(net)

    assert exported.adapter_name == "snakes"
    assert isinstance(exported.payload, WorkflowNetPayload)


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
