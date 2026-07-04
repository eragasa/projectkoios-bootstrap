from __future__ import annotations

from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = (
    REPO_ROOT
    / "agents" / "global" / "roles" / "ATHENA"
    / "archon_run_watch" / "scripts"
)
sys.path.insert(0, str(SCRIPTS_DIR))


from _run import ArchonClient, RunStatus  # noqa: E402
from projectkoios.bootstrap.harness.headers import extract_handoff_headers  # noqa: E402


# ===================================================================
# _run — RunStatus.is_stale()
# ===================================================================

def test_is_stale_not_running() -> None:
    rs = RunStatus(
        run_id="a", status="completed",
        pid=None, log_path=None, started_at=None,
        workflow_name=None, raw=None,
    )
    assert rs.is_stale() is None


def test_is_stale_pid_alive() -> None:
    import os
    rs = RunStatus(
        run_id="a", status="running",
        pid=os.getpid(), log_path=None, started_at=None,
        workflow_name=None, raw=None,
    )
    assert rs.is_stale() is None


def test_is_stale_pid_gone() -> None:
    """A PID that does not exist should be detected as stale."""
    rs = RunStatus(
        run_id="a", status="running",
        pid=999_999_999, log_path=None, started_at="2026-06-30T00:00:00+00:00",
        workflow_name=None, raw=None,
    )
    reason = rs.is_stale()
    assert reason is not None
    assert "no longer exists" in reason


def test_is_stale_no_pid_no_started_at() -> None:
    """No PID and no started_at is inconclusive — not stale."""
    rs = RunStatus(
        run_id="a", status="running",
        pid=None, log_path=None, started_at=None,
        workflow_name=None, raw=None,
    )
    assert rs.is_stale() is None


def test_is_stale_no_pid_recent() -> None:
    """No PID but recently started is not stale."""
    from datetime import datetime, timezone
    recent = datetime.now(timezone.utc).isoformat()
    rs = RunStatus(
        run_id="a", status="running",
        pid=None, log_path=None, started_at=recent,
        workflow_name=None, raw=None,
    )
    assert rs.is_stale() is None


def test_is_stale_no_pid_old() -> None:
    """No PID and older than max_age_minutes is stale."""
    rs = RunStatus(
        run_id="a", status="running",
        pid=None, log_path=None,
        started_at="2020-01-01T00:00:00+00:00",
        workflow_name=None, raw=None,
    )
    reason = rs.is_stale(max_age_minutes=60)
    assert reason is not None
    assert "without PID" in reason


def test_is_stale_invalid_started_at() -> None:
    """Invalid started_at string is handled gracefully — not stale."""
    rs = RunStatus(
        run_id="a", status="running",
        pid=None, log_path=None, started_at="not-a-date",
        workflow_name=None, raw=None,
    )
    assert rs.is_stale() is None


# ===================================================================
# _run — ArchonClient
# ===================================================================

