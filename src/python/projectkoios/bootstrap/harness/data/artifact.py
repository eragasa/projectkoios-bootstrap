from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class HandoffArtifact:
    id: str
    path: Path
    kind: str
    origin: str
    sender: str
    recipient: str
    acting_as: str | None = None
    repository: str | None = None
    status: str = "active"
    created_at: str | None = None
    delegated_operator: str | None = None
    provenance: list[str] | None = None

    def provenance_has_codex(self) -> bool:
        if self.delegated_operator and self.delegated_operator.lower() == "codex":
            return True
        if self.provenance:
            return any("codex" in ref.lower() for ref in self.provenance)
        return False
