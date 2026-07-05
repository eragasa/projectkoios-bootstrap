from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TypeAlias


@dataclass(frozen=True, slots=True)
class PetriNetTransitionFiredEvent:
    """Event emitted when a Petri-net transition fires."""

    transition_id: str
    input_place_ids: tuple[str, ...]
    output_place_ids: tuple[str, ...]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, str | list[str]]:
        """Return a deterministic dictionary representation of the fired event."""

        return {
            "event_type": "petri-net-transition-fired",
            "transition_id": self.transition_id,
            "input_place_ids": list(self.input_place_ids),
            "output_place_ids": list(self.output_place_ids),
            "created_at": self.created_at,
        }


@dataclass(frozen=True, slots=True)
class PetriNetMarkingChangedEvent:
    """Event emitted when a Petri-net marking changes."""

    changed_place_ids: tuple[str, ...]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, str | list[str]]:
        """Return a deterministic dictionary representation of the marking event."""

        return {
            "event_type": "petri-net-marking-changed",
            "changed_place_ids": list(self.changed_place_ids),
            "created_at": self.created_at,
        }


PetriNetRuntimeEvent: TypeAlias = PetriNetTransitionFiredEvent | PetriNetMarkingChangedEvent
"""Runtime event emitted by a Petri-net executor."""


@dataclass(frozen=True, slots=True)
class PetriNetEventCollection:
    """In-process collection of Petri-net runtime events for debugging."""

    events: tuple[PetriNetRuntimeEvent, ...] = ()

    def append(self, event: PetriNetRuntimeEvent) -> PetriNetEventCollection:
        """Return a new event collection with an event appended.

        Args:
            event: Runtime event to append.

        Returns:
            New immutable event collection.
        """

        return PetriNetEventCollection(events=(*self.events, event))

    def extend(self, events: tuple[PetriNetRuntimeEvent, ...]) -> PetriNetEventCollection:
        """Return a new event collection with multiple events appended.

        Args:
            events: Runtime events to append.

        Returns:
            New immutable event collection.
        """

        return PetriNetEventCollection(events=(*self.events, *events))

    def to_dict(self) -> dict[str, list[dict[str, str | list[str]]]]:
        """Return a deterministic dictionary representation of the event collection."""

        # Serialized events preserve runtime event order for debugging assertions.
        serialized_events: list[dict[str, str | list[str]]] = []
        event: PetriNetRuntimeEvent
        for event in self.events:
            serialized_events.append(event.to_dict())
        return {"events": serialized_events}
