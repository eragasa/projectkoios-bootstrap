from __future__ import annotations

from dataclasses import dataclass

from projectkoios.workflow.model import Arc, WorkflowNet


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """Workflow validation issue."""

    code: str
    message: str


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Result of validating a workflow net."""

    issues: tuple[ValidationIssue, ...] = ()

    @property
    def is_valid(self) -> bool:
        """Return whether validation reported no issues."""

        return not self.issues


class WorkflowValidationError(ValueError):
    """Raised when a workflow net fails validation."""


class WorkflowValidator:
    """Validate canonical workflow net definitions before execution."""

    def validate(self, net: WorkflowNet) -> ValidationResult:
        """Validate a workflow net.

        Args:
            net: Workflow net to validate.

        Returns:
            Validation result with deterministic issues.
        """

        # Issues accumulate schema and reference failures for one deterministic report.
        issues: list[ValidationIssue] = []
        self.add_duplicate_issues("place", [place.place_id for place in net.places], issues)
        self.add_duplicate_issues("transition", [transition.transition_id for transition in net.transitions], issues)

        # Declared identifiers are used to validate every arc endpoint.
        place_ids: set[str] = net.place_ids()
        # Declared transition identifiers are used to validate every arc endpoint.
        transition_ids: set[str] = net.transition_ids()
        arc: Arc
        for arc in net.arcs:
            if arc.place_id not in place_ids:
                issues.append(ValidationIssue(code="unknown-place", message=f"unknown place: {arc.place_id}"))
            if arc.transition_id not in transition_ids:
                issues.append(
                    ValidationIssue(code="unknown-transition", message=f"unknown transition: {arc.transition_id}")
                )
            if arc.weight < 1:
                issues.append(ValidationIssue(code="invalid-arc-weight", message="arc weight must be >= 1"))

        return ValidationResult(issues=tuple(issues))

    def validate_or_raise(self, net: WorkflowNet) -> None:
        """Raise a validation error when a workflow net is invalid.

        Args:
            net: Workflow net to validate.

        Raises:
            WorkflowValidationError: When validation issues are present.
        """

        # Result contains all deterministic validation issues for error reporting.
        result: ValidationResult = self.validate(net)
        if result.is_valid:
            return
        # Message combines issue codes and messages for concise caller diagnostics.
        message: str = "; ".join(f"{issue.code}: {issue.message}" for issue in result.issues)
        raise WorkflowValidationError(message)

    def add_duplicate_issues(self, kind: str, identifiers: list[str], issues: list[ValidationIssue]) -> None:
        """Append duplicate identifier issues.

        Args:
            kind: Human-readable identifier kind.
            identifiers: Identifiers to inspect.
            issues: Mutable issue accumulator.
        """

        # Seen identifiers detect duplicate declarations while preserving input order.
        seen: set[str] = set()
        identifier: str
        for identifier in identifiers:
            if identifier in seen:
                issues.append(ValidationIssue(code=f"duplicate-{kind}", message=f"duplicate {kind}: {identifier}"))
            seen.add(identifier)
