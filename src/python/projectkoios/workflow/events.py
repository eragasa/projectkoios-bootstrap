from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class Event:
    """Structured workflow runtime event."""

    event_type: str
    transition_id: str | None = None
    details: dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(frozen=True, slots=True)
class ExecutionTrace:
    """Ordered workflow event trace."""

    events: tuple[Event, ...] = ()

    def append(self, event: Event) -> ExecutionTrace:
        """Return a new trace with an event appended.

        Args:
            event: Event to append.

        Returns:
            New immutable execution trace.
        """

        return ExecutionTrace(events=(*self.events, event))


@dataclass(frozen=True, slots=True)
class EventLog:
    """Serializable workflow event log for inspection."""

    trace: ExecutionTrace

    def to_dict(self) -> dict[str, list[dict[str, str | dict[str, str] | None]]]:
        """Return a deterministic dictionary representation of the event log."""

        # Serialized events preserve trace order for deterministic debugging output.
        serialized_events: list[dict[str, str | dict[str, str] | None]] = []
        event: Event
        for event in self.trace.events:
            serialized_events.append(
                {
                    "event_type": event.event_type,
                    "transition_id": event.transition_id,
                    "details": dict(sorted(event.details.items())),
                    "created_at": event.created_at,
                }
            )
        return {"events": serialized_events}
