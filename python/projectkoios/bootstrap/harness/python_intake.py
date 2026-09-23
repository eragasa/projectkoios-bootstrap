from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tomllib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

_SCHEMA_VERSION = 1
_MANIFEST_NAMES = {"pyproject.toml", "uv.lock"}
_REQUIREMENTS_PATTERN = re.compile(r"requirements(?:-[^.]+)?\.txt\Z")
_DISTRIBUTION_NAME = re.compile(r"^[A-Za-z0-9_.-]+")
_NETWORK_IMPORTS = {"aiohttp", "httpx", "requests", "socket", "urllib"}
_PROCESS_IMPORTS = {"asyncio", "multiprocessing", "subprocess"}
_DYNAMIC_CALLS = {"__import__", "compile", "eval", "exec"}
_MUTATING_METHODS = {
    "chmod",
    "mkdir",
    "remove",
    "rename",
    "replace",
    "rmdir",
    "rmtree",
    "touch",
    "unlink",
    "write_bytes",
    "write_text",
}


class IntakeAnalysisError(ValueError):
    """Raised when an intake cannot be inspected within the declared bounds."""


@dataclass(frozen=True)
class IntakeLimits:
    max_files: int = 1_000
    max_directories: int = 1_000
    max_depth: int = 64
    max_file_bytes: int = 5_000_000
    max_total_bytes: int = 50_000_000
    max_git_output_bytes: int = 10_000_000
    git_timeout_seconds: int = 15

    def __post_init__(self) -> None:
        for name in (
            "max_files",
            "max_directories",
            "max_depth",
            "max_file_bytes",
            "max_total_bytes",
            "max_git_output_bytes",
            "git_timeout_seconds",
        ):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")

    def as_dict(self) -> dict[str, int]:
        return {
            "git_timeout_seconds": self.git_timeout_seconds,
            "max_depth": self.max_depth,
            "max_directories": self.max_directories,
            "max_file_bytes": self.max_file_bytes,
            "max_files": self.max_files,
            "max_git_output_bytes": self.max_git_output_bytes,
            "max_total_bytes": self.max_total_bytes,
        }


_DEFAULT_LIMITS = IntakeLimits()


@dataclass(frozen=True)
class _File:
    path: str
    content: bytes
    sha256: str


@dataclass(frozen=True)
class _GitChange:
    status: str
    path: str
    old_path: str | None = None

    def as_dict(self) -> dict[str, str]:
        result = {"path": self.path, "status": self.status}
        if self.old_path is not None:
            result["old_path"] = self.old_path
        return result


