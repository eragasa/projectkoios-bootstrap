from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from projectkoios.ingestors.index import GraphIndex, Section


DEFAULT_RETRIEVAL_LIMIT: int = 3
DEFAULT_EXCERPT_WIDTH: int = 280


@dataclass(frozen=True, slots=True)
class Evidence:
    """Retrieved evidence section for a GraphRAG answer.

    Args:
        path: Absolute source path for the evidence.
        relative_path: Repository-relative source path.
        title: Section title.
        line_start: First source line included in the evidence.
        line_end: Last source line included in the evidence.
        excerpt: Compact evidence excerpt.
        score: Retrieval score for the matched section.
        page: Optional page number for citation-style sources.
        bibtex_key: Optional BibTeX key for citation-style sources.
    """

    path: Path
    relative_path: str
    title: str
    line_start: int
    line_end: int
    excerpt: str
    score: int
    page: int | None = None
    bibtex_key: str | None = None

    @property
    def citation(self) -> str:
        """Return the preferred citation label for this evidence."""
        if self.bibtex_key is not None and self.page is not None:
            return f"{self.bibtex_key}, p. {self.page}"
        if self.bibtex_key is not None:
            return self.bibtex_key
        return f"{self.relative_path}:{self.line_start}-{self.line_end}"


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    """Evidence returned for one retrieval query.

    Args:
        query: Original query text.
        depth: Section-neighbor expansion depth used for retrieval.
        evidence: Retrieved evidence items.
    """

    query: str
    depth: int
    evidence: tuple[Evidence, ...]


class Retriever:
    """Simple lexical retriever over a persisted graph index."""

    def retrieve(self, index: GraphIndex, query: str, *, depth: int = 1, limit: int = DEFAULT_RETRIEVAL_LIMIT) -> RetrievalResult:
        """Retrieve evidence for a query from an index.

        Args:
            index: Graph index containing source sections.
            query: Query text to match lexically.
            depth: Number of neighboring sections to include around a match.
            limit: Maximum number of evidence items to return.

        Returns:
            Retrieval result containing evidence in ranked order.
        """

        # Terms are normalized query tokens used for lexical matching.
        terms: tuple[str, ...] = self.terms(query)
        # Ranked contains scored sections sorted by score and stable source position.
        ranked: list[tuple[int, Section]] = sorted(
            (self.score(section, terms) for section in index.sections),
            key=lambda item: (-item[0], item[1].relative_path, item[1].line_start),
        )
        # Evidence accumulates returned sections after neighbor expansion.
        evidence: list[Evidence] = []
        # Seen prevents duplicate section evidence after expansion.
        seen: set[tuple[Path, int, int]] = set()
        score: int
        section: Section
        for score, section in ranked:
            if score <= 0:
                continue
            neighbour: Section
            for neighbour in self.expand(index.sections, section, depth=depth):
                # Key identifies one source span for duplicate suppression.
                key: tuple[Path, int, int] = (neighbour.path, neighbour.line_start, neighbour.line_end)
                if key in seen:
                    continue
                seen.add(key)
                evidence.append(
                    Evidence(
                        path=neighbour.path,
                        relative_path=neighbour.relative_path,
                        title=neighbour.title,
                        line_start=neighbour.line_start,
                        line_end=neighbour.line_end,
                        excerpt=self.excerpt(neighbour.text),
                        score=score,
                        page=neighbour.page,
                        bibtex_key=neighbour.bibtex_key,
                    )
                )
                if len(evidence) >= limit:
                    return RetrievalResult(query=query, depth=depth, evidence=tuple(evidence))
        return RetrievalResult(query=query, depth=depth, evidence=tuple(evidence))

    def terms(self, query: str) -> tuple[str, ...]:
        """Return normalized non-empty query terms.

        Args:
            query: Raw query text.

        Returns:
            Lower-cased query terms stripped of punctuation.
        """

        # Words are lower-cased token candidates after punctuation stripping.
        words: list[str] = [word.strip(".,:;!?()[]{}\"'` ").lower() for word in query.split()]
        return tuple(word for word in words if word)

    def score(self, section: Section, terms: tuple[str, ...]) -> tuple[int, Section]:
        """Score a section for query terms.

        Args:
            section: Candidate section to score.
            terms: Normalized query terms.

        Returns:
            Pair of score and original section.
        """

        # Haystack includes both title and body text for body-term scoring.
        haystack: str = f"{section.title}\n{section.text}".lower()
        # Score weights title hits higher than body hits.
        score: int = sum(2 for term in terms if term in section.title.lower())
        score += sum(1 for term in terms if term in haystack)
        return (score, section)

    def expand(self, sections: Iterable[Section], target: Section, *, depth: int) -> tuple[Section, ...]:
        """Expand one target section to neighboring sections in the same source.

        Args:
            sections: All sections available for expansion.
            target: Matched target section.
            depth: Number of positions to include around the target.

        Returns:
            Tuple of neighboring sections including the target.
        """

        # Group contains sections from the same relative source path as the target.
        group: list[Section] = [section for section in sections if section.relative_path == target.relative_path]
        if not group:
            return (target,)
        # Sorted group is ordered by source line for neighbor slicing.
        sorted_group: list[Section] = sorted(group, key=lambda section: section.line_start)
        # Index locates the target section inside its source group.
        index: int = sorted_group.index(target)
        # Left is the inclusive start index for neighbor slicing.
        left: int = max(0, index - (depth - 1))
        # Right is the exclusive end index for neighbor slicing.
        right: int = min(len(sorted_group), index + depth)
        return tuple(sorted_group[left:right])

    def excerpt(self, text: str, width: int = DEFAULT_EXCERPT_WIDTH) -> str:
        """Return a compact excerpt bounded to a maximum width.

        Args:
            text: Source section text.
            width: Maximum excerpt width.

        Returns:
            Single-line excerpt, truncated with an ellipsis when needed.
        """

        # Compact text removes repeated whitespace for concise evidence display.
        compact: str = " ".join(text.split())
        if len(compact) <= width:
            return compact
        return compact[: width - 1] + "…"
