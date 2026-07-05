from __future__ import annotations

from dataclasses import dataclass

from projectkoios.workflow.model import WorkflowNet


@dataclass(frozen=True, slots=True)
class AdapterExport:
    """Adapter export payload for future third-party Petri-net integrations."""

    adapter_name: str
    net: WorkflowNet


class SnakesColoredNetAdapter:
    """Boundary placeholder for future SNAKES colored-net integration.

    The first workflow slice intentionally avoids importing third-party Petri-net
    libraries outside adapter classes.
    """

    def export(self, net: WorkflowNet) -> AdapterExport:
        """Return a typed adapter export payload.

        Args:
            net: Canonical workflow net to export.

        Returns:
            Adapter export payload.
        """

        return AdapterExport(adapter_name="snakes", net=net)


class Pm4pyProcessMiningAdapter:
    """Boundary placeholder for future PM4Py process-mining integration.

    The first workflow slice intentionally avoids importing third-party Petri-net
    libraries outside adapter classes.
    """

    def export(self, net: WorkflowNet) -> AdapterExport:
        """Return a typed adapter export payload.

        Args:
            net: Canonical workflow net to export.

        Returns:
            Adapter export payload.
        """

        return AdapterExport(adapter_name="pm4py", net=net)
