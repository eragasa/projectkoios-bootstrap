from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Violation:
    code: str
    action: str
    actor: str
    token_path: str
    reason: str
    required_owner: str | None = None
    suggested_next_action: str | None = None

    def to_markdown_block(self) -> str:
        lines = [f"- code: {self.code}"]
        lines.append(f"  actor: {self.actor}")
        if self.required_owner:
            lines.append(f"  required_owner: {self.required_owner}")
        lines.append(f"  reason: {self.reason}")
        if self.suggested_next_action:
            lines.append(f"  suggested_next_action: {self.suggested_next_action}")
        return "\n".join(lines) + "\n"
