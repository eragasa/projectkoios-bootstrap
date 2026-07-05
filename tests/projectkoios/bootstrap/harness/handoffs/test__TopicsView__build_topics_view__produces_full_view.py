from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.handoffs.topics import TopicsView, Transition, build_topics_view


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


def test__TopicsView__build_topics_view__includes_messages_transitions_topics(
    tmp_path: Path,
) -> None:
    """Validate topics view includes messages, transitions, and topic places."""
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
        "Origin: Vulcan\nFrom: Vulcan\nTo: Hermes\nStatus: active\n\n"
        "# Implementation report: done\n",
    )

    # View is the full topics projection under assertion.
    view: TopicsView = build_topics_view(root)

    assert len(view.messages) == 2
    assert len(view.transitions) == 2
    assert view.topics is not None

    # Message IDs provide stable archive-relative identifiers.
    message_ids: set[str] = {message.message_id for message in view.messages}
    assert "archon/spec.md" in message_ids
    assert "opencode/report.md" in message_ids

    assert "archon_inbox" in view.topics.places
    assert "opencode_inbox" in view.topics.places


def test__TopicsView__build_topics_view__each_message_has_created_transition(
    tmp_path: Path,
) -> None:
    """Validate every parsed message has an inferred created transition."""
    # Root is the repository fixture used to build a topics view.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/archon/spec.md",
        "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n"
        "# Architecture spec\n",
    )

    # View is the full topics projection under assertion.
    view: TopicsView = build_topics_view(root)

    assert len(view.transitions) == 1
    # Transition is the inferred creation transition for the message.
    transition: Transition = view.transitions[0]
    assert transition.kind == "created"
    assert transition.source == "inferred"
    assert "inferred_from" in transition.evidence


def test__TopicsView__build_topics_view__no_timestamp_by_default(
    tmp_path: Path,
) -> None:
    """Validate topics view omits generated timestamp by default."""
    # Root is the repository fixture used to build a topics view.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/archon/spec.md",
        "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n"
        "# Architecture spec\n",
    )

    # View is the full topics projection under assertion.
    view: TopicsView = build_topics_view(root)
    assert view.generated_at is None


def test__TopicsView__build_topics_view__with_timestamp_includes_generated_at(
    tmp_path: Path,
) -> None:
    """Validate topics view can include generated timestamp metadata."""
    # Root is the repository fixture used to build a topics view.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/archon/spec.md",
        "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n"
        "# Architecture spec\n",
    )

    # View is the timestamped topics projection under assertion.
    view: TopicsView = build_topics_view(root, include_timestamp=True)
    assert view.generated_at is not None
    assert "T" in view.generated_at


def test__TopicsView__build_topics_view__skipped_files_included(
    tmp_path: Path,
) -> None:
    """Validate files without parseable headers are reported as skipped."""
    # Root is the repository fixture used to build a topics view.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/archon/good.md",
        "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n"
        "# Architecture spec\n",
    )
    _write(
        root,
        "docs/archive/handoffs/archon/bad.md",
        "No frontmatter here\n\nJust prose\n",
    )

    # View is the full topics projection under assertion.
    view: TopicsView = build_topics_view(root)

    assert len(view.messages) == 1
    assert len(view.skipped) == 1
    assert "bad.md" in view.skipped[0].source_path
    assert "headers" in view.skipped[0].reason


def test__TopicsView__build_topics_view__handles_empty_repo(
    tmp_path: Path,
) -> None:
    """Validate topics view handles repositories with no handoff files."""
    # Root is the empty repository fixture used to build a topics view.
    root: Path = _make_repo(tmp_path)
    # View is the empty topics projection under assertion.
    view: TopicsView = build_topics_view(root)
    assert len(view.messages) == 0
    assert len(view.transitions) == 0
    assert len(view.guard_violations) == 0
    assert len(view.skipped) == 0


def test__TopicsView__build_topics_view__guard_violations_mapped_to_messages(
    tmp_path: Path,
) -> None:
    """Validate guard violations are included in the topics view."""
    # Root is the repository fixture used to build a topics view.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/opencode/hermes-impl.md",
        "Origin: Hermes\nFrom: Hermes\nTo: Athena\nStatus: active\n\n"
        "# Implementation report: done by Hermes\n",
    )

    # View is the full topics projection under assertion.
    view: TopicsView = build_topics_view(root)

    assert len(view.guard_violations) > 0
    # Codes provide a concise assertion over emitted guard violation kinds.
    codes: set[str] = {violation.code for violation in view.guard_violations}
    assert "wrong-implementation-owner" in codes
