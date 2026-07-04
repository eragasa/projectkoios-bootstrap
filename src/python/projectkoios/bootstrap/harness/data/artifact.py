from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class HandoffArtifact:
    """A colored token in the meta-harness Petri net.

    Each handoff file under ``*/handoffs/*.md`` is parsed into one artifact.
    The fields other than ``path`` form the token's *color* — the metadata
    that determines which guard rules apply.

    Fields map directly to handoff file headers:
    - ``kind`` is inferred from the title and header combination
      (see ``HandoffParser.infer_kind``).
    - ``origin``, ``sender``, ``recipient`` come from ``Origin``, ``From``,
      ``To`` headers.
    - ``acting_as`` and ``delegated_operator`` come from their eponymous headers.
    - ``provenance`` is a collated list of selected header values used by
      ``check_codex_as_pi_identity_collapse``.
    """

    path: Path
    kind: str
    origin: str
    sender: str
    recipient: str
    acting_as: str | None = None
    delegated_operator: str | None = None
    provenance: list[str] | None = None

    def provenance_has_codex(self) -> bool:
        """True if any provenance field references Codex, indicating mediation."""
        if self.delegated_operator and self.delegated_operator.lower() == "codex":
            return True
        if self.provenance:
            return any("codex" in ref.lower() for ref in self.provenance)
        return False
