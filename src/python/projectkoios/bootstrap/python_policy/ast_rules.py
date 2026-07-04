from __future__ import annotations

import ast
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
import tokenize


@dataclass(frozen=True, slots=True)
class PolicyFinding:
    """A single Python policy violation.

    Args:
        path: Source file containing the finding.
        line: One-based source line.
        column: Zero-based source column.
        rule_id: Stable policy rule identifier.
        message: Human-readable finding details.
    """

    path: Path
    line: int
    column: int
    rule_id: str
    message: str

    def format(self) -> str:
        """Return the finding in command-line friendly form.

        Returns:
            Stable text containing rule, path, location, and message.
        """
        return f"{self.rule_id} {self.path}:{self.line}:{self.column} {self.message}"


@dataclass(frozen=True, slots=True)
class PythonPolicyAstValidator:
    """Validate Python source against Project Koios AST-checkable policy rules.

    Args:
        path: Source path used in findings.
    """

    path: Path

    def validate_source(self, source: str) -> tuple[PolicyFinding, ...]:
        """Validate one Python source string.

        Args:
            source: Python source text.

        Returns:
            Policy findings discovered in the source.

        Raises:
            SyntaxError: If the source cannot be parsed as Python.
        """
        # Parsed module is the root used by every AST policy rule.
        tree: ast.Module = ast.parse(source, filename=str(self.path))
        # Comment line map supports the local-variable purpose-comment rule.
        comment_lines: frozenset[int] = self.comment_lines(source)
        # Findings are accumulated in source traversal order for stable output.
        findings: list[PolicyFinding] = []
        node: ast.AST
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                findings.extend(self.validate_documented_node(node, kind="class"))
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                findings.extend(self.validate_documented_node(node, kind="function or method"))
                findings.extend(self.validate_function(node, comment_lines))
            if isinstance(node, ast.Try):
                findings.extend(self.validate_try(node))
        return tuple(findings)

    def validate_documented_node(self, node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef, *, kind: str) -> tuple[PolicyFinding, ...]:
        """Validate public class/function/method docstring presence.

        Args:
            node: Class or function node to validate.
            kind: Human-readable node kind for finding messages.

        Returns:
            A finding when a public node has no docstring.
        """
        if node.name.startswith("_"):
            return ()
        if ast.get_docstring(node) is not None:
            return ()
        return (self.finding(node, "PY-POLICY-006", f"public {kind} '{node.name}' must have a generated-docs-compatible docstring"),)

    def validate_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef, comment_lines: frozenset[int]) -> tuple[PolicyFinding, ...]:
        """Validate function return and local variable policy rules.

        Args:
            node: Function or method AST node.
            comment_lines: Source lines containing comments.

        Returns:
            Findings for return annotations, local annotations, and local comments.
        """
        # Findings are local to the current function body.
        findings: list[PolicyFinding] = []
        if node.returns is None:
            findings.append(self.finding(
                node,
                "PY-POLICY-001",
                f"function or method '{node.name}' must declare a return type",
            ))
        # Parameters count as already introduced names for reassignment checks.
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
            findings.extend(self.validate_node(child, annotated_names, comment_lines))
        return tuple(findings)

    def function_body_nodes(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[ast.AST, ...]:
        """Return nodes in a function body without descending into nested scopes.

        Args:
            node: Function or method AST node.

        Returns:
            Body nodes belonging to the function's own scope.
        """
        # Nodes are traversed with an explicit stack so nested scopes can be skipped.
        nodes: list[ast.AST] = []
        # Stack preserves source order while avoiding recursion.
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

    def validate_node(self, node: ast.AST, annotated_names: set[str], comment_lines: frozenset[int]) -> tuple[PolicyFinding, ...]:
        """Validate local variable rules for one function-body AST node.

        Args:
            node: Function-body AST node.
            annotated_names: Names with known local annotations.
            comment_lines: Source lines containing comments.

        Returns:
            Findings for the node.
        """
        # Findings from one AST node are returned as an immutable tuple.
        findings: list[PolicyFinding] = []
        if isinstance(node, ast.AnnAssign):
            # Annotated targets introduce local names and must carry comments.
            target_names: tuple[str, ...] = self.target_names(node.target)
            name: str
            for name in target_names:
                annotated_names.add(name)
            if self.annotation_contains_any(node.annotation):
                findings.append(self.finding(node, "PY-POLICY-003", "local variable annotation must not use Any"))
            if target_names and node.value is not None and not self.has_nearby_comment(node, comment_lines):
                findings.append(self.finding(node, "PY-POLICY-005", f"local variable '{target_names[0]}' must have a nearby purpose comment"))
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

    def validate_try(self, node: ast.Try) -> tuple[PolicyFinding, ...]:
        """Validate error handling policy for broad generic returns.

        Args:
            node: Try statement to inspect.

        Returns:
            Findings for handlers that hide errors with generic return values.
        """
        # Findings identify exception handlers that hide errors behind sentinel values.
        findings: list[PolicyFinding] = []
        handler: ast.ExceptHandler
        for handler in node.handlers:
            statement: ast.stmt
            for statement in handler.body:
                if isinstance(statement, ast.Return) and self.is_generic_error_return(statement.value):
                    findings.append(self.finding(statement, "PY-POLICY-007", "except block must not hide errors by returning None, False, or an empty collection"))
        return tuple(findings)

    def find_unannotated_targets(self, target: ast.expr, annotated_names: set[str]) -> tuple[PolicyFinding, ...]:
        """Find target names introduced without prior annotations.

        Args:
            target: Assignment-like target.
            annotated_names: Names with known annotations.

        Returns:
            Findings for unannotated names.
        """
        # Findings are emitted for each unannotated target name.
        findings: list[PolicyFinding] = []
        name: str
        for name in self.target_names(target):
            if name not in annotated_names:
                findings.append(self.finding(target, "PY-POLICY-002", f"local variable '{name}' must have an explicit annotation"))
        return tuple(findings)

    def target_names(self, target: ast.expr) -> tuple[str, ...]:
        """Return local names introduced by an assignment target.

        Args:
            target: Assignment-like target.

        Returns:
            Names contained in the target.
        """
        if isinstance(target, ast.Name):
            return (target.id,)
        if isinstance(target, ast.Tuple | ast.List):
            # Destructuring targets may introduce multiple local names.
            names: list[str] = []
            element: ast.expr
            for element in target.elts:
                names.extend(self.target_names(element))
            return tuple(names)
        return ()

    def annotation_contains_any(self, annotation: ast.expr) -> bool:
        """Return whether an annotation contains direct or nested Any.

        Args:
            annotation: Annotation AST node.

        Returns:
            True when `Any` appears in the annotation.
        """
        node: ast.AST
        for node in ast.walk(annotation):
            if isinstance(node, ast.Name) and node.id == "Any":
                return True
            if isinstance(node, ast.Attribute) and node.attr == "Any":
                return True
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and "Any" in node.value:
                return True
        return False

    def has_nearby_comment(self, node: ast.AST, comment_lines: frozenset[int]) -> bool:
        """Return whether a node has a same-line or previous-line comment.

        Args:
            node: AST node for a local variable introduction.
            comment_lines: Source lines containing comments.

        Returns:
            True when a nearby purpose comment exists.
        """
        # Local comments may be inline or directly above the variable.
        line: int = getattr(node, "lineno", 1)
        return line in comment_lines or (line - 1) in comment_lines

    def is_generic_error_return(self, value: ast.expr | None) -> bool:
        """Return whether an exception handler returns a generic sentinel.

        Args:
            value: Return value expression.

        Returns:
            True for None, False, or empty collection returns.
        """
        if value is None:
            return True
        if isinstance(value, ast.Constant) and value.value in (None, False):
            return True
        if isinstance(value, ast.List | ast.Tuple | ast.Set | ast.Dict) and len(value.elts if not isinstance(value, ast.Dict) else value.keys) == 0:
            return True
        return False

    def comment_lines(self, source: str) -> frozenset[int]:
        """Return source lines that contain comments.

        Args:
            source: Python source text.

        Returns:
            One-based line numbers containing comments.
        """
        # Tokenization identifies inline comments without relying on regex parsing.
        lines: set[int] = set()
        token: tokenize.TokenInfo
        for token in tokenize.generate_tokens(StringIO(source).readline):
            if token.type == tokenize.COMMENT:
                lines.add(token.start[0])
        return frozenset(lines)

    def finding(self, node: ast.AST, rule_id: str, message: str) -> PolicyFinding:
        """Build a finding from an AST node location.

        Args:
            node: AST node carrying source location.
            rule_id: Stable rule identifier.
            message: Human-readable finding details.

        Returns:
            Policy finding with source location.
        """
        # AST line and column attributes are absent on synthetic nodes only.
        line: int = getattr(node, "lineno", 1)
        # Columns are zero-based to match Python AST conventions.
        column: int = getattr(node, "col_offset", 0)
        return PolicyFinding(path=self.path, line=line, column=column, rule_id=rule_id, message=message)
