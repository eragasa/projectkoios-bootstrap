from __future__ import annotations

from argparse import ArgumentParser, Namespace
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, TypeAlias, cast

from projectkoios.workflow import (
    PetriNetArc,
    PetriNetArcKind,
    PetriNetExecutor,
    PetriNetMarking,
    PetriNetPlace,
    PetriNetState,
    PetriNetToken,
    PetriNetTransition,
    WorkflowNet,
)


SubparserCollection: TypeAlias = Any


@dataclass(frozen=True, slots=True)
class WorkflowDecisionStatus:
    """Static decision metadata copied from the bootstrap workflow-net fixture.

    Args:
        requires_user_decision: Whether the fixture marks the current state as waiting on a user decision.
        reason: Human-readable reason copied from the fixture.
    """

    requires_user_decision: bool
    reason: str


@dataclass(frozen=True, slots=True)
class WorkflowStatusFixture:
    """Loaded static workflow status fixture mapped into existing Petri-net runtime objects.

    Args:
        path: Fixture path used for the load.
        net_id: Stable workflow net identifier.
        state: Petri-net state assembled from the fixture.
        decision: Static decision metadata copied from the fixture.
    """

    path: Path
    net_id: str
    state: PetriNetState
    decision: WorkflowDecisionStatus


class WorkflowStatusFixtureLoader:
    """Load the one bootstrap workflow-net fixture into existing workflow runtime classes."""

    def load(self, fixture_path: Path) -> WorkflowStatusFixture:
        """Load the static workflow-net fixture.

        Args:
            fixture_path: Path to the static fixture JSON file.

        Returns:
            Fixture mapped into a Petri-net state plus decision metadata.
        """
        # Raw JSON data is validated by narrow field readers before runtime mapping.
        raw_data: object = json.loads(fixture_path.read_text(encoding="utf-8"))
        # Top-level fixture object owns the net, marking, and decision metadata.
        fixture_data: Mapping[str, object] = self.require_mapping(raw_data, "fixture")
        # Net identifier is printed so an operator can see which net is active.
        net_id: str = self.require_string(fixture_data, "net_id")
        # Places are mapped directly to existing PetriNetPlace objects.
        places: tuple[PetriNetPlace, ...] = self.load_places(self.require_sequence(fixture_data.get("places"), "places"))
        # Transitions are mapped directly to existing PetriNetTransition objects.
        transitions: tuple[PetriNetTransition, ...] = self.load_transitions(
            self.require_sequence(fixture_data.get("transitions"), "transitions")
        )
        # Arcs use existing PetriNetArcKind values from the fixture strings.
        arcs: tuple[PetriNetArc, ...] = self.load_arcs(self.require_sequence(fixture_data.get("arcs"), "arcs"))
        # WorkflowNet inherits the canonical PetriNet runtime representation.
        net: WorkflowNet = WorkflowNet(places=places, transitions=transitions, arcs=arcs)
        # Marking maps current token locations into immutable PetriNetMarking state.
        marking: PetriNetMarking = self.load_marking(self.require_mapping(fixture_data.get("marking", {}), "marking"))
        # Decision metadata stays a static fixture signal, not permission authority.
        decision: WorkflowDecisionStatus = self.load_decision(
            self.require_mapping(fixture_data.get("decision", {}), "decision")
        )
        return WorkflowStatusFixture(path=fixture_path, net_id=net_id, state=PetriNetState(net=net, marking=marking), decision=decision)

    def load_places(self, place_values: Sequence[object]) -> tuple[PetriNetPlace, ...]:
        """Map fixture place objects into Petri-net places.

        Args:
            place_values: Raw place objects from the fixture.

        Returns:
            Places in fixture declaration order.
        """
        # Places preserve declaration order for operator-readable output.
        places: list[PetriNetPlace] = []
        place_value: object
        for place_value in place_values:
            # Each place object carries an identifier and display label.
            place_data: Mapping[str, object] = self.require_mapping(place_value, "place")
            places.append(
                PetriNetPlace(
                    place_id=self.require_string(place_data, "place_id"),
                    label=self.require_string(place_data, "label"),
                )
            )
        return tuple(places)

    def load_transitions(self, transition_values: Sequence[object]) -> tuple[PetriNetTransition, ...]:
        """Map fixture transition objects into Petri-net transitions.

        Args:
            transition_values: Raw transition objects from the fixture.

        Returns:
            Transitions in fixture declaration order.
        """
        # Transitions preserve fixture labels while enabledness remains runtime-computed.
        transitions: list[PetriNetTransition] = []
        transition_value: object
        for transition_value in transition_values:
            # Each transition object carries an identifier and display label.
            transition_data: Mapping[str, object] = self.require_mapping(transition_value, "transition")
            transitions.append(
                PetriNetTransition(
                    transition_id=self.require_string(transition_data, "transition_id"),
                    label=self.require_string(transition_data, "label"),
                )
            )
        return tuple(transitions)

    def load_arcs(self, arc_values: Sequence[object]) -> tuple[PetriNetArc, ...]:
        """Map fixture arc objects into Petri-net arcs.

        Args:
            arc_values: Raw arc objects from the fixture.

        Returns:
            Arcs in fixture declaration order.
        """
        # Arcs preserve existing PetriNetArcKind text values from the fixture.
        arcs: list[PetriNetArc] = []
        arc_value: object
        for arc_value in arc_values:
            # Each arc object binds one place to one transition in one direction.
            arc_data: Mapping[str, object] = self.require_mapping(arc_value, "arc")
            # Weight is optional in this narrow fixture and defaults to one.
            weight: int = self.optional_integer(arc_data, "weight", default=1)
            arcs.append(
                PetriNetArc(
                    place_id=self.require_string(arc_data, "place_id"),
                    transition_id=self.require_string(arc_data, "transition_id"),
                    kind=PetriNetArcKind(self.require_string(arc_data, "kind")),
                    weight=weight,
                )
            )
        return tuple(arcs)

    def load_marking(self, marking_data: Mapping[str, object]) -> PetriNetMarking:
        """Map fixture marking data into immutable Petri-net marking.

        Args:
            marking_data: Raw mapping of place identifiers to token objects.

        Returns:
            Petri-net marking with tokens at their current places.
        """
        # Tokens are grouped by place before freezing into PetriNetMarking.
        tokens_by_place: dict[str, list[PetriNetToken]] = {}
        place_id: str
        token_values: object
        for place_id, token_values in marking_data.items():
            # Each marking entry is a place-specific token collection.
            tokens_by_place[place_id] = self.load_tokens(self.require_sequence(token_values, f"marking.{place_id}"))
        return PetriNetMarking.from_tokens(tokens_by_place)

    def load_tokens(self, token_values: Sequence[object]) -> list[PetriNetToken]:
        """Map fixture token objects into Petri-net tokens.

        Args:
            token_values: Raw token objects from one marking place.

        Returns:
            Tokens in fixture declaration order.
        """
        # Tokens remain mutable only until PetriNetMarking freezes the collection.
        tokens: list[PetriNetToken] = []
        token_value: object
        for token_value in token_values:
            # Each token has a stable id and string-valued color payload.
            token_data: Mapping[str, object] = self.require_mapping(token_value, "token")
            tokens.append(
                PetriNetToken.from_color(
                    token_id=self.require_string(token_data, "token_id"),
                    color=self.load_color(self.require_mapping(token_data.get("color", {}), "color")),
                )
            )
        return tokens

    def load_color(self, color_data: Mapping[str, object]) -> dict[str, str]:
        """Map fixture token color data into the current string-valued token color shape.

        Args:
            color_data: Raw token color mapping.

        Returns:
            String-valued color mapping for PetriNetToken.
        """
        # Color values stay strings to match the current PetriNetToken contract.
        color: dict[str, str] = {}
        color_key: str
        color_value: object
        for color_key, color_value in color_data.items():
            if not isinstance(color_value, str):
                raise ValueError(f"color field must be a string: {color_key}")
            color[color_key] = color_value
        return color

    def load_decision(self, decision_data: Mapping[str, object]) -> WorkflowDecisionStatus:
        """Map fixture decision metadata into a status object.

        Args:
            decision_data: Raw decision metadata from the fixture.

        Returns:
            Static decision status copied from the fixture.
        """
        # Decision boolean answers whether the operator must decide now.
        requires_user_decision: bool = self.optional_boolean(decision_data, "requires_user_decision", default=False)
        # Reason is explanatory only and does not create permission authority.
        reason: str = self.optional_string(decision_data, "reason", default="")
        return WorkflowDecisionStatus(requires_user_decision=requires_user_decision, reason=reason)

    def require_mapping(self, value: object, field_name: str) -> Mapping[str, object]:
        """Require a JSON value to be an object mapping.

        Args:
            value: JSON value to inspect.
            field_name: Field name used in the error message.

        Returns:
            Mapping view of the JSON object.
        """
        if not isinstance(value, dict):
            raise ValueError(f"expected object for {field_name}")
        return cast(Mapping[str, object], value)

    def require_sequence(self, value: object, field_name: str) -> Sequence[object]:
        """Require a JSON value to be an array sequence.

        Args:
            value: JSON value to inspect.
            field_name: Field name used in the error message.

        Returns:
            Sequence view of the JSON array.
        """
        if not isinstance(value, list):
            raise ValueError(f"expected array for {field_name}")
        return cast(Sequence[object], value)

    def require_string(self, mapping: Mapping[str, object], field_name: str) -> str:
        """Require a mapping field to be a string.

        Args:
            mapping: Mapping containing the field.
            field_name: Field name to read.

        Returns:
            String field value.
        """
        # Field value is checked before being returned as a string.
        value: object = mapping.get(field_name)
        if not isinstance(value, str):
            raise ValueError(f"expected string field: {field_name}")
        return value

    def optional_string(self, mapping: Mapping[str, object], field_name: str, *, default: str) -> str:
        """Read an optional string field.

        Args:
            mapping: Mapping containing the field.
            field_name: Field name to read.
            default: Value used when the field is absent.

        Returns:
            String field value or default.
        """
        # Optional field defaults only when omitted.
        value: object = mapping.get(field_name, default)
        if not isinstance(value, str):
            raise ValueError(f"expected string field: {field_name}")
        return value

    def optional_integer(self, mapping: Mapping[str, object], field_name: str, *, default: int) -> int:
        """Read an optional integer field.

        Args:
            mapping: Mapping containing the field.
            field_name: Field name to read.
            default: Value used when the field is absent.

        Returns:
            Integer field value or default.
        """
        # Optional field defaults only when omitted.
        value: object = mapping.get(field_name, default)
        if not isinstance(value, int):
            raise ValueError(f"expected integer field: {field_name}")
        return value

    def optional_boolean(self, mapping: Mapping[str, object], field_name: str, *, default: bool) -> bool:
        """Read an optional boolean field.

        Args:
            mapping: Mapping containing the field.
            field_name: Field name to read.
            default: Value used when the field is absent.

        Returns:
            Boolean field value or default.
        """
        # Optional field defaults only when omitted.
        value: object = mapping.get(field_name, default)
        if not isinstance(value, bool):
            raise ValueError(f"expected boolean field: {field_name}")
        return value


