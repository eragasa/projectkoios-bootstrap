from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import Callable, TypeAlias


@dataclass(frozen=True, slots=True)
class Place:
    """Canonical workflow place.

    Args:
        place_id: Stable identifier for the place.
        label: Human-readable label for inspection output.
    """

    place_id: str
    label: str = ""


@dataclass(frozen=True, slots=True)
class Token:
    """Canonical colored workflow token.

    Args:
        token_id: Stable identifier for the token instance.
        color: Immutable token color payload used by guards.
    """

    token_id: str
    color: MappingProxyType[str, str] = field(default_factory=lambda: MappingProxyType({}))

    @classmethod
    def from_color(cls, token_id: str, color: dict[str, str] | None = None) -> Token:
        """Construct a token with an immutable color payload.

        Args:
            token_id: Stable identifier for the token instance.
            color: Optional mutable color payload to freeze.

        Returns:
            Token with copied immutable color data.
        """

        # Frozen color prevents callers from mutating token semantics after construction.
        frozen_color: MappingProxyType[str, str] = MappingProxyType(dict(color or {}))
        return cls(token_id=token_id, color=frozen_color)


@dataclass(frozen=True, slots=True)
class Transition:
    """Canonical workflow transition.

    Args:
        transition_id: Stable identifier for the transition.
        label: Human-readable label for inspection output.
        guard: Optional token-aware predicate for enabledness.
    """

    transition_id: str
    label: str = ""
    guard: Callable[[tuple[Token, ...]], bool] | None = None


class ArcKind(StrEnum):
    """Direction kind for workflow arcs."""

    INPUT = "input"
    OUTPUT = "output"


@dataclass(frozen=True, slots=True)
class Arc:
    """Connection between a place and transition.

    Args:
        place_id: Place endpoint identifier.
        transition_id: Transition endpoint identifier.
        kind: Whether the arc is an input or output arc for the transition.
        weight: Number of tokens consumed or produced by the arc.
    """

    place_id: str
    transition_id: str
    kind: ArcKind
    weight: int = 1


@dataclass(frozen=True, slots=True)
class Marking:
    """Current immutable token distribution by place."""

    tokens_by_place: MappingProxyType[str, tuple[Token, ...]] = field(default_factory=lambda: MappingProxyType({}))

    @classmethod
    def from_tokens(cls, tokens_by_place: Mapping[str, Sequence[Token]]) -> Marking:
        """Construct a marking from mutable place-token collections.

        Args:
            tokens_by_place: Mutable mapping of place identifiers to tokens.

        Returns:
            Immutable marking copy.
        """

        # Frozen mapping preserves checkpoint state for deterministic inspection.
        frozen_tokens: dict[str, tuple[Token, ...]] = {
            place_id: tuple(tokens) for place_id, tokens in tokens_by_place.items()
        }
        return cls(tokens_by_place=MappingProxyType(frozen_tokens))

    def tokens_at(self, place_id: str) -> tuple[Token, ...]:
        """Return tokens currently present at a place.

        Args:
            place_id: Place identifier to inspect.

        Returns:
            Immutable tuple of tokens at the place.
        """

        return self.tokens_by_place.get(place_id, ())


@dataclass(frozen=True, slots=True)
class WorkflowNet:
    """Canonical Petri-net workflow definition."""

    places: tuple[Place, ...]
    transitions: tuple[Transition, ...]
    arcs: tuple[Arc, ...]

    def place_ids(self) -> set[str]:
        """Return all declared place identifiers."""

        return {place.place_id for place in self.places}

    def transition_ids(self) -> set[str]:
        """Return all declared transition identifiers."""

        return {transition.transition_id for transition in self.transitions}

    def transition_by_id(self, transition_id: str) -> Transition:
        """Return a declared transition by identifier.

        Args:
            transition_id: Transition identifier to find.

        Raises:
            KeyError: When the transition is not declared.
        """

        transition: Transition
        for transition in self.transitions:
            if transition.transition_id == transition_id:
                return transition
        raise KeyError(transition_id)

    def input_arcs(self, transition_id: str) -> tuple[Arc, ...]:
        """Return input arcs for a transition."""

        return tuple(arc for arc in self.arcs if arc.transition_id == transition_id and arc.kind is ArcKind.INPUT)

    def output_arcs(self, transition_id: str) -> tuple[Arc, ...]:
        """Return output arcs for a transition."""

        return tuple(arc for arc in self.arcs if arc.transition_id == transition_id and arc.kind is ArcKind.OUTPUT)


@dataclass(frozen=True, slots=True)
class Binding:
    """Enabled transition binding over consumed tokens."""

    transition_id: str
    tokens_by_input_place: Mapping[str, tuple[Token, ...]]


@dataclass(frozen=True, slots=True)
class FiringRule:
    """Explicit firing request for a transition."""

    transition_id: str


@dataclass(frozen=True, slots=True)
class NetSchema:
    """Named schema marker for a workflow net definition."""

    schema_id: str = "projectkoios.workflow.net.v1"


@dataclass(frozen=True, slots=True)
class ExecutionState:
    """Runtime state for a workflow net and marking."""

    net: WorkflowNet
    marking: Marking


@dataclass(frozen=True, slots=True)
class DataObject:
    """Semantic wrapper for data objects carried by workflow tokens."""

    object_id: str


@dataclass(frozen=True, slots=True)
class ActivityObject:
    """Semantic wrapper for workflow activities."""

    object_id: str


@dataclass(frozen=True, slots=True)
class AgentObject:
    """Semantic wrapper for workflow agents."""

    object_id: str


@dataclass(frozen=True, slots=True)
class WorkspaceObject:
    """Semantic wrapper for workflow workspaces."""

    object_id: str


@dataclass(frozen=True, slots=True)
class ArtifactObject:
    """Semantic wrapper for workflow artifacts."""

    object_id: str


@dataclass(frozen=True, slots=True)
class PermissionObject:
    """Semantic wrapper for workflow permissions."""

    object_id: str


Guard: TypeAlias = Callable[[Marking], bool]
"""Read-only guard predicate over a marking."""
