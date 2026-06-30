"""Scan handoff directories and summarize current session state."""

from __future__ import annotations

from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
import json
import subprocess
import sys

from projectkoios.bootstrap.harness.headers import extract_handoff_headers


HANDOFF_DIRS: list[tuple[str, Path]] = [
    ("archon", Path("archon") / "handoffs"),
    ("opencode", Path("opencode") / "handoffs"),
    ("pi", Path("pi") / "handoffs"),
    ("goose", Path("goose") / "handoffs"),
]

REQUIRED_HEADERS = frozenset({"Origin", "Created", "From", "To", "Status"})


def scan_handoff_dir(dir_path: Path, root: Path | None = None) -> list[dict[str, str]]:
    """Parse all handoff files in *dir_path* and return their headers.

    When *root* is provided, ``_path`` is resolved relative to *root*.
    Otherwise ``_path`` is the absolute path as a string.
    """
    results: list[dict[str, str]] = []
    if not dir_path.exists():
        return results
    for path in sorted(dir_path.iterdir()):
        if not path.is_file() or path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        headers = extract_handoff_headers(text)
        if headers:
            if root:
                headers["_path"] = str(path.relative_to(root))
            else:
                headers["_path"] = str(path)
            results.append(headers)
    return results


def get_git_summary() -> dict[str, str]:
    """Return current git branch and status, or empty dict if not a git repo."""
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        status_text = subprocess.run(
            ["git", "status", "--short", "--branch"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return {"branch": branch, "status": status_text}
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}


def build_summary(root: Path) -> dict:
    """Build a complete session-state summary."""
    summary: dict = {}
    git = get_git_summary()
    if git:
        summary["git"] = git

    total_files = 0
    files_with_warnings = 0
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)

    for harness_name, rel_path in HANDOFF_DIRS:
        full_path = root / rel_path
        entries = scan_handoff_dir(full_path, root=root)
        for entry in entries:
            status = entry.get("Status", "unknown")
            groups[status].append(entry)
            total_files += 1
            missing = REQUIRED_HEADERS - set(entry)
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


def format_text(summary: dict) -> str:
    """Render summary as human-readable text."""
    lines: list[str] = []

    if "git" in summary:
        g = summary["git"]
        lines.append(f"branch: {g.get('branch', '?')}")
        status = g.get("status", "")
        if status:
            for line in status.splitlines():
                lines.append(f"  {line}")
        lines.append("")

    f = summary["files"]
    lines.append(f"handoff files: {f['total']} total, {f['with_missing_headers']} with missing headers")
    lines.append("")

    for status, count in summary.get("by_status", {}).items():
        lines.append(f"  {status}: {count}")
    lines.append("")

    for status, entries in summary.get("entries", {}).items():
        for e in entries:
            path = e.pop("_path", "?")
            warnings = e.pop("_warnings", None)
            parts = [path]
            for key in ("Origin", "From", "To", "Status"):
                v = e.get(key)
                if v:
                    parts.append(f"{key}={v}")
            if warnings:
                parts.append(f"missing={','.join(warnings)}")
            lines.append("  " + " | ".join(parts))

    return "\n".join(lines)


def main() -> None:
    p = ArgumentParser(description="Scan handoff directories and print session-state summary")
    p.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root (default: cwd)")
    p.add_argument("--json", action="store_true", help="Output JSON")
    args = p.parse_args()

    root = args.root.resolve()
    summary = build_summary(root)

    if args.json:
        json.dump(summary, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
    else:
        print(format_text(summary))


if __name__ == "__main__":
    main()
