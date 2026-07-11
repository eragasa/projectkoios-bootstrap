from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import json
from pathlib import Path
from typing import cast

from projectkoios.workflow.petrinet import (
    PetriNetArc,
    PetriNetArcKind,
    PetriNetMarking,
    PetriNetPlace,
    PetriNetState,
    PetriNetToken,
    PetriNetTransition,
)
from projectkoios.workflow.runtime import PetriNetExecutor
from projectkoios.workflow.workflownet import WorkflowNet


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


@dataclass(frozen=True, slots=True)
class WorkflowQueueItem:
    """Static queue item copied from the queue-state fixture.

    Args:
        name: Stable queue item name.
        state: Queue state label from the fixture.
        artifact_refs: Source artifact locators copied from the fixture.
        why: Optional human-readable reason for the queue item.
        dependency_or_blocker: Optional dependency or blocker text.
        recommendation: Optional item-specific recommendation.
        commit: Optional commit reference for completed items.
    """

    name: str
    state: str
    artifact_refs: tuple[str, ...]
    why: str = ""
    dependency_or_blocker: str = ""
    recommendation: str = ""
    commit: str = ""


@dataclass(frozen=True, slots=True)
class WorkflowQueueStateFixture:
    """Loaded static workflow queue-state fixture.

    Args:
        path: Fixture path used for the load.
        queue_id: Stable queue-state identifier.
        surface: Fixture surface identifier.
        parent_effort: Parent effort name.
        status: Fixture status label.
        authority: Non-authority caveat copied from the fixture.
        active_item: Active queue item or None.
        queued_items: Queued/proposed items in fixture order.
        completed_items: Completed/accepted recent items in fixture order.
        superseded_items: Superseded/rejected items in fixture order.
        deferred_items: Deferred items in fixture order.
        next_decision_needed: Exact next decision copied from the fixture.
    """

    path: Path
    queue_id: str
    surface: str
    parent_effort: str
    status: str
    authority: str
    active_item: WorkflowQueueItem | None
    queued_items: tuple[WorkflowQueueItem, ...]
    completed_items: tuple[WorkflowQueueItem, ...]
    superseded_items: tuple[WorkflowQueueItem, ...]
    deferred_items: tuple[WorkflowQueueItem, ...]
    next_decision_needed: str


