from __future__ import annotations

import asyncio

from projectkoios.bootstrap.harness.daemon.scheduler import (
    SchedulerState,
    run_with_coalesce,
)


def test__SchedulerState__no_overlap_fires_immediately() -> None:
    """Validate events fire immediately when no update is in flight."""
    # State tracks update-in-flight and follow-up scheduling flags.
    state: SchedulerState[int] = SchedulerState()
    # Fired records event batches passed to the update callback.
    fired: list[list[int]] = []

    async def do_update(events: list[int]) -> None:
        """Record one update callback invocation."""
        fired.append(events)

    asyncio.run(run_with_coalesce([1, 2], state, do_update))
    assert len(fired) == 1
    assert fired[0] == [1, 2]
    assert not state.update_in_flight
    assert not state.follow_up_scheduled


def test__SchedulerState__in_flight_schedules_one_follow_up() -> None:
    """Validate in-flight updates schedule exactly one follow-up."""
    # State tracks update-in-flight and follow-up scheduling flags.
    state: SchedulerState[int] = SchedulerState()
    # Update-done signals when the first update callback has run.
    update_done: asyncio.Event = asyncio.Event()
    # Fired records event batches passed to the update callback.
    fired: list[list[int]] = []

    async def do_update(events: list[int]) -> None:
        """Record update callback invocations and signal first completion."""
        fired.append(events)
        if len(fired) == 1:
            update_done.set()

    async def run_tasks() -> None:
        """Run overlapping scheduler calls to trigger a follow-up update."""
        # First task starts the initial in-flight update.
        task1: asyncio.Task[None] = asyncio.create_task(run_with_coalesce([1], state, do_update))
        await asyncio.sleep(0.01)
        # Second task submits events while the first update is in flight.
        task2: asyncio.Task[None] = asyncio.create_task(run_with_coalesce([2, 3], state, do_update))
        await task1
        await task2

    asyncio.run(asyncio.wait_for(run_tasks(), timeout=5.0))
    assert len(fired) == 2
    assert fired[0] == [1]
    assert fired[1] == [2, 3]


def test__SchedulerState__multiple_events_during_flight_coalesce() -> None:
    """Validate multiple in-flight event batches coalesce into one follow-up."""
    # State tracks update-in-flight and follow-up scheduling flags.
    state: SchedulerState[int] = SchedulerState()
    # Gate blocks the first callback so later events arrive during flight.
    gate: asyncio.Event = asyncio.Event()
    # Fired records event batches passed to the update callback.
    fired: list[list[int]] = []

    async def do_update(events: list[int]) -> None:
        """Record callback invocations and hold the first update open."""
        fired.append(events)
        if len(fired) == 1:
            await gate.wait()

    async def run_tasks() -> None:
        """Run multiple overlapping scheduler calls."""
        # First task starts the initial in-flight update.
        task1: asyncio.Task[None] = asyncio.create_task(run_with_coalesce([1], state, do_update))
        await asyncio.sleep(0.01)
        # Second task contributes pending follow-up events.
        task2: asyncio.Task[None] = asyncio.create_task(run_with_coalesce([2], state, do_update))
        await asyncio.sleep(0.01)
        # Third task contributes additional events to the same follow-up.
        task3: asyncio.Task[None] = asyncio.create_task(run_with_coalesce([3, 4], state, do_update))
        gate.set()
        await task1
        await task2
        await task3

    asyncio.run(asyncio.wait_for(run_tasks(), timeout=5.0))
    assert len(fired) == 2
    assert fired[0] == [1]
    assert fired[1] == [2, 3, 4]


def test__SchedulerState__no_follow_up_when_no_pending() -> None:
    """Validate no follow-up is scheduled when no pending events arrive."""
    # State tracks update-in-flight and follow-up scheduling flags.
    state: SchedulerState[int] = SchedulerState()
    # Fired records event batches passed to the update callback.
    fired: list[list[int]] = []

    async def do_update(events: list[int]) -> None:
        """Record one update callback invocation."""
        fired.append(events)

    asyncio.run(run_with_coalesce([1], state, do_update))
    assert len(fired) == 1
    assert not state.follow_up_scheduled
