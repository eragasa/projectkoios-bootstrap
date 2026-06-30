from __future__ import annotations

import asyncio

from projectkoios.bootstrap.harness.daemon.scheduler import (
    SchedulerState,
    run_with_coalesce,
)


def test__SchedulerState__no_overlap_fires_immediately() -> None:
    """When no update is in flight, events fire the update immediately."""
    state = SchedulerState()
    fired: list[list[int]] = []

    async def do_update(events: list[int]) -> None:
        fired.append(events)

    asyncio.run(run_with_coalesce([1, 2], state, do_update))
    assert len(fired) == 1
    assert fired[0] == [1, 2]
    assert not state.update_in_flight
    assert not state.follow_up_scheduled


def test__SchedulerState__in_flight_schedules_one_follow_up() -> None:
    """When an update is running, new events schedule exactly one follow-up."""
    state = SchedulerState()
    update_done = asyncio.Event()
    fired: list[list[int]] = []

    async def do_update(events: list[int]) -> None:
        fired.append(events)
        if len(fired) == 1:
            update_done.set()

    async def _run() -> None:
        task1 = asyncio.create_task(run_with_coalesce([1], state, do_update))
        await asyncio.sleep(0.01)
        task2 = asyncio.create_task(run_with_coalesce([2, 3], state, do_update))
        await task1
        await task2

    asyncio.run(asyncio.wait_for(_run(), timeout=5.0))
    assert len(fired) == 2
    assert fired[0] == [1]
    assert fired[1] == [2, 3]


def test__SchedulerState__multiple_events_during_flight_coalesce() -> None:
    """Multiple event batches during flight coalesce into one follow-up."""
    state = SchedulerState()
    gate = asyncio.Event()
    fired: list[list[int]] = []

    async def do_update(events: list[int]) -> None:
        fired.append(events)
        if len(fired) == 1:
            await gate.wait()

    async def _run() -> None:
        task1 = asyncio.create_task(run_with_coalesce([1], state, do_update))
        await asyncio.sleep(0.01)
        task2 = asyncio.create_task(run_with_coalesce([2], state, do_update))
        await asyncio.sleep(0.01)
        task3 = asyncio.create_task(run_with_coalesce([3, 4], state, do_update))
        gate.set()
        await task1
        await task2
        await task3

    asyncio.run(asyncio.wait_for(_run(), timeout=5.0))
    assert len(fired) == 2
    assert fired[0] == [1]
    assert fired[1] == [2, 3, 4]


def test__SchedulerState__no_follow_up_when_no_pending() -> None:
    """No follow-up is scheduled when no events arrive during flight."""
    state = SchedulerState()
    fired: list[list[int]] = []

    async def do_update(events: list[int]) -> None:
        fired.append(events)

    asyncio.run(run_with_coalesce([1], state, do_update))
    assert len(fired) == 1
    assert not state.follow_up_scheduled