class WorkflowQueueStateFixtureLoader:
    """Load the static workflow queue-state fixture."""

    def __init__(self) -> None:
        """Initialize the queue-state fixture loader."""
        # Field reader reuses the existing narrow JSON validation helpers.
        self.field_reader: WorkflowStatusFixtureLoader = WorkflowStatusFixtureLoader()

    def load(self, fixture_path: Path) -> WorkflowQueueStateFixture:
        """Load the static queue-state fixture.

        Args:
            fixture_path: Queue-state fixture path.

        Returns:
            Loaded queue-state fixture.
        """
        # Raw JSON data is parsed from the explicit static fixture only.
        raw_data: object = json.loads(fixture_path.read_text(encoding="utf-8"))
        # Fixture data is validated by narrow field readers before rendering.
        fixture_data: Mapping[str, object] = self.field_reader.require_mapping(raw_data, "queue fixture")
        # Active item is optional and may be null when no item is active.
        active_item: WorkflowQueueItem | None = self.load_optional_item(fixture_data.get("active_item"), "active_item")
        return WorkflowQueueStateFixture(
            path=fixture_path,
            queue_id=self.field_reader.require_string(fixture_data, "queue_id"),
            surface=self.field_reader.require_string(fixture_data, "surface"),
            parent_effort=self.field_reader.require_string(fixture_data, "parent_effort"),
            status=self.field_reader.require_string(fixture_data, "status"),
            authority=self.field_reader.require_string(fixture_data, "authority"),
            active_item=active_item,
            queued_items=self.load_items(self.field_reader.require_sequence(fixture_data.get("queued_items"), "queued_items")),
            completed_items=self.load_items(
                self.field_reader.require_sequence(fixture_data.get("completed_items"), "completed_items")
            ),
            superseded_items=self.load_items(
                self.field_reader.require_sequence(fixture_data.get("superseded_items"), "superseded_items")
            ),
            deferred_items=self.load_items(
                self.field_reader.require_sequence(fixture_data.get("deferred_items"), "deferred_items")
            ),
            next_decision_needed=self.field_reader.require_string(fixture_data, "next_decision_needed"),
        )

    def load_optional_item(self, item_value: object, field_name: str) -> WorkflowQueueItem | None:
        """Load an optional queue item.

        Args:
            item_value: Raw queue item value or None.
            field_name: Field name used for errors.

        Returns:
            Loaded queue item or None.
        """
        if item_value is None:
            return None
        return self.load_item(self.field_reader.require_mapping(item_value, field_name))

    def load_items(self, item_values: Sequence[object]) -> tuple[WorkflowQueueItem, ...]:
        """Load queue items from a fixture array.

        Args:
            item_values: Raw queue item values.

        Returns:
            Queue items in fixture order.
        """
        # Items preserve fixture order so queue output remains deterministic.
        items: list[WorkflowQueueItem] = []
        item_value: object
        for item_value in item_values:
            # Each queue item is represented by one JSON object.
            item_data: Mapping[str, object] = self.field_reader.require_mapping(item_value, "queue item")
            items.append(self.load_item(item_data))
        return tuple(items)

    def load_item(self, item_data: Mapping[str, object]) -> WorkflowQueueItem:
        """Load one queue item.

        Args:
            item_data: Raw queue item mapping.

        Returns:
            Queue item data object.
        """
        # Artifact refs are display locators only, not live file readers.
        artifact_refs: tuple[str, ...] = self.load_artifact_refs(
            self.field_reader.require_sequence(item_data.get("artifact_refs", []), "artifact_refs")
        )
        return WorkflowQueueItem(
            name=self.field_reader.require_string(item_data, "name"),
            state=self.field_reader.require_string(item_data, "state"),
            artifact_refs=artifact_refs,
            why=self.field_reader.optional_string(item_data, "why", default=""),
            dependency_or_blocker=self.field_reader.optional_string(item_data, "dependency_or_blocker", default=""),
            recommendation=self.field_reader.optional_string(item_data, "recommendation", default=""),
            commit=self.field_reader.optional_string(item_data, "commit", default=""),
        )

    def load_artifact_refs(self, ref_values: Sequence[object]) -> tuple[str, ...]:
        """Load artifact reference strings.

        Args:
            ref_values: Raw artifact reference values.

        Returns:
            Artifact reference strings in fixture order.
        """
        # References are copied strings used only for display.
        refs: list[str] = []
        ref_value: object
        for ref_value in ref_values:
            if not isinstance(ref_value, str):
                raise ValueError("artifact_refs entries must be strings")
            refs.append(ref_value)
        return tuple(refs)


class WorkflowQueueStateReporter:
    """Render workflow queue-state fixtures for operator-readable CLI output."""

    def render(self, fixture: WorkflowQueueStateFixture) -> str:
        """Render deterministic queue-state text.

        Args:
            fixture: Loaded queue-state fixture.

        Returns:
            Human-readable queue-state text.
        """
        # Output lines are accumulated in fixed section order.
        lines: list[str] = [
            f"workflow queue: {fixture.queue_id}",
            f"fixture: {fixture.path.as_posix()}",
            f"mode: {fixture.status}; {fixture.authority}",
            "",
            "active:",
        ]
        lines.extend(self.active_lines(fixture.active_item))
        if fixture.active_item is not None:
            lines.extend([
                "",
                "WARNING: queue active_item is set; do not recommend or activate queued items until active item is cleared/accepted/rejected by HERMES/USER.",
            ])
        lines.extend(["", "queued/proposed:"])
        lines.extend(self.numbered_item_lines(fixture.queued_items))
        lines.extend(["", "completed/recent:"])
        lines.extend(self.bullet_item_lines(fixture.completed_items))
        lines.extend(["", "superseded/rejected:"])
        lines.extend(self.bullet_item_lines(fixture.superseded_items))
        lines.extend(["", "deferred:"])
        lines.extend(self.bullet_item_lines(fixture.deferred_items))
        lines.extend(["", "next decision needed:", f"  {fixture.next_decision_needed}"])
        return "\n".join(lines)

    def active_lines(self, active_item: WorkflowQueueItem | None) -> list[str]:
        """Render active queue item lines.

        Args:
            active_item: Active item or None.

        Returns:
            Active section lines.
        """
        if active_item is None:
            return ["  none"]
        return self.item_detail_lines(active_item, prefix="  - ")

    def numbered_item_lines(self, items: tuple[WorkflowQueueItem, ...]) -> list[str]:
        """Render numbered queue item lines.

        Args:
            items: Queue items to render.

        Returns:
            Numbered item lines.
        """
        if not items:
            return ["  none"]
        # Numbered items show queue/proposal order explicitly.
        lines: list[str] = []
        index: int
        item: WorkflowQueueItem
        for index, item in enumerate(items, start=1):
            lines.extend(self.item_detail_lines(item, prefix=f"  {index}. "))
        return lines

    def bullet_item_lines(self, items: tuple[WorkflowQueueItem, ...]) -> list[str]:
        """Render bullet queue item lines.

        Args:
            items: Queue items to render.

        Returns:
            Bullet item lines.
        """
        if not items:
            return ["  none"]
        # Bullet items preserve fixture order for stable output.
        lines: list[str] = []
        item: WorkflowQueueItem
        for item in items:
            lines.extend(self.item_detail_lines(item, prefix="  - "))
        return lines

    def item_detail_lines(self, item: WorkflowQueueItem, *, prefix: str) -> list[str]:
        """Render one queue item.

        Args:
            item: Queue item to render.
            prefix: Prefix for the first line.

        Returns:
            Item detail lines.
        """
        # First line carries the optional commit reference.
        commit_text: str = f" commit={item.commit}" if item.commit else ""
        # Detail lines begin with the item name and state before optional fields.
        lines: list[str] = [f"{prefix}{item.name} state={item.state}{commit_text}"]
        if item.why:
            lines.append(f"     why: {item.why}")
        if item.dependency_or_blocker:
            lines.append(f"     blocker: {item.dependency_or_blocker}")
        if item.recommendation:
            lines.append(f"     recommendation: {item.recommendation}")
        if item.artifact_refs:
            lines.append(f"     refs: {', '.join(item.artifact_refs)}")
        return lines


