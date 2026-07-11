from __future__ import annotations

from pathlib import Path

import pytest

from projectkoios.cli.main import main


def test__OperatorConsolePreviewCommand__run__uses_package_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """Validate that the preview command hides the long package cd from the user."""
    calls: list[tuple[list[str], Path, bool]] = []

    def record_run(command: list[str], cwd: Path, check: bool) -> None:
        calls.append((command, cwd, check))

    monkeypatch.setattr("subprocess.run", record_run)
    monkeypatch.setattr(
        "sys.argv",
        [
            "projectkoios",
            "operator-console",
            "preview",
            "--package-dir",
            str(tmp_path),
            "--host",
            "127.0.0.1",
            "--port",
            "4173",
        ],
    )

    main()

    assert calls == [
        (["npm", "install", "--ignore-scripts"], tmp_path, True),
        (["npm", "run", "build"], tmp_path, True),
        (["npm", "run", "preview", "--", "--host", "127.0.0.1", "--port", "4173"], tmp_path, True),
    ]
    output: str = capsys.readouterr().out
    assert f"operator-console package: {tmp_path}" in output
    assert "operator-console preview: http://127.0.0.1:4173/" in output


def test__OperatorConsolePreviewCommand__run__can_skip_install(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Validate that repeat previews can skip install while preserving build-before-preview."""
    calls: list[list[str]] = []

    def record_run(command: list[str], cwd: Path, check: bool) -> None:
        calls.append(command)

    monkeypatch.setattr("subprocess.run", record_run)
    monkeypatch.setattr(
        "sys.argv",
        [
            "projectkoios",
            "operator-console",
            "preview",
            "--package-dir",
            str(tmp_path),
            "--skip-install",
        ],
    )

    main()

    assert calls == [
        ["npm", "run", "build"],
        ["npm", "run", "preview", "--", "--host", "127.0.0.1", "--port", "4173"],
    ]
