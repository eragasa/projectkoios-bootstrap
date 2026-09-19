from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.candidates.adversarial_architecture_packet import (
    CLOSE_DELIMITER,
    MAX_ARTIFACT_BYTES,
    OPEN_DELIMITER,
    PacketError,
    build_packet,
    render_task,
    validate_packet_text,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def serialized_packet(**overrides: object) -> str:
    content = "bounded evidence\n"
    packet: dict[str, object] = {
        "artifacts": [
            {
                "byte_length": len(content.encode()),
                "content": content,
                "locator": "docs/proposal.md",
                "sha256": hashlib.sha256(content.encode()).hexdigest(),
            }
        ],
        "schema_version": 1,
        "scope": "Review one bounded proposal.",
    }
    packet.update(overrides)
    return (
        json.dumps(packet, separators=(",", ":"), sort_keys=True)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def test_builder_reads_closed_allowlist_and_renders_one_envelope(
    tmp_path: Path,
) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    proposal = docs / "proposal.md"
    proposal.write_text("proposal <untrusted>\n", encoding="utf-8")

    built = build_packet(tmp_path, ["docs/proposal.md"], "Review the proposal.")
    value = validate_packet_text(built.text)
    task = render_task(built.text, "Review only the supplied packet.")

    assert value["artifacts"][0]["content"] == "proposal <untrusted>\n"  # type: ignore[index]
    assert "<untrusted>" not in built.text
    assert built.artifact_bytes == proposal.stat().st_size
    assert task.count(OPEN_DELIMITER) == 1
    assert task.count(CLOSE_DELIMITER) == 1


@pytest.mark.parametrize(
    "locator",
    [
        "/absolute.md",
        "../escape.md",
        "docs/../escape.md",
        "docs/./proposal.md",
        "docs//proposal.md",
        "docs\\proposal.md",
        "",
    ],
)
def test_builder_rejects_non_normalized_locator(tmp_path: Path, locator: str) -> None:
    with pytest.raises(PacketError):
        build_packet(tmp_path, [locator], "Review scope.")


def test_builder_rejects_symlink_components(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.md").write_text("secret", encoding="utf-8")
    (tmp_path / "linked").symlink_to(outside, target_is_directory=True)

    with pytest.raises(PacketError, match="cannot be opened safely"):
        build_packet(tmp_path, ["linked/secret.md"], "Review scope.")


def test_builder_rejects_oversized_artifact(tmp_path: Path) -> None:
    (tmp_path / "large.md").write_bytes(b"x" * (MAX_ARTIFACT_BYTES + 1))

    with pytest.raises(PacketError, match="exceeds byte limit"):
        build_packet(tmp_path, ["large.md"], "Review scope.")


def test_builder_rejects_fifo_without_blocking(tmp_path: Path) -> None:
    fifo = tmp_path / "artifact.fifo"
    os.mkfifo(fifo)
    code = """
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[2])
from scripts.candidates.adversarial_architecture_packet import PacketError, build_packet
try:
    build_packet(Path(sys.argv[1]), ["artifact.fifo"], "Review scope.")
except PacketError:
    print("rejected")
else:
    raise SystemExit("FIFO was accepted")
"""
    completed = subprocess.run(
        [sys.executable, "-c", code, str(tmp_path), str(REPOSITORY_ROOT)],
        check=True,
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert completed.stdout == "rejected\n"


def test_builder_rejects_non_utf8_scope_value(tmp_path: Path) -> None:
    (tmp_path / "artifact.md").write_text("evidence", encoding="utf-8")
    with pytest.raises(PacketError, match="scope is not valid UTF-8"):
        build_packet(tmp_path, ["artifact.md"], "\ud800")


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ({"schema_version": 2}, "schema version"),
        ({"schema_version": True}, "schema version"),
        ({"extra": True}, "missing or unknown fields"),
        ({"scope": ""}, "scope"),
        ({"artifacts": []}, "artifact count"),
    ],
)
def test_validator_rejects_invalid_top_level_contract(
    mutation: dict[str, object], message: str
) -> None:
    with pytest.raises(PacketError, match=message):
        validate_packet_text(serialized_packet(**mutation))


def test_validator_rejects_duplicate_json_fields_and_noncanonical_text() -> None:
    duplicate = serialized_packet().replace(
        '"schema_version":1', '"schema_version":1,"schema_version":1'
    )
    with pytest.raises(PacketError, match="duplicate field"):
        validate_packet_text(duplicate)

    noncanonical = json.dumps(json.loads(serialized_packet()), indent=2, sort_keys=True)
    with pytest.raises(PacketError, match="not canonical"):
        validate_packet_text(noncanonical)


def test_validator_rejects_invalid_unicode_as_packet_error() -> None:
    with pytest.raises(PacketError, match="scope is not valid UTF-8"):
        validate_packet_text(serialized_packet(scope="\ud800"))

    value = json.loads(serialized_packet())
    value["artifacts"][0]["locator"] = "\ud800"
    locator_text = json.dumps(value, separators=(",", ":"), sort_keys=True)
    with pytest.raises(PacketError, match="locator is not valid UTF-8"):
        validate_packet_text(locator_text)

    value = json.loads(serialized_packet())
    value["artifacts"][0]["content"] = "\ud800"
    content_text = json.dumps(value, separators=(",", ":"), sort_keys=True)
    with pytest.raises(PacketError, match="content is not valid UTF-8"):
        validate_packet_text(content_text)


def test_validator_rejects_duplicate_locator_and_hash_mismatch() -> None:
    value = json.loads(serialized_packet())
    duplicate = dict(value["artifacts"][0])
    value["artifacts"].append(duplicate)
    duplicate_text = json.dumps(value, separators=(",", ":"), sort_keys=True)
    with pytest.raises(PacketError, match="unique"):
        validate_packet_text(duplicate_text)

    value = json.loads(serialized_packet())
    value["artifacts"][0]["sha256"] = "0" * 64
    mismatch_text = json.dumps(value, separators=(",", ":"), sort_keys=True)
    with pytest.raises(PacketError, match="does not match"):
        validate_packet_text(mismatch_text)


def test_validator_rejects_literal_angle_bracket_and_focus_delimiter() -> None:
    unsafe = (
        serialized_packet(scope="review <unsafe>")
        .replace("\\u003c", "<")
        .replace("\\u003e", ">")
    )
    with pytest.raises(PacketError, match="escape angle brackets"):
        validate_packet_text(unsafe)

    with pytest.raises(PacketError, match="must not contain"):
        render_task(serialized_packet(), f"invalid {OPEN_DELIMITER}")
