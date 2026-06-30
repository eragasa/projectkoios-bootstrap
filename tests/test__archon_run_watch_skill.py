from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = (
    REPO_ROOT
    / "agents" / "global" / "roles" / "ATHENA"
    / "archon_run_watch" / "scripts"
)
sys.path.insert(0, str(SCRIPTS_DIR))


from projectkoios.bootstrap.harness.headers import extract_handoff_headers  # noqa: E402


# ---------------------------------------------------------------------------
# extract_handoff_headers (shared module, importable via PYTHONPATH)
# ---------------------------------------------------------------------------

VALID_HEADERS = """\
Origin: Athena
Created: 2026-06-30 12:00
From: Athena
To: Vulcan
Status: active

# Title

Body text.
"""

NO_HEADERS = """\
# Just a title

No headers here.
"""

DUPLICATE_KEYS = """\
Origin: Hermes
Status: draft
Origin: Athena

Body.
"""


def test_extract_headers_parses_valid_text() -> None:
    result = extract_handoff_headers(VALID_HEADERS)
    assert result["Origin"] == "Athena"
    assert result["From"] == "Athena"
    assert result["To"] == "Vulcan"
    assert result["Status"] == "active"


def test_extract_headers_no_headers_returns_empty() -> None:
    assert extract_handoff_headers(NO_HEADERS) == {}


def test_extract_headers_duplicate_last_wins() -> None:
    result = extract_handoff_headers(DUPLICATE_KEYS)
    assert result["Origin"] == "Athena"


def test_extract_headers_stops_at_first_blank_line() -> None:
    text = "Origin: pi\n\nFrom: Hermes\nTo: Athena\n"
    result = extract_handoff_headers(text)
    assert "Origin" in result
    assert "From" not in result


def test_extract_headers_stops_at_prose_line() -> None:
    text = "Origin: pi\nSome prose text\nFrom: Hermes\n"
    result = extract_handoff_headers(text)
    assert "Origin" in result
    assert "From" not in result


def test_extract_headers_whitespace_in_value() -> None:
    text = "Origin:   Athena  \nStatus: active\n"
    result = extract_handoff_headers(text)
    assert result["Origin"] == "Athena"
    assert result["Status"] == "active"


# ---------------------------------------------------------------------------
# handoff_new.py slugify and render_fields
# ---------------------------------------------------------------------------

def test_slugify() -> None:
    import handoff_new
    assert handoff_new.slugify("Hello World") == "hello-world"
    assert handoff_new.slugify("hello   world") == "hello-world"
    assert handoff_new.slugify("hello!!!world?") == "hello-world"
    assert handoff_new.slugify("hello_world_test") == "hello-world-test"
    assert handoff_new.slugify("--hello-world--") == "hello-world"
    assert handoff_new.slugify("Session Start") == handoff_new.slugify("Session Start")


def test_render_fields() -> None:
    import handoff_new

    result = handoff_new.render_fields(origin="pi", from_="Hermes", to="Athena")
    assert "Origin: pi" in result
    assert "From: Hermes" in result
    assert "To: Athena" in result
    assert "Status: draft" in result

    result2 = handoff_new.render_fields(
        origin="pi", from_="Hermes", to="Athena",
        acting_as="Codex", scope="projectkoios-bootstrap",
        repository="/repo", delegated_operator="Codex",
    )
    assert "Acting-As: Codex" in result2
    assert "Scope: projectkoios-bootstrap" in result2
    assert "Repository: /repo" in result2
    assert "Delegated-Operator: Codex" in result2

    assert "Status: active" in handoff_new.render_fields(
        origin="pi", from_="Hermes", to="Athena", status="active"
    )
    assert handoff_new.render_fields(origin="pi", from_="Hermes", to="Athena").endswith("\n")


def test_handoff_new_cli_creates_file(tmp_path: Path) -> None:
    import subprocess
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "handoff_new.py"),
         "--dir", str(tmp_path),
         "--topic", "cli-test",
         "--origin", "pi",
         "--from", "Hermes",
         "--to", "Athena",
         "--status", "active",
         "--title", "CLI Test"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    created_path = result.stdout.strip()
    assert Path(created_path).exists()
    text = Path(created_path).read_text(encoding="utf-8")
    assert "Origin: pi" in text
    assert "From: Hermes" in text
    assert "# CLI Test" in text


# ---------------------------------------------------------------------------
# session_scan.py
# ---------------------------------------------------------------------------

def test_scan_empty_directory(tmp_path: Path) -> None:
    import session_scan
    assert session_scan.scan_handoff_dir(tmp_path) == []


