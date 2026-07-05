from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from projectkoios.bootstrap.harness.handoffs.topics import TopicsView, build_topics_view


def _make_repo(tmp_path: Path) -> Path:
    """Create a repository fixture with archived handoff directories."""
    # Root is the repository fixture used to build a topics view.
    root: Path = tmp_path / "repo"
    # Place directory identifies one archived handoff inbox path.
    place_dir: str
    for place_dir in (
        "docs/archive/handoffs/archon",
        "docs/archive/handoffs/opencode",
        "docs/archive/handoffs/pi",
        "docs/archive/handoffs/goose",
    ):
        (root / place_dir).mkdir(parents=True)
    return root


def _write(root: Path, rel: str, content: str) -> None:
    """Write a handoff fixture file relative to the repository root."""
    # Path is the concrete fixture file to create.
    path: Path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test__TopicsView__build_topics_view__deterministic_across_runs(
    tmp_path: Path,
) -> None:
    """Validate topics view output is deterministic across runs."""
    # Root is the repository fixture used to build a topics view.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/archon/spec.md",
        "Origin: Athena\nFrom: Athena\nTo: Vulcan\nStatus: active\n\n"
        "# Implementation brief: evaluator\n",
    )
    _write(
        root,
        "docs/archive/handoffs/opencode/report.md",
        "Origin: Vulcan\nFrom: Vulcan\nTo: Hermes\n\n"
        "# Implementation report: done\n",
    )

    # First view is the baseline topics projection.
    view_a: TopicsView = build_topics_view(root)
    # Second view should match the baseline topics projection.
    view_b: TopicsView = build_topics_view(root)

    # First dictionary removes environment-specific fields before comparison.
    dict_a: dict[str, object] = asdict(view_a)
    # Second dictionary removes environment-specific fields before comparison.
    dict_b: dict[str, object] = asdict(view_b)

    dict_a.pop("generated_at", None)
    dict_b.pop("generated_at", None)
    dict_a.pop("repo_root", None)
    dict_b.pop("repo_root", None)

    assert dict_a == dict_b


def test__TopicsView__build_topics_view__does_not_mutate_files(
    tmp_path: Path,
) -> None:
    """Validate topics view construction does not mutate source files."""
    # Root is the repository fixture used to build a topics view.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/archon/spec.md",
        "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n"
        "# Architecture spec\n",
    )

    # Spec path is the source handoff file checked for read-only behavior.
    spec_path: Path = root / "docs/archive/handoffs/archon/spec.md"
    # Content before captures the source file before topics view construction.
    content_before: str = spec_path.read_text(encoding="utf-8")

    build_topics_view(root)

    # Content after captures the source file after topics view construction.
    content_after: str = spec_path.read_text(encoding="utf-8")
    assert content_before == content_after


def test__TopicsView__build_topics_view__deterministic_ids_across_runs(
    tmp_path: Path,
) -> None:
    """Validate topics view message identifiers are deterministic."""
    # Root is the repository fixture used to build a topics view.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/archon/spec.md",
        "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n"
        "# Architecture spec\n",
    )

    # First view is the baseline topics projection.
    view_a: TopicsView = build_topics_view(root)
    # Second view should preserve message identifiers.
    view_b: TopicsView = build_topics_view(root)

    # First message identifiers are the baseline stable IDs.
    ids_a: list[str] = [message.message_id for message in view_a.messages]
    # Second message identifiers should match baseline stable IDs.
    ids_b: list[str] = [message.message_id for message in view_b.messages]
    assert ids_a == ids_b
