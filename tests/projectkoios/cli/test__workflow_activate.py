from __future__ import annotations

import json
from pathlib import Path
import shutil

from projectkoios.workflow.fixtures import WorkflowQueueActivationResult, WorkflowQueueStateActivator


def test__WorkflowQueueStateActivator__activate__moves_queued_item_to_active(tmp_path: Path) -> None:
    """Validate activation moves one queued item to active and writes deterministic JSON."""
    # Fixture path is a temp copy so the repository fixture is not mutated by tests.
    fixture_path: Path = copied_queue_fixture(tmp_path)
    # Temp fixture is cleared so this test exercises successful activation independent of live active queue state.
    clear_active_item(fixture_path)
    # Activator is the command service under test.
    activator: WorkflowQueueStateActivator = WorkflowQueueStateActivator()

    # Activation result summarizes the written fixture update.
    result: WorkflowQueueActivationResult = activator.activate(fixture_path, "pi-skill-determinism-slice-0")

    assert result.success is True
    assert result.wrote_fixture is True
    assert result.previous_active_name == "none"
    assert result.activated_name == "pi-skill-determinism-slice-0"
    assert result.remaining_queued_names == ()
    assert "Complete or review active item pi-skill-determinism-slice-0" in result.next_decision_needed

    # Written fixture remains valid deterministic JSON.
    written_text: str = fixture_path.read_text(encoding="utf-8")
    assert written_text.endswith("\n")
    # Written data is parsed to verify mutation semantics.
    written_data: dict[str, object] = json.loads(written_text)
    # Active item should now be the requested queued item.
    active_item: dict[str, object] = typed_mapping(written_data["active_item"])
    # Queued items should be empty after activating the only queued item.
    queued_items: list[object] = typed_list(written_data["queued_items"])
    # Completed items should preserve the reconciled Slice 4 commit entry.
    completed_items: list[object] = typed_list(written_data["completed_items"])

    assert active_item["name"] == "pi-skill-determinism-slice-0"
    assert active_item["state"] == "active"
    assert queued_items == []
    # Completed items are keyed by name so queue order changes do not break activation assertions.
    completed_items_by_name: dict[str, dict[str, object]] = {
        str(typed_mapping(item)["name"]): typed_mapping(item) for item in completed_items
    }
    assert completed_items_by_name["petrinet-workflow-queue-state-slice-4"]["commit"] == "5f209114"


def test__WorkflowQueueStateActivator__activate__fails_when_active_item_exists(tmp_path: Path) -> None:
    """Validate activation fails without writing when an active item already exists."""
    # Fixture path is a temp copy so failure can prove no-write behavior.
    fixture_path: Path = copied_queue_fixture(tmp_path)
    # Fixture data is modified to contain an existing active item.
    fixture_data: dict[str, object] = json.loads(fixture_path.read_text(encoding="utf-8"))
    fixture_data["active_item"] = {
        "name": "existing-active",
        "state": "active",
        "artifact_refs": [],
    }
    fixture_path.write_text(json.dumps(fixture_data, indent=2) + "\n", encoding="utf-8")
    # Original text is used to assert the command did not write on failure.
    before_text: str = fixture_path.read_text(encoding="utf-8")

    # Activation result should be a safe no-write failure.
    result: WorkflowQueueActivationResult = WorkflowQueueStateActivator().activate(
        fixture_path,
        "pi-skill-determinism-slice-0",
    )

    assert result.success is False
    assert result.wrote_fixture is False
    assert "active item already exists: existing-active" in result.message
    assert fixture_path.read_text(encoding="utf-8") == before_text


def test__WorkflowQueueStateActivator__activate__fails_when_item_is_not_queued(tmp_path: Path) -> None:
    """Validate activation fails without writing when the requested item is absent."""
    # Fixture path is a temp copy so failure can prove no-write behavior.
    fixture_path: Path = copied_queue_fixture(tmp_path)
    # Temp fixture is cleared so this test exercises missing-item failure rather than active-item blocking.
    clear_active_item(fixture_path)
    # Original text is used to assert the command did not write on failure.
    before_text: str = fixture_path.read_text(encoding="utf-8")

    # Activation result should be a safe no-write failure.
    result: WorkflowQueueActivationResult = WorkflowQueueStateActivator().activate(
        fixture_path,
        "missing-slice",
    )

    assert result.success is False
    assert result.wrote_fixture is False
    assert "item is not queued/proposed" in result.message
    assert fixture_path.read_text(encoding="utf-8") == before_text


def test__WorkflowQueueStateActivator__activate__dry_run_does_not_write(tmp_path: Path) -> None:
    """Validate dry-run computes activation without writing the fixture."""
    # Fixture path is a temp copy so dry-run can prove no-write behavior.
    fixture_path: Path = copied_queue_fixture(tmp_path)
    # Temp fixture is cleared so dry-run computes a success independent of live active queue state.
    clear_active_item(fixture_path)
    # Original text is used to assert dry-run did not write.
    before_text: str = fixture_path.read_text(encoding="utf-8")

    # Dry-run result should succeed while preserving fixture bytes.
    result: WorkflowQueueActivationResult = WorkflowQueueStateActivator().activate(
        fixture_path,
        "pi-skill-determinism-slice-0",
        dry_run=True,
    )

    assert result.success is True
    assert result.wrote_fixture is False
    assert result.dry_run is True
    assert result.activated_name == "pi-skill-determinism-slice-0"
    assert fixture_path.read_text(encoding="utf-8") == before_text


def copied_queue_fixture(tmp_path: Path) -> Path:
    """Copy the repository queue fixture into a temp path.

    Args:
        tmp_path: Pytest temporary directory.

    Returns:
        Temporary queue fixture path.
    """
    # Source fixture is copied so tests do not mutate repository state.
    source_path: Path = Path("dev/workflow-nets/bootstrap-harness.queue-state.json")
    # Destination fixture is the only file mutated by activation tests.
    destination_path: Path = tmp_path / "bootstrap-harness.queue-state.json"
    shutil.copyfile(source_path, destination_path)
    return destination_path


def clear_active_item(fixture_path: Path) -> None:
    """Clear active item in a copied queue fixture.

    Args:
        fixture_path: Temporary queue fixture path to modify.
    """
    # Fixture copy is normalized to the no-active state needed by activation behavior tests.
    fixture_data: dict[str, object] = json.loads(fixture_path.read_text(encoding="utf-8"))
    fixture_data["active_item"] = None
    fixture_path.write_text(json.dumps(fixture_data, indent=2) + "\n", encoding="utf-8")



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