def test_scan_non_existent_directory() -> None:
    import session_scan
    assert session_scan.scan_handoff_dir(Path("/nonexistent")) == []


def test_scan_parses_headers(tmp_path: Path) -> None:
    import session_scan
    f = tmp_path / "test.md"
    f.write_text("Origin: pi\nFrom: Hermes\nTo: Athena\nStatus: active\n\nBody\n", encoding="utf-8")
    results = session_scan.scan_handoff_dir(tmp_path)
    assert len(results) == 1
    assert results[0]["Origin"] == "pi"
    assert results[0]["Status"] == "active"


def test_scan_skips_files_without_headers(tmp_path: Path) -> None:
    import session_scan
    f = tmp_path / "notes.md"
    f.write_text("# Notes\n\nJust prose.\n", encoding="utf-8")
    assert session_scan.scan_handoff_dir(tmp_path) == []


def test_build_summary_groups_by_status(tmp_path: Path) -> None:
    import session_scan

    d1 = tmp_path / "archon" / "handoffs"
    d2 = tmp_path / "opencode" / "handoffs"
    d1.mkdir(parents=True)
    d2.mkdir(parents=True)

    (d1 / "a.md").write_text("Origin: pi\nFrom: Hermes\nTo: Athena\nStatus: active\n\n", encoding="utf-8")
    (d1 / "b.md").write_text("Origin: pi\nFrom: Hermes\nTo: Athena\nStatus: active\n\n", encoding="utf-8")
    (d2 / "c.md").write_text("Origin: pi\nFrom: Hermes\nTo: Vulcan\nStatus: draft\n\n", encoding="utf-8")

    summary = session_scan.build_summary(tmp_path)
    assert summary["files"]["total"] == 3
    assert summary["by_status"]["active"] == 2
    assert summary["by_status"]["draft"] == 1


def test_build_summary_detects_missing_headers(tmp_path: Path) -> None:
    import session_scan

    d = tmp_path / "pi" / "handoffs"
    d.mkdir(parents=True)

    (d / "a.md").write_text("Origin: pi\nFrom: Hermes\n\nBody\n", encoding="utf-8")
    summary = session_scan.build_summary(tmp_path)
    assert summary["files"]["with_missing_headers"] == 1


# ---------------------------------------------------------------------------
# archon_run_watch.py
# ---------------------------------------------------------------------------

def test_run_status_dataclass() -> None:
    import archon_run_watch
    rs = archon_run_watch.RunStatus(
        run_id="abc", status="running", pid=123,
        log_path="/tmp/log", raw={"key": "val"},
    )
    assert rs.run_id == "abc"
    assert rs.status == "running"
    assert rs.pid == 123
    assert rs.log_path == "/tmp/log"
    assert rs.raw == {"key": "val"}


def test_detect_stale_not_running() -> None:
    import archon_run_watch
    rs = archon_run_watch.RunStatus(
        run_id="a", status="completed", pid=None, log_path=None, raw=None,
    )
    assert archon_run_watch.detect_stale(rs) is None


def test_detect_stale_running_no_pid() -> None:
    import archon_run_watch
    rs = archon_run_watch.RunStatus(
        run_id="a", status="running", pid=None, log_path=None, raw=None,
    )
    reason = archon_run_watch.detect_stale(rs)
    assert reason is not None
    assert "no PID" in reason


def test_detect_stale_running_with_live_pid() -> None:
    import archon_run_watch
    import os
    rs = archon_run_watch.RunStatus(
        run_id="a", status="running", pid=os.getpid(), log_path=None, raw=None,
    )
    assert archon_run_watch.detect_stale(rs) is None


def _make_failing_run_archon():
    def mock_run(*a, **kw):
        raise FileNotFoundError("archon not found")
    return mock_run


def test_fetch_run_archon_not_found() -> None:
    import archon_run_watch

    original = archon_run_watch.run_archon
    archon_run_watch.run_archon = _make_failing_run_archon()

    try:
        result = archon_run_watch.fetch_run("test-id")
        assert isinstance(result, str)
        assert "not found" in result
    finally:
        archon_run_watch.run_archon = original


def test_abandon_run_archon_not_found() -> None:
    import archon_run_watch

    original = archon_run_watch.run_archon
    archon_run_watch.run_archon = _make_failing_run_archon()

    try:
        result = archon_run_watch.abandon_run("test-id")
        assert isinstance(result, str)
        assert "not found" in result
    finally:
        archon_run_watch.run_archon = original
