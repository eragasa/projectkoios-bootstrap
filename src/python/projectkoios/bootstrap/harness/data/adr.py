from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class AdrStatus(StrEnum):
    """Lifecycle status values for architecture decision records."""

    DRAFT = "draft"
    ACCEPTED = "accepted"
    COMPLETED = "completed"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"


@dataclass(frozen=True)
class ArchitecturalDataRecord:
    """An Architecture Decision Record (ADR).

    Maps to ADR files under ``docs/adr/`` with stable semantic filenames such
    as ``adr.<topic>.md`` or ``adr.<topic>.<status>.md``.
    Provides a programmatic view independent of the file format.
    """

    id: str
    title: str
    status: AdrStatus
    context: str
    decision: str
    consequences: str
    rationale: str | None = None
    alternatives: list[str] = field(default_factory=list)
    supersedes: str | None = None
    non_goals: list[str] = field(default_factory=list)
    priority: str | None = None
    created: str | None = None
    path: Path | None = None
