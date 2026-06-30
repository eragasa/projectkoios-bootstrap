"""Local Ollama universal chunk-card generator.

Calls local Ollama at ``localhost:11434`` via stdlib ``urllib`` to produce
universal (role-neutral) chunk cards. Degrades gracefully when Ollama is
absent or unreachable: emits a warning, skips chunk-card generation, and
keeps the graph snapshot fresh. No new pip dependencies.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from projectkoios.bootstrap.harness.daemon.activities import DaemonContext
from projectkoios.bootstrap.harness.daemon.data import (
    ChunkCard,
    ChunkCardSet,
    FreshnessState,
)
from projectkoios.bootstrap.harness.daemon.exclusions import ExclusionPolicy


OLLAMA_DEFAULT_ENDPOINT = "http://localhost:11434"
OLLAMA_DEFAULT_MODEL = "llama3.2"
OLLAMA_TIMEOUT_SECONDS = 60


def _log(message: str) -> None:
    print(f"[ollama] {message}", flush=True)


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


def _list_ollama_models(endpoint: str, timeout: int = 5) -> list[str]:
    """Return the list of model names reported by Ollama, or an empty list."""
    url = f"{endpoint.rstrip('/')}/api/tags"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = data.get("models", [])
            names: list[str] = []
            for model in models:
                if isinstance(model, dict):
                    name = model.get("name") or model.get("model")
                    if name:
                        names.append(str(name))
            return names
    except (urllib.error.URLError, OSError, TimeoutError, json.JSONDecodeError):
        return []


def _check_ollama(endpoint: str, timeout: int = 5) -> bool:
    """Quick connectivity check — returns True if Ollama responds."""
    return bool(_list_ollama_models(endpoint, timeout=timeout))


def _resolve_ollama_model(endpoint: str, preferred: str) -> str | None:
    """Resolve a usable model name from Ollama's local registry.

    Prefers an exact match, then a prefix match (``llama3.2`` → ``llama3.2:1b``),
    then falls back to the first available model.
    """
    models = _list_ollama_models(endpoint)
    if not models:
        return None
    if preferred in models:
        return preferred
    prefix_matches = [name for name in models if name.startswith(preferred + ":") or name.startswith(preferred + "-")]
    if prefix_matches:
        return prefix_matches[0]
    return models[0]


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


def _render_chunk_body(repo_root: Path, item: object) -> tuple[str, str]:
    """Return ``(source_path, chunk_text)`` for a Graphify chunk item.

    Graphify's chunk output can vary by extractor shape. The first daemon slice
    supports dict-style chunks with embedded text and list-style chunks that
    contain repo file paths. For list-style chunks, the prompt is built from a
    small snippet of each referenced file so Ollama receives actual content.
    """
    if isinstance(item, dict):
        chunk_id = str(item.get("id", item.get("chunk_id", "unknown")))
        source = str(item.get("source", item.get("file", "unknown")))
        text = str(item.get("text", item.get("content", "")))
        return (f"{chunk_id}:{source}", text)

    if isinstance(item, list):
        paths = [Path(p) for p in item if isinstance(p, str)]
        if not paths:
            return ("unknown", "")
        snippets: list[str] = []
        for path in paths[:4]:
            try:
                rel = path.as_posix()
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            snippets.append(f"FILE: {rel}\n{text[:1200]}")
        source = paths[0].name if len(paths) == 1 else f"{paths[0].name} +{len(paths) - 1} more"
        return (source, "\n\n".join(snippets))

    return ("unknown", "")


def _chunk_batches_from_manifest(repo_root: Path) -> list[list[str]]:
    """Build corpus-wide chunk batches from Graphify's manifest when possible."""
    manifest = repo_root / "graphify-out" / "manifest.json"
    if not manifest.exists():
        return []
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, dict):
        return []
    rel_paths = [str(p) for p in data.keys()]
    batches: list[list[str]] = []
    for i in range(0, len(rel_paths), 20):
        batch = [str((repo_root / rel).resolve()) for rel in rel_paths[i : i + 20]]
        if batch:
            batches.append(batch)
    return batches


