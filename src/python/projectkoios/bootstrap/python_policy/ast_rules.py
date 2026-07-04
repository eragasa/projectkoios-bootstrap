from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PolicyFinding:
    path: Path
    line: int
    column: int
    rule_id: str
    message: str

    def format(self) -> str:
        return f"{self.rule_id} {self.path}:{self.line}:{self.column} {self.message}"


@dataclass(frozen=True, slots=True)
class PythonPolicyAstValidator:
    path: Path

    def validate_source(self, source: str) -> tuple[PolicyFinding, ...]:
        tree: ast.Module = ast.parse(source, filename=str(self.path))
        findings: list[PolicyFinding] = []
        node: ast.AST
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                findings.extend(self.validate_function(node))
        return tuple(findings)

    def validate_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[PolicyFinding, ...]:
        findings: list[PolicyFinding] = []
        if node.returns is None:
            findings.append(self.finding(
                node,
                "PY-POLICY-001",
                f"function or method '{node.name}' must declare a return type",
            ))
        annotated_names: set[str] = set()
        argument: ast.arg
        for argument in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
            annotated_names.add(argument.arg)
        if node.args.vararg is not None:
            annotated_names.add(node.args.vararg.arg)
        if node.args.kwarg is not None:
            annotated_names.add(node.args.kwarg.arg)
        child: ast.AST
        for child in self.function_body_nodes(node):
            findings.extend(self.validate_node(child, annotated_names))
        return tuple(findings)

    def function_body_nodes(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[ast.AST, ...]:
        nodes: list[ast.AST] = []
        stack: list[ast.AST] = list(reversed(node.body))
        current: ast.AST
        child: ast.AST
        while stack:
            current = stack.pop()
            if isinstance(current, ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda | ast.ClassDef):
                continue
            nodes.append(current)
            for child in reversed(tuple(ast.iter_child_nodes(current))):
                stack.append(child)
        return tuple(nodes)

    def validate_node(self, node: ast.AST, annotated_names: set[str]) -> tuple[PolicyFinding, ...]:
        findings: list[PolicyFinding] = []
        if isinstance(node, ast.AnnAssign):
            target_names: tuple[str, ...] = self.target_names(node.target)
            name: str
            for name in target_names:
                annotated_names.add(name)
            if self.annotation_contains_any(node.annotation):
                findings.append(self.finding(node, "PY-POLICY-003", "local variable annotation must not use Any"))
            return tuple(findings)
        if isinstance(node, ast.Assign):
            target: ast.expr
            for target in node.targets:
                findings.extend(self.find_unannotated_targets(target, annotated_names))
            return tuple(findings)
        if isinstance(node, ast.AugAssign):
            findings.extend(self.find_unannotated_targets(node.target, annotated_names))
            return tuple(findings)
        if isinstance(node, ast.For | ast.AsyncFor):
            findings.extend(self.find_unannotated_targets(node.target, annotated_names))
            return tuple(findings)
        if isinstance(node, ast.With | ast.AsyncWith):
            item: ast.withitem
            for item in node.items:
                if item.optional_vars is not None:
                    findings.extend(self.find_unannotated_targets(item.optional_vars, annotated_names))
            return tuple(findings)
        if isinstance(node, ast.ExceptHandler):
            if node.name is not None and node.name not in annotated_names:
                findings.append(self.finding(node, "PY-POLICY-002", f"local variable '{node.name}' must have an explicit annotation"))
            return tuple(findings)
        if isinstance(node, ast.NamedExpr):
            findings.extend(self.find_unannotated_targets(node.target, annotated_names))
            return tuple(findings)
        return ()

    def find_unannotated_targets(self, target: ast.expr, annotated_names: set[str]) -> tuple[PolicyFinding, ...]:
        findings: list[PolicyFinding] = []
        name: str
        for name in self.target_names(target):
            if name not in annotated_names:
                findings.append(self.finding(target, "PY-POLICY-002", f"local variable '{name}' must have an explicit annotation"))
        return tuple(findings)

    def target_names(self, target: ast.expr) -> tuple[str, ...]:
        if isinstance(target, ast.Name):
            return (target.id,)
        if isinstance(target, ast.Tuple | ast.List):
            names: list[str] = []
            element: ast.expr
            for element in target.elts:
                names.extend(self.target_names(element))
            return tuple(names)
        return ()

    def annotation_contains_any(self, annotation: ast.expr) -> bool:
        node: ast.AST
        for node in ast.walk(annotation):
            if isinstance(node, ast.Name) and node.id == "Any":
                return True
            if isinstance(node, ast.Attribute) and node.attr == "Any":
                return True
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and "Any" in node.value:
                return True
        return False

    def finding(self, node: ast.AST, rule_id: str, message: str) -> PolicyFinding:
        line: int = getattr(node, "lineno", 1)
        column: int = getattr(node, "col_offset", 0)
        return PolicyFinding(path=self.path, line=line, column=column, rule_id=rule_id, message=message)