def analyze_python_intake(
    root: str | Path,
    *,
    limits: IntakeLimits = _DEFAULT_LIMITS,
) -> dict[str, Any]:
    """Statically inspect an intake without importing or executing its code."""
    root_path = Path(root)
    files = _read_tree(root_path, limits)
    module_names = {
        module
        for file in files
        if (module := _module_name(file.path)) is not None
    }
    available_modules = _module_prefixes(module_names)
    local_roots = {module.partition(".")[0] for module in module_names}

    python_records: list[dict[str, Any]] = []
    all_imports: set[str] = set()
    optional_imports: set[str] = set()
    all_definitions: set[str] = set()
    test_functions: list[tuple[str, str]] = []

    for file in files:
        if not file.path.endswith(".py"):
            continue
        record, imports, optional, definitions, tests = _analyze_python_file(
            file,
            module_name=_module_name(file.path),
        )
        python_records.append(record)
        all_imports.update(imports)
        optional_imports.update(optional)
        all_definitions.update(definitions)
        test_functions.extend((file.path, name) for name in tests)

    absolute_imports = {
        name
        for name in all_imports | optional_imports
        if not name.startswith(".")
    }
    import_roots = {name.partition(".")[0] for name in absolute_imports}
    external_imports = sorted(
        root_name
        for root_name in import_roots
        if root_name not in sys.stdlib_module_names
        and root_name not in local_roots
    )
    missing_local = sorted(
        name
        for name in absolute_imports
        if name.partition(".")[0] in local_roots
        and not _module_is_available(name, available_modules)
    )

    manifests = sorted(
        file.path
        for file in files
        if _is_manifest(PurePosixPath(file.path).name)
    )
    declared_dependencies, manifest_errors = _declared_dependencies(files)
    undeclared_imports = sorted(
        name
        for name in external_imports
        if _normalized_name(name)
        not in {_normalized_name(item) for item in declared_dependencies}
    )

    test_targets: dict[str, list[str]] = {}
    for path, test_name in test_functions:
        target = _test_target(test_name)
        if target is not None:
            test_targets.setdefault(target, []).append(f"{path}::{test_name}")

    file_records = [
        {
            "kind": _file_kind(file.path),
            "path": file.path,
            "sha256": file.sha256,
            "size_bytes": len(file.content),
        }
        for file in files
    ]
    total_bytes = sum(len(file.content) for file in files)
    syntax_error_count = sum(
        record["syntax_error"] is not None for record in python_records
    )
    capability_signals = sorted(
        {
            signal
            for record in python_records
            for signal in record["capability_signals"]
        }
    )

    return {
        "schema_version": _SCHEMA_VERSION,
        "analysis_kind": "python-intake-static-analysis",
        "root_label": root_path.name,
        "limits": limits.as_dict(),
        "summary": {
            "capability_signal_count": len(capability_signals),
            "file_count": len(files),
            "python_file_count": len(python_records),
            "syntax_error_count": syntax_error_count,
            "test_function_count": len(test_functions),
            "total_bytes": total_bytes,
        },
        "files": file_records,
        "python_files": sorted(python_records, key=lambda item: item["path"]),
        "dependencies": {
            "declared": sorted(declared_dependencies),
            "external_imports": external_imports,
            "manifest_errors": sorted(manifest_errors),
            "external_imports_not_declared_in_intake": undeclared_imports,
            "local_imports_not_present_in_intake": missing_local,
            "optional_imports": sorted(optional_imports),
        },
        "manifests": manifests,
        "tests": {
            "functions": [
                {"name": name, "path": path}
                for path, name in sorted(test_functions)
            ],
            "targets": [
                {
                    "definition_found": target in all_definitions,
                    "target": target,
                    "tests": sorted(names),
                }
                for target, names in sorted(test_targets.items())
            ],
        },
        "capability_signals": capability_signals,
        "validation_plan": _validation_plan(
            files,
            uses_pytest="pytest" in import_roots,
        ),
        "limitations": [
            "Static signals are review leads, not security findings.",
            "The analyzer does not import or execute intake code.",
            "Dependency names are inferred from imports and local manifests.",
            "Semantic repository ownership still requires architecture review.",
        ],
    }


