from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from projectkoios.bootstrap.harness.data.marking import Marking
from projectkoios.bootstrap.harness.data.violation import Violation


@dataclass(frozen=True)
class TransitionResult:
    ok: bool
    action: str
    violations: list[Violation] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


class ActionObject(Protocol):
    def enabled(self, marking: Marking) -> TransitionResult: ...
    def apply(self, marking: Marking) -> TransitionResult: ...
