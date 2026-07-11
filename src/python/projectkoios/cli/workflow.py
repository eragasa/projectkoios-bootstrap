from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, TypeAlias

from projectkoios.workflow.fixtures import (
    WorkflowQueueActivationReporter,
    WorkflowQueueActivationResult,
    WorkflowQueueStateActivator,
    WorkflowQueueStateFixture,
    WorkflowQueueStateFixtureLoader,
    WorkflowQueueStateReporter,
    WorkflowStatusFixture,
    WorkflowStatusFixtureLoader,
    WorkflowStatusReconciliationReporter,
    WorkflowStatusReconciliationResult,
    WorkflowStatusReconciler,
    WorkflowStatusReporter,
)


SubparserCollection: TypeAlias = Any


class Command:
    """Workflow CLI command adapter."""

    def __init__(
        self,
        loader: WorkflowStatusFixtureLoader | None = None,
        reporter: WorkflowStatusReporter | None = None,
        queue_loader: WorkflowQueueStateFixtureLoader | None = None,
        queue_reporter: WorkflowQueueStateReporter | None = None,
        queue_activator: WorkflowQueueStateActivator | None = None,
        activation_reporter: WorkflowQueueActivationReporter | None = None,
        status_reconciler: WorkflowStatusReconciler | None = None,
        reconciliation_reporter: WorkflowStatusReconciliationReporter | None = None,
    ) -> None:
        """Initialize the command adapter.

        Args:
            loader: Optional fixture loader for tests.
            reporter: Optional status reporter for tests.
            queue_loader: Optional queue-state fixture loader for tests.
            queue_reporter: Optional queue-state reporter for tests.
            queue_activator: Optional queue-state activator for tests.
            activation_reporter: Optional activation reporter for tests.
            status_reconciler: Optional status reconciler for tests.
            reconciliation_reporter: Optional reconciliation reporter for tests.
        """
        # Loader maps the static fixture into runtime objects.
        self.loader: WorkflowStatusFixtureLoader = loader or WorkflowStatusFixtureLoader()
        # Reporter formats runtime-computed status for CLI output.
        self.reporter: WorkflowStatusReporter = reporter or WorkflowStatusReporter()
        # Queue loader maps the static queue fixture into queue data objects.
        self.queue_loader: WorkflowQueueStateFixtureLoader = queue_loader or WorkflowQueueStateFixtureLoader()
        # Queue reporter formats static queue state for CLI output.
        self.queue_reporter: WorkflowQueueStateReporter = queue_reporter or WorkflowQueueStateReporter()
        # Queue activator mutates only the static queue fixture by explicit command.
        self.queue_activator: WorkflowQueueStateActivator = queue_activator or WorkflowQueueStateActivator()
        # Activation reporter formats before/after mutation summaries.
        self.activation_reporter: WorkflowQueueActivationReporter = activation_reporter or WorkflowQueueActivationReporter()
        # Status reconciler mutates only the static status fixture from queue state.
        self.status_reconciler: WorkflowStatusReconciler = status_reconciler or WorkflowStatusReconciler()
        # Reconciliation reporter formats status before/after summaries.
        self.reconciliation_reporter: WorkflowStatusReconciliationReporter = reconciliation_reporter or WorkflowStatusReconciliationReporter()

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

        # Queue parser exposes static workflow queue-state inspectability.
        queue_parser: ArgumentParser = workflow_subparsers.add_parser("queue", help="Show workflow queue state")
        queue_parser.set_defaults(func=self.run_queue)

        # Activate parser mutates only the static queue-state fixture by explicit item name.
        activate_parser: ArgumentParser = workflow_subparsers.add_parser("activate", help="Activate a queued workflow item")
        activate_parser.add_argument("item")
        activate_parser.add_argument("--dry-run", action="store_true")
        activate_parser.set_defaults(func=self.run_activate)

        # Reconcile-status parser mutates only the static status fixture from queue state.
        reconcile_parser: ArgumentParser = workflow_subparsers.add_parser("reconcile-status", help="Reconcile workflow status from queue state")
        reconcile_parser.add_argument("--dry-run", action="store_true")
        reconcile_parser.set_defaults(func=self.run_reconcile_status)

    def run_status(self, args: Namespace) -> None:
        """Run the read-only workflow status command.

        Args:
            args: Parsed CLI namespace.
        """
        # Fixture path is intentionally fixed for slice 0 static bootstrap inspectability.
        fixture_path: Path = Path("dev/workflow-nets/bootstrap-harness.workflow-net.json")
        # Loaded fixture contains both static metadata and Petri-net runtime state.
        fixture: WorkflowStatusFixture = self.loader.load(fixture_path)
        # Queue fixture path is read-only overlay state for operator safety.
        queue_fixture_path: Path = Path("dev/workflow-nets/bootstrap-harness.queue-state.json")
        # Queue fixture prevents Petri-net token status from hiding queue blockers.
        queue_fixture: WorkflowQueueStateFixture = self.queue_loader.load(queue_fixture_path)
        # Status text preserves the existing Petri-net runtime-derived output.
        status_text: str = self.reporter.render(fixture)
        # Queue text is displayed as read-only overlay control state.
        queue_text: str = self.queue_reporter.render(queue_fixture)
        print(f"{status_text}\n\nqueue control surface:\n{queue_text}")

    def run_queue(self, args: Namespace) -> None:
        """Run the read-only workflow queue-state command.

        Args:
            args: Parsed CLI namespace.
        """
        # Fixture path is intentionally fixed for static queue-state inspectability.
        fixture_path: Path = Path("dev/workflow-nets/bootstrap-harness.queue-state.json")
        # Loaded queue fixture contains static control-surface state only.
        fixture: WorkflowQueueStateFixture = self.queue_loader.load(fixture_path)
        print(self.queue_reporter.render(fixture))

    def run_activate(self, args: Namespace) -> None:
        """Run the workflow queue activation command.

        Args:
            args: Parsed CLI namespace.
        """
        # Fixture path is the only persistent write target authorized for activation.
        fixture_path: Path = Path("dev/workflow-nets/bootstrap-harness.queue-state.json")
        # Activation result describes either a safe no-write failure or the written update.
        result: WorkflowQueueActivationResult = self.queue_activator.activate(
            fixture_path,
            args.item,
            dry_run=args.dry_run,
        )
        print(self.activation_reporter.render(result))
        if not result.success:
            raise SystemExit(1)

    def run_reconcile_status(self, args: Namespace) -> None:
        """Run the workflow status reconciliation command.

        Args:
            args: Parsed CLI namespace.
        """
        # Status fixture is the only persistent write target authorized for reconciliation.
        status_fixture_path: Path = Path("dev/workflow-nets/bootstrap-harness.workflow-net.json")
        # Queue fixture is read-only source state for reconciliation.
        queue_fixture_path: Path = Path("dev/workflow-nets/bootstrap-harness.queue-state.json")
        # Reconciliation result describes the status fixture before and after update.
        result: WorkflowStatusReconciliationResult = self.status_reconciler.reconcile(
            status_fixture_path,
            queue_fixture_path,
            dry_run=args.dry_run,
        )
        print(self.reconciliation_reporter.render(result))


def register(subparsers: SubparserCollection) -> None:
    """Register workflow commands on a parent subparser collection.

    Args:
        subparsers: Parent argparse subparser collection receiving the command group.
    """

    Command().register(subparsers)
