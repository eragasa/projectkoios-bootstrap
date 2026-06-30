"""Local Ollama universal chunk-card generator.

Calls local Ollama at ``localhost:11434`` via stdlib ``urllib`` to produce
universal (role-neutral) chunk cards. Degrades gracefully when Ollama is
absent or unreachable: emits a warning, skips chunk-card generation, and
keeps the graph snapshot fresh. No new pip dependencies.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

from projectkoios.bootstrap.harness.daemon.activities import DaemonContext
from projectkoios.bootstrap.harness.daemon.data import (
    ChunkCard,
    ChunkCardSet,
    FreshnessState,
)


OLLAMA_DEFAULT_ENDPOINT = "http://localhost:11434"
OLLAMA_DEFAULT_MODEL = "llama3.2"
OLLAMA_TIMEOUT_SECONDS = 60


def _ollama_generate(
    endpoint: str,
    model: str,
    prompt: str,
    timeout: int = OLLAMA_TIMEOUT_SECONDS,
) -> str | None:
    """Call Ollama ``/api/generate`` and return the response text, or None on failure."""
    url = f"{endpoint.rstrip('/')}/api/generate"
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            data = json.loads(body)
            return data.get("response")
    except (urllib.error.URLError, OSError, json.JSONDecodeError, TimeoutError):
        return None


def _check_ollama(endpoint: str, timeout: int = 5) -> bool:
    """Quick connectivity check — returns True if Ollama responds."""
    url = f"{endpoint.rstrip('/')}/api/tags"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as _:
            return True
    except (urllib.error.URLError, OSError, TimeoutError):
        return False


def _build_chunk_prompt(source_path: str, chunk_text: str) -> str:
    """Build a role-neutral prompt for a universal chunk card.

    The prompt asks for a concise, role-neutral summary suitable for any
    agent. It explicitly avoids role-specific overlays, review hints, or
    knowledge-ontology language.
    """
    return (
        "Summarise the following code chunk as a concise, role-neutral "
        "orientation card for any AI agent. Do not produce role-specific "
        "review hints, knowledge-ontology entries, or architecture decisions. "
        f"Source file: {source_path}\n\nChunk:\n{chunk_text[:2000]}"
    )


def generate_chunk_cards(ctx: DaemonContext) -> DaemonContext:
    """Generate universal chunk cards from Graphify chunks via local Ollama.

    Degrades gracefully: if Ollama is unreachable, returns the context with a
    warning, no chunk-card set, and keeps the freshness state from the graph
    build. If some chunks fail, records partial failures.
    """
    from dataclasses import replace

    repo_root = Path(ctx.repo_root)
    chunks_file = repo_root / "graphify-out" / ".graphify_chunks.json"
    if not chunks_file.exists():
        return replace(
            ctx,
            warnings=ctx.warnings + ("no graphify chunks file found; skipping chunk cards",),
        )

    if not _check_ollama(OLLAMA_DEFAULT_ENDPOINT):
        return replace(
            ctx,
            warnings=ctx.warnings + (
                f"ollama unreachable at {OLLAMA_DEFAULT_ENDPOINT}; skipping chunk cards",
            ),
        )

    try:
        chunks_data = json.loads(chunks_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return replace(
            ctx,
            warnings=ctx.warnings + (f"failed to read chunks file: {exc}",),
        )

    cards: list[ChunkCard] = []
    failures: list[str] = []
    items = chunks_data if isinstance(chunks_data, list) else list(chunks_data.values())
    for item in items[:20]:
        if not isinstance(item, dict):
            continue
        chunk_id = str(item.get("id", item.get("chunk_id", "unknown")))
        source = str(item.get("source", item.get("file", "unknown")))
        text = str(item.get("text", item.get("content", "")))
        if not text:
            continue
        response = _ollama_generate(
            OLLAMA_DEFAULT_ENDPOINT,
            OLLAMA_DEFAULT_MODEL,
            _build_chunk_prompt(source, text),
        )
        if response is None:
            failures.append(f"ollama generation failed for chunk {chunk_id}")
            continue
        cards.append(ChunkCard(
            chunk_id=chunk_id,
            source_path=source,
            summary=response.strip(),
            model=OLLAMA_DEFAULT_MODEL,
        ))

    degraded = bool(failures) and len(failures) >= len(cards) if cards else bool(failures)
    card_set = ChunkCardSet(
        run_id=ctx.run_id,
        path="",  # filled by publisher
        card_count=len(cards),
        model=OLLAMA_DEFAULT_MODEL,
        degraded=degraded,
    )

    new_warnings = tuple(failures) if failures else ()
    new_freshness = FreshnessState.DEGRADED if degraded and ctx.freshness == FreshnessState.UPDATING else ctx.freshness

    return replace(
        ctx,
        chunk_card_set=card_set,
        chunk_cards=tuple(cards),
        failures=ctx.failures + tuple(failures),
        warnings=ctx.warnings + new_warnings,
        freshness=new_freshness,
    )
