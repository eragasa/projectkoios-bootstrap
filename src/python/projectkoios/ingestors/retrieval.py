from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from projectkoios.ingestors.index import GraphIndex, Section


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
    def retrieve(self, index: GraphIndex, query: str, *, depth: int = 1, limit: int = 3) -> RetrievalResult:
        terms = self._terms(query)
        ranked = sorted(
            (self._score(section, terms) for section in index.sections),
            key=lambda item: (-item[0], item[1].relative_path, item[1].line_start),
        )
        evidence: list[Evidence] = []
        seen: set[tuple[Path, int, int]] = set()
        for score, section in ranked:
            if score <= 0:
                continue
            for neighbour in self._expand(index.sections, section, depth=depth):
                key = (neighbour.path, neighbour.line_start, neighbour.line_end)
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
                        excerpt=self._excerpt(neighbour.text),
                        score=score,
                    )
                )
                if len(evidence) >= limit:
                    return RetrievalResult(query=query, depth=depth, evidence=tuple(evidence))
        return RetrievalResult(query=query, depth=depth, evidence=tuple(evidence))

    def _terms(self, query: str) -> tuple[str, ...]:
        words = [word.strip(".,:;!?()[]{}\"'` ").lower() for word in query.split()]
        return tuple(word for word in words if word)

    def _score(self, section: Section, terms: tuple[str, ...]) -> tuple[int, Section]:
        haystack = f"{section.title}\n{section.text}".lower()
        score = sum(2 for term in terms if term in section.title.lower())
        score += sum(1 for term in terms if term in haystack)
        return (score, section)

    def _expand(self, sections: Iterable[Section], target: Section, *, depth: int) -> tuple[Section, ...]:
        group = [section for section in sections if section.relative_path == target.relative_path]
        if not group:
            return (target,)
        group = sorted(group, key=lambda section: section.line_start)
        index = group.index(target)
        left = max(0, index - (depth - 1))
        right = min(len(group), index + depth)
        return tuple(group[left:right])

    def _excerpt(self, text: str, width: int = 280) -> str:
        compact = " ".join(text.split())
        if len(compact) <= width:
            return compact
        return compact[: width - 1] + "…"
