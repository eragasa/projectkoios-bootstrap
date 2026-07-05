from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from types import ModuleType

from projectkoios.workflow.model import Arc, Place, Transition, WorkflowNet


class AdapterUnavailableError(RuntimeError):
    """Raised when an optional workflow adapter dependency is unavailable."""


@dataclass(frozen=True, slots=True)
class WorkflowPlacePayload:
    """Data object for a place in an adapter-neutral workflow payload."""

    place_id: str
    label: str

    def to_dict(self) -> dict[str, str]:
        """Return a deterministic dictionary representation of the place payload."""

        return {"place_id": self.place_id, "label": self.label}


@dataclass(frozen=True, slots=True)
class WorkflowTransitionPayload:
    """Data object for a transition in an adapter-neutral workflow payload."""

    transition_id: str
    label: str

    def to_dict(self) -> dict[str, str]:
        """Return a deterministic dictionary representation of the transition payload."""

        return {"transition_id": self.transition_id, "label": self.label}


@dataclass(frozen=True, slots=True)
class WorkflowArcPayload:
    """Data object for an arc in an adapter-neutral workflow payload."""

    place_id: str
    transition_id: str
    kind: str
    weight: int

    def to_dict(self) -> dict[str, str | int]:
        """Return a deterministic dictionary representation of the arc payload."""

        return {
            "place_id": self.place_id,
            "transition_id": self.transition_id,
            "kind": self.kind,
            "weight": self.weight,
        }


@dataclass(frozen=True, slots=True)
class WorkflowNetPayload:
    """Data object for a deterministic library-neutral workflow net payload."""

    places: tuple[WorkflowPlacePayload, ...]
    transitions: tuple[WorkflowTransitionPayload, ...]
    arcs: tuple[WorkflowArcPayload, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a deterministic dictionary representation of the workflow payload."""

        return {
            "places": [place.to_dict() for place in self.places],
            "transitions": [transition.to_dict() for transition in self.transitions],
            "arcs": [arc.to_dict() for arc in self.arcs],
        }


@dataclass(frozen=True, slots=True)
class AdapterExport:
    """Adapter export payload for third-party Petri-net integrations.

    Args:
        adapter_name: Stable adapter identifier.
        net: Canonical workflow net being exported.
        payload: Deterministic library-neutral export payload data object.
    """

    adapter_name: str
    net: WorkflowNet
    payload: WorkflowNetPayload


@dataclass(frozen=True, slots=True)
class WorkflowNetPayloadBuilder:
    """Action object that builds adapter-neutral payload data objects."""

    def build(self, net: WorkflowNet) -> WorkflowNetPayload:
        """Build a deterministic library-neutral payload for a workflow net.

        Args:
            net: Canonical workflow net to serialize for adapter handoff.

        Returns:
            Workflow payload data object containing places, transitions, and arcs.
        """

        # Places preserve declaration order for deterministic adapter exports.
        places: list[WorkflowPlacePayload] = []
        place: Place
        for place in net.places:
            places.append(WorkflowPlacePayload(place_id=place.place_id, label=place.label))

        # Transitions preserve declaration order and omit non-serializable guard callables.
        transitions: list[WorkflowTransitionPayload] = []
        transition: Transition
        for transition in net.transitions:
            transitions.append(
                WorkflowTransitionPayload(transition_id=transition.transition_id, label=transition.label)
            )

        # Arcs preserve declaration order and expose explicit direction and weight.
        arcs: list[WorkflowArcPayload] = []
        arc: Arc
        for arc in net.arcs:
            arcs.append(
                WorkflowArcPayload(
                    place_id=arc.place_id,
                    transition_id=arc.transition_id,
                    kind=arc.kind.value,
                    weight=arc.weight,
                )
            )

        return WorkflowNetPayload(places=tuple(places), transitions=tuple(transitions), arcs=tuple(arcs))


@dataclass(frozen=True, slots=True)
class SnakesColoredNetAdapter:
    """Adapter boundary for future SNAKES colored-net integration.

    The core workflow package uses canonical `WorkflowNet` objects. This adapter
    owns the optional SNAKES dependency boundary and loads it lazily only when a
    caller explicitly requests backend access.
    """

    module_name: str = "snakes"
    payload_builder: WorkflowNetPayloadBuilder = WorkflowNetPayloadBuilder()

    def export(self, net: WorkflowNet) -> AdapterExport:
        """Return a typed adapter export payload.

        Args:
            net: Canonical workflow net to export.

        Returns:
            Adapter export payload.
        """

        return AdapterExport(adapter_name="snakes", net=net, payload=self.payload_builder.build(net))

    def backend_module(self) -> ModuleType:
        """Load and return the optional SNAKES backend module.

        Returns:
            Imported SNAKES module.

        Raises:
            AdapterUnavailableError: When SNAKES is not installed.
        """

        try:
            # Backend module is imported lazily so core workflow imports stay dependency-free.
            module: ModuleType = import_module(self.module_name)
        except ModuleNotFoundError:
            raise AdapterUnavailableError("optional workflow adapter dependency is unavailable: snakes") from None
        return module


@dataclass(frozen=True, slots=True)
class Pm4pyProcessMiningAdapter:
    """Adapter boundary for future PM4Py process-mining integration.

    The core workflow package uses canonical `WorkflowNet` objects. This adapter
    owns the optional PM4Py dependency boundary and loads it lazily only when a
    caller explicitly requests backend access.
    """

    module_name: str = "pm4py"
    payload_builder: WorkflowNetPayloadBuilder = WorkflowNetPayloadBuilder()

    def export(self, net: WorkflowNet) -> AdapterExport:
        """Return a typed adapter export payload.

        Args:
            net: Canonical workflow net to export.

        Returns:
            Adapter export payload.
        """

        return AdapterExport(adapter_name="pm4py", net=net, payload=self.payload_builder.build(net))

    def backend_module(self) -> ModuleType:
        """Load and return the optional PM4Py backend module.

        Returns:
            Imported PM4Py module.

        Raises:
            AdapterUnavailableError: When PM4Py is not installed.
        """

        try:
            # Backend module is imported lazily so core workflow imports stay dependency-free.
            module: ModuleType = import_module(self.module_name)
        except ModuleNotFoundError:
            raise AdapterUnavailableError("optional workflow adapter dependency is unavailable: pm4py") from None
        return module