class WorkflowStatusReporter:
    """Render workflow status fixtures for operator-readable CLI output."""

    def __init__(self, executor: PetriNetExecutor | None = None) -> None:
        """Initialize the reporter.

        Args:
            executor: Optional Petri-net executor used to compute enabled transitions.
        """
        # Executor computes enabled transitions from runtime state, not fixture prose.
        self.executor: PetriNetExecutor = executor or PetriNetExecutor()

    def render(self, fixture: WorkflowStatusFixture) -> str:
        """Render deterministic status text for the workflow fixture.

        Args:
            fixture: Loaded workflow status fixture.

        Returns:
            Human-readable status text.
        """
        # Enabled bindings are computed through the existing Petri-net runtime.
        enabled_transition_ids: tuple[str, ...] = tuple(
            binding.transition_id for binding in self.executor.enabled_bindings(fixture.state)
        )
        # Output lines are accumulated in display order for deterministic assertions.
        lines: list[str] = [
            f"workflow: {fixture.net_id}",
            f"fixture: {fixture.path.as_posix()}",
            "",
            "active:",
            f"  user decision required: {self.yes_no(fixture.decision.requires_user_decision)}",
        ]
        if fixture.decision.reason:
            lines.append(f"  reason: {fixture.decision.reason}")
        lines.extend(["", "places:"])
        place: PetriNetPlace
        for place in fixture.state.net.places:
            lines.append(f"  - {place.place_id}: {place.label}")
        lines.extend(["", "tokens:"])
        lines.extend(self.token_lines(fixture))
        lines.extend(["", "enabled transitions:"])
        lines.extend(self.enabled_transition_lines(fixture, enabled_transition_ids))
        lines.extend(["", f"user decision required: {self.yes_no(fixture.decision.requires_user_decision)}"])
        return "\n".join(lines)

    def token_lines(self, fixture: WorkflowStatusFixture) -> list[str]:
        """Render current token locations.

        Args:
            fixture: Loaded workflow status fixture.

        Returns:
            Token lines for CLI output.
        """
        # Token lines are generated by declared place order to keep output stable.
        lines: list[str] = []
        place: PetriNetPlace
        for place in fixture.state.net.places:
            token: PetriNetToken
            for token in fixture.state.marking.tokens_at(place.place_id):
                lines.append(f"  - {token.token_id} at {place.place_id} color={self.color_text(token.color)}")
        if not lines:
            lines.append("  - none")
        return lines

    def enabled_transition_lines(self, fixture: WorkflowStatusFixture, enabled_transition_ids: tuple[str, ...]) -> list[str]:
        """Render transitions currently enabled by the Petri-net runtime.

        Args:
            fixture: Loaded workflow status fixture.
            enabled_transition_ids: Transition identifiers returned by the executor.

        Returns:
            Enabled transition lines for CLI output.
        """
        # Enabled identifiers are converted back to transition labels for display.
        lines: list[str] = []
        transition_id: str
        for transition_id in enabled_transition_ids:
            # Transition lookup uses the runtime net definition, not hard-coded labels.
            transition: PetriNetTransition = fixture.state.net.transition_by_id(transition_id)
            lines.append(f"  - {transition.transition_id}: {transition.label}")
        if not lines:
            lines.append("  - none")
        return lines

    def color_text(self, color: Mapping[str, str]) -> str:
        """Render deterministic token color text.

        Args:
            color: Token color mapping.

        Returns:
            Compact color text.
        """
        # Color fields are sorted to avoid JSON insertion-order surprises.
        items: list[str] = [f"{key}={color[key]}" for key in sorted(color)]
        return "{" + ", ".join(items) + "}"

    def yes_no(self, value: bool) -> str:
        """Render a boolean as yes or no.

        Args:
            value: Boolean status value.

        Returns:
            Operator-readable yes/no text.
        """
        if value:
            return "yes"
        return "no"