def _chunk_batches_from_graphify(repo_root: Path) -> list[list[str]]:
    """Fallback chunk batches from Graphify's chunk list output."""
    chunks_file = repo_root / "graphify-out" / ".graphify_chunks.json"
    if not chunks_file.exists():
        return []
    try:
        chunks_data = json.loads(chunks_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(chunks_data, list):
        return []
    batches: list[list[str]] = []
    for item in chunks_data:
        if isinstance(item, list):
            paths = [str(Path(p).resolve()) for p in item if isinstance(p, str)]
            if paths:
                batches.append(paths)
        elif isinstance(item, dict):
            source = item.get("source") or item.get("file")
            text = item.get("text") or item.get("content")
            if source or text:
                batches.append([str((repo_root / str(source)).resolve())] if source else [])
    return [b for b in batches if b]


def _load_chunk_batches(repo_root: Path) -> tuple[str, list[list[str]]]:
    manifest_batches = _chunk_batches_from_manifest(repo_root)
    if manifest_batches:
        return ("manifest", manifest_batches)
    return ("graphify_chunks", _chunk_batches_from_graphify(repo_root))


def _count_eligible_files(repo_root: Path) -> int:
    policy = ExclusionPolicy.for_repo(repo_root)
    count = 0
    for dirpath, dirnames, filenames in os.walk(repo_root, topdown=True):
        dir_path = Path(dirpath)
        try:
            dir_path.relative_to(repo_root)
        except ValueError:
            continue
        if policy.is_excluded(dir_path) and dir_path != repo_root:
            dirnames[:] = []
            continue
        pruned: list[str] = []
        for d in dirnames:
            if policy.is_excluded(dir_path / d):
                pruned.append(d)
        for d in pruned:
            dirnames.remove(d)
        for fname in filenames:
            fpath = dir_path / fname
            if policy.is_excluded(fpath):
                continue
            count += 1
    return count


def _count_indexed_files(batches: list[list[str]]) -> int:
    return len({path for batch in batches for path in batch})


def generate_chunk_cards(ctx: DaemonContext) -> DaemonContext:
    """Generate universal chunk cards from Graphify chunks via local Ollama.

    Degrades gracefully: if Ollama is unreachable, returns the context with a
    warning, no chunk-card set, and keeps the freshness state from the graph
    build. If some chunks fail, records partial failures.
    """
    from dataclasses import replace

    repo_root = Path(ctx.repo_root)
    eligible_files_count = _count_eligible_files(repo_root)

    _log(f"checking {OLLAMA_DEFAULT_ENDPOINT} for model {OLLAMA_DEFAULT_MODEL}")
    if not _check_ollama(OLLAMA_DEFAULT_ENDPOINT):
        _log(f"unreachable at {OLLAMA_DEFAULT_ENDPOINT}; skipping chunk cards")
        return replace(
            ctx,
            warnings=ctx.warnings + (
                f"ollama unreachable at {OLLAMA_DEFAULT_ENDPOINT}; skipping chunk cards",
            ),
        )

    resolved_model = _resolve_ollama_model(OLLAMA_DEFAULT_ENDPOINT, OLLAMA_DEFAULT_MODEL)
    if resolved_model is None:
        return replace(
            ctx,
            warnings=ctx.warnings + ("ollama reported no usable models; skipping chunk cards",),
        )
    _log(f"using model {resolved_model}")

    source_kind, batches = _load_chunk_batches(repo_root)
    if not batches:
        return replace(
            ctx,
            warnings=ctx.warnings + ("no graphify chunk inputs found; skipping chunk cards",),
        )

    indexed_files_count = _count_indexed_files(batches)
    skipped_files_count = max(eligible_files_count - indexed_files_count, 0)
    _log(
        f"summary eligible={eligible_files_count} indexed={indexed_files_count} "
        f"batches={len(batches)} skipped={skipped_files_count} source={source_kind}"
    )

    cards: list[ChunkCard] = []
    failures: list[str] = []
    _log(f"processing {len(batches)} batch(es) from {source_kind}")
    for index, batch in enumerate(batches, start=1):
        source, text = _render_chunk_body(repo_root, batch)
        if not text:
            _log(f"batch {index}/{len(batches)} skipped (no readable content)")
            continue
        chunk_id = f"chunk-{index}"
        _log(f"batch {index}/{len(batches)} source={source}")
        response = _ollama_generate(
            OLLAMA_DEFAULT_ENDPOINT,
            resolved_model,
            _build_chunk_prompt(source, text),
        )
        if response is None:
            failures.append(f"ollama generation failed for chunk {chunk_id}")
            _log(f"batch {index}/{len(batches)} failed")
            continue
        cards.append(ChunkCard(
            chunk_id=chunk_id,
            source_path=source,
            summary=response.strip(),
            model=resolved_model,
        ))
        _log(f"batch {index}/{len(batches)} complete")

    degraded = bool(failures) and len(failures) >= len(cards) if cards else bool(failures)
    _log(f"finished cards={len(cards)} failures={len(failures)} degraded={degraded}")
    card_set = ChunkCardSet(
        run_id=ctx.run_id,
        path="",  # filled by publisher
        card_count=len(cards),
        model=resolved_model,
        degraded=degraded,
    )

    new_warnings = tuple(failures) if failures else ()
    new_freshness = FreshnessState.DEGRADED if degraded and ctx.freshness == FreshnessState.UPDATING else ctx.freshness

    enriched_metadata = None
    if ctx.metadata is not None:
        enriched_metadata = replace(
            ctx.metadata,
            ollama_model=resolved_model,
            ollama_endpoint=OLLAMA_DEFAULT_ENDPOINT,
            ollama_degraded=degraded,
            eligible_files_count=eligible_files_count,
            indexed_files_count=indexed_files_count,
            chunk_batch_count=len(batches),
            chunk_batch_source=source_kind,
            skipped_paths_count=skipped_files_count,
        )

    return replace(
        ctx,
        chunk_card_set=card_set,
        chunk_cards=tuple(cards),
        failures=ctx.failures + tuple(failures),
        warnings=ctx.warnings + new_warnings,
        freshness=new_freshness,
        metadata=enriched_metadata or ctx.metadata,
    )
