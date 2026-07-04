"""Local Ollama universal chunk-card generator.

Calls local Ollama at ``localhost:11434`` via stdlib ``urllib`` to produce
universal (role-neutral) chunk cards. Degrades gracefully when Ollama is
absent or unreachable: emits a warning, skips chunk-card generation, and
keeps the graph snapshot fresh. No new pip dependencies.
"""

from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
from typing import Any
import urllib.error
import urllib.request

from projectkoios.bootstrap.harness.daemon.activities import DaemonContext
from projectkoios.bootstrap.harness.daemon.data import (
    ChunkCard,
    ChunkCardSet,
    FreshnessState,
    RunMetadata,
)
from projectkoios.bootstrap.harness.daemon.exclusions import ExclusionPolicy


OLLAMA_DEFAULT_ENDPOINT: str = "http://localhost:11434"
OLLAMA_DEFAULT_MODEL: str = "llama3.2"
OLLAMA_TIMEOUT_SECONDS: int = 60
OLLAMA_TAGS_TIMEOUT_SECONDS: int = 5
CHUNK_PROMPT_TEXT_LIMIT: int = 2000
CHUNK_FILE_SNIPPET_LIMIT: int = 1200
CHUNK_PATH_BATCH_SIZE: int = 20
CHUNK_SNIPPET_FILE_LIMIT: int = 4


def log_ollama(message: str) -> None:
    """Print an Ollama daemon message."""
    print(f"[ollama] {message}", flush=True)


def ollama_generate(
    endpoint: str,
    model: str,
    prompt: str,
    timeout: int = OLLAMA_TIMEOUT_SECONDS,
) -> str | None:
    """Call Ollama ``/api/generate`` and return response text when available."""
    url: str = f"{endpoint.rstrip('/')}/api/generate"
    payload: bytes = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    request: urllib.request.Request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body: str = response.read().decode("utf-8")
            data: Any = json.loads(body)
            if not isinstance(data, dict):
                return None
            response_text: object = data.get("response")
            return str(response_text) if response_text is not None else None
    except (urllib.error.URLError, OSError, json.JSONDecodeError, TimeoutError):
        return None


def list_ollama_models(endpoint: str, timeout: int = OLLAMA_TAGS_TIMEOUT_SECONDS) -> list[str]:
    """Return model names reported by Ollama, or an empty list."""
    url: str = f"{endpoint.rstrip('/')}/api/tags"
    request: urllib.request.Request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data: Any = json.loads(response.read().decode("utf-8"))
            if not isinstance(data, dict):
                return []
            models: object = data.get("models", [])
            if not isinstance(models, list):
                return []
            names: list[str] = []
            model: object
            for model in models:
                if isinstance(model, dict):
                    name: object = model.get("name") or model.get("model")
                    if name:
                        names.append(str(name))
            return names
    except (urllib.error.URLError, OSError, TimeoutError, json.JSONDecodeError):
        return []


def check_ollama(endpoint: str, timeout: int = OLLAMA_TAGS_TIMEOUT_SECONDS) -> bool:
    """Return True when Ollama responds to the tags endpoint."""
    return bool(list_ollama_models(endpoint, timeout=timeout))


def resolve_ollama_model(endpoint: str, preferred: str) -> str | None:
    """Resolve a usable model name from Ollama's local registry."""
    models: list[str] = list_ollama_models(endpoint)
    if not models:
        return None
    if preferred in models:
        return preferred
    prefix_matches: list[str] = [
        name for name in models if name.startswith(preferred + ":") or name.startswith(preferred + "-")
    ]
    if prefix_matches:
        return prefix_matches[0]
    return models[0]


def build_chunk_prompt(source_path: str, chunk_text: str) -> str:
    """Build a role-neutral prompt for a universal chunk card."""
    return (
        "Summarise the following code chunk as a concise, role-neutral "
        "orientation card for any AI agent. Do not produce role-specific "
        "review hints, knowledge-ontology entries, or architecture decisions. "
        f"Source file: {source_path}\n\nChunk:\n{chunk_text[:CHUNK_PROMPT_TEXT_LIMIT]}"
    )


def render_dict_chunk(item: dict[Any, Any]) -> tuple[str, str]:
    """Render a Graphify dict-style chunk as source and text."""
    chunk_id: str = str(item.get("id", item.get("chunk_id", "unknown")))
    source: str = str(item.get("source", item.get("file", "unknown")))
    text: str = str(item.get("text", item.get("content", "")))
    return (f"{chunk_id}:{source}", text)


