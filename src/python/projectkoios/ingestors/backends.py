from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
import os
from pathlib import Path
import urllib.error
import urllib.request


@dataclass(frozen=True, slots=True)
class BackendSelection:
    name: str
    endpoint: str | None = None
    model: str | None = None
    timeout_seconds: int = 60


class BackendAdapter(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class OllamaBackendAdapter(BackendAdapter):
    def __init__(self, endpoint: str | None = None, model: str | None = None, timeout_seconds: int = 60) -> None:
        self._endpoint = endpoint or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self._model = model or os.environ.get("OLLAMA_MODEL", "llama3.2")
        self._timeout_seconds = timeout_seconds

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def model(self) -> str:
        return self._model

    def generate(self, prompt: str) -> str:
        url = f"{self._endpoint.rstrip('/')}/api/generate"
        payload = json.dumps({"model": self._model, "prompt": prompt, "stream": False}).encode("utf-8")
        request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self._timeout_seconds) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, OSError, json.JSONDecodeError, TimeoutError) as exc:
            raise RuntimeError(f"ollama backend unavailable: {exc}") from exc
        text = data.get("response")
        if not isinstance(text, str):
            raise RuntimeError("ollama backend returned no response text")
        return text.strip()


class BackendFactory:
    def from_selection(self, selection: BackendSelection) -> BackendAdapter:
        if selection.name == "ollama":
            return OllamaBackendAdapter(
                endpoint=selection.endpoint,
                model=selection.model,
                timeout_seconds=selection.timeout_seconds,
            )
        raise ValueError(f"unsupported backend: {selection.name}")
