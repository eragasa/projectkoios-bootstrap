from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Callable, TypeAlias


@dataclass(frozen=True, slots=True)
class PetriNetPlace:
    """Canonical Petri-net place.

    Args:
        place_id: Stable identifier for the place.
        label: Human-readable label for inspection output.
    """

    place_id: str
    label: str = ""


@dataclass(frozen=True, slots=True)
class PetriNetToken:
    """Canonical colored Petri-net token.

    Args:
        token_id: Stable identifier for the token instance.
        color: Immutable token color payload used by guards.
    """

    token_id: str
    color: MappingProxyType[str, str] = field(default_factory=lambda: MappingProxyType({}))

    @classmethod
    def from_color(cls, token_id: str, color: dict[str, str] | None = None) -> PetriNetToken:
        """Construct a token with an immutable color payload.

        Args:
            token_id: Stable identifier for the token instance.
            color: Optional mutable color payload to freeze.

        Returns:
            PetriNetToken with copied immutable color data.
        """

        # Frozen color prevents callers from mutating token semantics after construction.
        frozen_color: MappingProxyType[str, str] = MappingProxyType(dict(color or {}))
        return cls(token_id=token_id, color=frozen_color)


@dataclass(frozen=True, slots=True)
class PetriNetTransition:
    """Canonical Petri-net transition.

    Args:
        transition_id: Stable identifier for the transition.
        label: Human-readable label for inspection output.
        guard: Optional token-aware predicate for enabledness.
    """

    transition_id: str
    label: str = ""
    guard: Callable[[tuple[PetriNetToken, ...]], bool] | None = None


class PetriNetArcKind(StrEnum):
    """Direction kind for Petri-net arcs."""

    INPUT = "input"
    OUTPUT = "output"


@dataclass(frozen=True, slots=True)
class PetriNetArc:
    """Connection between a place and transition.

    Args:
        place_id: PetriNetPlace endpoint identifier.
        transition_id: PetriNetTransition endpoint identifier.
        kind: Whether the arc is an input or output arc for the transition.
        weight: Number of tokens consumed or produced by the arc.
    """

    place_id: str
    transition_id: str
    kind: PetriNetArcKind
    weight: int = 1


@dataclass(frozen=True, slots=True)
class PetriNetMarking:
    """Current immutable token distribution by place."""

    tokens_by_place: MappingProxyType[str, tuple[PetriNetToken, ...]] = field(default_factory=lambda: MappingProxyType({}))

    @classmethod
    def from_tokens(cls, tokens_by_place: Mapping[str, Sequence[PetriNetToken]]) -> PetriNetMarking:
        """Construct a marking from mutable place-token collections.

        Args:
            tokens_by_place: Mutable mapping of place identifiers to tokens.

        Returns:
            Immutable marking copy.
        """

        # Frozen mapping preserves checkpoint state for deterministic inspection.
        frozen_tokens: dict[str, tuple[PetriNetToken, ...]] = {
            place_id: tuple(tokens) for place_id, tokens in tokens_by_place.items()
        }
        return cls(tokens_by_place=MappingProxyType(frozen_tokens))

    def tokens_at(self, place_id: str) -> tuple[PetriNetToken, ...]:
        """Return tokens currently present at a place.

        Args:
            place_id: PetriNetPlace identifier to inspect.

        Returns:
            Immutable tuple of tokens at the place.
        """

        return self.tokens_by_place.get(place_id, ())


@dataclass(frozen=True, slots=True)
class PetriNet:
    """Canonical Petri-net definition."""

    places: tuple[PetriNetPlace, ...]
    transitions: tuple[PetriNetTransition, ...]
    arcs: tuple[PetriNetArc, ...]

    def place_ids(self) -> set[str]:
        """Return all declared place identifiers."""

        return {place.place_id for place in self.places}

    def transition_ids(self) -> set[str]:
        """Return all declared transition identifiers."""

        return {transition.transition_id for transition in self.transitions}

    def transition_by_id(self, transition_id: str) -> PetriNetTransition:
        """Return a declared transition by identifier.

        Args:
            transition_id: PetriNetTransition identifier to find.

        Raises:
            KeyError: When the transition is not declared.
        """

        transition: PetriNetTransition
        for transition in self.transitions:
            if transition.transition_id == transition_id:
                return transition
        raise KeyError(transition_id)

    def input_arcs(self, transition_id: str) -> tuple[PetriNetArc, ...]:
        """Return input arcs for a transition."""

        return tuple(arc for arc in self.arcs if arc.transition_id == transition_id and arc.kind is PetriNetArcKind.INPUT)

    def output_arcs(self, transition_id: str) -> tuple[PetriNetArc, ...]:
        """Return output arcs for a transition."""

        return tuple(arc for arc in self.arcs if arc.transition_id == transition_id and arc.kind is PetriNetArcKind.OUTPUT)


@dataclass(frozen=True, slots=True)
class PetriNetTransitionBinding:
    """Enabled transition binding over consumed tokens."""

    transition_id: str
    tokens_by_input_place: Mapping[str, tuple[PetriNetToken, ...]]


@dataclass(frozen=True, slots=True)
class PetriNetFiringRequest:
    """Explicit firing request for a transition."""

    transition_id: str


@dataclass(frozen=True, slots=True)
class PetriNetSchema:
    """Named schema marker for a workflow net definition."""

    schema_id: str = "projectkoios.workflow.net.v1"


@dataclass(frozen=True, slots=True)
class PetriNetState:
    """Runtime state for a Petri net and marking."""

    net: PetriNet
    marking: PetriNetMarking


Guard: TypeAlias = Callable[[PetriNetMarking], bool]
"""Read-only guard predicate over a marking."""
