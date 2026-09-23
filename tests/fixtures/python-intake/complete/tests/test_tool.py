from __future__ import annotations

import pytest
from example.tool import ExampleTool

pytest.importorskip("optional_backend")


def test__ExampleTool__encodes_deterministically() -> None:
    assert ExampleTool().encode({"b": 2, "a": 1}) == '{"a": 1, "b": 2}'
