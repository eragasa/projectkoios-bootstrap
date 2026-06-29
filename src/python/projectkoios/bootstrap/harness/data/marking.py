from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import ArtifactToken


@dataclass(frozen=True)
class Marking:
    tokens_by_place: dict[str, list[ArtifactToken]] = field(default_factory=dict)
    source_root: Path | None = None
    loaded_at: str | None = None

    def tokens_at(self, place: str) -> list[ArtifactToken]:
        return list(self.tokens_by_place.get(place, []))

    def tokens_for_harness(self, harness: str) -> list[ArtifactToken]:
        result: list[ArtifactToken] = []
        for tokens in self.tokens_by_place.values():
            for token in tokens:
                if token.recipient == harness or token.sender == harness:
                    result.append(token)
        return result

    def find_contradictory(self) -> list[tuple[ArtifactToken, ArtifactToken]]:
        pairs: list[tuple[ArtifactToken, ArtifactToken]] = []
        tokens = [t for ts in self.tokens_by_place.values() for t in ts]
        for i, a in enumerate(tokens):
            for b in tokens[i + 1:]:
                if a.kind == b.kind and a.status == b.status and a.recipient != b.recipient:
                    pairs.append((a, b))
        return pairs
