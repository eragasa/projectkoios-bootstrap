"""Debounce and coalesce scheduler for daemon update requests.

Turns bursts of filesystem events into a single update request and schedules
exactly one follow-up update when changes arrive while an update is already
running. No overlapping refreshes.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Awaitable, Callable, TypeVar

E = TypeVar("E")


@dataclass
class SchedulerState:
    """Mutable scheduler state tracking in-flight and pending updates."""

    update_in_flight: bool = False
    follow_up_scheduled: bool = False
    pending_events: list = field(default_factory=list)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)


async def run_with_coalesce(
    events: list[E],
    state: SchedulerState,
    do_update: Callable[[list[E]], Awaitable[None]],
) -> None:
    """Coalesce *events* into a single update, scheduling one follow-up.

    If no update is in flight, fires ``do_update`` immediately with the
    accumulated events. If an update is already running, accumulates events
    into exactly one follow-up (further events merge into the same follow-up).
    The follow-up fires after the current update completes.
    """
    async with state._lock:
        state.pending_events.extend(events)
        if state.update_in_flight:
            state.follow_up_scheduled = True
            return
        state.update_in_flight = True
        batch, state.pending_events = state.pending_events, []

    try:
        await do_update(batch)
    finally:
        async with state._lock:
            state.update_in_flight = False
            needs_follow_up = state.follow_up_scheduled
            follow_up_batch, state.pending_events = state.pending_events, []
            state.follow_up_scheduled = False

    if needs_follow_up:
        await run_with_coalesce(follow_up_batch, state, do_update)
