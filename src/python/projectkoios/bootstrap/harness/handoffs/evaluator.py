from __future__ import annotations

from pathlib import Path
from typing import Callable

from projectkoios.bootstrap.harness.actions.guards import (
    ALL_GUARDS,
)
from projectkoios.bootstrap.harness.data.artifact import ArtifactToken
from projectkoios.bootstrap.harness.data.marking import Marking
from projectkoios.bootstrap.harness.data.violation import Violation
from projectkoios.bootstrap.harness.handoffs.parser import HandoffParser


PLACE_DIRECTORIES: dict[str, str] = {
    "archon_inbox": "archon/handoffs",
    "opencode_inbox": "opencode/handoffs",
    "pi_inbox": "pi/handoffs",
    "goose_inbox": "goose/handoffs",
}


class HandoffEvaluator:
    def __init__(
        self,
        repo_root: Path,
        parser: HandoffParser | None = None,
        guards: list[tuple[str, Callable[[Marking], list[Violation]]]] | None = None,
    ) -> None:
        self.repo_root = repo_root.resolve()
        self.parser = parser or HandoffParser()
        self.guards = guards or ALL_GUARDS

    def build_marking(self) -> Marking:
        tokens_by_place: dict[str, list[ArtifactToken]] = {}
        for place_name, rel_path in PLACE_DIRECTORIES.items():
            dir_path = self.repo_root / rel_path
            tokens = self.parser.parse_directory(dir_path)
            if tokens:
                tokens_by_place[place_name] = tokens

        return Marking(
            tokens_by_place=tokens_by_place,
            source_root=self.repo_root,
        )

    def evaluate(self) -> list[Violation]:
        marking = self.build_marking()
        violations: list[Violation] = []
        for _name, guard_fn in self.guards:
            violations.extend(guard_fn(marking))
        return violations

    def violations_by_file(self, violations: list[Violation]) -> dict[Path, list[Violation]]:
        by_file: dict[Path, list[Violation]] = {}
        for v in violations:
            path = Path(v.token_path).resolve() if v.token_path else Path()
            if path not in by_file:
                by_file[path] = []
            by_file[path].append(v)
        return by_file
