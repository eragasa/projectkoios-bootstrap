from __future__ import annotations

from argparse import Namespace
from pathlib import Path

import pytest

from projectkoios.bootstrap.commands import validate_python_policy


def test_run_exits_zero_for_policy_compliant_source(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Validate that the command exits successfully for compliant Python source."""
    # Source file contains a documented public function with return and local annotations.
    source_path: Path = tmp_path / "good.py"
    source_path.write_text(
        'def example() -> int:\n'
        '    """Return an example value."""\n'
        '    # Value exists to exercise the local annotation rule.\n'
        '    value: int = 1\n'
        '    return value\n',
        encoding="utf-8",
    )
    # Args mirror argparse output for an explicit path validation run.
    args: Namespace = Namespace(root=tmp_path, paths=(source_path,), all=False, changed=False)

    # Exit info captures the command's SystemExit for status assertions.
    exit_info: pytest.ExceptionInfo[SystemExit]
    with pytest.raises(SystemExit) as exit_info:
        validate_python_policy.run(args)

    assert exit_info.value.code == 0
    assert capsys.readouterr().out == "summary: 0 finding(s), 1 file(s)\n"


def test_run_exits_one_and_prints_findings_for_policy_violations(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Validate that the command reports findings and exits non-zero."""
    # Source file intentionally omits a return annotation and public docstring.
    source_path: Path = tmp_path / "bad.py"
    source_path.write_text("def example():\n    return 1\n", encoding="utf-8")
    # Args mirror argparse output for an explicit path validation run.
    args: Namespace = Namespace(root=tmp_path, paths=(source_path,), all=False, changed=False)

    # Exit info captures the command's SystemExit for status assertions.
    exit_info: pytest.ExceptionInfo[SystemExit]
    with pytest.raises(SystemExit) as exit_info:
        validate_python_policy.run(args)

    # Output should expose stable policy identifiers for CLI consumers.
    output: str = capsys.readouterr().out
    assert exit_info.value.code == 1
    assert "PY-POLICY-001" in output
    assert "PY-POLICY-006" in output
    assert "summary: 2 finding(s), 1 file(s)" in output
