from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from projectkoios.bootstrap.harness.daemon.activities import DaemonContext
from projectkoios.bootstrap.harness.daemon.data import (
    FreshnessState,
    GraphSnapshot,
    RunMetadata,
)
from projectkoios.bootstrap.harness.daemon.ollama import (
    OLLAMA_DEFAULT_ENDPOINT,
    OLLAMA_DEFAULT_MODEL,
    build_chunk_prompt,
    check_ollama,
    resolve_ollama_model,
    generate_chunk_cards,
)


def make_ctx(repo_root: str) -> DaemonContext:
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


def test_build_chunk_prompt__is_role_neutral() -> None:
    prompt = build_chunk_prompt("src/main.py", "def main(): pass")
    assert "role-neutral" in prompt
    assert "Do not produce role-specific" in prompt
    assert "src/main.py" in prompt


def test__generate_chunk_cards__degrades_when_no_chunks_file(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    ctx = make_ctx(str(repo))
    result = generate_chunk_cards(ctx)
    assert result.chunk_card_set is None
    assert len(result.warnings) > 0
    assert "no graphify" in result.warnings[-1].lower() or "skipping chunk cards" in result.warnings[-1].lower()


def test__generate_chunk_cards__degrades_when_ollama_unreachable(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    out = repo / "graphify-out"
    out.mkdir()
    (out / ".graphify_chunks.json").write_text('[{"id":"c1","source":"f.py","text":"x"}]', encoding="utf-8")
    ctx = make_ctx(str(repo))
    with patch("projectkoios.bootstrap.harness.daemon.ollama.check_ollama", return_value=False):
        result = generate_chunk_cards(ctx)
    assert result.chunk_card_set is None
    assert any("unreachable" in w.lower() for w in result.warnings)


def test_check_ollama__returns_false_for_unreachable() -> None:
    assert check_ollama("http://localhost:99999") is False


def test__ollama_constants__use_localhost() -> None:
    assert "localhost:11434" in OLLAMA_DEFAULT_ENDPOINT
    assert OLLAMA_DEFAULT_MODEL


def test_resolve_ollama_model__matches_prefixed_model() -> None:
    with patch(
        "projectkoios.bootstrap.harness.daemon.ollama.list_ollama_models",
        return_value=["llama3.2:1b", "qwen3:latest"],
    ):
        assert resolve_ollama_model("http://localhost:11434", "llama3.2") == "llama3.2:1b"


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


def test__generate_chunk_cards__logs_processing(tmp_path: Path, capsys) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    out = repo / "graphify-out"
    out.mkdir()
    (out / ".graphify_chunks.json").write_text(
        '[{"id":"c1","source":"f.py","text":"x"},{"id":"c2","source":"g.py","text":"y"}]',
        encoding="utf-8",
    )
    ctx = make_ctx(str(repo))
    with patch("projectkoios.bootstrap.harness.daemon.ollama.check_ollama", return_value=True), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.resolve_ollama_model", return_value="llama3.2:1b"), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.count_eligible_files", return_value=10), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.count_indexed_files", return_value=8), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.load_chunk_batches", return_value=("graphify_chunks", [[str(repo / 'a.py')], [str(repo / 'b.py')]])), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.render_chunk_body", side_effect=[("a.py", "x"), ("b.py", "y")]), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.ollama_generate", side_effect=["one", "two"]):
        result = generate_chunk_cards(ctx)
    captured = capsys.readouterr().out
    assert result.chunk_card_set is not None
    assert result.chunk_card_set.card_count == 2
    assert "[ollama] summary eligible=10 indexed=8 batches=2 skipped=2 source=graphify_chunks" in captured
    assert "[ollama] processing 2 batch(es) from graphify_chunks" in captured
    assert "[ollama] batch 1/2" in captured
    assert "[ollama] finished cards=2 failures=0 degraded=False" in captured


def test__generate_chunk_cards__reads_list_chunks(tmp_path: Path, capsys) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    src = repo / "src"
    src.mkdir()
    (src / "a.py").write_text("print('a')\n", encoding="utf-8")
    (src / "b.py").write_text("print('b')\n", encoding="utf-8")
    out = repo / "graphify-out"
    out.mkdir()
    (out / ".graphify_chunks.json").write_text(
        f'[["{src / "a.py"}", "{src / "b.py"}"]]',
        encoding="utf-8",
    )
    ctx = make_ctx(str(repo))
    with patch("projectkoios.bootstrap.harness.daemon.ollama.check_ollama", return_value=True), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.resolve_ollama_model", return_value="llama3.2:1b"), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.count_eligible_files", return_value=4), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.count_indexed_files", return_value=2), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.load_chunk_batches", return_value=("graphify_chunks", [[str(src / 'a.py'), str(src / 'b.py')]])), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.render_chunk_body", return_value=("a.py +1 more", "print('a')\n\nprint('b')\n")), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.ollama_generate", return_value="summary") as gen:
        result = generate_chunk_cards(ctx)
    captured = capsys.readouterr().out
    assert result.chunk_card_set is not None
    assert result.chunk_card_set.card_count == 1
    assert gen.call_count == 1
    assert "print('a')" in gen.call_args.args[2]
    assert "[ollama] batch 1/1" in captured


def test__generate_chunk_cards__enriches_metadata(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    out = repo / "graphify-out"
    out.mkdir()
    (out / ".graphify_chunks.json").write_text('[{"id":"c1","source":"f.py","text":"x"}]', encoding="utf-8")
    ctx = DaemonContext(
        run_id="r1",
        repo_root=str(repo),
        started_at="",
        trigger_kind="test",
        freshness=FreshnessState.UPDATING,
        graph_snapshot=GraphSnapshot(run_id="r1", path="/g", node_count=1, edge_count=0, community_count=0),
        metadata=RunMetadata(run_id="r1", repo_path=str(repo), repo_identity="repo", daemon_version="0.1.0", graphify_version="1.0"),
    )
    with patch("projectkoios.bootstrap.harness.daemon.ollama.check_ollama", return_value=True), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.resolve_ollama_model", return_value="llama3.2:1b"), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.count_eligible_files", return_value=5), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.count_indexed_files", return_value=4), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.load_chunk_batches", return_value=("manifest", [[str(repo / 'f.py')]])), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.render_chunk_body", return_value=("f.py", "x")), \
         patch("projectkoios.bootstrap.harness.daemon.ollama.ollama_generate", return_value="summary"):
        result = generate_chunk_cards(ctx)
    assert result.metadata is not None
    assert result.metadata.eligible_files_count == 5
    assert result.metadata.indexed_files_count == 4
    assert result.metadata.chunk_batch_count == 1
    assert result.metadata.chunk_batch_source == "manifest"
    assert result.metadata.skipped_paths_count == 1
