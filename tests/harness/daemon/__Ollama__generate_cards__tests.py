from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from projectkoios.bootstrap.harness.daemon.ollama import (
    OLLAMA_DEFAULT_ENDPOINT,
    OLLAMA_DEFAULT_MODEL,
    _build_chunk_prompt,
    _check_ollama,
    generate_chunk_cards,
)
from projectkoios.bootstrap.harness.daemon.activities import DaemonContext
from projectkoios.bootstrap.harness.daemon.data import (
    FreshnessState,
    GraphSnapshot,
)


def _make_ctx(repo_root: str) -> DaemonContext:
    return DaemonContext(
        run_id="r1",
        repo_root=repo_root,
        started_at="",
        trigger_kind="test",
        freshness=FreshnessState.UPDATING,
        graph_snapshot=GraphSnapshot(
            run_id="r1", path="/g", node_count=1, edge_count=0, community_count=0,
        ),
    )


def test__build_chunk_prompt__is_role_neutral() -> None:
    prompt = _build_chunk_prompt("src/main.py", "def main(): pass")
    assert "role-neutral" in prompt
    assert "Do not produce role-specific" in prompt
    assert "src/main.py" in prompt


def test__generate_chunk_cards__degrades_when_no_chunks_file(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    ctx = _make_ctx(str(repo))
    result = generate_chunk_cards(ctx)
    assert result.chunk_card_set is None
    assert len(result.warnings) > 0
    assert "no graphify chunks" in result.warnings[-1].lower() or "skipping chunk cards" in result.warnings[-1].lower()


def test__generate_chunk_cards__degrades_when_ollama_unreachable(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    out = repo / "graphify-out"
    out.mkdir()
    (out / ".graphify_chunks.json").write_text('[{"id":"c1","source":"f.py","text":"x"}]', encoding="utf-8")
    ctx = _make_ctx(str(repo))
    with patch(
        "projectkoios.bootstrap.harness.daemon.ollama._check_ollama",
        return_value=False,
    ):
        result = generate_chunk_cards(ctx)
    assert result.chunk_card_set is None
    assert any("unreachable" in w.lower() for w in result.warnings)


def test__check_ollama__returns_false_for_unreachable() -> None:
    assert _check_ollama("http://localhost:99999") is False


def test__ollama_constants__use_localhost() -> None:
    assert "localhost:11434" in OLLAMA_DEFAULT_ENDPOINT
    assert OLLAMA_DEFAULT_MODEL


def test__generate_chunk_cards__skips_when_no_graph_snapshot(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    ctx = DaemonContext(
        run_id="r1",
        repo_root=str(repo),
        started_at="",
        trigger_kind="test",
        freshness=FreshnessState.UPDATING,
        graph_snapshot=None,
    )
    result = generate_chunk_cards(ctx)
    assert result.chunk_card_set is None
