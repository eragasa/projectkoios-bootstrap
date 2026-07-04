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
from typing import TypeAlias, cast
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


JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]

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


def read_json_value(text: str) -> JsonValue | None:
    """Parse JSON text into the local JSON value alias."""
    # Value is absent when JSON decoding fails.
    value: JsonValue | None = None
    try:
        value = cast(JsonValue, json.loads(text))
    except json.JSONDecodeError:
        value = None
    return value


def ollama_generate(
    endpoint: str,
    model: str,
    prompt: str,
    timeout: int = OLLAMA_TIMEOUT_SECONDS,
) -> str | None:
    """Call Ollama ``/api/generate`` and return response text when available."""
    # URL targets the Ollama generate endpoint for the selected local server.
    url: str = f"{endpoint.rstrip('/')}/api/generate"
    # Payload is the JSON request body expected by Ollama.
    payload: bytes = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    # Request carries the POST body and content-type header.
    request: urllib.request.Request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    # Response text remains absent when Ollama cannot generate a usable response.
    response_text: str | None = None
    try:
        # Response body is the raw bytes returned by Ollama.
        response_body: bytes = urllib.request.urlopen(request, timeout=timeout).read()
        # Body is decoded as UTF-8 JSON before response extraction.
        body: str = response_body.decode("utf-8")
        # Data is the parsed Ollama response object.
        data: JsonValue | None = read_json_value(body)
        if isinstance(data, dict):
            # Raw response is the generated text field from Ollama.
            raw_response: JsonValue = data.get("response")
            response_text = str(raw_response) if raw_response is not None else None
    except (urllib.error.URLError, OSError, TimeoutError):
        response_text = None
    return response_text


def list_ollama_models(endpoint: str, timeout: int = OLLAMA_TAGS_TIMEOUT_SECONDS) -> list[str]:
    """Return model names reported by Ollama, or an empty list."""
    # URL targets the Ollama tags endpoint for local model discovery.
    url: str = f"{endpoint.rstrip('/')}/api/tags"
    # Request is a simple GET against the tags endpoint.
    request: urllib.request.Request = urllib.request.Request(url, method="GET")
    # Names accumulates model names from a successful tags response.
    names: list[str] = []
    try:
        # Response body contains Ollama model metadata as JSON.
        response_body: bytes = urllib.request.urlopen(request, timeout=timeout).read()
        # Data is the parsed tags response object.
        data: JsonValue | None = read_json_value(response_body.decode("utf-8"))
        if isinstance(data, dict):
            # Models is the raw models list from the tags response.
            models: JsonValue = data.get("models", [])
            if isinstance(models, list):
                model: JsonValue
                for model in models:
                    if isinstance(model, dict):
                        # Name is the model identifier field accepted by generate.
                        name: JsonValue = model.get("name") or model.get("model")
                        if name:
                            names.append(str(name))
    except (urllib.error.URLError, OSError, TimeoutError):
        names = []
    return names


def check_ollama(endpoint: str, timeout: int = OLLAMA_TAGS_TIMEOUT_SECONDS) -> bool:
    """Return True when Ollama responds to the tags endpoint."""
    return bool(list_ollama_models(endpoint, timeout=timeout))


def resolve_ollama_model(endpoint: str, preferred: str) -> str | None:
    """Resolve a usable model name from Ollama's local registry."""
    # Models are the locally available Ollama model names.
    models: list[str] = list_ollama_models(endpoint)
    if not models:
        return None
    if preferred in models:
        return preferred
    # Prefix matches allow preferred base names to resolve tagged variants.
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


def render_dict_chunk(item: JsonObject) -> tuple[str, str]:
    """Render a Graphify dict-style chunk as source and text."""
    # Chunk ID prefers explicit chunk fields and falls back to unknown.
    chunk_id: str = str(item.get("id", item.get("chunk_id", "unknown")))
    # Source prefers Graphify source/file fields and falls back to unknown.
    source: str = str(item.get("source", item.get("file", "unknown")))
    # Text prefers Graphify text/content fields and falls back to empty content.
    text: str = str(item.get("text", item.get("content", "")))
    return (f"{chunk_id}:{source}", text)


