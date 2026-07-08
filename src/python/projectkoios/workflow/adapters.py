from __future__ import annotations

from collections.abc import Callable, Iterable, Sized
from dataclasses import dataclass
from importlib import import_module
from types import ModuleType

from projectkoios.workflow.petrinet import PetriNetArc, PetriNetPlace, PetriNetTransition, PetriNet


ObjectFactory = Callable[..., object]
"""Dynamic backend object factory type used inside lazy adapter conversions."""


class AdapterUnavailableError(RuntimeError):
    """Raised when an optional workflow adapter dependency is unavailable."""


@dataclass(frozen=True, slots=True)
class PetriNetPlacePayload:
    """Data object for a place in an adapter-neutral workflow payload."""

    place_id: str
    label: str

    def to_dict(self) -> dict[str, str]:
        """Return a deterministic dictionary representation of the place payload."""

        return {"place_id": self.place_id, "label": self.label}


@dataclass(frozen=True, slots=True)
class PetriNetTransitionPayload:
    """Data object for a transition in an adapter-neutral workflow payload."""

    transition_id: str
    label: str

    def to_dict(self) -> dict[str, str]:
        """Return a deterministic dictionary representation of the transition payload."""

        return {"transition_id": self.transition_id, "label": self.label}


@dataclass(frozen=True, slots=True)
class PetriNetArcPayload:
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
class PetriNetPayload:
    """Data object for a deterministic library-neutral workflow net payload."""

    places: tuple[PetriNetPlacePayload, ...]
    transitions: tuple[PetriNetTransitionPayload, ...]
    arcs: tuple[PetriNetArcPayload, ...]

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
    net: PetriNet
    payload: PetriNetPayload


@dataclass(frozen=True, slots=True)
class PetriNetPayloadBuilder:
    """Action object that builds adapter-neutral payload data objects."""

    def build(self, net: PetriNet) -> PetriNetPayload:
        """Build a deterministic library-neutral payload for a workflow net.

        Args:
            net: Canonical workflow net to serialize for adapter handoff.

        Returns:
            Workflow payload data object containing places, transitions, and arcs.
        """

        # PetriNetPlaces preserve declaration order for deterministic adapter exports.
        places: list[PetriNetPlacePayload] = []
        place: PetriNetPlace
        for place in net.places:
            places.append(PetriNetPlacePayload(place_id=place.place_id, label=place.label))

        # PetriNetTransitions preserve declaration order and omit non-serializable guard callables.
        transitions: list[PetriNetTransitionPayload] = []
        transition: PetriNetTransition
        for transition in net.transitions:
            transitions.append(
                PetriNetTransitionPayload(transition_id=transition.transition_id, label=transition.label)
            )

        # PetriNetArcs preserve declaration order and expose explicit direction and weight.
        arcs: list[PetriNetArcPayload] = []
        arc: PetriNetArc
        for arc in net.arcs:
            arcs.append(
                PetriNetArcPayload(
                    place_id=arc.place_id,
                    transition_id=arc.transition_id,
                    kind=arc.kind.value,
                    weight=arc.weight,
                )
            )

        return PetriNetPayload(places=tuple(places), transitions=tuple(transitions), arcs=tuple(arcs))


