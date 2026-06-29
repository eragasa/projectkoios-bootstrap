from __future__ import annotations

from dataclasses import dataclass, field

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact


@dataclass(frozen=True)
class Marking:
    tokens_by_place: dict[str, list[HandoffArtifact]] = field(default_factory=dict)

    def tokens_at(self, place: str) -> list[HandoffArtifact]:
        return list(self.tokens_by_place.get(place, []))

    @property
    def all_tokens(self) -> list[HandoffArtifact]:
        result: list[HandoffArtifact] = []
        for tokens in self.tokens_by_place.values():
            result.extend(tokens)
        return result
