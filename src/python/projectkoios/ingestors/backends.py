from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
import os
from typing import TypeAlias, cast
import urllib.error
import urllib.request


JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]


@dataclass(frozen=True, slots=True)
class BackendSelection:
    """Backend selection settings for answer generation.

    Args:
        name: Backend adapter name.
        endpoint: Optional backend endpoint override.
        model: Optional model override.
        timeout_seconds: Backend request timeout in seconds.
    """

    name: str
    endpoint: str | None = None
    model: str | None = None
    timeout_seconds: int = 60


class BackendAdapter(ABC):
    """Abstract text-generation backend used by answer composition."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the backend adapter name."""
        raise NotImplementedError

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate response text for a prompt.

        Args:
            prompt: Prompt text to send to the backend.

        Returns:
            Generated response text.
        """

        raise NotImplementedError


class OllamaBackendAdapter(BackendAdapter):
    """Ollama-backed answer-generation adapter."""

    def __init__(self, endpoint: str | None = None, model: str | None = None, timeout_seconds: int = 60) -> None:
        self.endpoint_value: str = endpoint or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self.model_value: str = model or os.environ.get("OLLAMA_MODEL", "llama3.2")
        self.timeout_seconds: int = timeout_seconds

    @property
    def name(self) -> str:
        """Return the backend adapter name."""
        return "ollama"

    @property
    def endpoint(self) -> str:
        """Return the configured Ollama endpoint."""
        return self.endpoint_value

    @property
    def model(self) -> str:
        """Return the configured Ollama model name."""
        return self.model_value

    def generate(self, prompt: str) -> str:
        """Generate response text from Ollama.

        Args:
            prompt: Prompt text to send to Ollama.

        Returns:
            Generated response text.

        Raises:
            RuntimeError: If Ollama is unavailable or returns malformed output.
        """

        # URL targets Ollama's generate endpoint for the configured server.
        url: str = f"{self.endpoint_value.rstrip('/')}/api/generate"
        # Payload is the JSON request body expected by Ollama.
        payload: bytes = json.dumps({"model": self.model_value, "prompt": prompt, "stream": False}).encode("utf-8")
        # Request contains method, headers, and encoded payload for urllib.
        request: urllib.request.Request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        try:
            # Response body contains the raw JSON bytes returned by Ollama.
            response_body: bytes = urllib.request.urlopen(request, timeout=self.timeout_seconds).read()
            # Data is the parsed JSON response object from Ollama.
            data: JsonValue = cast(JsonValue, json.loads(response_body.decode("utf-8")))
        except (urllib.error.URLError, OSError, json.JSONDecodeError, TimeoutError):
            raise RuntimeError("ollama backend unavailable") from None
        if not isinstance(data, dict):
            raise RuntimeError("ollama backend returned non-object response")
        # Text is the generated response value from the Ollama response object.
        text: JsonValue = data.get("response")
        if not isinstance(text, str):
            raise RuntimeError("ollama backend returned no response text")
        return text.strip()


class BackendFactory:
    """Factory for constructing answer-generation backend adapters."""

    def from_selection(self, selection: BackendSelection) -> BackendAdapter:
        """Create a backend adapter from a backend selection.

        Args:
            selection: Backend selection settings.

        Returns:
            Configured backend adapter.
        """

        if selection.name == "ollama":
            return OllamaBackendAdapter(
                endpoint=selection.endpoint,
                model=selection.model,
                timeout_seconds=selection.timeout_seconds,
            )
        raise ValueError(f"unsupported backend: {selection.name}")