def compare_intake_to_git_patch(
    root: str | Path,
    *,
    repository: str | Path,
    base_ref: str,
    head_ref: str,
    limits: IntakeLimits = _DEFAULT_LIMITS,
) -> dict[str, Any]:
    """Compare intake files with a read-only Git patch and its head blobs."""
    analysis = analyze_python_intake(root, limits=limits)
    repository_path = Path(repository)
    if not repository_path.is_dir():
        raise IntakeAnalysisError("Git repository path is not a directory")

    top_level = (
        _git(
            repository_path,
            ("rev-parse", "--show-toplevel"),
            limits=limits,
        )
        .decode("utf-8", errors="strict")
        .strip()
    )
    if Path(top_level).resolve() != repository_path.resolve():
        raise IntakeAnalysisError("repository must name the Git worktree root")
    base_commit = _resolve_commit(repository_path, base_ref, limits)
    head_commit = _resolve_commit(repository_path, head_ref, limits)
    changes = _git_changes(repository_path, base_commit, head_commit, limits)

    intake_files = {item["path"]: item for item in analysis["files"]}
    changed_paths = {change.path for change in changes}
    comparisons: list[dict[str, Any]] = []
    for path, item in sorted(intake_files.items()):
        blob = _git_blob(repository_path, head_commit, path, limits)
        if blob is None:
            status = "missing-at-head"
            head_sha256 = None
        else:
            head_sha256 = hashlib.sha256(blob).hexdigest()
            status = (
                "exact-match" if head_sha256 == item["sha256"] else "different"
            )
        comparisons.append(
            {
                "head_sha256": head_sha256,
                "in_patch": path in changed_paths,
                "path": path,
                "status": status,
            }
        )

    companion_changes = [
        change.as_dict()
        for change in changes
        if change.path not in intake_files
    ]
    return {
        "schema_version": _SCHEMA_VERSION,
        "analysis": analysis,
        "comparison": {
            "base_commit": base_commit,
            "base_ref": base_ref,
            "changes": [change.as_dict() for change in changes],
            "companion_changes_absent_from_intake": companion_changes,
            "head_commit": head_commit,
            "head_ref": head_ref,
            "intake_files": comparisons,
            "repository_label": repository_path.name,
            "summary": {
                "companion_change_count": len(companion_changes),
                "different_count": sum(
                    item["status"] == "different" for item in comparisons
                ),
                "exact_match_count": sum(
                    item["status"] == "exact-match" for item in comparisons
                ),
                "missing_at_head_count": sum(
                    item["status"] == "missing-at-head" for item in comparisons
                ),
            },
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    """Render a concise deterministic report from an analysis result."""
    analysis = report.get("analysis", report)
    summary = analysis["summary"]
    dependencies = analysis["dependencies"]
    lines = [
        "# Python intake analysis",
        "",
        f"- Root label: `{_markdown(analysis['root_label'])}`",
        f"- Files: {summary['file_count']}",
        f"- Python files: {summary['python_file_count']}",
        f"- Tests discovered: {summary['test_function_count']}",
        f"- Syntax errors: {summary['syntax_error_count']}",
        f"- Total bytes: {summary['total_bytes']}",
        "",
        "## Dependencies",
        "",
        _bullet("External imports", dependencies["external_imports"]),
        _bullet(
            "External imports not declared in intake",
            dependencies["external_imports_not_declared_in_intake"],
        ),
        _bullet(
            "Local imports not present in intake",
            dependencies["local_imports_not_present_in_intake"],
        ),
        _bullet("Manifests", analysis["manifests"]),
        "",
        "## Capability signals",
        "",
        _bullet("Signals", analysis["capability_signals"]),
        "",
        "## Test targets",
        "",
    ]
    targets = analysis["tests"]["targets"]
    if targets:
        for target in targets:
            state = "found" if target["definition_found"] else "not found"
            lines.append(
                f"- `{_markdown(target['target'])}`: definition {state}; "
                f"{len(target['tests'])} test(s)"
            )
    else:
        lines.append("- none")

    comparison = report.get("comparison")
    if comparison is not None:
        comparison_summary = comparison["summary"]
        lines.extend(
            [
                "",
                "## Git patch comparison",
                "",
                f"- Repository: `{_markdown(comparison['repository_label'])}`",
                f"- Exact matches: {comparison_summary['exact_match_count']}",
                f"- Different: {comparison_summary['different_count']}",
                "- Missing at head: "
                f"{comparison_summary['missing_at_head_count']}",
                "- Companion changes absent from intake: "
                f"{comparison_summary['companion_change_count']}",
                "",
            ]
        )
        companions = comparison["companion_changes_absent_from_intake"]
        if companions:
            for item in companions:
                lines.append(
                    f"- `{_markdown(item['status'])}` "
                    f"`{_markdown(item['path'])}`"
                )
        else:
            lines.append("- No absent companion changes detected.")

    lines.extend(
        [
            "",
            "## Validation plan",
            "",
        ]
    )
    for item in analysis["validation_plan"]:
        command = " ".join(item["argv"])
        execution = (
            "executes intake code" if item["executes_intake_code"] else "static"
        )
        lines.append(
            f"- **{_markdown(item['name'])}** ({execution}): "
            f"`{_markdown(command)}`"
        )
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            *[f"- {_markdown(item)}" for item in analysis["limitations"]],
            "",
        ]
    )
    return "\n".join(lines)


