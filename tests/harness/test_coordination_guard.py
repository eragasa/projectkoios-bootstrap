from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

_REPOSITORY = Path(__file__).parents[2]


def test_coordination_guard_with_node() -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is required to execute Pi extension tests")

    result = subprocess.run(
        [
            node,
            "--test",
            str(_REPOSITORY / "tests/harness/coordination_guard.test.mjs"),
        ],
        cwd=_REPOSITORY,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr
