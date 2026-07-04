from __future__ import annotations

from dataclasses import dataclass

from projectkoios.bootstrap.python_policy.ast_rules import PolicyFinding, PythonPolicyAstValidator
from projectkoios.bootstrap.python_policy.mypy_runner import MypyResult
from projectkoios.bootstrap.python_policy.targets import ValidationTarget


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Combined Python policy validation result.

    Args:
        findings: AST policy findings.
        mypy_result: Optional mypy execution result.
    """

    findings: tuple[PolicyFinding, ...]
    mypy_result: MypyResult | None = None

    @property
    def passed(self) -> bool:
        """Return whether policy and type validation passed.

        Returns:
            True when there are no AST findings and mypy did not fail.
        """
        if self.findings:
            return False
        if self.mypy_result is not None and self.mypy_result.exit_code != 0:
            return False
        return True


@dataclass(frozen=True, slots=True)
class PythonPolicyValidator:
    """Validate selected Python files against AST-checkable policy rules."""

    def validate_targets(self, targets: tuple[ValidationTarget, ...]) -> ValidationResult:
        """Validate selected Python targets.

        Args:
            targets: Python file targets to validate.

        Returns:
            Combined validation result with AST findings.
        """
        # Findings are accumulated across all selected files.
        findings: list[PolicyFinding] = []
        target: ValidationTarget
        for target in targets:
            # Source text is parsed by the AST validator.
            source: str = target.path.read_text(encoding="utf-8")
            findings.extend(PythonPolicyAstValidator(path=target.path).validate_source(source))
        return ValidationResult(findings=tuple(findings))
