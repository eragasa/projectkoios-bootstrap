from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.handoffs.topics import (
    build_topics_view,
)


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


def test__TopicsView__build_topics_view__includes_messages_transitions_topics(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "docs/archive/handoffs/archon/spec.md",
           "Origin: Athena\nFrom: Athena\nTo: Vulcan\nStatus: active\n\n"
           "# Implementation brief: evaluator\n")
    _write(root, "docs/archive/handoffs/opencode/report.md",
           "Origin: Vulcan\nFrom: Vulcan\nTo: Hermes\nStatus: active\n\n"
           "# Implementation report: done\n")

    view = build_topics_view(root)

    assert len(view.messages) == 2
    assert len(view.transitions) == 2
    assert view.topics is not None

    message_ids = {m.message_id for m in view.messages}
    assert "archon/spec.md" in message_ids
    assert "opencode/report.md" in message_ids

    assert "archon_inbox" in view.topics.places
    assert "opencode_inbox" in view.topics.places


def test__TopicsView__build_topics_view__each_message_has_created_transition(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "docs/archive/handoffs/archon/spec.md",
           "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n"
           "# Architecture spec\n")

    view = build_topics_view(root)

    assert len(view.transitions) == 1
    t = view.transitions[0]
    assert t.kind == "created"
    assert t.source == "inferred"
    assert "inferred_from" in t.evidence


def test__TopicsView__build_topics_view__no_timestamp_by_default(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "docs/archive/handoffs/archon/spec.md",
           "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n"
           "# Architecture spec\n")

    view = build_topics_view(root)
    assert view.generated_at is None


def test__TopicsView__build_topics_view__with_timestamp_includes_generated_at(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "docs/archive/handoffs/archon/spec.md",
           "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n"
           "# Architecture spec\n")

    view = build_topics_view(root, include_timestamp=True)
    assert view.generated_at is not None
    assert "T" in view.generated_at


def test__TopicsView__build_topics_view__skipped_files_included(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "docs/archive/handoffs/archon/good.md",
           "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n"
           "# Architecture spec\n")
    _write(root, "docs/archive/handoffs/archon/bad.md",
           "No frontmatter here\n\nJust prose\n")

    view = build_topics_view(root)

    assert len(view.messages) == 1
    assert len(view.skipped) == 1
    assert "bad.md" in view.skipped[0].source_path
    assert "headers" in view.skipped[0].reason


def test__TopicsView__build_topics_view__handles_empty_repo(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    view = build_topics_view(root)
    assert len(view.messages) == 0
    assert len(view.transitions) == 0
    assert len(view.guard_violations) == 0
    assert len(view.skipped) == 0


def test__TopicsView__build_topics_view__guard_violations_mapped_to_messages(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "docs/archive/handoffs/opencode/hermes-impl.md",
           "Origin: Hermes\nFrom: Hermes\nTo: Athena\nStatus: active\n\n"
           "# Implementation report: done by Hermes\n")

    view = build_topics_view(root)

    assert len(view.guard_violations) > 0
    codes = {g.code for g in view.guard_violations}
    assert "wrong-implementation-owner" in codes
