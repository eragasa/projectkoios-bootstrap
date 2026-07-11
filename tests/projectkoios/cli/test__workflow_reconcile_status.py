from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys

import pytest

from projectkoios.cli.main import main
from projectkoios.workflow.fixtures import WorkflowStatusReconciliationResult, WorkflowStatusReconciler


def test__workflow_reconcile_status__dry_run_prints_summary_without_writing(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    """Validate CLI dry-run reports reconciliation without writing fixtures."""
    # Status fixture text is captured to prove dry-run does not write it.
    status_path: Path = Path("dev/workflow-nets/bootstrap-harness.workflow-net.json")
    # Queue fixture text is captured to prove reconciliation never writes it.
    queue_path: Path = Path("dev/workflow-nets/bootstrap-harness.queue-state.json")
    # Original fixture bytes should be preserved by dry-run.
    status_before: str = status_path.read_text(encoding="utf-8")
    # Original queue bytes should be preserved by reconciliation.
    queue_before: str = queue_path.read_text(encoding="utf-8")
    # CLI argv selects the new reconcile-status dry-run command.
    argv: list[str] = ["projectkoios", "workflow", "reconcile-status", "--dry-run"]
    monkeypatch.setattr(sys, "argv", argv)

    main()

    # Captured output is the operator-facing reconciliation summary.
    output: str = capsys.readouterr().out
    assert "workflow reconcile-status: reconciled status fixture from queue fixture" in output
    assert "status fixture: dev/workflow-nets/bootstrap-harness.workflow-net.json" in output
    assert "queue fixture: dev/workflow-nets/bootstrap-harness.queue-state.json" in output
    assert "not canonical workflow authority" in output
    assert "queue active item: none" in output
    assert "new status active_slice: none" in output
    assert "written: no" in output
    assert "dry run: no changes written" in output
    assert status_path.read_text(encoding="utf-8") == status_before
    assert queue_path.read_text(encoding="utf-8") == queue_before


def test__WorkflowStatusReconciler__reconcile__writes_status_from_queue_active_none(tmp_path: Path) -> None:
    """Validate reconciliation writes active_slice none when queue has no active item."""
    # Status fixture is copied so the test can mutate it without touching repo state.
    status_path: Path = copied_status_fixture(tmp_path)
    # Queue fixture is copied and remains read-only source state.
    queue_path: Path = copied_queue_fixture(tmp_path)
    # Temp fixture is cleared so this test covers explicit no-active reconciliation behavior.
    clear_active_item(queue_path)
    # Reconciler performs the fixture-only status update.
    reconciler: WorkflowStatusReconciler = WorkflowStatusReconciler()

    # Result summarizes the status fixture update.
    result: WorkflowStatusReconciliationResult = reconciler.reconcile(status_path, queue_path)

    assert result.success is True
    assert result.queue_active_item_name == "none"
    assert result.new_active_slice == "none"
    assert result.wrote_fixture is True

    # Written status JSON is parsed to verify only visible status fields changed.
    status_data: dict[str, object] = json.loads(status_path.read_text(encoding="utf-8"))
    # Color data should carry the reconciled active-slice sentinel.
    color_data: dict[str, object] = status_token_color(status_data)
    # Decision data should preserve the user-decision gate.
    decision_data: dict[str, object] = typed_mapping(status_data["decision"])
    # Marking data should preserve the user_decision token location.
    marking_data: dict[str, object] = typed_mapping(status_data["marking"])

    assert color_data["active_slice"] == "none"
    assert color_data["requires_user_decision"] == "true"
    assert decision_data["requires_user_decision"] is True
    assert "activate a queued item" in str(decision_data["reason"])
    assert list(marking_data) == ["user_decision"]


def test__WorkflowStatusReconciler__reconcile__uses_queue_active_item_name(tmp_path: Path) -> None:
    """Validate reconciliation copies queue active item name when present."""
    # Status fixture is copied so the test can mutate it without touching repo state.
    status_path: Path = copied_status_fixture(tmp_path)
    # Queue fixture is copied and modified to contain an active item.
    queue_path: Path = copied_queue_fixture(tmp_path)
    # Queue fixture data is modified only in the temporary copy.
    queue_data: dict[str, object] = json.loads(queue_path.read_text(encoding="utf-8"))
    queue_data["active_item"] = {
        "name": "active-workflow-item",
        "state": "active",
        "artifact_refs": [],
    }
    queue_path.write_text(json.dumps(queue_data, indent=2) + "\n", encoding="utf-8")

    # Result should mirror queue active item into status active_slice.
    result: WorkflowStatusReconciliationResult = WorkflowStatusReconciler().reconcile(status_path, queue_path)

    assert result.queue_active_item_name == "active-workflow-item"
    assert result.new_active_slice == "active-workflow-item"
    assert status_token_color(json.loads(status_path.read_text(encoding="utf-8")))["active_slice"] == "active-workflow-item"


def test__WorkflowStatusReconciler__reconcile__dry_run_does_not_write_status(tmp_path: Path) -> None:
    """Validate dry-run computes reconciliation without writing status fixture."""
    # Status fixture is copied so the test can prove no-write behavior.
    status_path: Path = copied_status_fixture(tmp_path)
    # Queue fixture is copied and used as read-only source state.
    queue_path: Path = copied_queue_fixture(tmp_path)
    # Original status text should survive dry-run unchanged.
    before_text: str = status_path.read_text(encoding="utf-8")

    # Dry-run result should not write the status fixture.
    result: WorkflowStatusReconciliationResult = WorkflowStatusReconciler().reconcile(status_path, queue_path, dry_run=True)

    assert result.success is True
    assert result.wrote_fixture is False
    assert result.dry_run is True
    assert status_path.read_text(encoding="utf-8") == before_text


def copied_status_fixture(tmp_path: Path) -> Path:
    """Copy the repository status fixture into a temp path.

    Args:
        tmp_path: Pytest temporary directory.

    Returns:
        Temporary status fixture path.
    """
    # Source fixture is copied so tests do not mutate repository state.
    source_path: Path = Path("dev/workflow-nets/bootstrap-harness.workflow-net.json")
    # Destination fixture is the only status file mutated by reconciliation tests.
    destination_path: Path = tmp_path / "bootstrap-harness.workflow-net.json"
    shutil.copyfile(source_path, destination_path)
    return destination_path


def copied_queue_fixture(tmp_path: Path) -> Path:
    """Copy the repository queue fixture into a temp path.

    Args:
        tmp_path: Pytest temporary directory.

    Returns:
        Temporary queue fixture path.
    """
    # Source fixture is copied so tests do not mutate repository state.
    source_path: Path = Path("dev/workflow-nets/bootstrap-harness.queue-state.json")
    # Destination fixture is read by reconciliation tests.
    destination_path: Path = tmp_path / "bootstrap-harness.queue-state.json"
    shutil.copyfile(source_path, destination_path)
    return destination_path


def clear_active_item(fixture_path: Path) -> None:
    """Clear active item in a copied queue fixture.

    Args:
        fixture_path: Temporary queue fixture path to modify.
    """
    # Fixture copy is normalized to the no-active state needed by reconciliation behavior tests.
    fixture_data: dict[str, object] = json.loads(fixture_path.read_text(encoding="utf-8"))
    fixture_data["active_item"] = None
    fixture_path.write_text(json.dumps(fixture_data, indent=2) + "\n", encoding="utf-8")



def status_token_color(status_data: dict[str, object]) -> dict[str, object]:
    """Return the status fixture token color mapping.

    Args:
        status_data: Parsed status fixture data.

    Returns:
        Token color mapping.
    """
    # Marking data contains the user-decision token location.
    marking_data: dict[str, object] = typed_mapping(status_data["marking"])
    # User-decision token list contains one current-slice token.
    token_values: list[object] = typed_list(marking_data["user_decision"])
    # Token data contains the color map under assertion.
    token_data: dict[str, object] = typed_mapping(token_values[0])
    return typed_mapping(token_data["color"])


def typed_mapping(value: object) -> dict[str, object]:
    """Cast parsed JSON object to a typed mapping for assertions.

    Args:
        value: Parsed JSON value.

    Returns:
        Typed dictionary value.
    """
    assert isinstance(value, dict)
    return value


def typed_list(value: object) -> list[object]:
    """Cast parsed JSON array to a typed list for assertions.

    Args:
        value: Parsed JSON value.

    Returns:
        Typed list value.
    """
    assert isinstance(value, list)
    return value