def render_path_snippets(paths: list[Path]) -> tuple[str, str]:
    """Render snippets for a Graphify path batch."""
    if not paths:
        return ("unknown", "")
    # Snippets accumulates readable file previews for the prompt body.
    snippets: list[str] = []
    path: Path
    for path in paths[:CHUNK_SNIPPET_FILE_LIMIT]:
        try:
            # Relative display path is currently represented as POSIX input path.
            rel: str = path.as_posix()
            # Text is a bounded UTF-8 source preview for the chunk prompt.
            text: str = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        snippets.append(f"FILE: {rel}\n{text[:CHUNK_FILE_SNIPPET_LIMIT]}")
    # Source summarizes one file or a batch of multiple files.
    source: str = paths[0].name if len(paths) == 1 else f"{paths[0].name} +{len(paths) - 1} more"
    return (source, "\n\n".join(snippets))


def render_chunk_body(repo_root: Path, item: object) -> tuple[str, str]:
    """Return ``(source_path, chunk_text)`` for a Graphify chunk item."""
    if isinstance(item, dict):
        return render_dict_chunk(cast(JsonObject, item))
    if isinstance(item, list):
        # Paths converts string list entries into path objects for snippet rendering.
        paths: list[Path] = [Path(path) for path in item if isinstance(path, str)]
        return render_path_snippets(paths)
    return ("unknown", "")


def chunk_batches_from_manifest(repo_root: Path) -> list[list[str]]:
    """Build corpus-wide chunk batches from Graphify's manifest when possible."""
    # Manifest is Graphify's generated file list and metadata surface.
    manifest: Path = repo_root / "graphify-out" / "manifest.json"
    if not manifest.exists():
        return []
    # Data is absent when the manifest cannot be read or parsed.
    data: JsonValue | None = None
    try:
        data = read_json_value(manifest.read_text(encoding="utf-8"))
    except OSError:
        data = None
    if not isinstance(data, dict):
        return []
    # Relative paths are manifest keys that identify indexed files.
    rel_paths: list[str] = [str(path) for path in data]
    # Batches groups manifest paths into bounded prompt batches.
    batches: list[list[str]] = []
    start: int
    for start in range(0, len(rel_paths), CHUNK_PATH_BATCH_SIZE):
        # Batch contains absolute path strings consumed by snippet rendering.
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
        # Source is the file path field when Graphify emits object chunks.
        source: object = item.get("source") or item.get("file")
        # Text indicates the object contains usable chunk content.
        text: object = item.get("text") or item.get("content")
        if source or text:
            return [str((repo_root / str(source)).resolve())] if source else []
    return []


def chunk_batches_from_graphify(repo_root: Path) -> list[list[str]]:
    """Return fallback chunk batches from Graphify's chunk list output."""
    # Chunks file is Graphify's optional chunk-list output.
    chunks_file: Path = repo_root / "graphify-out" / ".graphify_chunks.json"
    if not chunks_file.exists():
        return []
    # Chunks data is absent when the chunk list cannot be read or parsed.
    chunks_data: JsonValue | None = None
    try:
        chunks_data = read_json_value(chunks_file.read_text(encoding="utf-8"))
    except OSError:
        chunks_data = None
    if not isinstance(chunks_data, list):
        return []
    # Batches converts each Graphify item into a path batch and removes empties.
    batches: list[list[str]] = [chunk_batch_from_graphify_item(repo_root, item) for item in chunks_data]
    return [batch for batch in batches if batch]


def load_chunk_batches(repo_root: Path) -> tuple[str, list[list[str]]]:
    """Load chunk batches and return their source kind."""
    # Manifest batches are preferred because they cover the corpus-wide file set.
    manifest_batches: list[list[str]] = chunk_batches_from_manifest(repo_root)
    if manifest_batches:
        return ("manifest", manifest_batches)
    return ("graphify_chunks", chunk_batches_from_graphify(repo_root))


