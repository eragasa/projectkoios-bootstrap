from __future__ import annotations

from pathlib import Path

import pytest

from projectkoios.cli.main import main

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def test__KoiosCli__index_build(tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    """Validate that the Koios CLI builds a persisted index fixture."""
    # Config and schema paths are passed through sys.argv to the CLI.
    config_path: Path = write_config(tmp_path)
    # Schema path validates the fixture config for the CLI run.
    schema_path: Path = write_schema(tmp_path)
    monkeypatch.setattr(
        "sys.argv",
        [
            "projectkoios",
            "koios",
            "index",
            "build",
            "--config",
            str(config_path),
            "--schema",
            str(schema_path),
        ],
    )

    main()

    # Output summarizes the built index and section count.
    output: str = capsys.readouterr().out
    assert "koios index build:" in output
    assert "sections=" in output
    assert (tmp_path / "graph" / "index.json").exists()
