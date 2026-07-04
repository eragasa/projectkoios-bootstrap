from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.python_policy import TargetSelector, ValidationTarget


def test__TargetSelector__explicit_targets__includes_python_files(tmp_path: Path) -> None:
    """Validate that explicit directory targets include only Python files."""
    # Source directory contains Python and non-Python files for selection.
    source_dir: Path = tmp_path / "src"
    source_dir.mkdir()
    # Python file should be returned by target selection.
    python_file: Path = source_dir / "example.py"
    python_file.write_text("value: int = 1\n", encoding="utf-8")
    # Text file should be ignored by target selection.
    text_file: Path = source_dir / "example.txt"
    text_file.write_text("ignore\n", encoding="utf-8")

    # Targets are selected recursively from the explicit source directory.
    targets: tuple[ValidationTarget, ...] = TargetSelector(repo_root=tmp_path).explicit_targets((source_dir,))

    assert tuple(target.path for target in targets) == (python_file.resolve(),)


def test__TargetSelector__explicit_targets__excludes_cache_and_venv(tmp_path: Path) -> None:
    """Validate that cache and virtualenv directories are excluded."""
    # Cache directory should be excluded even when it contains Python files.
    cache_dir: Path = tmp_path / "__pycache__"
    cache_dir.mkdir()
    # Cache Python file should not be selected.
    cache_file: Path = cache_dir / "cached.py"
    cache_file.write_text("value: int = 1\n", encoding="utf-8")
    # Virtualenv directory should be excluded even when it contains Python files.
    venv_dir: Path = tmp_path / ".venv"
    venv_dir.mkdir()
    # Virtualenv Python file should not be selected.
    venv_file: Path = venv_dir / "site.py"
    venv_file.write_text("value: int = 1\n", encoding="utf-8")

    # Targets are selected recursively from the repository root.
    targets: tuple[ValidationTarget, ...] = TargetSelector(repo_root=tmp_path).explicit_targets((tmp_path,))

    assert targets == ()
