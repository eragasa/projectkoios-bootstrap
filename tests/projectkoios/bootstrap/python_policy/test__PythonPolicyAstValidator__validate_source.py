from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.python_policy import PolicyFinding, PythonPolicyAstValidator


def findings_for(source: str) -> tuple[str, ...]:
    """Return policy rule identifiers for one source snippet."""
    # Findings are produced by the AST validator for a synthetic source path.
    findings: tuple[PolicyFinding, ...] = PythonPolicyAstValidator(path=Path("example.py")).validate_source(source)
    return tuple(finding.rule_id for finding in findings)


def test__PythonPolicyAstValidator__validate_source__accepts_documented_annotated_locals_and_return() -> None:
    """Validate that fully documented and annotated source passes."""
    # Source exercises the valid local annotation and return annotation path.
    source: str = '''
def valid() -> int:
    """Return a documented value.

    Returns:
        Integer value.
    """
    # Value returned by the function.
    value: int = 1
    value = 2
    return value
'''
    assert findings_for(source) == ()


def test__PythonPolicyAstValidator__validate_source__rejects_missing_return_annotation() -> None:
    """Validate that missing return annotations are reported."""
    # Source intentionally omits the function return annotation.
    source: str = '''
def invalid():
    """Return a value."""
    # Value returned by the function.
    value: int = 1
    return value
'''
    assert "PY-POLICY-001" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_plain_local_assignment_without_prior_annotation() -> None:
    """Validate that first local assignments require annotations."""
    # Source introduces a local name through plain assignment.
    source: str = '''
def invalid() -> int:
    """Return a value.

    Returns:
        Integer value.
    """
    value = 1
    return value
'''
    assert "PY-POLICY-002" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_annotated_local_without_comment() -> None:
    """Validate that annotated locals require nearby purpose comments."""
    # Source omits a nearby comment for an annotated local value.
    source: str = '''
def invalid() -> int:
    """Return a value.

    Returns:
        Integer value.
    """
    value: int = 1
    return value
'''
    assert "PY-POLICY-005" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_loop_target_without_prior_annotation() -> None:
    """Validate that loop targets require prior annotations."""
    # Source introduces a loop target without prior annotation.
    source: str = '''
def invalid(values: tuple[int, ...]) -> int:
    """Sum values.

    Args:
        values: Values to sum.

    Returns:
        Sum of values.
    """
    # Running total.
    total: int = 0
    for value in values:
        total += value
    return total
'''
    assert "PY-POLICY-002" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__accepts_loop_target_with_prior_annotation() -> None:
    """Validate that prior annotations satisfy loop target policy."""
    # Source annotates the loop target before the loop statement.
    source: str = '''
def valid(values: tuple[int, ...]) -> int:
    """Sum values.

    Args:
        values: Values to sum.

    Returns:
        Sum of values.
    """
    # Running total.
    total: int = 0
    # Current loop value.
    value: int
    for value in values:
        total += value
    return total
'''
    assert findings_for(source) == ()


def test__PythonPolicyAstValidator__validate_source__rejects_with_target_without_prior_annotation() -> None:
    """Validate that context-manager targets require annotations."""
    # Source introduces a with-statement target without prior annotation.
    source: str = '''
def invalid(path: str) -> str:
    """Read a file.

    Args:
        path: File path.

    Returns:
        File content.
    """
    with open(path) as handle:
        return handle.read()
'''
    assert "PY-POLICY-002" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_exception_alias_without_prior_annotation() -> None:
    """Validate that exception aliases require annotations."""
    # Source introduces an exception alias without prior annotation.
    source: str = '''
def invalid() -> str:
    """Return an error string.

    Returns:
        Error text.
    """
    try:
        raise ValueError('bad')
    except ValueError as error:
        return str(error)
'''
    assert "PY-POLICY-002" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_assignment_expression_without_prior_annotation() -> None:
    """Validate that assignment expressions require prior annotations."""
    # Source introduces a walrus target without prior annotation.
    source: str = '''
def invalid(values: tuple[int, ...]) -> int:
    """Return count.

    Args:
        values: Values to count.

    Returns:
        Count of values.
    """
    if (count := len(values)) > 0:
        return count
    return 0
'''
    assert "PY-POLICY-002" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_direct_any_annotation() -> None:
    """Validate that direct Any annotations are rejected."""
    # Source uses direct Any in a local annotation.
    source: str = '''
from typing import Any

def invalid() -> None:
    """Set a value."""
    # Value under test.
    value: Any = None
'''
    assert "PY-POLICY-003" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_typing_any_annotation() -> None:
    """Validate that typing.Any annotations are rejected."""
    # Source uses typing.Any in a local annotation.
    source: str = '''
import typing

def invalid() -> None:
    """Set a value."""
    # Value under test.
    value: typing.Any = None
'''
    assert "PY-POLICY-003" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_nested_any_annotation() -> None:
    """Validate that nested Any annotations are rejected."""
    # Source uses nested Any in a parameterized local annotation.
    source: str = '''
from typing import Any

def invalid() -> None:
    """Set a value."""
    # Value under test.
    value: dict[str, Any] = {}
'''
    assert "PY-POLICY-003" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__validates_nested_function_independently() -> None:
    """Validate that nested functions are checked as independent scopes."""
    # Source includes a nested function with an unannotated local introduction.
    source: str = '''
def valid() -> int:
    """Return a value.

    Returns:
        Integer value.
    """
    # Outer value.
    value: int = 1
    def nested() -> int:
        """Return nested value.

        Returns:
            Integer value.
        """
        nested_value = 2
        return nested_value
    return value
'''
    assert "PY-POLICY-002" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_missing_public_docstring() -> None:
    """Validate that public functions require docstrings."""
    # Source omits a public function docstring.
    source: str = '''
def invalid() -> None:
    # Local value.
    value: int = 1
'''
    assert "PY-POLICY-006" in findings_for(source)


def test__PythonPolicyAstValidator__validate_source__rejects_except_return_none() -> None:
    """Validate that broad error handlers cannot hide errors with None."""
    # Source returns None from an exception handler.
    source: str = '''
def invalid() -> int | None:
    """Return a value or fail badly.

    Returns:
        Integer value or None.
    """
    try:
        # Value under test.
        value: int = 1
        return value
    except ValueError:
        return None
'''
    assert "PY-POLICY-007" in findings_for(source)
