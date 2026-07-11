from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
import sys

import pytest

from projectkoios.cli.main import main
from projectkoios.cli.workflow import WorkflowStatusFixture, WorkflowStatusFixtureLoader, WorkflowStatusReporter
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
    assert "active_slice=petrinet-workflow-current-slice-status-reconciliation-slice-2" in output
    assert "live-petri-net-skeleton-slice-0" not in output
    assert "enabled transitions:" in output
    assert "- approve_next_slice: Approve next slice" in output
    assert "complete_implementation" not in output
    assert "user decision required: yes" in output


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
