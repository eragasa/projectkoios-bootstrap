from __future__ import annotations

from dataclasses import dataclass, field

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact


@dataclass(frozen=True)
class Marking:
    """The current distribution of colored tokens across all places.

    In Petri net terms, a marking assigns each place (inbox) a set of tokens.
    This class provides read-only access: ``tokens_at(place_name)`` returns the
    tokens currently at that place, and ``all_tokens`` flattens every place for
    guards that scan across the entire net (e.g. ``check_wrong_implementation_owner``).

    A marking is built once per ``HandoffEvaluator.evaluate()`` call and
    passed to every guard function. It is never persisted.
    """

    tokens_by_place: dict[str, list[HandoffArtifact]] = field(default_factory=dict)

    def tokens_at(self, place: str) -> list[HandoffArtifact]:
        """Tokens currently present at *place*, or an empty list."""
        return list(self.tokens_by_place.get(place, []))

    @property
    def all_tokens(self) -> list[HandoffArtifact]:
        """Every token across every place, flattened."""
        result: list[HandoffArtifact] = []
        for tokens in self.tokens_by_place.values():
            result.extend(tokens)
        return result
