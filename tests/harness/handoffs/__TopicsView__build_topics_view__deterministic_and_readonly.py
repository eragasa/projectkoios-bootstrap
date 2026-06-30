from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from projectkoios.bootstrap.harness.handoffs.topics import build_topics_view


def _make_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    for place_dir in (
        "docs/archive/handoffs/archon",
        "docs/archive/handoffs/opencode",
        "docs/archive/handoffs/pi",
        "docs/archive/handoffs/goose",
    ):
        (root / place_dir).mkdir(parents=True)
    return root


def _write(root: Path, rel: str, content: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def test__TopicsView__build_topics_view__deterministic_across_runs(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "docs/archive/handoffs/archon/spec.md",
           "Origin: Athena\nFrom: Athena\nTo: Vulcan\nStatus: active\n\n"
           "# Implementation brief: evaluator\n")
    _write(root, "docs/archive/handoffs/opencode/report.md",
           "Origin: Vulcan\nFrom: Vulcan\nTo: Hermes\n\n"
           "# Implementation report: done\n")

    view_a = build_topics_view(root)
    view_b = build_topics_view(root)

    dict_a = asdict(view_a)
    dict_b = asdict(view_b)

    dict_a.pop("generated_at", None)
    dict_b.pop("generated_at", None)
    dict_a.pop("repo_root", None)
    dict_b.pop("repo_root", None)

    assert dict_a == dict_b


def test__TopicsView__build_topics_view__does_not_mutate_files(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "docs/archive/handoffs/archon/spec.md",
           "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n"
           "# Architecture spec\n")

    spec_path = root / "docs/archive/handoffs/archon/spec.md"
    content_before = spec_path.read_text(encoding="utf-8")

    build_topics_view(root)

    content_after = spec_path.read_text(encoding="utf-8")
    assert content_before == content_after


def test__TopicsView__build_topics_view__deterministic_ids_across_runs(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "docs/archive/handoffs/archon/spec.md",
           "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n"
           "# Architecture spec\n")

    view_a = build_topics_view(root)
    view_b = build_topics_view(root)

    ids_a = [m.message_id for m in view_a.messages]
    ids_b = [m.message_id for m in view_b.messages]
    assert ids_a == ids_b
