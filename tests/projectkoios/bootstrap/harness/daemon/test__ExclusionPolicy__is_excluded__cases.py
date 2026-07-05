from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.daemon.exclusions import (
    BUILTIN_EXCLUDES,
    ExclusionPolicy,
)


def _make_repo(tmp_path: Path) -> Path:
    """Create a repository fixture with gitignore exclusions."""
    # Root is the repository fixture used by exclusion policy tests.
    root: Path = tmp_path / "repo"
    root.mkdir()
    (root / ".gitignore").write_text(
        "*.log\nbuild/\nsecrets.env\n# comment\n!keep.log\n", encoding="utf-8",
    )
    return root


def test__ExclusionPolicy__for_repo__loads_gitignore(tmp_path: Path) -> None:
    """Validate repository policy loads supported gitignore entries."""
    # Root is the repository fixture used by exclusion policy tests.
    root: Path = _make_repo(tmp_path)
    # Policy is the exclusion policy loaded from repository configuration.
    policy: ExclusionPolicy = ExclusionPolicy.for_repo(root)
    assert "*.log" in policy.gitignore_patterns
    assert "build/" in policy.gitignore_patterns
    assert "secrets.env" in policy.gitignore_patterns
    assert "# comment" not in policy.gitignore_patterns
    assert "!keep.log" not in policy.gitignore_patterns


def test__ExclusionPolicy__is_excluded__builtin_patterns(tmp_path: Path) -> None:
    """Validate built-in daemon exclusions filter generated and local paths."""
    # Root is the repository fixture used by exclusion policy tests.
    root: Path = _make_repo(tmp_path)
    # Policy is the exclusion policy loaded from repository configuration.
    policy: ExclusionPolicy = ExclusionPolicy.for_repo(root)
    assert policy.is_excluded(root / ".git" / "config")
    assert policy.is_excluded(root / "graphify-out" / "graph.json")
    assert policy.is_excluded(root / ".venv" / "bin" / "python")
    assert policy.is_excluded(root / "src" / "__pycache__" / "mod.pyc")
    assert policy.is_excluded(root / "src.egg-info" / "PKG-INFO")
    assert ".pi/koios-ingestion" in BUILTIN_EXCLUDES


def test__ExclusionPolicy__is_excluded__gitignore_patterns(tmp_path: Path) -> None:
    """Validate gitignore patterns exclude matching repository paths."""
    # Root is the repository fixture used by exclusion policy tests.
    root: Path = _make_repo(tmp_path)
    # Policy is the exclusion policy loaded from repository configuration.
    policy: ExclusionPolicy = ExclusionPolicy.for_repo(root)
    assert policy.is_excluded(root / "app.log")
    assert policy.is_excluded(root / "build" / "output.o")
    assert policy.is_excluded(root / "secrets.env")


def test__ExclusionPolicy__is_excluded__not_excluded(tmp_path: Path) -> None:
    """Validate eligible source and documentation paths are not excluded."""
    # Root is the repository fixture used by exclusion policy tests.
    root: Path = _make_repo(tmp_path)
    (root / "src").mkdir()
    (root / "src" / "main.py").write_text("print('hi')", encoding="utf-8")
    # Policy is the exclusion policy loaded from repository configuration.
    policy: ExclusionPolicy = ExclusionPolicy.for_repo(root)
    assert not policy.is_excluded(root / "src" / "main.py")
    assert not policy.is_excluded(root / "README.md")


def test__ExclusionPolicy__is_excluded__outside_repo(tmp_path: Path) -> None:
    """Validate paths outside the repository are excluded safely."""
    # Root is the repository fixture used by exclusion policy tests.
    root: Path = _make_repo(tmp_path)
    # Policy is the exclusion policy loaded from repository configuration.
    policy: ExclusionPolicy = ExclusionPolicy.for_repo(root)
    assert policy.is_excluded(tmp_path / "other" / "file.py")


def test__ExclusionPolicy__filter_eligible__removes_excluded(tmp_path: Path) -> None:
    """Validate eligible path filtering removes excluded inputs."""
    # Root is the repository fixture used by exclusion policy tests.
    root: Path = _make_repo(tmp_path)
    (root / "src").mkdir()
    (root / "src" / "main.py").write_text("x", encoding="utf-8")
    # Policy is the exclusion policy loaded from repository configuration.
    policy: ExclusionPolicy = ExclusionPolicy.for_repo(root)
    # Paths include eligible files, gitignored files, and generated files.
    paths: list[Path] = [
        root / "src" / "main.py",
        root / "app.log",
        root / "graphify-out" / "graph.json",
        root / "README.md",
    ]
    # Eligible paths are the filter output under assertion.
    eligible: list[Path] = policy.filter_eligible(paths)
    assert root / "src" / "main.py" in eligible
    assert root / "README.md" in eligible
    assert root / "app.log" not in eligible
    assert root / "graphify-out" / "graph.json" not in eligible
