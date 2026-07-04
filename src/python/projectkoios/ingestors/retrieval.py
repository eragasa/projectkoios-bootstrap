from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from projectkoios.ingestors.index import GraphIndex, Section


DEFAULT_RETRIEVAL_LIMIT: int = 3
DEFAULT_EXCERPT_WIDTH: int = 280


@dataclass(frozen=True, slots=True)
class Evidence:
    path: Path
    relative_path: str
    title: str
    line_start: int
    line_end: int
    excerpt: str
    score: int

    @property
    def citation(self) -> str:
        return f"{self.relative_path}:{self.line_start}-{self.line_end}"


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    query: str
    depth: int
    evidence: tuple[Evidence, ...]


class Retriever:
    def retrieve(self, index: GraphIndex, query: str, *, depth: int = 1, limit: int = DEFAULT_RETRIEVAL_LIMIT) -> RetrievalResult:
        terms: tuple[str, ...] = self.terms(query)
        ranked: list[tuple[int, Section]] = sorted(
            (self.score(section, terms) for section in index.sections),
            key=lambda item: (-item[0], item[1].relative_path, item[1].line_start),
        )
        evidence: list[Evidence] = []
        seen: set[tuple[Path, int, int]] = set()
        score: int
        section: Section
        for score, section in ranked:
            if score <= 0:
                continue
            neighbour: Section
            for neighbour in self.expand(index.sections, section, depth=depth):
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
                    )
                )
                if len(evidence) >= limit:
                    return RetrievalResult(query=query, depth=depth, evidence=tuple(evidence))
        return RetrievalResult(query=query, depth=depth, evidence=tuple(evidence))

    def terms(self, query: str) -> tuple[str, ...]:
        words: list[str] = [word.strip(".,:;!?()[]{}\"'` ").lower() for word in query.split()]
        return tuple(word for word in words if word)

    def score(self, section: Section, terms: tuple[str, ...]) -> tuple[int, Section]:
        haystack: str = f"{section.title}\n{section.text}".lower()
        score: int = sum(2 for term in terms if term in section.title.lower())
        score += sum(1 for term in terms if term in haystack)
        return (score, section)

    def expand(self, sections: Iterable[Section], target: Section, *, depth: int) -> tuple[Section, ...]:
        group: list[Section] = [section for section in sections if section.relative_path == target.relative_path]
        if not group:
            return (target,)
        sorted_group: list[Section] = sorted(group, key=lambda section: section.line_start)
        index: int = sorted_group.index(target)
        left: int = max(0, index - (depth - 1))
        right: int = min(len(sorted_group), index + depth)
        return tuple(sorted_group[left:right])

    def excerpt(self, text: str, width: int = DEFAULT_EXCERPT_WIDTH) -> str:
        compact: str = " ".join(text.split())
        if len(compact) <= width:
            return compact
        return compact[: width - 1] + "…"