def _read_tree(root: Path, limits: IntakeLimits) -> tuple[_File, ...]:
    try:
        root_status = root.lstat()
    except OSError as error:
        raise IntakeAnalysisError("intake root is unavailable") from error
    if stat.S_ISLNK(root_status.st_mode):
        raise IntakeAnalysisError("intake root must not be a symlink")
    if not stat.S_ISDIR(root_status.st_mode):
        raise IntakeAnalysisError("intake root must be a directory")

    paths: list[Path] = []
    directory_count = 0

    def visit(directory: Path, depth: int) -> None:
        nonlocal directory_count
        if depth > limits.max_depth:
            raise IntakeAnalysisError("intake exceeds max_depth")
        directory_count += 1
        if directory_count > limits.max_directories:
            raise IntakeAnalysisError("intake exceeds max_directories")
        try:
            with os.scandir(directory) as entries:
                unordered: list[os.DirEntry[str]] = []
                for entry in entries:
                    unordered.append(entry)
                    if len(unordered) > (
                        limits.max_files + limits.max_directories
                    ):
                        raise IntakeAnalysisError(
                            "intake directory exceeds entry bounds"
                        )
                ordered = sorted(unordered, key=lambda item: item.name)
        except OSError as error:
            raise IntakeAnalysisError("cannot enumerate intake") from error
        for entry in ordered:
            path = Path(entry.path)
            if entry.is_symlink():
                raise IntakeAnalysisError(
                    f"intake contains a symlink: {_relative(root, path)}"
                )
            if entry.is_dir(follow_symlinks=False):
                visit(path, depth + 1)
            elif entry.is_file(follow_symlinks=False):
                paths.append(path)
                if len(paths) > limits.max_files:
                    raise IntakeAnalysisError("intake exceeds max_files")
            else:
                raise IntakeAnalysisError(
                    f"intake contains a non-regular entry: "
                    f"{_relative(root, path)}"
                )

    visit(root, 0)
    result: list[_File] = []
    total_bytes = 0
    for path in paths:
        relative = _relative(root, path)
        content = _read_file(path, relative, limits.max_file_bytes)
        total_bytes += len(content)
        if total_bytes > limits.max_total_bytes:
            raise IntakeAnalysisError("intake exceeds max_total_bytes")
        result.append(
            _File(
                path=relative,
                content=content,
                sha256=hashlib.sha256(content).hexdigest(),
            )
        )
    return tuple(sorted(result, key=lambda item: item.path))


