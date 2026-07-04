from __future__ import annotations

from projectkoios.cli.main import main

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def test__KoiosCli__index_build(tmp_path, capsys, monkeypatch):
    config_path = write_config(tmp_path)
    schema_path = write_schema(tmp_path)
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

    output = capsys.readouterr().out
    assert "koios index build:" in output
    assert "sections=" in output
    assert (tmp_path / "graph" / "index.json").exists()
