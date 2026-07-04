from __future__ import annotations

import pytest

from projectkoios.ingestors import AnswerFormat, App, BackendAdapter, BackendFactory, BackendSelection

from tests.projectkoios.ingestors._helpers import write_config, write_schema


class FakeBackend(BackendAdapter):
    def __init__(self, *, fail: bool = False) -> None:
        self._fail = fail

    @property
    def name(self) -> str:
        return "fake"

    def generate(self, prompt: str) -> str:
        if self._fail:
            raise RuntimeError("fake backend failure")
        return f"fake answer for prompt containing {prompt.splitlines()[0]}"


class FakeBackendFactory(BackendFactory):
    def __init__(self, *, fail: bool = False) -> None:
        self._fail = fail
        self.selection: BackendSelection | None = None

    def from_selection(self, selection: BackendSelection) -> BackendAdapter:
        self.selection = selection
        return FakeBackend(fail=self._fail)


def test__App__validate_config(tmp_path):
    app = App()
    report = app.validate_config(write_config(tmp_path), schema_path=write_schema(tmp_path))
    assert report.schema_valid is True
    assert report.runtime_valid is True
    assert report.sources == 1


def test__App__answer(tmp_path):
    factory = FakeBackendFactory()
    app = App(backend_factory=factory)
    answer = app.answer(write_config(tmp_path), "ADR Example", schema_path=write_schema(tmp_path), format=AnswerFormat.CITED_SUMMARY)
    assert "fake answer" in answer.text
    assert answer.citations
    assert factory.selection is not None
    assert factory.selection.name == "ollama"
    assert factory.selection.endpoint == "http://localhost:11434"
    assert factory.selection.model == "llama3.2"
    assert factory.selection.timeout_seconds == 60


def test__App__answer__backend_failure_is_explicit_by_default(tmp_path):
    app = App(backend_factory=FakeBackendFactory(fail=True))
    with pytest.raises(RuntimeError, match="backend 'fake' failed"):
        app.answer(write_config(tmp_path), "ADR Example", schema_path=write_schema(tmp_path), format=AnswerFormat.CITED_SUMMARY)


def test__App__answer__backend_failure_can_fallback_by_config(tmp_path):
    config_path = write_config(tmp_path)
    text = config_path.read_text(encoding="utf-8")
    config_path.write_text(text.replace("on_failure: error", "on_failure: fallback"), encoding="utf-8")
    app = App(backend_factory=FakeBackendFactory(fail=True))
    answer = app.answer(config_path, "ADR Example", schema_path=write_schema(tmp_path), format=AnswerFormat.CITED_SUMMARY)
    assert "Answering: ADR Example" in answer.text
    assert answer.citations


def test__App__validate_config__rejects_non_adr_sources(tmp_path):
    app = App()
    config_path = write_config(tmp_path)
    text = config_path.read_text(encoding="utf-8")
    config_path.write_text(text.replace("docs/adr/**/*.md", "docs/**/*.md", 1), encoding="utf-8")
    report = app.validate_config(config_path, schema_path=write_schema(tmp_path))
    assert report.schema_valid is True
    assert report.runtime_valid is False
    assert "ADR-only" in report.issues[0]