def _read_file(path: Path, label: str, max_bytes: int) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise IntakeAnalysisError(
            f"cannot read intake file: {label}"
        ) from error
    try:
        file_status = os.fstat(descriptor)
        if not stat.S_ISREG(file_status.st_mode):
            raise IntakeAnalysisError(
                f"intake entry is not a regular file: {label}"
            )
        if file_status.st_size > max_bytes:
            raise IntakeAnalysisError(
                f"intake file exceeds max_file_bytes: {label}"
            )
        chunks: list[bytes] = []
        observed = 0
        while chunk := os.read(descriptor, min(1_048_576, max_bytes + 1)):
            observed += len(chunk)
            if observed > max_bytes:
                raise IntakeAnalysisError(
                    f"intake file exceeds max_file_bytes: {label}"
                )
            chunks.append(chunk)
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _analyze_python_file(
    file: _File,
    *,
    module_name: str | None,
) -> tuple[
    dict[str, Any],
    set[str],
    set[str],
    set[str],
    list[str],
]:
    try:
        tree = ast.parse(file.content, filename=file.path)
    except (SyntaxError, UnicodeDecodeError) as error:
        if isinstance(error, SyntaxError):
            line = error.lineno or 0
            offset = error.offset or 0
            detail = f"{line}:{offset}: {error.msg}"
        else:
            detail = "source encoding is invalid"
        record: dict[str, Any] = {
            "capability_signals": [],
            "definitions": [],
            "imports": [],
            "module": module_name,
            "optional_imports": [],
            "path": file.path,
            "syntax_error": detail,
            "test_functions": [],
        }
        return record, set(), set(), set(), []

    imports: set[str] = set()
    optional_imports: set[str] = set()
    definitions: set[str] = set()
    tests: list[str] = []
    signals: set[str] = set()

    for statement in tree.body:
        if isinstance(
            statement,
            (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
        ):
            definitions.add(statement.name)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * node.level
            imports.add(prefix + (node.module or ""))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("test"):
                tests.append(node.name)
        elif isinstance(node, ast.Call):
            qualified = _qualified_name(node.func)
            if qualified.endswith("importorskip") and node.args:
                first = node.args[0]
                if isinstance(first, ast.Constant) and isinstance(
                    first.value, str
                ):
                    optional_imports.add(first.value)
            if qualified in _DYNAMIC_CALLS:
                signals.add("dynamic-code-execution")
            if qualified in {"os.system", "subprocess.call", "subprocess.run"}:
                signals.add("process-execution")
            method = qualified.rpartition(".")[2]
            if method in _MUTATING_METHODS:
                signals.add("filesystem-mutation")
            if qualified == "open" and _open_mutates(node):
                signals.add("filesystem-mutation")

    roots = {name.lstrip(".").partition(".")[0] for name in imports}
    if roots & _NETWORK_IMPORTS:
        signals.add("network-capable-import")
    if roots & _PROCESS_IMPORTS:
        signals.add("process-capable-import")

    record = {
        "capability_signals": sorted(signals),
        "definitions": sorted(definitions),
        "imports": sorted(imports),
        "module": module_name,
        "optional_imports": sorted(optional_imports),
        "path": file.path,
        "syntax_error": None,
        "test_functions": sorted(tests),
    }
    return record, imports, optional_imports, definitions, tests


def _qualified_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _qualified_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return ""


def _open_mutates(node: ast.Call) -> bool:
    mode: ast.expr | None = None
    if len(node.args) >= 2:
        mode = node.args[1]
    for keyword in node.keywords:
        if keyword.arg == "mode":
            mode = keyword.value
    if isinstance(mode, ast.Constant) and isinstance(mode.value, str):
        return any(character in mode.value for character in "wax+")
    return False


def _module_name(path: str) -> str | None:
    pure = PurePosixPath(path)
    if pure.suffix != ".py":
        return None
    parts = list(pure.parts)
    start = 0
    for index in range(len(parts) - 1):
        if parts[index : index + 2] == ["src", "python"]:
            start = index + 2
            break
    else:
        if parts and parts[0] in {"tests", "test"}:
            return None
        if parts and parts[0] == "python":
            start = 1
    module_parts = parts[start:]
    module_parts[-1] = PurePosixPath(module_parts[-1]).stem
    if module_parts[-1] == "__init__":
        module_parts.pop()
    if not module_parts:
        return None
    return ".".join(module_parts)


def _module_prefixes(modules: Iterable[str]) -> set[str]:
    result: set[str] = set()
    for module in modules:
        parts = module.split(".")
        result.update(
            ".".join(parts[:index]) for index in range(1, len(parts) + 1)
        )
    return result


def _module_is_available(name: str, available: set[str]) -> bool:
    return name in available or any(
        module.startswith(name + ".") for module in available
    )


def _declared_dependencies(
    files: Sequence[_File],
) -> tuple[set[str], list[str]]:
    dependencies: set[str] = set()
    errors: list[str] = []
    for file in files:
        if PurePosixPath(file.path).name != "pyproject.toml":
            continue
        try:
            data = tomllib.loads(file.content.decode("utf-8"))
            project = data.get("project", {})
            groups: list[Any] = [project.get("dependencies", [])]
            optional = project.get("optional-dependencies", {})
            if isinstance(optional, dict):
                groups.extend(optional.values())
            for group in groups:
                if not isinstance(group, list):
                    continue
                for specification in group:
                    if not isinstance(specification, str):
                        continue
                    match = _DISTRIBUTION_NAME.match(specification.strip())
                    if match:
                        dependencies.add(match.group(0))
        except (
            UnicodeDecodeError,
            tomllib.TOMLDecodeError,
            AttributeError,
        ) as error:
            errors.append(f"{file.path}: {type(error).__name__}")
    return dependencies, errors


def _normalized_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).casefold()


