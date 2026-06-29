from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.violation import Violation, ViolationCode


def test__Violation__to_markdown_block__formats_with_all_fields() -> None:
    v = Violation(
        code=ViolationCode.WRONG_IMPLEMENTATION_OWNER,
        actor="Hermes",
        path=Path("/fake/handoff.md"),
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
        code=ViolationCode.HERMES_FORWARDED_WITHOUT_DECISION,
        actor="Hermes",
        path=Path("/fake/handoff.md"),
        reason="No routing decision produced.",
    )
    block = v.to_markdown_block()
    assert "code: hermes-forwarded-without-decision" in block
    assert "required_owner:" not in block
    assert "suggested_next_action:" not in block