def render_path_snippets(paths: list[Path]) -> tuple[str, str]:
    """Render snippets for a Graphify path batch."""
    if not paths:
        return ("unknown", "")
    snippets: list[str] = []
    path: Path
    for path in paths[:CHUNK_SNIPPET_FILE_LIMIT]:
        try:
            rel: str = path.as_posix()
            text: str = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        snippets.append(f"FILE: {rel}\n{text[:CHUNK_FILE_SNIPPET_LIMIT]}")
    source: str = paths[0].name if len(paths) == 1 else f"{paths[0].name} +{len(paths) - 1} more"
    return (source, "\n\n".join(snippets))


def render_chunk_body(repo_root: Path, item: object) -> tuple[str, str]:
    """Return ``(source_path, chunk_text)`` for a Graphify chunk item."""
    if isinstance(item, dict):
        return render_dict_chunk(item)
    if isinstance(item, list):
        paths: list[Path] = [Path(path) for path in item if isinstance(path, str)]
        return render_path_snippets(paths)
    return ("unknown", "")


def chunk_batches_from_manifest(repo_root: Path) -> list[list[str]]:
    """Build corpus-wide chunk batches from Graphify's manifest when possible."""
    manifest: Path = repo_root / "graphify-out" / "manifest.json"
    if not manifest.exists():
        return []
    try:
        data: Any = json.loads(manifest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, dict):
        return []
    rel_paths: list[str] = [str(path) for path in data]
    batches: list[list[str]] = []
    start: int
    for start in range(0, len(rel_paths), CHUNK_PATH_BATCH_SIZE):
        batch: list[str] = [
            str((repo_root / rel_path).resolve())
            for rel_path in rel_paths[start : start + CHUNK_PATH_BATCH_SIZE]
        ]
        if batch:
            batches.append(batch)
    return batches


def chunk_batch_from_graphify_item(repo_root: Path, item: object) -> list[str]:
    """Convert one Graphify chunk list item into a path batch."""
    if isinstance(item, list):
        return [str(Path(path).resolve()) for path in item if isinstance(path, str)]
    if isinstance(item, dict):
        source: object = item.get("source") or item.get("file")
        text: object = item.get("text") or item.get("content")
        if source or text:
            return [str((repo_root / str(source)).resolve())] if source else []
    return []