@dataclass(frozen=True, slots=True)
class WorkflowStatusReconciliationResult:
    """Result of reconciling status fixture active-slice from queue state.

    Args:
        success: Whether reconciliation completed.
        status_fixture_path: Status fixture path inspected or written.
        queue_fixture_path: Queue fixture path used as source.
        queue_active_item_name: Queue active item name or none.
        previous_active_slice: Status active-slice before reconciliation.
        new_active_slice: Status active-slice after reconciliation.
        next_decision_needed: Queue next-decision text.
        wrote_fixture: Whether the status fixture was written.
        dry_run: Whether the attempt intentionally avoided writing.
    """

    success: bool
    status_fixture_path: Path
    queue_fixture_path: Path
    queue_active_item_name: str
    previous_active_slice: str
    new_active_slice: str
    next_decision_needed: str
    wrote_fixture: bool
    dry_run: bool


class WorkflowStatusReconciler:
    """Reconcile static workflow status fixture from static queue state."""

    def __init__(self) -> None:
        """Initialize the status reconciler."""
        # Field reader reuses existing narrow JSON validation helpers.
        self.field_reader: WorkflowStatusFixtureLoader = WorkflowStatusFixtureLoader()

    def reconcile(self, status_fixture_path: Path, queue_fixture_path: Path, *, dry_run: bool = False) -> WorkflowStatusReconciliationResult:
        """Reconcile the status fixture active-slice from queue state.

        Args:
            status_fixture_path: Status fixture path that may be written.
            queue_fixture_path: Queue fixture path used as source state.
            dry_run: Whether to render the update without writing.

        Returns:
            Reconciliation result with before/after summary data.
        """
        # Queue fixture is read-only source state for reconciliation.
        queue_data: Mapping[str, object] = self.load_json_mapping(queue_fixture_path, "queue fixture")
        # Status fixture is copied into a mutable mapping before optional write.
        status_data: dict[str, object] = dict(self.load_json_mapping(status_fixture_path, "status fixture"))
        # Queue active name determines the desired status active-slice value.
        queue_active_item_name: str = self.queue_active_item_name(queue_data)
        # Previous active-slice is reported for operator review.
        previous_active_slice: str = self.status_active_slice(status_data)
        # New active-slice mirrors queue active item or none.
        new_active_slice: str = queue_active_item_name if queue_active_item_name != "none" else "none"
        self.update_status_fixture(status_data, new_active_slice)
        if not dry_run:
            self.write_status_fixture(status_fixture_path, status_data)
        return WorkflowStatusReconciliationResult(
            success=True,
            status_fixture_path=status_fixture_path,
            queue_fixture_path=queue_fixture_path,
            queue_active_item_name=queue_active_item_name,
            previous_active_slice=previous_active_slice,
            new_active_slice=new_active_slice,
            next_decision_needed=self.field_reader.require_string(queue_data, "next_decision_needed"),
            wrote_fixture=not dry_run,
            dry_run=dry_run,
        )

    def load_json_mapping(self, fixture_path: Path, field_name: str) -> Mapping[str, object]:
        """Load one JSON fixture object.

        Args:
            fixture_path: Fixture path to read.
            field_name: Field name used for errors.

        Returns:
            Parsed fixture mapping.
        """
        # Raw JSON data is read only from explicit fixture paths.
        raw_data: object = json.loads(fixture_path.read_text(encoding="utf-8"))
        return self.field_reader.require_mapping(raw_data, field_name)

    def queue_active_item_name(self, queue_data: Mapping[str, object]) -> str:
        """Return queue active item name or none.

        Args:
            queue_data: Queue fixture mapping.

        Returns:
            Active item name or none.
        """
        # Active item may be null when no workflow-engine item is active.
        active_item_value: object = queue_data.get("active_item")
        if active_item_value is None:
            return "none"
        # Active item name is copied from the queue fixture.
        active_item: Mapping[str, object] = self.field_reader.require_mapping(active_item_value, "active_item")
        return self.field_reader.require_string(active_item, "name")

    def status_active_slice(self, status_data: Mapping[str, object]) -> str:
        """Return the current status fixture active-slice value.

        Args:
            status_data: Status fixture mapping.

        Returns:
            Active-slice token color value.
        """
        # Color mapping contains the active-slice status under the current token.
        color_data: Mapping[str, object] = self.status_token_color(status_data)
        return self.field_reader.require_string(color_data, "active_slice")

    def update_status_fixture(self, status_data: dict[str, object], active_slice: str) -> None:
        """Update only status active-slice and decision reason.

        Args:
            status_data: Mutable status fixture mapping.
            active_slice: Active-slice value derived from queue state.
        """
        # Color mapping is the only token field modified by reconciliation.
        color_data: dict[str, object] = dict(self.status_token_color(status_data))
        color_data["active_slice"] = active_slice
        # Token mapping is copied so unrelated token fields are preserved.
        token_data: dict[str, object] = dict(self.status_token(status_data))
        token_data["color"] = color_data
        # Marking is copied and retains token id/place/topology.
        marking_data: dict[str, object] = dict(self.field_reader.require_mapping(status_data.get("marking"), "marking"))
        marking_data["user_decision"] = [token_data]
        status_data["marking"] = marking_data
        # Decision reason is aligned with queue state while preserving the decision requirement.
        decision_data: dict[str, object] = dict(self.field_reader.require_mapping(status_data.get("decision"), "decision"))
        decision_data["reason"] = "USER/HERMES decision is required to activate a queued item or define the next workflow-engine control slice."
        status_data["decision"] = decision_data

    def status_token(self, status_data: Mapping[str, object]) -> Mapping[str, object]:
        """Return the current status token mapping.

        Args:
            status_data: Status fixture mapping.

        Returns:
            Current token mapping at user_decision.
        """
        # Marking object contains token locations and must preserve user_decision place.
        marking_data: Mapping[str, object] = self.field_reader.require_mapping(status_data.get("marking"), "marking")
        # User-decision tokens contain the single current-slice token.
        token_values: Sequence[object] = self.field_reader.require_sequence(marking_data.get("user_decision"), "marking.user_decision")
        if len(token_values) != 1:
            raise ValueError("expected exactly one user_decision token")
        return self.field_reader.require_mapping(token_values[0], "current token")

    def status_token_color(self, status_data: Mapping[str, object]) -> Mapping[str, object]:
        """Return the current status token color mapping.

        Args:
            status_data: Status fixture mapping.

        Returns:
            Current token color mapping.
        """
        # Token color holds active_slice and requires_user_decision fields.
        token_data: Mapping[str, object] = self.status_token(status_data)
        return self.field_reader.require_mapping(token_data.get("color"), "token color")

    def write_status_fixture(self, status_fixture_path: Path, status_data: Mapping[str, object]) -> None:
        """Write deterministic status fixture JSON.

        Args:
            status_fixture_path: Status fixture path to write.
            status_data: Status fixture mapping to write.
        """
        # Deterministic JSON keeps fixture diffs reviewable.
        rendered_json: str = json.dumps(status_data, indent=2) + "\n"
        status_fixture_path.write_text(rendered_json, encoding="utf-8")


