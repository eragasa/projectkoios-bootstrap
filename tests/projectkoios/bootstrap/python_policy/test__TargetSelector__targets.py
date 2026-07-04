from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.python_policy import TargetSelector


def test__TargetSelector__explicit_targets__includes_python_files(tmp_path: Path):
    source_dir: Path = tmp_path / "src"
    source_dir.mkdir()
    python_file: Path = source_dir / "example.py"
    python_file.write_text("value: int = 1\n", encoding="utf-8")
    text_file: Path = source_dir / "example.txt"
    text_file.write_text("ignore\n", encoding="utf-8")

    targets = TargetSelector(repo_root=tmp_path).explicit_targets((source_dir,))

    assert tuple(target.path for target in targets) == (python_file.resolve(),)


def test__TargetSelector__explicit_targets__excludes_cache_and_venv(tmp_path: Path):
    cache_dir: Path = tmp_path / "__pycache__"
    cache_dir.mkdir()
    cache_file: Path = cache_dir / "cached.py"
    cache_file.write_text("value: int = 1\n", encoding="utf-8")
    venv_dir: Path = tmp_path / ".venv"
    venv_dir.mkdir()
    venv_file: Path = venv_dir / "site.py"
    venv_file.write_text("value: int = 1\n", encoding="utf-8")

    targets = TargetSelector(repo_root=tmp_path).explicit_targets((tmp_path,))

    assert targets == ()
