from __future__ import annotations

from dataclasses import dataclass, field

from projectkoios.workflow.events import (
    PetriNetEventCollection,
    PetriNetMarkingChangedEvent,
    PetriNetTransitionFiredEvent,
)
from projectkoios.workflow.petrinet import (
    PetriNet,
    PetriNetArc,
    PetriNetMarking,
    PetriNetState,
    PetriNetToken,
    PetriNetTransition,
    PetriNetTransitionBinding,
)
from projectkoios.workflow.validation import WorkflowValidator


@dataclass(frozen=True, slots=True)
class PetriNetFiringResult:
    """Result of firing one enabled transition."""

    state: PetriNetState
    events: PetriNetEventCollection


@dataclass(slots=True)
class PetriNetExecutor:
    """Runtime executor for canonical Petri nets."""

    validator: WorkflowValidator = field(default_factory=WorkflowValidator)

    def enabled_bindings(self, state: PetriNetState) -> tuple[PetriNetTransitionBinding, ...]:
        """Return enabled transition bindings for the current state.

        Args:
            state: Petri-net state to inspect.

        Returns:
            Enabled bindings in declared transition order.
        """

        self.validator.validate_or_raise(state.net)
        # PetriNetTransitionBindings accumulate enabled transitions in deterministic declaration order.
        bindings: list[PetriNetTransitionBinding] = []
        transition_id: str
        for transition_id in sorted(state.net.transition_ids()):
            # PetriNetTransitionBinding is present only when all input places provide required tokens.
            binding: PetriNetTransitionBinding | None = self.binding_for_transition(state, transition_id)
            if binding is not None:
                bindings.append(binding)
        return tuple(bindings)

    def binding_for_transition(self, state: PetriNetState, transition_id: str) -> PetriNetTransitionBinding | None:
        """Return the enabled binding for a transition, if any.

        Args:
            state: Petri-net state to inspect.
            transition_id: PetriNetTransition identifier to inspect.

        Returns:
            Enabled binding or None when the transition is disabled.
        """

        # Input arcs define the required token counts per input place.
        input_arcs: tuple[PetriNetArc, ...] = state.net.input_arcs(transition_id)
        # PetriNetTokens by input place become the candidate binding for guard evaluation.
        tokens_by_input_place: dict[str, tuple[PetriNetToken, ...]] = {}
        arc: PetriNetArc
        for arc in input_arcs:
            # Available tokens at this input place are consumed by declaration order.
            available_tokens: tuple[PetriNetToken, ...] = state.marking.tokens_at(arc.place_id)
            if len(available_tokens) < arc.weight:
                return None
            tokens_by_input_place[arc.place_id] = available_tokens[: arc.weight]

        # PetriNetTransition guard optionally filters the token tuple candidate.
        transition_tokens: tuple[PetriNetToken, ...] = tuple(
            token for tokens in tokens_by_input_place.values() for token in tokens
        )
        # PetriNetTransition declaration supplies the optional guard for this binding.
        transition: PetriNetTransition = state.net.transition_by_id(transition_id)
        if transition.guard is not None and not transition.guard(transition_tokens):
            return None
        return PetriNetTransitionBinding(transition_id=transition_id, tokens_by_input_place=tokens_by_input_place)

    def fire(
        self,
        state: PetriNetState,
        transition_id: str,
        events: PetriNetEventCollection | None = None,
    ) -> PetriNetFiringResult:
        """Fire an enabled transition and return the next state.

        Args:
            state: Current Petri-net state.
            transition_id: PetriNetTransition identifier to fire.
            events: Optional existing in-process event collection.

        Returns:
            Firing result with new state and emitted events.

        Raises:
            ValueError: When the transition is not enabled.
        """

        # PetriNetTransitionBinding proves the transition is enabled and selects consumed tokens.
        binding: PetriNetTransitionBinding | None = self.binding_for_transition(state, transition_id)
        if binding is None:
            raise ValueError(f"transition is not enabled: {transition_id}")

        # Mutable token lists make consumption and production explicit before freezing.
        next_tokens: dict[str, list[PetriNetToken]] = {
            place_id: list(tokens) for place_id, tokens in state.marking.tokens_by_place.items()
        }
        self.consume_input_tokens(state.net, binding, next_tokens)
        self.produce_output_tokens(state.net, binding, next_tokens)

        # Next marking freezes the updated token distribution for inspection safety.
        next_marking: PetriNetMarking = PetriNetMarking.from_tokens(next_tokens)
        # Next state pairs the static Petri net with the new marking.
        next_state: PetriNetState = PetriNetState(net=state.net, marking=next_marking)
        # Runtime events expose transition firing and marking changes for in-process debugging.
        emitted_events: tuple[PetriNetTransitionFiredEvent | PetriNetMarkingChangedEvent, ...] = (
            self.transition_fired_event(state.net, binding),
            self.marking_changed_event(state.marking, next_marking),
        )
        # Event collection remains immutable and append-only for deterministic inspection.
        next_events: PetriNetEventCollection = (events or PetriNetEventCollection()).extend(emitted_events)
        return PetriNetFiringResult(state=next_state, events=next_events)

    def transition_fired_event(self, net: PetriNet, binding: PetriNetTransitionBinding) -> PetriNetTransitionFiredEvent:
        """Build the event emitted for a fired transition.

        Args:
            net: Petri net defining transition arcs.
            binding: Transition binding that fired.

        Returns:
            Transition-fired event.
        """

        # Input place identifiers describe the consumed side of the firing.
        input_place_ids: tuple[str, ...] = tuple(arc.place_id for arc in net.input_arcs(binding.transition_id))
        # Output place identifiers describe the produced side of the firing.
        output_place_ids: tuple[str, ...] = tuple(arc.place_id for arc in net.output_arcs(binding.transition_id))
        return PetriNetTransitionFiredEvent(
            transition_id=binding.transition_id,
            input_place_ids=input_place_ids,
            output_place_ids=output_place_ids,
        )

    def marking_changed_event(
        self,
        previous_marking: PetriNetMarking,
        next_marking: PetriNetMarking,
    ) -> PetriNetMarkingChangedEvent:
        """Build the event emitted for a marking change.

        Args:
            previous_marking: PetriNetMarking before firing.
            next_marking: PetriNetMarking after firing.

        Returns:
            PetriNetMarking-changed event.
        """

        # Place identifiers include every place touched by either marking snapshot.
        place_ids: set[str] = set(previous_marking.tokens_by_place) | set(next_marking.tokens_by_place)
        # Changed place identifiers are stable for deterministic event assertions.
        changed_place_ids: tuple[str, ...] = tuple(
            sorted(
                place_id
                for place_id in place_ids
                if previous_marking.tokens_at(place_id) != next_marking.tokens_at(place_id)
            )
        )
        return PetriNetMarkingChangedEvent(changed_place_ids=changed_place_ids)

    def consume_input_tokens(
        self,
        net: PetriNet,
        binding: PetriNetTransitionBinding,
        next_tokens: dict[str, list[PetriNetToken]],
    ) -> None:
        """Consume tokens selected by an enabled binding.

        Args:
            net: Petri net defining input arcs.
            binding: Enabled transition binding.
            next_tokens: Mutable next-token accumulator.
        """

        arc: PetriNetArc
        for arc in net.input_arcs(binding.transition_id):
            # Consumed tokens are removed from the front to preserve deterministic order.
            del next_tokens[arc.place_id][: arc.weight]

    def produce_output_tokens(
        self,
        net: PetriNet,
        binding: PetriNetTransitionBinding,
        next_tokens: dict[str, list[PetriNetToken]],
    ) -> None:
        """Produce output tokens for a fired transition.

        Args:
            net: Petri net defining output arcs.
            binding: Enabled transition binding.
            next_tokens: Mutable next-token accumulator.
        """

        # Produced tokens preserve the consumed token colors for first-slice semantics.
        consumed_tokens: tuple[PetriNetToken, ...] = tuple(
            token for tokens in binding.tokens_by_input_place.values() for token in tokens
        )
        arc: PetriNetArc
        for arc in net.output_arcs(binding.transition_id):
            # Output place is created lazily so sparse markings remain valid.
            output_tokens: list[PetriNetToken] = next_tokens.setdefault(arc.place_id, [])
            output_tokens.extend(consumed_tokens[: arc.weight])
