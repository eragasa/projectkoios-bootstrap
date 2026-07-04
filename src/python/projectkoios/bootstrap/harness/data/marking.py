from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeAlias, TypeVar

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact

T = TypeVar("T")


@dataclass(frozen=True)
class Marking(Generic[T]):
    """The current distribution of colored tokens across all places.

    In Petri net terms, a marking assigns each place a set of tokens.
    This class provides read-only access: ``tokens_at(place_name)`` returns the
    tokens currently at that place, and ``all_tokens`` flattens every place for
    guards that scan across the entire net (e.g. ``check_wrong_implementation_owner``).

    A marking is built once per ``HandoffEvaluator.evaluate()`` call and
    passed to every guard function. It is never persisted.

    Generic over the token type ``T`` so the same marking structure serves
    handoff tokens (``Marking[HandoffArtifact]``) and daemon tokens
    (``Marking[DemonToken]``) without duplicating the type.
    """

    tokens_by_place: dict[str, list[T]] = field(default_factory=dict)

    def tokens_at(self, place: str) -> list[T]:
        """Tokens currently present at *place*, or an empty list."""
        return list(self.tokens_by_place.get(place, []))

    @property
    def all_tokens(self) -> list[T]:
        """Every token across every place, flattened."""
        # Result accumulates a stable flattened copy without exposing internal lists.
        result: list[T] = []
        tokens: list[T]
        for tokens in self.tokens_by_place.values():
            result.extend(tokens)
        return result


HandoffMarking: TypeAlias = Marking[HandoffArtifact]
"""Type alias for the handoff-specific marking used by the evaluator."""
