from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.violation import Violation, ViolationCode


def test__Violation__to_markdown_block__formats_with_all_fields() -> None:
    """Validate to_markdown_block formats required and optional fields."""
    # Violation fixture includes every optional markdown output field.
    violation: Violation = Violation(
        code=ViolationCode.WRONG_IMPLEMENTATION_OWNER,
        actor="Hermes",
        path=Path("/fake/handoff.md"),
        reason="Only Vulcan may produce implementation-report artifacts.",
        required_owner="Vulcan",
        suggested_next_action="Route implementation completion to Vulcan.",
    )

    # Markdown block is the serialized violation output under assertion.
    block: str = violation.to_markdown_block()
    assert "code: wrong-implementation-owner" in block
    assert "actor: Hermes" in block
    assert "required_owner: Vulcan" in block
    assert "reason: Only Vulcan may produce" in block
    assert "suggested_next_action: Route implementation" in block


def test__Violation__to_markdown_block__omits_optional_fields_when_none() -> None:
    """Validate to_markdown_block omits unset optional fields."""
    # Violation fixture includes only required markdown output fields.
    violation: Violation = Violation(
        code=ViolationCode.HERMES_FORWARDED_WITHOUT_DECISION,
        actor="Hermes",
        path=Path("/fake/handoff.md"),
        reason="No routing decision produced.",
    )

    # Markdown block is the serialized violation output under assertion.
    block: str = violation.to_markdown_block()
    assert "code: hermes-forwarded-without-decision" in block
    assert "required_owner:" not in block
    assert "suggested_next_action:" not in block
