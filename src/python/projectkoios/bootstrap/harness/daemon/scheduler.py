"""Debounce and coalesce scheduler for daemon update requests."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Generic, TypeVar

E = TypeVar("E")


@dataclass
class SchedulerState(Generic[E]):
    """Mutable scheduler state tracking in-flight and pending updates."""

    update_in_flight: bool = False
    follow_up_scheduled: bool = False
    pending_events: list[E] = field(default_factory=list)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


async def run_with_coalesce(
    events: list[E],
    state: SchedulerState[E],
    do_update: Callable[[list[E]], Awaitable[None]],
) -> None:
    """Coalesce *events* into a single update, scheduling one follow-up."""
    async with state.lock:
        state.pending_events.extend(events)
        if state.update_in_flight:
            state.follow_up_scheduled = True
            return
        state.update_in_flight = True
        batch: list[E] = list(state.pending_events)
        state.pending_events.clear()

    try:
        await do_update(batch)
    finally:
        async with state.lock:
            state.update_in_flight = False
            needs_follow_up: bool = state.follow_up_scheduled
            follow_up_batch: list[E] = list(state.pending_events)
            state.pending_events.clear()
            state.follow_up_scheduled = False

    if needs_follow_up:
        await run_with_coalesce(follow_up_batch, state, do_update)
