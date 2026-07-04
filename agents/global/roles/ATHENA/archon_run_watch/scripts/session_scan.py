"""Scan handoff directories and summarize current session state."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from collections import defaultdict
from pathlib import Path
from typing import Any
import subprocess

from projectkoios.bootstrap.harness.headers import extract_handoff_headers
from _utils import write_json


HANDOFF_DIRS: list[tuple[str, Path]] = [
    ("archon", Path("archon") / "handoffs"),
    ("opencode", Path("opencode") / "handoffs"),
    ("pi", Path("pi") / "handoffs"),
    ("goose", Path("goose") / "handoffs"),
]

REQUIRED_HEADERS: frozenset[str] = frozenset({"Origin", "Created", "From", "To", "Status"})


def scan_handoff_dir(dir_path: Path, root: Path | None = None) -> list[dict[str, Any]]:
    """Parse all handoff files in *dir_path* and return their headers."""
    results: list[dict[str, Any]] = []
    if not dir_path.exists():
        return results
    path: Path
    for path in sorted(dir_path.iterdir()):
        if not path.is_file() or path.suffix != ".md":
            continue
        text: str = path.read_text(encoding="utf-8")
        headers: dict[str, str] = extract_handoff_headers(text)
        if headers:
            entry: dict[str, Any] = dict(headers)
            entry["_path"] = str(path.relative_to(root)) if root else str(path)
            results.append(entry)
    return results


def get_git_summary() -> dict[str, str]:
    """Return current git branch and status, or empty dict if not a git repo."""
    try:
        branch: str = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        status_text: str = subprocess.run(
            ["git", "status", "--short", "--branch"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return {"branch": branch, "status": status_text}
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}


def build_summary(root: Path) -> dict[str, Any]:
    """Build a complete session-state summary."""
    summary: dict[str, Any] = {}
    git_summary: dict[str, str] = get_git_summary()
    if git_summary:
        summary["git"] = git_summary

    total_files: int = 0
    files_with_warnings: int = 0
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)

    harness_name: str
    rel_path: Path
    for harness_name, rel_path in HANDOFF_DIRS:
        full_path: Path = root / rel_path
        entries: list[dict[str, Any]] = scan_handoff_dir(full_path, root=root)
        entry: dict[str, Any]
        for entry in entries:
            status: str = str(entry.get("Status", "unknown"))
            groups[status].append(entry)
            total_files += 1
            missing: frozenset[str] = REQUIRED_HEADERS - set(entry)
            if missing:
                files_with_warnings += 1
                entry["_warnings"] = sorted(missing)

    summary["files"] = {
        "total": total_files,
        "with_missing_headers": files_with_warnings,
    }
    summary["by_status"] = {
        status: len(entries) for status, entries in sorted(groups.items())
    }
    summary["entries"] = dict(groups)

    return summary


def format_text(summary: dict[str, Any]) -> str:
    """Render summary as human-readable text."""
    lines: list[str] = []

    if "git" in summary:
        git_summary: dict[str, Any] = summary["git"]
        lines.append(f"branch: {git_summary.get('branch', '?')}")
        status_text: str = str(git_summary.get("status", ""))
        if status_text:
            line: str
            for line in status_text.splitlines():
                lines.append(f"  {line}")
        lines.append("")

    files_summary: dict[str, Any] = summary["files"]
    lines.append(f"handoff files: {files_summary['total']} total, {files_summary['with_missing_headers']} with missing headers")
    lines.append("")

    status: str
    count: int
    for status, count in summary.get("by_status", {}).items():
        lines.append(f"  {status}: {count}")
    lines.append("")

    entries_by_status: dict[str, list[dict[str, Any]]] = summary.get("entries", {})
    entries: list[dict[str, Any]]
    for status, entries in entries_by_status.items():
        entry: dict[str, Any]
        for entry in entries:
            entry_path: object = entry.get("_path", "?")
            warnings: object = entry.get("_warnings")
            parts: list[str] = [str(entry_path)]
            key: str
            for key in ("Origin", "From", "To", "Status"):
                value: object = entry.get(key)
                if value:
                    parts.append(f"{key}={value}")
            if isinstance(warnings, list):
                parts.append(f"missing={','.join(str(warning) for warning in warnings)}")
            lines.append("  " + " | ".join(parts))

    return "\n".join(lines)


def main() -> None:
    parser: ArgumentParser = ArgumentParser(description="Scan handoff directories and print session-state summary")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root (default: cwd)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args: Namespace = parser.parse_args()

    root: Path = args.root.resolve()
    summary: dict[str, Any] = build_summary(root)

    if args.json:
        write_json(summary, default=str)
    else:
        print(format_text(summary))


if __name__ == "__main__":
    main()