def _test_target(name: str) -> str | None:
    parts = name.split("__")
    if len(parts) >= 3 and parts[1]:
        return parts[1]
    return None


def _validation_plan(
    files: Sequence[_File],
    *,
    uses_pytest: bool,
) -> list[dict[str, Any]]:
    paths = {file.path for file in files}
    python_roots: list[str] = []
    if any(path.startswith("src/python/") for path in paths):
        python_roots.append("src/python")
    elif any(path.startswith("python/") for path in paths):
        python_roots.append("python")
    test_roots = (
        ["tests"] if any(path.startswith("tests/") for path in paths) else []
    )
    targets = python_roots + test_roots
    plan: list[dict[str, Any]] = []
    if targets:
        plan.extend(
            [
                {
                    "argv": ["ruff", "check", *targets],
                    "executes_intake_code": False,
                    "name": "lint",
                },
                {
                    "argv": ["ruff", "format", "--check", *targets],
                    "executes_intake_code": False,
                    "name": "format",
                },
            ]
        )
    if python_roots:
        plan.append(
            {
                "argv": ["mypy", *python_roots],
                "executes_intake_code": False,
                "name": "type-check",
            }
        )
    if test_roots:
        test_command = (
            ["python3.14", "-m", "pytest", "-q", *test_roots]
            if uses_pytest
            else [
                "python3.14",
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-p",
                "test_*.py",
            ]
        )
        plan.append(
            {
                "argv": test_command,
                "executes_intake_code": True,
                "name": "tests",
            }
        )
    return plan


def _is_manifest(name: str) -> bool:
    return name in _MANIFEST_NAMES or bool(
        _REQUIREMENTS_PATTERN.fullmatch(name)
    )


def _file_kind(path: str) -> str:
    name = PurePosixPath(path).name
    if path.endswith(".py"):
        return "python"
    if _is_manifest(name):
        return "manifest"
    if path.startswith("tests/") or "/tests/" in path:
        return "test-resource"
    return "resource"


