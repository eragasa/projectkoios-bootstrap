from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact
from projectkoios.bootstrap.harness.data.marking import Marking


def _token(
    tag: str = "token",
    kind: str = "user-request",
    sender: str = "Athena",
    recipient: str = "Vulcan",
) -> HandoffArtifact:
    return HandoffArtifact(
        path=Path(f"/fake/{tag}.md"),
        kind=kind,
        origin=sender,
        sender=sender,
        recipient=recipient,
    )


def test__Marking__tokens_at__returns_tokens_for_place() -> None:
    t1 = _token("t1")
    t2 = _token("t2")
    marking = Marking(tokens_by_place={"athena_inbox": [t1], "vulcan_inbox": [t2]})

    assert marking.tokens_at("athena_inbox") == [t1]
    assert marking.tokens_at("vulcan_inbox") == [t2]


def test__Marking__tokens_at__returns_empty_list_for_unknown_place() -> None:
    marking = Marking()
    assert marking.tokens_at("nonexistent") == []


def test__Marking__all_tokens__returns_all() -> None:
    t1 = _token("t1")
    t2 = _token("t2")
    marking = Marking(tokens_by_place={"a": [t1], "b": [t2]})

    result = marking.all_tokens
    assert len(result) == 2
    assert t1 in result
    assert t2 in result


def test__Marking__all_tokens__returns_empty_when_no_tokens() -> None:
    marking = Marking()
    assert marking.all_tokens == []
