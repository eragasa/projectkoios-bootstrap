from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from projectkoios.ingestors.sources import SourceDocument, SourceSet


@dataclass(frozen=True, slots=True)
class Section:
    path: Path
    relative_path: str
    title: str
    heading_level: int
    line_start: int
    line_end: int
    text: str


@dataclass(frozen=True, slots=True)
class DocumentIndex:
    document: SourceDocument
    sections: tuple[Section, ...]


@dataclass(frozen=True, slots=True)
class GraphIndex:
    root: Path
    documents: tuple[DocumentIndex, ...]

    @property
    def sections(self) -> tuple[Section, ...]:
        return tuple(section for document in self.documents for section in document.sections)


class GraphIndexBuilder:
    def build(self, source_set: SourceSet) -> GraphIndex:
        documents: tuple[DocumentIndex, ...] = tuple(
            DocumentIndex(document=document, sections=self.sections_for(document))
            for document in source_set.documents
        )
        return GraphIndex(root=source_set.root, documents=documents)

    def sections_for(self, document: SourceDocument) -> tuple[Section, ...]:
        lines: list[str] = document.text.splitlines()
        headings: list[tuple[int, int, str]] = []
        index: int
        line: str
        for index, line in enumerate(lines, start=1):
            stripped: str = line.lstrip()
            if not stripped.startswith("#"):
                continue
            level: int = len(stripped) - len(stripped.lstrip("#"))
            title: str = stripped[level:].strip()
            if title:
                headings.append((index, level, title))
        if not headings:
            return (
                Section(
                    path=document.path,
                    relative_path=document.relative_path,
                    title=document.path.stem,
                    heading_level=0,
                    line_start=1,
                    line_end=max(document.line_count, 1),
                    text=document.text,
                ),
            )

        sections: list[Section] = []
        position: int
        heading: tuple[int, int, str]
        for position, heading in enumerate(headings):
            line_start: int = heading[0]
            heading_level: int = heading[1]
            heading_title: str = heading[2]
            next_start: int = headings[position + 1][0] if position + 1 < len(headings) else len(lines) + 1
            section_lines: list[str] = lines[line_start - 1 : next_start - 1]
            sections.append(
                Section(
                    path=document.path,
                    relative_path=document.relative_path,
                    title=heading_title,
                    heading_level=heading_level,
                    line_start=line_start,
                    line_end=max(next_start - 1, line_start),
                    text="\n".join(section_lines).strip(),
                )
            )
        return tuple(sections)
