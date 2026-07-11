from __future__ import annotations

from pathlib import Path
import sys

import pytest

from projectkoios.cli.main import main
from projectkoios.workflow.fixtures import WorkflowQueueItem, WorkflowQueueStateFixture, WorkflowQueueStateFixtureLoader, WorkflowQueueStateReporter


def test__workflow_queue__prints_static_queue_state(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    """Validate the workflow queue command prints operator-readable queue state."""
    # CLI argv selects the new read-only workflow queue command.
    argv: list[str] = ["projectkoios", "workflow", "queue"]
    monkeypatch.setattr(sys, "argv", argv)

    main()

    # Captured output is the operator-facing queue surface under assertion.
    output: str = capsys.readouterr().out
    assert "workflow queue: bootstrap-harness.queue-state" in output
    assert "fixture: dev/workflow-nets/bootstrap-harness.queue-state.json" in output
    assert "mode: static-read-only-fixture" in output
    assert "not canonical workflow authority" in output
    assert "active:" in output
    assert "queued/proposed:" in output
    assert "1. pi-skill-determinism-slice-0 state=queued" in output
    assert "adr-template-schema-contract-successor-draft-slice-11 state=accepted-committed" in output
    assert "petrinet-workflow-queue-state-slice-4 state=proposed-next" not in output
    assert "completed/recent:" in output
    assert "petrinet-workflow-queue-state-slice-4 state=accepted-committed-pushed commit=5f209114" in output
    assert "petrinet-workflow-interactive-control-skill-slice-3 state=accepted-committed-pushed commit=b4de9c64" in output
    assert "vulcan-interactive-control-state-fix state=accepted-committed-pushed commit=ed9110b9" in output
    assert "superseded/rejected:" in output
    assert "slicing.20260711.120200_agent-skills-workflow-inspectability.md" in output
    assert "implementation-brief.20260711.120300_agent-skills-workflow-status-slice-0.md" in output
    assert "slicing.20260711.120900_agent-skills-workflow-project.md" in output
    assert "implementation-brief.20260711.121000_agent-skills-workflow-status-slice-0.md" in output
    assert "deferred:" in output
    assert "next decision needed:" in output
    assert "activate adr-schema-record-envelope-architecture-slice-14" in output


def test__WorkflowQueueStateFixtureLoader__loads_static_fixture() -> None:
    """Validate the queue-state fixture loader preserves known static queue facts."""
    # Loader maps the explicit static queue fixture into queue data objects.
    loader: WorkflowQueueStateFixtureLoader = WorkflowQueueStateFixtureLoader()
    # Fixture contains static queue state, not live reconstructed state.
    fixture: WorkflowQueueStateFixture = loader.load(PathLikeQueueFixture.default_path())

    assert fixture.queue_id == "bootstrap-harness.queue-state"
    assert fixture.surface == "projectkoios.workflow.queue_state"
    assert fixture.status == "static-read-only-fixture"
    assert fixture.active_item is None
    assert fixture.queued_items[0].name == "pi-skill-determinism-slice-0"
    assert fixture.queued_items[0].state == "queued"
    # Completed items are keyed by name so fixture queue order changes do not break this loader contract test.
    completed_items_by_name: dict[str, WorkflowQueueItem] = {item.name: item for item in fixture.completed_items}
    assert completed_items_by_name["adr-schema-base-architecture-extraction-planning-slice-13"].state == "accepted-committed-pending"
    assert completed_items_by_name["adr-schema-base-source-disposition-planning-slice-12"].state == "accepted-committed"
    assert completed_items_by_name["adr-template-schema-contract-successor-draft-slice-11"].state == "accepted-committed"
    assert completed_items_by_name["petrinet-workflow-queue-state-slice-4"].commit == "5f209114"
    assert completed_items_by_name["petrinet-workflow-interactive-control-skill-slice-3"].commit == "b4de9c64"
    assert completed_items_by_name["vulcan-interactive-control-state-fix"].commit == "ed9110b9"
    assert len(fixture.superseded_items) == 4
    assert fixture.deferred_items == ()


def test__WorkflowQueueStateReporter__renders_empty_sections_as_none() -> None:
    """Validate empty queue sections render explicitly as none."""
    # Synthetic fixture avoids coupling absence behavior to current live queue state.
    fixture: WorkflowQueueStateFixture = WorkflowQueueStateFixture(
        path=PathLikeQueueFixture.default_path(),
        queue_id="bootstrap-harness.queue-state",
        surface="projectkoios.workflow.queue_state",
        parent_effort="test",
        status="static-read-only-fixture",
        authority="Static read-only fixture; not canonical workflow authority and not product authority.",
        active_item=None,
        queued_items=(),
        completed_items=(),
        superseded_items=(),
        deferred_items=(),
        next_decision_needed="None.",
    )

    # Rendered text must make absent sections explicit for operators.
    output: str = WorkflowQueueStateReporter().render(fixture)

    assert "active:\n  none" in output
    assert "queued/proposed:\n  none" in output
    assert "deferred:\n  none" in output
    assert "WARNING: queue active_item is set" not in output


class PathLikeQueueFixture:
    """Test helper exposing the default queue-state fixture path."""

    @classmethod
    def default_path(cls) -> Path:
        """Return the default static queue-state fixture path.

        Returns:
            Fixture path object accepted by the loader.
        """
        return Path("dev/workflow-nets/bootstrap-harness.queue-state.json")
