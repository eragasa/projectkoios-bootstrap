from __future__ import annotations

from projectkoios.bootstrap.harness.data.violation import Violation


def test__Violation__to_markdown_block__formats_with_all_fields() -> None:
    v = Violation(
        code="wrong-implementation-owner",
        action="CompleteImplementation",
        actor="Hermes",
        token_path="/fake/handoff.md",
        reason="Only Vulcan may produce implementation-report artifacts.",
        required_owner="Vulcan",
        suggested_next_action="Route implementation completion to Vulcan.",
    )
    block = v.to_markdown_block()
    assert "code: wrong-implementation-owner" in block
    assert "actor: Hermes" in block
    assert "required_owner: Vulcan" in block
    assert "reason: Only Vulcan may produce" in block
    assert "suggested_next_action: Route implementation" in block


def test__Violation__to_markdown_block__omits_optional_fields_when_none() -> None:
    v = Violation(
        code="hermes-forwarded-without-decision",
        action="ForwardInboxState",
        actor="Hermes",
        token_path="/fake/handoff.md",
        reason="No routing decision produced.",
    )
    block = v.to_markdown_block()
    assert "code: hermes-forwarded-without-decision" in block
    assert "required_owner:" not in block
    assert "suggested_next_action:" not in block
