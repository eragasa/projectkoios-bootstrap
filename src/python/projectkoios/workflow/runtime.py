from __future__ import annotations

from dataclasses import dataclass, field

from projectkoios.workflow.events import Event, ExecutionTrace
from projectkoios.workflow.model import Arc, Binding, ExecutionState, Marking, Token, Transition, WorkflowNet
from projectkoios.workflow.validation import WorkflowValidator


@dataclass(frozen=True, slots=True)
class FiredTransition:
    """Result of firing one enabled transition."""

    state: ExecutionState
    trace: ExecutionTrace


@dataclass(slots=True)
class WorkflowRuntime:
    """Runtime orchestrator for canonical workflow nets."""

    validator: WorkflowValidator = field(default_factory=WorkflowValidator)

    def enabled_bindings(self, state: ExecutionState) -> tuple[Binding, ...]:
        """Return enabled transition bindings for the current state.

        Args:
            state: Workflow execution state to inspect.

        Returns:
            Enabled bindings in declared transition order.
        """

        self.validator.validate_or_raise(state.net)
        # Bindings accumulate enabled transitions in deterministic declaration order.
        bindings: list[Binding] = []
        transition_id: str
        for transition_id in sorted(state.net.transition_ids()):
            # Binding is present only when all input places provide required tokens.
            binding: Binding | None = self.binding_for_transition(state, transition_id)
            if binding is not None:
                bindings.append(binding)
        return tuple(bindings)

    def binding_for_transition(self, state: ExecutionState, transition_id: str) -> Binding | None:
        """Return the enabled binding for a transition, if any.

        Args:
            state: Workflow execution state to inspect.
            transition_id: Transition identifier to inspect.

        Returns:
            Enabled binding or None when the transition is disabled.
        """

        # Input arcs define the required token counts per input place.
        input_arcs: tuple[Arc, ...] = state.net.input_arcs(transition_id)
        # Tokens by input place become the candidate binding for guard evaluation.
        tokens_by_input_place: dict[str, tuple[Token, ...]] = {}
        arc: Arc
        for arc in input_arcs:
            # Available tokens at this input place are consumed by declaration order.
            available_tokens: tuple[Token, ...] = state.marking.tokens_at(arc.place_id)
            if len(available_tokens) < arc.weight:
                return None
            tokens_by_input_place[arc.place_id] = available_tokens[: arc.weight]

        # Transition guard optionally filters the token tuple candidate.
        transition_tokens: tuple[Token, ...] = tuple(
            token for tokens in tokens_by_input_place.values() for token in tokens
        )
        # Transition declaration supplies the optional guard for this binding.
        transition: Transition = state.net.transition_by_id(transition_id)
        if transition.guard is not None and not transition.guard(transition_tokens):
            return None
        return Binding(transition_id=transition_id, tokens_by_input_place=tokens_by_input_place)

    def fire(self, state: ExecutionState, transition_id: str, trace: ExecutionTrace | None = None) -> FiredTransition:
        """Fire an enabled transition and return the next state.

        Args:
            state: Current workflow execution state.
            transition_id: Transition identifier to fire.
            trace: Optional existing execution trace.

        Returns:
            Fired transition result with new state and trace.

        Raises:
            ValueError: When the transition is not enabled.
        """

        # Binding proves the transition is enabled and selects consumed tokens.
        binding: Binding | None = self.binding_for_transition(state, transition_id)
        if binding is None:
            raise ValueError(f"transition is not enabled: {transition_id}")

        # Mutable token lists make consumption and production explicit before freezing.
        next_tokens: dict[str, list[Token]] = {
            place_id: list(tokens) for place_id, tokens in state.marking.tokens_by_place.items()
        }
        self.consume_input_tokens(state.net, binding, next_tokens)
        self.produce_output_tokens(state.net, binding, next_tokens)

        # Next marking freezes the updated token distribution for inspection safety.
        next_marking: Marking = Marking.from_tokens(next_tokens)
        # Trace is extended with one deterministic firing event.
        base_trace: ExecutionTrace = trace or ExecutionTrace()
        # Next trace records the completed firing event.
        next_trace: ExecutionTrace = base_trace.append(
            Event(event_type="transition-fired", transition_id=transition_id, details={"status": "completed"})
        )
        return FiredTransition(state=ExecutionState(net=state.net, marking=next_marking), trace=next_trace)

    def consume_input_tokens(
        self,
        net: WorkflowNet,
        binding: Binding,
        next_tokens: dict[str, list[Token]],
    ) -> None:
        """Consume tokens selected by an enabled binding.

        Args:
            net: Workflow net defining input arcs.
            binding: Enabled transition binding.
            next_tokens: Mutable next-token accumulator.
        """

        arc: Arc
        for arc in net.input_arcs(binding.transition_id):
            # Consumed tokens are removed from the front to preserve deterministic order.
            del next_tokens[arc.place_id][: arc.weight]

    def produce_output_tokens(
        self,
        net: WorkflowNet,
        binding: Binding,
        next_tokens: dict[str, list[Token]],
    ) -> None:
        """Produce output tokens for a fired transition.

        Args:
            net: Workflow net defining output arcs.
            binding: Enabled transition binding.
            next_tokens: Mutable next-token accumulator.
        """

        # Produced tokens preserve the consumed token colors for first-slice semantics.
        consumed_tokens: tuple[Token, ...] = tuple(
            token for tokens in binding.tokens_by_input_place.values() for token in tokens
        )
        arc: Arc
        for arc in net.output_arcs(binding.transition_id):
            # Output place is created lazily so sparse markings remain valid.
            output_tokens: list[Token] = next_tokens.setdefault(arc.place_id, [])
            output_tokens.extend(consumed_tokens[: arc.weight])
