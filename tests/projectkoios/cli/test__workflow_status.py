from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
import sys

import pytest

from projectkoios.cli.main import main
from projectkoios.cli.workflow import (
    WorkflowQueueItem,
    WorkflowQueueStateFixture,
    WorkflowQueueStateReporter,
    WorkflowStatusFixture,
    WorkflowStatusFixtureLoader,
    WorkflowStatusReporter,
)
from projectkoios.workflow import PetriNetExecutor, PetriNetState, PetriNetTransitionBinding


def test__workflow_status__prints_static_fixture_status(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    """Validate the workflow status command prints operator-readable fixture status."""
    # CLI argv selects the new read-only workflow status command.
    argv: list[str] = ["projectkoios", "workflow", "status"]
    monkeypatch.setattr(sys, "argv", argv)

    main()

    # Captured output is the operator-facing status surface under assertion.
    output: str = capsys.readouterr().out
    assert "workflow: bootstrap-harness.slice-0" in output
    assert "fixture: dev/workflow-nets/bootstrap-harness.workflow-net.json" in output
    assert "what" not in output.lower()
    assert "places:" in output
    assert "- intake: Intake" in output
    assert "- user_decision: User decision" in output
    assert "- implementation: Implementation" in output
    assert "tokens:" in output
    assert "current-slice at user_decision" in output
    assert "requires_user_decision=true" in output
    assert "active_slice=none" in output
    assert "petrinet-workflow-current-slice-status-reconciliation-slice-2" not in output
    assert "live-petri-net-skeleton-slice-0" not in output
    assert "enabled transitions:" in output
    assert "- approve_next_slice: Approve next slice" in output
    assert "complete_implementation" not in output
    assert "user decision required: yes" in output
    assert "queue control surface:" in output
    assert "workflow queue: bootstrap-harness.queue-state" in output
    assert "queued/proposed:" in output
    assert "next decision needed:" in output
    assert "WARNING: queue active_item is set" not in output


def test__WorkflowStatusReporter__renders_queue_active_item_warning() -> None:
    """Validate queue overlay warns when an active item blocks queued activation."""
    # Active item simulates queue state that should block queued advancement.
    active_item: WorkflowQueueItem = WorkflowQueueItem(
        name="active-workflow-item",
        state="active",
        artifact_refs=("docs/plans/active.md",),
    )
    # Queued item demonstrates that warning must appear before recommending activation.
    queued_item: WorkflowQueueItem = WorkflowQueueItem(
        name="queued-workflow-item",
        state="queued",
        artifact_refs=("docs/plans/queued.md",),
    )
    # Queue fixture is synthetic read-only state for reporter behavior.
    queue_fixture: WorkflowQueueStateFixture = WorkflowQueueStateFixture(
        path=Path("dev/workflow-nets/bootstrap-harness.queue-state.json"),
        queue_id="bootstrap-harness.queue-state",
        surface="projectkoios.workflow.queue_state",
        parent_effort="test",
        status="static-read-only-fixture",
        authority="Static read-only fixture; not canonical workflow authority and not product authority.",
        active_item=active_item,
        queued_items=(queued_item,),
        completed_items=(),
        superseded_items=(),
        deferred_items=(),
        next_decision_needed="Clear active item before queued activation.",
    )

    # Queue reporter output is the status overlay warning source.
    output: str = WorkflowQueueStateReporter().render(queue_fixture)

    assert "active-workflow-item state=active" in output
    assert "queued-workflow-item state=queued" in output
    assert "WARNING: queue active_item is set" in output
    assert "do not recommend or activate queued items" in output


def test__WorkflowStatusReporter__uses_executor_enabled_bindings(monkeypatch: pytest.MonkeyPatch) -> None:
    """Validate enabled transitions come from PetriNetExecutor.enabled_bindings."""
    # Loader maps the static fixture into existing Petri-net runtime objects.
    loader: WorkflowStatusFixtureLoader = WorkflowStatusFixtureLoader()
    # Fixture contains one real token at the user-decision place.
    fixture: WorkflowStatusFixture = loader.load(Path("dev/workflow-nets/bootstrap-harness.workflow-net.json"))
    # Spy state tracks whether the runtime enabled-bindings method was invoked.
    spy_state: dict[str, bool] = {"called": False}
    # Original method keeps the test tied to real runtime enabledness semantics.
    original_enabled_bindings: Callable[[PetriNetExecutor, PetriNetState], tuple[PetriNetTransitionBinding, ...]] = PetriNetExecutor.enabled_bindings

    def spy_enabled_bindings(self: PetriNetExecutor, state: PetriNetState) -> tuple[PetriNetTransitionBinding, ...]:
        """Record runtime invocation and delegate to the original implementation."""
        spy_state["called"] = True
        return original_enabled_bindings(self, state)

    monkeypatch.setattr(PetriNetExecutor, "enabled_bindings", spy_enabled_bindings)

    # Reporter must call the executor instead of printing hard-coded enabled transitions.
    output: str = WorkflowStatusReporter().render(fixture)

    assert spy_state["called"] is True
    assert "- approve_next_slice: Approve next slice" in output
    assert "complete_implementation" not in output