class WorkflowStatusReconciliationReporter:
    """Render status reconciliation results for CLI output."""

    def render(self, result: WorkflowStatusReconciliationResult) -> str:
        """Render a status reconciliation result.

        Args:
            result: Reconciliation result to render.

        Returns:
            Human-readable reconciliation summary.
        """
        # Output lines are intentionally compact for command-line review.
        lines: list[str] = [
            "workflow reconcile-status: reconciled status fixture from queue fixture",
            f"status fixture: {result.status_fixture_path.as_posix()}",
            f"queue fixture: {result.queue_fixture_path.as_posix()}",
            "mode: static fixture update; not canonical workflow authority and not product authority.",
            f"queue active item: {result.queue_active_item_name}",
            f"previous status active_slice: {result.previous_active_slice}",
            f"new status active_slice: {result.new_active_slice}",
            f"next decision needed: {result.next_decision_needed}",
            f"written: {'yes' if result.wrote_fixture else 'no'}",
        ]
        if result.dry_run:
            lines.append("dry run: no changes written")
        return "\n".join(lines)


@dataclass(frozen=True, slots=True)
class WorkflowQueueActivationResult:
    """Result of a static queue activation attempt.

    Args:
        success: Whether activation succeeded.
        fixture_path: Queue fixture path inspected by the command.
        previous_active_name: Active item name before activation, or none.
        activated_name: Item activated by this attempt, or none.
        remaining_queued_names: Queue item names remaining after the attempt.
        next_decision_needed: Next decision text after the attempt.
        message: Human-readable result message.
        wrote_fixture: Whether the fixture was written.
        dry_run: Whether the attempt intentionally avoided writing.
    """

    success: bool
    fixture_path: Path
    previous_active_name: str
    activated_name: str
    remaining_queued_names: tuple[str, ...]
    next_decision_needed: str
    message: str
    wrote_fixture: bool
    dry_run: bool


