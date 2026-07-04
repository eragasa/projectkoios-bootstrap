from __future__ import annotations

from pathlib import Path
from typing import Callable

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact
from projectkoios.bootstrap.harness.data.marking import HandoffMarking, Marking
from projectkoios.bootstrap.harness.data.violation import Violation
from projectkoios.bootstrap.harness.handoffs.guards import (
    ALL_GUARDS,
)
from projectkoios.bootstrap.harness.handoffs.parser import HandoffParser


PLACE_DIRECTORIES: dict[str, str] = {
    "archon_inbox": "docs/archive/handoffs/archon",
    "opencode_inbox": "docs/archive/handoffs/opencode",
    "pi_inbox": "docs/archive/handoffs/pi",
    "goose_inbox": "docs/archive/handoffs/goose",
}
"""Maps Petri net place names to handoff directory paths relative to repo root."""


class HandoffEvaluator:
    """Orchestrator for the read-only handoff evaluation flow.

    Usage::

        evaluator = HandoffEvaluator(repo_root=Path("."))
        violations = evaluator.evaluate()
        by_file = evaluator.violations_by_file(violations)

    The evaluator owns a ``HandoffParser`` and a list of guard functions.
    Each call to ``evaluate()`` rebuilds the marking from scratch —
    there is no caching or state persistence.
    """

    def __init__(
        self,
        repo_root: Path,
        parser: HandoffParser | None = None,
        guards: list[Callable[[HandoffMarking], list[Violation]]] | None = None,
    ) -> None:
        self.repo_root = repo_root.resolve()
        self.parser = parser or HandoffParser()
        self.guards = guards or list(ALL_GUARDS)

    def build_marking(self) -> HandoffMarking:
        """Parse all handoff directories and return the current marking.

        Iterates ``PLACE_DIRECTORIES``, parses each directory through
        ``self.parser``, and groups the resulting tokens by place name.
        Directories that don't exist or contain no parseable files are
        omitted from the marking.
        """
        tokens_by_place: dict[str, list] = {}
        for place_name, rel_path in PLACE_DIRECTORIES.items():
            dir_path: Path = self.repo_root / rel_path
            tokens: list[HandoffArtifact] = self.parser.parse_directory(dir_path)
            if tokens:
                tokens_by_place[place_name] = tokens

        return Marking(
            tokens_by_place=tokens_by_place,
        )

    def evaluate(self) -> list[Violation]:
        """Build the current marking and run all guards.

        Returns a flat list of ``Violation`` instances aggregated from every
        guard function. Each guard receives the same ``Marking`` and returns
        its own list; the evaluator concatenates them in guard registration
        order.
        """
        marking: HandoffMarking = self.build_marking()
        violations: list[Violation] = []
        for guard_fn in self.guards:
            violations.extend(guard_fn(marking))
        return violations

    def violations_by_file(self, violations: list[Violation]) -> dict[Path, list[Violation]]:
        """Group a violation list by the affected file path.

        Useful for writing violations back to their source files via
        ``append_violations``.
        """
        by_file: dict[Path, list[Violation]] = {}
        for v in violations:
            if v.path not in by_file:
                by_file[v.path] = []
            by_file[v.path].append(v)
        return by_file
