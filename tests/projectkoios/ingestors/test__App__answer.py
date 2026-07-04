from __future__ import annotations

from pathlib import Path

import pytest

from projectkoios.ingestors import Answer, AnswerFormat, App, BackendAdapter, BackendFactory, BackendSelection, PersistedIndexReport, ValidationReport

from tests.projectkoios.ingestors._helpers import write_config, write_schema


class FakeBackend(BackendAdapter):
    """Backend adapter fixture that can return text or fail on demand."""

    def __init__(self, *, fail: bool = False) -> None:
        self._fail: bool = fail

    @property
    def name(self) -> str:
        """Return the backend fixture name."""
        return "fake"

    def generate(self, prompt: str) -> str:
        """Generate a deterministic fake answer for a prompt."""
        if self._fail:
            raise RuntimeError("fake backend failure")
        return f"fake answer for prompt containing {prompt.splitlines()[0]}"


class FakeBackendFactory(BackendFactory):
    """Backend factory fixture that records the requested backend selection."""

    def __init__(self, *, fail: bool = False) -> None:
        self._fail: bool = fail
        self.selection: BackendSelection | None = None

    def from_selection(self, selection: BackendSelection) -> BackendAdapter:
        """Return a fake backend for the selected backend settings."""
        self.selection = selection
        return FakeBackend(fail=self._fail)


def test__App__validate_config(tmp_path: Path) -> None:
    """Validate that app config validation accepts the minimal fixture."""
    # App owns runtime and schema validation orchestration.
    app: App = App()
    # Report captures schema validity, runtime validity, and source count.
    report: ValidationReport = app.validate_config(write_config(tmp_path), schema_path=write_schema(tmp_path))
    assert report.schema_valid is True
    assert report.runtime_valid is True
    assert report.sources == 1


def test__App__persist_index(tmp_path: Path) -> None:
    """Validate that the app persists a deterministic GraphRAG index."""
    # App owns persisted-index orchestration for the fixture config.
    app: App = App()
    # Config path anchors persisted output under the temp directory.
    config_path: Path = write_config(tmp_path)
    # Report describes persisted output and indexed source counts.
    report: PersistedIndexReport = app.persist_index(config_path, schema_path=write_schema(tmp_path))

    assert report.sources == 1
    assert report.sections > 0
    assert report.output_path == tmp_path / "graph" / "index.json"
    assert report.output_path.exists()
    assert "docs/adr/adr.example.md" in report.output_path.read_text(encoding="utf-8")


def test__App__answer(tmp_path: Path) -> None:
    """Validate that the app answers through the configured backend factory."""
    # Factory records backend settings selected from config.
    factory: FakeBackendFactory = FakeBackendFactory()
    # App uses the fake backend factory to avoid network dependencies.
    app: App = App(backend_factory=factory)
    # Answer contains text and citations produced from the fixture index.
    answer: Answer = app.answer(write_config(tmp_path), "ADR Example", schema_path=write_schema(tmp_path), format=AnswerFormat.CITED_SUMMARY)
    assert "fake answer" in answer.text
    assert answer.citations
    assert factory.selection is not None
    assert factory.selection.name == "ollama"
    assert factory.selection.endpoint == "http://localhost:11434"
    assert factory.selection.model == "llama3.2"
    assert factory.selection.timeout_seconds == 60


def test__App__answer__backend_failure_is_explicit_by_default(tmp_path: Path) -> None:
    """Validate that default backend failures are raised explicitly."""
    # App is configured with a backend that raises during generation.
    app: App = App(backend_factory=FakeBackendFactory(fail=True))
    with pytest.raises(RuntimeError, match="backend 'fake' failed"):
        app.answer(write_config(tmp_path), "ADR Example", schema_path=write_schema(tmp_path), format=AnswerFormat.CITED_SUMMARY)


def test__App__answer__backend_failure_can_fallback_by_config(tmp_path: Path) -> None:
    """Validate that fallback config converts backend failure to fallback text."""
    # Config is rewritten to request fallback behavior on backend failure.
    config_path: Path = write_config(tmp_path)
    # Text holds the editable YAML fixture content.
    text: str = config_path.read_text(encoding="utf-8")
    config_path.write_text(text.replace("on_failure: error", "on_failure: fallback"), encoding="utf-8")
    # App uses a backend factory that fails during answer generation.
    app: App = App(backend_factory=FakeBackendFactory(fail=True))
    # Answer should fall back to deterministic local text and preserve citations.
    answer: Answer = app.answer(config_path, "ADR Example", schema_path=write_schema(tmp_path), format=AnswerFormat.CITED_SUMMARY)
    assert "Answering: ADR Example" in answer.text
    assert answer.citations


def test__App__validate_config__rejects_non_adr_sources(tmp_path: Path) -> None:
    """Validate that runtime validation rejects non-ADR source globs."""
    # App owns runtime source-scope validation.
    app: App = App()
    # Config path is rewritten to include a non-ADR glob.
    config_path: Path = write_config(tmp_path)
    # Text holds the editable YAML fixture content.
    text: str = config_path.read_text(encoding="utf-8")
    config_path.write_text(text.replace("docs/adr/**/*.md", "docs/**/*.md", 1), encoding="utf-8")
    # Report should keep schema validity while failing runtime validation.
    report: ValidationReport = app.validate_config(config_path, schema_path=write_schema(tmp_path))
    assert report.schema_valid is True
    assert report.runtime_valid is False
    assert "ADR-only" in report.issues[0]
