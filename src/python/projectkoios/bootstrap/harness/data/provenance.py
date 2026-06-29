from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Authority:
    level: int
    basis: str


LEVELS: tuple[Authority, ...] = (
    Authority(1, "explicit user instruction"),
    Authority(2, "current repository state"),
    Authority(3, "passing tests / executable validation"),
    Authority(4, "approved architecture specification"),
    Authority(5, "acceptance criteria"),
    Authority(6, "implementation report"),
    Authority(7, "knowledge note"),
    Authority(8, "agent inference"),
)


@dataclass(frozen=True)
class Provenance:
    origin: str
    sender: str
    acting_as: str | None = None
    delegated_operator: str | None = None
    repository: str | None = None
    source_artifacts: tuple[str, ...] = ()