def count_eligible_files(repo_root: Path) -> int:
    """Count non-excluded files under the repository root."""
    # Policy applies repository exclusion rules during traversal.
    policy: ExclusionPolicy = ExclusionPolicy.for_repo(repo_root)
    # Count accumulates eligible file totals.
    count: int = 0
    dirpath: str
    dirnames: list[str]
    filenames: list[str]
    for dirpath, dirnames, filenames in os.walk(repo_root, topdown=True):
        # Directory path is the current os.walk directory.
        dir_path: Path = Path(dirpath)
        try:
            dir_path.relative_to(repo_root)
        except ValueError:
            continue
        if policy.is_excluded(dir_path) and dir_path != repo_root:
            dirnames[:] = []
            continue
        # Pruned contains excluded child directories removed from traversal.
        pruned: list[str] = [dirname for dirname in dirnames if policy.is_excluded(dir_path / dirname)]
        dirname: str
        for dirname in pruned:
            dirnames.remove(dirname)
        filename: str
        for filename in filenames:
            # File path is the candidate file counted when not excluded.
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
    # Response is the Ollama-generated summary text when generation succeeds.
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
    # Repository root is the daemon context path converted for filesystem operations.
    repo_root: Path = Path(ctx.repo_root)
    # Eligible file count records all non-excluded repository files for metadata.
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

    # Resolved model is the concrete local Ollama model used for generation.
    resolved_model: str | None = resolve_ollama_model(OLLAMA_DEFAULT_ENDPOINT, OLLAMA_DEFAULT_MODEL)
    if resolved_model is None:
        return replace(
            ctx,
            warnings=ctx.warnings + ("ollama reported no usable models; skipping chunk cards",),
        )
    log_ollama(f"using model {resolved_model}")

    # Loaded batches includes the source kind and concrete path batches.
    loaded_batches: tuple[str, list[list[str]]] = load_chunk_batches(repo_root)
    # Source kind identifies which Graphify artifact produced the batches.
    source_kind: str = loaded_batches[0]
    # Batches contains path groups rendered into chunk-card prompts.
    batches: list[list[str]] = loaded_batches[1]
    if not batches:
        return replace(
            ctx,
            warnings=ctx.warnings + ("no graphify chunk inputs found; skipping chunk cards",),
        )

    # Indexed file count records unique files represented by the chunk batches.
    indexed_files_count: int = count_indexed_files(batches)
    # Skipped file count estimates eligible files not represented by chunk batches.
    skipped_files_count: int = max(eligible_files_count - indexed_files_count, 0)
    log_ollama(
        f"summary eligible={eligible_files_count} indexed={indexed_files_count} "
        f"batches={len(batches)} skipped={skipped_files_count} source={source_kind}"
    )

    # Cards accumulates successful generated chunk cards.
    cards: list[ChunkCard] = []
    # Failures accumulates per-chunk generation failures.
    failures: list[str] = []
    log_ollama(f"processing {len(batches)} batch(es) from {source_kind}")
    index: int
    batch: list[str]
    for index, batch in enumerate(batches, start=1):
        # Rendered chunk contains source label and prompt text.
        rendered_chunk: tuple[str, str] = render_chunk_body(repo_root, batch)
        # Source is the human-readable source label for the chunk card.
        source: str = rendered_chunk[0]
        # Text is the rendered chunk body passed to Ollama.
        text: str = rendered_chunk[1]
        if not text:
            log_ollama(f"batch {index}/{len(batches)} skipped (no readable content)")
            continue
        # Chunk ID is a stable ordinal identifier within this daemon run.
        chunk_id: str = f"chunk-{index}"
        log_ollama(f"batch {index}/{len(batches)} source={source}")
        # Card result contains either a generated card or a failure string.
        card_result: tuple[ChunkCard | None, str | None] = make_chunk_card(
            chunk_id=chunk_id,
            source=source,
            text=text,
            resolved_model=resolved_model,
        )
        # Card is present when generation succeeded.
        card: ChunkCard | None = card_result[0]
        # Failure is present when generation failed.
        failure: str | None = card_result[1]
        if failure is not None:
            failures.append(failure)
            log_ollama(f"batch {index}/{len(batches)} failed")
            continue
        if card is not None:
            cards.append(card)
        log_ollama(f"batch {index}/{len(batches)} complete")

    # Degraded records whether failures are severe enough to mark card generation degraded.
    degraded: bool = bool(failures) and len(failures) >= len(cards) if cards else bool(failures)
    log_ollama(f"finished cards={len(cards)} failures={len(failures)} degraded={degraded}")
    # Card set summarizes the generated chunk cards for publisher metadata.
    card_set: ChunkCardSet = ChunkCardSet(
        run_id=ctx.run_id,
        path="",
        card_count=len(cards),
        model=resolved_model,
        degraded=degraded,
    )

    # New warnings surface generation failures without hiding graph freshness.
    new_warnings: tuple[str, ...] = tuple(failures) if failures else ()
    # New freshness marks the run degraded only while the run is still updating.
    new_freshness: FreshnessState = (
        FreshnessState.DEGRADED if degraded and ctx.freshness == FreshnessState.UPDATING else ctx.freshness
    )

    # Enriched metadata adds chunk-card counts and Ollama details when metadata exists.
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
