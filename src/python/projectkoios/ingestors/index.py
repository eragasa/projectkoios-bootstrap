from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import TypeAlias

from projectkoios.ingestors.sources import SourceDocument, SourceSet


JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]


@dataclass(frozen=True, slots=True)
class Section:
    """Indexed section extracted from one source document.

    Args:
        path: Absolute source path.
        relative_path: Repository-relative source path.
        title: Section title.
        heading_level: Markdown heading level, or zero for whole-document fallback.
        line_start: First source line in the section.
        line_end: Last source line in the section.
        text: Section text.
        page: Optional page number for citation-style sources.
        bibtex_key: Optional BibTeX key for citation-style sources.
    """

    path: Path
    relative_path: str
    title: str
    heading_level: int
    line_start: int
    line_end: int
    text: str
    page: int | None = None
    bibtex_key: str | None = None

    @property
    def citation(self) -> str:
        """Return a source-line citation for this section."""
        return f"{self.relative_path}:{self.line_start}-{self.line_end}"


@dataclass(frozen=True, slots=True)
class DocumentIndex:
    """Index entries for one source document.

    Args:
        document: Source document represented by this index entry.
        sections: Sections extracted from the document.
    """

    document: SourceDocument
    sections: tuple[Section, ...]


@dataclass(frozen=True, slots=True)
class GraphIndex:
    """In-memory GraphRAG index over source documents.

    Args:
        root: Source root for the index.
        documents: Indexed documents.
    """

    root: Path
    documents: tuple[DocumentIndex, ...]

    @property
    def sections(self) -> tuple[Section, ...]:
        """Return every section across every indexed document."""
        return tuple(section for document in self.documents for section in document.sections)


class GraphIndexJsonSerializer:
    """Serialize graph indexes to deterministic JSON."""

    def document(self, document_index: DocumentIndex) -> JsonObject:
        """Return a JSON-compatible object for one document index."""
        return {
            "path": str(document_index.document.path),
            "relative_path": document_index.document.relative_path,
            "sections": [self.section(section) for section in document_index.sections],
        }

    def section(self, section: Section) -> JsonObject:
        """Return a JSON-compatible object for one section."""
        return {
            "bibtex_key": section.bibtex_key,
            "citation": section.citation,
            "evidence": section.text,
            "heading_level": section.heading_level,
            "line_end": section.line_end,
            "line_start": section.line_start,
            "page": section.page,
            "path": str(section.path),
            "relative_path": section.relative_path,
            "title": section.title,
        }

    def to_dict(self, index: GraphIndex) -> JsonObject:
        """Return a JSON-compatible dictionary for a graph index."""
        return {
            "documents": [self.document(document) for document in index.documents],
            "root": str(index.root),
            "version": 1,
        }

    def to_json(self, index: GraphIndex) -> str:
        """Return deterministic serialized JSON for a graph index."""
        return json.dumps(self.to_dict(index), ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    def write(self, index: GraphIndex, path: Path) -> None:
        """Write a graph index JSON artifact to disk."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_json(index), encoding="utf-8")


class GraphIndexBuilder:
    """Build a graph index from resolved source documents."""

    def build(self, source_set: SourceSet) -> GraphIndex:
        """Build an index from a source set.

        Args:
            source_set: Resolved source documents.

        Returns:
            Graph index containing per-document sections.
        """

        # Documents contains one document index per resolved source document.
        documents: tuple[DocumentIndex, ...] = tuple(
            DocumentIndex(document=document, sections=self.sections_for(document))
            for document in source_set.documents
        )
        return GraphIndex(root=source_set.root, documents=documents)

    def sections_for(self, document: SourceDocument) -> tuple[Section, ...]:
        """Extract Markdown-heading sections for one source document.

        Args:
            document: Source document to split into sections.

        Returns:
            Extracted sections, or one whole-document section when no headings exist.
        """

        # Lines are the source document split for heading and section boundaries.
        lines: list[str] = document.text.splitlines()
        # Headings stores tuples of line number, heading level, and heading title.
        headings: list[tuple[int, int, str]] = []
        index: int
        line: str
        for index, line in enumerate(lines, start=1):
            # Stripped removes indentation before Markdown heading detection.
            stripped: str = line.lstrip()
            if not stripped.startswith("#"):
                continue
            # Level counts leading Markdown heading markers.
            level: int = len(stripped) - len(stripped.lstrip("#"))
            # Title is the human-readable heading text after markers.
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

        # Sections accumulates extracted heading-bounded document sections.
        sections: list[Section] = []
        position: int
        heading: tuple[int, int, str]
        for position, heading in enumerate(headings):
            # Line start is the heading line that begins this section.
            line_start: int = heading[0]
            # Heading level is the Markdown depth for this section.
            heading_level: int = heading[1]
            # Heading title is the section title stored in the index.
            heading_title: str = heading[2]
            # Next start is the following heading line or one past document end.
            next_start: int = headings[position + 1][0] if position + 1 < len(headings) else len(lines) + 1
            # Section lines are the source lines covered by this section.
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