class WorkflowQueueStateActivator:
    """Activate one item in the static workflow queue fixture."""

    def __init__(self) -> None:
        """Initialize the queue activator."""
        # Field reader reuses the existing narrow JSON validation helpers.
        self.field_reader: WorkflowStatusFixtureLoader = WorkflowStatusFixtureLoader()

    def activate(self, fixture_path: Path, item_name: str, *, dry_run: bool = False) -> WorkflowQueueActivationResult:
        """Activate one queued item in the static queue fixture.

        Args:
            fixture_path: Queue-state fixture path to update.
            item_name: Queued item name to activate.
            dry_run: Whether to render the update without writing.

        Returns:
            Activation result with before/after summary data.
        """
        # Fixture data is the only persistent state this command may inspect or write.
        fixture_data: dict[str, object] = self.load_fixture_data(fixture_path)
        # Previous active item blocks activation when present.
        active_item_value: object = fixture_data.get("active_item")
        if active_item_value is not None:
            # Active item mapping is inspected to build a clear no-write failure.
            active_item: Mapping[str, object] = self.field_reader.require_mapping(active_item_value, "active_item")
            # Active item name is reported without mutating the fixture.
            active_name: str = self.field_reader.require_string(active_item, "name")
            return WorkflowQueueActivationResult(
                success=False,
                fixture_path=fixture_path,
                previous_active_name=active_name,
                activated_name="",
                remaining_queued_names=self.queued_names(fixture_data),
                next_decision_needed=self.field_reader.require_string(fixture_data, "next_decision_needed"),
                message=f"cannot activate {item_name}: active item already exists: {active_name}",
                wrote_fixture=False,
                dry_run=dry_run,
            )

        # Queued values are copied into a mutable list for deterministic removal.
        queued_values: list[object] = list(self.field_reader.require_sequence(fixture_data.get("queued_items"), "queued_items"))
        # Matching indexes identify the exact queued item requested by name.
        matching_indexes: list[int] = self.matching_item_indexes(queued_values, item_name)
        if len(matching_indexes) != 1:
            return WorkflowQueueActivationResult(
                success=False,
                fixture_path=fixture_path,
                previous_active_name="none",
                activated_name="",
                remaining_queued_names=self.queued_names(fixture_data),
                next_decision_needed=self.field_reader.require_string(fixture_data, "next_decision_needed"),
                message=f"cannot activate {item_name}: item is not queued/proposed",
                wrote_fixture=False,
                dry_run=dry_run,
            )

        # Activated index identifies the queued item to move.
        activated_index: int = matching_indexes[0]
        # Activated item is removed from the queue and marked active.
        activated_item: dict[str, object] = dict(
            self.field_reader.require_mapping(queued_values.pop(activated_index), "queued item")
        )
        activated_item["state"] = "active"
        fixture_data["active_item"] = activated_item
        fixture_data["queued_items"] = queued_values
        fixture_data["next_decision_needed"] = (
            f"Complete or review active item {item_name}; do not activate another item until active_item is cleared."
        )

        if not dry_run:
            self.write_fixture(fixture_path, fixture_data)

        return WorkflowQueueActivationResult(
            success=True,
            fixture_path=fixture_path,
            previous_active_name="none",
            activated_name=item_name,
            remaining_queued_names=self.queued_names(fixture_data),
            next_decision_needed=self.field_reader.require_string(fixture_data, "next_decision_needed"),
            message=f"activated {item_name}",
            wrote_fixture=not dry_run,
            dry_run=dry_run,
        )

    def load_fixture_data(self, fixture_path: Path) -> dict[str, object]:
        """Load queue fixture JSON as a mutable mapping.

        Args:
            fixture_path: Queue-state fixture path.

        Returns:
            Mutable fixture mapping.
        """
        # Raw JSON data is parsed from the explicit static fixture only.
        raw_data: object = json.loads(fixture_path.read_text(encoding="utf-8"))
        # Fixture object is copied so activation can mutate a local mapping before writing.
        fixture_data: dict[str, object] = dict(self.field_reader.require_mapping(raw_data, "queue fixture"))
        return fixture_data

    def matching_item_indexes(self, queued_values: list[object], item_name: str) -> list[int]:
        """Find queued item indexes matching a requested name.

        Args:
            queued_values: Raw queued item values.
            item_name: Requested item name.

        Returns:
            Matching indexes in queue order.
        """
        # Matching indexes preserve exact-match semantics and detect duplicates.
        indexes: list[int] = []
        index: int
        item_value: object
        for index, item_value in enumerate(queued_values):
            # Each queued value must be an object with a name.
            item_data: Mapping[str, object] = self.field_reader.require_mapping(item_value, "queued item")
            if self.field_reader.require_string(item_data, "name") == item_name:
                indexes.append(index)
        return indexes

    def queued_names(self, fixture_data: Mapping[str, object]) -> tuple[str, ...]:
        """Return queued item names from fixture data.

        Args:
            fixture_data: Queue fixture mapping.

        Returns:
            Queued item names in fixture order.
        """
        # Queued values are read from the fixture mapping for summary output.
        queued_values: Sequence[object] = self.field_reader.require_sequence(fixture_data.get("queued_items"), "queued_items")
        # Names preserve queue order for deterministic summaries.
        names: list[str] = []
        item_value: object
        for item_value in queued_values:
            # Each queued item contributes one display name.
            item_data: Mapping[str, object] = self.field_reader.require_mapping(item_value, "queued item")
            names.append(self.field_reader.require_string(item_data, "name"))
        return tuple(names)

    def write_fixture(self, fixture_path: Path, fixture_data: Mapping[str, object]) -> None:
        """Write deterministic queue fixture JSON.

        Args:
            fixture_path: Queue-state fixture path.
            fixture_data: Fixture mapping to write.
        """
        # Deterministic JSON keeps fixture diffs reviewable.
        rendered_json: str = json.dumps(fixture_data, indent=2) + "\n"
        fixture_path.write_text(rendered_json, encoding="utf-8")


class WorkflowQueueActivationReporter:
    """Render queue activation results for CLI output."""

    def render(self, result: WorkflowQueueActivationResult) -> str:
        """Render an activation result.

        Args:
            result: Activation result to render.

        Returns:
            Human-readable activation summary.
        """
        # Remaining queue text is explicit even when empty.
        remaining_text: str = ", ".join(result.remaining_queued_names) if result.remaining_queued_names else "none"
        # Output lines are intentionally compact for command-line review.
        lines: list[str] = [
            f"workflow activate: {result.message}",
            f"fixture: {result.fixture_path.as_posix()}",
            "mode: static fixture update; not canonical workflow authority and not product authority.",
            f"previous active: {result.previous_active_name}",
            f"activated item: {result.activated_name or 'none'}",
            f"remaining queued: {remaining_text}",
            f"next decision needed: {result.next_decision_needed}",
            f"written: {'yes' if result.wrote_fixture else 'no'}",
        ]
        if result.dry_run:
            lines.append("dry run: no changes written")
        return "\n".join(lines)