@dataclass(frozen=True, slots=True)
class SnakesColoredNetAdapter:
    """Adapter boundary for future SNAKES colored-net integration.

    The core workflow package uses canonical `PetriNet` objects. This adapter
    owns the optional SNAKES dependency boundary and loads it lazily only when a
    caller explicitly requests backend access.
    """

    module_name: str = "snakes"
    payload_builder: PetriNetPayloadBuilder = PetriNetPayloadBuilder()

    def export(self, net: PetriNet) -> AdapterExport:
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

    def export_backend_topology(self, net: PetriNet) -> object:
        """Build a SNAKES backend topology object from a canonical Petri net.

        Args:
            net: Canonical Petri net whose topology should be converted.

        Returns:
            SNAKES PetriNet backend object.
        """

        # SNAKES net classes are imported lazily to keep core workflow imports dependency-free.
        snakes_nets: ModuleType = self.snakes_nets_module()
        # Dynamic backend net factory creates the concrete SNAKES PetriNet.
        backend_net_factory: ObjectFactory = snakes_nets.PetriNet
        # Dynamic place factory creates SNAKES places without a module-level import.
        place_factory: ObjectFactory = snakes_nets.Place
        # Dynamic transition factory creates SNAKES transitions without a module-level import.
        transition_factory: ObjectFactory = snakes_nets.Transition
        # Dynamic value factory creates topology-only arc annotations.
        value_factory: ObjectFactory = snakes_nets.Value
        # Dynamic multi-arc factory preserves weighted topology arcs.
        multi_arc_factory: ObjectFactory = snakes_nets.MultiArc
        # Backend net accumulates the converted topology.
        backend_net: object = backend_net_factory("projectkoios-workflow")

        place: PetriNetPlace
        for place in net.places:
            # Backend place carries canonical label metadata for topology round trips.
            backend_place: object = place_factory(place.place_id)
            setattr(backend_place, "label", place.label)
            getattr(backend_net, "add_place")(backend_place)

        transition: PetriNetTransition
        for transition in net.transitions:
            # Backend transition label preserves canonical transition label metadata.
            backend_transition: object = transition_factory(transition.transition_id)
            setattr(backend_transition, "label", transition.label)
            getattr(backend_net, "add_transition")(backend_transition)

        arc: PetriNetArc
        for arc in net.arcs:
            # SNAKES arc annotations model topology-only multiplicity for round-trip comparison.
            arc_annotation: object = self.snakes_arc_annotation(arc.weight, value_factory, multi_arc_factory)
            if arc.kind.value == "input":
                getattr(backend_net, "add_input")(arc.place_id, arc.transition_id, arc_annotation)
            else:
                getattr(backend_net, "add_output")(arc.place_id, arc.transition_id, arc_annotation)

        return backend_net

    def import_backend_topology_payload(self, backend_net: object) -> PetriNetPayload:
        """Import a SNAKES backend topology object into a canonical payload.

        Args:
            backend_net: SNAKES PetriNet backend object to inspect.

        Returns:
            Deterministic canonical topology payload.
        """

        # Backend places are sorted so round trips do not depend on SNAKES set ordering.
        places: list[PetriNetPlacePayload] = []
        backend_place: object
        for backend_place in sorted(getattr(backend_net, "place")(), key=lambda item: getattr(item, "name")):
            places.append(
                PetriNetPlacePayload(
                    place_id=getattr(backend_place, "name"),
                    label=getattr(backend_place, "label", ""),
                )
            )

        # Backend transitions are sorted so round trips do not depend on SNAKES set ordering.
        transitions: list[PetriNetTransitionPayload] = []
        backend_transition: object
        for backend_transition in sorted(getattr(backend_net, "transition")(), key=lambda item: getattr(item, "name")):
            transitions.append(
                PetriNetTransitionPayload(
                    transition_id=getattr(backend_transition, "name"),
                    label=getattr(backend_transition, "label", ""),
                )
            )

        # Backend arcs are sorted after extraction for deterministic topology comparison.
        arcs: list[PetriNetArcPayload] = []
        for backend_transition in getattr(backend_net, "transition")():
            self.extend_snakes_arc_payloads(arcs, backend_transition, "input")
            self.extend_snakes_arc_payloads(arcs, backend_transition, "output")
        arcs.sort(key=lambda item: (item.transition_id, item.kind, item.place_id, item.weight))

        return PetriNetPayload(places=tuple(places), transitions=tuple(transitions), arcs=tuple(arcs))

    def snakes_nets_module(self) -> ModuleType:
        """Load and return the SNAKES nets module for topology conversion.

        Returns:
            Imported SNAKES nets module.

        Raises:
            AdapterUnavailableError: When SNAKES is not installed.
        """

        try:
            # Concrete topology conversion imports the backend nets module lazily.
            module: ModuleType = import_module(f"{self.module_name}.nets")
        except ModuleNotFoundError:
            raise AdapterUnavailableError("optional workflow adapter dependency is unavailable: snakes") from None
        return module

    def snakes_arc_annotation(
        self,
        weight: int,
        value_factory: ObjectFactory,
        multi_arc_factory: ObjectFactory,
    ) -> object:
        """Build a SNAKES arc annotation preserving topology-only weight.

        Args:
            weight: Petri-net arc weight to preserve.
            value_factory: Lazy SNAKES Value factory.
            multi_arc_factory: Lazy SNAKES MultiArc factory.

        Returns:
            SNAKES arc annotation object.
        """

        if weight <= 1:
            return value_factory("token")
        return multi_arc_factory(tuple(value_factory(f"token-{index}") for index in range(weight)))

    def extend_snakes_arc_payloads(
        self,
        arcs: list[PetriNetArcPayload],
        backend_transition: object,
        kind: str,
    ) -> None:
        """Append canonical arc payloads from SNAKES transition arcs.

        Args:
            arcs: Mutable canonical arc payload accumulator.
            backend_transition: SNAKES transition object to inspect.
            kind: Canonical arc kind to extract.
        """

        # SNAKES exposes input and output arc endpoints from transition objects.
        backend_arcs: Iterable[tuple[object, object]] = getattr(backend_transition, kind)()
        backend_arc: tuple[object, object]
        for backend_arc in backend_arcs:
            # Backend place is the arc endpoint to convert into canonical payload form.
            backend_place: object = backend_arc[0]
            # Backend annotation carries topology-only multiplicity.
            backend_annotation: object = backend_arc[1]
            arcs.append(
                PetriNetArcPayload(
                    place_id=getattr(backend_place, "name"),
                    transition_id=getattr(backend_transition, "name"),
                    kind=kind,
                    weight=self.snakes_arc_weight(backend_annotation),
                )
            )

    def snakes_arc_weight(self, backend_annotation: object) -> int:
        """Return topology-only weight from a SNAKES arc annotation.

        Args:
            backend_annotation: SNAKES arc annotation to inspect.

        Returns:
            Arc weight represented by the annotation.
        """

        if isinstance(backend_annotation, Sized):
            return len(backend_annotation)
        return 1


@dataclass(frozen=True, slots=True)
class Pm4pyProcessMiningAdapter:
    """Adapter boundary for future PM4Py process-mining integration.

    The core workflow package uses canonical `PetriNet` objects. This adapter
    owns the optional PM4Py dependency boundary and loads it lazily only when a
    caller explicitly requests backend access.
    """

    module_name: str = "pm4py"
    payload_builder: PetriNetPayloadBuilder = PetriNetPayloadBuilder()

    def export(self, net: PetriNet) -> AdapterExport:
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
