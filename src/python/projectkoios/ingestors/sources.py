from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

from projectkoios.ingestors.config import Config


@dataclass(frozen=True, slots=True)
class SourceDocument:
    path: Path
    relative_path: str
    text: str
    line_count: int


@dataclass(frozen=True, slots=True)
class SourceSet:
    root: Path
    documents: tuple[SourceDocument, ...]

    @property
    def paths(self) -> tuple[Path, ...]:
        return tuple(document.path for document in self.documents)


class SourceResolver:
    def resolve(self, config: Config) -> SourceSet:
        root: Path = config.root
        includes: tuple[str, ...] = config.source_includes()
        if not includes:
            raise ValueError("no source include patterns defined")

        documents: list[SourceDocument] = []
        pattern: str
        for pattern in includes:
            matches: list[Path] = sorted(root.glob(pattern))
            if not matches:
                raise FileNotFoundError(f"no files matched include pattern: {pattern}")
            match: Path
            for match in matches:
                if not match.is_file():
                    continue
                if self.is_excluded(match, root, config.source_excludes()):
                    continue
                text: str = match.read_text(encoding="utf-8")
                documents.append(
                    SourceDocument(
                        path=match.resolve(),
                        relative_path=str(match.relative_to(root)),
                        text=text,
                        line_count=max(len(text.splitlines()), 1),
                    )
                )
        unique: dict[Path, SourceDocument] = {document.path: document for document in documents}
        ordered: tuple[SourceDocument, ...] = tuple(sorted(unique.values(), key=lambda item: item.relative_path))
        if not ordered:
            raise FileNotFoundError("no source files resolved after exclusions")
        return SourceSet(root=root, documents=ordered)

    def is_excluded(self, path: Path, root: Path, patterns: tuple[str, ...]) -> bool:
        rel: str = str(path.relative_to(root)).replace("\\", "/")
        return any(fnmatch(rel, pattern) for pattern in patterns)
