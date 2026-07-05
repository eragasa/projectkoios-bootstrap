from __future__ import annotations

import ast
from pathlib import Path

from projectkoios.workflow import Arc, ArcKind, Place, Transition, ValidationResult, WorkflowNet, WorkflowValidator


def test__WorkflowValidator__validate__rejects_unknown_arc_endpoints() -> None:
    """Validate workflow validation rejects unknown arc endpoints."""
    # Net fixture references an unknown place and transition from one arc.
    net: WorkflowNet = WorkflowNet(
        places=(Place("known"),),
        transitions=(Transition("known-transition"),),
        arcs=(Arc(place_id="missing", transition_id="missing-transition", kind=ArcKind.INPUT),),
    )

    # Result contains deterministic endpoint validation issues.
    result: ValidationResult = WorkflowValidator().validate(net)

    assert [issue.code for issue in result.issues] == ["unknown-place", "unknown-transition"]


def test__WorkflowAdapters__source__does_not_import_third_party_libraries() -> None:
    """Validate adapter boundary avoids direct third-party Petri-net imports."""
    # Adapter source path is inspected for import-boundary enforcement.
    source_path: Path = Path("src/python/projectkoios/workflow/adapters.py")
    # Parsed syntax tree exposes imports without executing adapter code.
    tree: ast.Module = ast.parse(source_path.read_text(encoding="utf-8"))

    # Imported module names are collected for boundary assertions.
    imported_modules: list[str] = []
    statement: ast.stmt
    for statement in tree.body:
        if isinstance(statement, ast.Import):
            imported_modules.extend(alias.name for alias in statement.names)
        if isinstance(statement, ast.ImportFrom) and statement.module is not None:
            imported_modules.append(statement.module)

    assert "snakes" not in imported_modules
    assert "pm4py" not in imported_modules