def _relative(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError as error:
        raise IntakeAnalysisError("entry escapes intake root") from error


def _git(
    repository: Path,
    arguments: Sequence[str],
    *,
    limits: IntakeLimits,
) -> bytes:
    try:
        environment = os.environ.copy()
        environment.update(
            {
                "GIT_OPTIONAL_LOCKS": "0",
                "GIT_PAGER": "cat",
                "LC_ALL": "C",
                "PAGER": "cat",
            }
        )
        completed = subprocess.run(
            ["git", "-C", os.fspath(repository), *arguments],
            check=False,
            capture_output=True,
            env=environment,
            timeout=limits.git_timeout_seconds,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise IntakeAnalysisError("read-only Git operation failed") from error
    if (
        len(completed.stdout) > limits.max_git_output_bytes
        or len(completed.stderr) > limits.max_git_output_bytes
    ):
        raise IntakeAnalysisError("Git output exceeds max_git_output_bytes")
    if completed.returncode != 0:
        raise IntakeAnalysisError("read-only Git operation failed")
    return completed.stdout


def _resolve_commit(
    repository: Path,
    reference: str,
    limits: IntakeLimits,
) -> str:
    if not reference or "\x00" in reference:
        raise IntakeAnalysisError("Git reference is invalid")
    return (
        _git(
            repository,
            ("rev-parse", "--verify", f"{reference}^{{commit}}"),
            limits=limits,
        )
        .decode("ascii", errors="strict")
        .strip()
    )


def _git_changes(
    repository: Path,
    base_commit: str,
    head_commit: str,
    limits: IntakeLimits,
) -> tuple[_GitChange, ...]:
    payload = _git(
        repository,
        (
            "diff",
            "--no-ext-diff",
            "--no-textconv",
            "--name-status",
            "-z",
            "-M",
            f"{base_commit}...{head_commit}",
            "--",
        ),
        limits=limits,
    )
    tokens = payload.split(b"\x00")
    if tokens and tokens[-1] == b"":
        tokens.pop()
    changes: list[_GitChange] = []
    index = 0
    try:
        while index < len(tokens):
            status_value = tokens[index].decode("utf-8", errors="strict")
            index += 1
            if status_value.startswith(("R", "C")):
                old_path = tokens[index].decode("utf-8", errors="strict")
                path = tokens[index + 1].decode("utf-8", errors="strict")
                index += 2
                changes.append(_GitChange(status_value, path, old_path))
            else:
                path = tokens[index].decode("utf-8", errors="strict")
                index += 1
                changes.append(_GitChange(status_value, path))
    except (IndexError, UnicodeDecodeError) as error:
        raise IntakeAnalysisError(
            "Git change list is not representable"
        ) from error
    return tuple(sorted(changes, key=lambda item: (item.path, item.status)))


def _git_blob(
    repository: Path,
    commit: str,
    path: str,
    limits: IntakeLimits,
) -> bytes | None:
    object_name = f"{commit}:{path}"
    try:
        size_payload = _git(
            repository,
            ("cat-file", "-s", object_name),
            limits=limits,
        )
    except IntakeAnalysisError:
        return None
    try:
        size = int(size_payload.decode("ascii", errors="strict").strip())
    except (UnicodeDecodeError, ValueError) as error:
        raise IntakeAnalysisError("Git blob size is invalid") from error
    if size > limits.max_file_bytes:
        raise IntakeAnalysisError(f"Git blob exceeds max_file_bytes: {path}")
    blob = _git(
        repository,
        ("show", object_name),
        limits=limits,
    )
    if len(blob) != size:
        raise IntakeAnalysisError("Git blob changed during inspection")
    return blob


def _markdown(value: object) -> str:
    return str(value).replace("`", "\\`").replace("\n", " ")


def _bullet(label: str, values: Sequence[object]) -> str:
    rendered = ", ".join(f"`{_markdown(value)}`" for value in values)
    return f"- {label}: {rendered or 'none'}"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Statically inspect a bounded Python intake.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        dest="output_format",
    )
    parser.add_argument("--max-files", type=int, default=1_000)
    parser.add_argument("--max-directories", type=int, default=1_000)
    parser.add_argument("--max-depth", type=int, default=64)
    parser.add_argument("--max-file-bytes", type=int, default=5_000_000)
    parser.add_argument("--max-total-bytes", type=int, default=50_000_000)
    parser.add_argument("--max-git-output-bytes", type=int, default=10_000_000)
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("root")

    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("root")
    compare_parser.add_argument("--repository", required=True)
    compare_parser.add_argument("--base-ref", required=True)
    compare_parser.add_argument("--head-ref", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        limits = IntakeLimits(
            max_files=arguments.max_files,
            max_directories=arguments.max_directories,
            max_depth=arguments.max_depth,
            max_file_bytes=arguments.max_file_bytes,
            max_total_bytes=arguments.max_total_bytes,
            max_git_output_bytes=arguments.max_git_output_bytes,
        )
        if arguments.command == "analyze":
            report = analyze_python_intake(arguments.root, limits=limits)
        else:
            report = compare_intake_to_git_patch(
                arguments.root,
                repository=arguments.repository,
                base_ref=arguments.base_ref,
                head_ref=arguments.head_ref,
                limits=limits,
            )
    except (IntakeAnalysisError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if arguments.output_format == "markdown":
        print(render_markdown(report), end="")
    else:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
