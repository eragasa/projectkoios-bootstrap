from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Place:
    name: str
    accepted_kinds: tuple[str, ...]
    owner_harness: str | None = None
    description: str | None = None
