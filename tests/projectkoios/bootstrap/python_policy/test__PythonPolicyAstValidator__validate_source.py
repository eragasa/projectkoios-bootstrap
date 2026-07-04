from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.python_policy import PythonPolicyAstValidator


def findings_for(source: str) -> tuple[str, ...]:
    findings = PythonPolicyAstValidator(path=Path("example.py")).validate_source(source)
    return tuple(finding.rule_id for finding in findings)


def test__PythonPolicyAstValidator__validate_source__accepts_annotated_locals_and_return():
    source = """
def valid() -> int:
    value: int = 1
    value = 2
    return value
"""
    assert findings_for(source) == ()


def test__PythonPolicyAstValidator__validate_source__rejects_missing_return_annotation():
    source = """
def invalid():
    value: int = 1
    return value
"""
    assert findings_for(source) == ("PY-POLICY-001",)


def test__PythonPolicyAstValidator__validate_source__rejects_plain_local_assignment_without_prior_annotation():
    source = """
def invalid() -> int:
    value = 1
    return value
"""
    assert findings_for(source) == ("PY-POLICY-002",)


def test__PythonPolicyAstValidator__validate_source__rejects_loop_target_without_prior_annotation():
    source = """
def invalid(values: tuple[int, ...]) -> int:
    total: int = 0
    for value in values:
        total += value
    return total
"""
    assert "PY-POLICY-002" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__accepts_loop_target_with_prior_annotation():
    source = """
def valid(values: tuple[int, ...]) -> int:
    total: int = 0
    value: int
    for value in values:
        total += value
    return total
"""
    assert findings_for(source) == ()


def test__PythonPolicyAstValidator__validate_source__rejects_with_target_without_prior_annotation():
    source = """
def invalid(path: str) -> str:
    with open(path) as handle:
        return handle.read()
"""
    assert "PY-POLICY-002" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_exception_alias_without_prior_annotation():
    source = """
def invalid() -> str:
    try:
        raise ValueError('bad')
    except ValueError as error:
        return str(error)
"""
    assert "PY-POLICY-002" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_assignment_expression_without_prior_annotation():
    source = """
def invalid(values: tuple[int, ...]) -> int:
    if (count := len(values)) > 0:
        return count
    return 0
"""
    assert "PY-POLICY-002" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_direct_any_annotation():
    source = """
from typing import Any

def invalid() -> None:
    value: Any = None
"""
    assert findings_for(source) == ("PY-POLICY-003",)


def test__PythonPolicyAstValidator__validate_source__rejects_typing_any_annotation():
    source = """
import typing

def invalid() -> None:
    value: typing.Any = None
"""
    assert findings_for(source) == ("PY-POLICY-003",)


def test__PythonPolicyAstValidator__validate_source__rejects_nested_any_annotation():
    source = """
from typing import Any

def invalid() -> None:
    value: dict[str, Any] = {}
"""
    assert findings_for(source) == ("PY-POLICY-003",)


def test__PythonPolicyAstValidator__validate_source__validates_nested_function_independently():
    source = """
def valid() -> int:
    value: int = 1
    def nested() -> int:
        nested_value = 2
        return nested_value
    return value
"""
    assert findings_for(source) == ("PY-POLICY-002",)
