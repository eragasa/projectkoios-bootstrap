from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class ViolationCode(StrEnum):
    HERMES_FORWARDED_WITHOUT_DECISION = "hermes-forwarded-without-decision"
    WRONG_IMPLEMENTATION_OWNER = "wrong-implementation-owner"
    DELEGATED_OPERATOR_MISSING = "delegated-operator-missing"
    CODEX_AS_PI_IDENTITY_COLLAPSE = "codex-as-pi-identity-collapse"


@dataclass(frozen=True)
class Violation:
    code: ViolationCode
    action: str
    actor: str
    path: Path
    reason: str
    required_owner: str | None = None
    suggested_next_action: str | None = None

    def to_markdown_block(self) -> str:
        lines = [f"- code: {self.code.value}"]
        lines.append(f"  actor: {self.actor}")
        if self.required_owner:
            lines.append(f"  required_owner: {self.required_owner}")
        lines.append(f"  reason: {self.reason}")
        if self.suggested_next_action:
            lines.append(f"  suggested_next_action: {self.suggested_next_action}")
        return "\n".join(lines) + "\n"
