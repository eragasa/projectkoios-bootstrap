from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.daemon.exclusions import (
    BUILTIN_EXCLUDES,
    ExclusionPolicy,
)


def _make_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    (root / ".gitignore").write_text(
        "*.log\nbuild/\nsecrets.env\n# comment\n!keep.log\n", encoding="utf-8",
    )
    return root


def test__ExclusionPolicy__for_repo__loads_gitignore(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    policy = ExclusionPolicy.for_repo(root)
    assert "*.log" in policy.gitignore_patterns
    assert "build/" in policy.gitignore_patterns
    assert "secrets.env" in policy.gitignore_patterns
    assert "# comment" not in policy.gitignore_patterns
    assert "!keep.log" not in policy.gitignore_patterns


def test__ExclusionPolicy__is_excluded__builtin_patterns(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    policy = ExclusionPolicy.for_repo(root)
    assert policy.is_excluded(root / ".git" / "config")
    assert policy.is_excluded(root / "graphify-out" / "graph.json")
    assert policy.is_excluded(root / ".venv" / "bin" / "python")
    assert policy.is_excluded(root / "src" / "__pycache__" / "mod.pyc")
    assert policy.is_excluded(root / "src.egg-info" / "PKG-INFO")
    assert ".pi/koios-ingestion" in BUILTIN_EXCLUDES


def test__ExclusionPolicy__is_excluded__gitignore_patterns(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    policy = ExclusionPolicy.for_repo(root)
    assert policy.is_excluded(root / "app.log")
    assert policy.is_excluded(root / "build" / "output.o")
    assert policy.is_excluded(root / "secrets.env")


def test__ExclusionPolicy__is_excluded__not_excluded(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    (root / "src").mkdir()
    (root / "src" / "main.py").write_text("print('hi')", encoding="utf-8")
    policy = ExclusionPolicy.for_repo(root)
    assert not policy.is_excluded(root / "src" / "main.py")
    assert not policy.is_excluded(root / "README.md")


def test__ExclusionPolicy__is_excluded__outside_repo(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    policy = ExclusionPolicy.for_repo(root)
    assert policy.is_excluded(tmp_path / "other" / "file.py")


def test__ExclusionPolicy__filter_eligible__removes_excluded(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    (root / "src").mkdir()
    (root / "src" / "main.py").write_text("x", encoding="utf-8")
    policy = ExclusionPolicy.for_repo(root)
    paths = [
        root / "src" / "main.py",
        root / "app.log",
        root / "graphify-out" / "graph.json",
        root / "README.md",
    ]
    eligible = policy.filter_eligible(paths)
    assert root / "src" / "main.py" in eligible
    assert root / "README.md" in eligible
    assert root / "app.log" not in eligible
    assert root / "graphify-out" / "graph.json" not in eligible
