from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

from projectkoios.ingestors.config import Config


@dataclass(frozen=True, slots=True)
class SourceDocument:
    """Resolved source document used by the ingestion pipeline.

    Args:
        path: Absolute filesystem path to the source file.
        relative_path: Repository-relative display path.
        text: UTF-8 source text.
        line_count: Source line count, with a minimum of one.
    """

    path: Path
    relative_path: str
    text: str
    line_count: int


@dataclass(frozen=True, slots=True)
class SourceSet:
    """Collection of source documents resolved for one config.

    Args:
        root: Root directory used for source resolution.
        documents: Resolved source documents in deterministic order.
    """

    root: Path
    documents: tuple[SourceDocument, ...]

    @property
    def paths(self) -> tuple[Path, ...]:
        """Return source document paths in source-set order."""
        return tuple(document.path for document in self.documents)


class SourceResolver:
    """Resolve configured source include and exclude patterns into documents."""

    def resolve(self, config: Config) -> SourceSet:
        """Resolve source documents for a validated ingestion config.

        Args:
            config: Ingestion configuration containing root and source patterns.

        Returns:
            Resolved source set in deterministic order.
        """

        # Root is the base directory for include and exclude pattern resolution.
        root: Path = config.root
        # Includes are glob patterns selecting source files for ingestion.
        includes: tuple[str, ...] = config.source_includes()
        if not includes:
            raise ValueError("no source include patterns defined")

        # Documents accumulates matched, readable, non-excluded source files.
        documents: list[SourceDocument] = []
        pattern: str
        for pattern in includes:
            # Matches are sorted to keep source resolution deterministic.
            matches: list[Path] = sorted(root.glob(pattern))
            if not matches:
                raise FileNotFoundError(f"no files matched include pattern: {pattern}")
            match: Path
            for match in matches:
                if not match.is_file():
                    continue
                if self.is_excluded(match, root, config.source_excludes()):
                    continue
                # Text is read once and reused for both content and line counting.
                text: str = match.read_text(encoding="utf-8")
                documents.append(
                    SourceDocument(
                        path=match.resolve(),
                        relative_path=str(match.relative_to(root)),
                        text=text,
                        line_count=max(len(text.splitlines()), 1),
                    )
                )
        # Unique removes duplicate paths that matched multiple include patterns.
        unique: dict[Path, SourceDocument] = {document.path: document for document in documents}
        # Ordered is the deterministic final source document tuple.
        ordered: tuple[SourceDocument, ...] = tuple(sorted(unique.values(), key=lambda item: item.relative_path))
        if not ordered:
            raise FileNotFoundError("no source files resolved after exclusions")
        return SourceSet(root=root, documents=ordered)

    def is_excluded(self, path: Path, root: Path, patterns: tuple[str, ...]) -> bool:
        """Return whether a source path matches configured exclude patterns.

        Args:
            path: Candidate source file path.
            root: Source root for relative-path calculation.
            patterns: Exclude patterns to match.

        Returns:
            True when the candidate path should be excluded.
        """

        # Relative path is normalized to POSIX separators for pattern matching.
        rel: str = str(path.relative_to(root)).replace("\\", "/")
        return any(fnmatch(rel, pattern) for pattern in patterns)
