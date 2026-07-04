from __future__ import annotations

from dataclasses import dataclass

from projectkoios.bootstrap.python_policy.ast_rules import PolicyFinding, PythonPolicyAstValidator
from projectkoios.bootstrap.python_policy.mypy_runner import MypyResult
from projectkoios.bootstrap.python_policy.targets import ValidationTarget


@dataclass(frozen=True, slots=True)
class ValidationResult:
    findings: tuple[PolicyFinding, ...]
    mypy_result: MypyResult | None = None

    @property
    def passed(self) -> bool:
        if self.findings:
            return False
        if self.mypy_result is not None and self.mypy_result.exit_code != 0:
            return False
        return True


@dataclass(frozen=True, slots=True)
class PythonPolicyValidator:
    def validate_targets(self, targets: tuple[ValidationTarget, ...]) -> ValidationResult:
        findings: list[PolicyFinding] = []
        target: ValidationTarget
        for target in targets:
            source: str = target.path.read_text(encoding="utf-8")
            findings.extend(PythonPolicyAstValidator(path=target.path).validate_source(source))
        return ValidationResult(findings=tuple(findings))
