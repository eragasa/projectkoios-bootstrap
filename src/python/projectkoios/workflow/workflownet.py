from __future__ import annotations

from dataclasses import dataclass

from projectkoios.workflow.petrinet import PetriNetArc, PetriNetMarking, PetriNet, PetriNetPlace, PetriNetTransition


@dataclass(frozen=True, slots=True)
class WorkflowNet(PetriNet):
    """Workflow-specific Petri net.

    WorkflowNet inherits core Petri-net behavior from `PetriNet` so the generic
    Petri-net substrate can be extracted independently later.
    """

    places: tuple[PetriNetPlace, ...]
    transitions: tuple[PetriNetTransition, ...]
    arcs: tuple[PetriNetArc, ...]


@dataclass(frozen=True, slots=True)
class WorkflowExecutionState:
    """Runtime state for a workflow net and marking."""

    net: WorkflowNet
    marking: PetriNetMarking


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