def chunk_batches_from_graphify(repo_root: Path) -> list[list[str]]:
    """Return fallback chunk batches from Graphify's chunk list output."""
    chunks_file: Path = repo_root / "graphify-out" / ".graphify_chunks.json"
    if not chunks_file.exists():
        return []
    try:
        chunks_data: Any = json.loads(chunks_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(chunks_data, list):
        return []
    batches: list[list[str]] = [chunk_batch_from_graphify_item(repo_root, item) for item in chunks_data]
    return [batch for batch in batches if batch]


def load_chunk_batches(repo_root: Path) -> tuple[str, list[list[str]]]:
    """Load chunk batches and return their source kind."""
    manifest_batches: list[list[str]] = chunk_batches_from_manifest(repo_root)
    if manifest_batches:
        return ("manifest", manifest_batches)
    return ("graphify_chunks", chunk_batches_from_graphify(repo_root))


def count_eligible_files(repo_root: Path) -> int:
    """Count non-excluded files under the repository root."""
    policy: ExclusionPolicy = ExclusionPolicy.for_repo(repo_root)
    count: int = 0
    dirpath: str
    dirnames: list[str]
    filenames: list[str]
    for dirpath, dirnames, filenames in os.walk(repo_root, topdown=True):
        dir_path: Path = Path(dirpath)
        try:
            dir_path.relative_to(repo_root)
        except ValueError:
            continue
        if policy.is_excluded(dir_path) and dir_path != repo_root:
            dirnames[:] = []
            continue
        pruned: list[str] = [dirname for dirname in dirnames if policy.is_excluded(dir_path / dirname)]
        dirname: str
        for dirname in pruned:
            dirnames.remove(dirname)
        filename: str
        for filename in filenames:
            file_path: Path = dir_path / filename
            if policy.is_excluded(file_path):
                continue
            count += 1
    return count


def count_indexed_files(batches: list[list[str]]) -> int:
    """Count unique paths represented by chunk batches."""
    return len({path for batch in batches for path in batch})


def enrich_run_metadata(
    *,
    metadata: RunMetadata | None,
    resolved_model: str,
    degraded: bool,
    eligible_files_count: int,
    indexed_files_count: int,
    batches_count: int,
    source_kind: str,
    skipped_files_count: int,
) -> RunMetadata | None:
    """Return run metadata enriched with Ollama chunk-card fields."""
    if metadata is None:
        return None
    return replace(
        metadata,
        ollama_model=resolved_model,
        ollama_endpoint=OLLAMA_DEFAULT_ENDPOINT,
        ollama_degraded=degraded,
        eligible_files_count=eligible_files_count,
        indexed_files_count=indexed_files_count,
        chunk_batch_count=batches_count,
        chunk_batch_source=source_kind,
        skipped_paths_count=skipped_files_count,
    )


def make_chunk_card(
    *,
    chunk_id: str,
    source: str,
    text: str,
    resolved_model: str,
) -> tuple[ChunkCard | None, str | None]:
    """Generate one chunk card and return either the card or a failure string."""
    response: str | None = ollama_generate(
        OLLAMA_DEFAULT_ENDPOINT,
        resolved_model,
        build_chunk_prompt(source, text),
    )
    if response is None:
        return (None, f"ollama generation failed for chunk {chunk_id}")
    return (
        ChunkCard(
            chunk_id=chunk_id,
            source_path=source,
            summary=response.strip(),
            model=resolved_model,
        ),
        None,
    )


def generate_chunk_cards(ctx: DaemonContext) -> DaemonContext:
    """Generate universal chunk cards from Graphify chunks via local Ollama."""
    repo_root: Path = Path(ctx.repo_root)
    eligible_files_count: int = count_eligible_files(repo_root)

    log_ollama(f"checking {OLLAMA_DEFAULT_ENDPOINT} for model {OLLAMA_DEFAULT_MODEL}")
    if not check_ollama(OLLAMA_DEFAULT_ENDPOINT):
        log_ollama(f"unreachable at {OLLAMA_DEFAULT_ENDPOINT}; skipping chunk cards")
        return replace(
            ctx,
            warnings=ctx.warnings + (
                f"ollama unreachable at {OLLAMA_DEFAULT_ENDPOINT}; skipping chunk cards",
            ),
        )

    resolved_model: str | None = resolve_ollama_model(OLLAMA_DEFAULT_ENDPOINT, OLLAMA_DEFAULT_MODEL)
    if resolved_model is None:
        return replace(
            ctx,
            warnings=ctx.warnings + ("ollama reported no usable models; skipping chunk cards",),
        )
    log_ollama(f"using model {resolved_model}")

    loaded_batches: tuple[str, list[list[str]]] = load_chunk_batches(repo_root)
    source_kind: str = loaded_batches[0]
    batches: list[list[str]] = loaded_batches[1]
    if not batches:
        return replace(
            ctx,
            warnings=ctx.warnings + ("no graphify chunk inputs found; skipping chunk cards",),
        )

    indexed_files_count: int = count_indexed_files(batches)
    skipped_files_count: int = max(eligible_files_count - indexed_files_count, 0)
    log_ollama(
        f"summary eligible={eligible_files_count} indexed={indexed_files_count} "
        f"batches={len(batches)} skipped={skipped_files_count} source={source_kind}"
    )

    cards: list[ChunkCard] = []
    failures: list[str] = []
    log_ollama(f"processing {len(batches)} batch(es) from {source_kind}")
    index: int
    batch: list[str]
    for index, batch in enumerate(batches, start=1):
        rendered_chunk: tuple[str, str] = render_chunk_body(repo_root, batch)
        source: str = rendered_chunk[0]
        text: str = rendered_chunk[1]
        if not text:
            log_ollama(f"batch {index}/{len(batches)} skipped (no readable content)")
            continue
        chunk_id: str = f"chunk-{index}"
        log_ollama(f"batch {index}/{len(batches)} source={source}")
        card_result: tuple[ChunkCard | None, str | None] = make_chunk_card(
            chunk_id=chunk_id,
            source=source,
            text=text,
            resolved_model=resolved_model,
        )
        card: ChunkCard | None = card_result[0]
        failure: str | None = card_result[1]
        if failure is not None:
            failures.append(failure)
            log_ollama(f"batch {index}/{len(batches)} failed")
            continue
        if card is not None:
            cards.append(card)
        log_ollama(f"batch {index}/{len(batches)} complete")

    degraded: bool = bool(failures) and len(failures) >= len(cards) if cards else bool(failures)
    log_ollama(f"finished cards={len(cards)} failures={len(failures)} degraded={degraded}")
    card_set: ChunkCardSet = ChunkCardSet(
        run_id=ctx.run_id,
        path="",
        card_count=len(cards),
        model=resolved_model,
        degraded=degraded,
    )

    new_warnings: tuple[str, ...] = tuple(failures) if failures else ()
    new_freshness: FreshnessState = (
        FreshnessState.DEGRADED if degraded and ctx.freshness == FreshnessState.UPDATING else ctx.freshness
    )

    enriched_metadata: RunMetadata | None = enrich_run_metadata(
        metadata=ctx.metadata,
        resolved_model=resolved_model,
        degraded=degraded,
        eligible_files_count=eligible_files_count,
        indexed_files_count=indexed_files_count,
        batches_count=len(batches),
        source_kind=source_kind,
        skipped_files_count=skipped_files_count,
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