class Command:
    """Workflow CLI command adapter."""

    def __init__(self, loader: WorkflowStatusFixtureLoader | None = None, reporter: WorkflowStatusReporter | None = None) -> None:
        """Initialize the command adapter.

        Args:
            loader: Optional fixture loader for tests.
            reporter: Optional status reporter for tests.
        """
        # Loader maps the static fixture into runtime objects.
        self.loader: WorkflowStatusFixtureLoader = loader or WorkflowStatusFixtureLoader()
        # Reporter formats runtime-computed status for CLI output.
        self.reporter: WorkflowStatusReporter = reporter or WorkflowStatusReporter()

    def register(self, subparsers: SubparserCollection) -> None:
        """Register workflow commands on the top-level parser.

        Args:
            subparsers: Parent argparse subparser collection receiving the command group.
        """
        # Parser owns the top-level workflow command group.
        parser: ArgumentParser = subparsers.add_parser("workflow", help="Workflow Petri-net inspection commands")
        # Workflow subparsers dispatch read-only workflow actions.
        workflow_subparsers: SubparserCollection = parser.add_subparsers(dest="action")
        workflow_subparsers.required = True

        # Status parser exposes the static bootstrap harness net for inspection.
        status_parser: ArgumentParser = workflow_subparsers.add_parser("status", help="Show current workflow status")
        status_parser.set_defaults(func=self.run_status)

    def run_status(self, args: Namespace) -> None:
        """Run the read-only workflow status command.

        Args:
            args: Parsed CLI namespace.
        """
        # Fixture path is intentionally fixed for slice 0 static bootstrap inspectability.
        fixture_path: Path = Path("dev/workflow-nets/bootstrap-harness.workflow-net.json")
        # Loaded fixture contains both static metadata and Petri-net runtime state.
        fixture: WorkflowStatusFixture = self.loader.load(fixture_path)
        print(self.reporter.render(fixture))


def register(subparsers: SubparserCollection) -> None:
    """Register workflow commands on a parent subparser collection.

    Args:
        subparsers: Parent argparse subparser collection receiving the command group.
    """

    Command().register(subparsers)
