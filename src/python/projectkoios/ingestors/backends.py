from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
import os
from typing import Any
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
        self.endpoint_value: str = endpoint or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self.model_value: str = model or os.environ.get("OLLAMA_MODEL", "llama3.2")
        self.timeout_seconds: int = timeout_seconds

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def endpoint(self) -> str:
        return self.endpoint_value

    @property
    def model(self) -> str:
        return self.model_value

    def generate(self, prompt: str) -> str:
        url: str = f"{self.endpoint_value.rstrip('/')}/api/generate"
        payload: bytes = json.dumps({"model": self.model_value, "prompt": prompt, "stream": False}).encode("utf-8")
        request: urllib.request.Request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                data: Any = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, OSError, json.JSONDecodeError, TimeoutError) as exc:
            raise RuntimeError(f"ollama backend unavailable: {exc}") from exc
        if not isinstance(data, dict):
            raise RuntimeError("ollama backend returned non-object response")
        text: object = data.get("response")
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
