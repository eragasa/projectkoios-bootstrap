"""Dormant candidate helper for bounded adversarial-review packets."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Iterable

SCHEMA_VERSION: Final = 1
MAX_ARTIFACTS: Final = 16
MAX_ARTIFACT_BYTES: Final = 131_072
MAX_TOTAL_ARTIFACT_BYTES: Final = 262_144
MAX_LOCATOR_BYTES: Final = 512
MAX_SCOPE_BYTES: Final = 4_096
READ_CHUNK_BYTES: Final = 65_536
OPEN_DELIMITER: Final = "<architecture-review-packet>"
CLOSE_DELIMITER: Final = "</architecture-review-packet>"
SHA256_PATTERN: Final = re.compile(r"[0-9a-f]{64}\Z")
TOP_LEVEL_FIELDS: Final = frozenset({"artifacts", "schema_version", "scope"})
ARTIFACT_FIELDS: Final = frozenset({"byte_length", "content", "locator", "sha256"})


class PacketError(ValueError):
    """The requested packet violates the candidate contract."""


@dataclass(frozen=True)
class BuiltPacket:
    """Validated serialized packet and content identity."""

    text: str
    sha256: str
    artifact_bytes: int


def _utf8_bytes(value: str, field: str) -> bytes:
    try:
        return value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise PacketError(f"{field} is not valid UTF-8") from error


def _validate_locator(locator: str) -> tuple[str, ...]:
    if not locator or "\\" in locator or "\x00" in locator:
        raise PacketError("locator must be a non-empty POSIX path")
    if len(_utf8_bytes(locator, "artifact locator")) > MAX_LOCATOR_BYTES:
        raise PacketError("locator exceeds byte limit")
    parts = locator.split("/")
    if locator.startswith("/") or any(part in {"", ".", ".."} for part in parts):
        raise PacketError("locator must be normalized and repository-relative")
    return tuple(parts)


def _read_regular_file(root_fd: int, locator: str) -> bytes:
    parts = _validate_locator(locator)
    directory_fd = os.dup(root_fd)
    try:
        for part in parts[:-1]:
            next_fd = os.open(
                part,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=directory_fd,
            )
            os.close(directory_fd)
            directory_fd = next_fd
        file_fd = os.open(
            parts[-1],
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | getattr(os, "O_NONBLOCK", 0),
            dir_fd=directory_fd,
        )
        try:
            metadata = os.fstat(file_fd)
            if not stat.S_ISREG(metadata.st_mode):
                raise PacketError(f"artifact is not a regular file: {locator}")
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = os.read(file_fd, READ_CHUNK_BYTES)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_ARTIFACT_BYTES:
                    raise PacketError(f"artifact exceeds byte limit: {locator}")
                chunks.append(chunk)
            return b"".join(chunks)
        finally:
            os.close(file_fd)
    except OSError as error:
        raise PacketError(f"artifact cannot be opened safely: {locator}") from error
    finally:
        os.close(directory_fd)


def _artifact(locator: str, raw: bytes) -> dict[str, object]:
    try:
        content = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise PacketError(f"artifact is not UTF-8: {locator}") from error
    return {
        "byte_length": len(raw),
        "content": content,
        "locator": locator,
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def _serialize(packet: dict[str, object]) -> str:
    text = json.dumps(
        packet,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return text.replace("<", "\\u003c").replace(">", "\\u003e")


def build_packet(repository: Path, locators: Iterable[str], scope: str) -> BuiltPacket:
    """Read one closed allowlist through descriptor-confined no-follow opens."""

    locator_list = list(locators)
    if not 1 <= len(locator_list) <= MAX_ARTIFACTS:
        raise PacketError("artifact count is outside candidate limits")
    if len(set(locator_list)) != len(locator_list):
        raise PacketError("artifact locators must be unique")
    if (
        not isinstance(scope, str)
        or not scope
        or len(_utf8_bytes(scope, "scope")) > MAX_SCOPE_BYTES
    ):
        raise PacketError("scope is empty or exceeds its byte limit")
    if repository.is_symlink():
        raise PacketError("repository root must not be a symlink")

    root_fd = os.open(
        repository,
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
    )
    try:
        artifacts: list[dict[str, object]] = []
        artifact_bytes = 0
        for locator in locator_list:
            raw = _read_regular_file(root_fd, locator)
            artifact_bytes += len(raw)
            if artifact_bytes > MAX_TOTAL_ARTIFACT_BYTES:
                raise PacketError("aggregate artifact bytes exceed candidate limit")
            artifacts.append(_artifact(locator, raw))
    finally:
        os.close(root_fd)

    packet: dict[str, object] = {
        "artifacts": artifacts,
        "schema_version": SCHEMA_VERSION,
        "scope": scope,
    }
    text = _serialize(packet)
    validate_packet_text(text)
    return BuiltPacket(
        text=text,
        sha256=hashlib.sha256((text + "\n").encode("utf-8")).hexdigest(),
        artifact_bytes=artifact_bytes,
    )


def _require_exact_fields(value: dict[str, Any], expected: frozenset[str]) -> None:
    if set(value) != expected:
        raise PacketError("packet contains missing or unknown fields")


def _reject_duplicate_fields(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise PacketError(f"packet contains duplicate field: {key}")
        value[key] = item
    return value


def validate_packet_text(text: str) -> dict[str, object]:
    """Validate serialized packet structure, bounds, identities, and escaping."""

    if "<" in text or ">" in text:
        raise PacketError("packet JSON must escape angle brackets")
    try:
        value = json.loads(text, object_pairs_hook=_reject_duplicate_fields)
    except json.JSONDecodeError as error:
        raise PacketError("packet is not valid JSON") from error
    if not isinstance(value, dict):
        raise PacketError("packet must be a JSON object")
    _require_exact_fields(value, TOP_LEVEL_FIELDS)
    if (
        type(value["schema_version"]) is not int
        or value["schema_version"] != SCHEMA_VERSION
    ):
        raise PacketError("unsupported packet schema version")

    scope = value["scope"]
    if (
        not isinstance(scope, str)
        or not scope
        or len(_utf8_bytes(scope, "scope")) > MAX_SCOPE_BYTES
    ):
        raise PacketError("scope is empty or exceeds its byte limit")
    artifacts = value["artifacts"]
    if not isinstance(artifacts, list) or not 1 <= len(artifacts) <= MAX_ARTIFACTS:
        raise PacketError("artifact count is outside candidate limits")

    locators: set[str] = set()
    aggregate = 0
    for item in artifacts:
        if not isinstance(item, dict):
            raise PacketError("artifact entry must be an object")
        _require_exact_fields(item, ARTIFACT_FIELDS)
        locator = item["locator"]
        content = item["content"]
        byte_length = item["byte_length"]
        digest = item["sha256"]
        if not isinstance(locator, str):
            raise PacketError("artifact locator must be a string")
        _validate_locator(locator)
        if locator in locators:
            raise PacketError("artifact locators must be unique")
        locators.add(locator)
        if not isinstance(content, str):
            raise PacketError("artifact content must be a string")
        raw = _utf8_bytes(content, "artifact content")
        if len(raw) > MAX_ARTIFACT_BYTES:
            raise PacketError("artifact exceeds byte limit")
        if type(byte_length) is not int or byte_length != len(raw):
            raise PacketError("artifact byte length does not match content")
        if not isinstance(digest, str) or SHA256_PATTERN.fullmatch(digest) is None:
            raise PacketError("artifact SHA-256 has invalid syntax")
        if hashlib.sha256(raw).hexdigest() != digest:
            raise PacketError("artifact SHA-256 does not match content")
        aggregate += len(raw)
        if aggregate > MAX_TOTAL_ARTIFACT_BYTES:
            raise PacketError("aggregate artifact bytes exceed candidate limit")
    if _serialize(value) != text:
        raise PacketError("packet JSON is not canonical")
    return value


def render_task(packet_text: str, focus: str) -> str:
    """Return one delimiter-safe user task after complete packet validation."""

    validate_packet_text(packet_text)
    if OPEN_DELIMITER in focus or CLOSE_DELIMITER in focus:
        raise PacketError("focus must not contain packet delimiters")
    task = f"{focus.rstrip()}\n{OPEN_DELIMITER}\n{packet_text}\n{CLOSE_DELIMITER}"
    if task.count(OPEN_DELIMITER) != 1 or task.count(CLOSE_DELIMITER) != 1:
        raise PacketError("task must contain exactly one lexical packet envelope")
    return task