def _completed(args: list[str] | None = None,
               stdout: str = "",
               stderr: str = "",
               returncode: int = 0) -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(
        args=args or [],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def test_archon_client_fetch_run_success() -> None:
    client = ArchonClient()
    client.run_process = lambda *a, json_output=False: _completed(stdout='''{
        "id": "run-1",
        "status": "running",
        "pid": 12345,
        "log": "/tmp/log",
        "started_at": "2026-06-30T12:00:00+00:00",
        "workflow_name": "test-wf"
    }''')
    result = client.fetch_run("run-1")
    assert isinstance(result, RunStatus)
    assert result.run_id == "run-1"
    assert result.status == "running"
    assert result.pid == 12345
    assert result.log_path == "/tmp/log"
    assert result.started_at == "2026-06-30T12:00:00+00:00"
    assert result.workflow_name == "test-wf"


def test_archon_client_fetch_run_archon_not_found() -> None:
    client = ArchonClient(archon_bin="/nonexistent/archon")
    result = client.fetch_run("x")
    assert isinstance(result, str)
    assert "not found" in result


def test_archon_client_fetch_run_nonzero_exit() -> None:
    client = ArchonClient()
    client.run_process = lambda *a, json_output=False: _completed(
        returncode=1, stderr="workflow not found",
    )
    result = client.fetch_run("bad-id")
    assert isinstance(result, str)
    assert "not found" in result


def test_archon_client_fetch_run_invalid_json() -> None:
    client = ArchonClient()
    client.run_process = lambda *a, json_output=False: _completed(stdout="not json")
    result = client.fetch_run("bad-id")
    assert isinstance(result, str)
    assert "failed to parse" in result


def test_archon_client_abandon_run_success() -> None:
    client = ArchonClient()
    client.run_process = lambda *a, json_output=False: _completed(stdout='{"ok": true}')
    assert client.abandon_run("run-1") is None


def test_archon_client_abandon_run_nonzero_exit() -> None:
    client = ArchonClient()
    client.run_process = lambda *a, json_output=False: _completed(
        returncode=1, stderr="not found",
    )
    result = client.abandon_run("bad-id")
    assert isinstance(result, str)
    assert "not found" in result


def test_archon_client_list_runs_success() -> None:
    client = ArchonClient()
    client.run_process = lambda *a, json_output=False: _completed(stdout='''{
        "runs": [
            {"id": "r1", "status": "running", "workflow_name": "wf1"},
            {"id": "r2", "status": "running", "workflow_name": "wf2"}
        ],
        "total": 2
    }''')
    result = client.list_runs(status="running")
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == "r1"


def test_archon_client_list_runs_nonzero_exit() -> None:
    client = ArchonClient()
    client.run_process = lambda *a, json_output=False: _completed(
        returncode=1, stderr="error",
    )
    result = client.list_runs()
    assert isinstance(result, str)


# ===================================================================
# sweep_stale
# ===================================================================

def test_sweep_stale_empty() -> None:
    import sweep_stale
    client = ArchonClient()
    client.run_process = lambda *a, json_output=False: _completed(
        stdout='{"runs": [], "total": 0}',
    )
    results = sweep_stale.sweep_stale(client)
    assert len(results) == 0


def test_sweep_stale_all_alive() -> None:
    import os
    import sweep_stale
    client = ArchonClient()
    responses = iter([
        _completed(stdout='{"runs": [{"id": "r1", "workflow_name": "wf"}]}'),
        _completed(stdout='{"id": "r1", "status": "running", "pid": ' + str(os.getpid()) + ', "started_at": "2026-06-30T12:00:00+00:00", "workflow_name": "wf"}'),
    ])
    client.run_process = lambda *a, json_output=False: next(responses)
    results = sweep_stale.sweep_stale(client)
    assert len(results) == 1
    assert results[0]["stale"] is False


def test_sweep_stale_with_stale_no_abandon() -> None:
    import sweep_stale
    client = ArchonClient()
    responses = iter([
        _completed(stdout='{"runs": [{"id": "r1", "workflow_name": "wf"}]}'),
        _completed(stdout='{"id": "r1", "status": "running", "pid": null, "started_at": "2020-01-01T00:00:00+00:00", "workflow_name": "wf"}'),
    ])
    client.run_process = lambda *a, json_output=False: next(responses)
    results = sweep_stale.sweep_stale(client, abandon=False)
    assert len(results) == 1
    assert results[0]["stale"] is True
    assert results[0]["abandoned"] is False


def test_sweep_stale_with_abandon() -> None:
    import sweep_stale
    client = ArchonClient()
    responses = iter([
        _completed(stdout='{"runs": [{"id": "r1", "workflow_name": "wf"}]}'),
        _completed(stdout='{"id": "r1", "status": "running", "pid": 999999999, "started_at": "2026-06-30T12:00:00+00:00", "workflow_name": "wf"}'),
        _completed(stdout='{"ok": true}'),
    ])
    client.run_process = lambda *a, json_output=False: next(responses)
    results = sweep_stale.sweep_stale(client, abandon=True)
    assert len(results) == 1
    assert results[0]["stale"] is True
    assert results[0]["abandoned"] is True


def test_sweep_stale_writes_handoff(tmp_path: Path) -> None:
    import sweep_stale
    handoff_path = tmp_path / "sweep.md"

    client = ArchonClient()
    responses = iter([
        _completed(stdout='{"runs": [{"id": "r1", "workflow_name": "wf"}]}'),
        _completed(stdout='{"id": "r1", "status": "running", "pid": 999999999, "started_at": "2026-06-30T12:00:00+00:00", "workflow_name": "wf"}'),
        _completed(stdout='{"ok": true}'),
    ])
    client.run_process = lambda *a, json_output=False: next(responses)
    results = sweep_stale.sweep_stale(client, abandon=True, handoff_path=handoff_path)
    assert any(r.get("abandoned") for r in results)
    assert handoff_path.exists()


def test_sweep_stale_list_error() -> None:
    import sweep_stale
    client = ArchonClient()
    client.run_process = lambda *a, json_output=False: _completed(returncode=1, stderr="DB locked")
    results = sweep_stale.sweep_stale(client)
    assert len(results) == 1
    assert "error" in results[0]


def test_sweep_stale_fetch_error() -> None:
    import sweep_stale
    client = ArchonClient()
    responses = iter([
        _completed(stdout='{"runs": [{"id": "r1", "workflow_name": "wf"}]}'),
        _completed(returncode=1, stderr="not found"),
    ])
    client.run_process = lambda *a, json_output=False: next(responses)
    results = sweep_stale.sweep_stale(client)
    assert len(results) == 1
    assert results[0].get("error") is not None


# ===================================================================
# handoff_new
# ===================================================================

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


# ===================================================================
# extract_handoff_headers
# ===================================================================

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


# ===================================================================
# session_scan
# ===================================================================

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
