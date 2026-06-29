from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import ArtifactToken
from projectkoios.bootstrap.harness.data.marking import Marking


def _token(
    id: str,
    kind: str = "user-request",
    sender: str = "Athena",
    recipient: str = "Vulcan",
) -> ArtifactToken:
    return ArtifactToken(
        id=id,
        path=Path(f"/fake/{id}.md"),
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


def test__Marking__tokens_for_harness__matches_sender_or_recipient() -> None:
    t1 = _token("t1", sender="Athena", recipient="Vulcan")
    t2 = _token("t2", sender="Vulcan", recipient="Hermes")
    marking = Marking(tokens_by_place={"a": [t1], "b": [t2]})

    result = marking.tokens_for_harness("Vulcan")
    assert len(result) == 2
    assert t1 in result
    assert t2 in result


def test__Marking__find_contradictory__detects_same_kind_different_recipient() -> None:
    t1 = _token("t1", kind="implementation-brief", recipient="Vulcan")
    t2 = _token("t2", kind="implementation-brief", recipient="Hermes")
    marking = Marking(tokens_by_place={"a": [t1], "b": [t2]})

    pairs = marking.find_contradictory()
    assert len(pairs) == 1
    assert (t1, t2) in pairs or (t2, t1) in pairs


def test__Marking__find_contradictory__returns_empty_for_no_conflicts() -> None:
    t1 = _token("t1", kind="architecture-spec", recipient="Vulcan")
    t2 = _token("t2", kind="implementation-brief", recipient="Vulcan")
    marking = Marking(tokens_by_place={"a": [t1], "b": [t2]})

    assert marking.find_contradictory() == []
