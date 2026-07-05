from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.handoff import KoiosHandoff
from projectkoios.bootstrap.harness.data.marking import HandoffMarking, PetriNetMarking


def _token(
    tag: str = "token",
    kind: str = "user-request",
    sender: str = "Athena",
    recipient: str = "Vulcan",
) -> KoiosHandoff:
    """Create a Koios handoff fixture for marking tests."""
    return KoiosHandoff(
        path=Path(f"/fake/{tag}.md"),
        kind=kind,
        origin=sender,
        sender=sender,
        recipient=recipient,
    )


def test__Marking__tokens_at__returns_tokens_for_place() -> None:
    """Validate tokens_at returns tokens for the requested place."""
    # First token is assigned to the Athena inbox fixture.
    token_one: KoiosHandoff = _token("t1")
    # Second token is assigned to the Vulcan inbox fixture.
    token_two: KoiosHandoff = _token("t2")
    # PetriNetMarking stores tokens by place for lookup assertions.
    marking: HandoffMarking = PetriNetMarking(tokens_by_place={"athena_inbox": [token_one], "vulcan_inbox": [token_two]})

    assert marking.tokens_at("athena_inbox") == [token_one]
    assert marking.tokens_at("vulcan_inbox") == [token_two]


def test__Marking__tokens_at__returns_empty_list_for_unknown_place() -> None:
    """Validate tokens_at returns an empty list for missing places."""
    # PetriNetMarking contains no tokens or places.
    marking: HandoffMarking = PetriNetMarking()
    assert marking.tokens_at("nonexistent") == []


def test__Marking__all_tokens__returns_all() -> None:
    """Validate all_tokens flattens tokens from every place."""
    # First token is assigned to one marking place.
    token_one: KoiosHandoff = _token("t1")
    # Second token is assigned to another marking place.
    token_two: KoiosHandoff = _token("t2")
    # PetriNetMarking stores both tokens across separate places.
    marking: HandoffMarking = PetriNetMarking(tokens_by_place={"a": [token_one], "b": [token_two]})

    # Result is the flattened token list under assertion.
    result: list[KoiosHandoff] = marking.all_tokens
    assert len(result) == 2
    assert token_one in result
    assert token_two in result


def test__Marking__all_tokens__returns_empty_when_no_tokens() -> None:
    """Validate all_tokens returns empty when marking has no tokens."""
    # PetriNetMarking contains no tokens or places.
    marking: HandoffMarking = PetriNetMarking()
    assert marking.all_tokens == []
